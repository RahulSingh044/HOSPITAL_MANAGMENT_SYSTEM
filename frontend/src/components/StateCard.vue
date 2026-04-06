<script setup>
import { TrendingUp, TrendingDown } from 'lucide-vue-next';

// We'll use 'type' to determine the icon's color theme
defineProps(['title', 'value', 'trend', 'isUp', 'icon', 'type']);
</script>

<template>
  <div class="stat-card">
    <div class="stat-header">
      <div :class="['stat-icon-box', `is-${type}`]">
        <component :is="icon" :size="20" />
      </div>
      
      <div :class="['stat-trend', isUp ? 'is-up' : 'is-down']">
        <component :is="isUp ? TrendingUp : TrendingDown" :size="14" />
        <span>{{ trend }}</span>
      </div>
    </div>

    <div class="stat-body">
      <p class="stat-label">{{ title }}</p>
      <h3 class="stat-value">{{ value }}</h3>
    </div>
  </div>
</template>

<style>
.stat-card {
  background-color: #ffffff;
  padding: 24px;
  border-radius: 20px;
  border: 1px solid #f1f5f9; /* slate-100 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.04);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

/* --- Icon Container --- */
.stat-icon-box {
  padding: 10px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Color Themes */
.stat-icon-box.is-blue {
  background-color: #eff6ff; /* blue-50 */
  color: #2563eb; /* blue-600 */
}

.stat-icon-box.is-indigo {
  background-color: #eef2ff; /* indigo-50 */
  color: #4f46e5; /* indigo-600 */
}

.stat-icon-box.is-orange {
  background-color: #fff7ed; /* orange-50 */
  color: #ea580c; /* orange-600 */
}

/* --- Trend Badge --- */
.stat-trend {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 700;
}

.stat-trend.is-up {
  color: #10b981; /* emerald-500 */
}

.stat-trend.is-down {
  color: #ef4444; /* red-500 */
}

/* --- Text Content --- */
.stat-label {
  color: #94a3b8; /* slate-400 */
  font-size: 14px;
  font-weight: 500;
  margin: 0;
}

.stat-value {
  color: #1e293b; /* slate-800 */
  font-size: 24px;
  font-weight: 700;
  margin-top: 4px;
  margin-bottom: 0;
}
</style>