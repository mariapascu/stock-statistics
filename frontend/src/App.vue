<template>
  <h1>Stocks' Performance Graph and Statistics</h1>
  <StockPerformance/>
  <StockStatistics/>
</template>

<script>
import StockPerformance from './components/StockPerformance.vue'
import StockStatistics from "@/components/StockStatistics";

export default {
  name: 'App',
  components: {
    StockStatistics,
    StockPerformance
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
