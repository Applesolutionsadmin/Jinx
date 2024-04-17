from flask import Flask, request, render_template, redirect, url_for
import yfinance as yf
import tensorflow as tf
import pandas as pd
import numpy as np
import datetime as dt
# app.py
import os

# Run the jinxServer command
os.system('jinxServer')

app = Flask(__name__)

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker

    def fetch_data(self):
        data = yf.download(self.ticker, start='2024-01-01', end=dt.datetime.now().strftime('%Y-%m-%d'))
        self.data = pd.DataFrame(data['Close'])
        self.reset_index(inplace=True)

    def calculate_regression(self):
        x = np.array(range(len(self.data)))
        y = np.array(self.data['Close'])
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(1, activation=tf.exp, input_shape=[1]))
        model.compile(optimizer=tf.optimizers.Adam(0.01), loss='mean_squared_error')
        model.fit(x, y, epochs=100)
        self.predictions = model.predict(x)

# Global variable to store the data
data = []

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    global data
    payload = request.get_json()
    data.append(payload)
    return '', 200

@app.route('/')
def home():
    global data
    # Render the data in the home.html template reverse order
    return render_template('index.html', data=data[::-1])

@app.route('/clear', methods=['GET', 'POST'])
def clear():
    global data
    # Clear the global variable
    data = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8000)