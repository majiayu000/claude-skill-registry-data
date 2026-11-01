---
name: vue
description: Vue 3 Composition API, script setup macros, reactivity system, and built-in components. Use when writing Vue SFCs, defineProps/defineEmits/defineModel, watchers, or using Transition/Teleport/Suspense/KeepAlive.
metadata:
  author: Anthony Fu
  version: "2026.9.25"
  source: Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills
---

> **CampusCove note.** Vendored from [antfu/skills](https://github.com/antfu/skills) @ 8886fe2, MIT (`_third-party/LICENSE-antfu.txt`); only this note was added.
>
> Here: Vue 3.5.27, `<script setup lang="ts">`, Tailwind, no Pinia (state lives in composables and `api/session.ts`). Keep Three.js objects, the renderer and the Colyseus `Room` out of deep reactivity: plain variables inside the composable, or `shallowRef` (as `gameRoomRef` in `GameView.vue`); a `ref()` around a scene graph proxies every node and costs frames. Game logic stays in `front/src/game/` (no Vue), Vue glue in `composables/game/`, and `GameView.vue` only wires them. API calls go through `api/http.ts` `apiRequest`, not `fetch`. The Suspense / top-level `await` examples are not used here.
>
> Advisory reference: CampusCove's own skills (`game-feature`, `socket-message`, `playtest-game`, ...) win on any conflict.

# Vue

> Based on Vue 3.5, generated at 2026-09-25. Always use Composition API with `<script setup lang="ts">`.

## Preferences

- Prefer TypeScript over JavaScript
- Prefer `<script setup lang="ts">` over `<script>`
- For performance, prefer `shallowRef` over `ref` if deep reactivity is not needed
- Always use Composition API over Options API
- Discourage using Reactive Props Destructure

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Script Setup & Macros | `<script setup>`, defineProps, defineEmits, defineModel, defineExpose, defineOptions, defineSlots, generics | [script-setup-macros](references/script-setup-macros.md) |
| Reactivity & Lifecycle | ref, shallowRef, computed, watch, watchEffect, effectScope, lifecycle hooks, composables | [core-new-apis](references/core-new-apis.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Built-in Components & Directives | Transition, Teleport, Suspense, KeepAlive, v-memo, custom directives | [advanced-patterns](references/advanced-patterns.md) |

## Quick Reference

### Component Template

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps<{
  title: string
  count?: number
}>()

const emit = defineEmits<{
  update: [value: string]
}>()

const model = defineModel<string>()

const doubled = computed(() => (props.count ?? 0) * 2)

watch(() => props.title, (newVal) => {
  console.log('Title changed:', newVal)
})

onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div>{{ title }} - {{ doubled }}</div>
</template>
```

### Key Imports

```ts
// Reactivity
import { ref, shallowRef, computed, reactive, readonly, toRef, toRefs, toValue } from 'vue'

// Watchers
import { watch, watchEffect, watchPostEffect, onWatcherCleanup } from 'vue'

// Lifecycle
import { onMounted, onUpdated, onUnmounted, onBeforeMount, onBeforeUpdate, onBeforeUnmount } from 'vue'

// Utilities
import { nextTick, defineComponent, defineAsyncComponent } from 'vue'
```
