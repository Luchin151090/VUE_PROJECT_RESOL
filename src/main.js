import Vue, { onMounted } from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import VueApexCharts from 'vue-apexcharts'
import VueTour from 'vue-tour'
import store from '../src/store.js'

require('vue-tour/dist/vue-tour.css')



Vue.config.productionTip = false;

import VueRouter from "vue-router";
Vue.use(VueRouter);
Vue.use(VueApexCharts);
Vue.use(VueTour)


Vue.component('apexchart', VueApexCharts)

import LoginVue from "./components/LoginVue.vue";
import BusquedaVue from "./components/BusquedaVue.vue";
import DashboardVue from "./components/DashboardVue.vue";

import Dash2Vue from "./components/Dash2Vue.vue";

import RegistroUser from "./components/RegistroUser.vue";
import ForgotPass from "./components/ForgotPass.vue";
import EditUser from "./components/EditUser.vue";
import ReVue from './components/ReVue.vue';


const router = new VueRouter({
  mode: "history",
  base: __dirname,
  routes: [
    {
      path: "/admin",
      name: "admin",
      component: Dash2Vue,
      children: 
      [
        {
          path: "/admin/busquedas",
          name: "adbus",
          component: BusquedaVue,
        },
        {
          path: "/admin/administrar",
          name: "ada",
          component: ReVue,
        },
        {
          path:"/admin/edit_user",
          name:"adedit_user",
          component: EditUser,
        }
      ],
    },
    {
      path: "/home",
      name: "home",
      component: DashboardVue,
      children: [
        {
          path: "/busquedas",
          name: "busquedas",
          component: BusquedaVue,
        },

      ],
    },
    
    {
      path: "/",
      name: "logins",
      component: LoginVue,
    },
    {
      path:"/registro_user",
      name:"registro_user",
      component: RegistroUser
    },
    {
      path:"/forgot_pass",
      name:"forgot_pass",
      component: ForgotPass
    }
  ],
});



new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
