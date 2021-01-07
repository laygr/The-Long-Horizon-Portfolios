import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import math

def capm(security_series, market_series, rf_series):
    data = pd.concat([security_series, market_series, rf_series], axis=1, keys=['Xi', 'Xm', 'rf']).dropna(how='any')
    if len(data) < 3:
        return [security_series.name] + [None] * 13 + [len(data)]
    data['Xi - rf'] = data['Xi'] - data['rf']
    data['Xm - rf'] = data['Xm'] - data['rf']
    X = data['Xm - rf'].values.reshape(-1, 1)
    Y = data['Xi - rf'].values.reshape(-1, 1)
    linear_regression = LinearRegression()
    linear_regression.fit(X, Y)
    Y_pred = linear_regression.predict(X)
    residuals = (Y - Y_pred).flatten()
    score = linear_regression.score(X, Y)
    M = len(data)
    se2 = sum(residuals ** 2) / (M - 2)
    mean_Xm = data['Xm'].mean()
    seb2 = se2/((data['Xm']-mean_Xm)**2).sum()
    return [security_series.name,            # fund
            score,                           # R2
            linear_regression.intercept_[0], # alpha
            linear_regression.coef_[0][0],   # beta
            math.sqrt(se2),                  # se
            math.sqrt(seb2),                 # se_b
            data['Xi'].mean(),               # miu_i
            data['Xm'].mean(),               # miu_m
            data['Xm'].std(),                # sigma_m
            data['rf'].mean(),               # miu_rf
            data['rf'].std(),                # sigma_rf
            data['Xi - rf'].mean(),          # miu_(i-rf)
            data['Xm - rf'].mean(),          # miu_(m-rf)
            data['Xm - rf'].std(),           # sigma_(m-rf)
            M                                # Number of datapoints
    ]

def many_capm(funds, index, risk_free):
    columns = ['fund', 'R2', 'alpha', 'beta', 'se', 'se_b', \
                'miu_i', 'miu_m', 'sigma_m', 'miu_rf', 'sigma_rf', \
                'miu_(i-rf)', 'miu_(m-rf)', 'sigma_(m-rf)', \
                'M']
    data = []
    for fund_name in funds.columns:
        data.append(capm(funds[fund_name], index, risk_free))
    return pd.DataFrame(data, columns=columns).set_index('fund')

def one(x_series, y_series):
    both = pd.concat([x_series, y_series], axis=1, keys=['X', 'Y']).dropna(how='any')
    if len(both) < 3:
        return [y_series.name, None, None, None, None, None, None, None, None, len(both)]
    X = both['X'].values.reshape(-1, 1)
    Y = both['Y'].values.reshape(-1, 1)
    linear_regression = LinearRegression()
    linear_regression.fit(X, Y)
    Y_pred = linear_regression.predict(X)
    residuals = (Y - Y_pred).flatten()
    score = linear_regression.score(X, Y)
    M = len(both)
    se2 = sum(residuals ** 2) / (M - 2)
    mean_X = both['X'].mean()
    seb2 = se2/((both['X']-mean_X)**2).sum()
    return [y_series.name,                   # fund
            score,                           # R2
            linear_regression.intercept_[0], # a
            linear_regression.coef_[0][0],   # b
            math.sqrt(se2),                  # se
            both['X'].std(),                 # sigma_beta_LS
            math.sqrt(seb2),                 # se_beta_LS
            both['Y'].mean(),                # miu_true_beta
            both['X'].mean(),                # miu_beta_LS
            M,                               # Number of datapoints
    ]


def for_bootstrapping(rs_it, rs_mt, rs_rf, fund_name):
    rs_ir_er = rs_it - rs_rf
    rs_mt_er = rs_mt - rs_rf
    X = rs_mt_er.reshape(-1, 1)
    Y = rs_ir_er.reshape(-1, 1)
    linear_regression = LinearRegression()
    linear_regression.fit(X, Y)
    return [fund_name,                       # fund
            linear_regression.intercept_[0], # alpha
            linear_regression.coef_[0][0],   # beta
            rs_it.mean(),                    # miu_i
            rs_mt.mean(),                    # miu_m
            np.std(rs_mt, ddof=1),           # sigma_m
    ]