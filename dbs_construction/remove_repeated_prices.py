import pandas as pd

import quitar_repetidos as qr
import remove_dying_returns
import pandas as pd


def main(prices_df, minimum_repeated):
    print('Prices: ', prices_df.count().sum())
    
    # Delete repeated prices
    prices_df, repetidos_info = qr.delete_repeated_in_df(prices_df, minimun_required=minimum_repeated)
    print('Prices after deleting repeated prices:', prices_df.count().sum())

    return prices_df, repetidos_info



import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--prices', help='the path to the excel file with the rates')
    parser.add_argument('--minimum_repeated', type=int, help='path to schema')
    parser.add_argument('--output', help='the path to the excel file with the rates')
    args = parser.parse_args()

    prices = pd.read_excel(args.prices, parse_dates=['Dates'], index_col=0)

    prices_df, repetidos_info = main(prices, args.minimum_repeated)
    
    prices_df.to_csv(args.output+'.csv')
    repetidos_info.to_csv(args.prices.split('.xlsx')[0] + '_repeated_info.csv', index=False)