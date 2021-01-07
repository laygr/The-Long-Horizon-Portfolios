import pandas as pd

import argparse
def main(rates_df, col_index, last_day_months_df):
    last_days_dict = {(row.Year, row.Month): pd.Timestamp(row.Year, row.Month, row.Day) \
        for _,row in last_day_months_df.iterrows()}

    col_name = rates_df.columns[col_index]
    rates_df[col_name] = rates_df[col_name]/12/100
    rates_df['Year'] = rates_df['Dates'].dt.year
    rates_df['Month'] = rates_df['Dates'].dt.month
    rates_df = rates_df.groupby(['Year', 'Month']).last()
    rates_df = rates_df.reset_index()
    rates_df['Dates'] = rates_df.apply(lambda row:last_days_dict[(int(row.Year), int(row.Month))], axis=1)
    rates_df = rates_df.drop(columns=['Year', 'Month'])
    rates_df = rates_df.set_index('Dates')
    rates_df = rates_df.shift().dropna()
    rates_df = rates_df[[col_name]]
    rates_df = rates_df.rename(columns={col_name:'Risk Free'})
    return rates_df
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--rates', help='the path to the excel file with the rates')
    parser.add_argument('--col', type=int, help='the index of the column with the rates to be transformed')
    parser.add_argument('--last_days_months', help='the path to the excel file')
    parser.add_argument('--output', help='name of the csv where the processed table will be saved')
    args = parser.parse_args()

    last_day_months_df = pd.read_csv(args.last_days_months)
    rates_df = pd.read_excel(args.rates, parse_dates=['Dates'])
    risk_free_df = main(rates_df, args.col, last_day_months_df)
    risk_free_df.to_csv(args.output + '.csv', index=True)