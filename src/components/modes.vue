<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      Select a Mode
    </div>
    <button id="start-button1" @click="startGame1" :style="startButtonStyle1">
      Single player 
    </button>
    <button id="start-button2" @click="startGame2" :style="startButtonStyle2">
      Multiplayer
    </button>

    <!-- Instructions Button -->
    <button :style="instructionsButtonStyle" @click="showDialog = true">
      Instructions
    </button>

    <!-- Custom Instructions Dialog -->
    <div v-if="showDialog" class="dialog-overlay" @click.self="showDialog = false">
      <div class="dialog" :style="dialogStyle">
        <h2>Game Instructions</h2>
        <p class="instruction-paragraph">Single player game: your goal is to unravel a mystery presented by asking strategic yes/no questions. You are permitted to ask any question that can be answered with "yes," "no," or "irrelevant" to deduce the circumstances of the scenario. Use your questions wisely to piece together the story to solve the mystery as efficiently as possible.</p>
        <p class="instruction-paragraph">Multi players game: your objective is to outsmart your opponents by being the first to solve a mystery through strategic yes/no questions. On your turn, you may ask the host any question that can be answered with "yes," "no," or "irrelevant" to piece together the hidden scenario. The game advances with each player's turn, escalating in intrigue as you collectively narrow down the possibilities. Victory is claimed by the first player to correctly unravel the mystery, while those who concede will await the host's revelation of the story's full details.</p>
        <button @click="showDialog = false">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModeSelection',
  data() {
    return {
      showDialog: false,
      gameContainerStyle: {
        position: 'relative',
        width: '100%',
        height: '100vh',
        overflow: 'hidden',
        backgroundColor: '#121f39'
      },
      titleStyle: {
        position: 'absolute',
        top: '15%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        color: 'white',
        fontSize: '2em',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif"
      },
      startButtonStyle1: {
        position: 'absolute',
        bottom: '55%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '15px 60px',
        fontSize: '1.5em',
        cursor: 'pointer',
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
        border: 'none',
        borderRadius: '5px',
        color: 'white',
        boxShadow: '2px 2px 4px #000000',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif"
      },
      startButtonStyle2: {
        position: 'absolute',
        bottom: '30%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '15px 70px',
        fontSize: '1.5em',
        cursor: 'pointer',
        backgroundColor: 'rgba(0, 0, 0, 0.3)',
        border: 'none',
        borderRadius: '5px',
        color: 'white',
        boxShadow: '2px 2px 4px #000000',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif"
      },
      instructionsButtonStyle: {
        position: 'absolute',
        top: '20px',
        left: '1250px',
        backgroundColor: 'transparent',
        color: 'white',
        border: 'none',
        textDecoration: 'underline',
        cursor: 'pointer',
        padding: '20px 20px',
        fontSize: '1em',
        fontFamily: "'Anta', sans-serif"
      }
    };
  },
  methods: {
    startGame1() {
      this.$router.push({ name: 'singleplayer' });
    },
    startGame2() {
      this.$router.push({ name: 'multiplayer' });
    }
  }
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: rgb(132, 143, 148);
  padding: 20px;
  border-radius: 5px;
  width: 90%;
  max-width: 600px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0);
}

.instruction-paragraph {
  margin-bottom: 1em;
}
</style>
