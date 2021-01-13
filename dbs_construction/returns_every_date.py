import pandas as pd

def main(prices, dates, h):
    returns = {}
    days = {}
    for start, end in zip(dates.index, dates.index[1:]):
        chunk = prices.loc[start:end]
        chunk = chunk.dropna()
        days_with_price = len(chunk)
        print(days_with_price)
        if days_with_price >= h * 0.8:
            returns[end] = chunk.iloc[-1] / chunk.iloc[0] - 1
            days[end] = days_with_price

    returns_df = pd.DataFrame.from_dict(returns, orient='index', columns=[prices.name])
    returns_df.index.name = 'Dates'

    days_df = pd.DataFrame.from_dict(days, orient='index', columns=[prices.name])
    days_df.index.name = 'Dates'
    return returns_df, days_df[prices.name]

def with_days_per_chunk(prices, dates, h, days):
    returns = {}
    allowed_days = set(days.index)
    for start, end in zip(dates.index, dates.index[1:]):
        if not end in allowed_days: continue
        chunk = prices.loc[start:end]
        chunk = chunk.dropna()
        days_with_price = len(chunk)
        if days_with_price == days[end]:
            returns[end] = chunk.iloc[-1] / chunk.iloc[0] - 1

    returns_df = pd.DataFrame.from_dict(returns, orient='index', columns=[prices.name])
    returns_df.index.name = 'Dates'

    return returns_df