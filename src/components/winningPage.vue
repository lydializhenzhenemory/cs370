<!-- startpage.vue -->
<template>
    <div id="game-container" :style="gameContainerStyle">
    </div>
  </template>
  
  <script>
  export default {
    name: 'DetectiveGame',
    data() {
      return {
        gameContainerStyle: {
          backgroundImage: 'url(' + require('@/assets/winning.png') + ')',
          backgroundSize: '100%',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center',
          position: 'relative',
          width: '100%',
          height: '100vh',
          overflow: 'hidden'
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
  