import pandas as pd
import pandas_datareader as pdr
from Forecaster import Forecaster

df = pdr.get_data_fred('HOUSTNSA',start='1900-01-01',end='2021-05-01')
f = Forecaster(y=df['HOUSTNSA'],current_dates=df.index)
f.set_test_length(12)
f.generate_future_dates(24) # forecast length
f.add_ar_terms(4)
f.add_AR_terms((2,12)) # seasonal AR terms
f.add_seasonal_regressors('month','dayofyear','week',raw=False,sincos=True)
f.add_seasonal_regressors('year')
f.add_covid19_regressor() # default is from when disney world closed to when U.S. cdc no longer recommended masks but can be changed
f.add_time_trend()
f.add_combo_regressors('t','COVID19') # multiplies time trend and COVID19 regressor
f.add_poly_terms('t') # t^2
f.diff() # non-stationary data forecasts better differenced with this model
f.set_estimator('elasticnet')
f.manual_forecast(alpha=.5,l1_ratio=.5,normalizer='scale')

f.undiff() # drops all added regressors

f.set_estimator('arima')
f.manual_forecast(order=(1,1,1),seasonal_order=(2,1,0,12),trend='ct')

f.plot()