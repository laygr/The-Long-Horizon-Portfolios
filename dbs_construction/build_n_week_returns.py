import pandas as pd

import quitar_repetidos as qr
import remove_dying_returns
import pandas as pd
import returns_every_date


def main(prices_df, index, rf, n, days_every_n_weeks):

    # --- INDEX ----
    index = index.rename(columns={'NAFTRAC':'Index'})
    index, days_index = returns_every_date.main(index['Index'], days_every_n_weeks, h=5*n)
    index = index[index['Index'].abs() < 0.2]

    
    # --- RISK FREE ---
    rf = rf.reindex(index.index)
    rf = rf.ffill().dropna()
    rf = rf / 13 / 4 / 100 * 0.8 * n

    # --- FUNDS ---
    print('Prices: ', prices_df.count().sum())
    # Compute n weeks returns
    acum_returns = []
    for fund_name in prices_df.columns:
        fund = prices_df[fund_name]
        fund_returns = returns_every_date.with_days_per_chunk(fund, days_every_n_weeks, 5*n, days_index)
        acum_returns.append(fund_returns)
    funds = pd.concat(acum_returns, axis=1)
    funds.index.name = 'Dates'
    print('Retornos:', funds.count().sum())

    # Remove moribund returns
    funds = remove_dying_returns.do(funds)
    print('Después de quitar retornos moribundos:', funds.count().sum())

    # Return outliers
    funds = funds[funds.abs() < 0.2]
    print('Después de quitar outliers:', funds.count().sum())
    
    return funds, index, rf


import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--funds')
    parser.add_argument('--index')
    parser.add_argument('--rf')
    parser.add_argument('--n', type=int)
    parser.add_argument('--dates_every_n_week')
    parser.add_argument('--funds_output')
    parser.add_argument('--index_output')
    parser.add_argument('--rf_output')
    args = parser.parse_args()

    days_every_n_weeks = pd.read_csv(args.dates_every_n_week, parse_dates=['Dates'], index_col=0)
    funds = pd.read_csv(args.funds,   parse_dates=['Dates'], index_col=0)
    index = pd.read_excel(args.index, parse_dates=['Dates'], index_col=0)
    rf = pd.read_excel(args.rf,       parse_dates=['Dates'], index_col=0)

    funds, index, rf = main(funds, index, rf, args.n, days_every_n_weeks)
    
    index.to_csv(args.index_output+'.csv')
    funds.to_csv(args.funds_output+'.csv')
    rf.to_csv(args.rf_output+'.csv')