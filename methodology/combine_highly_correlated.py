import pandas as pd
import numpy as np



def merge_series_in_group(funds, group):
    #print('before', funds[group['Fund']].count())
    merged = funds[group['Fund']].mean(axis=1, skipna=True)
    return merged
    #print('after', merged.count())

def main(funds, threshold):
    funds_names = funds.columns
    print('Funds before combining:', len(funds.columns))
    print('Returns before combining:', funds.count().sum())
    correls_matrix = funds.corr()

    correls_matrix[correls_matrix < threshold] = None
    np.fill_diagonal(correls_matrix.values, None)
    edges = correls_matrix.unstack().dropna()

    counts = funds.count()
    days_with_price = {}
    for column in funds_names:
        days_with_price[column] = set(funds[column].dropna().index)

    explored = set()
    group_counter = 0
    groups = {}
    for fund_name in funds_names:
        if fund_name in explored: continue
        group_counter += 1
        acum = set()
        dfs(fund_name, explored, edges, acum, days_with_price, counts)
        groups[group_counter] = list(acum)

    data = []
    for group_number, fund_names in groups.items():
        for fund_name in fund_names:
            data.append([group_number, fund_name])
    groups_df = pd.DataFrame(data, columns=['Group', 'Fund'])

    result = groups_df.groupby('Group').apply(lambda group:merge_series_in_group(funds, group)).transpose()
    result.columns = groups_df.groupby('Group').first()['Fund']

    print('Funds after combining:', len(result.columns))
    print('Returns after combining:', result.count().sum())
    return result, groups_df



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Splits the regressions in filtered and eliminated')
    parser.add_argument('--funds',                  help='path to the file with the regressions data')
    parser.add_argument('--filtered_by_metadata',   help='path to the file with the regressions data')
    parser.add_argument('--threshold', type=float,  help='path to the file with the regressions data')
    args = parser.parse_args()
    
    funds                 = pd.read_csv(args.funds,  parse_dates=['Dates'], index_col=0)
    filtered_by_metadata  = pd.read_csv(args.filtered_by_metadata,          index_col=0)
    funds = funds[filtered_by_metadata.index]
    combined_funds, groups_df = main(funds, args.threshold)
    combined_funds.to_csv(args.funds.split('.csv')[0] + '_c.csv')
    groups_df.to_csv(args.funds.split('.csv')[0] + '_groups.csv')