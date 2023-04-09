import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);

export default new Vuex.Store({
    state:{
        oficina:'',
        apellidos:'',
        id:0,
    },
    getters:{
        mostrarApellido (state){
            return state.apellidos;
        },

        mostrarOficina(state){
            return state.oficina;
        },
        mostrarID(state){
            return state.id
        }   
        
        
    }
  
})