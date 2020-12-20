import datetime
import pandas as pd

def delete_repeated_in_series(s, minimum_required):
    repeated = s.duplicated(keep='first')
    as_int_negated = (~repeated).astype(int)
    grouped = as_int_negated.groupby(as_int_negated.cumsum()).count()
    positions = grouped.cumsum() - grouped
    repeated_indexed = pd.DataFrame([grouped, positions], index=['Repeated', 'Position']).transpose()
    repeated_indexed['Repeated'] = repeated_indexed['Repeated']
    repeated_indexed['Position'] = repeated_indexed['Position']
    repeated_indexed = repeated_indexed[repeated_indexed['Repeated'] >= minimum_required]
    repeated_indexed['Date'] = s.index[repeated_indexed['Position']]
    repeated_indexed = repeated_indexed.set_index('Date')
    shifted_positions = repeated_indexed['Position'] + 1
    repeated_indexed['Value'] = s.iloc[shifted_positions].values
    repeated_indexed = repeated_indexed.dropna(how='any')
    repeated_indexed = repeated_indexed.reset_index()
    repeated_indexed = repeated_indexed[['Date', 'Value', 'Repeated', 'Position']]
    
    for _, row in repeated_indexed.iterrows():
        start = int(row['Position'] + 1)
        end   = int(row['Position'] + row['Repeated'])
        s.iloc[start:end] = None
    
    return repeated_indexed

def delete_repeated_in_df(df, minimun_required):
    df_copy = df.copy()
    acum = []
    for (columnName, s) in df_copy.iteritems():
        repeated = delete_repeated_in_series(s, minimum_required=4)
        repeated['Ticker'] = columnName
        acum.append(repeated)
    acum = pd.concat(acum)
    acum = acum[['Ticker', 'Date', 'Value', 'Repeated', 'Position']]
    return df_copy, acum

import argparse
def main(filepath, minimum_repeated, output_csv_name):
    df = pd.read_excel(filepath, index_col=0)
    sin_repetidos_df, repetidos_info = delete_repeated_in_df(df, minimum_repeated)
    sin_repetidos_df.to_csv(output_csv_name + '.csv')
    repetidos_info.to_csv(output_csv_name + '_info.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Removes repeated values from excel file')
    parser.add_argument('--filepath', help='the path to the excel file')
    parser.add_argument('--minimum_repeated', type=int, help='path to schema')
    parser.add_argument('--output_csv_name', help='name of the csv where the processed table will be saved')
    args = parser.parse_args()
    main(args.filepath, args.minimum_repeated, args.output_csv_name)