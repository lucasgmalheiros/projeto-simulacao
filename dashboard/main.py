"""Dashboard com apresentação dos KPIs da central de atendimentos."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from datetime import date, datetime
from time import gmtime, strftime
from df_manipulation import clean_original_data, clean_arena_data


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --------------------------------------------------------------------------- #
# Base de dados reais de 2021
df = pd.read_csv("https://raw.githubusercontent.com/lucasgmalheiros"
                 "/projeto-simulacao-VCBC/main/calls.csv")
df = clean_original_data(df)
print(df.head())

# --------------------------------------------------------------------------- #
# Layout do app
app.layout = dbc.Container([
    # Linha 1 - Header
    dbc.Row([
        dbc.Col(html.H1("Dashboard Central de Atendimentos"),
                className="text-center", width=12)
    ]),
    # Linha 2 - Picker
    dbc.Row([
        dbc.Col(
            dcc.DatePickerSingle(
                id="my-date-picker",
                min_date_allowed=min(df["date"]),
                max_date_allowed=max(df["date"]),
                initial_visible_month=max(df["date"]),
                date=max(df["date"]),
                display_format='DD/MM/Y'
            ), width=6, className="text-center"),
        dbc.Col(
            dcc.Slider(
                id="my-slider",
                min=4, max=6, step=1
            ), width=6, className="text-center")
    ]),
    # Linha 3 - KPIs de percentual e clientes atendidos
    dbc.Row([
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader(html.H3("Atendimento em até 1 minuto (%)")),
                 dbc.CardBody(html.H2(id="output-percent-atendimento"))]
                    ), width=6, className="text-center"),
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader(html.H3("Número de chamados no dia")),
                 dbc.CardBody(html.H2(id="output-chamados"))]
                    ), width=6, className="text-center"),
    ]),
    # Linha 4 - KPIs de tempo médio de atendimento
    dbc.Row([
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader(html.H3("Tempo médio de atendimento (min)")),
                 dbc.CardBody(html.H2(id="output-media-atendimento"))]
                    ), width=6, className="text-center"),
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader(html.H3("Tempo médio de espera (min)")),
                 dbc.CardBody(html.H2(id="output-media-espera"))]
                    ), width=6, className="text-center"),
    ]),
    # Linha 5 - Taxa de abandono ("service_length" < 30s)
    dbc.Row([
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader(html.H3("Taxa de desistência (%)")),
                 dbc.CardBody(html.H2(id="output-percent-desistencia"))]
                    ), width=6, className="text-center"),
        dbc.Col(
            dbc.Card(
                [dbc.CardHeader(html.H3("Utilização operadores (%)")),
                 dbc.CardBody(html.H2(id="output-utilizacao"))]
                    ), width=6, className="text-center"),
    ]),
], className="mt-3")


# --------------------------------------------------------------------------- #
# Callbacks


@app.callback(
    [Output("output-percent-atendimento", "children"),
     Output("output-chamados", "children"),
     Output("output-media-atendimento", "children"),
     Output("output-media-espera", "children"),
     Output("output-percent-desistencia", "children"),
     Output("output-utilizacao", "children")],
    [Input("my-date-picker", "date")]
)
def update_kpis(data):
    """Calcula os KPIs de acordo com a data."""
    # Percentual atendido em até 1 minuto
    dff = df.loc[df["date"] == data]
    percent = dff["meets_standard"].mean()
    # Chamados por dia
    callers = df.groupby(["date"])["daily_caller"].max()[data]
    # Média tempo de atendimento
    media_atendimento = df.groupby(["date"])["service_length"].mean()[data]
    media_atendimento = strftime("%M:%S", gmtime(media_atendimento))
    # Média tempo de espera
    media_espera = df.groupby(["date"])["wait_length"].mean()[data]
    media_espera = strftime("%M:%S", gmtime(media_espera))
    # Taxa de desistência
    if len(dff) > 0:
        taxa_desistencia = len(df.loc[(df["service_length"] < 30) &
                                      (df["date"] == data)]) / len(dff)
    else:
        taxa_desistencia = 0
    # Percentual de utilização
    n_atendentes = 4
    horas_disponiveis = 10 * 60 * 60 * n_atendentes
    utilizacao = dff["service_length"].sum() / horas_disponiveis
    # Retorna os valores
    return (f"{percent * 100 :.2f}%", f"{callers}",
            f"{media_atendimento}", f"{media_espera}",
            f"{taxa_desistencia * 100 :.2f}%", f"{utilizacao * 100 :.2f}%")


# --------------------------------------------------------------------------- #
# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
