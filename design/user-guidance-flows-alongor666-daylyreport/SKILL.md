---
name: user-guidance-flows
description: Create onboarding flows, tooltips, and help text for Vue 3 applications. Use when implementing first-time user guidance, feature introductions, help tooltips, or keyboard shortcuts. Mentions "onboarding", "tooltip", "help text", "user guide", or "feature introduction".
allowed-tools: Read, Edit, Grep, Glob
---

# User Guidance Flows

Onboarding, tooltips, and help systems for Vue 3 applications.

## When to Activate

Use this skill when the user:
- Says "create onboarding flow" or "first-time user experience"
- Asks "add tooltip" or "help text"
- Mentions "feature introduction" or "usage guide"
- Wants to implement "keyboard shortcuts help"

## Guidance Components

| Component | Use Case | Trigger |
|-----------|----------|---------|
| Onboarding Modal | First-time users | On first visit |
| Tooltip | Inline help | Hover/focus |
| Help Panel | Detailed guidance | Click "?" icon |
| Feature Highlight | New features | After update |
| Keyboard Shortcuts | Power users | Press "?" key |

---

## 1. Onboarding Flow

### 4-Step Onboarding

```vue
<template>
  <div v-if="showOnboarding" class="onboarding-overlay">
    <div class="onboarding-card">
      <div class="onboarding-card__progress">
        步骤 {{ currentStep }}/4
      </div>

      <div class="onboarding-card__content">
        <h2>{{ steps[currentStep - 1].title }}</h2>
        <p>{{ steps[currentStep - 1].description }}</p>
        <ul v-if="steps[currentStep - 1].features">
          <li v-for="feature in steps[currentStep - 1].features" :key="feature.icon">
            {{ feature.icon }} {{ feature.text }}
          </li>
        </ul>
      </div>

      <div class="onboarding-card__actions">
        <button v-if="currentStep > 1" @click="prevStep" class="btn btn--secondary">
          上一步
        </button>
        <button @click="nextStep" class="btn btn--primary">
          {{ currentStep < 4 ? '下一步' : '开始使用' }}
        </button>
      </div>

      <button @click="skipOnboarding" class="onboarding-card__skip">
        跳过引导
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showOnboarding = ref(!localStorage.getItem('onboarding_completed'))
const currentStep = ref(1)

const steps = [
  {
    title: '欢迎使用车险数据分析平台',
    description: '为您提供实时业务洞察和数据分析'
  },
  {
    title: '核心功能',
    features: [
      { icon: '📊', text: '实时 KPI 监控' },
      { icon: '📈', text: '周对比趋势分析' },
      { icon: '🔍', text: '多维度数据筛选' }
    ]
  },
  {
    title: '筛选器使用',
    description: '通过筛选器快速定位目标数据\n例如: 选择"达州"查看该机构业绩'
  },
  {
    title: '一切准备就绪',
    description: '开始探索您的数据吧！'
  }
]

const nextStep = () => {
  if (currentStep.value < 4) {
    currentStep.value++
  } else {
    completeOnboarding()
  }
}

const prevStep = () => {
  if (currentStep.value > 1) currentStep.value--
}

const skipOnboarding = () => completeOnboarding()

const completeOnboarding = () => {
  localStorage.setItem('onboarding_completed', 'true')
  showOnboarding.value = false
}
</script>
```

---

## 2. Tooltip Component

### Basic Tooltip

```vue
<template>
  <div class="tooltip-wrapper">
    <slot />
    <div v-if="visible" class="tooltip" :class="`tooltip--${placement}`">
      {{ content }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  content: { type: String, required: true },
  placement: {
    type: String,
    default: 'top',
    validator: v => ['top', 'bottom', 'left', 'right'].includes(v)
  }
})

const visible = ref(false)
</script>
```

### Usage

```vue
<Tooltip content="选择业务员所属机构" placement="top">
  <label>三级机构</label>
</Tooltip>
```

---

## 3. Feature Highlights

### Highlight Component

```vue
<template>
  <div class="feature-highlight" :style="highlightStyle">
    <div class="feature-highlight__content">
      <div class="feature-highlight__title">{{ title }}</div>
      <div class="feature-highlight__description">{{ description }}</div>
      <button @click="dismiss" class="btn btn--primary">知道了</button>
    </div>
    <div class="feature-highlight__arrow"></div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, required: true },
  target: { type: String, required: true }  // CSS selector
})

const emit = defineEmits(['dismiss'])

const highlightStyle = computed(() => {
  const element = document.querySelector(props.target)
  if (!element) return {}

  const rect = element.getBoundingClientRect()
  return {
    top: `${rect.bottom + 10}px`,
    left: `${rect.left}px`
  }
})

const dismiss = () => emit('dismiss')
</script>
```

---

## 4. Help Panel

### Expandable Help

```vue
<template>
  <div class="help-panel" :class="{ 'help-panel--open': isOpen }">
    <button class="help-panel__trigger" @click="toggle">
      <span v-if="!isOpen">?</span>
      <span v-else>×</span>
    </button>

    <Transition name="slide">
      <div v-if="isOpen" class="help-panel__content">
        <h3>使用帮助</h3>

        <div class="help-section">
          <h4>快捷键</h4>
          <ul>
            <li><kbd>Ctrl</kbd> + <kbd>R</kbd> 刷新数据</li>
            <li><kbd>Ctrl</kbd> + <kbd>F</kbd> 聚焦筛选</li>
            <li><kbd>Esc</kbd> 关闭弹窗</li>
            <li><kbd>?</kbd> 显示帮助</li>
          </ul>
        </div>

        <div class="help-section">
          <h4>常见问题</h4>
          <details>
            <summary>如何刷新数据？</summary>
            <p>点击右上角刷新按钮或按 Ctrl+R</p>
          </details>
          <details>
            <summary>如何筛选数据？</summary>
            <p>使用左侧筛选面板选择条件，点击"应用"</p>
          </details>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
const isOpen = ref(false)
const toggle = () => isOpen.value = !isOpen.value
</script>
```

---

## 5. Keyboard Shortcuts

### Shortcuts Handler

```javascript
// composables/useKeyboardShortcuts.js
export function useKeyboardShortcuts(handlers) {
  const handleKeyDown = (e) => {
    const ctrl = e.ctrlKey || e.metaKey

    // Ctrl+R: Refresh
    if (ctrl && e.key === 'r') {
      e.preventDefault()
      handlers.refresh?.()
    }

    // Ctrl+F: Focus filter
    if (ctrl && e.key === 'f') {
      e.preventDefault()
      handlers.focusFilter?.()
    }

    // Esc: Close modal
    if (e.key === 'Escape') {
      handlers.closeModal?.()
    }

    // ?: Show help
    if (e.shiftKey && e.key === '?') {
      handlers.showHelp?.()
    }
  }

  onMounted(() => {
    document.addEventListener('keydown', handleKeyDown)
  })

  onUnmounted(() => {
    document.removeEventListener('keydown', handleKeyDown)
  })
}
```

### Usage

```vue
<script setup>
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'

useKeyboardShortcuts({
  refresh: handleRefresh,
  focusFilter: () => filterPanelRef.value?.focus(),
  closeModal: () => modalVisible.value = false,
  showHelp: () => helpPanelVisible.value = true
})
</script>
```

---

## Help Text Library

### Field Help Texts

```javascript
export const HELP_TEXT = {
  institutionFilter: {
    title: '选择业务员所属机构',
    detail: '数据将仅显示该机构所有业务员的保单'
  },

  weekComparison: {
    title: '对比最近 3 周同星期的业绩',
    detail: '例如: 对比最近 3 个周一的保费数据，识别周期性规律'
  },

  premiumMetric: {
    title: '签单/批改保费净额',
    detail: '包含退保和批改调整，可能为负数'
  },

  kpiWindows: {
    title: '当日、近 7 天、近 30 天',
    detail: '所有时间范围从锚定日期向前推算(含当日)'
  }
}
```

---

## Best Practices

### 1. Onboarding
- Limit to 3-4 steps
- Allow skipping
- Don't repeat after dismissal
- Use localStorage to track completion

### 2. Tooltips
- Keep text under 20 words
- Show on hover/focus
- Position intelligently (avoid viewport edges)
- Add 200ms delay to avoid flashing

### 3. Help Text
- Provide examples
- Use simple language
- Link to detailed docs when needed

### 4. Keyboard Shortcuts
- Use standard conventions (Ctrl+R, Ctrl+F)
- Display shortcut list in help panel
- Don't override browser defaults

---

## Troubleshooting

### "Onboarding shows every time"
Check: Is localStorage working? Clear it if stuck:
```javascript
localStorage.removeItem('onboarding_completed')
```

### "Tooltip position is wrong"
Use a positioning library like FloatingUI

### "Keyboard shortcuts don't work"
Check: Are you preventing default? Is focus on correct element?

---

## Related Files

**Create These**:
- `components/guidance/OnboardingFlow.vue`
- `components/guidance/Tooltip.vue`
- `components/guidance/HelpPanel.vue`
- `composables/useKeyboardShortcuts.js`

**Related Skills**:
- `ux-copywriting-standards` - Write guidance copy
- `status-message-components` - Status UI patterns

---

**Skill Version**: v1.0
**Created**: 2025-11-09
**Focuses On**: User guidance only
