---
name: factory-forms-builder
description: Use when building multi-step forms, complex intake flows, drawer-CRUD forms, or anything beyond a one-shot Mantine form. Carries the factory's form conventions — react-hook-form + Zod via resolver, three Zod variants (server strict / client lenient / patch), modular section files from day one, field registry for AI-context-aware multi-step forms, declarative conditional visibility with auto-cleanup, debounced auto-save with dirty tracking, masked inputs for sensitive fields, dynamic field arrays, S3 presigned upload, `useTransition` for async submission, question numbering via context, review section with gap detection. Outputs form code that fits the house style — not bespoke form-state machinery.
---

Apply the **forms-builder** specialist workflow. Build forms grounded in the factory's conventions, not generic react-hook-form code. Load `factory-forms` through the host's skill capability when needed.

## How to think (in order)

1. **What kind of form?** Pick one:
   - **Single-step drawer-CRUD form** — create/edit one entity → use the drawer mode union from `factory-frontend.md`
   - **Single-step page form** — login, settings, simple intake → vanilla react-hook-form
   - **Multi-step wizard** — onboarding, complex intake → section files + field registry
   - **Inline edit** — DataTable cell editing → different pattern, see `factory-frontend.md`

2. **How many fields?**
   - **< 10** — inline schemas, hand-written JSX
   - **10–30** — section files but no registry needed
   - **30+** or AI-context-aware — field registry

3. **Schemas — three variants** (see `factory-forms.md`):
   - **Server input** — strict (real types, no empty-string fallbacks)
   - **Client form** — lenient (accepts empty strings because controlled inputs default to `''`)
   - **Patch** — partial input for updates

4. **Conditional visibility?** If any field's display depends on another's value:
   - Declarative rules in `src/lib/utils/conditional-visibility.ts`
   - **Auto-cleanup** when parent toggles off — set hidden child's value to `undefined`
   - Otherwise stale conditional data sneaks into submissions

5. **Sensitive fields?** SSN, EIN, government IDs, financial accounts:
   - Masked input (`mask="99-9999999"` etc.)
   - KMS encryption at rest — see `factory-security.md`
   - Mask in display, decrypt only at the handler that returns plaintext

6. **Auto-save?** If the form takes more than a couple minutes to fill out:
   - 2s debounce on field blur
   - 3min safety-net interval flush
   - Server accepts the lenient schema during auto-save; strict schema on submission

7. **Dynamic field arrays?** (contacts, beneficial owners, line items)
   - `useFieldArray` from react-hook-form
   - Max-count rule via `rules: { maxLength: { value: N, message: '...' } }`
   - Add/remove buttons; consider drag-reorder for ordered arrays

8. **File uploads?** Direct-to-S3 with presigned URLs (don't proxy through your server):
   - Server action generates upload URL
   - Client PUTs file to S3
   - Server action confirms upload (records fileKey)

9. **Submission UX?**
   - `useTransition` wrapping the async submit
   - `isPending` gates the submit button
   - Toast on success / error
   - Invalidate the right TanStack Query keys on success

## Reference: canonical drawer-CRUD form skeleton

```tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';   // or mantine-form-zod-resolver
import { customerFormSchema } from './schema';
import { useCreateCustomer, useUpdateCustomer } from './hooks';

type CustomerDrawerMode =
  | { kind: 'closed' }
  | { kind: 'create' }
  | { kind: 'edit'; customer: Customer };

export function CustomerDrawer({ mode, onClose }: { mode: CustomerDrawerMode; onClose: () => void }) {
  const form = useForm({
    resolver: zodResolver(customerFormSchema),
    defaultValues: emptyCustomerFormValues,
  });

  const createMutation = useCreateCustomer();
  const updateMutation = useUpdateCustomer();
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    if (mode.kind === 'edit') {
      form.reset(toFormValues(mode.customer));
    } else if (mode.kind === 'create') {
      form.reset(emptyCustomerFormValues);
    }
  }, [mode.kind, mode.kind === 'edit' ? mode.customer.id : null]);

  const onSubmit = form.handleSubmit((values) => {
    startTransition(async () => {
      const mutation = mode.kind === 'edit' ? updateMutation : createMutation;
      const result = await mutation.mutateAsync(values);
      if ('error' in result) { toast.error(result.error); return; }
      toast.success(mode.kind === 'edit' ? 'Updated' : 'Created');
      onClose();
    });
  });

  return (
    <Drawer opened={mode.kind !== 'closed'} onClose={onClose}>
      <form onSubmit={onSubmit}>
        {/* fields */}
        <Button type="submit" loading={isPending}>{mode.kind === 'edit' ? 'Save' : 'Create'}</Button>
      </form>
    </Drawer>
  );
}
```

## Reference: field registry shape (for ≥30-field forms)

```ts
// src/lib/fields/types.ts
export type FieldDef = {
  id: string;
  label: string;
  type: 'text' | 'email' | 'masked' | 'select' | 'date' | 'checkbox' | 'array';
  required?: boolean;
  validation: z.ZodTypeAny;
  options?: { value: string; label: string }[];
  mask?: string;
  sensitive?: boolean;
  aiContext?: string;     // for AI-augmented review / autofill
};

// src/lib/fields/sections/section-1-company.ts
export const SECTION_1_FIELDS: FieldDef[] = [
  { id: 'company_name', label: 'Legal name', type: 'text', required: true, validation: z.string().min(1) },
  { id: 'ein', label: 'EIN', type: 'masked', mask: '99-9999999', required: true, sensitive: true, validation: z.string().regex(/^\d{2}-\d{7}$/) },
  // ...
];
```

## Output format

```
## Restated request
<one sentence>

## Form shape
- Type: <drawer-CRUD / page / multi-step / inline edit>
- Field count: <count>
- Field registry: <yes / no — why>
- Conditional visibility: <yes / no>
- Auto-save: <yes / no>
- Sensitive fields: <list, with encryption strategy>

## Schemas
- Server input: <path>
- Client form: <path>
- Patch: <path>

## Files to create or modify
<bulleted with paths>

## Code
<organized by file>

## Conventions check
- Three Zod variants: <yes>
- Drawer mode union (if applicable): <yes>
- useTransition wrapping submit: <yes>
- Conditional auto-cleanup (if applicable): <yes>
- Sensitive fields encrypted at rest: <yes / N/A>

## Open questions
<things the user should confirm>
```

## What you do NOT do

- **Don't write a monolithic single-file form.** Modular section files from day one.
- **Don't unify server and client schemas.** Server strict, client lenient.
- **Don't leave stale conditional data in submissions.** Auto-cleanup on visibility change.
- **Don't proxy file uploads through your server.** Direct-to-S3 with presigned URLs.
- **Don't store SSN / PHI / government IDs in plaintext.** KMS-at-rest, mask in display.
- **Don't `await` the audit log on the submission path.** Fire-and-forget.
- **Don't skip `useTransition`.** Double-submission is a real bug class.
- **Don't reach for the field registry for a 5-field form.** Reserved for ≥30-field or AI-context-aware forms.

## When the request is too small for this framework

If the user asks to add one field to an existing form or change validation on a single field, do it directly. The framework is for new forms, new sections, or substantial form-state refactors.
