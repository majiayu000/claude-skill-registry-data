---
name: veevalidate-form-validator
description: This skill should be used when the user asks to "create a form", "add validation", "handle form submission", "use VeeValidate", or when creating login, signup, or data entry forms in Nuxt.js/Vue 3. Enforces VeeValidate + Zod pattern.
---

# VeeValidate + Zod Form Validator

## Activation Triggers

This skill activates when:
- Creating form components
- Mentioning "form", "validation", "input"
- Writing `<form>` or v-model
- Handling user input

## Required Pattern

```vue
<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'

// Define schema with Zod
const schema = toTypedSchema(
  z.object({
    email: z.string().email('Invalid email'),
    password: z.string().min(8, 'Password too short'),
  })
)

// Create form with VeeValidate
const { handleSubmit, errors, defineField } = useForm({
  validationSchema: schema,
})

// Define reactive fields
const [email, emailAttrs] = defineField('email')
const [password, passwordAttrs] = defineField('password')

// Type-safe submit handler
const onSubmit = handleSubmit((values) => {
  // values is typed: { email: string, password: string }
  console.log(values.email, values.password)
})
</script>

<template>
  <form @submit="onSubmit">
    <div>
      <label for="email">Email</label>
      <input
        id="email"
        v-model="email"
        v-bind="emailAttrs"
        type="email"
        aria-describedby="email-error"
      />
      <span v-if="errors.email" id="email-error" class="error" role="alert">
        {{ errors.email }}
      </span>
    </div>

    <div>
      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        v-bind="passwordAttrs"
        type="password"
        aria-describedby="password-error"
      />
      <span v-if="errors.password" id="password-error" class="error" role="alert">
        {{ errors.password }}
      </span>
    </div>

    <button type="submit">Submit</button>
  </form>
</template>
```

## Forbidden Patterns

```vue
<!-- WRONG: No validation -->
<input v-model="email" />
<button @click="submit">Submit</button>

<!-- WRONG: Manual validation -->
<input v-model="email" @blur="validateEmail" />

<!-- WRONG: Template-only validation -->
<input v-model="email" :class="{ error: !isValidEmail }" />
```

## Complex Form Example

```vue
<script setup lang="ts">
import { useForm, useFieldArray } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { z } from 'zod'

const schema = toTypedSchema(
  z.object({
    name: z.string().min(1, 'Name required'),
    email: z.string().email(),
    role: z.enum(['admin', 'user', 'guest']),
    skills: z.array(z.object({
      name: z.string().min(1),
      level: z.number().min(1).max(5),
    })).min(1, 'At least one skill required'),
  })
)

const { handleSubmit, errors, defineField, values } = useForm({
  validationSchema: schema,
  initialValues: {
    name: '',
    email: '',
    role: 'user',
    skills: [{ name: '', level: 1 }],
  },
})

const { fields, push, remove } = useFieldArray('skills')

const [name, nameAttrs] = defineField('name')
const [email, emailAttrs] = defineField('email')
const [role, roleAttrs] = defineField('role')
</script>
```

## Error Display Pattern

```vue
<!-- Inline errors -->
<div class="field">
  <label for="email">Email</label>
  <input
    id="email"
    v-model="email"
    v-bind="emailAttrs"
    :class="{ 'border-red-500': errors.email }"
    aria-invalid="errors.email ? 'true' : undefined"
    aria-describedby="email-error"
  />
  <Transition name="fade">
    <p v-if="errors.email" id="email-error" class="text-red-500 text-sm" role="alert">
      {{ errors.email }}
    </p>
  </Transition>
</div>
```

## Async Validation

```typescript
const schema = toTypedSchema(
  z.object({
    username: z.string()
      .min(3)
      .refine(async (val) => {
        const response = await $fetch(`/api/check-username?q=${val}`)
        return response.available
      }, 'Username already taken'),
  })
)
```

## Validation Report

```
FORM VALIDATION CHECK

File: components/LoginForm.vue

 VeeValidate: useForm imported and used
 Zod schema: Defined with proper types
 Error display: Errors shown with role="alert"
 Accessibility: Labels and aria attributes present
 Type safety: Form values properly typed

Issues:
 Line 23: Missing aria-describedby on password input
 Line 34: Error message not accessible (missing role="alert")

Summary: 2 issues to fix
```
