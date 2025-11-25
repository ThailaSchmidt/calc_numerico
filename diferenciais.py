import numpy as np
import matplotlib.pyplot as plt
import math


# ====================================================
# MÉTODOS DE PVI
# ====================================================

# Euler
def euler(f, x0, y0, h, n):
    xs = [x0]
    ys = [y0]

    x = x0
    y = y0

    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
        xs.append(x)
        ys.append(y)

    return xs, ys


# Runge-Kutta 2 (Heun)
def rk2(f, x0, y0, h, n):
    xs = [x0]
    ys = [y0]

    x = x0
    y = y0

    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h, y + h * k1)
        y = y + (h/2)*(k1 + k2)
        x = x + h
        xs.append(x)
        ys.append(y)

    return xs, ys


# Runge-Kutta 4
def rk4(f, x0, y0, h, n):
    xs = [x0]
    ys = [y0]

    x = x0
    y = y0

    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h/2, y + h*k1/2)
        k3 = f(x + h/2, y + h*k2/2)
        k4 = f(x + h, y + h*k3)
        y = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        x = x + h
        xs.append(x)
        ys.append(y)

    return xs, ys


# ====================================================
# PVI por Diferenças Finitas (aproxima y')
# dy/dx = f(x,y)
# y0 dado — usa Euler implícito simples (retroativo)
# ====================================================
def pvi_diferencas_finitas(f, x0, y0, h, n):
    xs = [x0 + i*h for i in range(n+1)]
    ys = [0]*(n+1)
    ys[0] = y0

    for i in range(1, n+1):
        ys[i] = ys[i-1] + h * f(xs[i], ys[i-1])

    return xs, ys


# ====================================================
# PVC por Diferenças Finitas
# y'' = g(x)
# y(a)=ya, y(b)=yb
# método clássico de malha tridiagonal
# ====================================================
def pvc_diferencas_finitas(g, a, b, ya, yb, n):
    h = (b - a) / n

    A = np.zeros((n-1, n-1))
    B = np.zeros(n-1)

    for i in range(1, n):
        A[i-1][i-1] = -2
        if i > 1:
            A[i-1][i-2] = 1
        if i < n-1:
            A[i-1][i] = 1
        B[i-1] = -h*h * g(a + i*h)

    # Ajusta condições de fronteira
    B[0] -= ya
    B[-1] -= yb

    Y = np.linalg.solve(A, B)

    xs = [a + i*h for i in range(n+1)]
    ys = [ya] + list(Y) + [yb]

    return xs, ys


def ler_funcao():
    expr = input("Digite a função: ")

    def f(x, y=None):
        return eval(expr, {"x": x, "y": y, "math": math})
    return f


# Função para PVC (somente g(x))
def ler_funcao_g():
    expr = input("Digite g(x): ")

    def g(x):
        return eval(expr, {"x": x, "math": math})
    return g


# ====================================================
# Gráfico
def plot_result(xs, ys):
    plt.figure(figsize=(8,5))
    plt.plot(xs, ys, marker="o")
    plt.title("Solução Numérica")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n=== EQUAÇÕES DIFERENCIAIS ===")
        print("1 - Método de Euler")
        print("2 - Runge-Kutta de 2ª ordem")
        print("3 - Runge-Kutta de 4ª ordem")
        print("4 - PVI por Diferenças Finitas")
        print("5 - PVC por Diferenças Finitas")
        print("0 - Sair")

        op = input("\nEscolha uma opção: ")

        if op == "0":
            break

        # ---------------------------
        # Métodos de PVI
        # ---------------------------
        if op in ["1","2","3","4"]:
            f = ler_funcao()
            x0 = float(input("x0: "))
            y0 = float(input("y0: "))
            h = float(input("Passo h: "))
            n = int(input("Número de passos n: "))

            if op == "1":
                xs, ys = euler(f, x0, y0, h, n)
            elif op == "2":
                xs, ys = rk2(f, x0, y0, h, n)
            elif op == "3":
                xs, ys = rk4(f, x0, y0, h, n)
            elif op == "4":
                xs, ys = pvi_diferencas_finitas(f, x0, y0, h, n)

            print("\nCálculo concluído.")
            plot_result(xs, ys)

        # ---------------------------
        # Método de PVC
        # ---------------------------
        elif op == "5":
            g = ler_funcao_g()
            a = float(input("a: "))
            b = float(input("b: "))
            ya = float(input("y(a): "))
            yb = float(input("y(b): "))
            n = int(input("Número de subdivisões n: "))

            xs, ys = pvc_diferencas_finitas(g, a, b, ya, yb, n)
            print("\nCálculo concluído.")
            plot_result(xs, ys)

        else:
            print("Opção inválida!")



if __name__ == "__main__":
    main()
