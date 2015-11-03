"""
Econometrics Book Regressions

Simple Gravity Model

Notes
-----
1.  Data is computed by data/construct_data.py.
    This generates a data file: gravity_dataset_2013.csv

"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

#-Import Data-#
data = pd.read_csv("./data/gravity_dataset_2013.csv")

#-Basic Model-#
model1 = smf.ols("np.log(value) ~ np.log(egdp) + np.log(igdp) + np.log(dist)", data)
result1 = model1.fit()
result1 = result1.get_robustcov_results()
print(result1.summary())

#-Model with additional Explanatory Variables-#
model2 = smf.ols("np.log(value) ~ np.log(egdp) + np.log(igdp) + np.log(dist)+\
                  contig + comlang_off + colony + ell + ill", data)
result2 = model2.fit()
result2 = result2.get_robustcov_results()
print(result2.summary())

#-Model with additional Explanatory Variables-#
model3 = smf.ols("np.log(value) ~ np.log(egdppc) + np.log(igdppc) + np.log(dist)+\
                  contig + comlang_off + colony + ell + ill", data)
result3 = model3.fit()
result3 = result3.get_robustcov_results()
print(result3.summary())


#-Plots-#
import matplotlib.pyplot as plt
import statsmodels.api as sm
fig = plt.figure(figsize=(12,8))
fig = sm.graphics.plot_partregress_grid(result1, fig=fig)
