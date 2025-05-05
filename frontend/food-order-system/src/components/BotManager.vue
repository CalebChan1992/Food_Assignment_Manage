<script setup lang="ts">
defineProps<{
  bots: Array<{
    id: string;
    status: string;
    current_order: number | null;
  }>;
}>();

const emit = defineEmits(['addBot', 'removeBot']);

const addBot = () => {
  emit('addBot');
};

const removeBot = () => {
  emit('removeBot');
};
</script>

<template>
  <div class="bot-manager">
    <h2>Bot Manager</h2>
    <div class="bot-controls">
      <button @click="addBot" class="bot-button add-bot">+ Bot</button>
      <button @click="removeBot" class="bot-button remove-bot" :disabled="bots.length === 0">- Bot</button>
    </div>
    <div class="bot-count">
      Total Bots: {{ bots.length }}
    </div>
    <div class="bots-container">
      <div v-for="bot in bots" :key="bot.id" class="bot-card" :class="{ 'bot-idle': bot.status === 'IDLE', 'bot-processing': bot.status === 'PROCESSING' }">
        <div class="bot-status">
          Status: {{ bot.status }}
        </div>
        <div v-if="bot.current_order" class="bot-order">
          Processing Order #{{ bot.current_order }}
        </div>
      </div>
      <div v-if="bots.length === 0" class="no-bots">
        No bots available
      </div>
    </div>
  </div>
</template>

<style scoped>
.bot-manager {
  margin-bottom: 2rem;
  position: relative;
}

.bot-manager h2 {
  color: var(--primary);
  font-size: 1.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--accent);
  display: inline-block;
}

.bot-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.bot-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 30px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.bot-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 5px;
  height: 5px;
  background: rgba(255, 255, 255, 0.5);
  opacity: 0;
  border-radius: 100%;
  transform: scale(1, 1) translate(-50%);
  transform-origin: 50% 50%;
}

.bot-button:active::after {
  animation: ripple 0.6s ease-out;
}

@keyframes ripple {
  0% {
    transform: scale(0, 0);
    opacity: 0.5;
  }
  100% {
    transform: scale(20, 20);
    opacity: 0;
  }
}

.add-bot {
  background-color: var(--success);
  color: white;
}

.add-bot:hover {
  background-color: #219653;
  transform: translateY(-2px);
}

.remove-bot {
  background-color: var(--primary);
  color: white;
}

.remove-bot:hover {
  background-color: #E55A35;
  transform: translateY(-2px);
}

.remove-bot:disabled {
  background-color: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.bot-count {
  margin-bottom: 1.5rem;
  font-weight: bold;
  font-size: 1.1rem;
  color: var(--text-color);
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.8rem 1rem;
  border-radius: 8px;
  display: inline-block;
}

.bots-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.2rem;
}

.bot-card {
  border: none;
  border-radius: 12px;
  padding: 1.2rem;
  width: 100%;
  max-width: 300px;
  background-color: var(--card-bg);
  box-shadow: var(--card-shadow);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  animation: slideIn 0.3s ease-out;
  color: var(--text-color);
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.bot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.bot-idle {
  border-left: 5px solid var(--success);
}

.bot-idle .bot-status::before {
  background-color: var(--success);
}

.bot-processing {
  border-left: 5px solid var(--accent);
  background-color: rgba(255, 210, 63, 0.1);
}

.bot-processing .bot-status::before {
  background-color: var(--accent);
}

.bot-status {
  font-weight: bold;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  font-size: 1rem;
}

.bot-status::before {
  content: '';
  display: inline-block;
  width: 10px;
  height: 10px;
  margin-right: 8px;
  border-radius: 50%;
}

.bot-order {
  font-size: 0.9rem;
  color: var(--text-color);
  padding: 0.5rem;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 6px;
}

.no-bots {
  font-style: italic;
  color: var(--text-color);
  opacity: 0.6;
  padding: 2rem;
  text-align: center;
  background-color: var(--card-bg);
  border-radius: 8px;
  width: 100%;
  border: 1px dashed var(--border-color);
}
</style>
