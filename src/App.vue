<template>
  <v-app id="app">
    <DashboardVue v-if="this.$router.currentRoute.name !== 'login'"/>
    <Dash2Vue v-if="this.$router.currentRoute.name !== 'login'"/>
    <router-view/>
  </v-app>
</template>

<script>
import Dash2Vue from './components/Dash2Vue.vue';
import DashboardVue from './components/DashboardVue.vue';
export default {
  name: 'App',

  components: {
    
    
},

  data: () => ({
    //
  }),
};
</script>