import numpy as np
import pandas as pd
import matplotlib.pylab as plt

#status second commit
df =pd.read_csv('C:\\Users\pickme1035\Desktop\DS\Machine Learning A-Z Template Folder\Part 1 - Data Preprocessing\gasUsage.csv')

from datetime import datetime
indexed_dataset = df.set_index(['Month'])
indexed_dataset.head()
indexed_dataset.tail()

plt.title("Raw Data")
plt.plot(indexed_dataset)

#calcualting the mean and std at a given interval (interval of 12 months)
rol_mean = indexed_dataset.rolling(window = 12).mean()
rol_std = indexed_dataset.rolling(window = 12).std()

"""

#plotting the calcualted mean and standard deviation
dataset = plt.plot(indexed_df, color = 'blue', label = 'Normal Data')
mean = plt.plot(rol_mean, color='red', label = 'mean')
std = plt.plot(rol_std, color='black', label = 'std')
plt.show(block=False)



#perform of Dickey-Fullers Test to confirm that the data is not stationary
from statsmodels.tsa.stattools import adfuller

print('Results of Dicky Fullers Test')
dftest = adfuller(indexed_df['Mins'], autolag = 'AIC')

dfoutput = pd.Series(dftest[0:4], index = ['Test Statistic', 'p-value', 'lags Used', 'Number of Observations used'])
for key,value in dftest[4].items():
    dfoutput['Critical Value (%s)'%key] = value
                            
print(dfoutput)

#for us to confirm that the data is not stationary we have to check the Critical Value cannot exceed the Test statistic, here we can see that the data is not stationary
"""

#very important step to convert the data to a log format which will be used later
indexedDataset_logscale = np.log(indexed_dataset)
plt.title("Logged Data")
plt.plot(indexedDataset_logscale)

#plotting the moving average against the indexed raw data
moving_average = indexedDataset_logscale.rolling(window = 12).mean()
plt.title("Logged Data")
plt.plot(indexedDataset_logscale, color = 'blue')

plt.title("Moving Average")
plt.plot(moving_average, color= 'red')
plt.show()

#the above two data tests which are the mean, std & dicky-fuellers test, which is compulsory to decide wether the data is stationary or movinf with time to apply the time serires
from statsmodels.tsa.stattools import adfuller
def test_staionary(timeseries):
    
    #determining rolling statistics
    rol_mean = timeseries.rolling(window = 12).mean()
    rol_std = timeseries.rolling(window = 12).std()
    
    #plotting the rolling stats comparitive to the real data
    dataset = plt.plot(timeseries, color = 'blue', label = 'Normal Data')
    plt.title("Rolling Mean")
    mean = plt.plot(rol_mean, color='red', label = 'mean')
    plt.title("Rolling Standard Deviation")
    std = plt.plot(rol_std, color='black', label = 'std')
    plt.show(block=False)
    
    #performing the Dicky-fuellers Test
    print('Results of Dicky Fullers Test')
    dftest = adfuller(timeseries['Mins'], autolag = 'AIC')

    dfoutput = pd.Series(dftest[0:4], index = ['Test Statistic', 'p-value', 'lags Used', 'Number of Observations used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value

    print(dfoutput)

    #for us to confirm that the data is not stationary we have to check the Critical Value cannot exceed the Test statistic, here we can see that the data is not stationary

#shifted the values by one to observe the to the left to oberserve the lag between two timestamps
df_logshifting = indexedDataset_logscale - indexedDataset_logscale.shift()
df_logshifting.dropna(inplace = True) #remove nan values when the topmost index is shifted
plt.title("Log Shifted Data")
plt.plot(df_logshifting)

#do the test to confirm that data is not stationary
test_staionary(df_logshifting)

from statsmodels.tsa.seasonal import seasonal_decompose
decomposition= seasonal_decompose(indexedDataset_logscale, freq = 1)
#decomposition = seasonal_decompose(indexedDataset_logscale)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.title("Logged Data")
plt.plot(indexedDataset_logscale, label = 'Original')
plt.legend(loc = 'best')

plt.subplot(412)
plt.title("Trend Data")
plt.plot(trend, label = 'Trend')
plt.legend(loc = 'best')

plt.subplot(413)
plt.title("Seasonal Data")
plt.plot(seasonal,  label = 'Seasonal')
plt.legend(loc = 'best')

plt.subplot(414)
plt.title("Residual Data")
plt.plot(residual,  label = 'Residual')
plt.legend(loc = 'best')
plt.tight_layout


#get residual data to clean noise
decomposedLogData = residual
decomposedLogData.dropna(inplace = True)
test_staionary(decomposedLogData)

#getting an idea for p,q values needed to apply ARIMA model
from statsmodels.tsa.stattools import acf,pacf

lag_acf = acf(indexedDataset_logscale, nlags= 20) 
lag_pacf = pacf(indexedDataset_logscale,nlags= 20, method= 'ols')

#plot Auto Correlation Function : to calc q 
plt.subplot(121) 
plt.plot(lag_acf) 
plt.title('Auto Correlation Function')

#plot Partial Auto Correlation Function : to calc p 
plt.subplot(122) 
plt.plot(lag_pacf) 
plt.title('Partial Auto Correlation Function') 
plt.tight_layout()

#checking Auto Regression
from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(indexedDataset_logscale, order = (2,1,0)) #ARIMA models expect the values of P,D,Q
results_AR = model.fit(disp = -1)
plt.subplot(121) 
plt.title('Logged Data')
plt.plot(df_logshifting)

plt.subplot(122) 
plt.title('Auto Regression Curve')
plt.plot(results_AR.fittedvalues, color = 'red')
data = (results_AR.fittedvalues-df_logshifting['Mins'])**2
plt.title(data.sum(axis =0, skipna=True))
print('Plotting AR Model')

#checking the moving average by varying the p,q values
from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(indexedDataset_logscale, order = (2,1,1)) #ARIMA models expect the values of P,D,Q

plt.subplot(211)
results_MA = model.fit(disp = -1)
plt.title('Logged Data')
plt.plot(df_logshifting)

plt.subplot(212)
plt.plot(results_MA.fittedvalues, color = 'red')
plt.title('Moving Average Curve')
data = (results_MA.fittedvalues-df_logshifting['Mins'])**2
plt.title(data.sum(axis =0, skipna=True))
print('Plotting MA Model')


#integrating the AR and MA models with p,d,q(2,1,1) values which gives the minimum values for RSS
from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(indexedDataset_logscale, order = (2,1,1)) #ARIMA models expect the values of P,D,Q
results_ARIMA = model.fit(disp = -1)
plt.subplot(211)
plt.plot(df_logshifting)

plt.subplot(212)
plt.title('ARIMA model curve')
plt.plot(results_ARIMA.fittedvalues, color = 'red')
data = (results_ARIMA.fittedvalues-df_logshifting['Mins'])**2
plt.title(data.sum(axis =0, skipna=True))
print('Plotting ARIMA Model')

#The least value is obtained for the combination of the above p,d,q values, which will be our final prediction value

#the model is done, we have to convert them to their original values now
predicted_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy = True)
print(predicted_ARIMA_diff.head())

#calculating the cumulative sum
predicted_ARIMA_diff_cumsum = predicted_ARIMA_diff.cumsum()
print(predicted_ARIMA_diff_cumsum.head())

#getting the log value (sqrt) of the needed predicted values through ARIMA
predictions_ARIMA_log = pd.Series(indexedDataset_logscale['Mins'].ix[0],index=indexedDataset_logscale.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predicted_ARIMA_diff_cumsum, fill_value = 0)
predictions_ARIMA_log.head()

#converting them to the original data format
predictions_ARIMA = np.exp(predictions_ARIMA_log)

plt.subplot(211)
plt.title('Logged Data')
plt.plot(indexed_dataset)

plt.subplot(212)
plt.title('Predicted Data')
plt.plot(predictions_ARIMA)

#we have data for 36 months, now we can plot the data for 108 months
results_ARIMA.plot_predict(1,108)
plt.title('Future Forcast')
plt.show()

def predict_gasUsage(date):
    try:
         year_var = (int(date.year) - 2016)*12
         month_var = int(date.strftime("%d"))
         prediction_index = year_var + month_var + indexed_dataset.count()
    
         #finally to obtain data for the 10 years (1200 records)
         df_predcited = results_ARIMA.forecast(steps = 1200)
         #print(df_predcited)
         predicted_gasUsage = df_predcited[0][prediction_index - 1]
         print("You predicted Gas Usage for ", date.strftime("%B"), " is ",predicted_gasUsage*10**3 , "mins")
         #return predicted_gasUsage
        
    except:
        user_date = input('Please Enter in yyyy/mm format the day you want find the usage for :',)
        #year = user_date.split("/",1)[0]
        #print(year)
        year_var = (int(user_date.split("/",1)[0]) - 2016)*12
        #print(year_var)
        month_var = int(user_date.split("/",1)[1])
        if month_var > 12 or month_var <=0:
            print('Invalid Month value')
            
        else:
            prediction_index = year_var + month_var + indexed_dataset.count()
            predicted_gasUsage = df_predcited[0][prediction_index - 1]
            print("You predicted Gas Usage for ",month_var," is ",predicted_gasUsage*10**3 , "mins")
            
        
            
            
        
   


#test
predict_gasUsage(6)
df_predcited = results_ARIMA.forecast(steps = 108)

a=10
b=20
    


