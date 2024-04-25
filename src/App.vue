 <!-- App.vue -->
 <template>
  <div id="app">
    <router-view></router-view> <!-- This renders the current route's component -->
  </div>
</template>

<script>
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyAel8It8cUySYD286fxw145yDP1nG9ryhE",
  authDomain: "test-330c7.firebaseapp.com",
  databaseURL: "https://test-330c7-default-rtdb.firebaseio.com",
  projectId: "test-330c7",
  storageBucket: "test-330c7.appspot.com",
  messagingSenderId: "925391627196",
  appId: "1:925391627196:web:d4d6e0282f5258dec541b9",
  measurementId: "G-G5SL6T2YKX"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// eslint-disable-next-line
const analytics = getAnalytics(app);

export default {
  name: 'App'
  // No need to declare components for router-view
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /*margin-top: 60px;*/
}
</style>
