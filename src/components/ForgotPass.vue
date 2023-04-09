<template>
  <v-app>
    <v-main class="fondo4">
      <v-card class="ma-auto mt-10 pa-10" height="300" width="600">
        <v-card-title>BuResol-v1.0 Solicite nueva contraseña</v-card-title>
        <v-card-subtitle
          >La respuesta será enviada, previa verificación</v-card-subtitle
        >
        <form ref="form" @submit.prevent="send">
          <label>Email</label>
          <input
            type="email"
            placeholder="Ingrese su email"
            name="user_email"
          />

          <input type="submit" value="Enviar" />
        </form>
      </v-card>
      <v-alert class="ma-auto mt-5" width="600" type="info" v-model="alert">Enviaremos una nueva contraseña a su correo</v-alert>
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
          "template_1txfrki",
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
    mostrar() {
      this.alert = false;
      this.$refs.form.reset();
    },
  },
};
</script>

<style scoped>
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
.fondo4 {
  background: url("https://media.istockphoto.com/vectors/books-sketch-seamless-vector-id594484448?k=20&m=594484448&s=612x612&w=0&h=6lvNgspQuiOQUidxaH7LPfiE7RcicUgwReKe-WEhSNc=");
}
</style>
