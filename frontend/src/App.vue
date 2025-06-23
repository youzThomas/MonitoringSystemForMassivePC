<template>
  <div class="p-6 max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-4">Remote Reservation Panel</h2>

    <form @submit.prevent="submit" class="space-y-4">
      <div>
        <label class="block">Target Device ID:</label>
        <input v-model="deviceId" class="border p-2 w-full" placeholder="e.g. pc-001" />
      </div>
      <div>
        <label class="block">Start Time:</label>
        <input v-model="start" type="datetime-local" class="border p-2 w-full" />
      </div>
      <div>
        <label class="block">End Time:</label>
        <input v-model="end" type="datetime-local" class="border p-2 w-full" />
      </div>
      <div>
        <label class="block">Credential:</label>
        <input v-model="credential" class="border p-2 w-full" type="text" placeholder="Enter credential (e.g. abc123)" />
      </div>

      <button class="bg-blue-600 text-white px-4 py-2 rounded" type="submit">
        Submit Reservation
      </button>
    </form>

    <p v-if="success" class="mt-4 text-green-600">✅ Reservation saved!</p>
    <p v-if="error" class="mt-4 text-red-600">❌ Failed to send reservation.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const deviceId = ref('')
const start = ref('')
const end = ref('')
const credential = ref('')
const success = ref(false)
const error = ref(false)

const submit = async () => {
  success.value = false
  error.value = false

  try {
    const res = await fetch('https://msmp-cloud-api.onrender.com/set-reservation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        device_id: deviceId.value,
        start_time: start.value,
        end_time: end.value,
        credential: credential.value
      })
    })

    const json = await res.json()
    success.value = json.status === 'saved'
    error.value = !success.value
  } catch (e) {
    console.error(e)
    error.value = true
  }
}
</script>
