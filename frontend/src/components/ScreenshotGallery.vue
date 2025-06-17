<script setup lang="ts">
defineProps<{
  screenshots: string[]
}>()
</script>

<template>
  <div class="gallery">
    <div v-for="(screenshot, index) in screenshots" :key="index" class="screenshot">
      <img :src="screenshot" :alt="`Screenshot ${index + 1}`">
      <span>Capture #{{ index + 1 }}</span>
    </div>
  </div>
</template>

<style scoped>
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.screenshot {
  border: 1px solid #ddd;
  padding: 0.5rem;
}
img {
  width: 100%;
  height: auto;
}
</style>