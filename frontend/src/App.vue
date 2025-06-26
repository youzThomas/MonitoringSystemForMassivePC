<template>
  <div class="p-6 max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-4">设备共享预约平台</h2>

    <form @submit.prevent="submit" class="space-y-4">
      <div>
        <label class="block">设备名称:</label>
        <input v-model="deviceId" class="border p-2 w-full" placeholder="e.g. pc-001" />
      </div>
      <div>
        <label class="block">开始时间:</label>
        <input v-model="start" type="datetime-local" class="border p-2 w-full" />
      </div>
      <div>
        <label class="block">结束时间:</label>
        <input v-model="end" type="datetime-local" class="border p-2 w-full" />
      </div>
      <div>
        <label class="block">预约人:</label>
        <input v-model="credential" class="border p-2 w-full" type="text" placeholder="Enter credential (e.g. abc123)" />
      </div>

      <button class="bg-blue-600 text-white px-4 py-2 rounded" type="submit">
        提交预约
      </button>
    </form>

    <p v-if="success" class="mt-4 text-green-600">✅ 预约成功！</p>
    <p v-if="error" class="mt-4 text-red-600">❌ 预约失败！</p>
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
