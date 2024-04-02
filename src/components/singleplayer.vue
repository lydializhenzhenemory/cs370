<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      <div class="typing-effect">{{ typedTitle }}</div>
    </div>
    <div v-if="!questionLimitReached" class="question-box">
      <input
        type="text"
        v-model="userQuestion"
        placeholder="Text a question:"
        class="question-input"
        @keyup.enter="submitQuestion"
      />
    </div>
    <div class="question-log" ref="questionLogContainer">
      <p v-for="(log, index) in questionLog" :key="index" class="log-item">{{ log }}</p>
    </div>
    <button class="fetch-prompt-button" @click="fetchNewPromptAndReset">Play New Game</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'DetectiveGame',
  data() {
    return {
      questionLimit: 10, //change later
      questionLog: [], //array for question log
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
  computed: {
    questionLimitReached() {
      return this.questionLog.length >= this.questionLimit;
    }
  },
  mounted() {
  // Check if the page has been visited in the same session
  if (sessionStorage.getItem('pageVisited')) {
    // The page has been refreshed, load the prompt from localStorage
    this.typedTitle = localStorage.getItem('typedTitle');
    this.story_id = localStorage.getItem('storyId');
    this.questionLog = JSON.parse(localStorage.getItem('questionLog')) || []; //added questionLog
    
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
    localStorage.removeItem('questionLog');
  },
  fetchNewPrompt() {
    this.questionLog = []; //makes sure that log is persistent with story prompt
    this.questionCount = 0;

    const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player';
    axios.get(path)
      .then((res) => {
        const prompt = 'story prompt: ' + res.data.surface_story;
        this.story_id = res.data.story_id;
        this.typeTitle(prompt); // Call typeTitle to create the typing effect
        // Store the fetched prompt and story ID in localStorage
        localStorage.setItem('typedTitle', prompt);
        localStorage.setItem('storyId', this.story_id);
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
      axios.post(path, { question: this.userQuestion, story_id: this.story_id, user_id: '' })
        .then((response) => {
          const responseData = JSON.parse(JSON.stringify(response.data));
          if (responseData.error) {
            this.responseData = responseData.error;
          } else {
            //response now saved and displayed in log
            //this.responseData = `User Question: ${this.userQuestion}, Response: ${responseData.response}`;

            //add question to the log
            this.questionLog.push(`User Question: ${this.userQuestion}, Response: ${responseData.response}`);
            this.saveQuestionLog(); //save question log after adding a new question
            this.scrollToBottom(); //need to do this after adding a new log entry

            //reset user input
            this.userQuestion = '';
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    saveQuestionLog() {
      localStorage.setItem('questionLog', JSON.stringify(this.questionLog));
    },
    scrollToBottom() {
      //$nextTick waits for Vue to update the DOM
      this.$nextTick(() => {
        //scroll to the bottom of the log container
        this.$refs.questionLogContainer.scrollTop = this.$refs.questionLogContainer.scrollHeight;
      });
    },
    fetchNewPromptAndReset() {
      //reset local storage
      localStorage.removeItem('typedTitle');
      localStorage.removeItem('storyId');
      localStorage.removeItem('questionLog');

      //need to reset question log and user question AND title
      this.questionLog = [];
      this.userQuestion = '';
      this.typedTitle = '';

      this.fetchNewPrompt(); //new prompt
    }
  }
}
</script>

<style scoped>
.question-box {
  position: absolute;
  bottom: 12%;
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

.question-log {
  position: absolute;
  top: 40%;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  overflow-y: auto;
  padding: 10px;
  background-color: transparent; 
  border-radius: 10px;
  max-height: 20%;
  overflow-y: auto; /*enables vertical scrolling when content overflows */
}

.question-log::-webkit-scrollbar {
  width: 20px; /*scrollbar width*/
}

.question-log::-webkit-scrollbar-thumb {
  background-color: darkslategrey; 
  border-radius: 20px; 
}

.log-item {
  font-family: 'Anta', sans-serif;
  font-size: 1em;
  color: white;
  margin: 5px 0;
}

.fetch-prompt-button {
  position: absolute;
  top: 5%;
  right: 5%;
  transform: translateX(0%);
  padding: 10px 20px;
  background-color: rgb(53, 68, 98);
  color: white;
  border: none;
  border-radius: 5px;
  font-family: 'Anta', sans-serif;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Added shadow */
}


</style>

