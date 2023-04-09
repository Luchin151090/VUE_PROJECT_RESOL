<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app width="180" class="grey darken-3">
      <v-list-item>
        <v-list-item-content class="justify-center">
          <v-list-item-title class="white--text text-h6 justify-center">
            Menu
          </v-list-item-title>
          <v-list-item-subtitle class="white--text justify-center">
            Ugel-Arequipa-Norte
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item
          class="v-step-1 pink darken-4"
          v-for="item in items"
          :key="item.title"
          link
          @click="$router.push({ path: item.route })"
        >
          <v-list-item-icon>
            <v-icon color="white">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="white--text">{{
              item.title
            }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <!--  -->
      <template v-slot:append>
        <div class="pa-2">
          <v-btn block @click="salir"> salir </v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-app-bar app class="grey darken-3">
      <v-app-bar-nav-icon
        class="white"
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>

      <v-toolbar-title class="v-step-0 white--text"
        >BuResol v1.0
      </v-toolbar-title>

      <!--span class="subheading white--text">{{}}</span-->

      <v-spacer></v-spacer>
      <span class="subheading white--text">{{ city }}</span>
      <v-divider class="mx-2 white" vertical></v-divider>
      <span class="subheading white--text">{{ temperature }}° C</span>
      <v-divider class="mx-2 white" vertical></v-divider>
      <span class="subheading white--text">{{ date_time }}</span>
    </v-app-bar>

    <div class="v-step-2"></div>
    <!-- MOSTRAR EL HOME SI ES DIFERENTE DE LOS OTROS COMPONENTES -->
    <v-main class="fondo2">
      <HomeVue
        v-if="
          this.$router.currentRoute.name !== 'adcuen' &&
          $router.currentRoute.name !== 'ajustes' &&
          $router.currentRoute.name !== 'adbus' &&
          $router.currentRoute.name !== 'ada' &&
          $router.currentRoute.name !== 'adedit_user'
        "
      />
      <router-view></router-view>
      <!--BusquedaVue/-->
      <!--v-tour name="myTour" :steps="steps"--><!--/v-tour-->
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";
import BusquedaVue from "./BusquedaVue.vue";
import HomeVue from "./HomeVue.vue";

export default {
  data: () => ({
    city: "",
    id_timer: null,
    temperature: 0,
    date_time: "",
    tiempo: 400000,

    items: [
      { title: "Inicio", icon: "mdi-home", route: "/admin" },
      { title: "Editar-Resol.",icon: "mdi-pencil",route: "/admin/administrar"},
      { title: "Busquedas", icon: "mdi-magnify", route: "/admin/busquedas" },
      { title: "Editar-Usuarios",icon:"mdi-account",route:"/admin/edit_user"}
    ],
    drawer: null,
  }),
  components: { BusquedaVue, HomeVue },
  async created() {
    axios
      .get(
        "https://api.openweathermap.org/data/2.5/weather?q=Arequipa&appid=14361693170d23bbffec093892b8f1c7"
      )
      .then((res) => {
        this.city = res.data.name;
        this.temperature = (res.data.main.temp - 273.15).toFixed();
      });
  },
  mounted() {
    /* si muevo */
    window.addEventListener(
      "mousemove",
      this.reset_time
    ); /*este llama al reseteo*/

    /* si no muevo corre el tiempo*/
    this.start();

    this.fecha_hora();

    this.$tours["myTour"].start();
  },
  methods: {
    start() {
      this.id_timer = setTimeout(() => {
        this.inactividad();
      }, this.tiempo);
    },
    inactividad() {
      this.$router.push("/");
    },
    reset_time() {
      clearTimeout(this.id_timer);
      this.start();
    },
    fecha_hora() {
      let hoy = new Date();
      let ahora = hoy.toLocaleDateString();
      this.date_time = ahora;
    },

    salir() {
      this.$router.push("/");
    },
  },
};
</script>

<style>
.fondo2 {
  background: url("https://fondosmil.com/fondo/52683.jpg");
}
</style>
