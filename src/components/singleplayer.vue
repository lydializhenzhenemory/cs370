<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      <div class="typing-effect">{{ typedTitle }}</div>
    </div>
    <div class="question-box">
      <input
        type="text"
        v-model="userQuestion"
        placeholder="Text a question:"
        class="question-input"
        @keyup.enter="submitQuestion"
      />
    </div>
    <div class="response-box">
      <p v-if="responseData" class="response-text">{{ responseData }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'DetectiveGame',
  data() {
    return {
      userQuestion: '',
      typedTitle: '',
      responseData: '',
      gameContainerStyle: {
        position: 'relative',
        width: '100%',
        height: '100vh',
        overflow: 'hidden',
        backgroundColor: '#121f39'
      },
      titleStyle: {
        position: 'absolute',
        top: '25%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        color: 'white',
        fontSize: '1.5em',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif",
        textAlign: 'center', // Center the text horizontally
        maxWidth: '80%', // Set a maximum width for the title
      }
    };
  },
  mounted() {
    this.typeTitle('story prompt: Jack ate a cake prjddg krnkxf jgkrsjgoiesj rogje rofi jawdoi jwqjgz ionfjnl knflker toiregnterkngawrngp ojrpweojrw3nrwejfpoand died.');
  },
  methods: {
    typeTitle(title) {
      let index = 0;
      const interval = setInterval(() => {
        this.typedTitle += title[index];
        index++;
        if (index === title.length) {
          clearInterval(interval);
        }
      }, 75); // Adjust the speed of typing by changing the interval time
    },
    submitQuestion() {
      if (this.userQuestion.trim() !== '') {
        // make an HTTP POST request to send the user's question to the Flask backend
        axios.post('http://127.0.0.1:5000/api/question', { //local for now
          question: this.userQuestion
        })
        .then(response => {
          console.log('Question submitted successfully');
          // handle the response from the backend
          this.handleResponse(response.data);
          //clear input
          this.userQuestion = '';
        })
        .catch(error => {
          console.error('Error submitting question:', error);
        });
      }
    },
    handleResponse(responseData) {
      // update variable to store the response data
      this.responseData = responseData;
    }
  }
}
</script>

<style scoped>
.response-box {
  position: absolute;
  top: 60%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.response-text {
  font-family: 'Anta', sans-serif;
  font-size: 1em;
  color: white; 
}

.question-box {
  position: absolute;
  bottom: 20%;
  left: 33%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 600px;
}

.question-input {
  width: 180%;
  padding: 2em; /* Increased padding to make the input box taller */
  font-size: 1.2em; /* Optional: Increase font-size if you want larger text */
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.5);
  color: #000;
  outline: none;
}

.typing-effect {
  display: inline; /* Make the element inline-block */
  border-right: 2px solid white; /* Cursor style */
  overflow: hidden; /* Hides the overflow text */
  animation: blink 0.75s step-end infinite;
}

.typing-effect:after {
  animation: blink 0.75s step-end infinite;
}

</style>
