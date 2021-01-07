import pandas as pd

def main(funds, index, rf):
    index_s = index.iloc[:,0]
    rf_s = rf.iloc[:,0]

    print('Returns before (funds, index, risk free):', \
        funds.count().sum(), index_s.count(), rf_s.count())

    common_dates = set(funds.index) & set(index.index) & set(rf.index)
    funds = funds.loc[common_dates].sort_index()
    index = index.loc[common_dates].sort_index()
    rf = rf.loc[common_dates].sort_index()

    print('Returns after (funds, index, risk free):', \
        funds.count().sum(), len(index), len(rf))

    return funds, index, rf



import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Selects the dates that are common among the 3 databases')
    parser.add_argument('--funds', help='the path to the excel file with the rates')
    parser.add_argument('--index', help='the path to the excel file with the rates')
    parser.add_argument('--rf', help='the path to the excel file with the rates')
    parser.add_argument('--output_sufix', help='the path to the excel file with the rates')
    args = parser.parse_args()


    funds_df = pd.read_csv(args.funds, parse_dates=['Dates'], index_col=0)
    index_df = pd.read_csv(args.index, parse_dates=['Dates'], index_col=0)
    rf_df    = pd.read_csv(args.rf,    parse_dates=['Dates'], index_col=0)
    
    funds_df, index_df, rf_df = main(funds_df, index_df, rf_df)

    funds_df.to_csv(args.funds.split('.csv')[0] + '_' + args.output_sufix + '.csv')
    index_df.to_csv(args.index.split('.csv')[0] + '_' + args.output_sufix + '.csv')
    rf_df.to_csv(args.rf.split('.csv')[0] + '_' + args.output_sufix + '.csv')

    