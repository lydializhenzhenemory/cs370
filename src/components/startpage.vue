<template>
  <div id="game-container" class="game-container">
    <div id="title" :style="titleStyle">
      <span class="typing-effect">{{ typedTitle }}</span>
    </div>
    <button id="start-button" @click="startGame" :style="startButtonStyle">
      Start Game
    </button>
  </div>
</template>

<script>
export default {
  name: 'DetectiveGame',
  data() {
    return {
      typedTitle: '',
      titleStyle: {
        position: 'absolute',
        top: '30%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        color: 'white',
        fontSize: '6em',
        fontWeight: '600',
        fontFamily: "'Anta', sans-serif"
      },
      startButtonStyle: {
        position: 'absolute',
        bottom: '30%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        padding: '15px 30px',
        fontSize: '1.5em',
        cursor: 'pointer',
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        border: 'none',
        borderRadius: '5px',
        color: 'white',
        boxShadow: '2px 2px 4px #000000',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif"
      }
    };
  },
  mounted() {
    this.typeTitle('DetectAIve', true);
  },
  methods: {
    typeTitle(title, recursive = false) {
      let index = 0;
      const interval = setInterval(() => {
        this.typedTitle += title[index];
        index++;
        if (index === title.length) {
          clearInterval(interval);
          if (recursive) {
            setTimeout(() => {
              this.typedTitle = '';
              this.typeTitle(title, recursive);
            }, 2000); // Wait 2 seconds before restarting the animation
          }
        }
      }, 150); // Adjust the speed of typing by changing the interval time
    },
    startGame() {
      this.$router.push({ name: 'modes' });
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Anta&display=swap');

.game-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: #121f39;
  font-family: 'Anta', sans-serif;
}

.typing-effect {
  border-right: 2px solid white;
  white-space: nowrap;
  overflow: hidden;
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
