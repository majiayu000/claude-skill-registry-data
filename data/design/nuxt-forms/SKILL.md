---
name: nuxt-forms
description: Form handling with XForm component and useFormBuilder. Use when creating forms, handling validation errors, managing form state, or building form-based slideovers and modals.
---

# Nuxt Forms

Form handling with XForm component and validation error display.

## Core Concepts

**[forms.md](references/forms.md)** - XForm, useFormBuilder, validation patterns

## XForm Component

```vue
<XForm
  ref="formRef"
  url="/api/posts"
  method="POST"
  :data="formData"
  :waiting="waitingFor.posts.creating"
  @submit="onSubmit"
  @success="onSuccess"
  @error="onError"
>
  <UFormField label="Title" name="title" :error="form?.errors.first('title')">
    <UInput v-model="formData.title" />
  </UFormField>

  <template #actions>
    <UButton type="submit" label="Create" :loading="form?.processing" />
  </template>
</XForm>
```

## Form Data Pattern

```typescript
const formData = ref<CreatePostData>({
  title: '',
  content: '',
  authorId: '',
  isDraft: true,
})

const onSubmit = async (data: CreatePostData) => {
  await createPostAction(data)
}

const onSuccess = () => {
  emits('close', true)
}
```

## Validation Errors

```typescript
// Access errors
form.errors.has('title')       // boolean
form.errors.first('title')     // string | undefined
form.errors.get('title')       // string[] | undefined
form.errors.any()              // boolean

// Display in template
<UFormField label="Title" name="title" :error="form?.errors.first('title')">
```
