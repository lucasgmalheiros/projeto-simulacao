"""Funções de tratamento de dados para serem utilizadas no dashboard."""
import pandas as pd
from datetime import datetime
import numpy as np


def clean_original_data(df):
    """
    Realiza o tratamento do dataframe para converter as datas e calcular
    tempos entre chegadas.
    """
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


def clean_arena_data(df):
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
    start_date = datetime(2021, 1, 1)  # O primeiro dia útil de 2021
    end_date = datetime(2021, 12, 31)  # O último dia útil de 2021

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
