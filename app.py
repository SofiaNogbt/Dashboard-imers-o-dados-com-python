import streamlit as st #Para criar a página
import pandas as pd
import plotly.express as px

#Configuração da página -> Define o título, o ícone e o layout para ocupar a largura inteira

st.set_page_config(

    page_title= 'Dashboard de Salários na Área de Dados',
    page_icon= '📊',
    layout= 'wide', #Página no formato largo
    
)

#Passo 2 -> Carregar os dados

df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

#Criação da barra lateral de filtros

st.sidebar.header("Filtros 🔍")

#Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano",anos_disponiveis)

#Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade",senioridades_disponiveis)

#Filtro por tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato",contratos_disponiveis)

#Filtro por tamanho da empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da empresa",tamanhos_disponiveis)

#Criar um df separado para armazenar os dados filtrados

df_filtrado = df [
                  
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
    
]

#Conteúdo principal da página, texto introdutório

st.title("🎲 Dashboard de Análise de Salários na Área de Dados 🎲")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para auxiliar em sua busca. Insira os filtros para visualizar as métricas.")

#Criar uma aba de métricas principais que funcionem como o comando describe para o usuário visualizar o principal da base de dado

st.subheader('Métricas gerais (Salário Anual em USD)')

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_max = df_filtrado['usd'].max()
    salario_min = df_filtrado['usd'].min()
    total_registrados = df_filtrado.shape[0] #Pega a primeira posição do vetor de tamanho o qual mostra quantas linhas há
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]

else:
    salario_medio,salario_max,salario_min,total_registrados,cargo_mais_frequente = 0,0,0,0,""

col1,col2,col3,col4,col5 = st.columns(5)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_max:,.0f}")
col3.metric("Salário mínimo", f"${salario_min:,.0f}")
col4.metric("Total de registros", f"${total_registrados}")
col5.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown('---')

#Gráficos interativos com Plotly

st.subheader("Gráficos") #Subtítulo

colgraf1,colgraf2 = st.columns(2)

with colgraf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index() #Pegar 10 os cargos por maior salario médio

        grafico_cargos = px.bar(

            top_cargos,
            x = 'usd',
            y = 'cargo',
            orientation= 'h',
            title= 'Top 10 cargos por salário médio',
            labels= {'usd': 'Média salarial anual (USD)' , 'cargo' : ''}

        )

        grafico_cargos.update_layout(title_x = 0.1, yaxis = {'categoryorder' : 'total ascending'}) #Alinhar o título
        st.plotly_chart(grafico_cargos,use_container_width=True) #Exibir o gráfico

    else: 
        st.warning('Nenhum dado para exibir no gráfico de cargos.')

with colgraf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            
            df_filtrado,
            x='usd',
            nbins = 30,
            title = 'Distribuição de salários anuais',
            labels= {'usd' : 'Faixa salarial (USD)' , 'count' : ''}

        )

        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist,use_container_width=True)

    else:
        st.warning('Nenhum dado para exibir no gráfico de distribuição.')

colgraf3, colgraf4 = st.columns(2)

with colgraf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with colgraf4:
    if not df_filtrado.empty:

        df_cientistas = df_filtrado.query('cargo == "Data Scientist"')
        media_ds_pais = df_cientistas.groupby('residencia_iso3')['usd'].mean().reset_index()

        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.") 

#Tabela da dados detalhados
st.subheader('Dados Detalhados')
st.dataframe(df_filtrado)

        

    




