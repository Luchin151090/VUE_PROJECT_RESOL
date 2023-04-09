<template>
  <v-app>
    <v-main class="fondito">
      <v-alert
        class="ma-auto mt-2 justify-top"
        width="800"
        type="info"
        v-model="alert"
      >
        Espere la CONFIRMACIÓN de su petición a Informática.
        Se enviará una respuesta a su correo</v-alert
      >
      <v-card
        class="ma-auto mt-6 pt-3 pl-6 pr-6"
        height="670"
        width="500"
      >
        <v-card-title class="justify-center mt-0" 
          >Registro de Informática - BuResol v1.0</v-card-title
        >
        <form ref="form" @submit.prevent="send">
          <label>Nombres</label>
          <input type="text" placeholder="Nombre Apellidos" name="user_name" />
          <label>Cargo</label>
          <input type="text" placeholder="Ingrese su cargo" name="user_cargo" />
          <label>Oficina</label>
          <input
            type="text"
            placeholder="Oficina donde labora"
            name="user_oficina"
          />
          <label>Email</label>
          <input
            type="email"
            placeholder="Ingrese su email"
            name="user_email"
          />
          <label>Motivo</label>
          <textarea name="message" placeholder="En breve su motivo"></textarea>
          <input type="submit" value="Enviar" />
        </form>
  
      </v-card>
    </v-main>
  </v-app>
</template>

<script>
import emailjs from "emailjs-com";

export default {
  data: () => ({
    alert: false,
  }),
  methods: {
    send() {
      emailjs
        .sendForm(
          "service_dy6tddv",
          "template_f8i8are",
          this.$refs.form,
          "wRJZARKxNfDIQpcrT"
        )
        .then(
          (result) => {
            console.log("SUCCESS!", result.text);
            if (result.status === 200) {
              this.alert = true;
              setTimeout(() => {
                this.mostrar();
              }, 5500);
            }
          },
          (error) => {
            console.log("FAILED...", error.text);
          }
        );
    },
    mostrar(){
        this.alert=false;
        this.$refs.form.reset();
    }
  },
};
</script>
<style scoped>
.alerta {
  width: 700px;
  top: 10px;
  margin-left: 300px;
}
label {
  float: left;
  color: black;
}

input[type="text"],
[type="email"],
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid purple;
  border-radius: 6px;
  box-sizing: border-box;
  margin-top: 6px;
  margin-bottom: 16px;
  resize: vertical;
  color: purple;
}

input[type="submit"] {
  background-color: #4caf50;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  width: 150px;
  margin: center;
}
.fondito {
  width: 100%;
  background: url("https://media.istockphoto.com/vectors/books-sketch-seamless-vector-id594484448?k=20&m=594484448&s=612x612&w=0&h=6lvNgspQuiOQUidxaH7LPfiE7RcicUgwReKe-WEhSNc=");
}
</style>
