<template>
  <div class="p-8 max-w-md mx-auto">
    <h1 class="text-2xl font-bold mb-4">Set Reservation</h1>
    <form @submit.prevent="submitReservation" class="space-y-4">
      <div>
        <label>Start Time:</label>
        <input v-model="start" type="datetime-local" class="border p-2 w-full" />
      </div>
      <div>
        <label>End Time:</label>
        <input v-model="end" type="datetime-local" class="border p-2 w-full" />
      </div>
      <button class="bg-blue-500 text-white px-4 py-2 rounded" type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const start = ref('')
const end = ref('')

const submitReservation = async () => {
  const res = await fetch('http://localhost:5000/set-reservation', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      start_time: start.value,
      end_time: end.value
    })
  })

  const json = await res.json()
  alert(json.status === 'saved' ? 'Reservation set successfully!' : 'Failed to save reservation.')
}
</script>
