<script setup>
import { ref, onMounted } from 'vue';
import { Settings, Star, Camera, Check, X, Mail, Phone } from 'lucide-vue-next';
import { useToast } from 'vue-toastification';
import { getPatientProfile, updatePatientProfile } from '../../services/patient';

const toast = useToast();
const isEditing = ref(false);
const loading = ref(false);
const original = ref({});
const selectedFile = ref(null);

const patient = ref({
  name: '', medical_id: '', age: 0, gender: '',
  mobile: '', email: '', dob: '', address: '',
  blood_type: '', condition: '', image_url: '',
  preferences: '[]'
});

const parsedPreferences = ref([
  { label: 'Appointment Reminders', desc: 'SMS and email reminders 24h before visit.', enabled: true },
  { label: 'Lab Notifications', desc: 'Get notified when test results are ready.', enabled: true },
  { label: 'Health Newsletter', desc: 'Monthly curated health advice.', enabled: false },
]);

onMounted(async () => {
  try {
    const res = await getPatientProfile();
    console.log("Fetched patient profile:", res);
    patient.value = res;
    original.value = JSON.parse(JSON.stringify(res.data));

    if (res.data.preferences) {
      // Simple logic to sync local toggle states with DB string
    }
  } catch (e) {
    console.error("Fetch error:", e);
  }
});

const saveChanges = async () => {
  loading.value = true;
  try {
    const formData = new FormData();
    patient.value.preferences = JSON.stringify(parsedPreferences.value);

    Object.keys(patient.value).forEach(key => {
      formData.append(key, patient.value[key]);
    });

    if (selectedFile.value) formData.append('image', selectedFile.value);

    const res = await updatePatientProfile(formData);

    if (res.status !== 200) throw new Error("Update failed");
    original.value = JSON.parse(JSON.stringify(patient.value));
    isEditing.value = false;
    toast.success("Profile updated successfully");
  } catch (e) {
    toast.error("Failed to update profile. Please try again.");
  } finally {
    loading.value = false;
  }
};

const cancelChanges = () => {
  patient.value = JSON.parse(JSON.stringify(original.value));
  isEditing.value = false;
};

</script>

<template>
  <div class="executive-container">
    <aside class="hero-pane">
      <div class="glass-card">
        <div class="profile-image-wrapper">
          <img
            :src="patient?.image_url || `https://ui-avatars.com/api/?name=${patient.name?.replace(' ', '+')}&background=0ea5e9&color=fff`"
            alt="Patient Profile" />
        </div>

        <div class="hero-meta">
          <h1 class="name-heading">{{ patient.name || 'Loading...' }}</h1>
          <p class="specialty-subtext">ID: {{ patient.medical_id }}</p>
          <div class="status-pill" :class="patient.condition?.toLowerCase().replace(' ', '-')">
            <span class="dot"></span> {{ patient.condition }}
          </div>
        </div>

        <div class="quick-stats">
          <div class="stat">
            <span class="stat-label">Blood Type</span>
            <span class="stat-value text-red-500">{{ patient.blood_type || 'N/A' }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Age</span>
            <span class="stat-value">{{ patient.age || '—' }}</span>
          </div>
        </div>
      </div>
    </aside>

    <main class="data-pane">
      <nav class="sticky-nav">
        <div class="nav-left">
          <span class="app-tag">Patient Portal / <span class="active-tag">Personal Registry</span></span>
        </div>
        <div class="nav-right">
          <button v-if="!isEditing" @click="isEditing = true" class="btn-action-outline">
            <Settings :size="16" /> Edit Profile
          </button>
          <div v-else class="edit-controls">
            <button @click="cancelChanges" class="flex items-center gap-2">
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
          <h2 class="data-header">Account Identity</h2>
          <div class="data-grid">
            <div class="data-item">
              <label>Registered Email</label>
              <div class="field-container readonly-container">
                <div class="static-value">
                  <Mail :size="14" class="inline-icon" /> {{ patient.email }}
                </div>
              </div>
            </div>
            <div class="data-item">
              <label>Mobile Number</label>
              <div class="field-container readonly-container">
                <div class="static-value">
                  <Phone :size="14" class="inline-icon" /> {{ patient.mobile }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="data-section">
          <h2 class="data-header">Personal Details</h2>
          <div class="data-grid">
            <div class="data-item">
              <label>Full Name</label>
              <div class="field-container" :class="{ 'editing': isEditing }">
                <input v-model="patient.name" :readonly="!isEditing" type="text" />
              </div>
            </div>
            <div class="data-item">
              <label>Date of Birth</label>
              <div class="field-container" :class="{ 'editing': isEditing }">
                <input v-model="patient.dob" :readonly="!isEditing" type="date" />
              </div>
            </div>
            <div class="data-item">
              <label>Gender</label>
              <div class="field-container" :class="{ 'editing': isEditing }">
                <select v-if="isEditing" v-model="patient.gender" class="sleek-select">
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
                <input v-else :value="patient.gender.toLocaleUpperCase()" readonly type="text" />
              </div>
            </div>
            <div class="data-item">
              <label>Blood Group</label>
              <div class="field-container" :class="{ 'editing': isEditing }">
                <select v-if="isEditing" v-model="patient.blood_type" class="sleek-select">
                  <option value="" disabled>Select Blood Group</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
                <input v-else :value="patient.blood_type || 'Not Set'" readonly type="text" />
              </div>
            </div>
          </div>
        </div>

        <div class="data-section">
          <h2 class="data-header">Residential Address</h2>
          <div class="editable-field full">
            <p v-if="!isEditing" class="bio-text">{{ patient.address || 'No address provided.' }}</p>
            <textarea v-else v-model="patient.address" class="sleek-textarea"
              placeholder="Enter your full home address..."></textarea>
          </div>
        </div>

        <div class="data-section">
          <h2 class="data-header">Notification Preferences</h2>
          <div class="preference-list">
            <div v-for="(pref, index) in parsedPreferences" :key="index" class="toggle-box mb-4">
              <div class="pref-info">
                <span class="toggle-status" :class="{ 'active-text': pref.enabled }">{{ pref.label }}</span>
                <p class="text-[11px] text-slate-400">{{ pref.desc }}</p>
              </div>
              <input type="checkbox" v-model="pref.enabled" :disabled="!isEditing" class="modern-switch" />
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style src="./styles/profile.css" scoped>
</style>