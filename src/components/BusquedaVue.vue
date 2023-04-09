<template>
  <v-card id="v-step-1" fluid class="ma-5">
    <v-card-title>
      Resoluciones
      <v-spacer></v-spacer>
      <v-text-field
      
        v-model="search"
        append-icon="mdi-magnify"
        label="Buscar resoluciones"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      class="v-step-0 cyan darken-1 white--text"
      :headers="headers"
      :items-per-page="5"
      :items="items"
      :search="search"
      show-select
    >
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small class="mr-2" @click="downloadItem(item)">
          mdi-download
          
        </v-icon>
       
      </template>
    </v-data-table>
   
  </v-card>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      search: "",
      headers: [
        {
          text: "N° ID",
          align: "start",
          sortable: false,
          value: "id",
        },
        { text: "N° Proyecto", value: "nproyecto" },
        { text: "Concepto", value: "concepto" },
        { text: "Descripción", value: "descripcion" },
        { text: "Monto(S/.)", value: "monto" },
        { text: "Distrito", value: "distrito" },
        { text: "F.Emision", value: "Femision" },
        { text: "F.Notificacion", value: "Fnotificacion" },
        { text: "Subido por:", value:"apellidos"},
        { text: "Oficina de:", value:"nombre"},
        { text: "Actions",value:"actions",sortable:false}
      ],
      items: [],
      postURL: "http://127.0.0.1:5000",
      config_request: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    };
  },

  methods: {
    async downloadItem(item){
      console.log("item :", item.id);
     axios
      .get("http://127.0.0.1:5000/download_file/"+item.id.toString(),{
        responseType:"blob",
      })
      .then((res)=>{
          let blob = new Blob([res.data],{type:'application/pdf'});
          let link = document.createElement("a");
          link.href = window.URL.createObjectURL(blob);
          console.log(res.data);
          link.download = item.nproyecto+item.concepto;
          link.click();

      })
      .catch((error)=>{
        console.log(error);
      })
  
    },
  },

  
  async created() {
    axios
      .get("http://127.0.0.1:5000/resolucion/", this.config_request)
      .then((res) => {
        
        this.items = res.data;
        console.log("busquedas",res.data)
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>
