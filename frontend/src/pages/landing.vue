<script setup>
import { 
    BriefcaseIcon, UsersIcon, BuildingOffice2Icon, 
    ChartBarIcon, BeakerIcon, UserCircleIcon, 
    ShareIcon, GlobeAltIcon, AtSymbolIcon 
} from '@heroicons/vue/24/outline'

import { useRouter } from 'vue-router';

const navLinks = ['Features', 'Solutions', 'Pricing', 'Resources'];
const router = useRouter()

const stats = [
    { label: 'Active Doctors', value: '500+', growth: '12%', icon: BriefcaseIcon },
    { label: 'Happy Patients', value: '10k+', growth: '25%', icon: UsersIcon },
    { label: 'Hospitals Joined', value: '120+', growth: '8%', icon: BuildingOffice2Icon }
]

const features = [
    {
        title: 'Admin Dashboard',
        description: 'Complete oversight of hospital resources, staffing, and real-time billing analytics.',
        icon: ChartBarIcon,
        list: ['Revenue Analytics', 'Staff Management', 'Resource Tracking']
    },
    {
        title: 'Doctor Portal',
        description: 'Manage electronic health records (EHR), daily consultation schedules, and patient history.',
        icon: BeakerIcon,
        list: ['Digital Prescriptions', 'EHR Management', 'Daily Rounds Planner']
    },
    {
        title: 'Patient Experience',
        description: 'Easy online appointment booking, digital prescriptions, and 24/7 access to medical records.',
        icon: UserCircleIcon,
        list: ['Instant Booking', 'Health Tracking', 'Digital Health Records']
    }
]

const footerLinks = {
    'Product': ['EHR Management', 'Billing Software', 'Telemedicine', 'Pharmacy Hub'],
    'Company': ['About Us', 'Careers', 'Press Kit', 'Contact'],
    'Support': ['Help Center', 'Security', 'API Documentation', 'System Status']
}
</script>

<template>
    <div class="landing-page">
        <header class="navbar-wrapper">
            <nav class="navbar">
                <div class="logo-area">
                    <div class="logo-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                            <path d="M3 12h3l3-9 4 18 3-9h5" />
                        </svg>
                    </div>
                    <span class="logo-text">Medi_Care</span>
                </div>

                <div class="nav-links">
                    <a v-for="link in navLinks" :key="link" href="#" class="nav-link">{{ link }}</a>
                </div>

                <div class="nav-actions">
                    <button @click="router.push('/auth/login')" class="btn btn-primary">Get Started</button>
                </div>
            </nav>
        </header>

        <section class="hero-section">
            <div class="hero-content">
                <span class="badge">Next Gen Healthcare</span>
                <h1 class="hero-title">
                    Streamline Your <br />
                    <span class="text-blue">Hospital</span> Operations
                </h1>
                <p class="hero-description">
                    The all-in-one healthcare SaaS for modern hospitals. Manage appointments,
                    patient records, and staff schedules in one professional platform.
                </p>
                <div class="hero-btns">
                    <button @click="router.push('/auth/login')" class="btn btn-primary btn-lg">Book Appointment</button>
                    <button class="btn btn-outline btn-lg">Watch Demo</button>
                </div>
            </div>

            <div class="hero-image-container">
                <div class="image-wrapper">
                    <img src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&q=80&w=800" alt="Hospital" />
                </div>
                <div class="floating-card">
                    <div class="avatar-group">
                        <div v-for="i in 3" :key="i" class="avatar">
                            <img :src="`https://i.pravatar.cc/100?img=${i + 10}`" alt="Doctor" />
                        </div>
                    </div>
                    <div>
                        <h4>Top Rated Professionals</h4>
                        <p>Available 24/7</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="stats-section">
            <div class="stats-grid">
                <div v-for="stat in stats" :key="stat.label" class="stat-card">
                    <component :is="stat.icon" class="stat-icon" />
                    <p class="stat-label">{{ stat.label }}</p>
                    <div class="stat-value-wrap">
                        <h3 class="stat-value">{{ stat.value }}</h3>
                        <span class="stat-growth">↑ {{ stat.growth }}</span>
                    </div>
                </div>
            </div>
        </section>

        <section class="features-section">
            <div class="section-header">
                <h4>Tailored Solutions</h4>
                <h2>One Platform, Every Professional</h2>
            </div>
            <div class="features-grid">
                <div v-for="feature in features" :key="feature.title" class="feature-card">
                    <div class="feature-icon-box">
                        <component :is="feature.icon" class="feature-icon" />
                    </div>
                    <h3>{{ feature.title }}</h3>
                    <p>{{ feature.description }}</p>
                    <ul class="feature-list">
                        <li v-for="item in feature.list" :key="item">
                            <div class="check-icon">✓</div>
                            <span>{{ item }}</span>
                        </li>
                    </ul>
                </div>
            </div>
        </section>

        <section class="cta-section">
            <div class="cta-card">
                <h2>Ready to transform your medical facility?</h2>
                <p>Join 120+ leading hospitals. Start your 30-day free trial today.</p>
                <div class="cta-btns">
                    <button class="btn btn-white">Get Started Now</button>
                    <button class="btn btn-ghost">Talk to Sales</button>
                </div>
            </div>
        </section>

        <footer class="main-footer">
            <div class="footer-grid">
                <div class="footer-brand">
                    <div class="logo-area">
                        <div class="logo-icon small">M</div>
                        <span class="logo-text">Medi_Care</span>
                    </div>
                    <p>Leading provider of healthcare management solutions.</p>
                    <div class="social-links">
                        <ShareIcon class="social-icon" />
                        <GlobeAltIcon class="social-icon" />
                        <AtSymbolIcon class="social-icon" />
                    </div>
                </div>
                <div v-for="(links, title) in footerLinks" :key="title">
                    <h4 class="footer-title">{{ title }}</h4>
                    <ul class="footer-links">
                        <li v-for="link in links" :key="link"><a href="#">{{ link }}</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 Medi_Care SaaS Inc.</p>
                <div class="legal-links">
                    <a href="#">Privacy</a>
                    <a href="#">Terms</a>
                </div>
            </div>
        </footer>
    </div>
</template>

<style src="../styles/landing.css" scoped></style>