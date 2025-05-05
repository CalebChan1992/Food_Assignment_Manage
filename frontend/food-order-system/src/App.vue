<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import OrderList from './components/OrderList.vue';
import BotManager from './components/BotManager.vue';
import OrderControls from './components/OrderControls.vue';

// API URL - would be in .env in a real app
const API_URL = 'http://localhost:5000/api';

// State
const pendingOrders = ref<any[]>([]);
const completedOrders = ref<any[]>([]);
const bots = ref<any[]>([]);
const loading = ref(false);
const error = ref('');

// Theme state
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true');

// Toggle dark mode
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  localStorage.setItem('darkMode', isDarkMode.value.toString());
  applyTheme();
};

// Apply theme based on current mode
const applyTheme = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark-theme');
  } else {
    document.documentElement.classList.remove('dark-theme');
  }
};

// Fetch all orders
const fetchOrders = async () => {
  try {
    const response = await fetch(`${API_URL}/orders`);
    const data = await response.json();

    pendingOrders.value = data.orders.filter((order: any) => order.status === 'PENDING' || order.status === 'PROCESSING');
    completedOrders.value = data.orders.filter((order: any) => order.status === 'COMPLETE');
  } catch (err) {
    console.error('Error fetching orders:', err);
    error.value = 'Failed to fetch orders';
  }
};

// Fetch all bots
const fetchBots = async () => {
  try {
    const response = await fetch(`${API_URL}/bots`);
    const data = await response.json();
    bots.value = data.bots;
  } catch (err) {
    console.error('Error fetching bots:', err);
    error.value = 'Failed to fetch bots';
  }
};

// Create a normal order
const createNormalOrder = async () => {
  loading.value = true;
  try {
    await fetch(`${API_URL}/orders/normal`, {
      method: 'POST',
    });
    await fetchOrders();
    await fetchBots();
  } catch (err) {
    console.error('Error creating normal order:', err);
    error.value = 'Failed to create normal order';
  } finally {
    loading.value = false;
  }
};

// Create a VIP order
const createVipOrder = async () => {
  loading.value = true;
  try {
    await fetch(`${API_URL}/orders/vip`, {
      method: 'POST',
    });
    await fetchOrders();
    await fetchBots();
  } catch (err) {
    console.error('Error creating VIP order:', err);
    error.value = 'Failed to create VIP order';
  } finally {
    loading.value = false;
  }
};

// Add a bot
const addBot = async () => {
  loading.value = true;
  try {
    await fetch(`${API_URL}/bots/add`, {
      method: 'POST',
    });
    await fetchBots();
    await fetchOrders();
  } catch (err) {
    console.error('Error adding bot:', err);
    error.value = 'Failed to add bot';
  } finally {
    loading.value = false;
  }
};

// Remove a bot
const removeBot = async () => {
  loading.value = true;
  try {
    await fetch(`${API_URL}/bots/remove`, {
      method: 'POST',
    });
    await fetchBots();
    await fetchOrders();
  } catch (err) {
    console.error('Error removing bot:', err);
    error.value = 'Failed to remove bot';
  } finally {
    loading.value = false;
  }
};

// Poll for updates
const startPolling = () => {
  setInterval(async () => {
    await fetchOrders();
    await fetchBots();
  }, 1000);
};

// Initialize
onMounted(async () => {
  // Apply theme on initial load
  applyTheme();

  // Check system preference for dark mode if not set in localStorage
  if (localStorage.getItem('darkMode') === null) {
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    isDarkMode.value = prefersDarkMode;
    localStorage.setItem('darkMode', isDarkMode.value.toString());
    applyTheme();
  }

  await fetchOrders();
  await fetchBots();
  startPolling();
});
</script>

<template>
  <div class="app">
    <header>
      <div class="logo">
        <span class="logo-icon">🍔</span>
      </div>
      <h1>FoodFlow Command Center</h1>
      <button @click="toggleDarkMode" class="theme-toggle" :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'">
        <span v-if="isDarkMode" class="theme-icon">☀️</span>
        <span v-else class="theme-icon">🌙</span>
      </button>
    </header>

    <main>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="loading" class="loading">
        Loading...
      </div>

      <OrderControls
        @create-normal-order="createNormalOrder"
        @create-vip-order="createVipOrder"
      />

      <div class="order-section">
        <OrderList title="PENDING ORDERS" :orders="pendingOrders" />
        <OrderList title="COMPLETED ORDERS" :orders="completedOrders" />
      </div>

      <BotManager
        :bots="bots"
        @add-bot="addBot"
        @remove-bot="removeBot"
      />
    </main>
  </div>
</template>

<style>
:root {
  --primary: #FF6B35;
  --secondary: #4CB944;
  --accent: #FFD23F;
  --dark: #292929;
  --light: #FFFFFF;
  --success: #27AE60;
  --pending: #F39C12;
  --shadow: rgba(0, 0, 0, 0.1);
  --bg-color: #f8f8f8;
  --card-bg: #FFFFFF;
  --text-color: #292929;
  --border-color: #eee;
  --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.dark-theme {
  --primary: #FF8B55;
  --secondary: #6CD964;
  --accent: #FFE25F;
  --dark: #f0f0f0;
  --light: #1E1E1E;
  --success: #4AE583;
  --pending: #FFB142;
  --shadow: rgba(0, 0, 0, 0.3);
  --bg-color: #121212;
  --card-bg: #2A2A2A;
  --text-color: #E0E0E0;
  --border-color: #444;
  --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', 'Arial', sans-serif;
}

body {
  color: var(--text-color);
  background-color: var(--bg-color);
  background-image: url('data:image/svg+xml;utf8,<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h100v100H0z" fill="none"/><path d="M10 10h10v10H10zM30 10h10v10H30zM50 10h10v10H50zM70 10h10v10H70zM90 10h10v10H90zM0 30h10v10H0zM20 30h10v10H20zM40 30h10v10H40zM60 30h10v10H60zM80 30h10v10H80zM10 50h10v10H10zM30 50h10v10H30zM50 50h10v10H50zM70 50h10v10H70zM90 50h10v10H90zM0 70h10v10H0zM20 70h10v10H20zM40 70h10v10H40zM60 70h10v10H60zM80 70h10v10H80zM10 90h10v10H10zM30 90h10v10H30zM50 90h10v10H50zM70 90h10v10H70zM90 90h10v10H90z" fill="%23FFD23F" fill-opacity="0.05"/></svg>');
  transition: background-color 0.3s ease;
}

.dark-theme body {
  background-image: url('data:image/svg+xml;utf8,<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h100v100H0z" fill="none"/><path d="M10 10h10v10H10zM30 10h10v10H30zM50 10h10v10H50zM70 10h10v10H70zM90 10h10v10H90zM0 30h10v10H0zM20 30h10v10H20zM40 30h10v10H40zM60 30h10v10H60zM80 30h10v10H80zM10 50h10v10H10zM30 50h10v10H30zM50 50h10v10H50zM70 50h10v10H70zM90 50h10v10H90zM0 70h10v10H0zM20 70h10v10H20zM40 70h10v10H40zM60 70h10v10H60zM80 70h10v10H80zM10 90h10v10H10zM30 90h10v10H30zM50 90h10v10H50zM70 90h10v10H70zM90 90h10v10H90z" fill="%23FFD23F" fill-opacity="0.03"/></svg>');
}

.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--card-bg);
  box-shadow: 0 4px 20px var(--shadow);
  border-radius: 12px;
  margin-top: 2rem;
  margin-bottom: 2rem;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

header {
  margin-bottom: 2rem;
  text-align: center;
  position: relative;
  padding-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background-color: var(--accent);
  border-radius: 2px;
}

h1 {
  color: var(--primary);
  font-size: 2.5rem;
  font-weight: bold;
  text-shadow: 2px 2px 4px var(--shadow);
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  border-left: 5px solid #f5c6cb;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-5px); }
  40%, 80% { transform: translateX(5px); }
}

.loading {
  text-align: center;
  margin-bottom: 1rem;
  font-style: italic;
  color: var(--dark);
  position: relative;
  padding-left: 24px;
}

.loading::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  border: 3px solid var(--accent);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: translateY(-50%) rotate(360deg); }
}

.order-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 2rem;
  width: 100%;
}

@media (min-width: 768px) {
  .order-section {
    flex-direction: row;
    justify-content: space-between;
  }

  .order-section > * {
    flex: 1;
    max-width: 48%;
  }
}

/* Logo styling */
.logo {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.logo .logo-icon {
  font-size: 3.5rem;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.2));
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Theme toggle button */
.theme-toggle {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.5rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background-color: rgba(0, 0, 0, 0.05);
}

.theme-toggle:hover {
  transform: rotate(15deg);
  background-color: rgba(0, 0, 0, 0.1);
}

.theme-icon {
  line-height: 1;
}

/* Add a subtle animation to the whole app */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

main {
  animation: fadeIn 0.5s ease-out;
}
</style>
