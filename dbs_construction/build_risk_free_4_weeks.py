import pandas as pd

import argparse
def main(rf):
    return (rf[0::4].shift() / 100 / 13 * 0.80)[1:]
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--rates', help='the path to the excel file with the rates')
    parser.add_argument('--output', help='name of the csv where the processed table will be saved')
    args = parser.parse_args()

    rates_df = pd.read_excel(args.rates, parse_dates=['Dates'], index_col=0)
    risk_free_df = main(rates_df)#, args.col, last_day_months_df)
    risk_free_df.to_csv(args.output + '.csv', index=True)