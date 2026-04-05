<script setup>
import { ref } from 'vue';

const props = defineProps({
  isOpen: Boolean,
  isSubmitting: Boolean
});

const emit = defineEmits(['close', 'submit']);

const rating = ref(5);
const comment = ref('');

const handleSubmit = () => {
  if (!comment.value.trim()) return alert("Please add a comment");
  
  emit('submit', {
    rating: rating.value,
    comment: comment.value
  });

  comment.value = '';
  rating.value = 5;
};
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-card">
          <div class="modal-header">
            <h3>Submit Your Review</h3>
            <button @click="$emit('close')" class="close-btn">&times;</button>
          </div>

          <div class="modal-body">
            <div class="star-rating-input">
              <p class="label-text">How was your experience?</p>
              <div class="stars">
                <span 
                  v-for="star in 5" 
                  :key="star" 
                  @click="rating = star"
                  :class="{ 'star-active': star <= rating }"
                >
                  ★
                </span>
              </div>
            </div>

            <div class="form-group">
              <label class="label-text">Your Comments</label>
              <textarea 
                v-model="comment" 
                placeholder="Tell others about your consultation..."
                rows="4"
                class="modal-textarea"
              ></textarea>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="$emit('close')" class="btn-cancel">Cancel</button>
            <button 
              @click="handleSubmit" 
              :disabled="isSubmitting" 
              class="btn-confirm"
            >
              {{ isSubmitting ? 'Posting...' : 'Post Review' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-card {
  background: white;
  width: 90%;
  max-width: 450px;
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #94a3b8;
  cursor: pointer;
  line-height: 1;
}

.star-rating-input {
  text-align: center;
  margin-bottom: 24px;
}

.label-text {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #475569;
  margin-bottom: 8px;
}

.stars {
  font-size: 36px;
  display: flex;
  justify-content: center;
  gap: 8px;
}

.stars span {
  color: #e2e8f0;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.stars span:hover {
  transform: scale(1.1);
}

.stars span.star-active {
  color: #facc15;
}

.modal-textarea {
  width: 100%;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px;
  font-size: 15px;
  outline: none;
  resize: none;
  transition: border-color 0.2s;
}

.modal-textarea:focus {
  border-color: #2563eb;
}

.modal-footer {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.btn-cancel {
  flex: 1;
  padding: 12px;
  background: #f1f5f9;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  color: #64748b;
  cursor: pointer;
}

.btn-confirm {
  flex: 2;
  padding: 12px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.btn-confirm:disabled {
  opacity: 0.6;
}

/* Animations */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>