import pandas as pd

import quitar_repetidos as qr
import remove_dying_returns
import pandas as pd


def main(prices_df, minimum_repeated, days_every_4_weeks):
    print('Prices: ', prices_df.count().sum())
    
    # Delete repeated prices
    prices_df, repetidos_info = qr.delete_repeated_in_df(prices_df, minimun_required=minimum_repeated)
    print('Prices after deleting repeated prices:', prices_df.count().sum())

    # Compute 4 weeks returns
    acum_returns = []
    for fund_name in prices_df.columns:
        fund = prices_df[fund_name]
        fund_returns = {}
        for start, end in zip(days_every_4_weeks.index, days_every_4_weeks.index[1:]):
            chunk = fund.loc[start:end]
            days = len(chunk)
            days_with_price = chunk.count()
            if days_with_price == days and days >= 18:
                fund_returns[end] = fund.loc[end] / fund.loc[start] - 1
        
        acum_returns.append(pd.DataFrame.from_dict(fund_returns, orient='index', columns=[fund_name]))

    returns_4_weeks = pd.concat(acum_returns, axis=1)
    returns_4_weeks.index.name = 'Dates'

    print('Retornos 4 semanas:', returns_4_weeks.count().sum())

    # Remove moribund returns
    returns_4_weeks = remove_dying_returns.do(returns_4_weeks)
    print('Después de quitar retornos moribundos:', returns_4_weeks.count().sum())

    # Return outliers
    returns_4_weeks = returns_4_weeks[returns_4_weeks.abs() < 0.5]
    print('Después de quitar outliers:', returns_4_weeks.count().sum())

    return returns_4_weeks, repetidos_info



import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--prices', help='the path to the excel file with the rates')
    parser.add_argument('--minimum_repeated', type=int, help='path to schema')
    parser.add_argument('--days_every_4_weeks', help='the path to the excel file with the rates')
    parser.add_argument('--output', help='the path to the excel file with the rates')
    args = parser.parse_args()

    prices             = pd.read_excel(args.prices,             parse_dates=['Dates'], index_col=0)
    days_every_4_weeks = pd.read_csv(args.days_every_4_weeks, parse_dates=['Dates'], index_col=0)

    returns_4_weeks, repetidos_info = main(prices, args.minimum_repeated, days_every_4_weeks)
    returns_4_weeks.to_csv(args.output+'.csv')

    repetidos_info.to_csv(args.prices.split('.xlsx')[0] + '_repeated_info.csv', index=False)



