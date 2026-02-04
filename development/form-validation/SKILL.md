---
name: form-validation
description: Validates forms using React Hook Form and Zod. Use when creating forms with validation, handling form state, showing error messages, or implementing multi-step forms. Includes schema patterns and Controller usage.
---

# Form Validation Skill

## Instructions

1. Use React Hook Form with Zod resolver
2. Set `mode: 'onChange'` for real-time validation
3. Use Korean error messages
4. Wrap inputs with `Controller` component

## Quick Start

```tsx
import { useForm, Controller } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(2, '2자 이상 입력해주세요.'),
  email: z.string().email('유효한 이메일을 입력해주세요.'),
})

type FormData = z.infer<typeof schema>

const { control, handleSubmit, formState: { errors, isValid } } = useForm<FormData>({
  resolver: zodResolver(schema),
  mode: 'onChange',
})
```

## Controller Pattern

```tsx
<Controller
  name="title"
  control={control}
  render={({ field, fieldState }) => (
    <input {...field} className={fieldState.error ? 'border-red-500' : ''} />
  )}
/>
```

For complete schema patterns, input components, and Zod 4.x migration notes, see [reference.md](reference.md).
