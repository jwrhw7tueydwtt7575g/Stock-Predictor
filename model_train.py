import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# 1. Download stock data
def get_data(ticker):
    stock_data = yf.download(ticker, start='2024-01-01')
    return stock_data['Close']


# 2. Check if the data is stationary
def stationary_check(close_price):
    adf_test = adfuller(close_price)
    p_value = round(adf_test[1], 3)
    return p_value


# 3. Rolling mean (optional)
def get_rolling_mean(close_price):
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price


# 4. Find differencing order to make data stationary
def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    while True:
        if p_value > 0.05:
            d += 1
            close_price = close_price.diff().dropna()
            p_value = stationary_check(close_price)
        else:
            break
    return d


# 5. Fit ARIMA model
def fit_model(data, differencing_order):
    model = ARIMA(data, order=(30, differencing_order, 30))
    model_fit = model.fit()
    
    forecast_steps = 30
    forecast = model_fit.get_forecast(steps=forecast_steps)
    predictions = forecast.predicted_mean
    
    return predictions


# 6. Evaluate using RMSE
def evaluate_model(original_price, differencing_order):
    train_data, test_data = original_price[:-30], original_price[-30:]
    predictions = fit_model(train_data, differencing_order)
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse, 2)


# 7. Apply scaling
def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1, 1))
    return scaled_data, scaler


# 8. Inverse the scaling
def inverse_scaling(scaler, scaled_data):
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1, 1))
    return close_price


# 9. Generate forecast DataFrame
def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)

    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=29)).strftime('%Y-%m-%d')
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')

    forecast_df = pd.DataFrame(predictions, index=forecast_index, columns=['Close'])
    return forecast_df
