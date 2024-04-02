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
    <button class="fetch-prompt-button" @click="fetchNewPromptAndReset">Change prompt</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DetectiveGame',
  data() {
    return {
      questionLimit: 10,
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
    questionLimitReached(newVal) {
      if (newVal) {
        this.$router.push('/modes/singleplayer/losing');
      }
    }
  },
  mounted() {
  if (sessionStorage.getItem('pageVisited')) {
    this.typedTitle = localStorage.getItem('typedTitle');
    this.story_id = localStorage.getItem('storyId');
    this.questionLog = JSON.parse(localStorage.getItem('questionLog')) || [];
    this.questionLog.length = 0; // Set the length of questionLog to 0
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
          localStorage.setItem('typedTitle', this.typedTitle);
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
      localStorage.setItem('questionLog', JSON.stringify(this.questionLog));
    },
    scrollToBottom() {
      this.$nextTick(() => {
        this.$refs.questionLogContainer.scrollTop = this.$refs.questionLogContainer.scrollHeight;
      });
    },
    fetchNewPromptAndReset() {
      localStorage.removeItem('typedTitle');
      localStorage.removeItem('storyId');
      localStorage.removeItem('questionLog');
      this.questionLog = [];
      this.userQuestion = '';
      this.typedTitle = '';
      this.fetchNewPrompt();
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
</style>
