---
name: TanStack Form Patterns
description: >-
  Auto-enforce TanStack Form best practices with Zod validation. Activates when
  creating forms, handling form state, implementing validation, or building
  input components in React applications.
version: 1.0.0
---

# TanStack Form Patterns

This skill enforces TanStack Form best practices for type-safe forms with Zod validation.

## Basic Form Setup

```typescript
import { useForm } from '@tanstack/react-form'
import { zodValidator } from '@tanstack/zod-form-adapter'
import { z } from 'zod'

const postSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  content: z.string().min(10, 'Content must be at least 10 characters'),
  published: z.boolean().default(false),
  tags: z.array(z.string()).min(1, 'At least one tag required'),
})

type PostFormData = z.infer<typeof postSchema>

export function PostForm({ onSubmit }: { onSubmit: (data: PostFormData) => void }) {
  const form = useForm({
    defaultValues: {
      title: '',
      content: '',
      published: false,
      tags: [],
    } satisfies PostFormData,
    onSubmit: async ({ value }) => {
      onSubmit(value)
    },
    validatorAdapter: zodValidator(),
    validators: {
      onChange: postSchema,
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        form.handleSubmit()
      }}
    >
      {/* Form fields */}
    </form>
  )
}
```

## Field Components

### Text Input Field
```typescript
<form.Field
  name="title"
  children={(field) => (
    <div className="field">
      <label htmlFor={field.name}>Title</label>
      <input
        id={field.name}
        name={field.name}
        value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur}
        aria-invalid={field.state.meta.errors.length > 0}
        aria-describedby={`${field.name}-error`}
      />
      {field.state.meta.isTouched && field.state.meta.errors.length > 0 && (
        <span id={`${field.name}-error`} className="error">
          {field.state.meta.errors[0]}
        </span>
      )}
    </div>
  )}
/>
```

### Textarea Field
```typescript
<form.Field
  name="content"
  children={(field) => (
    <div className="field">
      <label htmlFor={field.name}>Content</label>
      <textarea
        id={field.name}
        name={field.name}
        value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur}
        rows={5}
      />
      {field.state.meta.isTouched && field.state.meta.errors.length > 0 && (
        <span className="error">{field.state.meta.errors[0]}</span>
      )}
    </div>
  )}
/>
```

### Checkbox Field
```typescript
<form.Field
  name="published"
  children={(field) => (
    <div className="field-checkbox">
      <input
        id={field.name}
        type="checkbox"
        checked={field.state.value}
        onChange={(e) => field.handleChange(e.target.checked)}
      />
      <label htmlFor={field.name}>Published</label>
    </div>
  )}
/>
```

### Select Field
```typescript
<form.Field
  name="category"
  children={(field) => (
    <div className="field">
      <label htmlFor={field.name}>Category</label>
      <select
        id={field.name}
        value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur}
      >
        <option value="">Select category...</option>
        <option value="tech">Technology</option>
        <option value="business">Business</option>
        <option value="lifestyle">Lifestyle</option>
      </select>
    </div>
  )}
/>
```

## Array Fields

```typescript
const tagsSchema = z.array(z.string().min(1)).min(1, 'At least one tag')

<form.Field
  name="tags"
  mode="array"
  children={(field) => (
    <div className="field">
      <label>Tags</label>
      {field.state.value.map((_, index) => (
        <div key={index} className="tag-input">
          <form.Field
            name={`tags[${index}]`}
            children={(tagField) => (
              <input
                value={tagField.state.value}
                onChange={(e) => tagField.handleChange(e.target.value)}
              />
            )}
          />
          <button
            type="button"
            onClick={() => field.removeValue(index)}
          >
            Remove
          </button>
        </div>
      ))}
      <button
        type="button"
        onClick={() => field.pushValue('')}
      >
        Add Tag
      </button>
      {field.state.meta.errors.length > 0 && (
        <span className="error">{field.state.meta.errors[0]}</span>
      )}
    </div>
  )}
/>
```

## Async Validation

```typescript
const usernameSchema = z.string().min(3)

<form.Field
  name="username"
  validators={{
    onChange: usernameSchema,
    onChangeAsyncDebounceMs: 500,
    onChangeAsync: async ({ value }) => {
      const exists = await checkUsernameExists(value)
      if (exists) {
        return 'Username already taken'
      }
      return undefined
    },
  }}
  children={(field) => (
    <div className="field">
      <label htmlFor={field.name}>Username</label>
      <input
        id={field.name}
        value={field.state.value}
        onChange={(e) => field.handleChange(e.target.value)}
        onBlur={field.handleBlur}
      />
      {field.state.meta.isValidating && <span>Checking...</span>}
      {field.state.meta.errors.length > 0 && (
        <span className="error">{field.state.meta.errors[0]}</span>
      )}
    </div>
  )}
/>
```

## Form with Mutation

```typescript
import { useCreatePost } from '@/features/posts/hooks'

export function CreatePostForm() {
  const createPost = useCreatePost()

  const form = useForm({
    defaultValues: { title: '', content: '', published: false },
    onSubmit: async ({ value }) => {
      await createPost.mutateAsync(value)
    },
    validatorAdapter: zodValidator(),
    validators: {
      onChange: postSchema,
    },
  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); form.handleSubmit() }}>
      {/* Fields */}
      <form.Subscribe
        selector={(state) => [state.canSubmit, state.isSubmitting]}
        children={([canSubmit, isSubmitting]) => (
          <button type="submit" disabled={!canSubmit || isSubmitting}>
            {isSubmitting ? 'Creating...' : 'Create Post'}
          </button>
        )}
      />
      {createPost.isError && (
        <div className="error">{createPost.error.message}</div>
      )}
    </form>
  )
}
```

## Edit Form with Initial Data

```typescript
interface EditPostFormProps {
  post: Post
  onSuccess: () => void
}

export function EditPostForm({ post, onSuccess }: EditPostFormProps) {
  const updatePost = useUpdatePost()

  const form = useForm({
    defaultValues: {
      title: post.title,
      content: post.content,
      published: post.published,
    },
    onSubmit: async ({ value }) => {
      await updatePost.mutateAsync({ id: post.id, ...value })
      onSuccess()
    },
    validatorAdapter: zodValidator(),
    validators: {
      onChange: postSchema,
    },
  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); form.handleSubmit() }}>
      {/* Fields */}
    </form>
  )
}
```

## Reusable Field Component

```typescript
// components/ui/FormField.tsx
import type { FieldApi } from '@tanstack/react-form'

interface FormFieldProps<T> {
  field: FieldApi<any, any, any, any, T>
  label: string
  type?: 'text' | 'email' | 'password' | 'textarea'
}

export function FormField<T extends string>({
  field,
  label,
  type = 'text',
}: FormFieldProps<T>) {
  const hasError = field.state.meta.isTouched && field.state.meta.errors.length > 0

  const inputProps = {
    id: field.name,
    name: field.name,
    value: field.state.value,
    onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
      field.handleChange(e.target.value as T),
    onBlur: field.handleBlur,
    'aria-invalid': hasError,
    'aria-describedby': hasError ? `${field.name}-error` : undefined,
  }

  return (
    <div className="form-field">
      <label htmlFor={field.name}>{label}</label>
      {type === 'textarea' ? (
        <textarea {...inputProps} />
      ) : (
        <input type={type} {...inputProps} />
      )}
      {hasError && (
        <span id={`${field.name}-error`} className="error" role="alert">
          {field.state.meta.errors[0]}
        </span>
      )}
    </div>
  )
}
```

## Form State Subscription

```typescript
// Subscribe to specific form state
<form.Subscribe
  selector={(state) => ({
    canSubmit: state.canSubmit,
    isSubmitting: state.isSubmitting,
    isDirty: state.isDirty,
    errors: state.errors,
  })}
  children={({ canSubmit, isSubmitting, isDirty, errors }) => (
    <div>
      {isDirty && <span>Unsaved changes</span>}
      {errors.length > 0 && <span>Form has errors</span>}
      <button type="submit" disabled={!canSubmit || isSubmitting}>
        {isSubmitting ? 'Saving...' : 'Save'}
      </button>
    </div>
  )}
/>
```

## Conventions to Enforce

1. **Zod for validation** - Always use `zodValidator()` adapter
2. **Type inference** - Use `z.infer<typeof schema>` for form types
3. **Accessible forms** - Include labels, aria attributes, error associations
4. **Touch-based errors** - Show errors only after field interaction
5. **Submit handling** - Prevent default, use `form.handleSubmit()`
6. **Mutation integration** - Connect forms to TanStack Query mutations
7. **Default values** - Always provide with `satisfies` type check

## Anti-Patterns to Block

```typescript
// ❌ WRONG: No validation
const form = useForm({
  defaultValues: { title: '' },
  onSubmit: ({ value }) => save(value),
})

// ✅ CORRECT: Zod validation
const form = useForm({
  defaultValues: { title: '' },
  validatorAdapter: zodValidator(),
  validators: { onChange: schema },
  onSubmit: ({ value }) => save(value),
})

// ❌ WRONG: Missing error display
<input value={field.state.value} onChange={(e) => field.handleChange(e.target.value)} />

// ✅ CORRECT: Error handling
<input
  value={field.state.value}
  onChange={(e) => field.handleChange(e.target.value)}
  aria-invalid={field.state.meta.errors.length > 0}
/>
{field.state.meta.errors[0] && <span className="error">{field.state.meta.errors[0]}</span>}

// ❌ WRONG: No accessibility
<div>
  <span>Email</span>
  <input />
</div>

// ✅ CORRECT: Proper labeling
<div>
  <label htmlFor="email">Email</label>
  <input id="email" aria-describedby="email-error" />
</div>
```
