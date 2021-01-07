import pandas as pd

def clip_series(s, lower, upper):
    return s.clip(lower=s.quantile(lower), upper=s.quantile(upper))


def main(df, lower, upper):
    df = df.copy()
    feature_list = list(['alpha', 'beta', 'miu_(i-rf)', 'miu_(m-rf)', 'se', 'sigma_(m-rf)'])

    for f in feature_list:
        df[f] = clip_series(df[f], lower, upper)

    return df

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Removes repeated values from excel file')
    parser.add_argument('--regressions', help='the path to the file with the regressions data')
    parser.add_argument('--lower', type=int, help='lower_limit')
    parser.add_argument('--upper', type=int, help='upper limit')
    args = parser.parse_args()
    
    data = pd.read_csv(args.regressions, index_col=0)

    lower = args.lower / 100.0
    upper = args.upper / 100.0
    if not (0 <= lower <= 1):
        raise Exception('Lower limit is not between 0 and 100')
    if not (0 <= upper <= 1):
        raise Exception('Upper limit is not between 0 and 100')

    result = main(data, lower, upper)
    result.to_csv(args.regressions.split('.csv')[0] + '_w_'+str(args.lower) + '_' + str(args.upper)+'.csv')