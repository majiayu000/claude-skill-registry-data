---
name: vuejs-patterns
description: Vue.js 3 Composition API patterns and best practices. Use when creating Vue components, composables, or any reactive frontend code with Vue.js.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Vue.js 3 Patterns Skill

This skill provides guidance for writing clean, maintainable Vue.js 3 code using the Composition API.

## Component Structure

### Single File Component (SFC) Template
```vue
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useEmployeeStore } from '@/stores/employee'
import type { Employee } from '@/types'

// Props
interface Props {
  employeeId: string
  readonly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false
})

// Emits
const emit = defineEmits<{
  save: [employee: Employee]
  cancel: []
}>()

// Stores
const employeeStore = useEmployeeStore()

// Reactive State
const isLoading = ref(false)
const employee = ref<Employee | null>(null)
const formData = ref({
  name: '',
  email: '',
  department: ''
})

// Computed
const isValid = computed(() => {
  return formData.value.name.length > 0 && formData.value.email.includes('@')
})

const fullName = computed(() => {
  return `${employee.value?.firstName} ${employee.value?.lastName}`
})

// Methods
async function loadEmployee() {
  isLoading.value = true
  try {
    employee.value = await employeeStore.fetchById(props.employeeId)
    formData.value = { ...employee.value }
  } catch (error) {
    console.error('Failed to load employee:', error)
  } finally {
    isLoading.value = false
  }
}

function handleSubmit() {
  if (!isValid.value) return
  emit('save', formData.value as Employee)
}

// Watchers
watch(() => props.employeeId, (newId) => {
  if (newId) loadEmployee()
}, { immediate: true })

// Lifecycle
onMounted(() => {
  loadEmployee()
})

// Expose to parent (if needed)
defineExpose({
  refresh: loadEmployee
})
</script>

<template>
  <div class="employee-form">
    <div v-if="isLoading" class="loading-state">
      <LoadingSpinner />
    </div>

    <form v-else @submit.prevent="handleSubmit">
      <FormInput
        v-model="formData.name"
        label="Name"
        :disabled="readonly"
        required
      />

      <FormInput
        v-model="formData.email"
        type="email"
        label="Email"
        :disabled="readonly"
        required
      />

      <div class="form-actions">
        <BaseButton type="button" variant="secondary" @click="emit('cancel')">
          Cancel
        </BaseButton>
        <BaseButton type="submit" :disabled="!isValid || readonly">
          Save
        </BaseButton>
      </div>
    </form>
  </div>
</template>

<style scoped>
.employee-form {
  @apply max-w-lg mx-auto p-6;
}

.form-actions {
  @apply flex justify-end gap-3 mt-6;
}
</style>
```

## Composables (Reusable Logic)

### useAsync Composable
```typescript
// composables/useAsync.ts
import { ref, type Ref } from 'vue'

interface UseAsyncReturn<T> {
  data: Ref<T | null>
  error: Ref<Error | null>
  isLoading: Ref<boolean>
  execute: (...args: any[]) => Promise<T | null>
}

export function useAsync<T>(
  asyncFn: (...args: any[]) => Promise<T>
): UseAsyncReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>
  const error = ref<Error | null>(null)
  const isLoading = ref(false)

  async function execute(...args: any[]): Promise<T | null> {
    isLoading.value = true
    error.value = null

    try {
      data.value = await asyncFn(...args)
      return data.value
    } catch (e) {
      error.value = e as Error
      return null
    } finally {
      isLoading.value = false
    }
  }

  return { data, error, isLoading, execute }
}

// Usage
const { data: employees, isLoading, execute: fetchEmployees } = useAsync(
  () => api.getEmployees()
)
```

### usePagination Composable
```typescript
// composables/usePagination.ts
import { ref, computed, watch } from 'vue'

interface PaginationOptions {
  initialPage?: number
  initialPerPage?: number
  total?: number
}

export function usePagination(options: PaginationOptions = {}) {
  const currentPage = ref(options.initialPage ?? 1)
  const perPage = ref(options.initialPerPage ?? 15)
  const total = ref(options.total ?? 0)

  const totalPages = computed(() => Math.ceil(total.value / perPage.value))
  const hasNextPage = computed(() => currentPage.value < totalPages.value)
  const hasPrevPage = computed(() => currentPage.value > 1)

  const offset = computed(() => (currentPage.value - 1) * perPage.value)

  function nextPage() {
    if (hasNextPage.value) currentPage.value++
  }

  function prevPage() {
    if (hasPrevPage.value) currentPage.value--
  }

  function goToPage(page: number) {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  function setTotal(newTotal: number) {
    total.value = newTotal
  }

  return {
    currentPage,
    perPage,
    total,
    totalPages,
    hasNextPage,
    hasPrevPage,
    offset,
    nextPage,
    prevPage,
    goToPage,
    setTotal
  }
}
```

### useDebounce Composable
```typescript
// composables/useDebounce.ts
import { ref, watch, type Ref } from 'vue'

export function useDebounce<T>(value: Ref<T>, delay: number = 300): Ref<T> {
  const debouncedValue = ref(value.value) as Ref<T>
  let timeoutId: ReturnType<typeof setTimeout>

  watch(value, (newValue) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      debouncedValue.value = newValue
    }, delay)
  })

  return debouncedValue
}

// Usage
const searchQuery = ref('')
const debouncedSearch = useDebounce(searchQuery, 500)

watch(debouncedSearch, (query) => {
  fetchResults(query)
})
```

### useLocalStorage Composable
```typescript
// composables/useLocalStorage.ts
import { ref, watch, type Ref } from 'vue'

export function useLocalStorage<T>(key: string, defaultValue: T): Ref<T> {
  const stored = localStorage.getItem(key)
  const data = ref<T>(stored ? JSON.parse(stored) : defaultValue) as Ref<T>

  watch(data, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue))
  }, { deep: true })

  return data
}

// Usage
const theme = useLocalStorage('theme', 'light')
const userPreferences = useLocalStorage('preferences', { notifications: true })
```

## State Management with Pinia

### Store Definition
```typescript
// stores/employee.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Employee } from '@/types'
import { employeeApi } from '@/api'

export const useEmployeeStore = defineStore('employee', () => {
  // State
  const employees = ref<Employee[]>([])
  const currentEmployee = ref<Employee | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const activeEmployees = computed(() =>
    employees.value.filter(e => e.status === 'active')
  )

  const employeeCount = computed(() => employees.value.length)

  const getById = computed(() => {
    return (id: string) => employees.value.find(e => e.id === id)
  })

  // Actions
  async function fetchAll() {
    isLoading.value = true
    error.value = null
    try {
      employees.value = await employeeApi.getAll()
    } catch (e) {
      error.value = (e as Error).message
    } finally {
      isLoading.value = false
    }
  }

  async function fetchById(id: string) {
    isLoading.value = true
    try {
      currentEmployee.value = await employeeApi.getById(id)
      return currentEmployee.value
    } catch (e) {
      error.value = (e as Error).message
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function create(data: Partial<Employee>) {
    const newEmployee = await employeeApi.create(data)
    employees.value.push(newEmployee)
    return newEmployee
  }

  async function update(id: string, data: Partial<Employee>) {
    const updated = await employeeApi.update(id, data)
    const index = employees.value.findIndex(e => e.id === id)
    if (index !== -1) {
      employees.value[index] = updated
    }
    return updated
  }

  async function remove(id: string) {
    await employeeApi.delete(id)
    employees.value = employees.value.filter(e => e.id !== id)
  }

  function $reset() {
    employees.value = []
    currentEmployee.value = null
    isLoading.value = false
    error.value = null
  }

  return {
    // State
    employees,
    currentEmployee,
    isLoading,
    error,
    // Getters
    activeEmployees,
    employeeCount,
    getById,
    // Actions
    fetchAll,
    fetchById,
    create,
    update,
    remove,
    $reset
  }
})
```

## Component Patterns

### Base Component (Wrapper Pattern)
```vue
<!-- components/base/BaseButton.vue -->
<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
  disabled: false
})

const classes = computed(() => {
  const base = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2'

  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500',
    secondary: 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500',
    danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
    ghost: 'hover:bg-gray-100 text-gray-700 focus:ring-gray-500'
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  }

  return [
    base,
    variants[props.variant],
    sizes[props.size],
    (props.disabled || props.loading) && 'opacity-50 cursor-not-allowed'
  ]
})
</script>

<template>
  <button
    :class="classes"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <slot />
  </button>
</template>
```

### Renderless Component (Slot Props)
```vue
<!-- components/DataFetcher.vue -->
<script setup lang="ts" generic="T">
import { ref, onMounted, watch } from 'vue'

interface Props {
  url: string
  immediate?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  immediate: true
})

const data = ref<T | null>(null)
const error = ref<Error | null>(null)
const isLoading = ref(false)

async function fetch() {
  isLoading.value = true
  error.value = null
  try {
    const response = await window.fetch(props.url)
    data.value = await response.json()
  } catch (e) {
    error.value = e as Error
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  if (props.immediate) fetch()
})

watch(() => props.url, fetch)
</script>

<template>
  <slot
    :data="data"
    :error="error"
    :is-loading="isLoading"
    :refresh="fetch"
  />
</template>

<!-- Usage -->
<DataFetcher url="/api/employees" v-slot="{ data, isLoading, error, refresh }">
  <div v-if="isLoading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <EmployeeList v-else :employees="data" />
  <button @click="refresh">Refresh</button>
</DataFetcher>
```

### Form Component with v-model
```vue
<!-- components/form/FormInput.vue -->
<script setup lang="ts">
interface Props {
  modelValue: string
  label?: string
  type?: string
  placeholder?: string
  error?: string
  required?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  required: false,
  disabled: false
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const inputId = `input-${Math.random().toString(36).slice(2, 9)}`

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div class="form-group">
    <label
      v-if="label"
      :for="inputId"
      class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <input
      :id="inputId"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :class="[
        'block w-full px-4 py-2.5 rounded-lg border shadow-sm transition-colors',
        error
          ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
          : 'border-gray-300 focus:ring-blue-500 focus:border-blue-500',
        disabled && 'bg-gray-100 cursor-not-allowed'
      ]"
      @input="handleInput"
    />

    <p v-if="error" class="mt-1 text-sm text-red-500">
      {{ error }}
    </p>
  </div>
</template>
```

## TypeScript Integration

### Type Definitions
```typescript
// types/index.ts
export interface Employee {
  id: string
  name: string
  email: string
  department: string
  position: string
  status: 'active' | 'inactive' | 'on_leave'
  hireDate: string
  createdAt: string
  updatedAt: string
}

export interface Attendance {
  id: string
  employeeId: string
  date: string
  checkIn: string | null
  checkOut: string | null
  status: 'present' | 'absent' | 'late' | 'early_leave'
  notes?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  meta: {
    currentPage: number
    lastPage: number
    perPage: number
    total: number
  }
}

// API Response types
export type ApiResponse<T> = {
  success: true
  data: T
} | {
  success: false
  error: string
}
```

### Typed API Client
```typescript
// api/client.ts
import type { Employee, PaginatedResponse, ApiResponse } from '@/types'

const BASE_URL = '/api'

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers
    },
    ...options
  })

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }

  return response.json()
}

export const employeeApi = {
  getAll: () => request<PaginatedResponse<Employee>>('/employees'),

  getById: (id: string) => request<Employee>(`/employees/${id}`),

  create: (data: Partial<Employee>) =>
    request<Employee>('/employees', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  update: (id: string, data: Partial<Employee>) =>
    request<Employee>(`/employees/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

  delete: (id: string) =>
    request<void>(`/employees/${id}`, { method: 'DELETE' })
}
```

## Best Practices

### Component Naming
```
# PascalCase for components
BaseButton.vue
EmployeeCard.vue
DashboardStats.vue

# Kebab-case for template usage
<base-button />
<employee-card />
<dashboard-stats />
```

### Props Best Practices
```typescript
// ✅ Good - Type-safe with defaults
interface Props {
  title: string
  count?: number
  variant?: 'primary' | 'secondary'
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  variant: 'primary'
})

// ❌ Avoid - Runtime validation only
const props = defineProps({
  title: String,
  count: Number
})
```

### Event Naming
```typescript
// ✅ Good - Descriptive event names
const emit = defineEmits<{
  'update:modelValue': [value: string]
  'employee-selected': [employee: Employee]
  'form-submitted': [data: FormData]
}>()

// Usage in template
emit('employee-selected', employee)

// ❌ Avoid - Generic names
emit('change', value)
emit('click', data)
```

### Ref vs Reactive
```typescript
// Use ref for primitives
const count = ref(0)
const name = ref('')
const isLoading = ref(false)

// Use ref for objects you'll reassign
const employee = ref<Employee | null>(null)
employee.value = await fetchEmployee(id)

// Use reactive for objects you'll mutate
const form = reactive({
  name: '',
  email: '',
  department: ''
})
form.name = 'John'
```

### Template Organization
```vue
<template>
  <!-- 1. Loading State -->
  <LoadingSpinner v-if="isLoading" />

  <!-- 2. Error State -->
  <ErrorMessage v-else-if="error" :message="error" />

  <!-- 3. Empty State -->
  <EmptyState v-else-if="!data?.length" />

  <!-- 4. Main Content -->
  <div v-else>
    <!-- Content here -->
  </div>
</template>
```
