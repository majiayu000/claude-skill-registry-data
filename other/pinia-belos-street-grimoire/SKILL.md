---
name: pinia
description: Pinia state management for Vue 3. Use defineStore() with Composition API style (setup stores). Covers store definition, state, getters, actions, TypeScript, store composition, SSR, and best practices.
license: MIT
metadata:
  author: github.com/belos-street
  version: "1.0.0"
---

Pinia state management for Vue 3 using Composition API style stores.

### Store Definition
- Defining stores with defineStore() → See [define-store-composition-api](reference/define-store-composition-api.md)
- Choosing between setup stores and options stores → See [setup-vs-options-store](reference/setup-vs-options-store.md)
- Organizing store files and directory structure → See [store-organization](reference/store-organization.md)
- Using store composables in components → See [store-in-components](reference/store-in-components.md)
- Creating reusable store patterns → See [store-composition-patterns](reference/store-composition-patterns.md)

### State
- Mutating state directly vs using actions → See [state-mutation-best-practices](reference/state-mutation-best-practices.md)
- Resetting state to initial values → See [state-reset-pattern](reference/state-reset-pattern.md)
- Using reactive vs ref for state → See [state-reactive-vs-ref](reference/state-reactive-vs-ref.md)
- State persistence with localStorage → See [state-persistence](reference/state-persistence.md)
- Deep reactivity with nested objects → See [state-deep-reactivity](reference/state-deep-reactivity.md)
- State hydration from API → See [state-hydration](reference/state-hydration.md)

### Getters
- Getters not caching computed values → See [getter-computed-caching](reference/getter-computed-caching.md)
- Passing arguments to getters → See [getter-pass-arguments](reference/getter-pass-arguments.md)
- Accessing other store getters → See [getter-cross-store-access](reference/getter-cross-store-access.md)
- Getter performance with expensive operations → See [getter-performance-optimization](reference/getter-performance-optimization.md)

### Actions
- Async actions and error handling → See [action-async-error-handling](reference/action-async-error-handling.md)
- Calling actions from other stores → See [action-cross-store-calls](reference/action-cross-store-calls.md)
- Action composition and reusability → See [action-composition-patterns](reference/action-composition-patterns.md)
- Batch state updates in actions → See [action-batch-updates](reference/action-batch-updates.md)
- Testing actions with mocked dependencies → See [action-testing-strategies](reference/action-testing-strategies.md)

### TypeScript
- Typing store state with interfaces → See [typescript-state-typing](reference/typescript-state-typing.md)
- Typing getters and actions → See [typescript-getters-actions-typing](reference/typescript-getters-actions-typing.md)
- Using Pinia with TypeScript generics → See [typescript-generic-stores](reference/typescript-generic-stores.md)
- Type-safe store composition → See [typescript-store-composition](reference/typescript-store-composition.md)
- Type inference for auto-imported stores → See [typescript-auto-import-types](reference/typescript-auto-import-types.md)

### Store Composition
- Combining multiple stores → See [store-composition](reference/store-composition.md)
- Avoiding circular dependencies between stores → See [store-circular-dependencies](reference/store-circular-dependencies.md)
- Shared state across stores → See [store-shared-state](reference/store-shared-state.md)
- Extracting common store logic → See [store-logic-extraction](reference/store-logic-extraction.md)

### Best Practices
- Store size and performance → See [store-performance-optimization](reference/store-performance-optimization.md)
- When to use Pinia vs provide/inject → See [pinia-vs-provide-inject](reference/pinia-vs-provide-inject.md)
- Testing Pinia stores → See [testing-pinia-stores](reference/testing-pinia-stores.md)
- Migrating from Vuex to Pinia → See [migrating-from-vuex](reference/migrating-from-vuex.md)

## Quick Reference

### Basic Setup Store (Composition API)

```ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  
  function increment() {
    count.value++
  }
  
  function $reset() {
    count.value = 0
  }
  
  return { count, doubleCount, increment, $reset }
})
```

### Using Store in Component

```vue
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
</script>

<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <p>Double: {{ counter.doubleCount }}</p>
    <button @click="counter.increment">Increment</button>
  </div>
</template>
```

### Store with TypeScript

```ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: number
  name: string
  email: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => user.value !== null)
  
  async function login(email: string, password: string) {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })
    user.value = await response.json()
  }
  
  function logout() {
    user.value = null
  }
  
  return { user, isAuthenticated, login, logout }
})
```

### Store Composition

```ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'
import { useCartStore } from './cart'

export const useCheckoutStore = defineStore('checkout', () => {
  const authStore = useAuthStore()
  const cartStore = useCartStore()
  
  const isProcessing = ref(false)
  
  async function checkout() {
    if (!authStore.isAuthenticated) {
      throw new Error('User not authenticated')
    }
    
    isProcessing.value = true
    try {
      await processPayment(cartStore.items)
      cartStore.clear()
    } finally {
      isProcessing.value = false
    }
  }
  
  return { isProcessing, checkout }
})
```

## Key Imports

```ts
// Core
import { defineStore } from 'pinia'
import { createPinia } from 'pinia'

// Vue Composition API (used in setup stores)
import { ref, reactive, computed, watch } from 'vue'

// Store instance
import { storeToRefs } from 'pinia'

// Type utilities
import type { StoreDefinition } from 'pinia'
```

## Installation

```bash
npm install pinia
# or
yarn add pinia
# or
pnpm add pinia
```

## Setup in main.ts

```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.mount('#app')
```
