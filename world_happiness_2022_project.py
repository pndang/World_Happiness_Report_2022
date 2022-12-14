# -*- coding: utf-8 -*-
"""World_Happiness_2022_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qGA5vFw2h3OO1guIAuMAVzAbClQ7nnTk

Project Main Questions:

1) What does happiness index look like across the world?

2) What affects happiness index?

3) Can you group countries based on features such as economic production, social support, life expectancy etc?

4) What impact did COVID-19 have on this index?
"""

#from google.colab import files
#upload = files.upload()

# ^ no longer needed, datasets uploaded directly to google colab

from google.colab import drive
drive.mount('/content/drive')

# Importing libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy.linalg as la
import statsmodels.api as sm
from scipy import stats
import itertools
import warnings
warnings.filterwarnings('ignore')

"""Prospective Questions:

1) Which factor(s) affect a nation's happiness score the most?

2) Are there any relations between vaccination rates and happiness scores?

3) Do we see any problems with the ratings of each factor?
"""

# Importing and cleaning dataset

df = pd.read_csv("/content/drive/MyDrive/World Happiness Report 2022.csv")
df.drop(columns = ['Whisker-high', 'Whisker-low'], inplace = True)
df = df.drop(df.index[-1])
df['Country'] = df['Country'].str.replace('*', '')

df

# Grouping Countries by GDP
gdp = df.sort_values("Explained by: GDP per capita",)
gdp.head(10)

# Group Country by Social Support
sns.regplot(data=df, x="Explained by: Social support", y="Happiness score", 
            scatter_kws = {"color": 'b'}, line_kws = {"color": 'r'})

# Group Country by Life Expectancy
sns.regplot(data=df, x="Explained by: Healthy life expectancy", y="Happiness score", 
            scatter_kws = {"color": 'b'}, line_kws = {"color": 'r'})

# Grouping By Quantiles
x = np.linspace(0,1,5)
a = df['Explained by: GDP per capita'].quantile(x)
b = df['Explained by: Social support'].quantile(x)
c = df['Explained by: Healthy life expectancy'].quantile(x)
d = df['Happiness score'].quantile(x)

a

#GDP (Low To High)

GDP1 = df[df['Explained by: GDP per capita'].between(a[0],a[0.25])]
GDP2 = df[df['Explained by: GDP per capita'].between(a[0.25],a[0.5])]
GDP3 = df[df['Explained by: GDP per capita'].between(a[0.5],a[0.75])]
GDP4 = df[df['Explained by: GDP per capita'].between(a[0.75],a[1])]

#Social Support (Low To High)

Soc1 = df[df['Explained by: Social support'].between(b[0],b[0.25])]
Soc2 = df[df['Explained by: Social support'].between(b[0.25],b[0.5])]
Soc3 = df[df['Explained by: Social support'].between(b[0.5],b[0.75])]
Soc4 = df[df['Explained by: Social support'].between(b[0.75],b[1])]

#Life Exptecancy (Low To High)

Lif1 = df[df['Explained by: Healthy life expectancy'].between(c[0],c[0.25])]
Lif2 = df[df['Explained by: Healthy life expectancy'].between(c[0.25],c[0.5])]
Lif3 = df[df['Explained by: Healthy life expectancy'].between(c[0.5],c[0.75])]
Lif4 = df[df['Explained by: Healthy life expectancy'].between(c[0.75],c[1])]

#Happinese Score (Low To High)

Hap1 = df[df['Happiness score'].between(d[0],d[0.25])]
Hap2 = df[df['Happiness score'].between(d[0.25],d[0.5])]
Hap3 = df[df['Happiness score'].between(d[0.5],d[0.75])]
Hap4 = df[df['Happiness score'].between(d[0.75],d[1])]

# What affects Happiness Index

# Linear Regression function
def lin_reg(x, y):
    '''
    ordinary linear regression using least-squares
    
    Parameters
    ----------  
    x: regressors (numpy array)
    y: dependent variable (numpy array)
    
    Returns
    -------
    coefficients: regression coefficients (pandas Series)
    residuals: regression residuals (numpy array)
    r_squared: correlation coefficient (float)
    
    '''
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    coefficients = model.params
    residuals = model.resid
    r_squared = model.rsquared

    return coefficients, residuals, r_squared

a = lin_reg(df["Happiness score"].values, df["Explained by: GDP per capita"].values)
b = lin_reg(df["Happiness score"].values, df["Explained by: Social support"].values)
c = lin_reg(df["Happiness score"].values, df["Explained by: Healthy life expectancy"].values)
d = lin_reg(df["Happiness score"].values, df["Explained by: Freedom to make life choices"].values)
e = lin_reg(df["Happiness score"].values, df["Explained by: Generosity"].values)
f = lin_reg(df["Happiness score"].values, df["Explained by: Perceptions of corruption"].values)

# Plotting data points and regression line

x = np.linspace(1,8,250)

df.plot.scatter(x="Happiness score",y="Explained by: GDP per capita",label="GDP, Slope = {:.4}".format(a[0][1]))
plt.plot(x,a[0][0]+a[0][1]*x, "b")
plt.title("R^2 = {:.4}".format(a[2]))
plt.show()
df.plot.scatter(x="Happiness score",y="Explained by: Social support",label="Social Support, Slope = {:.4}".format(b[0][1]))
plt.plot(x,b[0][0]+b[0][1]*x, "b")
plt.title("R^2 = {:.4}".format(b[2]))
plt.show()
df.plot.scatter(x="Happiness score",y="Explained by: Healthy life expectancy",label="Life Expectancy, Slope = {:.4}".format(c[0][1]))
plt.plot(x,c[0][0]+c[0][1]*x, "b")
plt.title("R^2 = {:.4}".format(c[2]))
plt.show()
df.plot.scatter(x="Happiness score",y="Explained by: Freedom to make life choices",label="Freedom, Slope = {:.4}".format(d[0][1]))
plt.plot(x,d[0][0]+d[0][1]*x, "b")
plt.title("R^2 = {:.4}".format(d[2]))
plt.show()
df.plot.scatter(x="Happiness score",y="Explained by: Generosity",label="Genoristy, Slope = {:.4}".format(e[0][1]))
plt.plot(x,e[0][0]+e[0][1]*x, "b")
plt.title("R^2 = {:.4}".format(e[2]))
plt.show()
df.plot.scatter(x="Happiness score",y="Explained by: Perceptions of corruption",label="Corruption, Slope = {:.4}".format(f[0][1]))
plt.plot(x,f[0][0]+f[0][1]*x, "b")
plt.title("R^2 = {:.4}".format(f[2]))
plt.show()

# GDP has the most positive slope and a good corelation value

#Analyzing Pre Covid Data set

Precovid = pd.read_csv('/content/drive/MyDrive/World Happiness Report 2018.csv') 
#I used the 2018 Data set, but this data set actually averages out all the previous years
Precovid.rename(columns={'country': 'Country'}, inplace=True)
Precovid = Precovid.groupby(["Country"]).mean()
Precovid.rename(columns={'Life Ladder': 'Happiness score (Pre)'}, inplace=True)
Compare = pd.merge(df, Precovid, on ="Country")
Compare["Happiness score"] - Compare["Happiness score (Pre)"]
Compare.insert(2,'Difference', Compare["Happiness score"] - Compare["Happiness score (Pre)"] )
Compare.describe().head()

corre_coef, p_value = stats.pearsonr(np.linspace(1,141,140), Compare["Difference"])
plt.scatter(np.linspace(1,141,140), Compare["Difference"]) #X axis are the ranks of countries
plt.axhline(0, color='red')
plt.xlabel("Countries")
plt.ylabel("Difference in Happiness Score")
plt.text(0.07, -1.75, "P-value: {:.2}".format(p_value))
plt.text(0.07, -2.0, "Mean: {:.2}".format(0.120))
#mean difference in happiness increased by 0.12. Either covid made people happier or no difference

# Importing and Cleaning COVID dataset

covid =  pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
covid.drop(columns = ['excess_mortality_cumulative_absolute', 'excess_mortality_cumulative', \
                      'excess_mortality', 'excess_mortality_cumulative_per_million', \
                      'total_cases', 'new_cases',
                      'new_cases_smoothed', 'total_deaths', 'new_deaths',
                      'new_deaths_smoothed', 'total_cases_per_million',
                      'new_cases_per_million', 'new_cases_smoothed_per_million',
                      'total_deaths_per_million', 'new_deaths_per_million',
                      'new_deaths_smoothed_per_million', 'reproduction_rate', 'icu_patients',
                      'icu_patients_per_million', 'hosp_patients',
                      'hosp_patients_per_million', 'weekly_icu_admissions',
                      'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
                      'weekly_hosp_admissions_per_million', 'total_tests', 'new_tests',
                      'total_tests_per_thousand', 'new_tests_per_thousand',
                      'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
                      'positive_rate', 'tests_per_case', 'tests_units',
                      'stringency_index', 'total_boosters_per_hundred',
                      'new_vaccinations_smoothed_per_million',
                      'new_people_vaccinated_smoothed',
                      'population', 'population_density', 'median_age', 'aged_65_older',
                      'aged_70_older', 'extreme_poverty',
                      'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers',
                      'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',
                      'human_development_index', 'iso_code'], inplace = True)

covid.columns

covid.dropna(axis = 0, inplace = True)
covid

# Merge world happiness and covid datasets together

data = df.merge(covid, left_on='Country', right_on='location')
data = data[~(data == 0).any(axis=1)] #Drop rows with value 0
data.head()

data.columns

#Graphing people vaccinated per hundred and Happiness have no good results since total boosters has too great a range 
data.plot.scatter(x="people_fully_vaccinated_per_hundred", y="Happiness score")

#This is for Q1, finding Happiness score dist across the world 
continent = data.groupby("continent", as_index=False)[["Happiness score"]].mean()
continent.sort_values("Happiness score") 
#Oceania is happiest, africa is least happiest

world = sns.barplot(x = "continent", y="Happiness score", data=continent)
plt.setp(world.get_xticklabels(), rotation=90)
world.set_ylabel("Average Happiness Score", fontsize=15)
world.set_xlabel("Continent", fontsize=15)
plt.ylim(0,8)
#display y-values
for bar in world.patches:
    world.annotate(format(bar.get_height(), '.2f'),
                   (bar.get_x() + bar.get_width() / 2,
                    bar.get_height()), ha='center', va='center',
                   size=10, xytext=(0, 8),
                   textcoords='offset points')

#Effect of Total Vaccinations per hundred on Happiness
x = np.linspace(0,1,11)
a = data['people_fully_vaccinated_per_hundred'].quantile(x)
Vac1 = data[data['people_fully_vaccinated_per_hundred'].between(a[0],a[0.1])]
Vac2 = data[data['people_fully_vaccinated_per_hundred'].between(a[0.1],a[0.2])]
Vac3 = data[data['people_fully_vaccinated_per_hundred'].between(a[0.2],58.507)]
Vac4 = data[data['people_fully_vaccinated_per_hundred'].between(58.507,a[0.4])]
Vac5 = data[data['people_fully_vaccinated_per_hundred'].between(a[0.4],a[0.5])]
Vac6 = data[data['people_fully_vaccinated_per_hundred'].between(a[0.5],72.190)]
Vac7 = data[data['people_fully_vaccinated_per_hundred'].between(72.190,75.880)]
Vac8 = data[data['people_fully_vaccinated_per_hundred'].between(75.880,a[0.8])]
Vac9 = data[data['people_fully_vaccinated_per_hundred'].between(a[0.8],a[0.9])]
Vac10 = data[data['people_fully_vaccinated_per_hundred'].between(a[0.9],a[1])]

plt.scatter(np.linspace(0.1,1,10),  [Vac1["Happiness score"].mean(), Vac2["Happiness score"].mean(),Vac3["Happiness score"].mean(),Vac4["Happiness score"].mean(),Vac5["Happiness score"].mean(),Vac6["Happiness score"].mean(),Vac7["Happiness score"].mean(),Vac8["Happiness score"].mean(),Vac9["Happiness score"].mean(),Vac10["Happiness score"].mean()])
o = lin_reg(np.linspace(0.1,1,10), [Vac1["Happiness score"].mean(), Vac2["Happiness score"].mean(),Vac3["Happiness score"].mean(),Vac4["Happiness score"].mean(),Vac5["Happiness score"].mean(),Vac6["Happiness score"].mean(),Vac7["Happiness score"].mean(),Vac8["Happiness score"].mean(),Vac9["Happiness score"].mean(),Vac10["Happiness score"].mean()])
plt.plot(np.linspace(0.1,1,100),o[0][0]+o[0][1]*np.linspace(0.1,1,100), label=" Slope = {:.4}".format(o[0][1]))
plt.title('Average Happiness Score (per quantile) in average vaccination rate')
plt.xlabel('Quantile (Total Vaccinations Per Hundred)')
plt.ylabel('Average Happiness Score')
plt.show()

#Slightly positive

o[0][1] # slope of regression line

# Pearson correlation between happiness score and total fully-vaccinated per hundred

y = [Vac1["Happiness score"].mean(), Vac2["Happiness score"].mean(), Vac3["Happiness score"].mean(),
     Vac4["Happiness score"].mean(), Vac5["Happiness score"].mean(), Vac6["Happiness score"].mean(),
     Vac7["Happiness score"].mean(), Vac8["Happiness score"].mean(), Vac9["Happiness score"].mean(),
     Vac10["Happiness score"].mean()]
x = np.linspace(0,1,10)

corre_coef, p_value = stats.pearsonr(x, y)
intercept = stats.linregress(x, y)[1]
corre_coef, p_value, intercept

# Graph average happiness scores, total full_vac per hundred, correlation coefficient, and p-value

sns.set(style='whitegrid')
sns.relplot(np.linspace(0.1,1,10), y)
plt.plot(np.linspace(0.1,1,100), o[0][0]+o[0][1]*np.linspace(0.1,1,100), color='steelblue')
plt.title('Average Happiness and Total fully-vaccinated per Hundred')
plt.xlabel('Quantile (Total fully-vaccinated Per Hundred)')
plt.ylabel('Average Happiness Score')
plt.text(0.07, 6.7, "Correlation coefficient: {:.4}".format(corre_coef), size=11)
plt.text(0.07, 6.63, "P-value: {:.2}".format(p_value), size=11)
plt.show()

data.head()

# More cleaning and checking correlations between variables
countries = data.groupby(['Country']).mean()
sns.relplot(x='gdp_per_capita', y='total_vaccinations', data=countries)
countries[['gdp_per_capita', 'total_vaccinations']]
heatmap_data = data.drop(columns=['new_vaccinations_smoothed', 'people_fully_vaccinated',
       'total_boosters', 'new_vaccinations', 'new_vaccinations_smoothed',
       'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
       'new_people_vaccinated_smoothed_per_hundred', 'RANK', 'people_vaccinated'])
corr = countries.corr(method='pearson')

sns.kdeplot(data['Happiness score'], hue=data['continent'], fill=True)

# Factors correlation heatmap

plt.figure(figsize = (14, 6))
ax = sns.heatmap(heatmap_data.corr(), annot = True, fmt = '.2f', linewidth = 0.5)
props = plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', rotation_mode='anchor')
plt.title('Factor Correlation 2022', size = 15)

# Cleaning World Happiness dataset for stacked horizontal bar graph
stacked = df
stacked = df.iloc[0:len(df):3]
stacked.sort_values(by='Happiness score', ascending=False).head()

# Graphing horizontal bar chart

from itertools import cycle
colors = cycle(['lightcoral', 'yellow', 'paleturquoise', 'orange', 'lightpink', 'lime', 'deepskyblue'])

v1 = stacked['Dystopia (1.83) + residual']
v2 = stacked['Explained by: GDP per capita']
v3 = stacked['Explained by: Social support']
v4 = stacked['Explained by: Healthy life expectancy']
v5 = stacked['Explained by: Freedom to make life choices']
v6 = stacked['Explained by: Generosity']
v7 = stacked['Explained by: Perceptions of corruption']

plt.figure(figsize = (15, 15))
ax1 = plt.barh(stacked['Country'], v1, color=next(colors))
ax2 = plt.barh(stacked['Country'], v2, left=v1, color=next(colors))
ax3 = plt.barh(stacked['Country'], v3, left=v1+v2, color=next(colors))
ax4 = plt.barh(stacked['Country'], v4, left=v1+v2+v3, color=next(colors))
ax5 = plt.barh(stacked['Country'], v5, left=v1+v2+v3+v4, color=next(colors))
ax6 = plt.barh(stacked['Country'], v6, left=v1+v2+v3+v4+v5, color=next(colors))
ax7 = plt.barh(stacked['Country'], v7, left=v1+v2+v3+v4+v5+v6, color=next(colors))
plt.legend([ax1, ax2, ax3, ax4, ax5, ax6, ax7], ["Dystopia (1.83) + residual", 'Explained by: GDP per capita', 'Explained by: Social support', 
                                                 'Explained by: Healthy life expectancy', 'Explained by: Freedom to make life choices',
                                                 'Explained by: Generosity', 'Explained by: Perceptions of corruption'], title="Legend", loc="upper right");
plt.title("Happiness Score Compositions", size=15)
plt.xlabel("Happiness Scores (2005-2021)", size=12)
plt.ylabel("Countries", size=12)


# Incomplete for-loop version

# for col in df.columns[3:10]:
#   plt.barh(stacked['Country'], stacked[col], color=next(colors), bottom=True)

"""Cell below: Unused code archive"""

# Vac1['Happiness score normalized'] = (Vac1['Happiness score']-Vac1['Happiness score'].min()) / (Vac1['Happiness score'].max()-Vac1['Happiness score'].min())
# Vac2['Happiness score normalized'] = (Vac2['Happiness score']-Vac2['Happiness score'].min()) / (Vac2['Happiness score'].max()-Vac2['Happiness score'].min())
# Vac3['Happiness score normalized'] = (Vac3['Happiness score']-Vac3['Happiness score'].min()) / (Vac3['Happiness score'].max()-Vac3['Happiness score'].min())
# Vac4['Happiness score normalized'] = (Vac4['Happiness score']-Vac4['Happiness score'].min()) / (Vac4['Happiness score'].max()-Vac4['Happiness score'].min())
# Vac5['Happiness score normalized'] = (Vac5['Happiness score']-Vac5['Happiness score'].min()) / (Vac5['Happiness score'].max()-Vac5['Happiness score'].min())
# Vac6['Happiness score normalized'] = (Vac6['Happiness score']-Vac6['Happiness score'].min()) / (Vac6['Happiness score'].max()-Vac6['Happiness score'].min())
# Vac7['Happiness score normalized'] = (Vac7['Happiness score']-Vac7['Happiness score'].min()) / (Vac7['Happiness score'].max()-Vac7['Happiness score'].min())
# Vac8['Happiness score normalized'] = (Vac8['Happiness score']-Vac8['Happiness score'].min()) / (Vac8['Happiness score'].max()-Vac8['Happiness score'].min())
# Vac9['Happiness score normalized'] = (Vac9['Happiness score']-Vac9['Happiness score'].min()) / (Vac9['Happiness score'].max()-Vac9['Happiness score'].min())
# Vac10['Happiness score normalized'] = (Vac10['Happiness score']-Vac10['Happiness score'].min()) / (Vac10['Happiness score'].max()-Vac10['Happiness score'].min())

# y = [Vac1['Happiness score normalized'].mean(), Vac2['Happiness score normalized'].mean(), Vac3['Happiness score normalized'].mean(),
#      Vac4['Happiness score normalized'].mean(), Vac5['Happiness score normalized'].mean(), Vac6['Happiness score normalized'].mean(),
#      Vac7['Happiness score normalized'].mean(), Vac8['Happiness score normalized'].mean(), Vac9['Happiness score normalized'].mean(),
#      Vac10['Happiness score normalized'].mean()]
# x = np.linspace(0.1,1,10)
# x = [Vac1['total_vaccinations_per_hundred'].mean(), Vac2['total_vaccinations_per_hundred'].mean(), Vac3['total_vaccinations_per_hundred'].mean(),
#      Vac4['total_vaccinations_per_hundred'].mean(), Vac5['total_vaccinations_per_hundred'].mean(), Vac6['total_vaccinations_per_hundred'].mean(),
#      Vac7['total_vaccinations_per_hundred'].mean(), Vac8['total_vaccinations_per_hundred'].mean(), Vac9['total_vaccinations_per_hundred'].mean(),
#      Vac10['total_vaccinations_per_hundred'].mean()]
# x = np.linspace(0,1,10)
# slope, intercept = stats.linregress(x,y)[0:2]
# print(x)
# print(y)
# slope

# data['total_vac_normalized'] = data['total_vaccinations'] / data['total_vaccinations'].max()
# data['Happiness score normalized'] = data['Happiness score'] / data['Happiness score'].max()

# sns.lineplot(x=x, y=np.linspace(0.1,1,10)*coef+intercept);

# https://github.com/owid/covid-19-data/blob/master/public/data/README.md

