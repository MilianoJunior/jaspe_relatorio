from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
import os
import webbrowser
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import traceback

# load_dotenv()

info = {
    "Nome :": 'CGH JASPE',
    "Número de Turbinas :": 4,
    "Estado :": 'Santa Catarina',
    "Data Atual :": datetime.now().strftime("%Y-%m-%d"),
    "Localização :": 'Sao Miguel da Boa Vista, Estrada Sargento',
    "Potência :": 5.1,
}

engesep= {
    "title": 'EngeSEP Engenharia Integrada LTDA',
    "endereco": 'R. Roque Domingos Onghero, no 30d - Bom Retiro,Chapecó-SC',
    "CNPJ": 'CNPJ: 22.248.519/0001-26',
    "telefone":'(49)-991075958',
    "email": 'engesep@engesep.com.br'
}

DIR = os.path.dirname(os.path.abspath(__file__))
class PDF(FPDF):

    def __init__(self, dfs, logger=None):
        self.info = info
        self.dfs = dfs
        super().__init__()
        self.orientation = 'P'
        self.unit = 'mm'
        self.format = 'A4'
        self.fonte = 'helvetica'
        self.resolucao = int(2)
        self.logger = logger

    def error(self, err):
        tb = traceback.extract_tb(err.__traceback__)
        # Pegando o último nível do traceback (onde a exceção ocorreu)
        filename = tb[-1].filename
        line_no = tb[-1].lineno
        method_name = tb[-1].name
        self.logger.error(f"Erro: {err} - {filename} - {line_no} - {method_name}")
        raise Exception(f"Erro: {err} - {filename} - {line_no} - {method_name}")

    def compose(self):
        try:
            self.add_paginas({'values': 'UG-01'})
        except Exception as e:
            self.error(e)
    def add_paginas(self, values):
        try:
            name = values['values']
            UG = name #.split('_')[0].upper()
            title = f"Relatório - EngeSEP  {UG}" # - {UG}
            self.add_page()
            self.chapter_title(title)
            self.sub_title('Informações Gerais')
            self.simple_table()
            self.sub_title('Informações quantitativas')
            self.chapter_body(values['statistics'], UG)
        except Exception as e:
            self.error(e)

    def header(self):
        try:
            self.set_margins(20,20,20)
            img_path = os.path.join(DIR,'logo.png')
            fonte = "helvetica"
            self.image(img_path, 20, 20, 35)
            self.set_font(fonte, 'B', size=10)
            self.set_text_color(18, 27, 44)
            for key, value in engesep.items():
                if key == "telefone":
                    self.set_font(fonte, 'B', 8)
                    value += '  ' + engesep["email"]  # Concatena telefone e email
                elif key == "email":
                    continue  # Já tratamos o email junto com o telefone
                self.cell(40)
                self.cell(10, 4, value, 0, 1, 'L')
            self.ln(3)
        except Exception as e:
            self.error(e)

    def chapter_title(self, title):
        try:
            self.set_font(self.fonte, 'B', 12)
            self.set_text_color(244, 244, 244)
            self.set_fill_color(10, 10, 10)
            self.cell(0, 6, title, 0, 1, 'L', True)
            self.ln(4)
        except Exception as e:
            self.error(e)

    def sub_title(self, label):
        try:
            self.set_font(self.fonte, '', 10)
            self.set_fill_color(18, 27, 44)
            self.set_text_color(255, 246, 247)
            self.cell(0, 5,label, 0, 1, 'L', 1)
            self.ln(1)
        except Exception as e:
            self.error(e)

    def footer(self):
        try:
            data_atual = datetime.now()
            data_e_hora = data_atual.strftime('%d/%m/%Y %H:%M')
            self.set_fill_color(243, 245, 247)
            self.set_y(-15)
            self.set_font(self.fonte, 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, 'relatório gerado em '+str(data_e_hora)+ ' Página ' + str(self.page_no()), 0, 0, 'C')
            self.ln(3)
            self.cell(0, 10, 'Os valores referentes à produção de energia são obtidos a partir de dados operacionais.', 0, 0, 'C')
        except Exception as e:
            self.error(e)



# for key, value in self.dfs.items():
#     if 'energia' in key:
#         self.grafico_energia(value['values'])
#     if 'nivel' in key:
#         self.grafico_nivel(value['values'])
# for key, value in self.dfs.items():
#     if 'energia' in key:

# def simple_table(self, spacing=1):
#     try:
#         self.set_text_color(18, 27, 44)
#         self.set_font(self.fonte, size=10)
#         line_height = self.font_size * 1.5
#         col_width_ = round(self.epw / 2,2) # distribute content evenly
#         data = []
#         for key, value in self.info.items():
#             data.append([key, value])
#         for row in data:
#             for datum in row:
#                 col_width = round(max(40, self.get_string_width(datum) +5),2)
#                 self.multi_cell(col_width, line_height, datum, border=0, ln=3, align='L', max_line_height=self.font_size)
#             self.ln(line_height)
#         self.ln(1)
#     except Exception as e:
#         self.error(e)

# def chapter_body(self, stats, UG):
#     try:
#         arquivo = UG+'.png'
#         energia_img = os.path.join(DIR, '..', 'assets', arquivo)
#         self.image(energia_img, 100, 108, 87)
#         self.set_font(self.fonte, '', 8)
#         self.set_text_color(244, 244, 244)
#         self.set_fill_color(10, 10, 10)
#         self.cell(80, 5,'Relatório de energia', 0, 0, 'L', True)
#         self.ln()
#         self.set_fill_color(243, 245, 247)
#         self.set_text_color(18, 27, 44)
#         for key, value in stats.items():
#             self.cell(80, 5, key+': '+str(round(value[0],self.resolucao))+' MW/h', 0, 0, 'L', True)
#             self.ln()
#         self.set_text_color(244, 244, 244)
#         self.set_fill_color(10, 10, 10)
#         self.cell(80, 5,'Relatório de nível de águas', 0, 0, 'L', True)
#         self.ln()
#         self.set_fill_color(243, 245, 247)
#         self.set_text_color(18, 27, 44)
#         for key, value in self.dfs.items():
#             if 'nivel' in key:
#                 for key, value in value['statistics'].items():
#                     self.cell(80, 5, key+': '+str(round(value[0],self.resolucao))+' m', 0, 0, 'L', True)
#                     self.ln()
#         self.set_text_color(244, 244, 244)
#         self.set_fill_color(10, 10, 10)
#         self.cell(80, 5,'Gráfico nível de águas', 0, 0, 'L', True)
#         self.ln()
#         self.ln(10)
#         ly = self.get_y()
#         self.image(self.nivel_img,20,round(ly), 80)
#     except Exception as e:
#         self.error(e)

# def grafico_energia(self, dados):
#     try:
#         # Plotando o gráfico
#         # Convert the index to datetime if it's not already
#         if not isinstance(dados.index, pd.DatetimeIndex):
#             dados.index = pd.to_datetime(dados.index)
#
#         # Now you can format it as you like
#         dados.index = dados.index.strftime('%d/%m')
#
#         # Index(['22/01', '23/01', '24/01', '25/01'], dtype='object', name='data_hora')
#         name = dados.columns[0]
#         sns.set_theme(style="whitegrid")
#         f, ax = plt.subplots(figsize=(6, 13))
#         # ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
#         sns.set_color_codes("pastel")
#         sns.barplot(x=name, y=dados.index, data=dados, label="Energia em MW/h", color="b")
#         ax.bar_label(ax.containers[0], label_type='center')
#         ax.legend(ncol='', loc="lower right", frameon=True)
#         UG = name.split('_')[0].upper()
#         ax.set(xlim=(0, max(dados[name].values)), ylabel="Dias do mês",
#                xlabel="Geração de Energia em MW/h", title=f'Geração de energia: {UG}')
#         sns.despine(left=True, bottom=True)
#
#         arquivo = UG+'.png'
#         energia_img = os.path.join(DIR, '..', 'assets', arquivo)
#         plt.savefig(energia_img, bbox_inches='tight')
#     except Exception as e:
#         self.error(e)

# def grafico_nivel(self, dados):
#     try:
#         dados.index = dados.index.strftime('%d')
#         name = dados.columns[0]
#         sns.set_style("whitegrid")
#         f, ax = plt.subplots(figsize=(10, 9))
#         sns.set_color_codes("pastel")
#         g = sns.relplot(x=dados.index, y=name, kind="line", errorbar="sd", markers=True, data=dados).set_titles(
#             "Nível do reservatório de águas")
#         g.set_axis_labels("Dias do mês", "Volume de águas em metros")
#
#         # Rotaciona as etiquetas e configura o espaçamento entre elas
#         g.set_xticklabels(rotation=45)
#
#         num_points = len(dados.index)
#         every_nth = 5
#         g.set(xticks=dados.index[::every_nth])
#
#         self.nivel_img = os.path.join(DIR, '..', 'assets', 'nivel.png')
#         plt.savefig(self.nivel_img, bbox_inches='tight')
#         plt.close()
#     except Exception as e:
#         self.error(e)
































