import pandas as pd
import linear_regression as linear_regression

def main(funds, index, rf):
    funds_df = pd.read_csv(funds, parse_dates=['Dates'], index_col=0)
    index_df = pd.read_csv(index, parse_dates=['Dates'], index_col=0)
    rf_df = pd.read_csv(rf, parse_dates=['Dates'], index_col=0)
    index_s = index_df.iloc[:,0]
    rf_s = rf_df.iloc[:,0]

    '''
    er_funds = funds_df.sub(rf_s,axis=0)
    er_index = index_s.sub(rf_s,axis=0)
    '''

    return linear_regression.many_capm(funds_df, index_s, rf_s)


import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transform daily anual rates to monthly rates')
    parser.add_argument('--funds', help='the path to the excel file with the rates')
    parser.add_argument('--index', help='the path to the excel file with the rates')
    parser.add_argument('--rf', help='the path to the excel file with the rates')
    parser.add_argument('--output', help='the path to the excel file with the rates')
    args = parser.parse_args()
    
    regressions_df = main(args.funds, args.index, args.rf)
    
    regressions_df.to_csv(args.output + '.csv')