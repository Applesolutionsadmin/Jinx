from flask import Flask, render_template
import yfinance as yf
import tensorflow as tf
import pandas as pd
import numpy as np
import datetime as dt

app = Flask(__name__)

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_data(self):
        data = yf.download(self.ticker, start='2020-01-01', end=dt.datetime.now().strftime('%Y-%m-%d'))
        self.data = pd.DataFrame(data['Close'])

    def calculate_regression(self):
        x = np.array(range(len(self.data)))
        y = np.array(self.data['Close'])
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(1, activation=tf.exp, input_shape=[1]))
        model.compile(optimizer=tf.optimizers.Adam(0.01), loss='mean_squared_error')
        model.fit(x, y, epochs=100)
        self.predictions = model.predict(x)

@app.route('/')
def index():
    stock = StockData('TSLA')
    stock.fetch_data()
    stock.calculate_regression()
    return render_template('index.html', data=stock.predictions)

if __name__ == '__main__':
    app.run(debug=True)