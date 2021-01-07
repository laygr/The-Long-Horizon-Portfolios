import retornos_simples as rs
import pandas as pd
import argparse

def main(index, days_every_4_weeks):
    index_returns = {}
    index_prices = index[index.columns[0]]
    for start, end in zip(days_every_4_weeks.index, days_every_4_weeks.index[1:]):
        chunk = index_prices.loc[start:end]
        days = len(chunk)
        days_with_price = chunk.count()
        if days_with_price == days and days >= 18:
            index_returns[end] = index_prices.loc[end] / index_prices.loc[start] - 1
    index_4_weeks_returns = pd.DataFrame.from_dict(index_returns, orient='index', columns=['Index'])
    index_4_weeks_returns.index.name = 'Dates'
    return index_4_weeks_returns

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--prices', help='the path to the excel file with the rates')
    parser.add_argument('--days_every_4_weeks', help='the path to the excel file with the rates')
    parser.add_argument('--output', help='the path to the excel file with the rates')
    args = parser.parse_args()

    index              = pd.read_excel(args.prices,             parse_dates=['Dates'], index_col=0)
    days_every_4_weeks = pd.read_csv(args.days_every_4_weeks, parse_dates=['Dates'], index_col=0)

    index_4_weeks_returns = main(index, days_every_4_weeks)
    index_4_weeks_returns.to_csv(args.output+'.csv')
    