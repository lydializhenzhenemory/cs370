<template>
    <div id="game-container" :style="gameContainerStyle">
      <div id="title" :style="titleStyle">
        Sorry, you did not solve the mystery. Try play again!
      </div>
      <button @click="playAgain" class="play-again-button">Play again ;)</button>
    </div>
  </template>

  <script>
  export default {
    name: 'DetectiveGame',
    data() {
      return {
        gameContainerStyle: {
          position: 'relative',
          width: '100%',
          height: '100vh',
          overflow: 'hidden',
          backgroundColor: '#121f39'
        },
        titleStyle: {
          position: 'absolute',
          top: '40%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          color: 'white',
          fontSize: 'calc(1.5vw + 1.5vh)',
          fontWeight: '550',
          fontFamily: "'Anta', sans-serif"
        }
      };
    },
    methods: {
      playAgain() {
        // Use Vue Router to navigate to the /modes path
        this.$router.push('/modes');
      }
    }
  }
  </script>

  <style scoped>
  .play-again-button {
    position: absolute;
    top: 60%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 15px 30px;
    background-color: #182743;
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Anta', sans-serif;
    font-size: calc(1vw + 1vh);
    cursor: pointer;
    transition: background-color 0.3s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Added shadow */
  }
  
  .play-again-button:hover {
    background-color: #35485d;
  }

  </style>
  
