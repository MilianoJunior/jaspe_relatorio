import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import time
import multiprocessing
import random

from streamlit import session_state


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


def carregar_dados():
    # Leitura do arquivo CSV diretamente da pasta
    df = pd.read_csv("ug01_1.csv", sep=";")
    df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
    return df


def selecionar_colunas(df):
    # Criar um seletor para as colunas do DataFrame
    st.write("#### Dados para UG-01:")
    columns = df.columns.tolist()
    return st.multiselect("Selecione até 3 colunas para plotar em relação a data_hora:", columns, default=columns[:3])


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


@st.cache_data
def carregar_dados_filtrados(df, start_datetime, end_datetime):
    # Função para carregar dados em cache
    mask = (df.index >= start_datetime) & (df.index <= end_datetime)
    return df.loc[mask]

def mostrar_dados(df):
    # Converter o DataFrame para CSV
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


def plotar_graficos(df, selected_columns):
    # Lista de cores padrão
    cores_padrao = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
                    '#17becf']

    # Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
    if selected_columns:
        for i, column in enumerate(selected_columns):
            col_limite, col_grafico = st.columns([1, 15])

            with col_limite:
                max_val = st.number_input(f"Máx. para {column}", value=float(df[column].max()), key=f"max_{column}")
                min_val = st.number_input(f"Mín. para {column}", value=float(df[column].min()), key=f"min_{column}")
                cor_grafico = st.color_picker(f"Cor {column}", value=random.choice(cores_padrao), key=f"color_{column}")

            with col_grafico:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column, line=dict(color=cor_grafico)))
                fig.update_yaxes(range=[min_val, max_val])
                fig.update_layout(title=f"{column} vs Data e Hora", height=300)
                st.plotly_chart(fig)


# def mostrar_dados(df):
#     # Mostrar o DataFrame no Streamlit
#     st.write("#### Dados:")
#     st.dataframe(df)


def mostrar_estatisticas(df):
    # Mostrar estatísticas descritivas
    st.write("#### Estatísticas Descritivas:")
    st.write(df.describe())


def exibir_informacoes_empresa():
    # Exibir informações da empresa
    engesep = {
        "title": 'EngeSEP Engenharia Integrada LTDA',
        "endereco": 'R. Roque Domingos Onghero, no 30d - Bom Retiro,Chapecó-SC',
        "CNPJ": 'CNPJ: 22.248.519/0001-26', "telefone": '(49)-991075958', "email": 'engesep@engesep.com.br'
    }
    engesep_str = " | ".join([f"{key}: {value}" for key, value in engesep.items()])
    st.write(engesep_str)


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

# import pandas as pd
# import streamlit as st
# # import matplotlib.pyplot as plt
# import plotly.express as px
# from datetime import datetime
# # Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import threading
# import time
#
#
#
# def main():
#     st.set_page_config(layout="wide", page_icon="logo.png")
#     col1, col2 = st.columns([1, 5])
#     with col1:
#         st.image("logo.png", width=150)
#     with col2:
#         st.write("### PCH JASPE - Dados de Operação")
#
#     # Informações adicionais compactadas
#     info = {
#         "Nome :": 'CGH JASPE', "Número de Turbinas :": 4,
#         "Estado :": 'Santa Catarina', "Data Atual :": datetime.now().strftime("%Y-%m-%d"),
#         "Localização :": 'Sao Miguel da Boa Vista, Estrada Sargento', "Potência :": '5.1 MW'
#     }
#
#     # Mostrar informações no Streamlit de forma compacta
#     st.write("#### Informações da Usina: ")
#     info_str = " | ".join([f"{key} {value}" for key, value in info.items()])
#     st.write(info_str)
#
#     # Leitura do arquivo CSV diretamente da pasta
#     df = pd.read_csv("ug01_1.csv", sep=";")
#
#     # Converter a coluna 'data_hora' para datetime
#     df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
#
#     # Filtrar os dados
#     df = filtrar_dados(df)
#
#     # Criar um seletor para as colunas do DataFrame
#     st.write("#### Dados para UG-01:")
#     columns = df.columns.tolist()
#     selected_columns = st.multiselect("Selecione até 3 colunas para plotar em relação a data_hora:", columns, default=columns[:3])
#
#     # Criar a linha de seleção de datas, horas e simulação
#     col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])
#
#     with col1:
#         start_date = st.date_input("Data Inicial", df.index.min().date())
#
#     with col2:
#         start_time = st.time_input("Hora Inicial", df.index.min().time())
#
#     with col3:
#         end_date = st.date_input("Data Final", df.index.max().date())
#
#     with col4:
#         end_time = st.time_input("Hora Final", df.index.max().time())
#
#     with col5:
#         sim_speed = st.number_input("Velocidade de Simulação (x)", min_value=0.1, value=1.0, step=0.1)
#
#     with col6:
#         simulate = st.button("Simular")
#
#     # Combinar a data e hora para formar o datetime completo
#     start_datetime = pd.Timestamp.combine(start_date, start_time)
#     end_datetime = pd.Timestamp.combine(end_date, end_time)
#
#     # Filtrar o DataFrame pelo intervalo de tempo selecionado
#     mask = (df.index >= start_datetime) & (df.index <= end_datetime)
#     df_filtered = df.loc[mask]
#
#     # Espaço para o gráfico
#     plot_placeholder = st.empty()
#
#     # Simulação de dados se o botão for pressionado
#     if simulate:
#         # Inicializar o gráfico com Plotly
#         fig = go.Figure()
#
#         # Adicionar uma linha para cada coluna selecionada
#         for column in selected_columns:
#             fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name=column))
#
#         # Simular a plotagem dos dados em tempo real
#         for i in range(len(df)):
#             # Atualizar os dados para cada trace
#             for trace, column in zip(fig.data, selected_columns):
#                 trace.x = list(df.index[:i + 1])
#                 trace.y = list(df[column][:i + 1])
#
#             # Atualizar o gráfico no espaço reservado
#             plot_placeholder.plotly_chart(fig, use_container_width=True)
#             time.sleep(1 / sim_speed)  # Controlar a velocidade da simulação
#
#     else:
#
#         # Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
#         if selected_columns:
#             for i, column in enumerate(selected_columns):
#                 # Criar uma linha com duas colunas - uma para os inputs de limite e outra para o gráfico
#                 col_limite, col_grafico = st.columns([1, 20])  # A primeira coluna ocupa 5% e a segunda 95%
#
#                 with col_limite:
#                     # Adicionar entradas para definir a escala de cada variável no eixo y
#                     # st.write(f"Limites para {column}")
#                     max_val = st.number_input(f"Máx.", value=float(df_filtered[column].max()),
#                                               key=f"max_{column}")
#                     min_val = st.number_input(f"Mín.", value=float(df_filtered[column].min()),
#                                               key=f"min_{column}")
#
#
#                 with col_grafico:
#                     # Criar o gráfico da coluna específica e adicionar ao subplot
#                     fig = go.Figure()
#                     fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered[column], mode='lines', name=column))
#
#                     # Atualizar o layout para definir o intervalo do eixo y
#                     fig.update_yaxes(range=[min_val, max_val])
#                     fig.update_layout(title=f"{column} vs Data e Hora", height=300)
#
#                     # Plotar o gráfico no Streamlit
#                     st.plotly_chart(fig)
#
#     # Mostrando o DataFrame no Streamlit
#     st.write("#### Dados:")
#     st.dataframe(df)
#
#     # Algumas estatísticas básicas sobre o DataFrame
#     st.write("#### Estatísticas Descritivas:")
#     st.write(df.describe())
#
#     # Informações da empresa compactadas
#     engesep = {
#         "title": 'EngeSEP Engenharia Integrada LTDA', "endereco": 'R. Roque Domingos Onghero, no 30d - Bom Retiro,Chapecó-SC',
#         "CNPJ": 'CNPJ: 22.248.519/0001-26', "telefone": '(49)-991075958', "email": 'engesep@engesep.com.br'
#     }
#     engesep_str = " | ".join([f"{key}: {value}" for key, value in engesep.items()])
#     st.write(engesep_str)
#
#
# def filtrar_dados(df):
#     # Filtrar os dados a partir de 17/09/2024 coluna 'data_hora' dos últimos 30 dias
#     # df = df[df['data_hora'] > '2024-09-17']
#
#     # Filtrar as colunas desejadas
#     colunas = ['data_hora', 'tensao_fase_A', 'tensao_fase_B',  'tensao_fase_C', 'corrente_fase_A',
#                'corrente_fase_B', 'corrente_fase_C', 'potencia_ativa', 'potencia_reativa',
#                'tensao_excitacao', 'corrente_excitacao', 'temp_enrol_A',
#                'temp_enrol_B', 'temp_enrol_C','temp_manc_rad_LA', 'temp_manc_rad_LNA', 'temp_gaxeteiro']
#     df = df[colunas]
#
#     # Renomear colunas para textos apresentáveis
#     df.columns = [
#         'Data e Hora', 'Tensão Fase A', 'Tensão Fase B',  'Tensão Fase C',
#         'Corrente Fase A', 'Corrente Fase B', 'Corrente Fase C',
#         'Potência Ativa', 'Potência Reativa', 'Tensão Excitação', 'Corrente Excitação',
#         'Temp. Enrol. Fase A','Temp. Enrol. Fase B','Temp. Enrol. Fase C',
#         'Temp. Mancal Radial LA', 'Temp. Mancal Radial LNA', 'Temp. Gaxeteiro'
#     ]
#
#     # Definir data_hora como index
#     df.set_index('Data e Hora', inplace=True)
#
#     # Ordenar os dados por data_hora
#     df.sort_index(inplace=True)
#
#     return df
#
#
# if __name__ == "__main__":
#     main()



# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
# from datetime import datetime
# # from pdf_novo import PDF
# # import webbrowser
#
#
# def main():
#     st.set_page_config(layout="wide", page_icon="logo.png")
#     col1, col2 = st.columns([1, 5])
#     with col1:
#         st.image("logo.png", width=150)
#     with col2:
#         st.title("PCH JASPE")
#
#     # Informações adicionais
#     info = {
#         "Nome :": 'CGH JASPE',
#         "Número de Turbinas :": 4,
#         "Estado :": 'Santa Catarina',
#         "Data Atual :": datetime.now().strftime("%Y-%m-%d"),
#         "Localização :": 'Sao Miguel da Boa Vista, Estrada Sargento',
#         "Potência :": 5.1,
#     }
#     # Mostrar informações no Streamlit
#     st.write("### Informações da Usina:")
#     for key, value in info.items():
#         st.write(f"{key} {value}")
#
#     # Leitura do arquivo CSV diretamente da pasta
#     df = pd.read_csv("ug01_1.csv", sep=";")
#
#     # Converter a coluna 'data_hora' para datetime
#     df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
#
#     # filtrar os dados
#     df = filtrar_dados(df)
#
#     # Criar um seletor para as colunas do DataFrame
#     st.write("#### Selecionar Colunas para Gráfico:")
#     columns = df.columns.tolist()
#     selected_columns = st.multiselect("Selecione até 3 colunas para plotar em relação a data_hora:", columns,
#                                       default=columns[:3])
#
#     # Selecionar intervalo de tempo
#     st.write("##### Selecione o Espaço de Tempo:")
#     start_date = st.date_input("Data Inicial", df.index.min().date())
#     start_time = st.time_input("Hora Inicial", df.index.min().time())
#     end_date = st.date_input("Data Final", df.index.max().date())
#     end_time = st.time_input("Hora Final", df.index.max().time())
#
#     # Combinar a data e hora para formar o datetime completo
#     start_datetime = pd.Timestamp.combine(start_date, start_time)
#     end_datetime = pd.Timestamp.combine(end_date, end_time)
#
#     # Filtrar o DataFrame pelo intervalo de tempo selecionado
#     mask = (df.index >= start_datetime) & (df.index <= end_datetime)
#     df_filtered = df.loc[mask]
#
#     # Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
#     if selected_columns:
#         st.write(f"##### Gráfico de {', '.join(selected_columns)} em relação a data_hora:")
#         import plotly.express as px
#         fig = px.line(df_filtered, x=df_filtered.index, y=selected_columns,
#                       title=f"{', '.join(selected_columns)} vs Data e Hora")
#         st.plotly_chart(fig)
#
#     # Mostrando o DataFrame no Streamlit
#     st.write("#### Dados do CSV:")
#     st.dataframe(df)
#
#     # Algumas estatísticas básicas sobre o DataFrame
#     st.write("#### Estatísticas Descritivas:")
#     st.write(df.describe())
#
#     engesep = {
#         "title": 'EngeSEP Engenharia Integrada LTDA',
#         "endereco": 'R. Roque Domingos Onghero, no 30d - Bom Retiro,Chapecó-SC',
#         "CNPJ": 'CNPJ: 22.248.519/0001-26',
#         "telefone": '(49)-991075958',
#         "email": 'engesep@engesep.com.br'
#     }
#
#     # st.write("### Informações da Empresa:")
#     for key, value in engesep.items():
#         st.write(f"{key} {value}")
#
#
#
# def filtrar_dados(df):
#     # filtrar os dados a partir de 17/09/2024 coluna 'data_hora' dos últimos 30 dias
#     df = df[df['data_hora'] > '2024-09-17']
#
#     # filtrar as colunas desejadas
#     colunas = ['data_hora','tensao_fase_A', 'tensao_fase_B', 'tensao_neutro', 'tensao_fase_C', 'corrente_fase_A', 'corrente_fase_B',
#                'corrente_fase_C', 'corrente_neutro', 'potencia_ativa', 'potencia_reativa',
#                'tensao_excitacao', 'corrente_excitacao', 'temp_manc_rad_LA', 'temp_manc_rad_LNA', 'temp_gaxeteiro']
#     df = df[colunas]
#
#     # Renomear colunas para textos apresentáveis
#     df.columns = [
#         'Data e Hora', 'Tensão Fase A', 'Tensão Fase B', 'Tensão Neutro', 'Tensão Fase C',
#         'Corrente Fase A', 'Corrente Fase B', 'Corrente Fase C', 'Corrente Neutro',
#         'Potência Ativa', 'Potência Reativa', 'Tensão Excitação', 'Corrente Excitação',
#         'Temp. Mancal Radial LA', 'Temp. Mancal Radial LNA', 'Temp. Gaxeteiro'
#     ]
#
#     # definir data_hora como index
#     df.set_index('Data e Hora', inplace=True)
#
#     # ordenar os dados por data_hora
#     df.sort_index(inplace=True)
#
#     return df
#
# if __name__ == "__main__":
#     main()
#
#
# # def main():
# #     # st.set_page_config(layout="wide")
# #     # st.title("Visualizador de CSV com Pandas e Streamlit")
# #
# #     # Leitura do arquivo CSV diretamente da pasta
# #     df = pd.read_csv("ug01_1.csv", sep=";")
# #
# #     # Converter a coluna 'data_hora' para datetime
# #     df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')
#
#     # # Mostrando o DataFrame no Streamlit
#     # st.write("## Dados do CSV:")
#     # st.dataframe(df)
#     #
#     # # Algumas estatísticas básicas sobre o DataFrame
#     # st.write("## Estatísticas Descritivas:")
#     # st.write(df.describe())
#     #
#     # # Criar um seletor para as colunas do DataFrame
#     # st.write("## Selecionar Colunas para Gráfico:")
#     # columns = df.columns.tolist()
#     # columns.remove('data_hora')
#     # selected_columns = st.multiselect("Selecione até 3 colunas para plotar em relação a data_hora:", columns, default=columns[:3])
#     #
#     # # Selecionar intervalo de tempo
#     # st.write("## Selecione o Espaço de Tempo:")
#     # start_date = st.date_input("Data Inicial", df['data_hora'].min().date())
#     # start_time = st.time_input("Hora Inicial", df['data_hora'].min().time())
#     # end_date = st.date_input("Data Final", df['data_hora'].max().date())
#     # end_time = st.time_input("Hora Final", df['data_hora'].max().time())
#     #
#     # # Combinar a data e hora para formar o datetime completo
#     # start_datetime = pd.Timestamp.combine(start_date, start_time)
#     # end_datetime = pd.Timestamp.combine(end_date, end_time)
#     #
#     # # Filtrar o DataFrame pelo intervalo de tempo selecionado
#     # mask = (df['data_hora'] >= start_datetime) & (df['data_hora'] <= end_datetime)
#     # df_filtered = df.loc[mask]
#     #
#     # # Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
#     # if selected_columns:
#     #     st.write(f"## Gráfico de {', '.join(selected_columns)} em relação a data_hora:")
#     #     import plotly.express as px
#     #     fig = px.line(df_filtered, x='data_hora', y=selected_columns, title=f"{', '.join(selected_columns)} vs Data e Hora")
#     #     st.plotly_chart(fig)
#
#
# # Index(['id', 'uhlm_vaz_oleo', 'temp_uhlm_oleo', 'temp_troc_calor',
# #        'uhrv_pressao', 'temp_uhrv_oleo', 'status', 'distribuidor',
# #        'velocidade', 'temp_manc_rad_LA', 'temp_manc_rad_LNA', 'temp_gaxeteiro',
# #        'acumulador_energia', 'tensao_fase_A', 'tensao_fase_B', 'tensao_fase_C',
# #        'tensao_neutro', 'corrente_fase_A', 'corrente_fase_B',
# #        'corrente_fase_C', 'corrente_neutro', 'tensao_excitacao',
# #        'corrente_excitacao', 'frequencia', 'potencia_ativa',
# #        'potencia_reativa', 'potencia_aparente', 'fp', 'temp_enrol_A',
# #        'temp_enrol_B', 'temp_enrol_C', 'temp_csu1', 'nivel_montante',
# #        'nivel_jusante', 'nivel_jusante_cf', 'horimetro_eletrico',
# #        'tensaoL_fase_AB', 'tensaoL_fase_BC', 'tensaoL_fase_CA',
# #        'correnteL_fase_A', 'correnteL_fase_B', 'correnteL_fase_C',
# #        'temp_trafo_oleo', 'temp_trafo_enrol', 'data_hora'],
#
# #
# # def gerar_pdf(df):
# #     '''Gerar um PDF com as estatísticas descritivas do DataFrame'''
# #
# #     pdf = PDF(df)
# #
# #     pdf.output("relatorio.pdf")
# #
# #     # abrir o PDF
# #     webbrowser.open_new_tab("relatorio.pdf")

