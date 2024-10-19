import pandas as pd
import streamlit as st
# import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
# Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def main():
    st.set_page_config(layout="wide", page_icon="logo.png")
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

    # Leitura do arquivo CSV diretamente da pasta
    df = pd.read_csv("ug01_1.csv", sep=";")

    # Converter a coluna 'data_hora' para datetime
    df['data_hora'] = pd.to_datetime(df['data_hora'], errors='coerce')

    # Filtrar os dados
    df = filtrar_dados(df)

    # Criar um seletor para as colunas do DataFrame
    st.write("#### Dados para UG-01:")
    columns = df.columns.tolist()
    selected_columns = st.multiselect("Selecione até 3 colunas para plotar em relação a data_hora:", columns, default=columns[:3])

    # Selecionar intervalo de tempo em uma única linha
    col1, col2, col3, col4 = st.columns(4)
    start_date = col1.date_input("Data Inicial", df.index.min().date())
    start_time = col2.time_input("Hora Inicial", df.index.min().time())
    end_date = col3.date_input("Data Final", df.index.max().date())
    end_time = col4.time_input("Hora Final", df.index.max().time())

    # Combinar a data e hora para formar o datetime completo
    start_datetime = pd.Timestamp.combine(start_date, start_time)
    end_datetime = pd.Timestamp.combine(end_date, end_time)

    # Filtrar o DataFrame pelo intervalo de tempo selecionado
    mask = (df.index >= start_datetime) & (df.index <= end_datetime)
    df_filtered = df.loc[mask]

    # Plotar o gráfico das colunas selecionadas em relação à data_hora usando Plotly
    if selected_columns:
        for i, column in enumerate(selected_columns):
            # Criar uma linha com duas colunas - uma para os inputs de limite e outra para o gráfico
            col_limite, col_grafico = st.columns([1, 20])  # A primeira coluna ocupa 5% e a segunda 95%

            with col_limite:
                # Adicionar entradas para definir a escala de cada variável no eixo y
                # st.write(f"Limites para {column}")
                max_val = st.number_input(f"Máx.", value=float(df_filtered[column].max()),
                                          key=f"max_{column}")
                min_val = st.number_input(f"Mín.", value=float(df_filtered[column].min()),
                                          key=f"min_{column}")


            with col_grafico:
                # Criar o gráfico da coluna específica e adicionar ao subplot
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_filtered.index, y=df_filtered[column], mode='lines', name=column))

                # Atualizar o layout para definir o intervalo do eixo y
                fig.update_yaxes(range=[min_val, max_val])
                fig.update_layout(title=f"{column} vs Data e Hora", height=300)

                # Plotar o gráfico no Streamlit
                st.plotly_chart(fig)

    # Mostrando o DataFrame no Streamlit
    st.write("#### Dados:")
    st.dataframe(df)

    # Algumas estatísticas básicas sobre o DataFrame
    st.write("#### Estatísticas Descritivas:")
    st.write(df.describe())

    # Informações da empresa compactadas
    engesep = {
        "title": 'EngeSEP Engenharia Integrada LTDA', "endereco": 'R. Roque Domingos Onghero, no 30d - Bom Retiro,Chapecó-SC',
        "CNPJ": 'CNPJ: 22.248.519/0001-26', "telefone": '(49)-991075958', "email": 'engesep@engesep.com.br'
    }
    engesep_str = " | ".join([f"{key}: {value}" for key, value in engesep.items()])
    st.write(engesep_str)


def filtrar_dados(df):
    # Filtrar os dados a partir de 17/09/2024 coluna 'data_hora' dos últimos 30 dias
    # df = df[df['data_hora'] > '2024-09-17']

    # Filtrar as colunas desejadas
    colunas = ['data_hora', 'tensao_fase_A', 'tensao_fase_B',  'tensao_fase_C', 'corrente_fase_A',
               'corrente_fase_B', 'corrente_fase_C', 'potencia_ativa', 'potencia_reativa',
               'tensao_excitacao', 'corrente_excitacao', 'temp_enrol_A',
               'temp_enrol_B', 'temp_enrol_C','temp_manc_rad_LA', 'temp_manc_rad_LNA', 'temp_gaxeteiro']
    df = df[colunas]

    # Renomear colunas para textos apresentáveis
    df.columns = [
        'Data e Hora', 'Tensão Fase A', 'Tensão Fase B',  'Tensão Fase C',
        'Corrente Fase A', 'Corrente Fase B', 'Corrente Fase C',
        'Potência Ativa', 'Potência Reativa', 'Tensão Excitação', 'Corrente Excitação',
        'Temp. Enrol. Fase A','Temp. Enrol. Fase B','Temp. Enrol. Fase C',
        'Temp. Mancal Radial LA', 'Temp. Mancal Radial LNA', 'Temp. Gaxeteiro'
    ]

    # Definir data_hora como index
    df.set_index('Data e Hora', inplace=True)

    # Ordenar os dados por data_hora
    df.sort_index(inplace=True)

    return df


if __name__ == "__main__":
    main()



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