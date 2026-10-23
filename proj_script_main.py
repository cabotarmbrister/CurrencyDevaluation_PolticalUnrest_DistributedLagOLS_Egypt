# Currency Devaluation Political Unrest Distributed Lag OLS Model Egypt
# Cabot Armbrister
# 10-20-2026

import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import sqlite3 as sq

# created ACLED and FX data frames, connected to SQL

df_currency = pd.read_csv('usd_egp_monthly.csv')
df_acled = pd.read_csv('acled_political_unrest.csv')

conn = sq.connect("geopolitics.db")

df_currency.to_sql(
    name="fx_monthly",
    con=conn,
    if_exists="replace", 
    index=False 
)
# doesn't save the pandas row names (0, 1, 2, etc)
# overwrites table if re-run cell

df_acled.to_sql(
    name="acled_events",
    con=conn,
    if_exists="replace",
    index=False
)

'''
SQL query condenses acled data into monthly rows instead of daily, then joins 
the new monthly acled data with the monthly currency data all under one combined table,
ensures if no acled data value will be 0 and not NULL, sorts oldest to most recent
'''

# Data aggregation, integration, & cleaning

query = """

WITH monthly_events AS (
    SELECT 
        substr(week, 1, 7) AS year_month,
        COUNT(*) AS events_count
    FROM acled_events
    GROUP BY year_month
    )
SELECT 
    fx_monthly.year_month,
    fx_monthly.fx_rate,
    COALESCE(monthly_events.events_count, 0) AS events_count
FROM fx_monthly
LEFT JOIN monthly_events
    ON fx_monthly.year_month = monthly_events.year_month
ORDER BY fx_monthly.year_month ASC;

"""

df_joined = pd.read_sql_query(query, conn)
conn.close()

'''
finding lagging shock(political unrest) response to a specific
% change in FX, lagging response for 1 month, 2 months, 3 months, and 4 months
'''

df_joined['fx_pct_change'] = df_joined['fx_rate'].pct_change() * 100


df_joined["fx_lag_1"] = df_joined["fx_pct_change"].shift(1) 
df_joined["fx_lag_2"] = df_joined["fx_pct_change"].shift(2) 
df_joined["fx_lag_3"] = df_joined["fx_pct_change"].shift(3) 


'''
if there is no data available for % change in fx that corresponds with the lag,
this line of code deletes the "na" lines without data, makes a copy of the data
frame as well so no errors with pandas
'''

df_model = df_joined.dropna().copy() 

# Econometrics Modeling

model = smf.ols("events_count ~ fx_pct_change + fx_lag_1 + fx_lag_2 + fx_lag_3", data=df_model).fit()

# Econometrics Modeling post 2014, accounting for Arab Spring 

df_modern = df_model[df_model['year_month'] >= '2014-01'].copy()

modern_model = smf.ols("events_count ~ fx_pct_change + fx_lag_1 + fx_lag_2 + fx_lag_3", data=df_modern).fit()

print(modern_model.summary(alpha=.10))

# Visualizing Data w/ MatPlotLib

df_model['predicted_events'] = model.predict(df_model)

x_value = input('''Select which x-axis variable you would like: 
\tPercent Change: fx_pct_change
\tLag 1: fx_lag_1
\tLag 2: fx_lag_2
\tLag 3: fx_lag_3

''')

plt.figure(figsize=(9, 5))


sns.regplot(
    data=df_modern,
    x= x_value,       
    y='events_count',        
    ci=90,                   
    scatter_kws={'alpha': 0.5, 'color': 'steelblue'}, 
    line_kws={'color': 'firebrick', 'linewidth': 2}   
)

plt.axvline(0, color='gray', linestyle='--', linewidth=1, alpha=0.6) # axis line

plt.title('Egyptian Currency Devaluation vs. Conflict Events', fontsize=12)
plt.xlabel('Monthly FX % Depreciation (Shock)/Lag 1/Lag 2/Lag 3', fontsize=10)
plt.ylabel('Monthly Conflict Events Recorded', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()

plt.show()
