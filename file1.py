# -*- coding: utf-8 -*-
"""NHFS5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iltZoxyXwGGCN7Zu3HNose1hQj1bvzbT

# Getting Started

In this notebook we will explore the NHFS Survey data (2019-21).

Importing the necessary libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score

# @title
# Inject JavaScript to enable Hinterland (real-time code completion)
from IPython.display import display, Javascript

display(Javascript('''
require(["notebook/js/codecell"], function(codecell) {
  codecell.CodeCell.options_default.cm_config.extraKeys = {
    "Tab": "autocomplete"
  };
  console.log("Hinterland enabled.");
});
'''))

df = pd.read_csv("/content/drive/MyDrive/NFHS_5_India_Districts_Factsheet_Data.csv")

"""# Data Preprocessing
### Renaming some columns
"""

df.rename(columns={'Female population age 6 years and above who ever attended school (%)': 'Female_school ever %', ' Sex ratio of the total population (females per 1,000 males)':'current sex-ratio', 'Sex ratio at birth for children born in the last five years (females per 1,000 males)':'sex-ratio at birth',
                    'Population living in households with electricity (%)': 'population % electricity','Population living in households with an improved drinking-water source1 (%)': 'drinking water %',
                    'Population living in households that use an improved sanitation facility2 (%)':'sanitation %','Households using clean fuel for cooking3 (%)':'clean fuel %','Households using iodized salt (%)':'iodized salt %','Households with any usual member covered under a health insurance/financing scheme (%)':'Health insurance/finance scheme %','Women (age 15-49) who are literate4 (%)':'Women literacy %','Women age 20-24 years married before age 18 years (%)':'women child marriage %','Women age 15-24 years who use hygienic methods of protection during their menstrual period5 (%)': 'Women menstural hygiene','Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Any method6 (%)':'Family planning methods %','All women age 15-49 years who are anaemic22 (%)':'Anaemic women %','Women age 15 years and above wih high or very high (>140 mg/dl) Blood sugar level or taking medicine to control blood sugar level23 (%)':'Women high blood sugar %','Men age 15 years and above wih high or very high (>140 mg/dl) Blood sugar level  or taking medicine to control blood sugar level23 (%)': 'Men high blood sugar %',
                    ' Women age 15 years and above wih Elevated blood pressure (Systolic ?140 mm of Hg and/or Diastolic ?90 mm of Hg) or taking medicine to control blood pressure (%)':'Women High BP % ','Men age 15 years and above wih Elevated blood pressure (Systolic ?140 mm of Hg and/or Diastolic ?90 mm of Hg) or taking medicine to control blood pressure (%)':'Men high BP %',' Men age 15 years and above who use any kind of tobacco (%)': 'Men Tobacco %','Women age 15 years and above who consume alcohol (%)' : 'Women Alcohol %','Men age 15 years and above who consume alcohol (%)':'Men Alcohol %'}, inplace=True)

"""# List of columns:"""

print(df.shape)
df.head()

column_list = list(df.columns)
column_list

"""# Causal Study:

We will study the effects of Health and education in young women and mothers on the health and well being of children below 5 years of age.

Features type :

1. Education level in Women and girls
2. Living conditions related to work and hygiene in Women and Girls
3. Co morbidities and health status of women

Target (dependent variables):

1.'Total children age 6-23 months receiving an adequate diet16, 17  (%)',
2. 'Children under 5 years who are stunted (height-for-age)18 (%)',
3. 'Children under 5 years who are wasted (weight-for-height)18 (%)',
4. 'Children under 5 years who are severely wasted (weight-for-height)19 (%)',
5. 'Children under 5 years who are underweight (weight-for-age)18 (%)',
6. 'Children under 5 years who are overweight (weight-for-height)20 (%)'
7. 'Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)'
8. 'Children Prevalence of symptoms of acute respiratory infection (ARI) in the two weeks preceding the survey (Children under age 5 years) (%) '
9. 'Prevalence of diarrhoea in the 2 weeks preceding the survey (Children under age 5 years) (%) '

## Defining two separate data frames :

## 1. Femaledf
## 2. Childdf
"""

femaledf = df[['District Names',
 'State/UT',
'Female_school ever %',
 'population % electricity',
 'drinking water %',
 'sanitation %',
 'clean fuel %',
 'iodized salt %',
 'Health insurance/finance scheme %',
 'Women literacy %',
 'Women (age 15-49)  with 10 or more years of schooling (%)',
 'women child marriage %',
 'Births in the 5 years preceding the survey that are third or higher order (%)',
'Women menstural hygiene',
 'Family planning methods %',
 'Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Any modern method6 (%)',
 'Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Female sterilization (%)',
 'Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - IUD/PPIUD (%)',
 'Current Use of Family Planning Methods (Currently Married Women Age 15-49  years) - Pill (%)',
'Total Unmet need for Family Planning (Currently Married Women Age 15-49  years)7 (%)',
 'Unmet need for spacing (Currently Married Women Age 15-49  years)7 (%)',
 'Health worker ever talked to female non-users about family planning (%)',
'Mothers who had at least 4 antenatal care visits  (for last birth in the 5 years before the survey) (%)',
 'Mothers whose last birth was protected against neonatal tetanus (for last birth in the 5 years before the survey)9 (%)',
 'Mothers who consumed iron folic acid for 100 days or more when they were pregnant (for last birth in the 5 years before the survey) (%)',
 'Mothers who consumed iron folic acid for 180 days or more when they were pregnant (for last birth in the 5 years before the survey} (%)',
 'Registered pregnancies for which the mother received a Mother and Child Protection (MCP) card (for last birth in the 5 years before the survey) (%)',
 'Mothers who received postnatal care from a doctor/nurse/LHV/ANM/midwife/other health personnel within 2 days of delivery (for last birth in the 5 years before the survey) (%)',
 'Average out-of-pocket expenditure per delivery in a public health facility (for last birth in the 5 years before the survey) (Rs.)',
 'Children under age 6 months exclusively breastfed16 (%)',
 'Women (age 15-49 years) whose Body Mass Index (BMI) is below normal (BMI <18.5 kg/m2)21 (%)',
 'Women (age 15-49 years) who are overweight or obese (BMI ?25.0 kg/m2)21 (%)',
 'Women (age 15-49 years) who have high risk waist-to-hip ratio (?0.85) (%)',
'Non-pregnant women age 15-49 years who are anaemic (<12.0 g/dl)22 (%)',
 'Pregnant women age 15-49 years who are anaemic (<11.0 g/dl)22 (%)',
 'Anaemic women %',
 'All women age 15-19 years who are anaemic22 (%) ',
 'Women  age 15 years and above with high (141-160 mg/dl) Blood sugar level23 (%)',
 'Women age 15 years and above wih very high (>160 mg/dl) Blood sugar level23 (%)',
 'Women high blood sugar %',
'Women age 15 years and above wih Mildly elevated blood pressure (Systolic 140-159 mm of Hg and/or Diastolic 90-99 mm of Hg) (%)',
 'Women age 15 years and above wih Moderately or severely elevated blood pressure (Systolic ?160 mm of Hg and/or Diastolic ?100 mm of Hg) (%)',
 'Women age 15 years and above wih Elevated blood pressure (Systolic ?140 mm of Hg and/or Diastolic ?90 mm of Hg) or taking medicine to control blood pressure (%)',
'Women (age 30-49 years) Ever undergone a screening test for cervical cancer (%)',
 'Women (age 30-49 years) Ever undergone a breast examination for breast cancer (%)',
 'Women (age 30-49 years) Ever undergone an oral cavity examination for oral cancer (%)',
 'Women age 15 years and above who use any kind of tobacco (%)',
 'Women Alcohol %']]

femaledf.info()

"""## Child_df"""

childdf = df[['Total children age 6-23 months receiving an adequate diet16, 17  (%)',
'Children under 5 years who are stunted (height-for-age)18 (%)',
'Children under 5 years who are wasted (weight-for-height)18 (%)',
'Children under 5 years who are severely wasted (weight-for-height)19 (%)',
'Children under 5 years who are underweight (weight-for-age)18 (%)',
'Children under 5 years who are overweight (weight-for-height)20 (%)',
'Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)',
'Children Prevalence of symptoms of acute respiratory infection (ARI) in the 2 weeks preceding the survey (Children under age 5 years) (%) ',
'Prevalence of diarrhoea in the 2 weeks preceding the survey (Children under age 5 years) (%) ']]

childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)']

"""# Data Cleaning"""

# Function to clean some numerical columns

def cleaner(data):
  data = data.str.replace("(","",regex = False).str.replace(",","")
  data = data.str.replace(")","",regex = False).str.replace(",","")
  data = data.str.replace("''","",regex = False)
  data =  pd.to_numeric(data, errors = 'coerce')
  data = pd.DataFrame(data)
  return data

"""Here we have defined a function to clean our numerical data and convert data type to float or int 64"""

# @title
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)']= (
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'].str.replace("(","",regex = False).str.replace(",",""))

# @title
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)']= (
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'].str.replace(")","",regex = False).str.replace(",",""))

# @title
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)']= (
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'].str.replace("''","",regex = False))

# @title
pot = pd.DataFrame(childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'])

# @title

# Strip any leading/trailing spaces and then convert
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'] = (
    childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'].astype(str).str.strip()
)



# Convert to numeric
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'] = (
    pd.to_numeric(childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'], errors = 'coerce')
)

# Check unique values after conversion
cleaned = childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)']

# @title
cleaned = pd.DataFrame(cleaned)

# @title
cleaned.info()

# @title
childdf['Total children age 6-23 months receiving an adequate diet16, 17  (%)'] = cleaned

rot = cleaner(childdf['Children under 5 years who are stunted (height-for-age)18 (%)'])

childdf['Children under 5 years who are stunted (height-for-age)18 (%)'] = rot

fot = cleaner(childdf['Children under 5 years who are wasted (weight-for-height)18 (%)'])

childdf['Children under 5 years who are wasted (weight-for-height)18 (%)'] = fot

joy = cleaner(childdf['Children under 5 years who are severely wasted (weight-for-height)19 (%)'])

childdf['Children under 5 years who are severely wasted (weight-for-height)19 (%)'] = joy

koy = cleaner(childdf['Children under 5 years who are underweight (weight-for-age)18 (%)'])

childdf['Children under 5 years who are severely wasted (weight-for-height)19 (%)'] = koy

loy  = cleaner(childdf['Children under 5 years who are underweight (weight-for-age)18 (%)'])
childdf['Children under 5 years who are underweight (weight-for-age)18 (%)'] = loy

poy = cleaner(childdf['Children under 5 years who are overweight (weight-for-height)20 (%)'])
childdf['Children under 5 years who are overweight (weight-for-height)20 (%)'] = poy

yoy = cleaner(childdf['Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)'])
childdf['Children age 6-59 months who are anaemic (<11.0 g/dl)22 (%)'] = yoy

"""# Cleaned Childdf:

## All the columns are converted to float data type

"""

childdf.info()

"""Hence childdf is completely cleaned

# Cleaning Femaledf
"""

femaledf.info()

femaledf['women child marriage %'] = cleaner(femaledf['women child marriage %']).astype(float)

femaledf['Births in the 5 years preceding the survey that are third or higher order (%)'] = cleaner(femaledf['Births in the 5 years preceding the survey that are third or higher order (%)']).astype(float)

femaledf['All women age 15-19 years who are anaemic22 (%) '] = cleaner(femaledf['All women age 15-19 years who are anaemic22 (%) ']).astype(float)

femaledf['Pregnant women age 15-49 years who are anaemic (<11.0 g/dl)22 (%)'] = cleaner(femaledf['Pregnant women age 15-49 years who are anaemic (<11.0 g/dl)22 (%)']).astype(float)

goggins = pd.DataFrame(femaledf.iloc[:,22:29])
goggins.columns

femaledf['Mothers who had at least 4 antenatal care visits  (for last birth in the 5 years before the survey) (%)'] = cleaner(femaledf['Mothers who had at least 4 antenatal care visits  (for last birth in the 5 years before the survey) (%)']).astype(float)
femaledf['Mothers whose last birth was protected against neonatal tetanus (for last birth in the 5 years before the survey)9 (%)'] = cleaner(femaledf['Mothers whose last birth was protected against neonatal tetanus (for last birth in the 5 years before the survey)9 (%)']).astype(float)
femaledf['Mothers who consumed iron folic acid for 100 days or more when they were pregnant (for last birth in the 5 years before the survey) (%)'] = cleaner(femaledf['Mothers who consumed iron folic acid for 100 days or more when they were pregnant (for last birth in the 5 years before the survey) (%)']).astype(float)
femaledf['Mothers who consumed iron folic acid for 180 days or more when they were pregnant (for last birth in the 5 years before the survey} (%)'] = cleaner(femaledf['Mothers who consumed iron folic acid for 180 days or more when they were pregnant (for last birth in the 5 years before the survey} (%)']).astype(float)
femaledf['Registered pregnancies for which the mother received a Mother and Child Protection (MCP) card (for last birth in the 5 years before the survey) (%)'] = cleaner(femaledf['Registered pregnancies for which the mother received a Mother and Child Protection (MCP) card (for last birth in the 5 years before the survey) (%)']).astype(float)
femaledf['Mothers who received postnatal care from a doctor/nurse/LHV/ANM/midwife/other health personnel within 2 days of delivery (for last birth in the 5 years before the survey) (%)'] = cleaner(femaledf['Mothers who received postnatal care from a doctor/nurse/LHV/ANM/midwife/other health personnel within 2 days of delivery (for last birth in the 5 years before the survey) (%)']).astype(float)
femaledf['Average out-of-pocket expenditure per delivery in a public health facility (for last birth in the 5 years before the survey) (Rs.)'] = cleaner(femaledf['Average out-of-pocket expenditure per delivery in a public health facility (for last birth in the 5 years before the survey) (Rs.)']).astype(float)

femaledf = femaledf.drop(columns = ['Children under age 6 months exclusively breastfed16 (%)'])

"""# Cleaned Femaledf:"""

femaledf.info()

column_lis = list(femaledf.columns)
column_listt = column_lis[2:]

"""# NaN values
Let's check for NaN values and remove them if they're present

So we do have some NaN values.
Lets simple Impute them.
"""

# Imputing missing values with their means

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')
childdf_imp = pd.DataFrame(imputer.fit_transform(childdf), columns=childdf.columns)

femaledf_imp = pd.DataFrame(imputer.fit_transform(femaledf.iloc[:,2:]), columns= femaledf.iloc[:,2:].columns)

"""So here we have succesfully cleaned the Femaledf(related to the features of our future model)."""

X = femaledf_imp
y_anaemic = childdf_imp

"""# Scaling our data

We will try and apply two Scalers on our data namely:

1. MinMax Scaler : transform data to the range [0,1]
2. Robust Scaler : transform data and make it immune to outliers (But can have negative values).


"""

y_anaemic = pd.DataFrame(y_anaemic)

"""# MIn MAx scaling

"""

# @title

from sklearn.preprocessing import MinMaxScaler

minmax = MinMaxScaler()
min_max_scaled = minmax.fit_transform(X)
X_minmax= pd.DataFrame(min_max_scaled)

# @title
min_max_scaledy = minmax.fit_transform(y_anaemic)
y_anaemic_minmax  = pd.DataFrame(min_max_scaledy)

# @title
X_minmax.head()

# @title
y_anaemic_minmax

# @title
# Train Test Split:

X_train,X_test,y_train,y_test = train_test_split(X_minmax,y_anaemic_minmax.iloc[:,6],test_size=0.2,random_state=2)

# @title
# Linear Regression
reg = LinearRegression()
reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
t = r2_score(y_test,y_pred)

# @title
# Ridge
reg = Ridge(alpha=0.1)
reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
r2_score(y_test,y_pred)

# @title
# Lasso
reg = Lasso(alpha=0.01)
reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
r2_score(y_test,y_pred)

# @title
# ElasticNet
reg = ElasticNet(alpha=0.005,l1_ratio=0.9)
reg.fit(X_train,y_train)
y_pred = reg.predict(X_test)
r2_score(y_test,y_pred)

"""# Robust Scaling"""

from sklearn.preprocessing import RobustScaler

robust = RobustScaler()
X_robust = robust.fit_transform(X)
y_anaemic_robust  = pd.DataFrame(robust.fit_transform(y_anaemic))

#Robust Scaled Train-Test Split
X_train2,X_test2,y_train2,y_test2 = train_test_split(X_robust,y_anaemic_robust.iloc[:,6],test_size=0.2,random_state=2)

X.columns

y_anaemic.columns

X_train.columns = column_listt

X_train.columns

# Gradient boosting and RF

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

gbm = GradientBoostingRegressor()
gbm.fit(X_train2,y_train2)
y_pred2 = reg.predict(X_test2)
print(f"{r2_score(y_test2,y_pred2)} GBM")


rf = RandomForestRegressor()
rf.fit(X_train2,y_train2)
y_pred2 = reg.predict(X_test2)
print(f"{r2_score(y_test2,y_pred2)} RF")

# Linear Regression
reg = LinearRegression()
reg.fit(X_train2,y_train2)
y_pred2 = reg.predict(X_test2)
print(f"{r2_score(y_test2,y_pred2)} Linear Regression")

# feature importance :
print(f"highest coefficient = {max(reg.coef_)}")
feature_importance = np.abs(reg.coef_)
max_index = np.argmax(feature_importance)
print(f"Index of the column having the highest weight: {max_index}")




# Ridge
reg = Ridge(alpha=0.1)
reg.fit(X_train2,y_train2)
y_pred2 = reg.predict(X_test2)
print(f"{r2_score(y_test2,y_pred2)} Ridge")


# Lasso
reg = Lasso(alpha=0.01)
reg.fit(X_train2,y_train2)
y_pred2 = reg.predict(X_test2)
print(f"{r2_score(y_test2,y_pred2)} Lasso")


# ElasticNet
reg = ElasticNet(alpha=0.005,l1_ratio=0.9)
reg.fit(X_train2,y_train2)
y_pred2 = reg.predict(X_test2)
print(f"{r2_score(y_test2,y_pred2)} Elastic Net")


print("\n")
most_imp_feature = X_train.columns[4]
print(f"Feature having the highest impact on the percentage of anaemic kids in a district:{most_imp_feature}")

"""# Plotting the preliminary outcomes

Bar Plot for r2_scores
"""

#
model_names = ['Simple Regression', 'Ridge', 'LASSO', 'ElasticNet']

# R² scores for MinMax scaled data
r2_scores_minmax = [0.5447,0.5469,0.2902,0.4150]
# R² scores for Robust scaled data
r2_scores_robust = [0.5447,0.5447,0.5577,0.5594]

# Create a DataFrame for plotting
data = {
    'Model': model_names * 2,
    'R² Score': r2_scores_minmax + r2_scores_robust,
    'Scaling': ['MinMax'] * len(model_names) + ['Robust'] * len(model_names)
}

dt = pd.DataFrame(data)
# Set the plot style
sns.set(style="whitegrid")

# Create the bar plot
plt.figure(figsize=(10, 7))
sns.barplot(x='Model', y='R² Score', hue='Scaling', data=dt, palette='viridis')

# Add title and labels
plt.title('Comparison of R² Scores for Anaemia in kids')
plt.xlabel('Model')
plt.ylabel('R² Score')
plt.legend(loc='upper center')
# Show the plot
plt.show()

"""So for our current dataset and hypothesis,

Elastic NET with Robust Scaling works best but not satisfactory yet.

## Insight-1

About 55% of the variance in Children Anameia percentage can be explained from Mother health, education and living condition factors.

Rest 55% can be explained using conditions of children and other minor factors.


## Insight-2

The weight for clean fuel % is highest among all other factors (~0.45) in child anaemia cases can be explained by the percentage of usage of clean fuel in a household. This suggest that the usage of unclean fuel is highly correlated to child anaemia in poor Indian households.

# Study-2:  Stuntness in Children


Now we sill study about the top factors of Stuntness recorded in children below the age of 5
"""

# We will use the imputed versions of Child and Female Data Frames

childdf_imp.info()

femaledf_imp.info()

"""# Child and Mother Correlation Heatmap:"""

# Concatenate the DataFrames
combined_df = pd.concat([femaledf_imp, childdf_imp], axis=1)

# Compute the correlation matrix
corr_matrix = combined_df.corr()


plt.figure(figsize=(15, 15))
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', vmin=-1, vmax=1,xticklabels = True, yticklabels = True)
plt.title('Correlation Heatmap')
plt.show()

