import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import time
import multiprocessing
import random

from streamlit import session_state

cont = 0

def tempo_wrapper(func):
    # @st.cache(allow_output_mutation=True)
    def wrapper(*args, **kwargs):
        global cont
        cont += 1
        print(f' {cont} - name: {func.__name__}')
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
        print('____'*10)
        return result
    return wrapper

@tempo_wrapper
def main():
    # Configurar a página do Streamlit
    st.set_page_config(layout="wide", page_icon="logo.png")

    # Cabeçalho da página
    exibir_cabecalho()

    # Carregar dados e processar
    df = carregar_dados()
    df = filtrar_dados(df)

    # Selecionar colunas para visualização
    selected_columns = selecionar_colunas(df)

    # Selecionar intervalo de data e hora e velocidade de simulação
    start_datetime, end_datetime = selecionar_intervalo_simulacao(df)

    # Filtrar o DataFrame pelo intervalo de tempo selecionado
    df_filtered = carregar_dados_filtrados(df, start_datetime, end_datetime)

    # Espaço para o gráfico
    plot_placeholder = st.empty()

    plotar_graficos(df_filtered, selected_columns)

    # if not 'dados' in st.session_state:
    # Mostrar os dados e estatísticas
    mostrar_dados(df)
    mostrar_estatisticas(df)

    # Informações da empresa
    exibir_informacoes_empresa()

    # st.session_state['dados'] = True

@tempo_wrapper
def exibir_cabecalho():
    # Exibir o cabeçalho da página com o logo e o título
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("logo.png", width=150)
    with col2:
        st.write("### PCH JASPE - Dados de Operação")

    # Informações adicionais compactadas
    info = {
        "Nome :": 'CGH JASPE', "Número de Turbinas :": 4,
        "Estado :": 'Santa Catarina', "Data Atual :": datetime.now().strftime("%Y-%m-%d"),
        "Localização :": 'Sao Miguel da Boa Vista, Estrada Sargento', "Potência :": '5.1 MW'
    }

    # Mostrar informações no Streamlit de forma compacta
    st.write("#### Informações da Usina: ")
    info_str = " | ".join([f"{key} {value}" for key, value in info.items()])
    st.write(info_str)

@st.cache_data
@tempo_wrapper
def carregar_dados():
    # Leitura do arquivo CSV diretamente da pasta
    df = pd.read_csv("ug01_2.csv", sep=",")
    df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
    return df

@tempo_wrapper
def selecionar_colunas(df):
    # Criar um seletor para as colunas do DataFrame
    st.write("#### Dados para UG-01:")
    columns = df.columns.tolist()
    return st.multiselect("Selecione até 3 colunas para plotar em relação a data_hora:", columns, default=columns[:3])

@tempo_wrapper
def selecionar_intervalo_simulacao(df):
    # Criar a linha de seleção de datas, horas e simulação
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

    with col1:
        start_date = st.date_input("Data Inicial", df.index.min().date())

    with col2:
        start_time = st.time_input("Hora Inicial", df.index.min().time())

    with col3:
        end_date = st.date_input("Data Final", df.index.max().date())

    with col4:
        end_time = st.time_input("Hora Final", df.index.max().time())


    # Combinar a data e hora para formar o datetime completo
    start_datetime = pd.Timestamp.combine(start_date, start_time)
    end_datetime = pd.Timestamp.combine(end_date, end_time)

    return start_datetime, end_datetime


@tempo_wrapper
def carregar_dados_filtrados(df, start_datetime, end_datetime):
    # Função para carregar dados em cache
    mask = (df.index >= start_datetime) & (df.index <= end_datetime)
    return df.loc[mask]

@tempo_wrapper
def mostrar_dados(df):
    # Converter o DataFrame para CSV
    df['data_hora'] = df.index
    csv = df.to_csv(index=False)

    # Botão de download
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="dados.csv",
        mime="text/csv"
    )

def gerar_cor_aleatoria():
    # Gera uma cor aleatória em formato hexadecimal
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

@tempo_wrapper
def plotar_graficos(df, selected_columns):
    # Lista de cores padrão
    cores_padrao = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
                    '#17becf','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']

    # Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
    if selected_columns:
        for i, column in enumerate(selected_columns):
            col_limite, col_grafico = st.columns([1, 19])

            with col_limite:
                max_val = st.number_input(f"Máx.", value=float(df[column].max()), key=f"max_{column}")
                min_val = st.number_input(f"Mín.", value=float(df[column].min()), key=f"min_{column}")
                cor_grafico = st.color_picker(f"Cor", value=cores_padrao[i], key=f"color_{column}")

            with col_grafico:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column, line=dict(color=cor_grafico)))
                fig.update_yaxes(range=[min_val, max_val])
                fig.update_layout(title=f"{column} vs Data e Hora", height=500)
                st.plotly_chart(fig)

@tempo_wrapper
def mostrar_estatisticas(df):
    # Mostrar estatísticas descritivas
    st.write("#### Estatísticas Descritivas:")
    st.write(df.describe())

@tempo_wrapper
def exibir_informacoes_empresa():
    # Exibir informações da empresa
    engesep = {
        "title": 'EngeSEP Engenharia Integrada LTDA',
        "endereco": 'R. Roque Domingos Onghero, no 30d - Bom Retiro,Chapecó-SC',
        "CNPJ": 'CNPJ: 22.248.519/0001-26', "telefone": '(49)-991075958', "email": 'engesep@engesep.com.br'
    }
    engesep_str = " | ".join([f"{key}: {value}" for key, value in engesep.items()])
    st.write(engesep_str)

@tempo_wrapper
def filtrar_dados(df):
    # Filtrar colunas e processar DataFrame
    colunas = ['data_hora', 'tensao_fase_A', 'tensao_fase_B', 'tensao_fase_C', 'corrente_fase_A',
               'corrente_fase_B', 'corrente_fase_C', 'potencia_ativa', 'potencia_reativa',
               'tensao_excitacao', 'corrente_excitacao', 'temp_enrol_A',
               'temp_enrol_B', 'temp_enrol_C', 'temp_manc_rad_LA', 'temp_manc_rad_LNA', 'temp_gaxeteiro']
    df = df[colunas]

    df.columns = [
        'Data e Hora', 'Tensão Fase A', 'Tensão Fase B', 'Tensão Fase C',
        'Corrente Fase A', 'Corrente Fase B', 'Corrente Fase C',
        'Potência Ativa', 'Potência Reativa', 'Tensão Excitação', 'Corrente Excitação',
        'Temp. Enrol. Fase A', 'Temp. Enrol. Fase B', 'Temp. Enrol. Fase C',
        'Temp. Mancal Radial LA', 'Temp. Mancal Radial LNA', 'Temp. Gaxeteiro'
    ]


    df.set_index('Data e Hora', inplace=True)
    df.sort_index(inplace=True)
    return df


if __name__ == "__main__":
    main()




