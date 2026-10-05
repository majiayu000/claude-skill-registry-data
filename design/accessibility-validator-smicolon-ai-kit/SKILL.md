---
name: vue-accessibility-validator
description: Automatically validate Vue 3/Nuxt.js components meet WCAG 2.1 AA standards. Use when creating components, forms, buttons, modals, navigation, or any interactive UI elements.
---

# Vue Accessibility Validator

## Activation Triggers

This skill activates when:
- Creating Vue components
- Writing template sections
- Adding interactive elements
- Mentioning "component", "form", "button"

## Checks

### Check 1: Semantic HTML

```vue
<!-- WRONG -->
<div @click="handleAction">Click me</div>

<!-- CORRECT -->
<button type="button" @click="handleAction">
  Click me
</button>
```

**Rule**: Interactive elements must use semantic HTML (`<button>`, `<a>`, `<input>`) not generic `<div>` or `<span>`.

### Check 2: Form Labels

```vue
<!-- WRONG -->
<input v-model="email" placeholder="Email" />

<!-- CORRECT -->
<label for="email">Email</label>
<input id="email" v-model="email" aria-describedby="email-hint" />
<span id="email-hint">Your work email address</span>
```

**Rule**: All form inputs must have associated labels or aria-label.

### Check 3: Keyboard Navigation

```vue
<!-- WRONG - Only mouse -->
<div @click="toggle" class="dropdown">

<!-- CORRECT - Keyboard accessible -->
<button
  type="button"
  @click="toggle"
  @keydown.enter="toggle"
  @keydown.space.prevent="toggle"
  :aria-expanded="isOpen"
  aria-haspopup="listbox"
>
```

**Rule**: All interactive elements must be keyboard accessible.

### Check 4: Focus Management

```vue
<!-- Modal with focus trap -->
<template>
  <div
    v-if="isOpen"
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    @keydown.escape="close"
  >
    <h2 id="modal-title">Modal Title</h2>
    <!-- Focus trapped inside -->
    <button ref="closeButton" @click="close">Close</button>
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'

const closeButton = ref<HTMLButtonElement>()

watch(isOpen, async (open) => {
  if (open) {
    await nextTick()
    closeButton.value?.focus()
  }
})
</script>
```

### Check 5: Image Alt Text

```vue
<!-- WRONG -->
<img :src="product.image" />

<!-- CORRECT - Informative image -->
<img :src="product.image" :alt="product.name" />

<!-- CORRECT - Decorative image -->
<img :src="decorativePattern" alt="" role="presentation" />
```

### Check 6: Color Contrast

Ensure 4.5:1 ratio for normal text, 3:1 for large text.

```vue
<!-- Use Tailwind classes that meet contrast -->
<p class="text-gray-700 bg-white">Readable text</p>

<!-- WRONG - Low contrast -->
<p class="text-gray-400 bg-white">Hard to read</p>
```

### Check 7: ARIA Attributes

```vue
<!-- Loading state -->
<button :aria-busy="isLoading" :disabled="isLoading">
  <span v-if="isLoading" aria-live="polite">Loading...</span>
  <span v-else>Submit</span>
</button>

<!-- Expandable section -->
<button
  :aria-expanded="isExpanded"
  :aria-controls="panelId"
  @click="toggle"
>
  Show Details
</button>
<div :id="panelId" v-show="isExpanded">
  Details content
</div>
```

## Auto-Fix Actions

When issues detected:

1. **div with @click** -> Convert to `<button type="button">`
2. **Missing label** -> Add `<label>` or `aria-label`
3. **Missing keyboard handler** -> Add `@keydown` handlers
4. **Missing ARIA** -> Add appropriate ARIA attributes
5. **Missing alt** -> Prompt for alt text

## Validation Report

```
ACCESSIBILITY VALIDATION

File: components/ProductCard.vue

 Semantic HTML: Using button elements
 Form labels: All inputs labeled
 Keyboard nav: Tab order correct
 Focus management: Modal traps focus
 Image alt text: All images have alt

Issues:
 Line 45: <div @click> should be <button>
 Line 72: Input missing aria-describedby for error

Summary: 2 issues to fix
```

## WCAG 2.1 AA Checklist

- [ ] 1.1.1 Non-text Content: Alt text for images
- [ ] 1.3.1 Info and Relationships: Semantic markup
- [ ] 1.4.3 Contrast: 4.5:1 minimum
- [ ] 2.1.1 Keyboard: All functionality accessible
- [ ] 2.4.3 Focus Order: Logical tab sequence
- [ ] 2.4.7 Focus Visible: Focus indicators
- [ ] 3.3.2 Labels: Form inputs labeled
- [ ] 4.1.2 Name, Role, Value: ARIA correct
