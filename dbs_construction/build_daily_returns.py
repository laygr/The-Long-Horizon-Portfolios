import pandas as pd

import quitar_repetidos as qr
import remove_dying_returns
import pandas as pd


def main(prices_df, index, rf):
    print('Prices: ', prices_df.count().sum())

    funds = prices_df / prices_df.shift() - 1
    funds = funds[1:]
    print('Retornos diarios:', funds.count().sum())

    # Remove moribund returns
    funds = remove_dying_returns.do(funds)
    print('Después de quitar retornos moribundos:', funds.count().sum())

    # Return outliers
    funds = funds[funds.abs() < 0.2]
    print('Después de quitar outliers:', funds.count().sum())

    # Index
    index = index / index.shift() - 1
    index = index[1:]
    index = index.rename(columns={'NAFTRAC':'Index'})
    index = index[index['Index'].abs() < 0.2]
    index = index.dropna()

    # Risk Free
    rf = rf.reindex(index.index)
    rf = rf.ffill().dropna()
    rf = rf / 13 / 20 / 100 * 0.8

    print('Returns before (funds, index, risk free):', \
        funds.count().sum(), index.iloc[:,0].count(), rf.iloc[:,0].count())

    common_dates = set(funds.index) & set(index.index) & set(rf.index)
    funds = funds.loc[common_dates].sort_index()
    index = index.loc[common_dates].sort_index()
    rf = rf.loc[common_dates].sort_index()

    print('Returns after (funds, index, risk free):', \
        funds.count().sum(), len(index), len(rf))

    return funds, index, rf



import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--funds', help='the path to the csv file with the rates')
    parser.add_argument('--index', help='the path to the csv file with the rates')
    parser.add_argument('--rf', help='the path to the csv file with the rates')
    parser.add_argument('--funds_output', help='the path to the csv file with the rates')
    parser.add_argument('--index_output', help='the path to the csv file with the rates')
    parser.add_argument('--rf_output', help='the path to the csv file with the rates')


    args = parser.parse_args()

    prices = pd.read_csv(args.prices, parse_dates=['Dates'], index_col=0)
    index = pd.read_excel(args.index, parse_dates=['Dates'], index_col=0)
    rf = pd.read_excel(args.rf,       parse_dates=['Dates'], index_col=0)


    returns, index, rf = main(prices, index, rf)
    
    returns.to_csv(args.funds_output+'.csv')
    index.to_csv(args.index_output+'.csv')
    rf.to_csv(args.rf_output+'.csv')