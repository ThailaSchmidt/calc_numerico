'''
Método de Gauss;
Método de Jordan;
Método de Jacobi;
Método de Gauss-Seidel.

& C:/Users/thail/AppData/Local/Microsoft/WindowsApps/python3.11.exe c:/Users/thail/OneDrive/Documentos/calc_num/lineares.py
'''

# --------------------------------------------
# MÉTODO DE GAUSS
# --------------------------------------------
def gauss(A, b):
    # Copiar para não alterar os originais
    A = [row[:] for row in A]
    b = b[:]

    n = len(b)

    ops = 0

    # Eliminação para frente
    for k in range(n):
        if A[k][k] == 0:
            raise ValueError("Pivô zero encontrado durante a eliminação.")

        for i in range(k + 1, n):
            fator = A[i][k] / A[k][k]
            ops += 1
            for j in range(k, n):
                A[i][j] -= fator * A[k][j]
                ops += 1
            b[i] -= fator * b[k]
            ops += 1

    # Substituição para trás
    x = [0] * n
    for i in range(n - 1, -1, -1):
        soma = sum(A[i][j] * x[j] for j in range(i + 1, n))
        ops += (n - i)
        x[i] = (b[i] - soma) / A[i][i]
        ops += 1

    return x, ops


# MÉTODO DE JORDAN
def jordan(A, b):
    A = [row[:] for row in A]
    b = b[:]

    n = len(b)

    ops = 0

    for k in range(n):
        piv = A[k][k]
        if piv == 0:
            raise ValueError("Pivô zero encontrado no método de Jordan.")

        # Tornar pivô = 1
        for j in range(n):
            A[k][j] /= piv
            ops += 1
        b[k] /= piv
        ops += 1

        for i in range(n):
            if i != k:
                fator = A[i][k]
                for j in range(k, n):
                    A[i][j] -= fator * A[k][j]
                    ops += 1
                b[i] -= fator * b[k]
                ops += 1

    return b, ops


# MÉTODO DE JACOBI
def jacobi(A, b, x0=None, eps=1e-10, max_iter=100):
    n = len(b)
    x = x0[:] if x0 else [0] * n
    ops = 0

    for _ in range(max_iter):
        x_new = [0] * n
        for i in range(n):
            if A[i][i] == 0:
                raise ValueError("Pivô zero encontrado no Jacobi.")

            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            ops += 2*(n-1)  # multiplicações e somas
            x_new[i] = (b[i] - soma) / A[i][i]
            ops += 1

        if all(abs(x_new[i] - x[i]) < eps for i in range(n)):
            return x_new, ops

        x = x_new

    raise ValueError("Jacobi não convergiu.")


# MÉTODO DE GAUSS-SEIDEL
def gauss_seidel(A, b, x0=None, eps=1e-10, max_iter=100):
    n = len(b)
    x = x0[:] if x0 else [0] * n
    ops = 0

    for it in range(1, max_iter + 1):
        x_old = x[:]

        for i in range(n):
            if A[i][i] == 0:
                raise ValueError("Pivô zero encontrado no Gauss-Seidel.")

            soma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            ops += n

            x[i] = (b[i] - soma) / A[i][i]
            ops += 1

        if all(abs(x[i] - x_old[i]) < eps for i in range(n)):
            return x, it

    raise ValueError("Gauss-Seidel não convergiu.")


# FUNÇÃO PARA LER MATRIZ
def ler_matriz(n):
    A = []
    print(f"\nDigite os {n} elementos de cada linha da matriz A:")
    for i in range(n):
        linha = list(map(float, input(f"Linha {i+1}: ").split()))
        if len(linha) != n:
            raise ValueError("Número de elementos incorreto.")
        A.append(linha)
    return A


def main():
    print("\n=== RESOLUÇÃO DE SISTEMAS LINEARES ===")
    print("Métodos disponíveis:")
    print("1 - Gauss")
    print("2 - Jordan")
    print("3 - Jacobi")
    print("4 - Gauss-Seidel")

    metodo = input("\nEscolha o método (1-4): ").strip()

    n = int(input("\nDigite a ordem da matriz (n): "))
    A = ler_matriz(n)

    b = list(map(float, input("\nDigite o vetor b (separe por espaço): ").split()))
    if len(b) != n:
        raise ValueError("Tamanho do vetor b incorreto.")

    print("\nProcessando...")

    if metodo == "1":
        sol, ops = gauss(A, b)
    elif metodo == "2":
        sol, ops = jordan(A, b)
    elif metodo == "3":
        sol, ops = jacobi(A, b)
    elif metodo == "4":
        sol, ops = gauss_seidel(A, b)
    else:
        print("Método inválido.")
        return

    print("\nSolução encontrada:")
    for i, xi in enumerate(sol):
        print(f"x[{i}] = {xi:.4f}")

    print(f"\nOperações/Iterações: {ops}")


if __name__ == "__main__":
    main()
