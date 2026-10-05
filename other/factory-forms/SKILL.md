---
name: factory-forms
description: Form conventions distilled across builds. react-hook-form + Zod via resolver (Mantine or shadcn variant), three Zod schema variants (server strict / client lenient / patch), drawer-CRUD with mode union, field-registry pattern for multi-step forms, declarative conditional visibility with auto-cleanup, debounced auto-save with dirty tracking, masked inputs for sensitive fields with KMS encryption-at-rest, dynamic field arrays with constraints, S3 presigned-URL upload flow. Read when scaffolding any form — single-step CRUD or multi-step complex intake.
---

# Factory forms

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the react-hook-form / Zod / Mantine or shadcn shape), and **Failure mode** when there's one to name. Sections that are pure style with no deeper truth are marked `Recipe only`.

## Stack

**Recipe only.**

- **react-hook-form** — form state, validation, submission
- **Zod** — schemas
- **Resolver** — `mantine-form-zod-resolver` (Mantine) or `@hookform/resolvers/zod` (shadcn)
- **Server submission** — server action or tRPC mutation (see `factory-api.md`)

## Three Zod schema variants — server strict, client lenient, patch partial

**Principle.** Maintain three schema variants per entity: server strict, client lenient, patch partial. Don't try to unify them.

**Why.** HTML inputs in controlled React forms initialize to `''`; the server expects `null` or a valid value. A unified schema accommodates both by sprinkling `.or(z.literal(''))` everywhere, which leaves the server schema enforcing nothing. Three schemas keeps each contract sharp: the server enforces real shape, the client tolerates the input flux, the patch shape is structurally partial (only-what-changed). Cost: more schema. Benefit: each layer's invariants stay enforceable.

**Recipe.**

```ts
// features/customers/schema.ts

// Server input — strict types, server enforces these
export const customerInputSchema = z.object({
  orgId: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  phone: z.string().regex(/^\+?[0-9-]+$/),
  industry: z.enum(['retail', 'wholesale', 'manufacturing']),
});

// Client form — lenient, accepts empty strings (controlled-input compat)
export const customerFormSchema = z.object({
  orgId: z.string().uuid(),
  name: z.string().min(1, 'Required'),
  email: z.string().email().or(z.literal('')).optional(),
  phone: z.string().or(z.literal('')).optional(),
  industry: z.enum(['retail', 'wholesale', 'manufacturing']).or(z.literal('')).optional(),
});

// Patch — partial updates
export const customerPatchSchema = customerInputSchema.partial();
```

The two are deliberately different — don't try to unify.

## Drawer-CRUD mode union — drawer edits only the row it was opened from

**Principle.** Model the drawer as a discriminated union of states; the drawer only edits the row it was opened from.

**Why.** A drawer is a small modal state machine: closed / creating / editing-row-X. A boolean `isOpen` + nullable `editingId` lets impossible states represent themselves (open with no id, closed with an id). The discriminated union makes those states unrepresentable. The "edits only the row it was opened from" rule keeps the drawer simple — relations open their own drawers, so each drawer has one shape and one source of state.

**Recipe.**

```tsx
type CustomerDrawerMode =
  | { kind: 'closed' }
  | { kind: 'create' }
  | { kind: 'edit'; customer: Customer };

const [mode, setMode] = useState<CustomerDrawerMode>({ kind: 'closed' });
const form = useForm({ resolver: zodResolver(customerFormSchema) });

// Imperative form sync when mode changes
useEffect(() => {
  if (mode.kind === 'edit') {
    form.reset(toFormValues(mode.customer));
  } else if (mode.kind === 'create') {
    form.reset(emptyCustomerFormValues);
  }
}, [mode.kind, mode.kind === 'edit' ? mode.customer.id : null]);
```

## Field registry — metadata as the single source of truth

**Principle.** Each field is one entry in a registry; the form renderer reads metadata, not hardcoded JSX.

**Why.** Long forms (50+ fields) hand-rendered per-field accumulate duplication that diverges silently — one field gets a tooltip, another doesn't, validation drifts between schema and component. A registry with field metadata (label, type, validation, AI context, conditional visibility) collapses all of this into one source. The renderer reads it; the schema reads it; the AI context layer reads it. One edit propagates.

**Recipe.**

```ts
// src/lib/fields/registry.ts
export const FIELDS = {
  company_name: {
    label: 'Company name',
    type: 'text',
    required: true,
    validation: z.string().min(1),
    aiContext: 'Legal entity name as registered',
  },
  ein: {
    label: 'EIN',
    type: 'masked',
    mask: '99-9999999',
    validation: z.string().regex(/^\d{2}-\d{7}$/),
    sensitive: true,
  },
  // ... 70+ fields
} as const satisfies Record<string, FieldDef>;
```

See `factory-llm-workflows.md` for the AI-context angle.

## Modular section files from day one

**Principle.** Multi-step forms split into section files from the first commit; never write the monolith first.

**Why.** "We'll refactor when it's painful" is the lie every monolith tells. Forms grow predictably — section by section, field by field — and a 1,500-line single file is a refactor liability whose cost is paid in panic, not in steady increments. Splitting from day one is free; splitting at 1,500 lines costs a week.

**Recipe.**

```
src/components/forms/sections/
├── Section1_CompanyInformation.tsx
├── Section2_Regulatory.tsx
├── Section3_Banking.tsx
└── ...
```

Each file 500-1500 lines is fine.

**Failure mode.** Duezy's original 1,592-line form. Refactor took a week; the same content split from day one would have cost nothing.

## Conditional visibility implies auto-cleanup

**Principle.** When a conditional field becomes hidden, clear its value. Don't submit data the user can't see.

**Why.** Stale conditional data is a silent correctness bug. The user fills `beneficial_owner_2`, changes `has_multiple_owners` to `no`, and submits — without auto-cleanup, the hidden `beneficial_owner_2` data goes to the server. The server has no way to know that field shouldn't have been submitted; the data flows into reports and audit logs as if it were intentional. Auto-cleanup makes the form data match the form display.

**Recipe.**

```ts
// src/lib/utils/conditional-visibility.ts
export type VisibilityRule = {
  field: string;
  showWhen: (values: FormValues) => boolean;
};

export const VISIBILITY_RULES: VisibilityRule[] = [
  { field: 'beneficial_owner_2', showWhen: (v) => v.has_multiple_owners === 'yes' },
  // ...
];

export function useAutoCleanup(form: UseFormReturn, rules: VisibilityRule[]) {
  useEffect(() => {
    return form.watch((values) => {
      for (const rule of rules) {
        if (!rule.showWhen(values) && values[rule.field] != null) {
          form.setValue(rule.field, undefined);
        }
      }
    }).unsubscribe;
  }, [form, rules]);
}
```

## Debounced auto-save accepts the lenient schema

**Principle.** Auto-save accepts the lenient schema; submission re-validates against strict.

**Why.** Auto-save fires on every blur — including blurs where the field is empty or half-typed. If auto-save rejected invalid input, every interruption would lose progress. The lenient schema means "this is recoverable state"; the strict schema means "this is the contract for done." The two layers split the responsibility cleanly.

**Recipe.**

```ts
const DEBOUNCE_MS = 2000;
const SAFETY_INTERVAL_MS = 3 * 60 * 1000;

useEffect(() => {
  const sub = form.watch(() => {
    debouncedSave(form.getValues());
  });
  return () => sub.unsubscribe();
}, [form]);

// Safety net — flush every 3 minutes even if user doesn't blur
useInterval(() => flushSave(form.getValues()), SAFETY_INTERVAL_MS);
```

Server side, accept the lenient schema for auto-save endpoints. Validate against strict only on submission.

## Masked inputs — masked in display, encrypted at rest

**Principle.** Sensitive fields (SSN, EIN, financial accounts, PHI): masked in display, encrypted at rest, decrypted only at the specific handler that needs plaintext.

**Why.** Plaintext sensitive data in logs, audit trails, error reports, or admin UIs is one screenshot away from a breach. Masking the input protects the display channel; KMS encryption at rest protects the storage channel; decryption-at-the-call-site keeps the exposure surface as small as possible. Each layer is cheap individually; the composition is the actual defense.

**Recipe.**

```tsx
<MaskedInput
  mask="999-99-9999"
  placeholder="123-45-6789"
  {...form.register('ssn')}
/>
```

For SSN / government ID / financial accounts: encrypt at rest with KMS (see `factory-security.md` on KMS-at-rest). Mask in display; decrypt only at the specific handler that needs plaintext.

## Dynamic field arrays with max-count

**Recipe only** — pattern for variable-count entries like contacts or beneficial owners.

```tsx
const { fields, append, remove } = useFieldArray({
  control: form.control,
  name: 'contacts',
  rules: { maxLength: { value: 10, message: 'Max 10 contacts' } },
});
```

Max-count constraint enforces business rules at the form layer (mirror on the server too).

## S3 presigned-URL upload — direct, never proxied

**Principle.** Direct-to-S3 with presigned URLs; never proxy uploads through your server.

**Why.** Proxying uploads makes your server the bandwidth bottleneck and the file-size cap — Vercel and most serverless platforms cap body size at 4-10MB. Presigned URLs delegate the upload to S3 directly; your server only issues the URL and records the result. The user gets the full S3 bandwidth; you get no body-size headaches.

**Recipe.**

```ts
// 1. Generate URL (server action)
const { uploadUrl, fileKey } = await generateUploadUrl({ contentType, filename });

// 2. Upload directly to S3 (client)
await fetch(uploadUrl, { method: 'PUT', body: file, headers: { 'Content-Type': contentType } });

// 3. Confirm upload (server action — records the fileKey)
await confirmUpload({ formId, fieldId, fileKey });
```

## `useTransition` for async submission

**Principle.** Gate the submit button on `isPending`; one mutation in flight at a time.

**Why.** Without a gate, a fast double-click submits twice. The duplicate write may succeed (creating two rows), may fail (one of them violates a unique constraint with no clear error path), or may race (interleaved state on the server). `isPending` from `useTransition` makes the gate declarative and removes the failure mode.

**Recipe.**

```tsx
const [isPending, startTransition] = useTransition();

const onSubmit = (values: FormValues) => {
  startTransition(async () => {
    const result = await createCustomer(values);
    if (result.error) { toast.error(result.error); return; }
    setMode({ kind: 'closed' });
    queryClient.invalidateQueries({ queryKey: ['customers'] });
  });
};
```

## Question numbering via context

**Recipe only** — UX detail. Numbers update consistently when sections reorder.

```tsx
const QuestionNumberingContext = createContext<{ next: () => number }>(null);

export function QuestionLabel({ children }: { children: ReactNode }) {
  const { next } = useContext(QuestionNumberingContext);
  const num = useMemo(next, [next]);
  return <Label>{num}. {children}</Label>;
}
```

## Review section — visible fields only, flag the gaps

**Principle.** The review section shows only the fields the user could see, and flags only the gaps among those.

**Why.** A review section that lists all registry fields (including conditionally-hidden ones) confuses the user by showing fields they were never asked about. Worse, it flags empty "gaps" that the user couldn't have filled. The fix is the same conditional-visibility computation that the form uses; the review just walks the visible set.

**Recipe.**

```tsx
export function ReviewSection({ values, registry, visibilityRules }: ReviewProps) {
  const visibleFields = computeVisibleFields(registry, visibilityRules, values);
  const gaps = visibleFields.filter((f) => isEmpty(values[f.id]));
  return (
    <>
      {gaps.length > 0 && <Alert>You have {gaps.length} incomplete answers</Alert>}
      {visibleFields.map((f) => <ReviewRow key={f.id} field={f} value={values[f.id]} />)}
    </>
  );
}
```

## Source patterns

Duezy (field registry, modular section files, lenient/strict Zod variants, conditional visibility + auto-cleanup, debounced auto-save with dirty tracking, masked inputs, dynamic field arrays, S3 presigned uploads, question numbering context, review section with gap detection, unified progress calculator), kairos (drawer mode union, `useTransition` submission, Mantine + schemaResolver pattern, per-context Zod variants), fleet-advisor (shadcn + react-hook-form pattern).
