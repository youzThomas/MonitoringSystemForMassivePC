<template>
  <div class="reservation-system">
    <!-- Asset Info Header -->
    <div class="asset-info">
      <div>资产编号: 15011085</div>
      <div>
        设备名称:
        <input class="device-input" v-model="deviceId" placeholder="请输入设备名称" />
      </div>
      <div>设备类别: 通用</div>
      <div>领用单位: 科研平台管理服务中心</div>
      <div>校区: 东莞</div>
    </div>

    <!-- Calendar Table -->
    <div class="calendar-container">
      <div class="calendar-header">
        <button class="nav-btn">&#8592;</button>
        <button class="today-btn">今天</button>
        <span class="calendar-title">2025年6月23日 - 29日</span>
        <button class="view-btn">周</button>
        <button class="view-btn">日</button>
      </div>
      <table class="calendar-table">
        <thead>
          <tr>
            <th>全天</th>
            <th>6/23周一</th>
            <th>6/24周二</th>
            <th>6/25周三</th>
            <th>6/26周四</th>
            <th>6/27周五</th>
            <th>6/28周六</th>
            <th>6/29周日</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="hour in 17" :key="hour">
            <td>{{ hour - 1 }}时</td>
            <td v-for="day in 7" :key="day" :class="{ 'highlight': day === 5 }"></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Reservation Input -->
    <div class="reservation-input">
      <label>预约时段</label>
      <input class="input" v-model="start" type="datetime-local" placeholder="开始时间" />
      <input class="input" v-model="end" type="datetime-local" placeholder="结束时间" />
      <input class="input" v-model="credential" type="text" placeholder="预约人 (工号/姓名)" />
      <button class="reserve-btn" @click="submit">我要预约</button>
    </div>
    <p v-if="success" class="success-msg">预约成功！</p>
    <p v-if="error" class="error-msg">预约失败！</p>

    <!-- Reserved Slots Table -->
    <div class="reserved-slots">
      <div class="reserved-title">当天已被预约时段</div>
      <table class="reserved-table">
        <thead>
          <tr>
            <th>编号</th>
            <th>字母工号</th>
            <th>姓名</th>
            <th>开始时间</th>
            <th>结束时间</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>76057</td>
            <td>20230420191</td>
            <td>张三</td>
            <td>2025-06-13 12:30:00</td>
            <td>2025-06-13 14:30:00</td>
          </tr>
          <tr>
            <td>64154</td>
            <td>20240120024</td>
            <td>李四</td>
            <td>2025-06-13 16:00:00</td>
            <td>2025-06-13 18:00:00</td>
          </tr>
        </tbody>
      </table>
    </div>
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
    error.value = true
  }
}
</script>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}
.reservation-system {
  min-height: 100vh;
  width: 100vw;
  box-sizing: border-box;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  background: #fafbfc;
  padding: 32px 0 32px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
.asset-info {
  background: #f5f7fa;
  padding: 16px 24px;
  border-radius: 8px;
  margin-bottom: 24px;
  font-size: 15px;
  color: #333;
  line-height: 1.8;
  width: 90vw;
  max-width: 1200px;
  box-sizing: border-box;
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}
.device-input {
  padding: 4px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  margin-left: 8px;
  min-width: 180px;
}
.calendar-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px #0001;
  padding: 24px;
  margin-bottom: 24px;
  width: 90vw;
  max-width: 1200px;
  box-sizing: border-box;
}
.calendar-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}
.calendar-title {
  flex: 1;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
}
.nav-btn, .today-btn, .view-btn {
  background: #f0f1f3;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  margin-right: 8px;
  cursor: pointer;
}
.calendar-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
}
.calendar-table th, .calendar-table td {
  border: 1px solid #e5e7eb;
  text-align: center;
  padding: 6px 0;
  min-width: 60px;
}
.calendar-table th {
  background: #f5f7fa;
  font-weight: 500;
}
.calendar-table .highlight {
  background: #fffbe6;
}
.reservation-input {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 24px 0 16px 0;
  width: 90vw;
  max-width: 1200px;
  box-sizing: border-box;
}
.input {
  flex: 1;
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #f9fafb;
  min-width: 180px;
}
.reserve-btn {
  background: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 20px;
  font-size: 15px;
  cursor: pointer;
}
.success-msg {
  color: #16a34a;
  margin: 0 0 10px 0;
  font-size: 15px;
}
.error-msg {
  color: #dc2626;
  margin: 0 0 10px 0;
  font-size: 15px;
}
.reserved-slots {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px #0001;
  padding: 20px 24px;
  margin-top: 16px;
  width: 90vw;
  max-width: 1200px;
  box-sizing: border-box;
}
.reserved-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
}
.reserved-table {
  width: 100%;
  border-collapse: collapse;
}
.reserved-table th, .reserved-table td {
  border: 1px solid #e5e7eb;
  padding: 6px 10px;
  text-align: center;
}
.reserved-table th {
  background: #f5f7fa;
}
</style>