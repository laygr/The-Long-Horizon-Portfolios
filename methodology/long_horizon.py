def compute_beta_L(beta_i, miu_i, miu_m, sigma_m, N):
    var_m = sigma_m ** 2
    numerador = (beta_i*var_m + (1+miu_i)*(1+miu_m))**N - (1+miu_i)**N * (1+miu_m)**N
    denominador = (var_m + (1+miu_m)**2)**N - (1+miu_m)**(2*N)
    
    return numerador/denominador

def compute_betas_L(data):
    N       = data['N']
    miu_i   = data['miu_i']
    beta_i  = data['beta']
    miu_m   = data['miu_m']
    sigma_m = data['sigma_m']

    return compute_beta_L(beta_i, miu_i, miu_m, sigma_m, N)

def compute_alpha_L(data, beta_L):
    N       = data['N']
    miu_i_L = (1 + data['miu_i'])**N - 1
    miu_m_L = (1 + data['miu_m'])**N - 1
    miu_rf_L    = (1 + data['miu_rf'])**N - 1
    
    return miu_i_L - miu_rf_L - beta_L * (miu_m_L - miu_rf_L)

def compute_sigma_L(sigma, miu, N):
    var   = sigma**2
    var_L = (var + (1+miu)**2)**N - (1+miu)**(2*N)
    return var_L**0.5

def compute_se_L(se, sigma_i, sigma_i_L):
    return se * sigma_i_L / sigma_i

def compute_beta_LL(data):
    return data['a'] + data['b'] * data['beta L']