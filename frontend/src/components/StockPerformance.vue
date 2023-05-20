<template>
  <div id="stock-performance">
    <div class="graph" ref="stockPerformance"></div>
  </div>
</template>

<script>
import {getStocks} from "@/service/stocks";
import getTimestamp from "@/service/utils";
import * as d3 from 'd3';

const COLORS = ["blue", "green", "red"];
const STOCK_SYMBOLS = ["AAPL", "MSFT", "TSLA"];
const STOCK_INDICATOR = "high";

export default {
  name: 'StockPerformance',
  data() {
    return {
      stocksPerformance: [],
      startDate: new Date(),
      endDate: new Date(),
    };
  },
  methods: {
    async getStockPerformance() {
      const startTimestamp = getTimestamp(this.startDate);
      const endTimestamp = getTimestamp(this.endDate);
      for (const symbol of STOCK_SYMBOLS) {
        const stockPerf = await getStocks(symbol, startTimestamp, endTimestamp);
        this.stocksPerformance.push(stockPerf.data);
      }
      this.setGraph()
    },
    setGraph() {
      const width = 1260, height = 400, margin = 35;
      const gWidth = 1000;
      const svg = d3.select(".graph").append("svg")
          .attr("width", width)
          .attr("height", height);
      const g = svg.append("g");
      this.stocksPerformance.forEach(stockPerf => stockPerf.forEach(d => d['date'] = this.formatDate(d['timestamp'])));

      // X Axis
      const startFormatDate = this.formatDate(this.startDate)
      const endFormatDate = this.formatDate(this.endDate)

      const x = d3.scaleTime()
          .domain([d3.timeParse("%Y-%m-%d")(startFormatDate), d3.timeParse("%Y-%m-%d")(endFormatDate)])
          .range([margin + 2.5, gWidth - margin])

      g.append("g")
          .attr("transform", "translate(0," + (height - margin) + ")")
          .call(d3.axisBottom(x));

      // Y Axis
      const stocksMinAndMax = [100]
      this.stocksPerformance.forEach(stockPerf => {
        stocksMinAndMax.push(d3.min(stockPerf, d => {
          return d[STOCK_INDICATOR]
        }));
        stocksMinAndMax.push(d3.max(stockPerf, d => {
          return d[STOCK_INDICATOR]
        }));
      });

      const y = d3.scaleLinear()
          .domain(d3.extent(stocksMinAndMax))
          .range([height - margin, margin]);

      g.append("g")
          .attr("transform", "translate(" + margin + ", 0)")
          .call(d3.axisLeft(y));

      this.stocksPerformance.forEach(stockPerf =>
          stockPerf.forEach(d =>
              d['date'] = this.formatDate(this.getDateFromTimestamp(d['timestamp']))));


      this.stocksPerformance.forEach((stockPerf, i) => g.append("path")
          .data([stockPerf])
          .attr("d", d3.line()
              .x(d => {
                return x(d3.timeParse("%Y-%m-%d")(d['date']))
              })
              .y(d => {
                return y(d[STOCK_INDICATOR])
              }))
          .attr("fill", "none")
          .attr("stroke", COLORS[i])
          .attr("stroke-width", 1.5));

      const legend = g.append("g").attr("transform", "translate(" + gWidth + ", 0 )");
      legend.selectAll(".legendBox")
          .data(this.stocksPerformance)
          .enter()
          .append("circle")
          .attr("cx", 100)
          .attr("cy", (d, i) => 100 + i*25)
          .attr("r", 7)
          .style("fill", (d, i) => COLORS[i]);
      legend.selectAll("mylabels")
          .data(this.stocksPerformance)
          .enter()
          .append("text")
          .attr("x", 120)
          .attr("y", function(d,i){ return 100 + i*25}) // 100 is where the first dot appears. 25 is the distance between dots
          .style("fill", (d, i) => COLORS[i])
          .text((d, i) => STOCK_SYMBOLS[i])
          .attr("text-anchor", "left")
          .style("alignment-baseline", "middle")
    },
    getDateFromTimestamp(timestamp) {
      return new Date(timestamp * 1000);
    },
    formatDate(date) {
      // Get year, month, and day part from the date
      const year = date.toLocaleString("default", {year: "numeric"});
      const month = date.toLocaleString("default", {month: "2-digit"});
      const day = date.toLocaleString("default", {day: "2-digit"});

      // Generate yyyy-mm-dd date string
      return year + "-" + month + "-" + day;
    },
  },
  created() {
    this.startDate.setFullYear(this.startDate.getFullYear() - 1);
    this.getStockPerformance();
  },
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
