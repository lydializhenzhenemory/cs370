<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      <div class="typing-effect">{{ typedTitle }}</div>
    </div>
    <div v-if="!questionLimitReached" class="question-box">
      <input
        type="text"
        v-model="userQuestion"
        placeholder="Type Your Question Here:"
        class="question-input"
        @keyup.enter="submitQuestion"
        :disabled="questionLimitReached"
        maxlength="165"
      />
    </div>
    <div v-else class="question-limit-reached-message">
      No more questions remaining! You must use your detective skills and guess!
    </div>
    <div class="question-log" ref="questionLogContainer">
      <h3 class="log-header">Question History  ({{ this.questionLimit - this.questionLog.length }} Questions Remaining!)</h3>
      <p v-if="questionLog.length === 0" class="empty-log-message">You have not asked any questions yet.</p>
      <p v-for="(log, index) in questionLog" :key="index" class="log-item">{{ log }}</p>
    </div>
    <button class="fetch-prompt-button" @click="fetchNewPromptAndReset">Change Story Prompt</button>
    <button class="guess-button" @click="openGuessModal">
      Make A Guess! <span class="guess-attempts-text">(Guesses Remaining: {{ guessAttempts }})</span>
    </button>
    <!-- modal for guess -->
    <div class="modal" v-if="showGuessModal">
      <div class="modal-content">
        <span class="close" @click="closeGuessModal">&times;</span>
        <h2>Make a Guess</h2>
        <textarea v-model="guess" class="guess-textarea" placeholder="Enter Your Guess:" @keyup.enter="submitGuess"></textarea> 
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
      guessAttempts: sessionStorage.getItem('guessAttempts') || 4, //change later
      guess: '',
      showGuessModal: false,
      questionLimit: sessionStorage.getItem('questionLimit') || 24, //change later 
      questionLog: [],
      userQuestion: '',
      typedTitle: '',
      responseData: '',
      typingInterval: null,
      gameContainerStyle: {
        position: 'relative',
        width: '100%',
        height: '100vh',
        overflow: 'hidden',
        backgroundColor: '#121f39'
      },
      titleStyle: {
        position: 'absolute',
        top: '23%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        color: 'white',
        fontSize: '1.5em',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif",
        textAlign: 'center',
        width: '60%',
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

        this.endSession();
        //reset guess attempts and other game state when redirecting to losing page
        //moved these up here, let me know if they causes problems
        this.fetchNewPromptAndReset();
        sessionStorage.setItem('pageVisited', 'false');
        this.$router.push('/modes/singleplayer/losing');
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
      clearInterval(this.typingInterval); //clear interval if exists before typinf prompt
      this.questionLog = [];
      this.questionCount = 0;
      const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player';
      axios.get(path)
        .then((res) => {
          const prompt = 'Story Prompt: ' + res.data.surface_story;
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
      this.typingInterval = setInterval(() => {
        this.typedTitle += title[index];
        index++;
        if (index === title.length) {
          clearInterval(this.typingInterval);
          sessionStorage.setItem('typedTitle', this.typedTitle);
        }
      }, 75);
    },
    submitQuestion() {
      //first check if guess is empty
      if (this.userQuestion.trim() === '') {
        alert('Please enter a valid question before submitting!');
        return;
      }

      const path = 'https://cs370projectbackend-0t8f5ewp.b4a.run/single_player/question';
      axios.post(path, { question: this.userQuestion, story_id: this.story_id, user_id: '' })
        .then((response) => {
          const responseData = JSON.parse(JSON.stringify(response.data));
          if (responseData.error) {
            this.responseData = responseData.error;
          } else {
            this.questionLog.push(`-Your Question: ${this.userQuestion}, Response: ${responseData.response}`);
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
      this.guessAttempts = 4; //update to appropiate value!!! 
      sessionStorage.setItem('guessAttempts', this.guessAttempts);
      this.questionLimit = 24; // Reset the question limit
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
      //first check if guess is empty
      if (this.guess.trim() === '' || this.guess.trim().length < 12) {
        alert('Please enter a valid guess before submitting! (Your guess must at least 18 characters)');
        return;
      }

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
          this.guessResponse = 'Incorrect Guess! Try Again!';
          this.guessAttempts--;
          sessionStorage.setItem('guessAttempts', this.guessAttempts);
        }
        if (response.data.is_correct === 'Unexpected response. Prompt failed') { //we want to reduce this later, this should not count as a guess, fix later
          this.guessResponse = response.data.is_correct;
          this.guessAttempts--;
          sessionStorage.setItem('guessAttempts', this.guessAttempts);
        }
        
        this.endSession();
        if (response.data.is_correct === 'Correct') {
          this.fetchNewPrompt(); //after user wins, story now changes upon new game
          this.fetchNewPromptAndReset();
          sessionStorage.setItem('pageVisited', 'false');
          this.$router.push('/modes/singleplayer/winning');
        }
      })
      .catch(error => {
        console.error('Error submitting guess:', error);
        this.closeGuessModal();
      });

      this.resetGuessResponse(); //will help us disable guess response box again so user can get new response after each new guess
    },
    resetGuessResponse() {
      setTimeout(() => {
        this.guessResponse = ''; // Reset guess response
        //hides guess response box
        const guessResponseElement = document.querySelector('.guess-response');
        if (guessResponseElement) {
          guessResponseElement.style.display = 'none';
        }
      }, 10000); //milliseconds
    }, 
    // this should be called before redirecting to new page while now it is called for every question attempt
    endSession() {
      console.log("endSession called");
      this.checkAndSendUserInfo();
    },
    checkAndSendUserInfo() {
      console.log("checkAndSendUserInfo called");
      const userString = sessionStorage.getItem('user');
        if (userString) {
        let userInfo;
        try {
          // Try parsing the user data string into an object
          userInfo = JSON.parse(userString);
        } catch (e) {
          // If parsing fails, log the error and exit the function
          console.error("Error parsing user data from sessionStorage:", e);
          return; // Stop execution if there's an error
        }

        // Now that we have the userInfo, we can create the userData object
        const userData = {
          id: userInfo.uid, // User's unique ID from session storage
          win_or_lose: this.determineOutcome(), // This method should return 'win' or 'lose'
          questions_attempted: this.questionLog.length,
          story_id: this.story_id
        };

        // Send the user data to the backend
        axios.post('https://cs370projectbackend-0t8f5ewp.b4a.run/api/store_game_session', userData)
          .then(response => {
            console.log('User game data sent to backend:', response.data);
          })
          .catch(error => {
            console.error('Error during POST request:', error);
            console.error('Error details:', error.response);
          });
      }
  },

    determineOutcome() {
      return this.guessResponse === 'Correct' ? 1 : 0;
    }
  }
}
</script>
<style scoped>
.question-box {
  position: absolute;
  bottom: 6%;
  left: 40%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 1000px;
}

.question-limit-reached-message {
  position: absolute;
  bottom: 10%;
  left: 40%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 1000px;
  font-size: 22px;
  font-family: "Lucida Console", "Courier New", monospace;
  font-weight: bold;
  color: rgba(255,255,255,0.8);;
}

.question-input {
  width: 100%;
  padding: 1em;
  font-size: 1.5em;
  font-family: "Lucida Console", "Courier New", monospace;
  color: whitesmoke;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  background: rgba(90, 94, 109, 0.5);
}

.question-input::placeholder {
  font-family: "Lucida Console", "Courier New", monospace;
  color: rgba(255, 255, 255, 0.2);
}
.question-input,
.question-input:focus {
  font-family: "Lucida Console", "Courier New", monospace;
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
  top: 42%;
  left: 50%;
  transform: translateX(-50%);
  width: 85%;
  overflow-y: auto;
  padding: 10px;
  background-color: transparent;
  border-radius: 10px;
  max-height: 36%;
  overflow-y: auto;
  border: 2px solid rgb(135, 132, 132); 
}

.question-log::-webkit-scrollbar {
  width: 20px;
}

.question-log::-webkit-scrollbar-thumb {
  background-color: rgb(166, 210, 234);
  border-radius: 20px;
}

.log-header {
  font-size: 1.2em;
  font-weight: bold;
  font-family: 'Courier', monospace;
  color: whitesmoke;
  margin-bottom: 5px;
}

.empty-log-message {
  font-size: 1em;
  font-family: 'Courier New', monospace;
  color: rgba(255,255,255,0.5);
  margin-bottom: 5px;
}

.log-item {
  font-family: 'Courier New', monospace;
  font-size: 1em;
  color: white;
  margin: 5px 0;
}

.fetch-prompt-button {
  position: absolute;
  top: 5%;
  right: 3%;
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
  background-color: rgb(95, 113, 69);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
/*button starts here*/
.guess-button {
  position: absolute;
  bottom: 57px;
  right: 60px;
  background-color: rgb(88, 106, 52);
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 24px;
  font-family: 'Anta', sans-serif;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 16px;
  transition: background-color 0.3s ease;
}
.guess-button:hover {
  background-color: darkolivegreen; 
}

.guess-attempts-text {
  display: block;
  font-size: 0.6em;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 5px;
}

/*guess response, change later */
.guess-response {
  position: absolute;
  top: 17%;
  left: 80%;
  transform: translateX(-50%);
  font-family: 'Anta', sans-serif;
  font-size: 2em;
  font-weight: bold;
  color: rgb(198, 33, 33);
  animation: fadeIn 0.5s ease-in-out, pulse 1s infinite alternate;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes pulse {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.1);
  }
}

</style>