<template>
  <div id="game-container" :style="gameContainerStyle">
    <div id="title" :style="titleStyle">
      Select a Mode
    </div>
    <button id="start-button1" @click="startGame1" :style="startButtonStyle1">
      Single player 
    </button>

    <button id="leaderboard-button" @click="toggleLeaderboard" :style="startButtonStyle2">
      Leaderboard
    </button>


    <!-- Leaderboard Display -->
    <div v-if="showLeaderboard" :style="leaderboardStyle" class="leaderboard">
      <h2>Leaderboard</h2>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Wins</th>
              <th>Average Questions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(entry, index) in leaderboard" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ entry[0] }}</td> <!-- Username -->
              <td>{{ entry[1] }}</td> <!-- Wins -->
              <td>{{ entry[2] }}</td> <!-- Average Questions - if there's another element -->
            </tr>
          </tbody>
        </table>
    </div>

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
import axios from 'axios';
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
      showLeaderboard: false,
      leaderboard: [],
      leaderboardStyle: {
        color: 'white',
        backgroundColor: '#001d33', // Dark blue background
        padding: '20px',
        borderRadius: '10px',
        position: 'absolute',
        bottom: '30%', // Position where the Multiplayer button was
        left: '50%',
        transform: 'translate(-50%, -50%)', // Center it horizontally
        textAlign: 'center',
        fontSize: '1.2em', // Dynamic font-size adjustment
        width: '100%', // Take full width to center the content
        maxWidth: '600px', // Max width of the content
        zIndex: 2, // Ensure it's above other content
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.5)', // subtle shadow
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
  created() {
    this.fetchLeaderboardData(); // Fetch leaderboard data when component is created
  },
  methods: {
    startGame1() {
      this.$router.push({ name: 'singleplayer' });
    },
    startGame2() {
      this.$router.push({ name: 'multiplayer' });
    },
    toggleLeaderboard() {
      this.showLeaderboard = !this.showLeaderboard;
      console.log("Show Leaderboard: ", this.showLeaderboard); // Debugging line to check the toggle
      if (this.showLeaderboard && this.leaderboard.length === 0) {
        this.fetchLeaderboardData();
      }
    },


    fetchLeaderboardData() {
      axios.get('http://127.0.0.1:5000/leaderboard')
        .then(response => {
          this.leaderboard = response.data;
        })
        .catch(error => {
          console.error('Error fetching leaderboard data:', error);
        });
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

.leaderboard-container {
  background-color: #001d33; /* Match the header background color */
  padding: 1rem; /* Or any other value to give some space around the table */
  border-radius: 8px; /* To match the table's border-radius if it has one */
}

.leaderboard table {
  width: 100%;
  text-align: left;
  border-collapse: separate;
  border-spacing: 0;
}

.leaderboard th {
  background-color: #001d33; /* Header background color */
  color: white;
  padding: 16px 8px;
}

.leaderboard td {
  padding: 12px 8px;
  color: white;
}

.leaderboard tr:nth-child(odd) {
  background-color: #005599; /* Darker shade for odd rows */
}

.leaderboard tr:nth-child(even) {
  background-color: #001d33; /* Lighter shade for even rows, matching the header */
}

.leaderboard {
  border: 2px solid #001d33; /* Adjusting the outer border to match the header and even rows */
  border-radius: 8px;
  overflow: hidden;
  border: none;
}

.leaderboard h2 {
  text-align: center;
  margin: 0;
  padding: 16px;
  background-color: #001d33; /* Making the header background consistent with the border */
  color: white;
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