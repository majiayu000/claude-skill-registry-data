---
name: tac-forms
description: >-
  Load when building any form in tac-express. Covers the standard form pattern: react-hook-form + zod resolver + server actions + Violet Grid field components. Includes validation, error states, loading states, and the forbidden patterns.
---

# TAC Express — Form Authoring

## Stack

- **Validation:** `zod` schemas from `@workspace/types/schemas/`
- **Form state:** `react-hook-form` with `@hookform/resolvers/zod`
- **Submission:** Next.js Server Actions (`"use server"`)
- **UI primitives:** shadcn `<Input>`, `<Select>`, `<Textarea>`, `<Checkbox>` from `@workspace/ui`
- **NO axios, NO fetch wrappers** — server actions are the data path

---

## Scope — when this pattern applies

This pattern is **mandatory** for forms that live in `packages/ui/src/components/composed/` — the reusable UI surface. Every form component there must use react-hook-form + zod.

This pattern is **optional** for page-shell client components in `apps/*/app/**/*-client.tsx` that handle a single-field or single-purpose interaction. For those:

- Plain `useState` + inline validation is acceptable.
- The page shell is not reusable; pulling `react-hook-form` into `apps/*` either adds workspace deps (diverging from the `packages/ui` ownership pattern that V7CustomerForm and V7CreateShipmentWizard established) or forces a LAW-5 extraction into `packages/ui` for a single-route component. Both are churn for marginal benefit.

The boundary: **if more than two interrelated fields, OR if the form is intended for reuse across routes, extract to `packages/ui` and apply this pattern.** Single-field route-shell forms can stay inline.

| File | Why it lives where it does |
|---|---|
| `packages/ui/src/components/composed/customers/v7-customer-form.tsx` | Multi-field reusable form → **RHF + zod required** |
| `packages/ui/src/components/composed/shipments/v7-create-shipment-wizard.tsx` | Multi-step wizard with draft persistence → **RHF + zod required** |
| `apps/dashboard/app/track/track-search-client.tsx` | Single AWB regex, single route, no reuse → plain `useState` acceptable |
| `apps/dashboard/app/track/track-tabs-client.tsx` | Toggle-only state → plain `useState` acceptable |
| `apps/dashboard/app/ops-console/.../*-detail-client.tsx` | Page shell; inline edits delegate to dialogs that use RHF-backed forms from `packages/ui` |

This boundary resolves [#25](https://github.com/cargotapan-collab/tac-express/issues/25) — Option 3 from the architectural finding (RHF+zod scope = `packages/ui` reusable forms only).

---

## Standard Form Pattern

```tsx
// packages/ui/src/components/composed/[feature]/[feature]-form.tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { createShipmentSchema, type CreateShipmentInput } from "@workspace/types/schemas/shipment.schema"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@workspace/ui/components/primitives/form"
import { Input } from "@workspace/ui/components/primitives/input"
import { Button } from "@workspace/ui/components/primitives/button"

interface ShipmentFormProps {
  onSubmit: (data: CreateShipmentInput) => Promise<void>
  defaultValues?: Partial<CreateShipmentInput>
}

function ShipmentForm({ onSubmit, defaultValues }: ShipmentFormProps) {
  const form = useForm<CreateShipmentInput>({
    resolver: zodResolver(createShipmentSchema),
    defaultValues: {
      pieces: 1,
      ...defaultValues,
    },
  })

  const { isSubmitting, isValid } = form.formState

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="sender.name"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
                Sender Name
              </FormLabel>
              <FormControl>
                <Input data-slot="sender-name-input" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={isSubmitting || !isValid}
          data-slot="submit-button"
        >
          {isSubmitting ? "Saving..." : "Create Shipment"}
        </Button>
      </form>
    </Form>
  )
}

export { ShipmentForm }
```

---

## Server Action Pattern

```ts
// apps/dashboard/app/shipments/actions.ts
"use server"

import { revalidatePath } from "next/cache"
import { createShipment } from "@workspace/services/shipment.service"
import { createShipmentSchema, type CreateShipmentInput } from "@workspace/types/schemas/shipment.schema"

export async function createShipmentAction(
  input: CreateShipmentInput
): Promise<{ success: boolean; error?: string }> {
  const parsed = createShipmentSchema.safeParse(input)
  if (!parsed.success) {
    return { success: false, error: parsed.error.errors[0]?.message }
  }

  try {
    await createShipment(parsed.data)
    revalidatePath("/shipments")
    return { success: true }
  } catch (err) {
    return {
      success: false,
      error: err instanceof Error ? err.message : "Failed to create shipment",
    }
  }
}
```

---

## Connecting Form to Server Action

```tsx
// apps/dashboard/app/shipments/new/page.tsx
import { ShipmentForm } from "@workspace/ui/components/composed/shipments/shipment-form"
import { createShipmentAction } from "../actions"

export default function NewShipmentPage() {
  async function handleSubmit(data: CreateShipmentInput) {
    "use server"
    const result = await createShipmentAction(data)
    if (!result.success) throw new Error(result.error)
  }

  return <ShipmentForm onSubmit={handleSubmit} />
}
```

---

## Select Field Pattern (Enum Values)

```tsx
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@workspace/ui/components/primitives/select"
import { HubCode } from "@workspace/types"

<FormField
  control={form.control}
  name="originHub"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Origin Hub</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger data-slot="origin-hub-select">
            <SelectValue placeholder="Select hub" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          {Object.values(HubCode).map((hub) => (
            <SelectItem key={hub} value={hub}>
              {hub.replace(/_/g, " ")}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

---

## Form Error Display Pattern

```tsx
// Inline field errors — handled by <FormMessage /> automatically

// Top-level server error banner:
{serverError && (
  <div
    data-slot="form-error"
    className="border border-accent-danger bg-accent-danger/10 px-4 py-3 text-sm text-accent-danger"
  >
    {serverError}
  </div>
)}
```

---

## Zod Schemas (Available in @workspace/types)

```ts
// Shipments
import {
  createShipmentSchema,      // full shipment creation
  updateShipmentStatusSchema,
  addressSchema,
  contactSchema,
  weightSchema,
} from "@workspace/types/schemas/shipment.schema"

// Manifests
import { createManifestSchema } from "@workspace/types/schemas/manifest.schema"

// Invoices
import { createInvoiceSchema } from "@workspace/types/schemas/invoice.schema"
```

**Never re-create these schemas in app code.** Import from `@workspace/types`.

---

## Form Field Label Style (Violet Grid)

```tsx
// Standard label — uppercase IBM Plex Mono, muted (mission-control field key)
<FormLabel className="font-mono text-xs uppercase tracking-wider text-muted-foreground">
  AWB Number
</FormLabel>

// Or use the .tac-mono-label utility (uppercase mono caps in primary violet):
<FormLabel className="tac-mono-label">AWB Number</FormLabel>

// Required indicator — use text-accent-danger, not red-500
<FormLabel>
  Sender Name <span className="text-accent-danger" aria-hidden="true">*</span>
</FormLabel>
```

---

## Loading & Disabled States

```tsx
const { isSubmitting } = form.formState

// Button:
<Button type="submit" disabled={isSubmitting}>
  {isSubmitting ? "Saving..." : "Create Shipment"}
</Button>

// Fieldset disable during submit:
<fieldset disabled={isSubmitting} className="space-y-4">
  {/* all fields */}
</fieldset>
```

---

## Pre-Completion Checklist

```
[ ] Schema imported from @workspace/types/schemas/ (not re-created)
[ ] useForm resolver uses zodResolver from @hookform/resolvers/zod
[ ] Form component lives in packages/ui/src/components/composed/
[ ] Server action in apps/*/app/[route]/actions.ts
[ ] Server action validates with .safeParse() before calling service
[ ] revalidatePath() called after successful mutation
[ ] Error states displayed with Violet Grid tokens (text-accent-danger)
[ ] Loading state disables submit button
[ ] Field labels use font-mono uppercase tracking-wider
[ ] data-slot attributes set on key elements
```

---

## Forbidden Patterns

```
❌ fetch("/api/...") in form submit — use server actions
❌ axios.post("/api/...") — axios is forbidden (LAW, forbidden packages)
❌ Re-defining zod schemas in the component file — import from @workspace/types
❌ Inline error string matching hardcoded field names
❌ className="text-red-500" for errors — use text-accent-danger
❌ Uncontrolled inputs without react-hook-form
```
