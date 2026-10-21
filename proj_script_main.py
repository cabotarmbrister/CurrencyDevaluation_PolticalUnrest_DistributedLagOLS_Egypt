# Currency Devaluation Political Unrest Distributed Lag OLS Model Egypt
# Cabot Armbrister
# 10-20-2026

import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import sqlite3 as sq


df_currency = pd.read_csv('usd_egp_monthly.csv')
df_acled = pd.read_csv('acled_political_unrest.csv')

conn = sq.connect("geopolitics.db")

df_currency.to_sql(
    name="fx_monthly",
    con=conn,
    if_exsists="replace", # overwrites table if re-run cell
    index=False # doesn't save the pandas row names (0, 1, 2, etc)
)

df_acled.to_sql(
    name="acled_events",
    con=conn,
    if_exsists="replace",
    index=False
)


query_initial = """

need to clean data here, need to make same formatting so meaning get acled data into 
YYYY-MM format

need to condense all acled events per each month into 1 row that represents that month that
will correspond with the fx data

need to run sql query to join the tables together

"""
df_joined = pd.read_sql_query(query_initial, conn)

conn.close()


"""
sql query rough draft:

WITH mothly_events AS (
    SELECT 
        substr(1, 7) AS month_year FROM,
        COUNT(*) AS events_count
    FROM acled_events
    GROUP BY year_month
)


"""