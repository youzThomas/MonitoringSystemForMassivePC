<script setup lang="ts">
import { useVeyonStore } from '@/stores/veyon'
import ScreenshotGallery from '@/components/ScreenshotGallery.vue'

const veyon = useVeyonStore()
</script>

<template>
  <main>
    <h1>Veyon Controller</h1>
    
    <div v-if="!veyon.isConnected">
      <button @click="veyon.connect">Connect</button>
    </div>
    
    <div v-else>
      <div v-if="veyon.error" class="error">{{ veyon.error }}</div>
      
      <div class="controls">
        <button @click="veyon.capture">Capture Screen</button>
        <button @click="veyon.lock">Lock Screens</button>
      </div>
      
      <ScreenshotGallery :screenshots="veyon.screenshots" />
    </div>
  </main>
</template>

<style scoped>
.error {
  color: red;
  margin: 1rem 0;
}
.controls {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}
</style>