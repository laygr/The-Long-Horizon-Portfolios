import pandas as pd
from collections import defaultdict

def find_holes(df, min_hole_size = 16):
    notnulls = df.notnull().astype(int)
    cumsums = df.notnull().astype(int).cumsum()
    size = len(df)
    acum = []
    for fund_name in df.columns:
        huecos = notnulls[fund_name].groupby(cumsums[fund_name]).count()
        huecos = pd.concat([huecos, huecos.cumsum()], axis=1, keys=['tamaño', 'end pos'])
        huecos['start pos'] = huecos['end pos'] - huecos['tamaño']
        #huecos = huecos[(huecos['tamaño'] >= min_hole_size) & (huecos['start pos'] > 0) & (huecos['end pos'] < size)]
        huecos = huecos[(huecos['tamaño'] >= min_hole_size) & (huecos['start pos'] > 0)]
        huecos['fund'] = fund_name
        huecos = huecos.reset_index(drop=True)
        acum.append(huecos)
    return pd.concat(acum).reset_index(drop=True)

def find_moribund_dates(s, k, h):
    s_abs = s.abs()
    k = 0.003
    h = 8
    moribund_dates = set()
    for i in range(len(s)-h):
        sub_series = s_abs.iloc[i:i+h]
        smaller_than_threshold = len(sub_series[sub_series < k])
        if smaller_than_threshold >= int(len(sub_series) * 0.8):
            moribund_dates = moribund_dates.union(set(sub_series.index))
    return moribund_dates

def delete_moribund_returns_from_holes(df, holes):
    to_remove = defaultdict(list)
    
    prior_len = len(df)
    for ith, hole in holes.iterrows():
        if ith > 0 and holes.loc[ith-1]['fund'] == hole['fund']:
            series_start = holes.loc[ith-1]['end pos']
        else:
            series_start = 0
        fund_name = hole['fund']
        s = df[fund_name].iloc[series_start:hole['start pos']].dropna()
        moribund_dates = find_moribund_dates(s, k=0.003, h=8)
        if len(moribund_dates) == 0: continue
        to_remove[fund_name].append(s.loc[moribund_dates].copy())
        df[fund_name].loc[moribund_dates] = None
        
    return to_remove

def delete_moribund_returns_from_series_without_holes(df, holes):
    to_remove = defaultdict(list)
    funds_with_holes = set(holes['fund'].tolist())
    for fund_name in df.columns:
        if fund_name in funds_with_holes: continue
        s = df[fund_name].dropna()
        moribund_dates = find_moribund_dates(s, k=0.003, h=10)
        if len(moribund_dates) == 0: continue
        to_remove[fund_name].append(s.loc[moribund_dates].copy())
        df[fund_name].loc[moribund_dates] = None
    return to_remove

def do(df):
    df_copy = df.copy()
    holes = find_holes(df_copy, min_hole_size=3)
    removed_from_series_with_holes = delete_moribund_returns_from_holes(df_copy, holes)
    removed_from_series_without_holes = delete_moribund_returns_from_series_without_holes(df_copy, holes)

    return df_copy