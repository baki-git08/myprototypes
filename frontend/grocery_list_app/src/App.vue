<script setup>
import { computed, onMounted, ref } from 'vue'

const API_BASE_URL = (import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

const addName = ref('')
const addPrice = ref('')
const addSubmitting = ref(false)
const addError = ref('')
const addSuccess = ref('')

const list = ref([])
const listLoading = ref(false)
const listError = ref('')

const lookupId = ref('')
const lookupLoading = ref(false)
const lookupError = ref('')
const lookupItem = ref(null)

const baseUrlHint = computed(() => {
  const fromEnv = import.meta.env?.VITE_API_BASE_URL
  return fromEnv ? `Using VITE_API_BASE_URL=${fromEnv}` : 'Using default API base URL (set VITE_API_BASE_URL to change)'
})

function normalizeItem(raw) {
  if (!raw || typeof raw !== 'object') return null
  const id = raw.id ?? raw.ID ?? raw.item_id ?? raw.itemId
  const item_name = raw.item_name ?? raw.name ?? raw.itemName
  const price = raw.price
  const is_done = raw.is_done ?? raw.done ?? raw.isDone
  return { ...raw, id, item_name, price, is_done }
}

async function readJsonOrText(res) {
  const ct = res.headers.get('content-type') || ''
  if (ct.includes('application/json')) return await res.json()
  const text = await res.text()
  try {
    return JSON.parse(text)
  } catch {
    return text
  }
}

function extractErrorMessage(payload) {
  if (!payload) return 'Request failed'
  if (typeof payload === 'string') return payload
  if (typeof payload?.detail === 'string') return payload.detail
  if (Array.isArray(payload?.detail)) return payload.detail.map((d) => d?.msg || String(d)).join(', ')
  return 'Request failed'
}

async function refreshList() {
  listLoading.value = true
  listError.value = ''
  try {
    const res = await fetch(`${API_BASE_URL}/itemsList`, {
      headers: { Accept: 'application/json' },
    })
    const payload = await readJsonOrText(res)
    if (!res.ok) throw new Error(extractErrorMessage(payload))

    const arr = Array.isArray(payload) ? payload : Array.from(payload || [])
    list.value = arr.map(normalizeItem).filter(Boolean)
  } catch (e) {
    listError.value = e instanceof Error ? e.message : String(e)
    list.value = []
  } finally {
    listLoading.value = false
  }
}

async function submitAdd() {
  addSubmitting.value = true
  addError.value = ''
  addSuccess.value = ''
  try {
    const item_name = addName.value.trim()
    const price = addPrice.value === '' ? 0 : Number(addPrice.value)
    if (!item_name) {
      addError.value = 'Item name is required.'
      return
    }
    if (!Number.isFinite(price) || price < 0) {
      addError.value = 'Price must be a valid non-negative number.'
      return
    }

    const res = await fetch(`${API_BASE_URL}/addItems`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({ item_name, price }),
    })
    const payload = await readJsonOrText(res)
    if (!res.ok) throw new Error(extractErrorMessage(payload))

    const created = normalizeItem(payload)
    addSuccess.value = created?.id != null ? `Added item #${created.id}.` : 'Added item.'
    addName.value = ''
    addPrice.value = ''
    await refreshList()
  } catch (e) {
    addError.value = e instanceof Error ? e.message : String(e)
  } finally {
    addSubmitting.value = false
  }
}

async function submitLookup() {
  lookupLoading.value = true
  lookupError.value = ''
  lookupItem.value = null
  try {
    const id = Number(lookupId.value)
    if (!Number.isInteger(id) || id <= 0) {
      lookupError.value = 'Please enter a valid positive integer id.'
      return
    }

    const res = await fetch(`${API_BASE_URL}/items/${id}`, {
      headers: { Accept: 'application/json' },
    })
    const payload = await readJsonOrText(res)
    if (!res.ok) throw new Error(extractErrorMessage(payload))

    lookupItem.value = normalizeItem(payload)
  } catch (e) {
    lookupError.value = e instanceof Error ? e.message : String(e)
  } finally {
    lookupLoading.value = false
  }
}

function clearAdd() {
  addName.value = ''
  addPrice.value = ''
  addError.value = ''
  addSuccess.value = ''
}

function clearLookup() {
  lookupId.value = ''
  lookupItem.value = null
  lookupError.value = ''
}

onMounted(async () => {
  await refreshList()
})
</script>

<template>
  <div class="page">
    <header class="header">
      <div>
        <h1 class="title">Grocery List</h1>
        <p class="subtitle">
          Simple UI for your FastAPI endpoints:
          <code>POST /addItems</code>, <code>GET /itemsList</code>, <code>GET /items/{id}</code>.
        </p>
      </div>
      <div class="hint">
        <div class="hintLabel">API</div>
        <div class="hintValue">
          <code>{{ API_BASE_URL }}</code>
        </div>
        <div class="hintSub">{{ baseUrlHint }}</div>
      </div>
    </header>

    <main class="grid">
      <section class="card">
        <h2 class="cardTitle">Add item</h2>

        <form class="form" @submit.prevent="submitAdd">
          <label class="field">
            <span class="fieldLabel">Item name</span>
            <input v-model="addName" class="input" type="text" placeholder="e.g. Milk" autocomplete="off" />
          </label>

          <label class="field">
            <span class="fieldLabel">Price</span>
            <input
              v-model="addPrice"
              class="input"
              type="number"
              inputmode="decimal"
              step="0.01"
              min="0"
              placeholder="0.00"
            />
          </label>

          <div class="row">
            <button class="button primary" type="submit" :disabled="addSubmitting">
              {{ addSubmitting ? 'Adding…' : 'Add' }}
            </button>
            <button class="button" type="button" :disabled="addSubmitting" @click="clearAdd">
              Clear
            </button>
          </div>

          <p v-if="addError" class="msg error">{{ addError }}</p>
          <p v-else-if="addSuccess" class="msg success">{{ addSuccess }}</p>
        </form>
      </section>

      <section class="card">
        <div class="cardHeader">
          <h2 class="cardTitle">Items</h2>
          <button class="button" type="button" :disabled="listLoading" @click="refreshList">
            {{ listLoading ? 'Refreshing…' : 'Refresh' }}
          </button>
        </div>

        <p v-if="listError" class="msg error">{{ listError }}</p>
        <p v-else-if="listLoading" class="msg">Loading…</p>
        <p v-else-if="list.length === 0" class="msg muted">No items yet.</p>

        <ul v-else class="list">
          <li v-for="it in list" :key="it.id ?? `${it.item_name}-${it.price}`" class="listItem">
            <div class="listMain">
              <span class="pill">#{{ it.id }}</span>
              <span class="name">{{ it.item_name }}</span>
            </div>
            <div class="listMeta">
              <span class="price">\${{ Number(it.price ?? 0).toFixed(2) }}</span>
              <span class="done" :class="{ yes: !!it.is_done }">{{ it.is_done ? 'done' : 'todo' }}</span>
            </div>
          </li>
        </ul>
      </section>

      <section class="card">
        <h2 class="cardTitle">Find item by id</h2>
        <form class="form" @submit.prevent="submitLookup">
          <label class="field">
            <span class="fieldLabel">Item id</span>
            <input v-model="lookupId" class="input" type="number" min="1" step="1" placeholder="e.g. 1" />
          </label>

          <div class="row">
            <button class="button primary" type="submit" :disabled="lookupLoading">
              {{ lookupLoading ? 'Fetching…' : 'Fetch' }}
            </button>
            <button
              class="button"
              type="button"
              :disabled="lookupLoading"
              @click="clearLookup"
            >
              Clear
            </button>
          </div>

          <p v-if="lookupError" class="msg error">{{ lookupError }}</p>
        </form>

        <div v-if="lookupItem" class="result">
          <div class="resultRow">
            <span class="resultKey">id</span>
            <span class="resultVal">#{{ lookupItem.id }}</span>
          </div>
          <div class="resultRow">
            <span class="resultKey">name</span>
            <span class="resultVal">{{ lookupItem.item_name }}</span>
          </div>
          <div class="resultRow">
            <span class="resultKey">price</span>
            <span class="resultVal">${{ Number(lookupItem.price ?? 0).toFixed(2) }}</span>
          </div>
          <div class="resultRow">
            <span class="resultKey">status</span>
            <span class="resultVal">{{ lookupItem.is_done ? 'done' : 'todo' }}</span>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="footerNote">
        If the UI can’t reach your API, ensure the backend is running and CORS is configured, then set
        <code>VITE_API_BASE_URL</code> (example: <code>http://127.0.0.1:8000</code>).
      </div>
    </footer>
  </div>
</template>

<style>
:root {
  color-scheme: light dark;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji",
    "Segoe UI Emoji";
  background: radial-gradient(1200px 800px at 20% 0%, rgba(99, 102, 241, 0.12), transparent 60%),
    radial-gradient(900px 600px at 100% 10%, rgba(16, 185, 129, 0.12), transparent 55%),
    linear-gradient(180deg, rgba(0, 0, 0, 0.02), transparent 40%);
  min-height: 100vh;
}

.page {
  max-width: 980px;
  margin: 0 auto;
  padding: 28px 18px 36px;
}

.header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 18px;
}

.title {
  margin: 0;
  font-size: 28px;
  letter-spacing: -0.02em;
}

.subtitle {
  margin: 8px 0 0;
  opacity: 0.85;
  line-height: 1.35;
}

.hint {
  min-width: 260px;
  border: 1px solid rgba(127, 127, 127, 0.25);
  border-radius: 12px;
  padding: 12px 12px 10px;
  background: rgba(255, 255, 255, 0.55);
  backdrop-filter: blur(8px);
}

.hintLabel {
  font-size: 12px;
  font-weight: 650;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  opacity: 0.7;
  margin-bottom: 6px;
}

.hintValue {
  font-size: 13px;
}

.hintSub {
  margin-top: 6px;
  font-size: 12px;
  opacity: 0.7;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.95em;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 14px;
}

@media (min-width: 860px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
  .grid > section:last-child {
    grid-column: 1 / -1;
  }
}

.card {
  border: 1px solid rgba(127, 127, 127, 0.25);
  border-radius: 14px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(10px);
}

.cardHeader {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.cardTitle {
  margin: 0 0 10px;
  font-size: 16px;
  letter-spacing: -0.01em;
}

.form {
  display: grid;
  gap: 10px;
}

.field {
  display: grid;
  gap: 6px;
}

.fieldLabel {
  font-size: 12px;
  font-weight: 600;
  opacity: 0.85;
}

.input {
  width: 100%;
  padding: 10px 10px;
  border-radius: 10px;
  border: 1px solid rgba(127, 127, 127, 0.3);
  background: rgba(255, 255, 255, 0.8);
  outline: none;
}

.input:focus {
  border-color: rgba(99, 102, 241, 0.65);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15);
}

.row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.button {
  border: 1px solid rgba(127, 127, 127, 0.35);
  border-radius: 10px;
  padding: 9px 12px;
  background: rgba(255, 255, 255, 0.85);
  cursor: pointer;
  font-weight: 600;
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button.primary {
  border-color: rgba(99, 102, 241, 0.55);
  background: rgba(99, 102, 241, 0.16);
}

.msg {
  margin: 0;
  font-size: 13px;
  line-height: 1.35;
}

.msg.muted {
  opacity: 0.7;
}

.msg.error {
  color: #b91c1c;
}

.msg.success {
  color: #047857;
}

.list {
  list-style: none;
  padding: 0;
  margin: 10px 0 0;
  display: grid;
  gap: 10px;
}

.listItem {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 10px 10px;
  border: 1px solid rgba(127, 127, 127, 0.22);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
}

.listMain {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.pill {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 999px;
  border: 1px solid rgba(127, 127, 127, 0.25);
  background: rgba(255, 255, 255, 0.8);
}

.name {
  font-weight: 650;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.listMeta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.price {
  font-variant-numeric: tabular-nums;
}

.done {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 999px;
  border: 1px solid rgba(127, 127, 127, 0.25);
  opacity: 0.8;
}

.done.yes {
  border-color: rgba(16, 185, 129, 0.5);
  background: rgba(16, 185, 129, 0.12);
  opacity: 1;
}

.result {
  margin-top: 10px;
  border: 1px solid rgba(127, 127, 127, 0.25);
  border-radius: 12px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.6);
  display: grid;
  gap: 8px;
}

.resultRow {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.resultKey {
  font-size: 12px;
  font-weight: 700;
  opacity: 0.7;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.resultVal {
  font-weight: 650;
}

.footer {
  margin-top: 16px;
  opacity: 0.8;
}

.footerNote {
  font-size: 12px;
  line-height: 1.35;
}
</style>
