# Importar as bibliotecas necessárias
import matplotlib.pyplot as plt
import pandas as pd
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Ler o arquivo excel e armazenar os dados em um DataFrame
df = pd.read_excel("resultados.xlsx", sheet_name="mega-sena", index_col="Concurso", header=0, usecols=["Concurso", "Coluna1", "Coluna2", "Coluna3", "Coluna4", "Coluna5", "Coluna6"])
print(df)

# Remover as linhas duplicadas com base em todas as colunas e manter a primeira entrada
df = df.drop_duplicates(keep='first')

# Transformar o dataframe em uma série única
serie = df.stack()
print(serie)

# Contar a frequência de cada valor na série
frequencia = serie.value_counts()
print(frequencia)

# Obter os 12 valores mais frequentes e armazená-los em uma lista
lista_mais = frequencia.head(12).index.tolist()

# Obter os 12 valores menos frequentes e armazená-los em uma lista
lista_menos = frequencia.tail(12).index.tolist()

# Criar uma função que sorteia uma combinação de números de acordo com a opção escolhida pelo usuário
def sortear():
    # Obter a opção escolhida pelo usuário usando o método get do objeto IntVar
    opcao = var.get()
    
    # Verificar qual opção foi escolhida e executar o código correspondente
    if opcao == 1:
        # Sortear uma combinação de 6 números da lista mais e ordená-los em ordem crescente
        numeros_sorteio = random.sample(lista_mais, 6)
        numeros_sorteio.sort()
        
    elif opcao == 2:
        # Sortear uma combinação de 6 números da lista menos e ordená-los em ordem crescente
        numeros_sorteio = random.sample(lista_menos, 6)
        numeros_sorteio.sort()
        
    else:
        # Sortear uma combinação de 6 números entre 1 e 60 e ordená-los em ordem crescente
        numeros_sorteio = random.sample(range(1,61),6)
        numeros_sorteio.sort()
        
    # Comparar a combinação sorteada com os resultados dos concursos anteriores usando o método equals do pandas
    
    # Cria um dataframe com a lista numeros_sorteio
    sorteio_df = pd.DataFrame([numeros_sorteio], columns=df.columns)
    
    # Compara o dataframe sorteio_df com cada linha do dataframe df usando o método equals
    equals = df.apply(lambda x: sorteio_df.equals(x.to_frame().T), axis=1)
    
    # Verifica se há alguma linha igual ao dataframe sorteio_df e mostra uma mensagem na tela usando o método showinfo do messagebox
    if equals.any():
        messagebox.showinfo("Resultado", "Essa combinação já foi sorteada antes no concurso {}\nA combinação sorteada foi: {}".format(df[equals].iloc[0,0], numeros_sorteio))
    else:
        messagebox.showinfo("Resultado", "Essa combinação é inédita!\nA combinação sorteada foi: {}".format(numeros_sorteio))

# Criar uma função que plota um gráfico de barras com a frequência dos números da Mega-Sena
def plotar():
# Criar uma figura e um eixo usando o método subplots do matplotlib.pyplot
    fig, ax = plt.subplots()

    # Plotar um gráfico de barras usando o método bar do objeto eixo, passando os valores da série frequencia como argumentos
    bars = ax.bar(frequencia.index, frequencia.values) # guardar o BarContainer em uma variável

    # Adicionar um título ao gráfico usando o método set_title do objeto eixo
    ax.set_title("Frequência dos números da Mega-Sena")

    # Adicionar um rótulo ao eixo x usando o método set_xlabel do objeto eixo
    ax.set_xlabel("Números")

    # Adicionar um rótulo ao eixo y usando o método set_ylabel do objeto eixo
    ax.set_ylabel("Frequência")

    # Adicionar rótulos às barras usando o método bar_label do objeto eixo, passando o BarContainer como argumento
    ax.bar_label(bars, rotation=90)

    # Definir os valores do eixo x usando o método xticks do matplotlib.pyplot, passando os índices da série frequencia como argumento
    plt.xticks(frequencia.index, rotation=90)

    # Mostrar o gráfico na tela usando o método show do matplotlib.pyplot
    plt.show()

# Criar uma janela principal usando o tkinter
window = tk.Tk()

# Obter a largura e a altura da tela
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Definir a largura e a altura da janela
window_width = 500
window_height = 250

# Calcular a posição x e y da janela
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Definir a geometria da janela usando o atributo geometry do objeto window
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Adicionar um título à janela usando o atributo title do objeto window
window.title("Sorteio da Mega-Sena")

# Adicionar um texto explicativo usando o widget Label do tkinter e posicioná-lo na janela usando o método pack 
label = tk.Label(window, text="\nVezes em que um numero foi sorteado!")
label.pack()

# Adicionar outro botão para executar a função plotar usando o widget Button do tkinter e posicioná-lo na janela usando o método pack
botao1 = tk.Button(window, text="Plotar Gráfico", command=plotar)
botao1.pack()

# Adicionar um texto explicativo usando o widget Label do tkinter e posicioná-lo na janela usando o método pack 
label = tk.Label(window, text="\nEscolha uma opção de sorteio:", anchor='w')
label.pack(fill='both')

# Criar um objeto IntVar para armazenar a opção escolhida pelo usuário usando os widgets Radiobutton do tkinter 
var = tk.IntVar(value=3)

# Criar uma função para criar os widgets Radiobutton com as opções de sorteio e posicioná-los na janela usando o método pack 
def criar_radio(texto, valor):
    radio = tk.Radiobutton(window, text=texto, variable=var, value=valor, anchor='w')
    radio.pack(fill='both')

# Criar três widgets Radiobutton com as opções de sorteio usando a função criar_radio 
criar_radio("Com apenas 12 números que mais aparecem: {}".format(lista_mais), 1)
criar_radio("Com apenas 12 números que menos aparecem: {}".format(lista_menos), 2)
criar_radio("Com qualquer número entre 1 e 60", 3)

# Adicionar um botão para executar a função sortear usando o widget Button do tkinter e posicioná-lo na janela usando o método pack
botao2 = tk.Button(window, text="Sortear", command=sortear)
botao2.pack()

# Adicionar um texto explicativo usando o widget Label do tkinter e posicioná-lo na janela usando o método pack 
label = tk.Label(window, text="\nSource Coder: Rafael Alonso Baugis")
label.pack()

# Iniciar o loop principal da janela usando o método mainloop do objeto window
window.mainloop()
