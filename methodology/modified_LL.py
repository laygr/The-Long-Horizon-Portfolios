import pandas as pd
import numpy as np
import linear_regression
from long_horizon import compute_beta_L, compute_betas_L, \
                          compute_beta_LL, compute_alpha_L

def simulate_one(data, betas_std, alphas_std):
    true_betas_L, betas_LS = {}, {}

    for fund_name in data.index:
        M         = data.at[fund_name, 'M']
        N         = data.at[fund_name, 'N']
        alpha     = data.at[fund_name, 'alpha']
        beta      = data.at[fund_name, 'beta']
        se        = data.at[fund_name, 'se']
        miu_i     = data.at[fund_name, 'miu_(i-rf)']
        miu_m     = data.at[fund_name, 'miu_(m-rf)']
        sigma_m   = data.at[fund_name, 'sigma_(m-rf)']
        miu_rf    = 0.0
        sigma_rf  = 0.0
        
        # generar true alpha, beta y rf
        true_alpha    = np.random.normal(alpha,    scale=alphas_std)
        true_beta     = np.random.normal(beta,     scale=betas_std)
        true_rf       = np.random.normal(miu_rf,   scale=sigma_rf)
        
        # eq 1:
        miu_i_t = true_alpha + true_rf + true_beta * (miu_m-true_rf)
        #eq 6:
        true_betas_L[fund_name] = compute_beta_L(true_beta, miu_i_t, miu_m, sigma_m, N)

        # generar M retornos de mercado y del security
        rs_mt         = np.random.normal(miu_m,    scale=sigma_m,  size=M)
        errors_it     = np.random.normal(0.0,      scale=se,       size=M)
        rs_rf         = [true_rf] * M

        rs_it = true_alpha + true_rf + true_beta*(rs_mt-true_rf) + errors_it

        [fund_s, alpha_s, beta_s, miu_i_s, miu_m_s, sigma_m_s] = \
            linear_regression.for_bootstrapping(rs_it, rs_mt, rs_rf, fund_name)

        betas_LS[fund_name] = compute_beta_L(beta_s, miu_i_s, miu_m_s, sigma_m_s, N)
        
    return pd.Series(true_betas_L), pd.Series(betas_LS)
    
def simulate_many(data, S=1000):
    true_betas_L, betas_LS = [], []
    betas_std  = data['beta'].std()
    alphas_std = data['alpha'].std()
    for i in range(S):
        one_true_betas_L, one_betas_LS = simulate_one(data, betas_std, alphas_std)
        print(i)
        true_betas_L.append(one_true_betas_L)
        betas_LS.append(one_betas_LS)
    
    true_betas_L = pd.concat(true_betas_L, axis=1)
    betas_LS = pd.concat(betas_LS, axis=1)
    return true_betas_L, betas_LS

def estimate_relations_between_true_and_sample(true_betas_L, betas_LS):
    regression_data = []
    for fund_name in true_betas_L.index:
        x_series = betas_LS.loc[fund_name]
        y_series = true_betas_L.loc[fund_name]
        regression_data.append(linear_regression.one(x_series, y_series))
    columns = ['fund', 'R2', 'a', 'b', 'se', 'sigma_beta_LS', 'se_beta_LS', 'miu_true_beta', 'miu_beta_LS', 'M']
    return pd.DataFrame(regression_data, columns = columns).set_index('fund')

def main(data, N, S=1000):
    data = data.dropna(how='any').copy()
    data['N']                = N
    data['beta L']           = compute_betas_L(data)
    data['alpha L']          = compute_alpha_L(data, data['beta L'])
    true_betas_L, betas_LS   = simulate_many(data, S)
    relation                 = estimate_relations_between_true_and_sample(true_betas_L, betas_LS)
    data['R2_S']             = relation['R2']
    data['a']                = relation['a']
    data['b']                = relation['b']
    data['beta LL']          = compute_beta_LL(data)
    data['alpha LL']         = compute_alpha_L(data, data['beta LL'])
    return data, relation



import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Removes repeated values from excel file')
    parser.add_argument('--regressions', help='the path to the file with the regressions data')
    parser.add_argument('--N', type=int, help='number of periods for the long horizon')
    parser.add_argument('--S', type=int, help='number of simulations to perform per fund')
    args = parser.parse_args()
    
    data = pd.read_csv(args.regressions, index_col=0)
    data['M'] = data['M'].astype(int)

    if args.N == 0:
        N = data['M']
    else:
        N = pd.Series(args.N, index=data.index)

    result, relation = main(data, N, args.S)
    result.to_csv(args.regressions.split('.csv')[0] + '_'+str(args.N) + '.csv')
    relation.to_csv(args.regressions.split('.csv')[0] + '_'+str(args.N) + '_relation.csv')