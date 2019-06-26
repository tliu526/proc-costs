"""
An interactive python file for exploring procedure costs
"""

#%% [markdown]

# # US Procedure Costs

#%% 
# imports

%matplotlib inline
from IPython.display import display, HTML

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#%%
# load data
BASE_DIR = "/home/tliu/repos/proc_costs/"

proc_freq_header = ['year', 'characteristic', 'characteristic_lvl', 
                    'maternal_neonatal_stays', 'rank', 'ccs', 'ccs_descr',
                    'weighted_num_stays', 'stay_rate_100k']

proc_costs = pd.read_csv(BASE_DIR + "data/hcup_proc_cost.csv")
proc_freq = pd.read_excel(BASE_DIR + \
                          "data/HCUP_National_Top_Procedures_DataExport.xls", 
                          sheet_name = 2,
                          skiprows = 2,
                          names = proc_freq_header)

proc_costs.columns = proc_costs.columns.str.lower()
proc_costs['ccs'] = proc_costs['ccscode'] 

# show head
display(proc_freq.head())
display(proc_costs.head())

# proc_freq characteristic options
display(list(proc_freq['characteristic'].unique()))

#%% 
# filter by all inpatient stays, including maternal
maternal_df = proc_freq.loc[(proc_freq['characteristic'] == "All Inpatient Stays") & \
                          (proc_freq['maternal_neonatal_stays'] == 'Included')]

# merge on ccs code and year
maternal_df = maternal_df.merge(proc_costs, on=['ccs', 'year'], how='left')

# top ten ccs codes in 2004
top_ten_ccs = proc_freq.loc[(proc_freq['year'] == 2004) & \
                            (proc_freq['characteristic'] == "All Inpatient Stays") & \
                            (proc_freq['maternal_neonatal_stays'] == 'Included')]
top_ten_ccs = top_ten_ccs["ccs"]

#%%
# plot top 10 procedures, including maternal
top_ten_df = maternal_df.loc[maternal_df['ccs'].isin(top_ten_ccs)]

with plt.style.context('default', True):
    sns.lineplot(x='year', y='weighted_num_stays', hue='ccs_descr', data=top_ten_df)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.ylabel("weighted number of stays per year")
    plt.title("Top 10 OR procedures frequency, including maternal")
    plt.show()

    sns.lineplot(x='year', y='meancharges', hue='ccs_descr', data=top_ten_df)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.ylabel("mean charge")
    plt.title("Top 10 OR procedures charge, including maternal")
    plt.show()

#%% 
# filter by all inpatient stays, excluding maternal
exclude_mat_df = proc_freq.loc[(proc_freq['characteristic'] == "All Inpatient Stays") & \
                          (proc_freq['maternal_neonatal_stays'] == 'Excluded')]

# merge on ccs code and year
exclude_mat_df = exclude_mat_df.merge(proc_costs, on=['ccs', 'year'], how='left')

# top ten ccs codes in 2004
top_ten_ccs = proc_freq.loc[(proc_freq['year'] == 2004) & \
                            (proc_freq['characteristic'] == "All Inpatient Stays") & \
                            (proc_freq['maternal_neonatal_stays'] == 'Excluded')]
top_ten_ccs = top_ten_ccs["ccs"]

#%%
# plot top 10 procedures, excluding maternal
top_ten_df = exclude_mat_df.loc[exclude_mat_df['ccs'].isin(top_ten_ccs)]

with plt.style.context('default', True):
    sns.lineplot(x='year', y='weighted_num_stays', hue='ccs_descr', data=top_ten_df)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.ylabel("weighted number of stays per year")
    plt.title("Top 10 OR procedures frequency, excluding maternal")
    plt.show()

    sns.lineplot(x='year', y='meancharges', hue='ccs_descr', data=top_ten_df)
    plt.tight_layout()
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.ylabel("mean charge")
    plt.title("Top 10 OR procedures charge, excluding maternal")
    plt.show()


#%%
top_ten_df[['year', 'ccs_descr', 'meancharges']]