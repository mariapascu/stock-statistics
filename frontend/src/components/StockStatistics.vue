<template>
  <div>
    <table class="table table-bordered table-striped">
      <thead>
      <tr>
        <th v-for="(key) in Object.keys(fields)" :key='key'>
          {{ fields[key] }} <i class="bi bi-sort-alpha-down" aria-label='Sort Icon'></i>
        </th>
      </tr>
      </thead>
      <tbody>
        <tr v-for="row in stockStatistics" :key='row'>
          <td v-for="(key) in Object.keys(fields)" :key='key'>{{ row[key] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import "bootstrap/dist/css/bootstrap.min.css";
import {getStockStats} from "@/service/stocks";
import getTimestamp from "@/service/utils";

const STOCK_SYMBOLS = ["AAPL", "MSFT", "TSLA"];

export default {
  name: "StockStatistics",
  data() {
    return {
      fields: {stock: "Stock", cumulativeReturn: "Annual Cumulative Return", volatility: "Annual volatility"},
      stockStatistics: [],
      startDate: new Date(),
      endDate: new Date(),
    }
  },
  methods: {
    async getStockStatistics() {
      const startTimestamp = getTimestamp(this.startDate);
      const endTimestamp = getTimestamp(this.endDate);
      for (const symbol of STOCK_SYMBOLS) {
        let stockStats = await getStockStats(symbol, startTimestamp, endTimestamp)
        stockStats = stockStats.data;
        stockStats["stock"] = symbol;
        stockStats["cumulativeReturn"] = (stockStats["cumulativeReturn"] * 100).toFixed(2) + "%"
        stockStats["volatility"] = stockStats["volatility"].toFixed(2)
        this.stockStatistics.push(stockStats);
      }
    }
  },
  created() {
    this.startDate.setFullYear(this.startDate.getFullYear() - 1);
    this.getStockStatistics();
  }
}
</script>

<style scoped>
.table {
  margin-top: 20px;
  margin-left: 7%;
  width: 1000px;
}
</style>