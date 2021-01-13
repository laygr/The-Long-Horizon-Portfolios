import pandas as pd

def main(rf, n):
    dates = list(rf[0::n].index)
    s = pd.Series(dates, name='Dates')
    return s



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extracts the last day of each month from the daily prices db')
    parser.add_argument('--rf', help='the path to the excel file with the risk free rates')
    parser.add_argument('--n', type=int)
    parser.add_argument('--output', help='name of the csv where the processed table will be saved')
    args = parser.parse_args()

    rf = pd.read_excel(args.rf, parse_dates=['Dates'], index_col=0)
    days_every_n_weeks_series = main(rf, args.n)
    days_every_n_weeks_series.to_csv(args.output+'.csv', index=False, header=True)