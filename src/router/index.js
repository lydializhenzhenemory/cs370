// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import StartPage from '@/components/startpage.vue';
import ModesPage from '@/components/modes.vue';
import SinglePlayer from '@/components/singleplayer.vue';
import MultiPlayer from '@/components/multiplayer.vue';
import Winning from '@/components/winningPage.vue';

const routes = [
  { path: '/', name: 'startpage', component: StartPage },
  { path: '/modes', name: 'modes', component: ModesPage },
  { path: '/modes/singleplayer', name: 'singleplayer', component: SinglePlayer },
  { path: '/modes/multiplayer', name: 'multiplayer', component: MultiPlayer },
  // Added unique names and meta fields for the winning routes
  {
    path: '/modes/singleplayer/winning',
    name: 'singleplayerWinning',
    component: Winning,
    meta: { mode: 'singleplayer' }
  },
  {
    path: '/modes/multiplayer/winning',
    name: 'multiplayerWinning',
    component: Winning,
    meta: { mode: 'multiplayer' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
