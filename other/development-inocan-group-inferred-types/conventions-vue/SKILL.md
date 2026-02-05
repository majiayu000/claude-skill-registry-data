---
name: conventions-vue
description: Apply when working with Vue components, composables, stores, or styling. Ensures code matches established project patterns.
---

# Vue Conventions

## Component Structure

**Always:** `<script setup lang="ts">` — no Options API, no class components, no mixins.

### Props

```typescript
// Library components (ui-vue): export interface for reuse
export interface BaseInputProps {
  modelValue: string | number;
  type?: "text" | "email" | "number";
  disabled?: boolean;
}
const props = withDefaults(defineProps<BaseInputProps>(), {
  type: "text",
});

// App components: local interface
interface Props {
  status: string;
  variant?: "solid" | "outline";
}
const props = withDefaults(defineProps<Props>(), {
  variant: "solid",
});
```

### Emits

```typescript
// Typed tuple syntax
const emit = defineEmits<{
  "update:modelValue": [value: string];
  focus: [];
}>();

// v-model via defineModel
const open = defineModel<boolean>("open", { required: true });
```

## File Organization

## Components high-level directory (atomic design)

- `atoms/` → `Base*` prefix (BaseButton, BaseInput, BaseCard)
- `molecules/` → Descriptive (FormControl, TabsGroup)
- `organisms/` → Complex (DataTable)
- `layouts/` → FlexLayout, ModalContainer, SlideOut

## Domain high-level directory

- `domain/common/` → Shared
- `domain/{feature}/` → Feature-specific, ie: domain/radar/

## Other high-level directories

- `composables/` → Feature hooks
- `stores/` → Pinia
- `services/` → API layer
- `types/` → TypeScript definitions

## Composables

**Naming:** `use*` prefix — `useModal`, `useAirportAutocomplete`

**Return pattern:** Object with refs, computed, methods

```typescript
export const useAirportAutocomplete = () => {
  const results = ref<Airport[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const search = async (term: string) => { ... }

  return { results, loading, error, search }
}
```

**Options for complex composables:**

```typescript
interface UseModalSubmissionOptions<T, R> {
  defaultFormData: T;
  submitAction: (data: T) => Promise<R>;
  onSuccess?: (result: R) => void;
}
```

## Pinia Stores

**Options API style** (not setup stores):

```typescript
export const useSessionStore = defineStore('session', {
  state: (): SessionState => ({
    user: null,
    isLoading: false,
    error: null
  }),
  actions: {
    async checkSession() { ... },
  }
})
```

- Explicit state interfaces
- All API calls in actions
- URL as source of truth for query state

## Styling

See **conventions-css** skill. Key points:

- `<style scoped>` for domain components, unscoped for atomic design components
- Design tokens via CSS custom properties exclusively
- No Tailwind, utility classes, or CSS-in-JS

## Common Patterns

**Loading/error states:**

```vue
<FlexLayout v-if="isLoading" align="center">
  <BaseIcon id="spinner" inline /> Loading...
</FlexLayout>
<AlertMessage v-else-if="error" :message="error" type="error" />
<template v-else>
  <!-- Content -->
</template>
```

**Forms:** FormControl molecule wrapping atoms

```vue
<FormControl v-model="formData.reason" :error="error" label="Reason" type="textarea" />
```

**Modals:** ModalContainer + useModalSubmission

```vue
<ModalContainer :is-open="open" title="Suspend" @close="open = false">
  <FormControl v-model="formData.reason" />
  <template #footer>
    <BaseButton :loading="isLoading" @click="submitForm">Submit</BaseButton>
  </template>
</ModalContainer>
```

**Layout:** FlexLayout/FlexItem, not raw flexbox

```vue
<FlexLayout direction="column" gap="xs">
  <FlexItem :span="6">Label</FlexItem>
  <FlexItem :span="6">Value</FlexItem>
</FlexLayout>
```

## TypeScript

- Strict mode
- `type` for object shapes (props, state)
- `type` for unions and aliases

## Never Do

- Options API
- Mixins
- Global components (always explicit imports)
- Vuex
- Inline styles (except dynamic values)
- Magic strings for events
- CSS-in-JS or Tailwind
