import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np 
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer,r2_score
from sklearn.model_selection import train_test_split
from numpy import absolute
from pandas import read_csv
from sklearn.model_selection import RepeatedKFold
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
df=pd.read_csv('anime project.csv')
print(df)
plt.scatter(df['score'],df['rank'])
plt.xlabel('score')
plt.ylabel('rank')
plt.show()
print('The correlation between rank and score is:'+ str(df['score'].corr(df['rank'])))
plt.style.use('classic')
plt.scatter(df['likes'],df['popularity'])
plt.xlabel('likes')
plt.ylabel('popularity')
plt.show()
print('The most popular animes are also the least liked ones')
plt.scatter(df['likes'],df['scored_by'])
plt.xlabel('likes')
plt.ylabel('scored_by')
plt.figure(figsize=(8, 6))
plt.show()
percentagetype=df.groupby(by=["type"]).size()
plt.pie(percentagetype)
red_patch = mpatches.Patch(color='c', label='OVA')
green_patch=mpatches.Patch(color='r',label='ONA')
blue_patch=mpatches.Patch(color='b',label='Movie')
purple_patch=mpatches.Patch(color='m',label='Special')
brown_patch=mpatches.Patch(color='yellow',label='TV')
yellow_patch=mpatches.Patch(color='green',label='Music')
plt.legend(handles=[red_patch,green_patch,blue_patch,purple_patch,brown_patch,yellow_patch],bbox_to_anchor=(1,1.025), loc="upper left")
plt.figure(figsize=(1,1))
plt.show()
avg_n_of_episodes_per_type=df.groupby('type', as_index=False)['episodes'].mean()
avg_n_of_episodes_per_type.values.reshape(1,-1)
plt.style.use('dark_background')
plt.bar(avg_n_of_episodes_per_type['type'],avg_n_of_episodes_per_type['episodes'],color='orange')
plt.xlabel(' type')
plt.ylabel('average number of episodes ')
plt.figure(figsize=(1, 1))
plt.show()
#Checking for null values 
MVpercentages = (df.isnull().sum()/df.shape[0]).sort_values(ascending=False)
print(MVpercentages.head(10))
#Looking for instances with null values in the rank column
NaN_rows = df[df['rank'].isnull()]
print(NaN_rows)
#deleting instances with null values 
df.dropna(subset=['rank','score','scored_by'], inplace=True)
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.shape
#Creating predictors and target variable 
X=df [['score','rank','popularity','scored_by']]
Y=df['likes']
Y=Y.values.reshape(-1,1)
#Plotting distribution of target variable 'likes'
plt.style.use('classic')
plt.hist(df['likes'], color = 'blue', edgecolor = 'white',bins = int(20))
plt.xlabel('likes ')
plt.show()
#Normalizing the distribution of the target variable likes (on the y axis there is the frequency )
scaler=StandardScaler()
Y=scaler.fit_transform(Y)
X=scaler.fit_transform(X)
plt.hist(Y, color = 'blue', edgecolor = 'black',
         bins = int(20))
plt.xlabel('likes normalized')
plt.show()
#Performing a train-test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=42)
#1st model with a simple multivariate linear regression 
model1=LinearRegression()
model1.fit(X_train,Y_train)
Y_pred = model1.predict(X_test)
print('Rsquared of the Linear Regression model is: '+ str(r2_score(Y_pred,Y_test)))
#Cross validation on linear regression model 
model1cv=LinearRegression()
model1cv.fit(X_train,Y_train)
cv_r2_scores_rf = cross_val_score(model1cv, X, Y, cv=5,scoring='r2')
print(cv_r2_scores_rf)
print("Mean 5-Fold R Squared of the Random Forest model is: {}".format(np.mean(cv_r2_scores_rf)))
#2nd model with Random forest regressor.We're using cross validation since we only have a few thousands of observations
model2 = RandomForestRegressor(n_estimators=20, random_state=0)
model2.fit(X_train, np.ravel(Y_train, order='c'))
Y_pred2=model2.predict(X_test)
print('R2 squared of the Random forest model is:' +str(r2_score(Y_pred2,Y_test)))
#2 model with Random forest but with cross validation score and not simply train-test splot
model2cv=RandomForestRegressor(n_estimators=20,random_state=0)
cv_r2_scores_rf = cross_val_score(model2cv, X, Y, cv=5,scoring='r2')
print(cv_r2_scores_rf)
print("Mean 5-Fold R Squared of the Random Forest model is: {}".format(np.mean(cv_r2_scores_rf)))
#3rd model with Extreme Gradient boosting 
model3=XGBRegressor()
model3.fit(X_train,Y_train)
Y_pred3= model3.predict(X_test)
print('The Rsquared of the XGBoost model is: '+ str(r2_score(Y_pred3,Y_test)))
#3rd modek with Extreme Gradient boosting but with cross validation score and not mere train-test split 
model3cv=XGBRegressor()
cv_r2_scores_rf = cross_val_score(model3cv, X, Y, cv=5,scoring='r2')
print(cv_r2_scores_rf)
print("Mean 5-Fold R Squared of the XGBoost model is: {}".format(np.mean(cv_r2_scores_rf)))
