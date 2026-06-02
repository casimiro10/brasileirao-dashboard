import pandas as pd
import streamlit as st
import plotly.express as px 

st.set_page_config(page_title="Brasileirão_dados", page_icon="⚽", layout="wide")   
@st.cache_data
def carregar_dados():
    tabela = pd.read_excel("Brasileirao_2006_2025.xlsx")    
    return tabela
df = carregar_dados() 
df["Time"] = df["Time"].str.strip() 



col1, col2 = st.columns([1, 8])
with col1:
    st.image("taca_brasileirao.png", width=70)  

with col2:
    st.title((":blue[Brasileirão de 2006 a 2025]"))
    st.subheader(":blue[Série A do Campeonato Brasileiro]")

st.sidebar.header("Filtros")

lista_anos= df["Ano"].unique()
lista_anos_ordenada = sorted(lista_anos, reverse=True)

ano_selecionado = st.sidebar.selectbox(" Selecione a temporada ", lista_anos_ordenada)  
df_filtrado = df[df["Ano"] == ano_selecionado]

df_ordenado = df_filtrado.sort_values(by="Pontos", ascending=False)
nome_campeao = df_ordenado.iloc[0]["Time"]
pontos_campeao = df_ordenado.iloc[0]["Pontos"]

indice_melhor_ataque = df_filtrado["Gols_Pro"].idxmax()
time_melhor_ataque = df_filtrado.loc[indice_melhor_ataque, "Time"]
gols_melhor_ataque = df_filtrado.loc[indice_melhor_ataque, "Gols_Pro"]

indice_melhor_defesa = df_filtrado["Gols_Sofridos"].idxmin()
time_melhor_defesa = df_filtrado.loc[indice_melhor_defesa, "Time"]
gols_melhor_defesa = df_filtrado.loc[indice_melhor_defesa, "Gols_Sofridos"]

st.write('---')

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="🏆 Campeão", value=nome_campeao)
with kpi2:
    st.metric(label="⭐ Pontos do Campeão", value=f"{pontos_campeao} pts")
with kpi3:
    st.metric(label="📅 Temporada", value=ano_selecionado)

kpi4, kpi5 = st.columns(2)

with kpi4:
    st.metric(label="⚽ Melhor Ataque", value=time_melhor_ataque, delta=f"{gols_melhor_ataque} gols feitos", delta_color="normal")
with kpi5:
    st.metric(label="🛡️ Melhor Defesa", value=time_melhor_defesa, delta=f"{gols_melhor_defesa} gols sofridos", delta_color="inverse")

st.write("----")
st.subheader(f"Tabela de classificação {ano_selecionado}")  
st.dataframe(df_filtrado[["Posicao", "Time", "Pontos", "Jogos", "Vitorias", "Empates", "Derrotas"]], hide_index=True, use_container_width=True) 
st.write("----")    
st.subheader("📊 Comparativo de Pontos")    

cores_times = {
    "Flamengo": "#c22a1e",      
    "Palmeiras": "#006437",     
    "São Paulo": "#FE0000",     
    "Corinthians": "#000000",   
    "Cruzeiro": "#003a70",      
    "Atlético-MG": "#000000",   
    "Grêmio": "#0d80bf",        
    "Internacional": "#e50000", 
    "Fluminense": "#7a0016",    
    "Botafogo": "#000000",      
    "Vasco": "#000000",         
    "Santos": "#ffffff",        
    "Bahia": "#003a70",         
    "Fortaleza": "#1d3989",     
    "Athletico-PR": "#c8102e",  
    "Bragantino": "#000000",    
    "Cuiabá": "#fdf228",        
    "Juventude": "#006437",     
    "Vitória": "#cc0000",       
    "Mirassol": "#fdf228"       
}
fig = px.bar(
    df_filtrado,
    x="Time",
    y="Pontos",
    color="Time",
    title=f"Pontuação dos Times - {ano_selecionado}",
    text_auto = True,
    color_discrete_map=cores_times      
)       
fig.update_traces(marker_line_color="black", marker_line_width=1)

st.plotly_chart(fig, use_container_width=True)