<template>
  <div>
    <apexchart
      width="500"
      type="donut"
      :options="options"
      :series="distritos"
    ></apexchart>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";
import axios from "axios";

export default {
  data: () => ({
    options: {
      chart: {
        type: "donut",
      },
      labels: [],
    },
    config_request: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    cantidades:0,
    distritos: [],
  }),
  async created() {
    axios
      .get("http://127.0.0.1:5000/resolucion/distritos", this.config_request)
      .then((res) => {
        this.cantidades= res.data.length;

        for(let i=0;i<this.cantidades;i++){
          this.options.labels.push(res.data[i].distrito);
          this.distritos.push(res.data[i].cantidad);
        }
        

        console.log("etiquetas", this.options.labels);

        
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>
