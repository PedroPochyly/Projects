import requests
import pandas as pd
import os
import urllib.request

class dados_fintz:

    def __init__(self, caminho_dados):
        
        self.chave_api = os.getenv("API_FINTZ")
        self.headers = {'accept': 'application/json',
                        'X-API-Key': self.chave_api}
        os.chdir(caminho_dados)

    def cdi(self):

        response = requests.get('https://api.fintz.com.br/taxas/historico?codigo=12&dataInicio=1994-06-30&ordem=ASC',
                                headers=self.headers)
    
        cdi = pd.DataFrame(response.json())
        cdi = cdi.drop(["dataFim", 'nome'], axis = 1)
        cdi.columns = ['data', 'retorno']
        cdi['retorno'] = cdi['retorno']/100 
        cdi.to_parquet('cdi.parquet', index = False)


    def ibov(self):

        response = requests.get('https://api.fintz.com.br/indices/historico?indice=IBOV&dataInicio=1994-06-30',
                                headers=self.headers)
        df = pd.DataFrame(response.json())
        df = df.sort_values('data', ascending=True)
        df.columns = ['indice', 'data', 'fechamento']
        df = df.drop('indice', axis = 1)
        df.to_parquet('ibov.parquet', index = False)          

    def pegar_cotacoes(self):
        
        
        response = requests.get(f'https://api.fintz.com.br/bolsa/b3/avista/cotacoes/historico/arquivos?classe=ACOES&preencher=true', 
                                headers=self.headers)
        

        link_download = (response.json())['link']
        urllib.request.urlretrieve(link_download, f"cotacoes.parquet")
        df = pd.read_parquet('cotacoes.parquet')
        colunas_pra_ajustar = ['preco_abertura', 'preco_maximo', 'preco_medio', 'preco_minimo']

        for coluna in colunas_pra_ajustar:

            df[f'{coluna}_ajustado'] = df[coluna] * df['fator_ajuste']

        df['preco_fechamento_ajustado'] = df.groupby('ticker')['preco_fechamento_ajustado'].transform('ffill')
        df = df.sort_values('data', ascending=True)
        df.to_parquet('cotacoes.parquet', index = False) 


    def pegando_arquivo_contabil(self, demonstracao = False, bp = False, indicadores = False, nome_dado = ''):

        if demonstracao:

            if bp:

                PARAMS = {'item': nome_dado, 'tipoPeriodo': 'TRIMESTRAL'}

            else:

                PARAMS = {'item': nome_dado, 'tipoPeriodo': '12M'}

            try:

                response = requests.get(f'https://api.fintz.com.br/bolsa/b3/avista/itens-contabeis/point-in-time/arquivos',
                                        headers=self.headers, params=PARAMS)
            
            except:

                print("Demonstração não encontrada!")
                exit()

            link_download = (response.json())['link']
            urllib.request.urlretrieve(link_download, f"{nome_dado}.parquet")

        elif indicadores:

            PARAMS = {'indicador': nome_dado}

            try:

                response = requests.get(f'https://api.fintz.com.br/bolsa/b3/avista/indicadores/point-in-time/arquivos',
                                        headers=self.headers, params=PARAMS)
            
            except:

                print("Indicador não encontrado!")
                exit()

            link_download = (response.json())['link']
            urllib.request.urlretrieve(link_download, f"{nome_dado}.parquet")

        else:

            print("Escolha uma demonstração ou indicador.")


if __name__ == "__main__":

    lendo_dados = dados_fintz(caminho_dados='./dados')

    lendo_dados.pegar_cotacoes()

    itens_contabeis_dre_e_dfc = ['ReceitaLiquida', 'Custos', 'ResultadoBruto', 
                                  'DespesasReceitasOperacionaisOuAdministrativas', 'EBIT', 'ResultadoFinanceiro', 
                                  'ReceitasFinanceiras', 'LAIR', 'Impostos', 'LucroLiquidoOperacoesContinuadas', 
                                  'LucroLiquidoOperacoesDescontinuadas', 'LucroLiquido', 'LucroLiquidoSociosControladora', 
                                  'DepreciacaoAmortizacao', 'EquivalenciaPatrimonial']

    itens_contabais_bp = ['AtivoCirculante', 'AtivoNaoCirculante', 'AtivoTotal', 'CaixaEquivalentes', 'DespesasFinanceiras', 
                           'Disponibilidades', 'DividaBruta', 'DividaLiquida', 'EBITDA', 'PassivoCirculante', 'PassivoNaoCirculante', 
                           'PassivoTotal', 'PatrimonioLiquido']

    lista_indicadores = ['ValorDeMercado', 'EV', 'P_L', 'P_VP', 'VPA', 'LPA', 
                           'DividendYield', 'EV_EBITDA', 'EV_EBIT', 'P_EBITDA', 'P_EBIT', 
                           'P_Ativos', 'P_SR', 'P_CapitalDeGiro', 'P_AtivoCirculanteLiquido', 
                           'ROE', 'ROA', 'ROIC', 'GiroAtivos', 'MargemBruta', 'MargemEBITDA', 
                           'MargemEBIT', 'MargemLiquida', 'DividaLiquida_PatrimonioLiquido', 
                           'DividaLiquida_EBITDA', 'DividaLiquida_EBIT', 'PatrimonioLiquido_Ativos', 
                           'Passivos_Ativos', 'LiquidezCorrente', 'DividaBruta_PatrimonioLiquido', 'EBIT_Ativos',
                             'EBIT_DespesasFinanceiras', 'EBITDA_DespesasFinanceiras', 'EBITDA_EV', 'EBIT_EV', 'L_P']


    for demonstracao in itens_contabeis_dre_e_dfc:

         print(demonstracao)

         lendo_dados.pegando_arquivo_contabil(demonstracao=True, nome_dado = demonstracao, bp = False)

    for demonstracao in itens_contabais_bp:

         print(demonstracao)

         lendo_dados.pegando_arquivo_contabil(demonstracao=True, nome_dado = demonstracao, bp = True)

    for indicador in lista_indicadores:

         print(indicador)

         lendo_dados.pegando_arquivo_contabil(indicadores=True, nome_dado = indicador)


    lendo_dados.cdi()
    lendo_dados.ibov()










