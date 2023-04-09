<template>
  
  <v-data-table
    :headers="headers"
    :items="items"
    :items-per-page="5"
    sort-by="calories"
    class="elevation-1 ma-6 grey darken-2 white--text"
    width="2000px"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title>Mi Resolución</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="grey darken-3"
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              Nueva resolución
            </v-btn>
          </template>
          <v-card class="blank" height="500">
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      
                      v-model="editedItem.nproyecto"
                      label="N° Proyecto"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      
                      v-model="editedItem.concepto"
                      label="Concepto"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                    
                      v-model="editedItem.descripcion"
                      label="Descripcion"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                    
                      v-model="editedItem.monto"
                      label="Monto (S/.)"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                    
                      v-model="editedItem.distrito"
                      label="Distrito"
                      
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                    
                      v-model="editedItem.Femision"
                      placeholder="DD/MM/AAAA"
                      label="Fecha emision"
                    
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                    
                      v-model="editedItem.Fnotificacion"
                      label="Fecha notificacion"
                      placeholder="DD/MM/AAAA"
                      
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <form
                      enctype="multipart/form-data"
                      @submit.prevent="submit"
                    >
                      <v-file-input
                        v-model="file"
                        
                        accept="application/pdf"
                        label="PDF"
                        prepend-icon="mdi-file"
                        
                      ></v-file-input>
                    </form>
                  </v-col>

                  <!-- PERSONA  -->
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
              <v-btn color="blue darken-1" type="submit" text @click="save">
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5"
              >Are you sure you want to delete this item?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete"
                >Cancel</v-btn
              >
              <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                >OK</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
      <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize"> Reset </v-btn>
    </template>
  </v-data-table>



</template>
<script>
import axios from "axios";
import LoginVue from "../components/LoginVue.vue";
export default {
  
  

  data: () => ({
    valid:true,
    recibido_index:0,
    dialog: false,
    dialogDelete: false,
    /*Cabecera de la tabla*/
    id_timer: null,
    items: [],
    Campos:[
      campo => !!campo || "Campo Obligatorio"
    ],
    file: null,
    id_new:0,
    headers: [
      { text: "N° ID",align: "start",value: "id"},
      { text: "N° Proyecto", value: "nproyecto" },
      { text: "Concepto", value: "concepto" },
      { text: "Admin. que Gestiona", value: "apellidos" },
      { text: "Oficina del Admin.",value:"nombre"},
      { text: "Monto", value: "monto" },
      { text: "Distrito", value: "distrito", sortable: false },
      { text: "F.Emision", value: "Femision" },
      { text: "F.Notificacion", value: "Fnotificacion" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    config_request: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    config_header: {
      "Content-Type": "multipart/form-data",
    },
    editedIndex: -1,
    editedItem: {
      nproyecto: "",
      usuario_id:0,
      concepto: "",
      descripcion: "",
      monto: 0.0,
      distrito: "",
      Femision: "",
      Fnotificacion: "",
    },
    defaultItem: {
      nproyecto: "",
      usuario_id:0,
      concepto: "",
      descripcion: "",
      monto: 0.0,
      distrito: "",
      Femision: "",
      Fnotificacion: "",
    },
  }),
  computed: {
   
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
    PrimeroValidar(){
      let emptyFile = [null].find(prop => !this[prop]);
      return emptyFile;
    }
    
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    
    this.initialize();
  
    
  },

  methods: {
    async initialize(){
      
      const objetos = await axios.get(
        "http://127.0.0.1:5000/resolucion/",
        this.config_request
      )
      this.items = await objetos.data;
      console.log("items",this.items)
      console.log(objetos.data)

      /*QUE LE PASA EL ADMIN QUE GESTIONA */

    },
    async editar() {
      console.log("editando...");

      const filedata = new FormData();
      filedata.append("file", this.file);

      const objeto = {
        nproyecto: "hoo",
        concepto: "hoo",
        descripcion: "",
        monto: 0.0,
        distrito: "",
        Femision: "",
        Fnotificacion: "hooh",
      };
      const id = "2";
      const editado = await axios.put(
        "http://127.0.0.1:5000/update/resolucion/" + id,
        objeto,
        this.config_request
      );

      const archivosubido = await axios.post(
        "http://127.0.0.1:5000/upload_file/" + id,
        filedata,
        this.config_header
      );

      console.log(editado);
      console.log("archivo", archivosubido.data);
    },
    editItem(item) {
      console.log("DENTRO EDIT ITEM")
      console.log(item.id," ----item.id....")
      this.editedIndex = item.id;
      console.log(this.editedIndex)
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.editedIndex=this.items.indexOf(item);
      console.log("terminando edit item")
      console.log(this.editedIndex)
      this.id_new = item.id
    },

    deleteItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
      
    },

    async deleteItemConfirm() {
      this.items.splice(this.editedIndex, 1);

      const eliminado = await axios.delete(
        "http://127.0.0.1:5000/delete/resolucion/"+this.editedItem.id
      )
      const { data } = eliminado;
      console.log(data)
      
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    async save() {
      const recibido_id = this.$store.getters.mostrarID;
      console.log("RECIBIDO _ID ",recibido_id)

      // PRIMERO : CUANDO YA EXISTE UN REGISTRO
      if (this.editedIndex > -1) {
        console.log("INDEX :",this.editedIndex)
        console.log("id_new",this.id_new)

      

        const formData = new FormData();
        formData.append("file",this.file)

        this.editedItem.usuario_id = recibido_id
        console.log("....actualizado",this.editedItem.usuario_id)

        const guardarobjeto = Object.assign(this.items[this.editedIndex], this.editedItem);
        
        const registroU = await axios.put(
          "http://127.0.0.1:5000/update/resolucion/"+this.id_new,
          guardarobjeto,
          this.config_request
        )
        console.log("actualizado:",registroU.data)
        console.log("------------------------")

        const documento = await axios.post(
          "http://127.0.0.1:5000/upload_file/"+this.id_new,
          formData,
          this.config_header
        )
        console.log(documento.data)

      } 
      // SEGUNDO : CUANDO CREAMOS UN REGISTRO
      else {
        console.log(" CREANDO ")
        console.log(this.editedIndex)
        const formPost = new FormData();
        formPost.append("file",this.file)

        this.editedItem.usuario_id = recibido_id
        console.log("...edit.usuari",this.editedItem.usuario_id)

        const postear = await axios.post(
          "http://127.0.0.1:5000/create/resolucion",
          this.editedItem,
          this.config_request
        )

        const {data} = postear

        const nuevoDocumento = await axios.post(
          "http://127.0.0.1:5000/upload_file/"+data.id,
          formPost,
          this.config_header
        )

      }
      this.close();
    },
  },
};
</script>
