import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração inicial
st.set_page_config(page_title="Análise de Matrizes", layout="wide")
st.title("📦 Dashboard de Matrizes e Ferramentais")

# 2. Carregar a sua planilha específica
# O comando header=1 avisa o Pandas para pular a primeira linha vazia do seu Excel
@st.cache_data # Isso faz o site carregar a planilha mais rápido
def carregar_dados():
    df = pd.read_excel("Matrizes_AA-B_Com_Dimensoes_e_Pesos.xlsx", sheet_name="TudoOK", header=1)
    
    # Limpeza básica: remover colunas vazias que o Excel cria (como 'Unnamed: 0')
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # Criar uma nova coluna de Volume (Altura x Largura x Comprimento)
    df['Volume'] = df['Altura'] * df['Largura'] * df['Comprimento']
    return df

df = carregar_dados()

# 3. Criar Filtro Interativo na Barra Lateral
st.sidebar.header("Filtros")
peso_min = int(df['Peso'].min())
peso_max = int(df['Peso'].max())

filtro_peso = st.sidebar.slider(
    "Filtrar por Peso:", 
    min_value=peso_min, 
    max_value=peso_max, 
    value=(peso_min, peso_max) # Seleciona tudo por padrão
)

# Aplicar o filtro na base de dados
df_filtrado = df[(df['Peso'] >= filtro_peso[0]) & (df['Peso'] <= filtro_peso[1])]

# 4. Exibir Cartões de Métricas (KPIs) baseados no filtro
col1, col2, col3 = st.columns(3)
col1.metric("Quantidade de Matrizes", len(df_filtrado))
col2.metric("Peso Médio", f"{df_filtrado['Peso'].mean():.0f} kg") # Assumindo kg, altere se for gramas
col3.metric("Maior Peso", f"{df_filtrado['Peso'].max():.0f} kg")

st.markdown("---")

# 5. Gráfico 3D Interativo: Altura x Largura x Comprimento (Cor = Peso)
st.subheader("Gráfico 3D das Dimensões (Gire com o mouse!)")

fig_3d = px.scatter_3d(
    df_filtrado, 
    x='Comprimento', 
    y='Largura', 
    z='Altura',
    color='Peso', # Itens mais pesados terão cores diferentes
    hover_name='Ferramental', # Ao passar o mouse, mostra o nome do ferramental
    hover_data=['Referência', 'Peso'],
    title="Análise Dimensional vs. Peso das Matrizes"
)
fig_3d.update_layout(template="plotly_dark", margin=dict(l=0, r=0, b=0, t=40))

# Mostra o gráfico no site
st.plotly_chart(fig_3d, use_container_width=True)

# 6. Mostrar a Tabela de Dados no final
st.subheader("📋 Tabela de Dados Filtrados")
st.dataframe(df_filtrado)