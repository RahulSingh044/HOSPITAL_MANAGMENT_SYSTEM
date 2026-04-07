<script setup>
import { ref, onMounted } from 'vue';
import { Settings, Star, Camera, Check, X, Mail, Phone } from 'lucide-vue-next';
import { getDoctorProfile, updateDoctorProfile } from '../../services/doctor';
import { useToast } from 'vue-toastification';

const toast = useToast();
const isEditing = ref(false);
const loading = ref(false);
const original = ref({});

const doctor = ref({
    name: '', specialization: '', experience: 0, fee: 0,
    clinic: '', education: '', bio: '', languages: '',
    online: false, status: 'Active', rating: 0, reviews: 0, image_url: ''
});


onMounted(async () => {
    await fetchProfile();
});

const fetchProfile = async () => {
    try {
        const res = await getDoctorProfile();
        doctor.value = { ...res };
        original.value = JSON.parse(JSON.stringify(res));
    } catch (e) {
        console.error("Error fetching profile:", e);
    }
};

const saveChanges = async () => {
    loading.value = true;
    try {
        const formData = new FormData();

        Object.keys(doctor.value).forEach(key => {
            formData.append(key, doctor.value[key]);
        });

        const response = await updateDoctorProfile(formData);
        if(response.status !== 200) {
            throw new Error(response.data?.error || "Failed to update profile");
        }
        toast.success("Profile updated successfully!");
    } catch (e) {
        toast.error("Error updating profile");
    } finally {
        loading.value = false;
        isEditing.value = false;
        await fetchProfile();
    }
};

const cancelChanges = () => {
    doctor.value = JSON.parse(JSON.stringify(original.value));
    isEditing.value = false;
    selectedFile.value = null;
};
</script>

<template>
  <div class="executive-container">
    <aside class="hero-pane">
      <div class="glass-card">
        <div class="profile-image-wrapper">
          <img 
            :src="doctor.image_url || `https://ui-avatars.com/api/?name=${doctor.name.replace(' ', '+')}&background=random`" 
            alt="Doctor Profile" 
          />
        </div>
        
        <div class="hero-meta">
          <h1 class="name-heading">{{ doctor.name || 'Loading...' }}</h1>
          <p class="specialty-subtext">{{ doctor.specialization || 'Medical Specialist' }}</p>
          <div class="status-pill" :class="doctor.status?.toLowerCase()">
            <span class="dot"></span> {{ doctor.status }}
          </div>
        </div>

        <div class="quick-stats">
          <div class="stat">
            <span class="stat-label">Patient Rating</span>
            <span class="stat-value">{{ doctor.rating || '0.0' }} <Star :size="14" fill="currentColor" /></span>
          </div>
          <div class="stat">
            <span class="stat-label">Total Reviews</span>
            <span class="stat-value">{{ doctor.reviews || 0 }}</span>
          </div>
        </div>
      </div>
    </aside>

    <main class="data-pane">
      <nav class="sticky-nav">
        <div class="nav-left">
          <span class="app-tag">Registry / <span class="active-tag">Professional Profile</span></span>
        </div>
        <div class="nav-right">
          <button v-if="!isEditing" @click="isEditing = true" class="btn-action-outline">
            <Settings :size="16" /> Edit Profile
          </button>
          <div v-else class="edit-controls">
            <button @click="cancelChanges" class="btn-link">
              <X :size="16" /> Discard
            </button>
            <button @click="saveChanges" class="btn-action-primary" :disabled="loading">
              <Check :size="16" v-if="!loading" />
              {{ loading ? 'Saving...' : 'Publish Changes' }}
            </button>
          </div>
        </div>
      </nav>

      <section class="details-wrapper">
        <div class="data-section">
          <h2 class="data-header">Professional Biography</h2>
          <div class="editable-field full">
            <p v-if="!isEditing" class="bio-text">
              {{ doctor.bio || 'Your professional biography will appear here for patients to read.' }}
            </p>
            <textarea v-else v-model="doctor.bio" class="sleek-textarea" placeholder="Describe your clinical background and patient philosophy..."></textarea>
          </div>
        </div>

        <div class="data-section">
          <h2 class="data-header">Account Identity</h2>
          <div class="data-grid">
            <div class="data-item">
              <label>Professional Email</label>
              <div class="field-container readonly-container">
                <div class="static-value">
                  <Mail :size="14" class="inline-icon" /> {{ doctor.email }}
                </div>
                <p class="helper-text-muted">Contact admin to change login email</p>
              </div>
            </div>

            <div class="data-item">
              <label>Registered Mobile</label>
              <div class="field-container readonly-container">
                <div class="static-value">
                  <Phone :size="14" class="inline-icon" /> {{ doctor.mobile }}
                </div>
                <p class="helper-text-muted">Primary verified contact number</p>
              </div>
            </div>
          </div>
        </div>

        <div class="data-section">
          <h2 class="data-header">Clinical Credentials</h2>
          <div class="data-grid">
            <div class="data-item">
              <label>Education & Training</label>
              <div class="field-container" :class="{ 'editing': isEditing }">
                <input v-model="doctor.education" :readonly="!isEditing" type="text" placeholder="e.g. MD - Harvard Medical" />
              </div>
            </div>

            <div class="data-item">
              <label>Years of Practice</label>
              <div class="field-container inline" :class="{ 'editing': isEditing }">
                <input v-model.number="doctor.experience" :readonly="!isEditing" type="number" />
                <span class="unit-text">Years</span>
              </div>
            </div>

            <div class="data-item">
              <label>Primary Facility / Clinic</label>
              <div class="field-container" :class="{ 'editing': isEditing }">
                <input v-model="doctor.clinic" :readonly="!isEditing" type="text" placeholder="Hospital or Clinic Name" />
              </div>
            </div>

            <div class="data-item">
              <label>Standard Consultation Fee</label>
              <div class="field-container inline" :class="{ 'editing': isEditing }">
                <span class="unit-text">$</span>
                <input v-model.number="doctor.fee" :readonly="!isEditing" type="number" step="0.01" />
              </div>
            </div>
          </div>
        </div>

        <div class="data-section">
          <h2 class="data-header">Reach & Accessibility</h2>
          <div class="data-grid">
            <div class="data-item">
              <label>Spoken Languages</label>
              <div class="field-container" :class="{ 'editing': isEditing }">
                <input v-model="doctor.languages" :readonly="!isEditing" type="text" placeholder="e.g. English, Spanish" />
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style src="../../styles/docProfile.css" scoped>
</style>