import pandas as pd
import numpy as np

def compute_daily_returns(df):
    return df / df.shift(1) - 1

def compute_end_of_month_returns(df):
    df_ = df.reset_index()
    df_['year_month'] = df_['DATES'].str.slice(6,10) + '/' + df_['DATES'].str.slice(3,5)
    df_['day'] = df_['DATES'].str.slice(0,2)
    df_ = df_.sort_values(['year_month', 'day'])
    ultimos_dias_mes_df = df_.groupby('year_month').last()
    ultimos_dias_mes_df = ultimos_dias_mes_df.reset_index(False)
    ultimos_dias_mes_df = ultimos_dias_mes_df.drop(columns=['year_month', 'day']).set_index('DATES')
    retornos_mensuales_df = ultimos_dias_mes_df / ultimos_dias_mes_df.shift(1) - 1
    retornos_mensuales_df = retornos_mensuales_df[1:]
    return retornos_mensuales_df