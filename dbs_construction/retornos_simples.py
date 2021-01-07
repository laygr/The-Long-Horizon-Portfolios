import pandas as pd
import numpy as np

def compute_end_of_month_returns(df):
    df_ = df.reset_index()
    df_['year'] = df_.Dates.dt.year
    df_['month'] = df_.Dates.dt.month
    df_['day'] = df_.Dates.dt.day
    df_ = df_.sort_values(['year', 'month', 'day'])
    ultimos_dias_mes_df = df_.groupby(['year','month']).last()
    ultimos_dias_mes_df = ultimos_dias_mes_df.sort_values(['year', 'month', 'day'])
    ultimos_dias_mes_df = ultimos_dias_mes_df.reset_index()
    ultimos_dias_mes_df = ultimos_dias_mes_df.drop(columns=['year', 'month', 'day']).set_index('Dates')
    retornos_mensuales_df = ultimos_dias_mes_df / ultimos_dias_mes_df.shift(1) - 1
    retornos_mensuales_df = retornos_mensuales_df[1:]
    return retornos_mensuales_df