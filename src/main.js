// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createVuetify } from 'vuetify';
import 'vuetify/dist/vuetify.min.css'; // Make sure to import the minified CSS

const app = createApp(App);

const vuetify = createVuetify(); // no need for options here unless you have them

app.use(router);
app.use(vuetify);
app.mount('#app');
