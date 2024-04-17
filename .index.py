from flask import Flask, render_template
import yfinance as yf
import tensorflow as tf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_data(self):
        self.data = yf.download(self.ticker, start='2023-01-01', end=dt.datetime.now().strftime('%Y-%m-%d'))

    def calculate_regression(self):
        self.predictions = {}
        for column in ['Open', 'High', 'Low', 'Close']:
            x = np.array(range(len(self.data)))
            y = np.array(self.data[column])
            model = tf.keras.Sequential()
            model.add(tf.keras.layers.Dense(1, activation=tf.exp, input_shape=[1]))
            model.compile(optimizer=tf.optimizers.Adam(0.01), loss='mean_squared_error')
            model.fit(x, y, epochs=100)
            self.predictions[column] = model.predict(x)

    def regression(self):
        self.predictions = {}
        for column in ['Open', 'High', 'Low', 'Close']:
            x = np.array(range(len(self.data)))
            y = np.log(np.array(self.data[column]))  # apply natural logarithm to y
            p = np.polyfit(x, y, 1)  # fit an exponential function to the data
            self.predictions[column] = np.exp(np.polyval(p, x))  # calculate the predictions

@app.route('/')
def index():
    stock = StockData('TSLA')
    stock.fetch_data()
    # stock.calculate_regression()
    stock.regression()

    fig = go.Figure(data=[go.Candlestick(x=stock.data.index,
        open=stock.data['Open'],
        high=stock.data['High'],
        low=stock.data['Low'],
        close=stock.data['Close'])])

    fig.add_trace(go.Candlestick(x=stock.data.index,
        open=stock.predictions['Open'].flatten(),
        high=stock.predictions['High'].flatten(),
        low=stock.predictions['Low'].flatten(),
        close=stock.predictions['Close'].flatten(),
        name='Predictions'))

    fig.update_yaxes(fixedrange=False)

    # for column, predictions in stock.predictions.items():
    #     fig.add_trace(go.Scatter(x=stock.data.index, y=predictions, mode='lines', name=f'{column} Regression'))

    # for column, predictions in stock.predictions.items():
    #     fig.add_trace(go.Scatter(x=stock.data.index, y=predictions.flatten(), mode='lines', name=f'{column} Regression'))

    fig_html = fig.to_html(full_html=True)

    return render_template('index.html', plot=fig_html)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)