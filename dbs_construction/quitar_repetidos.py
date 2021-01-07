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
    repeated_indexed['Dates'] = s.index[repeated_indexed['Position']]
    repeated_indexed = repeated_indexed.set_index('Dates')
    shifted_positions = repeated_indexed['Position'] + 1
    repeated_indexed['Value'] = s.iloc[shifted_positions].values
    repeated_indexed = repeated_indexed.dropna(how='any')
    repeated_indexed = repeated_indexed.reset_index()
    if repeated_indexed.empty: return repeated_indexed
    repeated_indexed = repeated_indexed[['Dates', 'Value', 'Repeated', 'Position']]
    
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
    acum = acum[['Ticker', 'Dates', 'Value', 'Repeated', 'Position']]
    return df_copy, acum