import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from executar import rodar_backtest_via_form

root = ttk.Window()
style = ttk.Style("darkly")
root.geometry("1440x1518")
root.title("VAROS")
root.config(bg = '#131313')

label1 = tk.Label(root, text='CALCULADORA DE MODELOS CÓDIGO.PY')
label1.config(font=('Red Hat Display', 24), bg="#131313", padx=8, pady=16, highlightthickness = 1, highlightbackground = '#39FFD9', fg = '#39FFD9')

label2 = tk.Label(root, text='Dados Gerais')
label2.config(font=('Red Hat Display Bold', 30), fg = '#FFFFFF', bg="#131313")

label3 = tk.Label(root, text='Dia Inicial')
label3.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label4 = tk.Label(root, text='Dia Final')
label4.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label5 = tk.Label(root, text='Duração da carteira')
label5.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label6 = tk.Label(root, text='Corretagem')
label6.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label7 = tk.Label(root, text='Ativos na carteira')
label7.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label8 = tk.Label(root, text='Filtro de liquidez (Em MM)')
label8.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")



#SEÇÃO 2

label9 = tk.Label(root, text='Carteiras')
label9.config(font=('Red Hat Display Bold', 30), fg = '#FFFFFF', bg="#131313")

label10 = tk.Label(root, text='Carteira 1')
label10.config(font=('Red Hat Display', 20), bg="#212946", padx=16, pady=16, fg = '#FFFFFF')

label11 = tk.Label(root, text='Carteira 2                     ')
label11.config(font=('Red Hat Display', 20), bg="#212946", padx=16, pady=16, fg = '#FFFFFF')

label12 = tk.Label(root, text='')
label12.config(font=('Red Hat Display', 20), bg="#131313", padx=16, pady=16, fg = '#FFFFFF')

label13 = tk.Label(root, text='Indicador')
label13.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label14 = tk.Label(root, text='Ordem')
label14.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label15 = tk.Label(root, text='Indicador')
label15.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label16 = tk.Label(root, text='Ordem')
label16.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label17 = tk.Label(root, text='Indicador')
label17.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label18 = tk.Label(root, text='Ordem')
label18.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label19 = tk.Label(root, text='Indicador')
label19.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label20 = tk.Label(root, text='Ordem')
label20.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label21 = tk.Label(root, text='Indicador')
label21.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label22 = tk.Label(root, text='Ordem')
label22.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label23 = tk.Label(root, text='Indicador')
label23.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label24 = tk.Label(root, text='Ordem')
label24.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label25 = tk.Label(root, text='Indicador')
label25.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label26 = tk.Label(root, text='Ordem')
label26.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label27 = tk.Label(root, text='Indicador')
label27.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")

label28 = tk.Label(root, text='Ordem')
label28.config(font=('Red Hat Display', 20), fg = '#FFFFFF', bg="#131313")



ttk.Style().configure(style = 'custom.TEntry', bordercolor = '#284741', fieldbackground = '#131516')


input1 = ttk.Entry(style='custom.TEntry')
input2 = ttk.Entry(style='custom.TEntry')
input3 = ttk.Entry(style='custom.TEntry')
input4 = ttk.Entry(style='custom.TEntry')
input5 = ttk.Entry(style='custom.TEntry')
input6 = ttk.Entry(style='custom.TEntry')
input7 = ttk.Entry(style='custom.TEntry')
input8 = ttk.Entry(style='custom.TEntry')
input9 = ttk.Entry(style='custom.TEntry')
input10 = ttk.Entry(style='custom.TEntry')
input11 = ttk.Entry(style='custom.TEntry')
input12 = ttk.Entry(style='custom.TEntry')
input13 = ttk.Entry(style='custom.TEntry')
input14 = ttk.Entry(style='custom.TEntry')
input15 = ttk.Entry(style='custom.TEntry')
input16 = ttk.Entry(style='custom.TEntry')
input17 = ttk.Entry(style='custom.TEntry')
input18 = ttk.Entry(style='custom.TEntry')
input19 = ttk.Entry(style='custom.TEntry')
input20 = ttk.Entry(style='custom.TEntry')
input21 = ttk.Entry(style='custom.TEntry')
input22 = ttk.Entry(style='custom.TEntry')

def rodar_modelo():

    dia_inicial = input1.get()
    dia_final = input2.get()
    duracao_carteira = input3.get()
    corretagem = input4.get()
    ativos = input5.get()
    filtro_liquidez = input6.get()
    indicador1 = input7.get()
    ordem1 = input8.get()
    indicador2 = input9.get()
    ordem2 = input10.get()
    indicador3 = input11.get()
    ordem3 = input12.get()
    indicador4 = input13.get()
    ordem4 = input14.get()
    indicador5 = input15.get()
    ordem5 = input16.get()
    indicador6 = input17.get()
    ordem6 = input18.get()
    indicador7 = input19.get()
    ordem7 = input20.get()
    indicador8 = input21.get()
    ordem8 = input22.get()

    
    estado = rodar_backtest_via_form(dia_inicial, dia_final, duracao_carteira, corretagem, ativos, filtro_liquidez, indicador1, ordem1,
                            indicador2, ordem2, indicador3, ordem3, indicador4, ordem4, indicador5, ordem5, indicador6, ordem6,
                            indicador7, ordem7, indicador8, ordem8)
    
    

    if estado != 'BACKTEST COMPLETO':

        label29 = tk.Label(root, text="ERRO: " + str(estado))
        label29.config(font=('Red Hat Display', 14), fg = '#FFFFFF', bg="#131313")
        root.after(5000, label29.destroy)
        label29.grid(row = 28, column= 4, columnspan= 6)

    else:

        label29 = tk.Label(root, text=estado)
        label29.config(font=('Red Hat Display', 14), fg = '#FFFFFF', bg="#131313")
        root.after(5000, label29.destroy)
        label29.grid(row = 28, column= 4, columnspan= 6)


botao = ttk.Button(text='RODAR MODELO', style='TButton', command =rodar_modelo)

linhas = tuple(range(0, 33))
colunas = tuple(range(0, 18))

root.columnconfigure(colunas, weight = 1)
root.rowconfigure(linhas, weight= 1)


label1.grid(row = 3, column= 3, columnspan= 7, sticky='wn')
label2.grid(row = 5, column= 3, columnspan= 5, sticky='wn')

label3.grid(row = 7, column= 3, columnspan= 4, sticky='wn')
input1.grid(row = 8, column= 3, columnspan= 4, sticky='wns')
label4.grid(row = 7, column= 5, columnspan= 6, sticky='wn')
input2.grid(row = 8, column= 5, columnspan= 6, sticky='wns')


label5.grid(row = 10, column= 3, columnspan= 4, sticky='wn')
input3.grid(row = 11, column= 3, columnspan= 4, sticky='wns')


label6.grid(row = 7, column= 8, columnspan= 9, sticky='wn')
input4.grid(row = 8, column= 8, columnspan= 9, sticky='wns')
label7.grid(row = 7, column= 10, columnspan= 11, sticky='wn')
input5.grid(row = 8, column= 10, columnspan= 11, sticky='wns')


label8.grid(row = 10, column= 8, columnspan= 9, sticky='wn')
input6.grid(row = 11, column= 8, columnspan= 9, sticky='wns')

label9.grid(row = 13, column= 3, columnspan= 5, sticky='wn')

label10.grid(row = 14, column= 3, columnspan= 4, sticky = 'wesn')
label11.grid(row = 14, column= 8, columnspan= 9, sticky = 'wsne')
label12.grid(row = 14, column= 14, columnspan= 14, sticky = 'wsne')

# carteira 1

label13.grid(row = 15, column= 3, columnspan= 4, sticky='w')
input7.grid(row = 16, column= 3, columnspan= 4, sticky='wns')
label14.grid(row = 15, column= 5, columnspan= 6, sticky='w')
input8.grid(row = 16, column= 5, columnspan= 6, sticky='wns')

label15.grid(row = 17, column= 3, columnspan= 4, sticky='w')
input9.grid(row = 18, column= 3, columnspan= 4, sticky='wns')
label16.grid(row = 17, column= 5, columnspan= 6, sticky='w')
input10.grid(row = 18, column= 5, columnspan= 6, sticky='wns')

label17.grid(row = 19, column= 3, columnspan= 4, sticky='w')
input11.grid(row = 20, column= 3, columnspan= 4, sticky='wns')
label18.grid(row = 19, column= 5, columnspan= 6, sticky='w')
input12.grid(row = 20, column= 5, columnspan= 6, sticky='wns')

label19.grid(row = 21, column= 3, columnspan= 4, sticky='w')
input13.grid(row = 22, column= 3, columnspan= 4, sticky='wns')
label20.grid(row = 21, column= 5, columnspan= 6, sticky='w')
input14.grid(row = 22, column= 5, columnspan= 6, sticky='wns')

#carteira 2

label21.grid(row = 15, column= 8, columnspan= 9, sticky='w')
input15.grid(row = 16, column= 8, columnspan= 9, sticky='wns')
label22.grid(row = 15, column= 10, columnspan= 11, sticky='w')
input16.grid(row = 16, column= 10, columnspan= 11, sticky='wns')

label23.grid(row = 17, column= 8, columnspan= 9, sticky='w')
input17.grid(row = 18, column= 8, columnspan= 9, sticky='wns')
label24.grid(row = 17, column= 10, columnspan= 11, sticky='w')
input18.grid(row = 18, column= 10, columnspan= 11, sticky='wns')

label25.grid(row = 19, column= 8, columnspan= 9, sticky='w')
input19.grid(row = 20, column= 8, columnspan= 9, sticky='wns')
label26.grid(row = 19, column= 10, columnspan= 11, sticky='w')
input20.grid(row = 20, column= 10, columnspan= 11, sticky='wns')

label27.grid(row = 21, column= 8, columnspan= 9, sticky='w')
input21.grid(row = 22, column= 8, columnspan= 9, sticky='wns')
label28.grid(row = 21, column= 10, columnspan= 11, sticky='w')
input22.grid(row = 22, column= 10, columnspan= 11, sticky='wns')

botao.grid(row = 26, column= 4, columnspan= 7, sticky='ewns')


root.mainloop()
