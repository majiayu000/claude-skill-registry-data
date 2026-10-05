---
name: vue
description: Use when building Vue 3 applications. Covers the Composition API, reactivity fundamentals, composables, Pinia state management, and the reactivity mistakes that cause silent update failures.
metadata:
  category: frontend
  version: 1.0.0
  tags: [vue, composition-api, reactivity, pinia, nuxt]
---

# Vue

## Purpose

Write Vue 3 with a correct mental model of reactivity. Most Vue bugs are not logic errors — they are a `ref` that was destructured, or a `reactive` object that was reassigned, and the view silently stopped updating.

## When to Use

- Building or reviewing Vue 3 applications.
- Extracting reusable logic into composables.
- Debugging a value that changes but does not re-render.
- Structuring state with Pinia.

## Capabilities

- Composition API with `<script setup>`.
- Reactivity: `ref`, `reactive`, `computed`, `watch`, `watchEffect`, and their differences.
- Composables for shared logic with proper lifecycle cleanup.
- Pinia stores, including typed state and actions.
- Performance: `shallowRef`, `v-memo`, and avoiding deep watchers.

## Inputs

- The component or composable, and where its state originates.
- The reactivity symptom, if debugging.

## Outputs

- Components using `<script setup>` with typed props and emits.
- Composables that clean up after themselves.
- Reactivity that survives destructuring and reassignment.

## Workflow

1. **Prefer `ref` over `reactive`** — `ref` survives destructuring (via `.value`) and reassignment. `reactive` loses reactivity on both, silently.
2. **Derive with `computed`** — Not with a `watch` that assigns to another ref. That is two renders and a chance to be out of sync.
3. **Extract composables for shared behavior** — Anything that owns a subscription, listener, or timer must clean it up in `onScopeDispose` or `onUnmounted`.
4. **Type the boundaries** — `defineProps<T>()` and `defineEmits<T>()` with type arguments. Runtime-only prop declarations discard type information.
5. **Watch narrowly** — Watch a specific getter, not a whole object with `deep: true`. Deep watchers on large objects are a common and invisible performance cost.

## Best Practices

- Destructuring a `reactive` object breaks reactivity: `const { count } = reactive({ count: 0 })` gives you a plain number. Use `toRefs` or, better, use `ref`.
- Reassigning a `reactive` object (`state = { ... }`) replaces the proxy and detaches every existing binding. `ref` does not have this failure mode.
- `watchEffect` tracks whatever it reads — including things you did not intend. `watch` with an explicit source is more predictable and should be the default.
- A composable that adds an event listener without removing it leaks on every mount. `onScopeDispose` handles the composable-in-composable case that `onUnmounted` does not.
- Prefer `shallowRef` for large immutable data structures; deep reactivity on a 10,000-element array is a real cost paid on every mutation.
- Do not mutate props. Emit an event and let the owner change its own state.

## Examples

**A composable with correct cleanup and derived state:**

```typescript
export function useOrderStream(orderId: Ref<string>) {
  const events = ref<OrderEvent[]>([]);
  const status = computed(() => events.value.at(-1)?.status ?? "unknown");
  const error = ref<Error | null>(null);

  let source: EventSource | null = null;

  const connect = (id: string) => {
    source?.close();
    events.value = [];
    source = new EventSource(`/api/orders/${id}/stream`);
    source.onmessage = (e) => events.value.push(JSON.parse(e.data));
    source.onerror = () => { error.value = new Error("stream disconnected"); };
  };

  watch(orderId, connect, { immediate: true });
  onScopeDispose(() => source?.close());   // fires even when used inside another composable

  return { events, status, error };
}
```

**Reactivity that silently fails:**

```typescript
// Broken: `count` is a plain number; the template never updates.
const state = reactive({ count: 0 });
const { count } = state;

// Broken: reassignment detaches every binding to the old proxy.
let state = reactive({ items: [] });
state = reactive({ items: newItems });

// Correct: refs survive both.
const count = ref(0);
const items = ref<Item[]>([]);
items.value = newItems;
```

## Notes

- `v-memo` skips re-rendering a subtree when its dependency array is unchanged. It is worth reaching for on large `v-for` lists and almost nowhere else.
- Pinia stores are reactive objects: destructuring them has the same failure mode as `reactive`. Use `storeToRefs`.
- `<script setup>` compiles props and emits at build time. The runtime `defineComponent` form still works but discards the type-level checking that makes Vue 3 pleasant.
