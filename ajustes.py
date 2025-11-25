# ---------------------------------------------------
# MÉTODOS DE AJUSTE DE CURVAS (com gráficos)
# Ajuste Linear Simples
# Ajuste Linear Múltiplo
# Ajuste Polinomial
# ---------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# AJUSTE LINEAR SIMPLES (Y = aX + b)
def ajuste_linear(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    n = len(x)

    sx = np.sum(x)
    sy = np.sum(y)
    sxy = np.sum(x*y)
    sx2 = np.sum(x*x)

    a = (n*sxy - sx*sy) / (n*sx2 - sx*sx)
    b = (sy - a*sx) / n

    return a, b


# Mostrar gráfico do ajuste linear simples
def grafico_ajuste_linear(x, y, a, b):
    xp = np.linspace(min(x), max(x), 200)
    yp = a * xp + b

    plt.figure()
    plt.scatter(x, y, label="Pontos", color="blue")
    plt.plot(xp, yp, label=f"y = {a:.4f}x + {b:.4f}", color="red")
    plt.title("Ajuste Linear")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()


# AJUSTE LINEAR MÚLTIPLO
def ajuste_linear_multiplo(X, y):
    X = np.array(X, dtype=float)
    y = np.array(y, dtype=float)

    ones = np.ones((X.shape[0], 1))
    X_aug = np.hstack((X, ones))

    coef = np.linalg.inv(X_aug.T @ X_aug) @ (X_aug.T @ y)
    return coef


# Gráfico para ajuste múltiplo: apenas até 2 variáveis
def grafico_ajuste_linear_multiplo(X, y, coef):
    X = np.array(X)
    y = np.array(y)

    m = X.shape[1]

    # Caso 1: X tem 1 variável → mesma coisa que ajuste linear simples
    if m == 1:
        a = coef[0]
        b = coef[1]
        grafico_ajuste_linear(X[:,0], y, a, b)
        return

    # Caso 2: X tem 2 variáveis → gráfico 3D
    if m == 2:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        x1 = X[:, 0]
        x2 = X[:, 1]

        # Plano
        x1g, x2g = np.meshgrid(
            np.linspace(min(x1), max(x1), 20),
            np.linspace(min(x2), max(x2), 20)
        )
        yg = coef[0]*x1g + coef[1]*x2g + coef[2]

        ax.scatter(x1, x2, y, color="blue", label="Pontos")
        ax.plot_surface(x1g, x2g, yg, color="red", alpha=0.6)

        ax.set_title("Ajuste Linear Múltiplo (Plano)")
        ax.set_xlabel("X1")
        ax.set_ylabel("X2")
        ax.set_zlabel("y")
        plt.show()


# AJUSTE POLINOMIAL
def ajuste_polinomial(x, y, grau):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)

    V = np.vander(x, grau+1, increasing=True)
    coef = np.linalg.inv(V.T @ V) @ (V.T @ y)

    return coef


# Mostrar gráfico polinomial
def grafico_ajuste_polinomial(x, y, coef):
    xp = np.linspace(min(x), max(x), 300)
    yp = sum(c * xp**i for i, c in enumerate(coef))

    plt.figure()
    plt.scatter(x, y, label="Pontos", color="blue")
    plt.plot(xp, yp, label="Polinômio Ajustado", color="red")
    plt.title("Ajuste Polinomial")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()


# LEITURA DE PONTOS
def ler_pontos_simples():
    x = list(map(float, input("\nDigite os valores de x: ").split()))
    y = list(map(float, input("Digite os valores de y: ").split()))
    if len(x) != len(y):
        raise ValueError("x e y devem ter o mesmo tamanho.")
    return x, y


def ler_matriz_features(n, m):
    print("\nDigite os valores das variáveis independentes (X1 X2 ... Xm) por linha:")
    X = []
    for i in range(n):
        linha = list(map(float, input(f"Linha {i+1}: ").split()))
        if len(linha) != m:
            raise ValueError("Valores insuficientes.")
        X.append(linha)
    return X


def main():
    print("\n=== AJUSTE DE CURVAS ===")
    print("1 - Ajuste Linear Simples")
    print("2 - Ajuste Linear Múltiplo")
    print("3 - Ajuste Polinomial")

    metodo = input("\nEscolha o método (1-3): ").strip()

    # ==============================
    # 1. AJUSTE LINEAR
    # ==============================
    if metodo == "1":
        x, y = ler_pontos_simples()
        a, b = ajuste_linear(x, y)

        print(f"\nEquação ajustada: y = {a:.4f}x + {b:.4f}")

        # gráfico automático
        grafico_ajuste_linear(x, y, a, b)

    # ==============================
    # 2. AJUSTE MÚLTIPLO
    # ==============================
    elif metodo == "2":
        n = int(input("Número de pontos (n): "))
        m = int(input("Número de variáveis independentes (m): "))

        X = ler_matriz_features(n, m)
        y = list(map(float, input("\nDigite os valores de y: ").split()))

        coef = ajuste_linear_multiplo(X, y)

        print("\nCoeficientes:")
        for i, c in enumerate(coef):
            print(f"a{i} = {c:.4f}")

        grafico_ajuste_linear_multiplo(X, y, coef)

    # ==============================
    # 3. AJUSTE POLINOMIAL
    # ==============================
    elif metodo == "3":
        x, y = ler_pontos_simples()
        grau = int(input("Grau do polinômio: "))

        coef = ajuste_polinomial(x, y, grau)

        print("\nCoeficientes:")
        for i, c in enumerate(coef):
            print(f"c{i} = {c:.4f}")

        grafico_ajuste_polinomial(x, y, coef)

    else:
        print("Método inválido.")


if __name__ == "__main__":
    main()
