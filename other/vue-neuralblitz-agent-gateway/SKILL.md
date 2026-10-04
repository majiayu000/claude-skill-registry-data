---
name: vue
description: Vue.js progressive JavaScript framework for building user interfaces
category: web-development
difficulty: intermediate
tags: [frontend, javascript, framework, component-based]
author: Vue.js Team
version: 3.4
last_updated: 2024-01-15
---

# Vue.js

## What I Do

I am Vue.js, a progressive JavaScript framework for building user interfaces. I combine declarative rendering with reactive data binding to create interactive web applications. My core philosophy centers on being incrementally adoptable - you can start using just my template syntax and gradually incorporate more advanced features as needed. I provide a reactive system that automatically tracks dependencies and updates the DOM when your data changes, eliminating the need for manual DOM manipulation. My Single File Components (SFCs) with `.vue` extension allow you to encapsulate template, logic, and styles in a single, maintainable file. I offer the Composition API for flexible code organization, built-in state management through Pinia, and seamless integration with the Vue Router for single-page application development. My gentle learning curve makes me an excellent choice for teams transitioning from traditional web development to modern frameworks.

## When to Use Me

- Building interactive single-page applications (SPAs)
- Creating reusable UI component libraries
- Developing progressive web applications (PWAs)
- Adding interactivity to existing server-rendered applications
- Rapid prototyping of user interfaces
- Projects requiring a gentle learning curve
- Applications needing fine-grained reactivity
- Teams transitioning from vanilla JavaScript or jQuery

## Core Concepts

**Reactive Data Binding**: Vue's reactivity system automatically updates the DOM when reactive data changes using `ref()` and `reactive()` declarations.

**Component Architecture**: Build encapsulated, reusable components that manage their own state and expose props for configuration.

**Directives**: Special attributes like `v-if`, `v-for`, `v-bind`, and `v-on` that provide declarative behavior to templates.

**Composition API**: Organize component logic by concern using functions like `setup()`, `computed()`, `watch()`, and lifecycle hooks.

**Single File Components**: `.vue` files containing `<template>`, `<script>`, and `<style>` blocks for complete component encapsulation.

**Pinia State Management**: Modern, type-safe state management with modular stores for centralized application state.

**Vue Router**: Official client-side routing solution for building single-page applications with nested routes and navigation guards.

**Server-Side Rendering**: Nuxt.js framework enables SSR, static site generation, and SEO-friendly Vue applications.

## Code Examples

### Example 1: Reactive Component with Composition API
```javascript
// UserProfile.vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  userId: { type: String, required: true }
})

const user = ref(null)
const isLoading = ref(true)
const error = ref(null)

const fullName = computed(() => 
  user.value ? `${user.value.firstName} ${user.value.lastName}` : ''
)

const fetchUser = async () => {
  try {
    isLoading.value = true
    const response = await fetch(`/api/users/${props.userId}`)
    if (!response.ok) throw new Error('User not found')
    user.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchUser)
</script>

<template>
  <div class="user-profile">
    <div v-if="isLoading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="user-info">
      <h1>{{ fullName }}</h1>
      <p>Email: {{ user.email }}</p>
      <p>Joined: {{ new Date(user.joinDate).toLocaleDateString() }}</p>
    </div>
  </div>
</template>

<style scoped>
.user-profile {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
.error {
  color: #dc3545;
}
</style>
```

### Example 2: Composable for Data Fetching
```javascript
// composables/useFetch.js
import { ref } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const error = ref(null)
  const loading = ref(false)

  const execute = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await fetch(url)
      if (!response.ok) throw new Error(`HTTP error ${response.status}`)
      data.value = await response.json()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { data, error, loading, execute }
}

// Usage in component
// const { data, error, loading, execute } = useFetch('/api/products')
```

### Example 3: Pinia Store for Cart Management
```javascript
// stores/cart.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const promoCode = ref('')
  const discount = ref(0)

  const totalItems = computed(() => 
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const subtotal = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )

  const total = computed(() => subtotal.value - discount.value)

  function addItem(product, quantity = 1) {
    const existing = items.value.find(i => i.id === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      items.value.push({ ...product, quantity })
    }
  }

  function removeItem(productId) {
    items.value = items.value.filter(item => item.id !== productId)
  }

  function applyPromo(code) {
    if (code === 'SAVE20') discount.value = subtotal.value * 0.2
  }

  function clearCart() {
    items.value = []
    promoCode.value = ''
    discount.value = 0
  }

  return { 
    items, promoCode, discount, totalItems, 
    subtotal, total, addItem, removeItem, 
    applyPromo, clearCart 
  }
})
```

### Example 4: Vue Router with Navigation Guards
```javascript
// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/Admin.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Home', query: { redirect: to.fullPath } })
  } else if (to.meta.role && authStore.userRole !== to.meta.role) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router
```

### Example 5: Custom Directive for Input Validation
```javascript
// directives/emailValidator.js
export default {
  mounted(el, binding) {
    const validateEmail = (value) => {
      const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      const isValid = regex.test(value)
      el.classList.toggle('valid', isValid)
      el.classList.toggle('invalid', !isValid)
      return isValid
    }

    const onInput = () => validateEmail(el.value)
    
    el.addEventListener('input', onInput)
    el.addEventListener('blur', () => validateEmail(el.value))
    
    if (binding.value) {
      el.value = binding.value
      validateEmail(el.value)
    }
  },
  updated(el, binding) {
    el.value = binding.value
    el.classList.remove('valid', 'invalid')
  }
}

// Usage in template: <input v-email-validator="user.email">
```

## Best Practices

- Use `<script setup>` syntax for cleaner, more concise components
- Keep components small and focused on a single responsibility
- Use Pinia for state management instead of Vuex (deprecated)
- Define PropTypes with `defineProps()` for type safety and documentation
- Extract reusable logic into composables for DRY code
- Use async components with `defineAsyncComponent()` for code splitting
- Implement proper error boundaries with `errorCaptured()` hook
- Follow consistent naming conventions: PascalCase for components, kebab-case for templates
- Use Vue DevTools for debugging and performance profiling
- Consider Nuxt.js for SSR/SSG and improved SEO

## Core Competencies

- Declarative template syntax with reactive data binding
- Composition API for flexible component logic organization
- Single File Components for encapsulated, maintainable code
- Pinia state management for centralized application state
- Vue Router for client-side navigation and routing
- Transition and animation system for smooth UI changes
- Provide/inject for cross-component communication
- Custom directives for reusable DOM behaviors
- Server-side rendering capabilities with Nuxt.js
- Vue DevTools for debugging and performance monitoring
