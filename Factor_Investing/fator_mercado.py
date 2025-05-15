import pandas as pd
import os

class market_premium():

    def __init__(self):

        pass

    def calculando_premio(self):

        cdi = pd.read_parquet(os.path.join(".", "dados", "cdi.parquet"))
        cdi['cota'] = (1 + cdi['retorno']).cumprod() - 1
        ibov = pd.read_parquet(os.path.join(".", "dados", 'ibov.parquet'))

        ibov_datas = ibov.sort_values('data', ascending = True)
        ibov_datas = ibov_datas.assign(year = pd.DatetimeIndex(ibov_datas['data']).year)
        ibov_datas = ibov_datas.assign(month = pd.DatetimeIndex(ibov_datas['data']).month)
        datas_final_mes = ibov_datas.groupby(['year', 'month'])['data'].last()
        dias_final_de_mes = datas_final_mes.to_list()

        ibov = ibov[ibov['data'].isin(dias_final_de_mes)]
        cdi = cdi[cdi['data'].isin(dias_final_de_mes)]
        ibov['retorno_ibov'] = ibov['fechamento'].pct_change()
        cdi['retorno_cdi'] = cdi['cota'].pct_change()
        ibov['data'] = ibov['data'].astype(str)
        cdi['data'] = cdi['data'].astype(str)

        df_dados_mercado = pd.merge(ibov, cdi, how = 'inner', on = "data")
        df_dados_mercado['mkt_premium'] = (1 + df_dados_mercado['retorno_ibov'])/(1 + df_dados_mercado['retorno_cdi']) - 1
        df_dados_mercado = df_dados_mercado.dropna()
        df_dados_mercado = df_dados_mercado[['data', 'mkt_premium']]
        df_dados_mercado['data'] = pd.to_datetime(df_dados_mercado['data']).dt.date

        df_dados_mercado.to_parquet(os.path.join(".", "dados", 'market_premium.parquet'), index = False)


if __name__ == "__main__":

    beta = market_premium()

    beta.calculando_premio() 


    