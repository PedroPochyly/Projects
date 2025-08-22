import pandas as pd
import numpy as np

# ================================
# 1. Leitura da planilha
# ================================
df = pd.read_excel("dados_acoes.xlsx")

# --- NOVO: VERIFICAR NOMES DAS COLUNAS ---
print("Nomes originais das colunas:", df.columns)
# ----------------------------------------

# Garantir nomes consistentes (remover espaços extras e caracteres especiais)
df.columns = [c.strip().replace('.', '').replace(' ', '_') for c in df.columns]

# --- NOVO: VERIFICAR NOMES DAS COLUNAS APÓS A MODIFICAÇÃO ---
print("Nomes das colunas após a limpeza:", df.columns)
# -----------------------------------------------------------

# ================================
# 2. Aplicar filtros básicos e de Small Cap
# ================================
# Definir um limite para o Patrimônio Líquido para capturar small caps.
limite_patrimonio_liquido = 2500000000 # 1 bilhão de reais

filtros = (
    (df["Liq2meses"] >= 200000) &       # liquidez mínima
    (df["Patrim_Líq"] > 0) &             # patrimônio líquido positivo
    (df["Patrim_Líq"] <= limite_patrimonio_liquido) & # Filtro para small caps
    (df["EV/EBIT"].between(0, 30)) &     # Faixa aceitável para EV/EBIT
    (df["DívBrut/_Patrim"] < 3.0)       # evitar alavancagem excessiva
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

## Value (focado em EV/EBIT e P/L)
df_filt["Score_Value"] = (
    rank_score(df_filt["EV/EBIT"], ascending=True) +
    rank_score(df_filt["P/L"], ascending=True)
) / 2

## Size (menor patrimônio líquido = maior prêmio)
df_filt["Score_Size"] = rank_score(df_filt["Patrim_Líq"], ascending=True)

## Quality (quanto maior ROE e ROIC, melhor)
df_filt["Score_Quality"] = (
    rank_score(df_filt["ROE"], ascending=False) +
    rank_score(df_filt["ROIC"], ascending=False)
) / 2

# ================================
# 5. Score final multifatorial
# ================================
# Ajustado para dar o mesmo peso a todos os 3 fatores.
df_filt["Score_Total"] = (
    df_filt["Score_Value"] +
    df_filt["Score_Size"] +
    df_filt["Score_Quality"]
) / 3

# ================================
# 6. Seleção do Top 20%
# ================================
top_acoes = df_filt.sort_values("Score_Total", ascending=False)
n_top = int(len(top_acoes) * 0.2)
carteira_final = top_acoes.head(n_top)

# ================================
# 7. Exportar resultado
# ================================
carteira_final.to_excel("carteira_small_caps_valor.xlsx", index=False)

print("✅ Ranking criado com sucesso!")
print("Foram selecionadas", n_top, "ações de Small Caps de Valor para a carteira.")