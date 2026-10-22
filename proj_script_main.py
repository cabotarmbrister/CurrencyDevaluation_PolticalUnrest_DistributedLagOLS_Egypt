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

print(df_joined.head(10))


