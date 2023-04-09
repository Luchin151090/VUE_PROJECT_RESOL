<template>
  <v-container>
    <div>
      <v-row>
        <v-col cols="12">
          <v-card id="v-step-0" class="grey darken-3">
            <v-card-title class="white--text justify-center"
              >Informe BuResol v1.0</v-card-title
            >
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card id="v-step-0" max-height="220">
            <v-card-title class="green--text">Último Registro</v-card-title>
            <v-row>
              <v-col cols="3">
                <v-icon class="ma-2 ml-10" size="85" color="green darken-2">
                  mdi-file-multiple
                </v-icon>
              </v-col>

              <v-col cols="9">
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title class="text-h6">
                      N° Proyecto :{{registro[0].nproyecto}}</v-list-item-title
                    >
                    <v-list-item-title class="text-h6">Concepto : {{registro[0].concepto}}</v-list-item-title>

                    <v-list-item-title class="text-h6">Descripción : {{registro[0].descripcion}}</v-list-item-title>
                    <v-list-item-title class="text-h6">Monto : S/.{{registro[0].monto}}</v-list-item-title>
                    <v-list-item-title class="text-h6">Distrito : {{registro[0].distrito}}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-col>
            </v-row>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card max-height="200">
            <v-card-title class="purple--text"
              >Total de Documentos</v-card-title
            >
            <v-row>
              <v-col cols="3">
                <v-progress-circular
                  class="ma-2 ml-10"
                  :rotate="360"
                  :size="100"
                  :width="10"
                  :value="documentos"
                  color="purple"
                >
                  {{ documentos }}
                </v-progress-circular>
              </v-col>
              <v-col cols="9">
                <v-card-text class="text-h5">Documentos en BuResol</v-card-text>
              </v-col>
            </v-row>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card>
            <v-card-title class="blue--text" max-height="100"
              >Monto en Proyectos</v-card-title
            >
            <v-row>
              <v-col cols="3">
                <v-icon class="ma-2 ml-10" size="85" color="blue">
                  mdi-currency-usd
                </v-icon>
              </v-col>

              <v-col cols="9">
                <v-card-text class="text-h2">S/. {{monto}}</v-card-text>
              </v-col>
            </v-row>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card>
            <v-card-title class="pink--text">
              Resoluciones-Distrito
            </v-card-title>
            <v-row>
              <v-col cols="12">
                <BarraVue />
              </v-col>

              <!--v-col cols="2">
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>
                      N° Proyecto : item asdf asdfas asdf</v-list-item-title
                    >
                    <v-list-item-title>Concepto : item</v-list-item-title>

                    <v-list-item-title>Descripción : item</v-list-item-title>
                    <v-list-item-title>Monto : S/. item</v-list-item-title>
                    <v-list-item-title>Distrito : item</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-col-->
            </v-row>
          </v-card>
        </v-col>

        <v-col cols="12">
          <v-card>
            <v-card-title class="grey darken-3 white--text">Últimas 5 Resoluciones</v-card-title>
          <v-data-table
            :headers="headers"
            :items="items2"
            :items-per-page="10"
            class="elevation-1"
          ></v-data-table>
        </v-card>
        </v-col>

        
        <v-col cols="12" >
          <v-card max-height="80">
            <v-row>
              <v-col cols="6">
                <v-card-title>Pulsa en el botón para obtener el Informe General</v-card-title>
       
              </v-col>

              <v-col cols="6" class="mt-4">
                <v-btn class="white--text" color="pink accent-2" @click="exportpdf">
                  <v-icon dark>mdi-download</v-icon>Descargar Informe General</v-btn>
              </v-col>

            </v-row>
  
          </v-card>

        </v-col>
      

      </v-row>


    </div>
    <!--v-tour name="myTour" :steps="steps"--><!--/v-tour-->
  </v-container>
</template>
<script>
import axios from "axios";
import BarraVue from "./BarraVue.vue";
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
pdfMake.vfs = pdfFonts.pdfMake.vfs;

export default {
  data:()=>({
    config_request: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },

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
        { text: "Monto", value: "monto" },
        { text: "Distrito", value: "distrito" },
        { text: "F.Emision", value: "Femision" },
        { text: "F.Notificación", value: "Fnotificacion" },
    
      ],
      items2: [],
      monto:0.0,
      documentos: 0,
      registro:[],
      cantidades:0,
      distritos:[],
      labels:[],
 
      items: [
        {
          src: "https://media.istockphoto.com/vectors/books-sketch-seamless-vector-id594484448?k=20&m=594484448&s=612x612&w=0&h=6lvNgspQuiOQUidxaH7LPfiE7RcicUgwReKe-WEhSNc=",
        },
        {
          src: "https://i.pinimg.com/736x/ea/f4/03/eaf4039b8860a73d2095d769411e12ae.jpg",
        },
      ],
      
    
  }),
  components: { BarraVue },
 
  methods:{
    async last(){
     try{
      const res = await axios.get("http://127.0.0.1:5000/resolucion/last_register", this.config_request)
      this.registro=res.data;
      console.log("datossss",this.registro);
      console.log(this.registro[0].nproyecto);
     }
     catch(error){
      console.log(error);
     }
    },
    async montos()
    {
      axios
      .get("http://127.0.0.1:5000/resolucion/monto", this.config_request)
      .then((res)=>{
        this.monto=res.data[0].total;

        console.log("MONTO",this.monto);
      })
      .catch((error)=>{
        console.log(error);
      })
    },
    async exportpdf(){
      var pdfdoc = {
        content:[
          {text:"Informe BuResol v1.1",fontSize:20},
          "\n",
          "La información de esta ventana es solo informativa",
          {text:"Cantidad de Resoluciones: "+this.documentos,fontSize:10},
          "\n",
          {text:"Monto en Soles de los proyectos: "+this.monto,fontSize:10},
          "\n",
          {text:"Distritos: "+this.labels,fontSize:10},
          "\n",
          {text:"Documentos por distrito: "+this.distritos,fontSize:10},
          "\n",
          {text:"Última 5 resoluciones: "+this.items2[0].distrito,fontSize:10},
        {text:this.items2[1].distrito,fontSize:10}



        ]
      };
      const pdf = pdfMake.createPdf(pdfdoc).open(); /*download();*/

    }
  },

  async created() {
    this.last();
    this.montos();
    /*cantidad resoluciones*/
    axios
      .get("http://127.0.0.1:5000/resolucion/cantidad")
      .then((res) => {
        this.documentos = res.data;
      })
      .catch((error) => {
        console.log(error);
      });
    console.log("documentos", this.documentos);
    /*la ultima resolucion*/
    axios
      .get("http://127.0.0.1:5000/resolucion/top", this.config_request)
      .then((res) => {
        this.items2 = res.data;
        console.log("5 datos:",this.items2)
      })
      .catch((error) => {
        console.log(error);
      });

    /*agrupacion de distritos*/
    axios
      .get("http://127.0.0.1:5000/resolucion/distritos", this.config_request)
      .then((res) => {
        this.cantidades= res.data.length;

        for(let i=0;i<this.cantidades;i++){
          this.labels.push(res.data[i].distrito);
          this.distritos.push(res.data[i].cantidad);
        }
        

        

        
      })
      .catch((error) => {
        console.log(error);
      }); 
  },

};
</script>

<style></style>
