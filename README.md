import numpy as np
import pandas as pd

np.random.seed(42)
n = 10000  # users
data = pd.DataFrame({
    'user_id': range(n),
    'biometric_adopt': np.random.binomial(1, 0.5, n),  # Treatment: 1 if adopted biometrics
    'lockouts': np.random.poisson(2, n) * (1 - 0.1 * np.random.binomial(1, 0.5, n)),  # Count outcome, slight reduction post-adopt
    'fraud_attempts': np.random.poisson(1, n),
    'pre_post': np.random.binomial(1, 0.6, n),  # For DiD: 1 post-rollout
    'age': np.random.randint(18, 80, n),
    'income': np.random.lognormal(10, 1, n)
})
data['lockouts'] = data['lockouts'].astype(int)
data.to_csv('biometric_sim_data.csv', index=False)
import statsmodels.api as sm
from statsmodels.discrete.count_model import ZeroInflatedPoisson

# Poisson
X = sm.add_constant(data[['biometric_adopt', 'age', 'income']])
model_pois = sm.Poisson(data['lockouts'], X).fit()
print(model_pois.summary())

# Negative Binomial (for overdispersion)
model_nb = sm.NegativeBinomial(data['lockouts'], X).fit()
print(model_nb.summary())

# Zero-Inflated Poisson
model_zip = ZeroInflatedPoisson(data['lockouts'], X).fit()
print(model_zip.summary()).
import matplotlib.pyplot as plt
residuals = model_pois.resid
plt.scatter(model_pois.fittedvalues, residuals)
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted')
plt.show().
from causalinference import CausalModel

covs = data[['age', 'income']]
treat = data['biometric_adopt']
outcome = data['lockouts']

cm = CausalModel(outcome, treat, covs)
cm.est_propensity_s()
cm.est_via_matching()
print(cm.estimates).
data['treated_post'] = data['biometric_adopt'] * data['pre_post']
X_did = sm.add_constant(data[['biometric_adopt', 'pre_post', 'treated_post', 'age']])
model_did = sm.OLS(data['lockouts'], X_did).fit()  # Or Poisson for counts
print(model_did.summary()).
import seaborn as sns
sns.lineplot(x='pre_post', y='lockouts', hue='biometric_adopt', data=data)
plt.show().
