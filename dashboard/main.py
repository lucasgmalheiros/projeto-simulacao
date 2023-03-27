"""Dashboard com apresentação dos KPIs da central de atendimentos."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from datetime import date, datetime
from df_manipulation import clean_original_data, clean_arena_data


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --------------------------------------------------------------------------- #
# Base de dados reais de 2021
df = pd.read_csv("https://raw.githubusercontent.com/lucasgmalheiros"
                 "/projeto-simulacao-VCBC/main/calls.csv")
df = clean_original_data(df)
print(df.head())

# --------------------------------------------------------------------------- #
# Build the scatter plot
# fig = px.scatter(data_frame=df)

# --------------------------------------------------------------------------- #
# Layout do app
app.layout = dbc.Container([
    # Linha 1 - Header
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard Central de Atendimentos",
                    style={"text-align": "center"})
        ], width=12)
    ]),
    # Linha 2 - Seleção do dia e número de funcionários
    dbc.Row([
        dbc.Col([
            dcc.DatePickerSingle(
                id="my-date-picker",
                min_date_allowed=date(2021, 1, 1),
                max_date_allowed=date(2021, 12, 31),
                initial_visible_month=date(2021, 1, 1),
                date=date(2021, 1, 1)
            )
        ]),
        dbc.Col([
            dcc.Slider(
                id="my-slider",
                min=4,
                max=6,
                step=1,
                value=4
            )
        ])
    ]),
    # Linha 3 - Taxa de falha e tempo médio de espera
])

# --------------------------------------------------------------------------- #
# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
