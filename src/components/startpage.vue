<!-- startpage.vue -->
<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      DetectAIve
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
      gameContainerStyle: {
        backgroundImage: 'url(' + require('@/assets/startpage.png') + ')',
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
        top: '30%',
        left: '54%',
        transform: 'translate(-50%, -50%)',
        color: 'black',
        fontSize: '6em',
        textShadow: '2px 2px 4px #FFFFE0',
        fontWeight: '600'
      },
      startButtonStyle: {
        position: 'absolute',
        bottom: '40%',
        left: '53%',
        transform: 'translate(-50%, -50%)',
        padding: '15px 30px',
        fontSize: '1.5em',
        cursor: 'pointer',
        backgroundColor: 'rgba(0, 0, 0, 0.4)',
        border: 'none',
        borderRadius: '5px',
        color: 'Black',
        boxShadow: '2px 2px 4px #000000',
        fontWeight: '550'
      }
    };
  },
  methods: {
    startGame() {
      this.$router.push({ name: 'modes' });
    }
  }
}
</script>

<style scoped>
/* Add general styles here */
</style>
