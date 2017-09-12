from flask import Flask, render_template, request, redirect
import flask
import quandl
import pandas as pd
import numpy as np
from datetime import timedelta
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph', methods = ['POST'])
def graph():


    # only proceed to get and plot data is ticker is given
    if request.form.get('ticker'):
      ticker = request.form['ticker']

      # get data from quandl API
      quandl.ApiConfig.api_key = "DotxFs2bJksfE6SfssR4"
      data = quandl.get("WIKI/{}".format(ticker))[['Open', 'Close', 'Adj. Open', 'Adj. Close']]
      # clean the data for plotting
      today = pd.to_datetime('today')
      last_mon = today - timedelta(days=30)
      index1 = (np.where(data.index > last_mon)[0])
      last_mon_data = data[index1[0]:]
      y = pd.to_datetime(last_mon_data.index)


      p = figure(title="Stock Price Plot for Last Month {}".format(ticker), x_axis_label='Date', y_axis_label='Price',
                 x_axis_type="datetime")

      # only plot if a feature is selected
      if request.form.get('feature1'):
        feature1 = request.form['feature1']
        x1 = last_mon_data[feature1]
        p.line(y, x1.values, legend="{}".format(feature1), line_width=2, color="green")

      if request.form.get('feature2'):
        feature2 = request.form['feature2']
        x2 = last_mon_data[feature2]
        p.line(y, x2.values, legend="{}".format(feature2), line_width=2, color="red")

      if request.form.get('feature3'):
        feature3 = request.form['feature3']
        x3 = last_mon_data[feature3]
        p.line(y, x3.values, legend="{}".format(feature3), line_width=2, color="blue")

      if request.form.get('feature4'):
        feature4 = request.form['feature4']
        x4 = last_mon_data[feature4]
        p.line(y, x4.values, legend="{}".format(feature4), line_width=2, color="orange")

      script, div = components(p)

      # if no field is chosen, simply return an error message
      if not request.form.get('feature1') and not request.form.get('feature2') and \
              not request.form.get('feature3') and not request.form.get('feature4'):
        return "Please select at least one value to plot!"
      # otherwise return the plot
      return render_template('graph.html', div=div, script=script)

    # if no ticker is given, simply return a message
    else:
      return "Please specify the ticker (e.g., GOOG)"


if __name__ == '__main__':
  app.run(debug=True)
