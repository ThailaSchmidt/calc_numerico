import math
import numpy as np
import matplotlib.pyplot as plt

# MÉTODO DOS TRAPÉZIOS (composto)
def trapezios(f, a, b, n):
    h = (b - a) / n
    soma = f(a) + f(b)
    for i in range(1, n):
        soma += 2 * f(a + i*h)
    return (h/2) * soma


# MÉTODO DE SIMPSON 1/3 (composto)
def simpson(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n deve ser par para Simpson.")
    
    h = (b - a) / n
    soma = f(a) + f(b)

    for i in range(1, n):
        x = a + i*h
        if i % 2 == 0:
            soma += 2 * f(x)
        else:
            soma += 4 * f(x)

    return (h/3) * soma



def ler_funcao():
    expr = input("Digite a função f(x): ")

    def f(x):
        return eval(expr, {"x": x, "math": math})
    
    return f


# GRÁFICO 
def plot_integral(f, a, b):
    x = np.linspace(a, b, 400)
    y = [f(xi) for xi in x]

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label="f(x)")
    plt.fill_between(x, y, alpha=0.3, color="orange", label="Área integrada")
    
    plt.title("Integração Numérica")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    while True:
        print("\n--- MÉTODOS DE INTEGRAÇÃO NUMÉRICA ---")
        print("1 - Método dos Trapézios")
        print("2 - Método de Simpson 1/3")
        print("0 - Sair")

        opc = input("Escolha uma opção: ")

        if opc == "0":
            print("Saindo...")
            break

        f = ler_funcao()
        a = float(input("Digite o limite inferior a: "))
        b = float(input("Digite o limite superior b: "))
        n = int(input("Digite o número de subdivisões n: "))

        try:
            if opc == "1":
                resultado = trapezios(f, a, b, n)
                print(f"\nResultado pelo Método dos Trapézios: {resultado}")

            elif opc == "2":
                resultado = simpson(f, a, b, n)
                print(f"\nResultado pelo Método de Simpson: {resultado}")

            else:
                print("Opção inválida!")
                continue

            # gráfico automático
            plot_integral(f, a, b)

        except Exception as e:
            print("Erro:", e)


if __name__ == "__main__":
    main()
