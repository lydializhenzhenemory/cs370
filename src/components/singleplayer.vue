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
        :disabled="questionLimitReached"
      />
    </div>
    <div class="question-log" ref="questionLogContainer">
      <p v-for="(log, index) in questionLog" :key="index" class="log-item">{{ log }}</p>
    </div>
    <button class="fetch-prompt-button" @click="fetchNewPromptAndReset">Change prompt</button>
    <button class="guess-button" @click="openGuessModal">Make a Guess</button>
    <!-- modal for guess -->
    <div class="modal" v-if="showGuessModal">
      <div class="modal-content">
        <span class="close" @click="closeGuessModal">&times;</span>
        <h2>Make a Guess</h2>
        <textarea v-model="guess" class="guess-textarea" placeholder="Enter your guess"></textarea>
        <button class="submit-guess-button" @click="submitGuess">Submit Guess</button>
      </div>
    </div>
    <div v-if="guessResponse" class="guess-response">
      {{ guessResponse }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DetectiveGame',
  data() {
    return {
      guessResponse: '',
      guessAttempts: sessionStorage.getItem('guessAttempts') || 3, //change later
      guess: '',
      showGuessModal: false,
      questionLimit: sessionStorage.getItem('questionLimit') || 20, //change later 
      questionLog: [],
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
        textAlign: 'center',
        maxWidth: '100%',
      }
    };
  },
  computed: {
    questionLimitReached() {
      return this.questionLog.length >= this.questionLimit;
    }
  },
  watch: {
    guessAttempts(newVal) {
      if (newVal === 0) {
        this.$router.push('/modes/singleplayer/losing');
        //reset guess attempts and other game state when redirecting to losing page
        this.fetchNewPromptAndReset();

        //sessionStorage.setItem('pageVisited', 'false');
      }
    }
  },
  mounted() {
    //this data stored in each session so refreshing wont affeect it
    if (sessionStorage.getItem('pageVisited')) {

      this.typedTitle = sessionStorage.getItem('typedTitle');
      this.story_id = sessionStorage.getItem('storyId');
      this.questionLog = JSON.parse(sessionStorage.getItem('questionLog')) || [];
  } else {
    this.fetchNewPrompt();
  }

  sessionStorage.setItem('pageVisited', 'true');
  },
  methods: {
    fetchNewPrompt() {
      this.questionLog = [];
      this.questionCount = 0;
      const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player';
      axios.get(path)
        .then((res) => {
          const prompt = 'story prompt: ' + res.data.surface_story;
          this.story_id = res.data.story_id;
          this.typeTitle(prompt);
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
          sessionStorage.setItem('typedTitle', this.typedTitle);
        }
      }, 75);
    },
    submitQuestion() {
      const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player/question';
      axios.post(path, { question: this.userQuestion, story_id: this.story_id, user_id: '' })
        .then((response) => {
          const responseData = JSON.parse(JSON.stringify(response.data));
          if (responseData.error) {
            this.responseData = responseData.error;
          } else {
            this.questionLog.push(`User Question: ${this.userQuestion}, Response: ${responseData.response}`);
            this.saveQuestionLog();
            this.scrollToBottom();
            this.userQuestion = '';
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    saveQuestionLog() {
      sessionStorage.setItem('questionLog', JSON.stringify(this.questionLog));
    },
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.questionLogContainer.scrollTop = this.$refs.questionLogContainer.scrollHeight;
      });
    },
    fetchNewPromptAndReset() {
      this.guessAttempts = 3;
      sessionStorage.setItem('guessAttempts', this.guessAttempts);
      this.questionLimit = 20; // Reset the question limit
      sessionStorage.setItem('questionLimit', this.questionLimit);

      sessionStorage.removeItem('typedTitle');
      sessionStorage.removeItem('storyId');
      sessionStorage.removeItem('questionLog');
      this.questionLog = [];
      this.userQuestion = '';
      this.typedTitle = '';
      this.guessResponse = '';
      this.fetchNewPrompt();
    },
    openGuessModal() {
      console.log("Opening Guess Modal");
      this.showGuessModal = true;
      this.guess = '';
    },
    closeGuessModal() {
      console.log("Closing Guess Modal");
      this.showGuessModal = false;
      this.guess = '';
    },
    submitGuess() {
      const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player/guess';
      axios.post(path, {
        guess: this.guess,
        story_id: this.story_id,
        surfacePrompt: this.typedTitle,
        user_id: '' 
      })
      .then(response => {
        console.log('Guess submitted successfully:', response.data);
        this.closeGuessModal(); //closes modal after guess, update later if needed
        //must decrement guess attempts if guess is incorrect
        if (response.data.is_correct === 'Incorrect') {
          this.guessAttempts--;
          sessionStorage.setItem('guessAttempts', this.guessAttempts);
        }
        if (response.data.is_correct === 'Unexpected response. Prompt failed') { //we want to reduce this later, this should not count as a guess, fix later
          this.guessAttempts--;
          sessionStorage.setItem('guessAttempts', this.guessAttempts);
        }
        this.guessResponse = response.data.is_correct;
        if (response.data.is_correct === 'Correct') {
          this.$router.push('/modes/singleplayer/winning');
        }
      })
      .catch(error => {
        console.error('Error submitting guess:', error);
        this.closeGuessModal();
      });
    }
  }
}
</script>
<style scoped>
.question-box {
  position: absolute;
  bottom: 8%;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 1000px;
}

.question-input {
  width: 100%;
  padding: 2em;
  font-size: 1em;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  background: rgba(90, 94, 109, 0.5);
  color: #000000;
  outline: none;
}

.typing-effect {
  display: inline;
  border-right: 2px solid white;
  overflow: hidden;
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
  overflow-y: auto;
}

.question-log::-webkit-scrollbar {
  width: 20px;
}

.question-log::-webkit-scrollbar-thumb {
  background-color: rgb(166, 210, 234);
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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
/* modal styles*/
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.5);
}
.modal-content {
  background-color: white;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}
.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.guess-textarea {
  width: 100%;
  height: 100px;
  margin-bottom: 10px;
}
.submit-guess-button {
  background-color: greenyellow;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
/*button starts here*/
.guess-button {
  position: absolute;
  bottom: 160px;
  right: 20px;
  background-color: yellowgreen;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 16px;
  transition: background-color 0.3s ease;
}
.guess-button:hover {
  background-color: darkolivegreen; 
}
/*guess response, change later */
.guess-response {
  position: absolute;
  top: 50%;
  left: 90%;
  transform: translate(-50%, -50%);
  font-size: 2em;
  font-weight: bold;
  color: white;
}

</style>
