from calculadora_factor import backtest_indicators

def rodar_backtest_via_form(dia_inicial, dia_final, duracao_carteira, corretagem, ativos, filtro_liquidez, 
                            indicador1, ordem1, indicador2, ordem2, indicador3, ordem3, indicador4, ordem4,
                            indicador5, ordem5, indicador6, ordem6, indicador7, ordem7, indicador8, ordem8):

    try:

        duracao_carteira = int(duracao_carteira)
        corretagem = float(corretagem)
        ativos = int(ativos)
        filtro_liquidez = float(filtro_liquidez)
    
        if indicador5 == "":
            
            indicadores = [indicador1, indicador2, indicador3, indicador4]
            ordens = [ordem1, ordem2, ordem3, ordem4]
            indicadores_preenchidos = {}

            for i, indicador in enumerate(indicadores):
                
                if indicador != "":
                    
                    indicadores_preenchidos.update({
                        indicador: {'caracteristica': ordens[i]}
                    })
            
        
            dicionario_carteira =  {'carteira1': {
                    'indicadores': indicadores_preenchidos,
                    'peso': 1,
                    }}      

        else:

            indicadores = [indicador1, indicador2, indicador3, indicador4]
            ordens = [ordem1, ordem2, ordem3, ordem4]
            indicadores_preenchidos1 = {}

            for i, indicador in enumerate(indicadores):
                
                if indicador != "":
                    
                    indicadores_preenchidos1.update({
                        indicador: {'caracteristica': ordens[i]}
                    })

            indicadores = [indicador5, indicador6, indicador7, indicador8]
            ordens = [ordem5, ordem6, ordem7, ordem8]
            indicadores_preenchidos2 = {}

            for i, indicador in enumerate(indicadores):
                
                if indicador != "":
                    
                    indicadores_preenchidos2.update({
                        indicador: {'caracteristica': ordens[i]}
                    })
            
        
            dicionario_carteira =  {'carteira1': {
                    'indicadores': indicadores_preenchidos1,
                    'peso': 0.5,
                    },
                    'carteira2': {
                    'indicadores': indicadores_preenchidos2,
                    'peso': 0.5,
                    },
                    
                    }          
        
        nome_pdf = ''

        for nome_carteira, carteira in dicionario_carteira.items():
                
                nome_pdf = nome_pdf + nome_carteira + "_peso" + str(carteira['peso']).replace(".", "") + "_" 

                indicadores = carteira['indicadores']

                for indicador, ordem in indicadores.items():

                    nome_pdf = nome_pdf + indicador + "_"


        if corretagem == "":
            
            corretagem = 0

        nome_pdf = nome_pdf + str(duracao_carteira) + '_' + str(filtro_liquidez) + "M_" + str(ativos) + "A.pdf"

        backtest = backtest_indicators(data_final=dia_final, data_inicial= dia_inicial, filtro_liquidez=(filtro_liquidez * 1000000), balanceamento=duracao_carteira, 
                                                    numero_ativos=ativos, corretagem=corretagem,
                                                    nome_arquivo= nome_pdf,
                                                **dicionario_carteira)
        

        backtest.pegando_dados()
        backtest.filtrando_datas()
        backtest.criando_carteiras()
        backtest.calculando_retorno_diario()
        backtest.make_report()

        estado = "BACKTEST COMPLETO"

        return estado

    except Exception as error:
         
         estado = error

         return estado









