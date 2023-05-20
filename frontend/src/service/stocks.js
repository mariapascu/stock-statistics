import axios from 'axios';

const PATH = "http://127.0.0.1:5000/";

function getStocks(stockSymbol, startTimestamp, endTimestamp) {
    return axios.get(PATH + "stock-performance",
        {
            params: {
                symbol: stockSymbol,
                startTimestamp: startTimestamp,
                endTimestamp: endTimestamp
            }
        });
}

function getStockStats(stockSymbol, startTimestamp, endTimestamp) {
    return axios.get(PATH + "stock-statistics",
        {
            params: {
                symbol: stockSymbol,
                startTimestamp: startTimestamp,
                endTimestamp: endTimestamp
            }
        });
}

export {getStocks, getStockStats};