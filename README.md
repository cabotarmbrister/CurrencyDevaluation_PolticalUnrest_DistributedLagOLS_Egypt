**Egyptian Pound Devaluation & Civil Unrest Analysis (2014–2025)**
An end-to-end econometrics and data science project evaluating the relationship between macroeconomic currency shocks in the Egyptian Pound and political protests and disruption events in Egypt using SQL, Pandas, Statsmodels, Matplotlib, and Seaborn.

**Project Overview**
This project tests to see whether there is a relationship between month-to-month devaluations in currency and political disruptions in the country. It also tests to see if there is a delayed response (lag) in political disruptions as response to currency devaluation, tests to see the magnitude of political disruptions for the current month, 30, and 60 days following the currency devaluation. 

**Distributed Lag Ordinary Least Squares Model**
Model: Y_subscript(t) = β + β₁(%ΔFX_subscript(t)) + β₂(%ΔFX_subscript(t-1)) + β₃(%ΔFX_subscript(t-2)) + ε_subscript(t)

the distributed lag ols model is used in this case to measure the how delayed the response is to currency devaluation in terms of political protests and disruptions, we also use the beta coefficients to display a relationship between currency devaluation and political unrest if the coefficients are found to be statistically significant (p < 0.10) with a 90% confidence interval [0.05, 0.95].

**Statistical Analysis & Findings**
I was unable to reject the null hypothesis, I found no statistically significant correlation between political unrest and currency devaluation for the immediate month, 30, and 60 days following the initial shock. 

**Data Architecture**
ACLED CSV + Yahoo Finance FX CSV --> SQL Database "geopolitics.db", loaded data into SQL using .to_sql()
Aggregated ACLED daily data into ACLED monthly data using substr(week, 1, 7) to extract the characters 1-7 from the "week" column, formatting data in monthly 
interval, "YYYY-MM"
Utilized COALESCE() to ensure months with 0 events remained 0 and not NULL
Left Joined ACLED monthly data onto FX monthly data
Created joined data frame using pd.read_sql_query() to execute SQL query
Added FX % change and lags to joined data frame using .pct_change() and .shift() from pandas

**Additional Conext**
During The Arab Spring (2011-2013) there was heightened political unrest and disruptions due to pro-democracy and individual liberties protests. While currency was affected and depreciated throughout various countries in the region, this was not the main driver of the protests and would be inaccurate to try to derive a relationship from currency depreciation and political unrest, which is why I opted to use data beginning in 2014. Additionally, in 2016 and 2024 the Egyptian government artificially depreciated substantially, up to 48% in a single day in 2016 and 60% in 2024 in order to secure a bailout loan package from the IMF. These two anomalies should be noted to account for any outlying data during these periods. 
