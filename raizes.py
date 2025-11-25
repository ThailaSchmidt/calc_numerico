'''
Método da bisseção;
Método das cordas;
Método de Newton;
Método da Secante;

& C:/Users/thail/AppData/Local/Microsoft/WindowsApps/python3.11.exe c:/Users/thail/OneDrive/Documentos/calc_num/raizes.py
'''
import math
import matplotlib.pyplot as plt  # type: ignore # gráfico

#BISSECÇÃO
def bisseccao(f, a, b, eps):
    if f(a) * f(b) > 0:
        raise ValueError("O intervalo não contém mudança de sinal.")

    iteracoes = 0
    while (b - a) / 2 > eps:
        c = (a + b) / 2
        if f(c) == 0: 
            return c, iteracoes
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iteracoes += 1
    return (a + b) / 2, iteracoes

#POSIÇÃO FALSA
def posicao_falsa(f, a, b, eps):
    if f(a) * f(b) > 0:
        raise ValueError("O intervalo não contém mudança de sinal.")

    iteracoes = 0
    while True:
        c = (a * f(b) - b * f(a)) / (f(b) - f(a))
        if abs(f(c)) < eps:
            return c, iteracoes
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        iteracoes += 1

def cordas(f, a, b, eps):
    if f(a) * f(b) > 0:
        raise ValueError("O intervalo não contém mudança de sinal.")

    x0 = a  # ponto inicial
    iteracoes = 0
    while True:
        # ponto de interseção usando b fixo
        x1 = x0 - f(x0) * (b - x0) / (f(b) - f(x0))
        if abs(f(x1)) < eps:
            return x1, iteracoes
        x0 = x1  # move apenas o ponto inicial
        iteracoes += 1

#NEWTON
def newton(f, x0, eps, max_iter=100):
    iteracoes = 0
    x = x0 #chute inicial
    
    while iteracoes < max_iter:
        # derivada aproximada por diferença finita
        h = 1e-8
        f_deriv = (f(x + h) - f(x - h)) / (2 * h)
        
        if f_deriv == 0:
            raise ZeroDivisionError("Derivada é zero. Escolha outro ponto inicial.")
        
        x_new = x - f(x) / f_deriv  # xn+1 = xn - f(xn)/f'(xn)
        
        if abs(x_new - x) < eps:
            return x_new, iteracoes
        
        x = x_new
        iteracoes += 1
    
    raise RuntimeError("Número máximo de iterações atingido.")

#SECANTE
def secante(f, x0, x1, eps, max_iter=100):
    iteracoes = 0
    while iteracoes < max_iter:
        if f(x1) - f(x0) == 0:
            raise ZeroDivisionError("Divisão por zero na secante. Escolha chutes iniciais diferentes.")
        
        x_new = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0))
        
        if abs(x_new - x1) < eps:
            return x_new, iteracoes
        
        x0, x1 = x1, x_new
        iteracoes += 1
    
    raise RuntimeError("Número máximo de iterações atingido.")

def plotar_funcao(f, a, b, raiz, expr):
    x_vals = [a + (b - a) * i / 400 for i in range(401)]
    y_vals = [f(x) for x in x_vals]

    plt.axhline(0, color="black", linewidth=1)
    plt.plot(x_vals, y_vals, label=f"f(x) = {expr}")
    plt.scatter(raiz, f(raiz), color="red", zorder=5, label=f"Raiz ≈ {raiz:.4f}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid()
    plt.title("Método Numérico")
    plt.show()


def main():
    while True:
        expr = input("Digite a função em x (ex: x**3 - 9*x + 3): ") #log= math.log10(x)  ln=math.log(x)
        a = float(input("Digite o limite inferior do intervalo (a): "))
        b = float(input("Digite o limite superior do intervalo (b): "))
        eps = float(input("Digite a tolerância (ex: 1e-3): "))

        metodo = input("Escolha o método 0- bisseccao 1- posição falsa 2- cordas 3- newton 4- secante").strip().lower()

        # Função usando eval
        def f(x):
            return eval(expr, {"x": x, "math": math})

        #calcula a raiz
        try:
            if metodo == "0":
                raiz, it = bisseccao(f, a, b, eps)
            elif metodo == "1":
                raiz, it = posicao_falsa(f, a, b, eps)
            elif metodo == "2":
                raiz, it = cordas(f, a, b, eps)  
            elif metodo == "3":
                x0 = (a + b) / 2  # chute inicial
                raiz, it = newton(f, x0, eps)
            elif metodo == "4":
                x0 = a  # primeiro chute
                x1 = b  # segundo chute
                raiz, it = secante(f, x0, x1, eps)
            else:
                print("Método inválido.")
                continue
            print(f"\nRaiz aproximada: {raiz:.4f} em {it} iterações")
        except ValueError as e:
            print("Erro:", e)
            continue

        # Plota gráfico
        plotar_funcao(f, a, b, raiz, expr)

        outra = input("Deseja calcular outra função? (s/n): ").strip().lower()
        if outra != 's':
            break

if __name__ == "__main__":
    main()
