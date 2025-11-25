# ---------------------------------------------------
# MÉTODOS DE INTERPOLAÇÃO
# Lagrange, 
# Diferenças Divididas (Newton),
# Diferenças Finitas (Gregory-Newton)
# ---------------------------------------------------

# LAGRANGE
def lagrange(x, y, xp):
    n = len(x)
    ops = 0
    yp = 0.0

    for i in range(n):
        L = 1.0
        for j in range(n):
            if j != i:
                L *= (xp - x[j]) / (x[i] - x[j])
                ops += 2  # multiplicação + divisão
        yp += L * y[i]
        ops += 1  # multiplicação final

    return yp, ops


# DIFERENÇAS DIVIDIDAS (NEWTON)
def newton_dd(x, y, xp):
    n = len(x)
    ops = 0

    # Tabela de diferenças divididas
    dd = [[0]*n for _ in range(n)]
    for i in range(n):
        dd[i][0] = y[i]

    for j in range(1, n):
        for i in range(n-j):
            dd[i][j] = (dd[i+1][j-1] - dd[i][j-1]) / (x[i+j] - x[i])
            ops += 2

    # Avaliação do polinômio de Newton
    yp = dd[0][0]
    prod = 1.0

    for k in range(1, n):
        prod *= (xp - x[k-1])
        ops += 1
        yp += dd[0][k] * prod
        ops += 1

    return yp, ops


# DIFERENÇAS FINITAS (GREGORY-NEWTON)
def gregory_newton(x, y, xp):
    n = len(x)
    ops = 0

    h = x[1] - x[0]
    t = (xp - x[0]) / h
    ops += 2

    # Verificação de espaçamento uniforme 
    for i in range(1, n):
        if abs((x[i] - x[i-1]) - h) > 1e-9:
            raise ValueError("Gregory-Newton requer pontos igualmente espaçados.")

    # tabela de diferenças finitas
    df = [y[:]]
    for k in range(1, n):
        linha = []
        for i in range(n-k):
            linha.append(df[k-1][i+1] - df[k-1][i])
            ops += 1
        df.append(linha)

    # avaliação
    yp = y[0]
    prod = 1

    for k in range(1, n):
        prod *= (t - (k-1))
        ops += 1
        yp += (df[k][0] * prod) / factorial(k)
        ops += 2

    return yp, ops


def factorial(n):
    f = 1
    for i in range(1, n+1):
        f *= i
    return f


# FUNÇÃO PARA LER PONTOS
def ler_pontos(n):
    x = list(map(float, input("\nDigite os valores de x (separe por espaço): ").split()))
    if len(x) != n:
        raise ValueError("Quantidade incorreta de valores de x.")

    y = list(map(float, input("Digite os valores de y (separe por espaço): ").split()))
    if len(y) != n:
        raise ValueError("Quantidade incorreta de valores de y.")

    return x, y


def main():
    print("\n=== INTERPOLAÇÃO NUMÉRICA ===")
    print("Métodos disponíveis:")
    print("1 - Lagrange")
    print("2 - Diferenças Divididas (Newton)")
    print("3 - Diferenças Finitas (Gregory-Newton)")

    metodo = input("\nEscolha o método (1-3): ").strip()

    n = int(input("\nDigite o número de pontos (n): "))
    x, y = ler_pontos(n)

    xp = float(input("\nDigite o valor de x para interpolar: "))

    print("\nProcessando...")

    if metodo == "1":
        yp, ops = lagrange(x, y, xp)
    elif metodo == "2":
        yp, ops = newton_dd(x, y, xp)
    elif metodo == "3":
        yp, ops = gregory_newton(x, y, xp)
    else:
        print("Método inválido.")
        return

    print("\nResultado:")
    print(f"f({xp}) = {yp:.4f}")

    print(f"\nOperações realizadas: {ops}")


if __name__ == "__main__":
    main()
