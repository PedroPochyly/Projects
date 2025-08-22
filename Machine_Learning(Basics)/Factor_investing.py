import pandas as pd
import numpy as np

# ================================
# 1. Leitura da planilha
# ================================
df = pd.read_excel("dados_acoes.xlsx")

# Garantir nomes consistentes (remover espaços extras)
df.columns = [c.strip() for c in df.columns]

# ================================
# 2. Aplicar filtros básicos
# ================================
filtros = (
    (df["Liq.2meses"] >= 500000) &       # liquidez mínima
    (df["Patrim. Líq"] > 0) &            # patrimônio líquido positivo
    (df["P/L"].between(0, 100)) &        # P/L em faixa aceitável
    (df["EV/EBITDA"].between(0, 20)) &   # EV/EBITDA em faixa aceitável
    (df["Dív.Brut/ Patrim."] < 2.5)      # evitar alavancagem excessiva
)

df_filt = df.loc[filtros].copy()

# ================================
# 3. Função para rankear métricas
# ================================
def rank_score(series, ascending=True):
    """
    Transforma uma série em score de 0 a 1 baseado em ranking percentual.
    ascending=True => menor valor é melhor (ex: P/L).
    ascending=False => maior valor é melhor (ex: ROE).
    """
    return series.rank(pct=True, ascending=ascending)

# ================================
# 4. Cálculo dos fatores
# ================================

## Value (quanto menor múltiplo, melhor)
df_filt["Score_Value"] = (
    rank_score(df_filt["P/L"], ascending=True) +
    rank_score(df_filt["P/VP"], ascending=True) +
    rank_score(df_filt["EV/EBITDA"], ascending=True)
) / 3

## Size (menor patrimônio líquido = maior prêmio)
df_filt["Score_Size"] = rank_score(df_filt["Patrim. Líq"], ascending=True)

## Quality (quanto maior ROE, ROIC e Margem Líquida, melhor)
df_filt["Score_Quality"] = (
    rank_score(df_filt["ROE"], ascending=False) +
    rank_score(df_filt["ROIC"], ascending=False) +
    rank_score(df_filt["Mrg Ebit"], ascending=False)
) / 3

## Investment (quanto menor o crescimento agressivo, melhor)
df_filt["Score_Investment"] = rank_score(df_filt["Cresc. Rec.5a"], ascending=True)

# ================================
# 5. Score final multifatorial
# ================================
df_filt["Score_Total"] = (
    df_filt["Score_Value"] +
    df_filt["Score_Size"] +
    df_filt["Score_Quality"] +
    df_filt["Score_Investment"]
) / 4

# ================================
# 6. Seleção do Top 20%
# ================================
top20 = df_filt.sort_values("Score_Total", ascending=False)
n_top = int(len(top20) * 0.2)
carteira_final = top20.head(n_top)

# ================================
# 7. Exportar resultado
# ================================
carteira_final.to_excel("carteira_factor_investing.xlsx", index=False)

print("✅ Ranking criado com sucesso!")
print("Foram selecionadas", n_top, "ações para a carteira multifatorial.")
