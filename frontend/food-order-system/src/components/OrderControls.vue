<script setup lang="ts">
const emit = defineEmits(['createNormalOrder', 'createVipOrder']);

const createNormalOrder = () => {
  emit('createNormalOrder');
};

const createVipOrder = () => {
  emit('createVipOrder');
};
</script>

<template>
  <div class="order-controls">
    <h2>Create New Order</h2>
    <div class="controls">
      <button @click="createNormalOrder" class="order-button normal-order">
        <span class="icon">🍔</span>
        <span class="text">New Normal Order</span>
      </button>
      <button @click="createVipOrder" class="order-button vip-order">
        <span class="icon">👑</span>
        <span class="text">New VIP Order</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.order-controls {
  margin-bottom: 3rem;
  position: relative;
}

.order-controls h2 {
  color: var(--primary);
  font-size: 1.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--accent);
  display: inline-block;
}

.controls {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.order-button {
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  min-width: 220px;
  position: relative;
  overflow: hidden;
}

.order-button::after {
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

.order-button:active::after {
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

.order-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

.order-button:active {
  transform: translateY(1px);
}

.icon {
  font-size: 1.5rem;
  margin-right: 0.8rem;
}

.normal-order {
  background-color: var(--primary);
  color: white;
}

.normal-order:hover {
  background-color: #E55A35;
}

.vip-order {
  background-color: var(--accent);
  color: var(--dark);
}

.vip-order:hover {
  background-color: #FFB800;
}
</style>
