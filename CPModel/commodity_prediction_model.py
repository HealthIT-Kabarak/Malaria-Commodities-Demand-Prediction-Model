#importing the required python libraries
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#test functionality
#test_county=input("Please key in your county: ")
#test_str_date=datetime(*map(int,input("Initial date yyyy-mm-dd: ").split("-")))
#test_end_date=datetime(*map(int,input("End date yyyy-mm-dd: ").split("-")))

#generates features
def feature_generator(dF):
    dF=dF.copy()
    dF['year']=dF.index.year#year
    dF['month']=dF.index.month #we get month from our datetime index
    
    return dF

def infer_model(county,start_date,end_date,pstr_date,pend_date):
    dataframe=pd.read_csv('./Data/data.csv',usecols=['periodid',county]).dropna()
    dataframe['periodid']=pd.to_datetime(dataframe['periodid'])
    dset_indexed=dataframe.set_index(['periodid'])
    plt.figure()#to avoid saving one type of plot
    plt.xlabel('Year')
    dset_indexed.plot(style='-', figsize=(15,5),color='blue',title='Commodity Demand')
    #save the picture for the county trend
    plt.savefig("./static/renderImages/county-trend.png")
    #split to train and split data set
    train=dset_indexed.loc[dset_indexed.index<'01-01-2021']
    test=dset_indexed.loc[dset_indexed.index>='01-01-2021'] 
    
    initial_date=start_date#yyyy-mm-dd
    final_date=end_date#yyyy-mm-dd
    
    #annual trend
    plt.figure()
    #time series plot
    dset_indexed.loc[(dset_indexed.index>initial_date)&(dset_indexed.index<final_date)].plot(figsize=(15,5), title=f"Trend {start_date} - {end_date}")
    plt.savefig("./static/renderImages/time-trend.png")
    
    #generate feature from indexed data
    df=feature_generator(dset_indexed)
    
    
    #save county box plot
    fig,ax=plt.subplots(figsize=(10,8))
    sns.boxplot(data=df,x='month',y=county)# the county specified at the top
    ax.set_title(f"Purchase per Month in {county}")
    plt.savefig("./static/renderImages/county-boxplot.png")
    
    #import necessary libraries then make pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.pipeline import Pipeline
    
    #run train and test through features function to create features we are going to use
    train_set=feature_generator(train)
    test_set=feature_generator(test)
    
    FEATURES=['year','month']
    TARGET=county
    
    X_train=train_set[FEATURES]
    y_train=train_set[TARGET]

    X_test=test_set[FEATURES]
    y_test=test_set[TARGET]
    
    #model pipeline
    model_pipeline=Pipeline([('scaler',StandardScaler()),('gbr',GradientBoostingRegressor(n_estimators=2500,loss='absolute_error',learning_rate=0.001))])
    
    #we fit the ML pipeline
    model_pipeline.fit(X_train,y_train)
    
    #add the predicted values to the dataframe
    test['prediction']=model_pipeline.predict(X_test)
    df=df.merge(test[['prediction']], how='left',left_index=True,right_index=True)
    
    #project prediction
    plt.figure()
    ax=df[county].plot(figsize=(15,5))
    df['prediction'].plot(ax=ax,style='-')
    plt.legend(['Original Data','Predictions'])
    ax.set_title('Original Plot Vs Projection')
    plt.savefig("./static/renderImages/trend-prediction.png")
    
    #create prediction with bar charts
    start_date=pstr_date.strftime('%Y-%m')
    end_date=pend_date.strftime('%Y-%m')
    dates_array=[]
    dates=pd.date_range(start_date,end_date)
    for date in dates:
        dates_array.append([date.year,date.month])
    transf_dates_array=np.unique(dates_array,axis=0)
    
    #the prediction
    date_input=pd.DataFrame(data=transf_dates_array,columns=['year','month'])
    y_hat=model_pipeline.predict(date_input)
    
    #the bar chart plot
    y_bar=y_hat
    x_bar=transf_dates_array[:,1]
    plt.figure()
    plt.xlabel('Month')
    plt.ylabel('Commodity demand')
    plt.title(f"Malaria Commodity Demand, {county} Prediction")
    plt.bar(x_bar,y_bar)
    plt.savefig("./static/renderImages/county-barchart.png")
    
    # Make predictions using the model
    predictions = y_hat

    # Create an array of indices for the x-axis
    x_bar = range(len(predictions))

    # Plot the increasing trend line
    plt.figure()
    plt.plot(x_bar, predictions)
    plt.xlabel('Index')
    plt.ylabel('Commodity demand')
    plt.title(f"Malaria Commodity Demand Trend {start_date} - {end_date} ")
    plt.savefig("./static/renderImages/line-trend.png")
    
    return predictions

#print(f"Kisumu County Predictions for dates {test_str_date}-{test_end_date}: {infer_model(test_county,test_str_date,test_end_date)}")



    
    
    