<script setup>
import { ref, computed } from "vue"
import { useRouter} from "vue-router";
import { User, Plus } from "lucide-vue-next";
import AddDoctorModal from "./AddDoctorModal.vue";
import { useUserStore } from '../store/userStore';

const addDoctor = ref(false)
const router = useRouter();
const userStore = useUserStore();

const pathSegments = computed(() => router.currentRoute.value.path.split("/").filter(Boolean));
const role = computed(() => pathSegments.value[0]);

const currentPath = computed(() => {
  const segments = pathSegments.value;  
  if (
    segments.length === 0 ||
    ['admin', 'doctor', 'patient'].includes(segments[segments.length - 1])
  ) {
    return "Dashboard";
  }
  return segments[segments.length - 1]
    .replace(/-/g, " ")
    .replace(/\b\w/g, char => char.toUpperCase());
});

const redirectToProfile = () => {
  if(role.value === "doctor") router.push("/doctor/profile");
  else if(role.value === "patient") router.push("/patient/profile");
};
</script>

<template>
  <nav class="top-nav">
    <div class="nav-left">
      <h1 class="nav-breadcrumb">{{ currentPath }}</h1>
    </div>

    <div class="nav-right">
      
      <div class="nav-actions">
        <template v-if="currentPath.toLowerCase() === 'doctors' && role === 'admin'">
          <button @click="addDoctor = true" class="btn btn-primary">
            <Plus :size="18" /> <span>Add Doctor</span>
          </button>
        </template>

        <template v-if="currentPath === 'My Appointments'">
          <button @click="router.push('/patient/doctors')" class="btn btn-primary">
            <Plus :size="18" /> <span>Book Appointment</span>
          </button>
        </template>
      </div>

      <div class="nav-divider"></div>

      <button @click="redirectToProfile" class="user-profile-btn">
        <div class="avatar-circle">
          <User :size="20" />
        </div>
        <div class="user-info">
          <p class="user-name">{{ userStore.user?.name }}</p>
          <p class="user-role">
            <span>{{ userStore.user?.role }}</span>
          </p>
        </div>
      </button>
    </div>

    <AddDoctorModal :isOpen="addDoctor" @close="addDoctor = false" />
  </nav>
</template>

<style src="./styles/navbar.css" scoped></style>