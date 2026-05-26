import json
import pandas as pd
import streamlit as st
import plotly.express as px

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard de Feedbacks",
    layout="wide"
)

# CARREGAR JSON
with open("resultado_sebrae_local.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# DATAFRAME
df = pd.DataFrame(dados)

# EXTRAIR NOTA 
df["nota"] = df["avaliacao"].str.extract(r"(\d)").astype(int)

# CLASSIFICAÇÃO
def sentimento(nota):
    if nota >= 4:
        return "Positivo"
    elif nota == 3:
        return "Neutro"
    else:
        return "Negativo"

df["sentimento"] = df["nota"].apply(sentimento)

# TÍTULO
st.title("📊 Dashboard de Feedbacks")

# SIDEBAR
st.sidebar.header("Filtros")

filtro_sentimento = st.sidebar.multiselect(
    "Sentimento",
    options=df["sentimento"].unique(),
    default=df["sentimento"].unique()
)

df_filtrado = df[df["sentimento"].isin(filtro_sentimento)]

# MÉTRICAS
media = df_filtrado["nota"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Feedbacks", len(df_filtrado))

with col2:
    st.metric("Média Avaliações", f"{media:.1f} ⭐")

with col3:
    positivos = len(df_filtrado[df_filtrado["sentimento"] == "Positivo"])
    st.metric("Feedbacks Positivos", positivos)

# TABELA
st.subheader("Feedbacks")

st.dataframe(
    df_filtrado[
        [
            "titulo_feedback",
            "comentario_usuario",
            "avaliacao",
            "sentimento"
        ]
    ],
    use_container_width=True
)

# GRÁFICO DE BARRAS
st.subheader("Distribuição das Avaliações")

fig = px.histogram(
    df_filtrado,
    x="nota",
    color="sentimento",
    nbins=5
)

st.plotly_chart(fig, use_container_width=True)

# GRÁFICO DE PIZZA
st.subheader("Sentimentos")

fig2 = px.pie(
    df_filtrado,
    names="sentimento"
)

st.plotly_chart(fig2, use_container_width=True)