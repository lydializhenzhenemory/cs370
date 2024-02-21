<!-- singleplayer.vue -->
<template>
    <div id="game-container" :style="gameContainerStyle">
      <div id="title" :style="titleStyle">
        story prompt: It is Jake's birthday today. His dog died in the afternoon.
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
        gameContainerStyle: {
          backgroundImage: 'url(' + require('@/assets/background.png') + ')',
          backgroundSize: '100%',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center',
          position: 'relative',
          width: '100%',
          height: '100vh',
          overflow: 'hidden'
        },
        titleStyle: {
          position: 'absolute',
          top: '25%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          color: 'black',
          fontSize: '1.5em',
          fontWeight: '550',
        }
      };
    },
    methods: {
        submitQuestion() {
      // Handle the submission of the question
        console.log(this.userQuestion); // For now, just log it to the console
        },
    }
  }
  </script>
  
  <style scoped>
  .question-box {
    position: absolute;
    bottom: 15%; /* Adjust as needed */
    left: 43%;
    transform: translateX(-50%);
    width: 100%; /* Adjust width as needed to match your design */
    max-width: 600px; /* Adjust max-width as needed */
  }

  .question-input {
  width: 120%;
  padding: 1em;
  font-size: 1em;
  border: none; /* Remove border if not desired */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Soft shadow around the input */
  border-radius: 20px; /* Rounded borders */
  background: rgba(255, 255, 255, 0.5); /* Semi-transparent white */
  color: #000;
  outline: none; /* Remove blue outline on focus */
}

  /* Add general styles here */
  </style>
  