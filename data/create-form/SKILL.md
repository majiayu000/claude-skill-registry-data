---
name: create-form
description: Set up hybrid client/server validated forms with Zod and React Hook Form. Use when creating forms with validation.
---

# Create Form

## When to Use

- Creating any form with validation
- User asks to "add a form" or "create a form"

## Critical Rule

```tsx
// CORRECT - Use <form> with manual fetcher.submit()
<form onSubmit={handleSubmit(onSubmit)}>

// WRONG - Causes submission conflicts
<fetcher.Form onSubmit={handleSubmit(onSubmit)}>
```

## Core Pattern

1. **Same Zod schema** on client and server
2. **Client:** Instant feedback with React Hook Form
3. **Server:** Security with `validateFormData()`
4. **Auto error sync:** Server errors populate form fields

## Quick Start

### 1. Schema (`app/lib/validations.ts`)

```typescript
import { z } from 'zod';

export const contactFormSchema = z.object({
    name: z.string().min(1, 'Name is required'),
    email: z.string().email('Invalid email'),
});

export type ContactFormData = z.infer<typeof contactFormSchema>;
```

### 2. Server Action

```typescript
import { validateFormData } from '~/lib/form-validation.server';
import { zodResolver } from '@hookform/resolvers/zod';

export async function action({ request }: Route.ActionArgs) {
    const formData = await request.formData();
    const { data, errors } = await validateFormData<ContactFormData>(
        formData,
        zodResolver(contactFormSchema)
    );

    if (errors) return data({ errors }, { status: 400 });

    await processData(data!);
    return redirect('/success');
}
```

### 3. Client Form

```tsx
import { useFetcher } from 'react-router';
import { useValidatedForm } from '~/lib/form-hooks';

export default function ContactPage() {
    const fetcher = useFetcher();
    const { register, handleSubmit, formState: { errors } } = useValidatedForm({
        resolver: zodResolver(contactFormSchema),
        errors: fetcher.data?.errors,
    });

    const onSubmit = (data: ContactFormData) => {
        const formData = new FormData();
        formData.append('name', data.name);
        fetcher.submit(formData, { method: 'POST' });
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <TextInput {...register('name')} error={errors.name?.message} />
            <Button type="submit">Submit</Button>
        </form>
    );
}
```

## Checklist

1. [ ] Define Zod schema in `app/lib/validations.ts`
2. [ ] Add server action with `validateFormData()`
3. [ ] Use `useValidatedForm` hook in component
4. [ ] Use `<form>` (not `<fetcher.Form>`) with `handleSubmit`

## Templates

- [Form Template](./templates/form.tsx)
- [Schema Template](./templates/schema.ts)

## Full Reference

See `.github/instructions/form-validation.instructions.md` for:
- Field-level vs form-level errors
- Conditional validation
- File uploads
- Complex schema patterns
