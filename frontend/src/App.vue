<script setup>
import { Analytics } from '@vercel/analytics/vue';
</script>
<template>
  <Suspense fallback="Loading...">
    <Analytics />
    <router-view />
  </Suspense>
</template>
