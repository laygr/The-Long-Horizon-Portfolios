import retornos_simples as rs
import quitar_repetidos as qr
import remove_dying_returns
import pandas as pd

def main(prices_df, minimum_repeated, last_days_months_df):
    print('Prices: ', prices_df.count().sum())
    
    prices_df, repetidos_info = qr.delete_repeated_in_df(prices_df, minimun_required=minimum_repeated)
    print('Prices after deleting repeated prices:', prices_df.count().sum())

    prices_df = prices_df.reset_index()
    # Retornos mensuales:
    prices_df['Year']  = prices_df.Dates.dt.year
    prices_df['Month'] = prices_df.Dates.dt.month
    prices_df['Day']   = prices_df.Dates.dt.day

    merged  = prices_df.merge(last_days_months_df, on=['Year', 'Month', 'Day'])
    merged  = merged.sort_values(['Year', 'Month', 'Day'])
    merged  = merged.drop(columns=['Year', 'Month', 'Day']).set_index('Dates')
    returns = merged / merged.shift(1) - 1
    returns = returns[1:]
    print('Retornos mensuales:', returns.count().sum())

    # Remove moribund returns
    returns = remove_dying_returns.do(returns)
    print('Después de quitar retornos moribundos:', returns.count().sum())

    # Return outliers
    returns = returns[returns.abs() < 0.5]
    print('Después de quitar outliers:', returns.count().sum())

    return returns, repetidos_info



import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Computes daily and monthly simple returns')
    parser.add_argument('--precios', help='file with the prices')
    parser.add_argument('--minimum_repeated', type=int, help='path to schema')
    parser.add_argument('--last_days_months', help='name of the csv with the last days of each month')
    parser.add_argument('--output', help='name of the csv where the monthly returns will be saved')
    args = parser.parse_args()

    last_days_months_df = pd.read_csv(args.last_days_months)
    prices_df = pd.read_excel(args.precios, parse_dates=['Dates'], index_col=0)
    returns, repetidos_info = main(prices_df, args.minimum_repeated, last_days_months_df)

    repetidos_info.to_csv(args.precios.split('.xlsx')[0] + '_repeated_info.csv', index=False)
    returns.to_csv(args.output + '.csv')