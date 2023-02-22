# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from datetime import timedelta,date

# %%
dataframe=pd.read_csv('./data.csv',usecols=['periodid','Nakuru County']).dropna()


# %%
dataframe['periodid']=pd.to_datetime(dataframe['periodid'])
dset_indexed=dataframe.set_index(['periodid'])


# %%
dset_indexed.plot(style='-', figsize=(15,10),color='blue',title='Commodity Demand')
plt.xlabel('Years')
plt.ylabel('Demand')
plt.savefig('Nakuru Series.png')

# %%
#train data
#upper bound
train=dset_indexed.loc[dset_indexed.index<'01-01-2021']
#test data
#lower bound
test=dset_indexed.loc[dset_indexed.index>='01-01-2021']

# %%
dset_indexed.loc[(dset_indexed.index>'01-01-2018')&(dset_indexed.index<'12-31-2018')].plot(figsize=(15,10), title='Trend in 2018')
plt.xlabel('Years')
plt.ylabel('Demand')
plt.savefig('Nakuru 2018.png')

# %%
dset_indexed.loc[(dset_indexed.index>'01-01-2022')&(dset_indexed.index<'12-31-2022')].plot(figsize=(15,10), title='Trend in 2022')
plt.xlabel('Years')
plt.ylabel('Demand')
plt.savefig('Nakuru 2022.png')

# %% [markdown]
# ## Generating Features
# We generate our features using time series index, where it is provided by pandas

# %%

def feature_generator(dF):
    dF=dF.copy()
    dF['year']=dF.index.year#year
    dF['month']=dF.index.month #we get month from our datetime index
    
    return dF


# %%
df=feature_generator(dset_indexed)
df.head()


# %% [markdown]
# ### Some of the basic discoveries with our new features
# Let's use a box plot and see the distribution of the data frame

# %%
fig,ax=plt.subplots(figsize=(10,8))
sns.boxplot(data=df,x='month',y='Nakuru County')
ax.set_title('Purchase per Month in Nakuru')
plt.savefig('Nakuru Month.png')


# %%
#run train and test through features function to create features we are going to use
train_set=feature_generator(train)
test_set=feature_generator(test)


# %%
FEATURES=['year','month']
TARGET='Nakuru County'

# %%
X_train=train_set[FEATURES]
y_train=train_set[TARGET]

X_test=test_set[FEATURES]
y_test=test_set[TARGET]


# %%
#model
reg=xgb.XGBRegressor(n_estimators=1000, early_stopping_rounds=50)
reg.fit(X_train,y_train,eval_set=[(X_train,y_train),(X_test,y_test)],verbose=100)

# %%
test['prediction']=reg.predict(X_test)

# %%
df=df.merge(test[['prediction']], how='left',left_index=True,right_index=True)


# %% [markdown]
# Further experiments

# %%
def timeseries_predictor(starting_date,end_date):
    #date format '2022-01'
    
    dates_array=[]
    dates=pd.date_range(starting_date,end_date)
    for date in dates:
        dates_array.append([date.year,date.month])
    transf_dates_array=np.unique(dates_array,axis=0)
    
    date_input=pd.DataFrame(data=transf_dates_array,columns=['year','month'])
    date_input
    y_hat=reg.predict(date_input)
    
    y_bar=y_hat
    x_bar=transf_dates_array[:,1]
    plt.xlabel('Month')
    plt.ylabel('Commodity demand')
    plt.title('Malaria Commodity Demand, Nakuru Prediction')
    plt.bar(x_bar,y_bar)
    plt.savefig('Prediction.png')





#print(int(starting_date[5:]))

# %%
#timeseries_predictor('2023-02','2023-06') - test


