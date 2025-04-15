# %%
#Automação Python - Preço Médio

# %%
import pdfplumber
import pandas as pd
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Função para extrair informações com data do pregão
def extrair_informacoes_com_data(pdf_path):
    informacoes_extracao = []

    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            linhas = texto.split('\n')

            # Buscar data do pregão na página
            data_pregao = None
            for i, linha in enumerate(linhas):
                if "Data pregão" in linha:
                    for j in range(1, 5):
                        if i + j < len(linhas):
                            data_match = re.search(r"\d{2}/\d{2}/\d{4}", linhas[i + j])
                            if data_match:
                                data_pregao = data_match.group(0)
                                break
                    break

            for linha in linhas:
                if "BOVESPA" in linha:
                    partes = linha.split()
                    if len(partes) > 2:
                        operacao_coluna = partes[1]
                        if operacao_coluna == "C":
                            operacao = 'Compra'
                        elif operacao_coluna == "V":
                            operacao = 'Venda'
                        else:
                            continue

                        especificacoes_titulo = ' '.join(partes[3:-5])
                        try:
                            quantidade = int(partes[-4].replace('.', ''))
                        except ValueError:
                            quantidade = 1

                        try:
                            valor_total = float(partes[-2].replace('.', '').replace(',', '.'))
                        except ValueError:
                            continue

                        valor_unitario = valor_total / quantidade
                        informacoes_extracao.append({
                            'Data do Pregão': data_pregao,
                            'Operação': operacao,
                            'Título': especificacoes_titulo,
                            'Quantidade': quantidade,
                            'Valor Total': valor_total,
                            'Valor Unitário': valor_unitario
                        })

    return informacoes_extracao

# Função para criar planilha com duas abas
def criar_planilha_com_abas(df_notas, df_preco_medio, nome_arquivo):
    with pd.ExcelWriter(nome_arquivo) as writer:
        df_notas.to_excel(writer, sheet_name='Notas de Negociação', index=False)
        df_preco_medio.to_excel(writer, sheet_name='Preço Médio', index=False)

# Função principal que integra tudo
def processar_pdf(pdf_path):
    informacoes = extrair_informacoes_com_data(pdf_path)
    df_notas = pd.DataFrame(informacoes)

    if df_notas.empty:
        messagebox.showerror("Erro", "Nenhuma negociação encontrada no PDF.")
        return

    df_notas['Quantidade_Compras'] = df_notas['Quantidade'].where(df_notas['Operação'] == 'Compra', 0)
    df_notas['Valor_Compras'] = df_notas['Valor Total'].where(df_notas['Operação'] == 'Compra', 0)

    agrupado = df_notas.groupby('Título').agg(
        Quantidade_Atual=('Quantidade', 'sum'),
        Soma_Operacoes=('Valor Total', 'sum'),
        Quantidade_Compras=('Quantidade_Compras', 'sum'),
        Valor_Compras=('Valor_Compras', 'sum')
    ).reset_index()

    agrupado['Preco_Medio_Compras'] = agrupado['Valor_Compras'] / agrupado['Quantidade_Compras']

    nome_excel = os.path.splitext(os.path.basename(pdf_path))[0] + "_preco_medio.xlsx"
    caminho_excel = os.path.join(os.path.dirname(pdf_path), nome_excel)
    criar_planilha_com_abas(df_notas, agrupado, caminho_excel)

    messagebox.showinfo("Sucesso", f"Planilha criada:\n{caminho_excel}")
    os.startfile(caminho_excel)

# Interface gráfica
def iniciar_interface():
    def selecionar_arquivo():
        caminho = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if caminho:
            entrada_pdf.delete(0, tk.END)
            entrada_pdf.insert(0, caminho)

    def executar():
        caminho = entrada_pdf.get()
        if not caminho or not os.path.isfile(caminho):
            messagebox.showerror("Erro", "Caminho do PDF inválido.")
            return
        processar_pdf(caminho)

    janela = tk.Tk()
    janela.title("Automação Preço Médio - Notas de Corretagem")
    janela.geometry("600x150")

    label = tk.Label(janela, text="Caminho do PDF da Nota de Corretagem:")
    label.pack(pady=5)

    entrada_pdf = tk.Entry(janela, width=80)
    entrada_pdf.pack(pady=5)

    btn_selecionar = tk.Button(janela, text="Selecionar Arquivo", command=selecionar_arquivo)
    btn_selecionar.pack(pady=2)

    btn_executar = tk.Button(janela, text="Processar PDF", command=executar, bg="green", fg="white")
    btn_executar.pack(pady=10)

    janela.mainloop()

# Iniciar a interface
iniciar_interface()



