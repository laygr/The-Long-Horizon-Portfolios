import pandas as pd

def main(prices_df):
    prices_df['Year'] = prices_df['Dates'].dt.year
    prices_df['Month'] = prices_df['Dates'].dt.month
    prices_df['Day'] = prices_df['Dates'].dt.day
    last_days_df = prices_df.groupby(['Year', 'Month']).last()['Day'].reset_index()
    return last_days_df



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracts the last day of each month from the daily prices db')
    parser.add_argument('--prices', help='the path to the excel file with the rates')
    parser.add_argument('--output', help='name of the csv where the processed table will be saved')
    args = parser.parse_args()

    prices_df = pd.read_excel(args.prices, parse_dates=['Dates'])
    last_days_df = main(prices_df)
    last_days_df.to_csv(args.output+'.csv', index=False)