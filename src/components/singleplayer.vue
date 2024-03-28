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
  // Check if the page has been visited in the same session
  if (sessionStorage.getItem('pageVisited')) {
    // The page has been refreshed, load the prompt from localStorage
    this.typedTitle = localStorage.getItem('typedTitle');
    this.story_id = localStorage.getItem('storyId');
  } else {
    // The page is visited for the first time in this session, fetch a new prompt
    this.fetchNewPrompt();
  }

  // Set the flag in sessionStorage to indicate that the page has been visited
  sessionStorage.setItem('pageVisited', 'true');
},

  methods: {
    handlePageUnload() {
    localStorage.removeItem('typedTitle');
    localStorage.removeItem('storyId');
  },
  fetchNewPrompt() {
    const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player';
    //const path = 'http://127.0.0.1:5000';
      axios.get(path)
        .then((res) => {
          const prompt = 'story prompt: ' + res.data.surface_story;
          this.story_id = res.data.story_id;
          this.typeTitle(prompt); // Call typeTitle to create the typing effect
          // Store the fetched prompt and story ID in localStorage
          sessionStorage.setItem('typedTitle', prompt);
          sessionStorage.setItem('storyId', this.story_id);
        })
        .catch((error) => {
          console.error(error);
        });
  },
    typeTitle(title) {
      let index = 0;
      const interval = setInterval(() => {
      this.typedTitle += title[index];
      index++;
      if (index === title.length) {
        clearInterval(interval);
        // When the title is finished typing, set it in localStorage
        localStorage.setItem('typedTitle', this.typedTitle);
      }
    }, 75); // Adjust the speed of typing by changing the interval time
  },
    submitQuestion() {
      const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player/question';
      //const path = 'http://127.0.0.1:5000';
      if (this.userQuestion.trim() !== '') {
        axios.post(path, {question: this.userQuestion, story_id: this.story_id, user_id: ''})
        .then((res) => {
          //this.typeTitle('response: ' + JSON.parse(JSON.stringify(res)).data.response);
          // handle the response from the backend
          this.handleResponse(res.data.response);
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
