<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      <span class="typing-effect">{{ typedTitle }}</span>
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
  </div>
</template>

<script>
export default {
  name: 'DetectiveGame',
  data() {
    return {
      userQuestion: '',
      typedTitle: '',
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
        fontFamily: "'Anta', sans-serif"
      }
    };
  },
  mounted() {
    this.typeTitle('story prompt: It is Jake\'s birthday today. His dog died in the afternoon.');
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
      }, 150); // Adjust the speed of typing by changing the interval time
    },
    submitQuestion() {
      console.log(this.userQuestion); // For now, just log it to the console
    }
  }
}
</script>

<style scoped>
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
  padding: 1em;
  font-size: 1em;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.5);
  color: #000;
  outline: none;
}

.typing-effect {
  border-right: 2px solid white; /* Cursor style */
  white-space: nowrap; /* Keeps the text in a single line */
  overflow: hidden; /* Hides the overflow text */
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
