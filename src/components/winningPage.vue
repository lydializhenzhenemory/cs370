<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      Congratulations, you have solved the mystery!
    </div>
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
        backgroundColor: '#121f39' // Set the background color to blue
      },
      titleStyle: {
        position: 'absolute',
        top: '40%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        color: 'white',
        fontSize: '4em',
        fontWeight: '550',
        fontFamily: "'Anta', sans-serif" // Set the font to Anta
      }
    };
  },
  methods: {
  }
}
</script>

<style scoped>
/* Add general styles here */
</style>
