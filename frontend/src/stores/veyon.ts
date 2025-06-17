import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useVeyonStore = defineStore('veyon', () => {
  const isConnected = ref(false)
  const screenshots = ref<string[]>([])
  const error = ref<string | null>(null)

  const connect = async () => {
    try {
      await axios.post('http://localhost:8000/auth', {
        auth_method: "0c69b301-81b4-42d6-8fae-128cdd113314",
        credentials: { keyname: "teacher", keydata: "YOUR_KEY" }
      })
      isConnected.value = true
    } catch (err) {
      error.value = 'Connection failed'
    }
  }

  const capture = async () => {
    try {
      const response = await axios.get('http://localhost:8000/screenshot', {
        responseType: 'blob'
      })
      screenshots.value.push(URL.createObjectURL(response.data))
    } catch (err) {
      error.value = 'Capture failed'
    }
  }

  const lock = async () => {
    try {
      await axios.post('http://localhost:8000/lock-screens')
    } catch (err) {
      error.value = 'Lock failed'
    }
  }

  return { isConnected, screenshots, error, connect, capture, lock }
})