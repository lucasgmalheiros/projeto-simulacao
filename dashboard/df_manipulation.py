"""Funções de tratamento de dados para serem utilizadas no dashboard."""
import pandas as pd
from datetime import datetime
import numpy as np


def clean_original_data(df: pd.DataFrame) -> pd.DataFrame:
    """Realiza o tratamento do dataframe original."""
    # Conversão do time stamp da data
    df["date"] = pd.to_datetime(df.date, format="%d/%m/%Y")
    df["call_started"] = pd.to_datetime(df.call_started, format="%I:%M:%S %p")

    # Cálculo dos tempos entre chegadas
    df["arrival_time_diff"] = df["call_started"].diff().dt.total_seconds()

    # Substitui os valores inadequados por 0
    df.loc[df["arrival_time_diff"] < 0, "arrival_time_diff"] = 0
    df = df.fillna(0)

    # Remove colunas que não serão mais utilizadas
    df = df.drop(columns=["call_id", "call_started",
                          "call_answered", "call_ended"])
    return df


def clean_arena_data(df: pd.DataFrame) -> pd.DataFrame:
    """Tratamento do arquivo .csv do Arena."""
    # Removendo coluna fantasma
    df = df.drop('Unnamed: 5', axis=1)

    # Ajustando os tipos das ligações
    df.loc[df["call_type"] == 2, "call_type"] = 0
    df.loc[df["call_type"] == 3, "call_type"] = 2

    # Tempos de serviço e de espera
    df["wait_length"] = df["call_answered"] - df["call_started"]
    df["service_length"] = df["call_ended"] - df["call_answered"]

    # Meets standard
    df["meets_standard"] = np.where(df["wait_length"] <= 60, True, False)

    # Ordenando o DataFrame de acordo com a ordem de chegada
    df = df.sort_values(by=["replication", "call_started"])
    df = df.reset_index(drop=True)

    # Coluna de ligação diária
    df['daily_caller'] = df.groupby('replication').cumcount() + 1

    # Define a data inicial e final
    start_date = datetime(2022, 1, 1)  # O primeiro dia útil de 2021
    end_date = datetime(2022, 12, 31)  # O último dia útil de 2021

    # Cria um DataFrame com um intervalo de datas úteis
    df_dates = pd.DataFrame(pd.date_range(start_date, end_date, freq='B'),
                            columns=['date'])

    # Adiciona uma coluna com o número de dias úteis desde o início do ano
    df_dates['replication'] = df_dates.index + 1

    # Mescla com o DataFrame de datas
    df_merged = pd.merge(df, df_dates, on='replication')
    df = df_merged.copy()

    # Reordenando colunas
    df = df.reindex(columns=['replication', 'date',
                             'daily_caller', 'call_started',
                             'call_answered', 'call_ended', 'wait_length',
                             'service_length', 'meets_standard', 'call_type'])

    # Tempos entre chegadas
    df["arrival_time_diff"] = df["call_started"].diff()
    df.loc[df["arrival_time_diff"] < 0, "arrival_time_diff"] = 0
    df = df.fillna(0)

    # Remove colunas que não serão mais utilizadas
    df = df.drop(columns=["replication", "call_started",
                          "call_answered", "call_ended"])

    # Retorna dataframe organizado
    return df


def upload_db() -> pd.DataFrame:
    """Carrega os arquivos csv do GitHub."""
    # Base de dados reais de 2021
    dr = pd.read_csv(
        "https://raw.githubusercontent.com/"
        "lucasgmalheiros/simulacao-call-center/main/calls.csv"
        )
    dr = clean_original_data(dr)
    dr["workers"] = 0

    # dados simulados com 4 trabalhadores
    da4 = pd.read_csv(
        "https://raw.githubusercontent.com/lucasgmalheiros/"
        "simulacao-call-center/main/arena/modelo-2022/output_call_center_4.csv"
        )
    da4 = clean_arena_data(da4)
    da4["workers"] = 4

    # dados simulados com 5 trabalhadores
    da5 = pd.read_csv(
        "https://raw.githubusercontent.com/lucasgmalheiros/"
        "simulacao-call-center/main/arena/modelo-2022/output_call_center_5.csv"
        )
    da5 = clean_arena_data(da5)
    da5["workers"] = 5

    # dados simulados com 6 trabalhadores
    da6 = pd.read_csv(
        "https://raw.githubusercontent.com/lucasgmalheiros/"
        "simulacao-call-center/main/arena/modelo-2022/output_call_center_6.csv"
        )
    da6 = clean_arena_data(da6)
    da6["workers"] = 6

    # dados simulados com 7 trabalhadores
    da7 = pd.read_csv(
        "https://raw.githubusercontent.com/lucasgmalheiros/"
        "simulacao-call-center/main/arena/modelo-2022/output_call_center_7.csv"
        )
    da7 = clean_arena_data(da7)
    da7["workers"] = 7

    # dados simulados com 8 trabalhadores
    da8 = pd.read_csv(
        "https://raw.githubusercontent.com/lucasgmalheiros/"
        "simulacao-call-center/main/arena/modelo-2022/output_call_center_8.csv"
        )
    da8 = clean_arena_data(da8)
    da8["workers"] = 8

    # dados simulados com 9 trabalhadores
    da9 = pd.read_csv(
        "https://raw.githubusercontent.com/lucasgmalheiros/"
        "simulacao-call-center/main/arena/modelo-2022/output_call_center_9.csv"
        )
    da9 = clean_arena_data(da9)
    da9["workers"] = 9

    # Junção dos dataframes
    d_merge = pd.concat([dr, da4, da5, da6, da7, da8, da9],
                        ignore_index=True, sort=False)

    return d_merge
