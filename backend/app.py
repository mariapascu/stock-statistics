from flask import Flask, request
from flask_cors import CORS
from stocks import StocksAPI
import json

app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/stock-performance')
def get_stock_performance():
    stock_symbol = request.args.get("symbol")
    start_timestamp = request.args.get("startTimestamp")
    end_timestamp = request.args.get("endTimestamp")
    s = StocksAPI()
    return json.dumps(s.get_stock_data(stock_symbol, start_timestamp, end_timestamp), default=vars)


@app.route('/stock-statistics')
def get_stock_cumulative_return():
    stock_symbol = request.args.get("symbol")
    start_timestamp = request.args.get("startTimestamp")
    end_timestamp = request.args.get("endTimestamp")
    s = StocksAPI()
    return json.dumps(
        {"cumulativeReturn": s.get_stock_cumulative_return(stock_symbol, start_timestamp, end_timestamp),
         "volatility": s.get_volatility(stock_symbol, start_timestamp, end_timestamp)},
        default=vars)


if __name__ == '__main__':
    app.run()
