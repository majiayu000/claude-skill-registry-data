---
name: vue
description: Vue 3 Composition API, Nuxt patterns, reactivity system, component architecture, and production development practices
layer: domain
category: frontend
triggers:
  - "vue"
  - "vue 3"
  - "nuxt"
  - "composition api"
  - "vue component"
  - "ref()"
  - "reactive()"
  - "computed()"
  - "defineProps"
  - "pinia"
  - "vue router"
inputs:
  - "Vue component or page requirements"
  - "Composition API pattern questions"
  - "Nuxt routing and data fetching"
  - "Vue reactivity system guidance"
outputs:
  - "Vue 3 SFC components with Composition API"
  - "Nuxt pages, layouts, and server routes"
  - "Composable function implementations"
  - "Pinia store patterns"
linksTo:
  - typescript-frontend
  - css-architecture
  - forms
  - state-management
linkedFrom:
  - code-writer
  - architect
preferredNextSkills:
  - typescript-frontend
  - state-management
  - forms
fallbackSkills:
  - react
  - svelte
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Vue 3 & Nuxt Patterns

## Purpose

Provide expert guidance on Vue 3 Composition API, Single File Components (SFC), Nuxt 3, reactivity patterns, composables, and production-grade Vue application development. Focus on `<script setup>`, TypeScript integration, and modern Vue idioms.

## Key Patterns

### Script Setup Components

**Basic component with props and emits:**

```vue
<!-- components/Button.vue -->
<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  loading: false,
});

const emit = defineEmits<{
  click: [event: MouseEvent];
}>();

// Slots typing
defineSlots<{
  default: () => any;
  icon?: () => any;
}>();

function handleClick(e: MouseEvent) {
  if (!props.loading) {
    emit('click', e);
  }
}
</script>

<template>
  <button
    :class="[
      'inline-flex items-center justify-center px-6 py-4 text-base rounded-lg',
      'transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2',
      variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700',
      variant === 'secondary' && 'bg-white border border-gray-300 hover:bg-gray-50',
      variant === 'ghost' && 'text-gray-600 hover:bg-gray-100',
      loading && 'opacity-50 pointer-events-none',
    ]"
    :disabled="loading"
    @click="handleClick"
  >
    <slot name="icon" />
    <slot />
  </button>
</template>
```

### Reactivity System

**`ref` vs `reactive`:**

```vue
<script setup lang="ts">
import { ref, reactive, computed, watch, watchEffect } from 'vue';

// ref — for primitives and values you reassign
const count = ref(0);
const name = ref('');
const isOpen = ref(false);

// reactive — for objects where you mutate properties
const form = reactive({
  title: '',
  description: '',
  tags: [] as string[],
});

// computed — derived values (cached, auto-tracked)
const isValid = computed(() => form.title.length > 0 && form.description.length > 0);
const tagCount = computed(() => form.tags.length);

// Writable computed
const fullName = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (val: string) => {
    const [first, ...rest] = val.split(' ');
    firstName.value = first;
    lastName.value = rest.join(' ');
  },
});

// watch — explicit dependency tracking
watch(count, (newVal, oldVal) => {
  console.log(`Count changed: ${oldVal} -> ${newVal}`);
});

// Watch multiple sources
watch([count, name], ([newCount, newName]) => {
  // Fires when either changes
});

// Deep watch on reactive object
watch(
  () => form.tags,
  (newTags) => { /* tags array changed */ },
  { deep: true }
);

// watchEffect — auto-tracks dependencies
watchEffect((onCleanup) => {
  if (name.value.length < 2) return;

  const controller = new AbortController();
  fetchSuggestions(name.value, { signal: controller.signal });

  onCleanup(() => controller.abort());
});
</script>
```

### Composables (Hooks)

**Reusable logic extraction:**

```ts
// composables/useToggle.ts
import { ref, type Ref } from 'vue';

export function useToggle(initial = false): {
  value: Ref<boolean>;
  toggle: () => void;
  setTrue: () => void;
  setFalse: () => void;
} {
  const value = ref(initial);
  const toggle = () => { value.value = !value.value; };
  const setTrue = () => { value.value = true; };
  const setFalse = () => { value.value = false; };
  return { value, toggle, setTrue, setFalse };
}
```

**Data fetching composable:**

```ts
// composables/useFetch.ts
import { ref, watchEffect, type Ref } from 'vue';

interface UseFetchReturn<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  loading: Ref<boolean>;
  refresh: () => Promise<void>;
}

export function useFetch<T>(url: Ref<string> | string): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function fetchData() {
    loading.value = true;
    error.value = null;
    try {
      const urlValue = typeof url === 'string' ? url : url.value;
      const response = await fetch(urlValue);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data.value = await response.json();
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e));
    } finally {
      loading.value = false;
    }
  }

  watchEffect(() => {
    fetchData();
  });

  return { data, error, loading, refresh: fetchData };
}
```

### Nuxt 3 Patterns

**File-based routing:**

```
pages/
  index.vue             # /
  about.vue             # /about
  dashboard/
    index.vue           # /dashboard
    settings.vue        # /dashboard/settings
    [teamId].vue        # /dashboard/:teamId
  posts/
    [...slug].vue       # /posts/* (catch-all)
```

**Server data loading:**

```vue
<!-- pages/dashboard.vue -->
<script setup lang="ts">
// useFetch: SSR + client hydration, auto-caching
const { data: stats, pending, error, refresh } = await useFetch('/api/dashboard/stats');

// useAsyncData for custom logic
const { data: user } = await useAsyncData('user', () => {
  return $fetch('/api/user/me');
});

// Parallel fetching
const [{ data: posts }, { data: categories }] = await Promise.all([
  useFetch('/api/posts'),
  useFetch('/api/categories'),
]);

// Lazy loading (non-blocking, loads after page renders)
const { data: suggestions, pending: suggestionsLoading } = useLazyFetch('/api/suggestions');
</script>

<template>
  <section class="py-16">
    <div v-if="pending" class="animate-pulse">Loading...</div>
    <div v-else-if="error" class="text-red-600">{{ error.message }}</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="stat in stats"
        :key="stat.id"
        class="p-6 rounded-xl shadow-sm border"
      >
        <p class="text-sm text-gray-500">{{ stat.label }}</p>
        <p class="text-2xl font-bold mt-1">{{ stat.value }}</p>
      </div>
    </div>
  </section>
</template>
```

**Server routes (API):**

```ts
// server/api/posts.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const posts = await db.post.findMany({
    take: Number(query.limit) || 20,
    orderBy: { createdAt: 'desc' },
  });
  return posts;
});

// server/api/posts.post.ts
import { z } from 'zod';

const PostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
});

export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const parsed = PostSchema.safeParse(body);

  if (!parsed.success) {
    throw createError({
      statusCode: 400,
      data: parsed.error.flatten().fieldErrors,
    });
  }

  return await db.post.create({ data: parsed.data });
});
```

**Middleware:**

```ts
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to) => {
  const user = useUser(); // composable that returns auth state

  if (!user.value && to.path.startsWith('/dashboard')) {
    return navigateTo('/login');
  }
});
```

### Provide/Inject (Dependency Injection)

```vue
<!-- components/Tabs.vue -->
<script setup lang="ts">
import { provide, ref, type InjectionKey } from 'vue';

interface TabsContext {
  activeTab: Ref<string>;
  setActive: (id: string) => void;
}

export const TABS_KEY: InjectionKey<TabsContext> = Symbol('tabs');

const props = defineProps<{ defaultTab: string }>();
const activeTab = ref(props.defaultTab);

provide(TABS_KEY, {
  activeTab,
  setActive: (id: string) => { activeTab.value = id; },
});
</script>

<template>
  <div role="tablist"><slot /></div>
</template>
```

```vue
<!-- components/Tab.vue -->
<script setup lang="ts">
import { inject } from 'vue';
import { TABS_KEY } from './Tabs.vue';

const props = defineProps<{ id: string }>();
const tabs = inject(TABS_KEY)!;
</script>

<template>
  <button
    role="tab"
    :aria-selected="tabs.activeTab.value === id"
    class="px-6 py-4 text-base rounded-lg transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
    :class="tabs.activeTab.value === id ? 'bg-blue-100 text-blue-700' : 'text-gray-600 hover:bg-gray-100'"
    @click="tabs.setActive(id)"
  >
    <slot />
  </button>
</template>
```

### Vue Transition System

```vue
<template>
  <!-- Single element transition -->
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 translate-y-4"
  >
    <div v-if="isVisible" class="p-6 rounded-xl shadow-sm">
      Animated content
    </div>
  </Transition>

  <!-- List transitions -->
  <TransitionGroup
    tag="ul"
    enter-active-class="transition-all duration-300"
    enter-from-class="opacity-0 translate-x-8"
    enter-to-class="opacity-100 translate-x-0"
    leave-active-class="transition-all duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
    move-class="transition-transform duration-300"
    class="space-y-4"
  >
    <li v-for="item in items" :key="item.id" class="p-6 rounded-xl shadow-sm">
      {{ item.name }}
    </li>
  </TransitionGroup>
</template>
```

## Best Practices

1. **`<script setup>` always** — The setup syntax is more concise, better typed, and has better performance.
2. **`ref` for primitives, `reactive` for objects** — But prefer `ref` everywhere for consistency if team prefers.
3. **Composables for logic reuse** — Extract shared logic into `composables/` functions, prefixed with `use`.
4. **`computed` over `watch`** — Use `computed` for derived state. Only use `watch` for side effects.
5. **Type props with generics** — `defineProps<Props>()` with interface, not runtime validation.
6. **Nuxt `useFetch` over `$fetch`** — `useFetch` handles SSR, caching, and hydration automatically.
7. **Provide/Inject for compound components** — Use `InjectionKey<T>` for type safety.
8. **`shallowRef` for large objects** — When you only replace (not mutate) the value, `shallowRef` skips deep tracking.
9. **`v-memo` for expensive lists** — Cache list items that haven't changed: `v-memo="[item.id, item.updated]"`.
10. **Auto-imports in Nuxt** — Components, composables, and Vue APIs are auto-imported. No manual imports needed.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Destructuring reactive | Loses reactivity: `const { x } = reactive({x: 1})` | Use `toRefs()` or keep using `state.x` |
| Forgetting `.value` with ref | Template auto-unwraps, JS does not | Always use `.value` in `<script>`, omit in `<template>` |
| Mutating props | Vue warns, data flow breaks | Emit events to parent, or use v-model |
| Watchers without cleanup | Memory leaks on component unmount | Use `onCleanup` in `watchEffect`, or `onUnmounted` |
| `v-if` with `v-for` | `v-if` on same element as `v-for` is ambiguous | Wrap in `<template v-for>` then `v-if` inside |
| Missing `:key` on `v-for` | Incorrect DOM reuse, bugs | Always use unique, stable keys |
| Blocking SSR with client APIs | `window is not defined` on server | Use `onMounted` or `<ClientOnly>` for browser APIs |
| Over-watching | Too many watchers, performance issues | Consolidate with `computed` or single `watchEffect` |
| Not using `defineModel` | Verbose v-model implementation | `const model = defineModel<string>()` in Vue 3.4+ |
| Fetch in `onMounted` in Nuxt | SSR miss, client waterfall | Use `useFetch` or `useAsyncData` at top level |
