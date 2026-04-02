<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  doctorName: String,
  currentDate: String,
  currentTime: String,
  slots: Array,
  next15Days: Array
});

const emit = defineEmits(['close', 'confirm']);

const selectedDate = ref(null);
const selectedSlot = ref(null);

// Reset selection when modal opens
watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    selectedDate.value = null;
    selectedSlot.value = null;
  }
});

const handleConfirm = () => {
  if (selectedDate.value && selectedSlot.value) {
    emit('confirm', { date: selectedDate.value, time: selectedSlot.value });
  }
};
</script>

<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-backdrop" @click="$emit('close')"></div>

    <div class="modal-content">

      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
        <div>
          <h3 style="font-size: 20px; font-weight: 800; margin: 0; color: #0f172a;">Reschedule Visit</h3>
          <p style="font-size: 14px; color: #64748b; margin: 4px 0 0 0; font-weight: 500;">Dr. {{ doctorName }}</p>
        </div>
        <button @click="$emit('close')"
          style="background: none; border: none; font-size: 18px; color: #94a3b8; cursor: pointer; padding: 4px;">✕</button>
      </div>

      <div class="reschedule-info-box" style="margin-bottom: 24px;">
        <span style="font-size: 18px;">📅</span>
        <p style="font-size: 11px; color: #1d4ed8; font-weight: 600; margin: 0; line-height: 1.5;">
          Current: <span style="font-weight: 900;">{{ currentDate }}</span> at <span style="font-weight: 900;">{{
            currentTime }}</span>.
          Please select a new slot.
        </p>
      </div>

      <div style="margin-bottom: 24px;">
        <p
          style="font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; margin-bottom: 16px;">
          Select New Date</p>
        <div class="no-scrollbar" style="display: flex; gap: 12px; overflow-x: auto; padding-bottom: 8px;">
          <button v-for="date in next15Days" :key="date.fullDate" @click="selectedDate = date.fullDate" :class="[
            'date-pill',
            selectedDate === date.fullDate ? 'date-pill-active' : '',
            date.fullDate === currentDate ? 'date-pill-disabled' : ''
          ]">
            <span style="font-size: 9px; text-transform: uppercase; font-weight: 800; opacity: 0.6;">{{ date.weekday
              }}</span>
            <span style="font-size: 14px; font-weight: 900;">{{ date.dayNum }}</span>
          </button>
        </div>
      </div>

      <div style="margin-bottom: 32px;">
        <p
          style="font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; margin-bottom: 16px;">
          Available Slots</p>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
          <button v-for="time in slots" :key="time" @click="selectedSlot = time" :class="[
            'time-slot',
            selectedSlot === time ? 'time-slot-active' : '',
            (selectedDate === currentDate && time === currentTime) ? 'date-pill-disabled' : ''
          ]">
            {{ time }}
          </button>
        </div>
      </div>

      <div style="display: flex; flex-direction: column; gap: 12px;">
        <button @click="handleConfirm" :disabled="!selectedDate || !selectedSlot" class="btn-confirm">
          Confirm Reschedule
        </button>
        <button @click="$emit('close')"
          style="background: none; border: none; color: #94a3b8; font-size: 12px; font-weight: 700; cursor: pointer; padding: 8px;">
          Nevermind, keep current slot
        </button>
      </div>
    </div>
  </div>
</template>

<style src="./styles/Reschdule.css" scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>