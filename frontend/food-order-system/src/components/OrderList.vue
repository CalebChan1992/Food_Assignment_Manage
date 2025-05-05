<script setup lang="ts">
defineProps<{
  title: string;
  orders: Array<{
    id: number;
    is_vip: boolean;
    status: string;
    timestamp: number;
  }>;
}>();
</script>

<template>
  <div class="order-list">
    <h2>{{ title }}</h2>
    <div class="orders-container">
      <div
        v-for="order in orders"
        :key="order.id"
        class="order-card"
        :class="{
          'vip-order': order.is_vip,
          'processing-order': order.status === 'PROCESSING',
          'pending-order': order.status === 'PENDING',
          'complete-order': order.status === 'COMPLETE'
        }"
      >
        <div class="order-header">
          <span class="order-id">Order #{{ order.id }}</span>
          <span v-if="order.is_vip" class="vip-badge">VIP</span>
        </div>

        <!-- Different display based on order status -->
        <div v-if="order.status === 'PROCESSING'" class="order-details">
          <div class="status-bar-container">
            <div class="status-bar-label">Processing...</div>
            <div class="status-bar">
              <div class="status-bar-progress"></div>
            </div>
          </div>
          <span class="order-time">Started: {{ new Date(order.timestamp * 1000).toLocaleTimeString() }}</span>
        </div>

        <div v-else-if="order.status === 'PENDING'" class="order-details pending-details">
          <span class="order-status">Waiting for bot...</span>
        </div>

        <div v-else class="order-details">
          <span class="order-status">Status: {{ order.status }}</span>
          <span class="order-time">Time: {{ new Date(order.timestamp * 1000).toLocaleTimeString() }}</span>
        </div>
      </div>
      <div v-if="orders.length === 0" class="no-orders">
        No orders
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-list {
  margin-bottom: 2rem;
  position: relative;
}

.order-list h2 {
  color: var(--primary);
  font-size: 1.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--accent);
  display: inline-block;
}

.orders-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  width: 100%;
}

.order-card {
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

.order-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.order-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background-color: var(--primary);
}

.vip-order {
  border: none;
  background-color: rgba(255, 210, 63, 0.1);
}

.vip-order::before {
  background-color: var(--accent);
}

.processing-order {
  border-left: 4px solid var(--accent);
}

.processing-order::before {
  background-color: var(--accent);
}

.pending-order {
  opacity: 0.85;
}

.complete-order::before {
  background-color: var(--success);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px dashed var(--border-color);
}

.order-id {
  font-weight: bold;
  font-size: 1.1rem;
  color: var(--dark);
}

.vip-badge {
  background-color: var(--accent);
  color: var(--dark);
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.order-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.order-status, .order-time {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
}

.order-status::before, .order-time::before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 8px;
  border-radius: 50%;
}

.order-status::before {
  background-color: var(--pending);
}

.order-time::before {
  background-color: var(--dark);
}

.no-orders {
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

/* Status bar styling */
.status-bar-container {
  margin-bottom: 0.8rem;
  width: 100%;
}

.status-bar-label {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
  color: var(--accent);
  display: flex;
  align-items: center;
}

.status-bar-label::before {
  content: '⏳';
  margin-right: 5px;
}

.status-bar {
  height: 8px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.status-bar-progress {
  height: 100%;
  background-color: var(--accent);
  border-radius: 4px;
  width: 0%;
  animation: progress 10s linear forwards;
}

@keyframes progress {
  0% { width: 0%; }
  100% { width: 100%; }
}

.pending-details {
  opacity: 0.7;
  font-style: italic;
}
</style>
