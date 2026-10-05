---
name: nuxtjs-import-enforcer
description: Automatically enforce consistent import patterns using Nuxt.js ~/ path aliases and proper organization. Use when writing imports, creating new Vue/TS files, or organizing code structure.
---

# Nuxt.js Import Convention Enforcer

## Activation Triggers

This skill activates when:
- Writing imports in Vue/TS files
- Creating new files
- Modifying existing files with imports

## Import Order

1. Vue/Nuxt built-ins (usually auto-imported)
2. Third-party packages
3. Composables (auto-imported from ~/composables/)
4. Components (auto-imported from ~/components/)
5. Types

## Pattern

```vue
<script setup lang="ts">
// 1. Vue (only if explicitly needed - usually auto-imported)
import { ref, computed, watch } from 'vue'

// 2. Third-party
import { z } from 'zod'
import dayjs from 'dayjs'

// 3. Composables (only if not auto-imported)
import { useAuth } from '~/composables/useAuth'

// 4. Types
import type { User } from '~/types/user'

// Implementation
const user = ref<User | null>(null)
</script>
```

## Path Aliases

```typescript
// CORRECT - Use ~/ alias
import { useAuth } from '~/composables/useAuth'
import type { User } from '~/types/user'
import { formatDate } from '~/utils/date'

// WRONG - Relative imports
import { useAuth } from '../../../composables/useAuth'

// WRONG - @ alias (use ~/ for Nuxt)
import { useAuth } from '@/composables/useAuth'
```

## Auto-Import Awareness

Nuxt auto-imports these - DON'T import explicitly:

### Vue Composition API
```typescript
// DON'T import - auto-imported
ref, reactive, computed, watch, watchEffect, toRef, toRefs
onMounted, onUnmounted, onBeforeMount, onBeforeUnmount
provide, inject
```

### Nuxt Composables
```typescript
// DON'T import - auto-imported
useFetch, useAsyncData, useLazyFetch, useLazyAsyncData
useState, useCookie, useHead, useSeoMeta
useRoute, useRouter, useRuntimeConfig
navigateTo, abortNavigation
definePageMeta, defineNuxtComponent
```

### Components
```typescript
// DON'T import - auto-imported from ~/components/
// Just use directly in template
<MyComponent />
<BaseButton />
<ui-card />
```

## Detection Rules

### Rule 1: Unnecessary Vue Imports

```typescript
// WRONG
import { ref, computed } from 'vue'

// CORRECT - Just use directly
const count = ref(0)
const doubled = computed(() => count.value * 2)
```

**Action**: Remove unnecessary imports, use auto-imported functions

### Rule 2: Unnecessary Nuxt Imports

```typescript
// WRONG
import { useFetch } from '#app'
import { useRoute } from 'vue-router'

// CORRECT - Just use directly
const { data } = await useFetch('/api/users')
const route = useRoute()
```

**Action**: Remove unnecessary imports

### Rule 3: Component Imports

```vue
<!-- WRONG -->
<script setup>
import MyComponent from '~/components/MyComponent.vue'
</script>
<template>
  <MyComponent />
</template>

<!-- CORRECT - Auto-imported -->
<script setup>
// No import needed
</script>
<template>
  <MyComponent />
</template>
```

### Rule 4: Relative Import Detection

```typescript
// WRONG
import { formatDate } from '../utils/date'
import { User } from '../../types/user'

// CORRECT
import { formatDate } from '~/utils/date'
import type { User } from '~/types/user'
```

**Action**: Convert to ~/ path alias

## Auto-Fix Actions

1. **Unnecessary Vue import** -> Remove import statement
2. **Unnecessary Nuxt import** -> Remove import statement
3. **Component import** -> Remove import, verify component exists
4. **Relative import** -> Convert to ~/path
5. **@ alias** -> Convert to ~/

## Validation Report

```
IMPORT CONVENTION CHECK

File: pages/users/[id].vue

 Import order: Correct (third-party, then local)
 Path aliases: Using ~/
 Auto-imports: Correctly utilized

Issues:
 Line 3: Remove "import { ref } from 'vue'" - auto-imported
 Line 5: Remove "import { useFetch } from '#app'" - auto-imported
 Line 8: Convert "../utils" to "~/utils"

Auto-fix available: Apply 3 fixes
```

## Configuration

In `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  imports: {
    // Customize auto-import dirs
    dirs: ['composables', 'utils'],
  },
  components: {
    // Customize component auto-import
    dirs: ['~/components'],
  },
})
```
