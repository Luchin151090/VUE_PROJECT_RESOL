<template>
  
  <v-data-table
    :headers="headers"
    :items="items"
    :items-per-page="5"
    sort-by="calories"
    class="elevation-1 ma-6 green darken-2 white--text"
    width="2000px"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-toolbar-title> Usuarios BuResol </v-toolbar-title>
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
              Nuevo Usuario
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
                      
                      v-model="editedItem.nombres"
                      label="Nombres"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      
                      v-model="editedItem.apellidos"
                      label="Apellidos"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      placeholder=" e.g. Luchin15 "
                      v-model="editedItem.nickname"
                      label="Usuario"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      
                      v-model="editedItem.contrasena"
                      label="Contrasena"
                      
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                    
                      v-model="editedItem.email_user"
                      label="Email"
                      
                    ></v-text-field>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <v-select
                      :items="roles_usuario"
                      :item-value="'id'"
                      :item-text="'nombre'"
                      v-model="rol.rol_id"
                      label="Rol de Usuario"
                      dense
                    ></v-select>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <v-select
                      :items="oficinas"
                      :item-value="'id'"
                      :item-text="'nombre'"
                      v-model="editedItem.oficina_id"
                      label="Oficina"
                      dense
                    ></v-select>
                  </v-col>


                  <!-- PERSONA  -->
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close"> Cancel </v-btn>
              <v-btn color="blue darken-1" type="submit" text @click="save">
                Guardar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5"
              >Eliminar Usuario?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete"
                >Cancelar</v-btn
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
    oficinas:[{id:1,nombre:"ADMINISTRACIÓN"},{id:2,nombre:"PERSONAL"},{id:3,nombre:"ASESORÍA JURÍDICA"},{id:4,nombre:"PROCESOS"}],
    roles_usuario:[{id:1,nombre:"admin"},{id:2,nombre:"usuario"}],
    rol:{
      rol_id:0
    },
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
      { text: "ID",align: "start",value: "id"},
      { text: "Nombres", value: "nombres" },
      { text: "Apellidos", value: "apellidos" },
      { text: "Usuario", value: "nickname" },
      { text: "Contraseña",value:"contrasena"},
      { text: "Email", value: "email" },
      { text: "Oficina", value: "oficina", sortable: false },
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
      nombres: "",
      apellidos:"",
      nickname: "",
      contrasena: "",
      email_user:"",
      oficina_id:0
    },
    defaultItem: {
      nombres: "",
      apellidos:"",
      nickname: "",
      contrasena: "",
      email_user: "",
      oficina_id:0
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
        "http://127.0.0.1:5000/user",
        this.config_request
      )
      this.items = await objetos.data;
      console.log("items",this.items)
      console.log(objetos.data)

      /*QUE LE PASA EL ADMIN QUE GESTIONA */

    },
    
    editItem(item) {
    
      this.editedIndex = item.id;
      console.log(this.editedIndex)
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.editedIndex=this.items.indexOf(item);
   
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
        "http://127.0.0.1:5000/delete/user/"+this.editedItem.id
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
      
      //v-select coloca el valor en el objeto...pero tiene que estar relacionado a v-model
       console.log("OFICINA:",this.editedItem.oficina_id)
       console.log("ROL_VALUE:",this.rol.rol_id)

        const postear = await axios.post(
          "http://127.0.0.1:5000/create/user",
          this.editedItem,
          this.config_request
        )

        const rol = await axios.post(
          "http://127.0.0.1:5000/assign/rol_user",
          this.rol,
          this.config_request
        )
        
        console.log("DATA ROL:",rol)
      
      this.close();
    },
  },
};
</script>
