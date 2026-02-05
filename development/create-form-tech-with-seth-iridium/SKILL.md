---
name: create-form
description: Set up hybrid client/server validated forms with Zod and React Hook Form. Use when creating forms with validation.
---

# Create Form

Creates forms with hybrid client + server validation using Zod schemas and React Hook Form.

## When to Use

- Creating any form with validation
- User asks to "add a form", "create a form", or "add validation"

## Core Pattern

1. **Same Zod schema** validates on both client and server
2. **Client:** Instant feedback with React Hook Form
3. **Server:** Security guarantee with `validateFormData()`
4. **Automatic error sync:** Server errors populate form fields

## Critical Rule: `<form>` vs `<fetcher.Form>`

```tsx
// ✅ CORRECT - Use <form> with manual fetcher.submit()
const onSubmit = (data: FormData) => {
    const formData = new FormData();
    formData.append('name', data.name);
    fetcher.submit(formData, { method: 'POST' });
};

<form onSubmit={handleSubmit(onSubmit)}>

// ❌ WRONG - Causes submission conflicts
<fetcher.Form onSubmit={handleSubmit(onSubmit)}>
```

## Implementation Steps

### Step 1: Define Zod Schema

**Location:** `app/lib/validations.ts`

```typescript
import { z } from 'zod';

export const contactFormSchema = z.object({
    name: z.string().min(1, 'Name is required'),
    email: z.string().min(1, 'Email is required').email('Invalid email'),
    message: z.string().min(10, 'Message must be at least 10 characters'),
});

export type ContactFormData = z.infer<typeof contactFormSchema>;
```

### Step 2: Server Action

```typescript
import type { Route } from './+types/contact';
import { data, redirect } from 'react-router';
import { zodResolver } from '@hookform/resolvers/zod';
import { validateFormData } from '~/lib/form-validation.server';
import { contactFormSchema, type ContactFormData } from '~/lib/validations';

export async function action({ request }: Route.ActionArgs) {
    const formData = await request.formData();
    const { data: validated, errors } = await validateFormData<ContactFormData>(
        formData,
        zodResolver(contactFormSchema)
    );

    if (errors) {
        return data({ errors }, { status: 400 });
    }

    // Process validated data
    await sendMessage(validated!);
    return redirect('/contact/success');
}
```

### Step 3: Client Form Component

```typescript
import { useFetcher } from 'react-router';
import { zodResolver } from '@hookform/resolvers/zod';
import { useValidatedForm } from '~/lib/form-hooks';
import { contactFormSchema, type ContactFormData } from '~/lib/validations';
import { TextInput } from '~/components/data-input/TextInput';
import { Textarea } from '~/components/data-input/Textarea';
import { Button } from '~/components/actions/Button';
import { Alert } from '~/components/feedback/Alert';

export default function ContactPage() {
    const fetcher = useFetcher();

    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useValidatedForm<ContactFormData>({
        resolver: zodResolver(contactFormSchema),
        errors: fetcher.data?.errors,  // Auto-syncs server errors
    });

    const onSubmit = (data: ContactFormData) => {
        const formData = new FormData();
        formData.append('name', data.name);
        formData.append('email', data.email);
        formData.append('message', data.message);
        fetcher.submit(formData, { method: 'POST' });
    };

    const isLoading = fetcher.state === 'submitting';

    return (
        <>
            <title>Contact | Iridium</title>

            {fetcher.data?.error && (
                <Alert status="error">{fetcher.data.error}</Alert>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <TextInput
                    {...register('name')}
                    label="Name"
                    error={errors.name?.message}
                    required
                />

                <TextInput
                    {...register('email')}
                    label="Email"
                    type="email"
                    error={errors.email?.message}
                    required
                />

                <Textarea
                    {...register('message')}
                    label="Message"
                    rows={5}
                    error={errors.message?.message}
                    required
                />

                <Button type="submit" loading={isLoading}>
                    Send Message
                </Button>
            </form>
        </>
    );
}
```

## Two Types of Errors

### Field-Level Errors (Validation)

```tsx
<TextInput
    {...register('email')}
    error={errors.email?.message}  // Shows inline with field
/>
```

### Form-Level Errors (Business Logic)

```tsx
{fetcher.data?.error && (
    <Alert status="error">{fetcher.data.error}</Alert>
)}
```

## Common Schema Patterns

### Optional Fields

```typescript
z.string().optional()
z.string().optional().or(z.literal(''))  // Allow empty string
```

### Conditional Validation

```typescript
z.object({
    hasAddress: z.boolean(),
    address: z.string().optional(),
}).refine(
    (data) => !data.hasAddress || data.address,
    { message: 'Address required', path: ['address'] }
);
```

### File Upload

```typescript
z.custom<FileList>()
    .refine((files) => files?.length > 0, 'File required')
    .refine((files) => files?.[0]?.size < 5_000_000, 'Max 5MB')
```

## Anti-Patterns

- ❌ Using `<fetcher.Form>` with `handleSubmit` (causes conflicts)
- ❌ Duplicating validation logic (use same schema everywhere)
- ❌ Trusting client-only validation
- ❌ Manual error syncing (use `useValidatedForm`)
- ❌ Missing `required` attribute for accessibility

## Templates

- [Form Template](./templates/form.tsx)
- [Schema Template](./templates/schema.ts)

## Full Reference

See `.github/instructions/form-validation.instructions.md` for comprehensive documentation.
