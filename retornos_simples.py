import pandas as pd
import numpy as np

def compute_daily_returns(df):
    return df / df.shift(1) - 1

def compute_end_of_month_returns(df):
    df_ = df.reset_index()
    df_['year_month'] = df_['Dates'].str.slice(0,4) + '/' + df_['Dates'].str.slice(5,7)
    df_['day'] = df_['Dates'].str.slice(8,10)
    df_ = df_.sort_values(['year_month', 'day'])
    ultimos_dias_mes_df = df_.groupby('year_month').last()
    ultimos_dias_mes_df = ultimos_dias_mes_df.reset_index(False)
    ultimos_dias_mes_df = ultimos_dias_mes_df.drop(columns=['year_month', 'day']).set_index('Dates')
    retornos_mensuales_df = ultimos_dias_mes_df / ultimos_dias_mes_df.shift(1) - 1
    retornos_mensuales_df = retornos_mensuales_df[1:]
    return retornos_mensuales_df





##### Para correrlo desde la línea de comandos #####
import argparse
def main(precios, diarios_csv_name, mensuales_csv_name):
    prices_df = pd.read_csv(precios, index_col=0)

    daily_returns_df = compute_daily_returns(prices_df)
    daily_returns_df.to_csv(diarios_csv_name+'.csv')

    monthly_returns_df = compute_end_of_month_returns(prices_df)
    monthly_returns_df.to_csv(mensuales_csv_name+'.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Computes daily and monthly simple returns')
    parser.add_argument('--precios', help='file with the prices')
    parser.add_argument('--diarios_csv_name', help='name of the csv where the daily returns will be saved')
    parser.add_argument('--mensuales_csv_name', help='name of the csv where the monthly returns will be saved')
    args = parser.parse_args()
    main(args.precios, args.diarios_csv_name, args.mensuales_csv_name)