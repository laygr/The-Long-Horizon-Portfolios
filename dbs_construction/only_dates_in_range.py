import pandas as pd
import datetime

def main(funds, index, rf, first_date, last_date):
    index_s = index.iloc[:,0]
    rf_s = rf.iloc[:,0]

    print('Returns before (funds, index, risk free):', \
        funds.count().sum(), index_s.count(), rf_s.count())

    def is_in_range(date):
        return first_date <= date <= last_date

    common_dates = set(funds.index) & set(index.index) & set(rf.index)
    common_dates = sorted(list(common_dates))
    dates_in_range = list(filter(is_in_range, common_dates))
    funds = funds.loc[dates_in_range].sort_index()
    index = index.loc[dates_in_range].sort_index()
    rf    = rf.loc[dates_in_range].sort_index()

    print('Returns after (funds, index, risk free):', \
        funds.count().sum(), len(index), len(rf))

    return funds, index, rf



import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Selects the dates that are common among the 3 databases')
    parser.add_argument('--funds')
    parser.add_argument('--index')
    parser.add_argument('--rf')
    parser.add_argument('--first_date')
    parser.add_argument('--last_date')

    parser.add_argument('--output_suffix')
    args = parser.parse_args()


    funds_df = pd.read_csv(args.funds, parse_dates=['Dates'], index_col=0)
    index_df = pd.read_csv(args.index, parse_dates=['Dates'], index_col=0)
    rf_df    = pd.read_csv(args.rf,    parse_dates=['Dates'], index_col=0)

    first_date_arr = args.first_date.split('-')
    first_date_arr = [int(x) for x in first_date_arr]
    first_date = datetime.date(first_date_arr[0], first_date_arr[1], first_date_arr[2])

    last_date_arr = args.last_date.split('-')
    last_date_arr = [int(x) for x in last_date_arr]
    last_date = datetime.date(last_date_arr[0], last_date_arr[1], last_date_arr[2])
    
    funds_df, index_df, rf_df = main(funds_df, index_df, rf_df, first_date, last_date)

    funds_df.to_csv(args.funds.split('.csv')[0] + '_' + args.output_suffix + '.csv')
    index_df.to_csv(args.index.split('.csv')[0] + '_' + args.output_suffix + '.csv')
    rf_df.to_csv(args.rf.split('.csv')[0] + '_' + args.output_suffix + '.csv')

    