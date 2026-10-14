---
name: forms-validation
description: How forms validate input in this template — Zod schema at the boundary, accessible error messaging, and the submit-validate-report pattern.
paths: ["src/components/**/*Form*", "src/components/**/*Dialog*"]
---

- Every form has a Zod schema in `src/lib/schemas.ts` that is the single source of truth for
  validity — the same schema is used for the client-side check on submit AND inside the
  mutation's `mutationFn` (`server-state-tanstack-query` skill) so the two can never disagree.
- Validate on submit with `schema.safeParse(...)`, not on every keystroke, unless the spec's
  EARS criteria explicitly call for inline/live validation — see `SubscribeDialog.tsx` for the
  submit-time pattern.
- Error messages: one `<p role="alert" id="<field>-error">` per invalid field, and the input
  carries `aria-invalid` + `aria-describedby` pointing at that id (see the email input in
  `SubscribeDialog.tsx`) — a validation error that isn't announced to assistive tech is an
  a11y bug, not just a UX one, and `a11y-auditor` will flag it.
- Never trust `zod`'s error message text verbatim for user-facing copy without checking it
  reads naturally — write an explicit `message` in the schema (`z.string().email("Enter a
valid email address")`) rather than relying on the default.
- Disable the submit control while the mutation is pending (`mutation.isPending`) and label it
  accordingly ("Subscribing..." not just a spinner with no text) so screen reader users get
  the same feedback sighted users do.
