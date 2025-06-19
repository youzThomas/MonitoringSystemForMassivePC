import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const keyname = import.meta.env.VITE_VEYON_KEYNAME
const keydata = import.meta.env.VITE_VEYON_PRIVATE_KEY

export const useVeyonStore = defineStore('veyon', () => {
  const isConnected = ref(false)
  const screenshots = ref<string[]>([])
  const error = ref<string | null>(null)

  const connect = async () => {
    try {
      await axios.post('http://10.71.0.109:11080/auth', {
        auth_method: "0c69b301-81b4-42d6-8fae-128cdd113314",
        credentials: { keyname: keyname, keydata: keydata }
      })
      isConnected.value = true
    } catch (err) {
      error.value = 'Connection failed'
    }
  }

  const capture = async () => {
    try {
      const response = await axios.get('http://10.71.0.109:11080/screenshot', {
        responseType: 'blob'
      })
      screenshots.value.push(URL.createObjectURL(response.data))
    } catch (err) {
      error.value = 'Capture failed'
    }
  }

  const lock = async () => {
    try {
      await axios.post('http://10.71.0.109:11080/lock-screens')
    } catch (err) {
      error.value = 'Lock failed'
    }
  }

  return { isConnected, screenshots, error, connect, capture, lock }
})