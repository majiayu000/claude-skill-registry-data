---
name: status-message-components
description: Implement loading, error, success, and empty state components for Vue 3. Use when creating toast notifications, loading spinners, empty state pages, or status indicators. Mentions "loading state", "empty state", "toast component", "error UI", or "success message".
allowed-tools: Read, Edit, Grep, Glob
---

# Status Message Components

Vue 3 components for loading, error, success, and empty states.

## When to Activate

Use this skill when the user:
- Says "create a loading spinner" or "show loading state"
- Asks "how to display empty state" or "no data UI"
- Mentions "toast notification", "success message", or "error popup"
- Wants to "implement status indicators"

## Component Overview

| Component | Purpose | Location |
|-----------|---------|----------|
| Toast | Success/error/warning messages | [Toast.vue](../../../frontend/src/components/common/Toast.vue) |
| Loading | Loading spinners and overlays | [Loading.vue](../../../frontend/src/components/common/Loading.vue) |
| EmptyState | No data placeholders | Create new |
| StatusBadge | Inline status indicators | Create new |

---

## 1. Toast Notifications

### Usage Patterns

**Via Pinia Store** (recommended):
```javascript
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

// Success
appStore.showToast('操作成功', 'success')

// Error
appStore.showToast('操作失败，请重试', 'error')

// Warning
appStore.showToast('数据质量较低', 'warning', { duration: 5000 })
```

### Component Structure

```vue
<template>
  <Teleport to="body">
    <Transition name="toast">
      <div v-if="visible" :class="['toast', `toast--${type}`]">
        <div class="toast__icon">{{ iconMap[type] }}</div>
        <div class="toast__content">
          <div v-if="title" class="toast__title">{{ title }}</div>
          <div class="toast__message">{{ message }}</div>
        </div>
        <button v-if="closable" class="toast__close" @click="close">×</button>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  message: { type: String, required: true },
  title: { type: String, default: '' },
  type: { type: String, default: 'info' }, // success, error, warning, info
  duration: { type: Number, default: 3000 },
  closable: { type: Boolean, default: true }
})

const iconMap = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ'
}
</script>
```

---

## 2. Loading States

### Inline Loading

```vue
<template>
  <div class="data-section">
    <Loading v-if="isLoading" :visible="true" text="加载图表..." />
    <ChartView v-else :data="chartData" />
  </div>
</template>
```

### Fullscreen Loading

```vue
<template>
  <Loading
    v-if="isRefreshing"
    :visible="true"
    text="正在刷新数据..."
    fullscreen
  />
</template>
```

### Loading Component

```vue
<template>
  <div v-if="visible" :class="['loading', { 'loading--fullscreen': fullscreen }]">
    <div class="loading__backdrop"></div>
    <div class="loading__content">
      <div class="loading__spinner">
        <div class="loading__spinner-ring"></div>
        <div class="loading__spinner-ring"></div>
        <div class="loading__spinner-ring"></div>
      </div>
      <div v-if="text" class="loading__text">{{ text }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  visible: { type: Boolean, default: false },
  text: { type: String, default: '加载中...' },
  fullscreen: { type: Boolean, default: false }
})
</script>
```

---

## 3. Empty States

### Component Template

```vue
<template>
  <div class="empty-state">
    <div class="empty-state__icon">{{ config.icon }}</div>
    <div class="empty-state__title">{{ config.title }}</div>
    <div class="empty-state__description">{{ config.description }}</div>
    <div class="empty-state__actions">
      <button
        v-for="action in config.actions"
        :key="action.text"
        :class="['btn', `btn--${action.type}`]"
        @click="action.handler"
      >
        {{ action.text }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  type: {
    type: String,
    default: 'no-results',
    validator: v => ['no-results', 'no-data', 'error'].includes(v)
  }
})

const configs = {
  'no-results': {
    icon: '🔍',
    title: '未找到匹配数据',
    description: '请调整筛选条件',
    actions: [{ text: '重置筛选', type: 'primary' }]
  },
  'no-data': {
    icon: '📁',
    title: '暂无数据',
    description: '请先上传或刷新数据',
    actions: [
      { text: '上传数据', type: 'primary' },
      { text: '刷新', type: 'secondary' }
    ]
  },
  'error': {
    icon: '⚠️',
    title: '数据加载失败',
    description: '请检查网络连接或刷新重试',
    actions: [{ text: '重试', type: 'primary' }]
  }
}

const config = computed(() => configs[props.type])
</script>
```

### Usage

```vue
<template>
  <div class="dashboard">
    <EmptyState v-if="data.length === 0" type="no-results" @reset-filters="handleReset" />
    <DataTable v-else :data="data" />
  </div>
</template>
```

---

## 4. Status Badges

### Badge Component

```vue
<template>
  <span :class="['badge', `badge--${type}`]">
    <span class="badge__dot"></span>
    <span class="badge__text">{{ text }}</span>
  </span>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    default: 'default',
    validator: v => ['success', 'warning', 'error', 'info', 'default'].includes(v)
  },
  text: { type: String, required: true }
})
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: var(--text-sm);
}

.badge__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.badge--success {
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-600);
}
.badge--success .badge__dot {
  background: var(--success-500);
}

/* ... other badge variants ... */
</style>
```

### Usage

```vue
<StatusBadge type="success" text="优秀" />
<StatusBadge type="warning" text="警告" />
<StatusBadge type="error" text="错误" />
```

---

## State Management Pattern

### Pinia Store for Toast

```javascript
// stores/app.js
export const useAppStore = defineStore('app', {
  state: () => ({
    toasts: []
  }),

  actions: {
    showToast(message, type = 'info', options = {}) {
      const toast = {
        id: Date.now(),
        message,
        type,
        title: options.title,
        duration: options.duration || 3000,
        closable: options.closable !== false
      }

      this.toasts.push(toast)

      // Auto remove after duration
      setTimeout(() => {
        this.removeToast(toast.id)
      }, toast.duration)
    },

    removeToast(id) {
      const index = this.toasts.findIndex(t => t.id === id)
      if (index > -1) {
        this.toasts.splice(index, 1)
      }
    }
  }
})
```

### Render Toasts in App.vue

```vue
<template>
  <div class="toast-container">
    <Toast
      v-for="toast in appStore.toasts"
      :key="toast.id"
      v-bind="toast"
      @close="appStore.removeToast(toast.id)"
    />
  </div>
</template>
```

---

## Best Practices

### 1. Loading States
- Show loading BEFORE API call starts
- Minimum display time: 300ms (avoid flashing)
- Use skeleton screens for better UX

### 2. Error Messages
- Always include recovery action
- Log errors to console for debugging
- Don't expose technical details to users

### 3. Success Messages
- Auto-dismiss after 2-3 seconds
- Use green color consistently
- Keep text brief (< 15 words)

### 4. Empty States
- Provide clear next steps
- Use friendly illustrations
- Distinguish "no results" vs "no data"

---

## Troubleshooting

### "Toast doesn't appear"
Check: Is Pinia store imported? Is Teleport target in DOM?

### "Loading spinner blocks interaction"
Use `pointer-events: auto` on loading overlay

### "Empty state shows briefly before data loads"
Add minimum delay or check data before rendering

---

## Related Files

**Existing Components**:
- [Toast.vue](../../../frontend/src/components/common/Toast.vue)
- [Loading.vue](../../../frontend/src/components/common/Loading.vue)

**Create These**:
- `EmptyState.vue`
- `StatusBadge.vue`

**Related Skills**:
- `ux-copywriting-standards` - Write message text
- `vue-component-dev` - Component development patterns

---

**Skill Version**: v1.0
**Created**: 2025-11-09
**Focuses On**: Status UI components only
