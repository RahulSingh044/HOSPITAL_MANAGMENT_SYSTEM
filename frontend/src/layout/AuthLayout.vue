<template>
    <div class="min-h-screen flex items-center justify-center">
        <Suspense fallback="Loading...">
            <router-view />
        </Suspense>
    </div>
</template>