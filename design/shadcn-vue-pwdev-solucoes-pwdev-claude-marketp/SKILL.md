---
name: shadcn-vue
description: >
  Skill for scaffolding, installation, and composition of shadcn-vue components
  (based on Reka UI v2). Use when you need to install components, understand
  Vue variants, compose patterns with vee-validate/Zod, or adapt existing components.
  Stack: Vue 3 + Reka UI v2 + Tailwind CSS.
---

# Skill: shadcn-vue + Reka UI v2

> shadcn-vue@latest uses Reka UI v2 by default (since Feb/2025).
> For legacy Radix Vue: `shadcn-vue@radix`

## CLI — Essential commands

```bash
# Initialize (new project)
npx shadcn-vue@latest init

# Add component
npx shadcn-vue@latest add button
npx shadcn-vue@latest add form dialog card

# Add from remote URL (custom registry)
npx shadcn-vue add https://acme.com/registry/navbar.json

# Check installed components
ls components/ui/
```

## Vite + Vue 3 Installation

```bash
npm create vue@latest my-app
cd my-app
npm install
npx shadcn-vue@latest init
```

## Nuxt 3 Installation

```bash
npx nuxi@latest init my-app
cd my-app
npx shadcn-vue@latest init
```

Generated `components.json`:
```json
{
  "$schema": "https://shadcn-vue.com/schema.json",
  "style": "new-york",
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "src/assets/index.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "composables": "@/composables"
  }
}
```

---

## Vue 3 Component Patterns

### Button
```vue
<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Loader2, Trash2 } from 'lucide-vue-next'
</script>

<template>
  <!-- Variants: default | destructive | outline | secondary | ghost | link -->
  <!-- Sizes: default | sm | lg | icon -->
  <Button variant="destructive" size="sm" :disabled="isLoading">
    <Loader2 v-if="isLoading" class="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
    Delete
  </Button>

  <!-- Icon-only button — always use aria-label -->
  <Button variant="ghost" size="icon" aria-label="Close panel">
    <X class="h-4 w-4" aria-hidden="true" />
  </Button>
</template>
```

### Card with actions
```vue
<script setup lang="ts">
import {
  Card, CardContent, CardDescription,
  CardFooter, CardHeader, CardTitle
} from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
</script>

<template>
  <Card>
    <CardHeader>
      <div class="flex items-center justify-between">
        <CardTitle>Card Title</CardTitle>
        <Badge variant="outline">Status</Badge>
      </div>
      <CardDescription>Clear and concise description.</CardDescription>
    </CardHeader>
    <CardContent>
      <slot />
    </CardContent>
    <CardFooter class="flex justify-end gap-2">
      <Button variant="outline" @click="emit('cancel')">Cancel</Button>
      <Button @click="emit('confirm')">Confirm</Button>
    </CardFooter>
  </Card>
</template>
```

### Dialog (Modal)
```vue
<script setup lang="ts">
import { ref } from 'vue'
import {
  Dialog, DialogContent, DialogDescription,
  DialogHeader, DialogTitle, DialogTrigger
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

const open = ref(false)
</script>

<template>
  <Dialog v-model:open="open">
    <DialogTrigger as-child>
      <Button>Open Dialog</Button>
    </DialogTrigger>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Accessible Title</DialogTitle>
        <DialogDescription>
          Description of what happens in this dialog.
        </DialogDescription>
      </DialogHeader>
      <!-- content -->
    </DialogContent>
  </Dialog>
</template>
```

### Select
```vue
<script setup lang="ts">
import { ref } from 'vue'
import {
  Select, SelectContent, SelectItem,
  SelectTrigger, SelectValue
} from '@/components/ui/select'

const value = ref('')
</script>

<template>
  <Select v-model="value">
    <SelectTrigger class="w-full">
      <SelectValue placeholder="Select an option" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="opt1">Option 1</SelectItem>
      <SelectItem value="opt2">Option 2</SelectItem>
    </SelectContent>
  </Select>
</template>
```

### Complete form with vee-validate + Zod
```vue
<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { toast } from 'vue-sonner'
import { Button } from '@/components/ui/button'
import {
  FormControl, FormDescription, FormField,
  FormItem, FormLabel, FormMessage
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

const schema = toTypedSchema(
  z.object({
    name: z.string().min(2, 'Name must have at least 2 characters'),
    email: z.string().email('Invalid email'),
    message: z.string().min(10, 'Message too short').max(500),
  })
)

const form = useForm({ validationSchema: schema })

const onSubmit = form.handleSubmit(async (values) => {
  try {
    await api.submit(values)
    toast.success('Message sent successfully!')
    form.resetForm()
  } catch {
    toast.error('Error sending. Please try again.')
  }
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-6" novalidate>
    <FormField v-slot="{ componentField }" name="name">
      <FormItem>
        <FormLabel>Name</FormLabel>
        <FormControl>
          <Input placeholder="Your name" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="email">
      <FormItem>
        <FormLabel>Email</FormLabel>
        <FormControl>
          <Input type="email" placeholder="name@company.com" v-bind="componentField" />
        </FormControl>
        <FormDescription>We never share your email.</FormDescription>
        <FormMessage />
      </FormItem>
    </FormField>

    <FormField v-slot="{ componentField }" name="message">
      <FormItem>
        <FormLabel>Message</FormLabel>
        <FormControl>
          <Textarea placeholder="Your message..." v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <Button type="submit" :disabled="form.isSubmitting.value" class="w-full">
      <Loader2
        v-if="form.isSubmitting.value"
        class="mr-2 h-4 w-4 animate-spin"
        aria-hidden="true"
      />
      {{ form.isSubmitting.value ? 'Sending...' : 'Send' }}
    </Button>
  </form>
</template>
```

### Field component (alternative without vee-validate)
```vue
<script setup lang="ts">
import {
  Field, FieldGroup, FieldLabel,
  FieldDescription, FieldError, FieldSet, FieldLegend
} from '@/components/ui/field'
import { Input } from '@/components/ui/input'
</script>

<template>
  <FieldGroup>
    <FieldSet>
      <FieldLegend>Personal Information</FieldLegend>
      <FieldGroup>
        <Field>
          <FieldLabel html-for="username">Username</FieldLabel>
          <Input id="username" v-model="username" />
          <FieldDescription>Your public username.</FieldDescription>
          <FieldError v-if="usernameError">{{ usernameError }}</FieldError>
        </Field>
      </FieldGroup>
    </FieldSet>
  </FieldGroup>
</template>
```

### Empty state (native shadcn-vue component)
```vue
<script setup lang="ts">
import { Empty, EmptyContent, EmptyDescription, EmptyHeader, EmptyTitle } from '@/components/ui/empty'
import { Button } from '@/components/ui/button'
import { SearchIcon } from 'lucide-vue-next'
</script>

<template>
  <Empty>
    <EmptyHeader>
      <EmptyTitle>No results found</EmptyTitle>
      <EmptyDescription>Try adjusting your search or filters.</EmptyDescription>
    </EmptyHeader>
    <EmptyContent>
      <Button variant="outline" @click="reset">Clear filters</Button>
    </EmptyContent>
  </Empty>
</template>
```

### Toast with vue-sonner
```vue
<script setup lang="ts">
import { toast } from 'vue-sonner'

function handleAction() {
  try {
    // action
    toast.success('Saved successfully!')
  } catch {
    toast.error('Error saving. Please try again.')
  }
}

// With undo action
toast('Email archived', {
  action: {
    label: 'Undo',
    onClick: () => undo(),
  },
})
</script>
```

Add `<Toaster />` in the root layout (app.vue or layouts/default.vue):
```vue
<script setup>
import { Toaster } from 'vue-sonner'
</script>
<template>
  <div>
    <slot />
    <Toaster richColors position="bottom-right" />
  </div>
</template>
```

---

## cn() — class composition

```ts
// lib/utils.ts (generated by init)
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

Usage in template:
```vue
<div :class="cn('base', isActive && 'active', props.class)" />
```

---

## Critical gotchas Vue + shadcn-vue

| Problem | Cause | Solution |
|---|---|---|
| `componentField` undefined | Auto-import conflict Form/vee-validate | Import explicitly `from '@/components/ui/form'` |
| `asChild` does not propagate props | Extra element wrapping the trigger | Use `as-child` directly on the component |
| Dialog does not close with Escape | `DialogContent` without `@keydown.esc` | Reka UI manages it — do not override |
| `v-model` on Select not reactive | Using `modelValue` without `update:modelValue` | Use `v-model` directly on the `Select` root |
| Skeleton wrong size | Dimensions do not mirror the actual content | Replicate h-* and w-* of the actual element |
| `Toaster` in child component | Reinitializes and loses state | Place only in root layout |
