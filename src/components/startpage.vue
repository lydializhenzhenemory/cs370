<template>
  <div id="game-container" class="game-container">
    <div id="title" :style="titleStyle">
      <span class="typing-effect">{{ typedTitle }}</span>
    </div>
    <button id="start-button" @click="startGame" :style="startButtonStyle">
      Start Game
    </button>
    <button id="sign-in-button" @click="signIn" :style="signinButtonStyle">
      {{ signInOut }}
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut } from "firebase/auth";

const provider = new GoogleAuthProvider();
const auth = getAuth();
export default {
  name: 'DetectiveGame',
  data() {
    return {
      typedTitle: '',
      titleStyle: {
        position: 'absolute',
        top: '36%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        color: 'white',
        fontSize: '14em',
        fontWeight: '600',
        fontFamily: "'Anta', sans-serif"
      },
      startButtonStyle: {
        position: 'absolute',
        bottom: '20%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '20px 40px',
        fontSize: '2.2em',
        cursor: 'pointer',
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        border: 'none',
        borderRadius: '5px',
        color: 'white',
        boxShadow: '2px 2px 4px #000000',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif"
      },
      signinButtonStyle: {
        position: 'absolute',
        bottom: '10%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '15px 30px',
        fontSize: '1.5em',
        cursor: 'pointer',
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        border: 'none',
        borderRadius: '5px',
        color: 'white',
        boxShadow: '2px 2px 4px #000000',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif"
      },
      signInOut: "Sign In"
    };
  },
  mounted() {
    this.typeTitle('DetectAIve', true);
    if(sessionStorage.getItem('user') == null){
      this.signInOut = "Sign In";
    } else {
      this.signInOut = "Sign Out";
    }
  },
  methods: {
    typeTitle(title, recursive = false) {
      let index = 0;
      const interval = setInterval(() => {
        this.typedTitle += title[index];
        index++;
        if (index === title.length) {
          clearInterval(interval);
          if (recursive) {
            setTimeout(() => {
              this.typedTitle = '';
              this.typeTitle(title, recursive);
            }, 2000); // Wait 2 seconds before restarting the animation
          }
        }
      }, 150); // Adjust the speed of typing by changing the interval time
    },
    startGame() {
      this.$router.push({ name: 'modes' });
    },
    signIn() {
      if(sessionStorage.getItem('user') == null){
        signInWithPopup(auth, provider)
          .then((result) => {
            // This gives you a Google Access Token. You can use it to access the Google API.
            const credential = GoogleAuthProvider.credentialFromResult(result);
            const token = credential.accessToken;
            sessionStorage.setItem('token', token)
            // The signed-in user info.
            const user = result.user;
            sessionStorage.setItem('user', user)
            // IdP data available using getAdditionalUserInfo(result)
            // ...
            this.signInOut = "Sign Out";

            const userData = {
              uid: user.uid,
              name: user.displayName,
              email: user.email,
            };
            sessionStorage.setItem('user', JSON.stringify({
              uid: user.uid,
              displayName: user.displayName,
              email: user.email,
            }));
            // store user information in the backend 
            
            axios.post('http://127.0.0.1:5000/api/store_user', userData)

              .then(response => {
                console.log('User data sent to backend:', response.data);
              })
              .catch(error => {
                console.error('Error sending user data:', error);
              });

          }).catch((error) => {
            // Handle Errors here.
            // eslint-disable-next-line
            const errorCode = error.code;
            // eslint-disable-next-line
            const errorMessage = error.message;
            // The email of the user's account used.
            // eslint-disable-next-line
            const email = error.customData.email;
            // The AuthCredential type that was used.
            // eslint-disable-next-line
            const credential = GoogleAuthProvider.credentialFromError(error);
            // ...
          });
        } else {
          signOut(auth).then(() => {
            // Sign-out successful.
            this.signInOut = "Sign In";
            sessionStorage.removeItem('token')
            sessionStorage.removeItem('user')
          }).catch((error) => {
            // error happened
            // eslint-disable-next-line
            const errorCode = error.code;
            // eslint-disable-next-line
            const errorMessage = error.message;
            // The email of the user's account used.
            // eslint-disable-next-line
            const email = error.customData.email;ß
            // The AuthCredential type that was used.
            // eslint-disable-next-line
            const credential = GoogleAuthProvider.credentialFromError(error);
          });
        }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Anta&display=swap');

.game-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #121f39;
  font-family: 'Anta', sans-serif;
}

.typing-effect {
  border-right: 2px solid white;
  white-space: nowrap;
  overflow: hidden;
  animation: typing 0.75s steps(30, end), blink 0.75s step-end infinite;
}

@keyframes typing {
  from { width: 0; }
  to { width: 100%; }
}

@keyframes blink {
  50% { border-color: transparent; }
}
</style>