---
name: nickstire-ios-pwa-primitives
description: Use when writing or editing client code in EITHER PWA (apps/nickstire/client/ or apps/statenour) that needs a confirm dialog, text capture, or alert — and as a periodic sweep — because window.prompt/alert/confirm is silently suppressed in iOS PWA standalone mode (the operator's actual operating environment on both apps) and customer-facing PWAs.
triggers: confirm dialog, alert, window.prompt, text capture, ios pwa, standalone mode, home screen, suppressed primitive, button does nothing on my phone, toast, modal, drawer, client code, sweep, admin pages, mobile
---

# nickstire-ios-pwa-primitives

iOS PWA standalone mode (a site added to the home screen) **silently
suppresses `window.prompt`, `window.alert`, and `window.confirm`**.
The functions return `null` / `undefined` with no UI shown. Code that
relies on a non-null return value to proceed silently no-ops on the
user's actual device.

This is the most-recurring single bug class in the nickstire codebase
(5+ waves and counting). It keeps shipping because no one runs a
proactive sweep.

## Triggers

Use this skill when:
- Writing client code that needs confirmation, text input, or an alert
- Seeing any of these patterns in `apps/nickstire/client/`:
  - `prompt(` / `window.prompt(`
  - `alert(` / `window.alert(`
  - `confirm(` / `window.confirm(`
- The operator reports "the [button/link] doesn't do anything on my
  phone" — classic symptom of a suppressed primitive

## The full sweep (run periodically)

From repo root — BOTH apps, and note the statenour list includes
`features` and `hooks`. The one live `window.prompt` that survived five
prior sweep waves (operator-conversation-drawer.tsx, fixed 2026-08-04)
lived in `apps/statenour/features/` — a source root OUTSIDE the
`{app,components,lib}` glob every earlier audit used. A sweep whose glob
misses a source root is structurally blind to regressions there.

```bash
grep -rn '\(window\.\)\?\(prompt\|alert\|confirm\)(' \
  apps/nickstire/client/src \
  apps/statenour/app apps/statenour/components apps/statenour/lib \
  apps/statenour/features apps/statenour/hooks \
  --include="*.tsx" --include="*.ts" 2>/dev/null \
  | grep -v 'confirmDialog\|confirmEmail\|window\.confirm\.\|//' \
  | head -30
```

Filter the noise: comments mentioning the bug class are fine; the
`confirmDialog` import is the fix, not a hit.

**statenour replacement primitives** (this skill applies there too —
statenour is also an installed iOS PWA): `useConfirmDialog` and
`usePromptDialog` in `apps/statenour/components/ui/confirm-dialog.tsx`.
nickstire's remain `confirmDialog` + sonner toasts as documented below.

## Replacement patterns (use what exists; don't invent new primitives)

### Confirmation (yes/no) — use `confirmDialog`

The codebase has a singleton imperative confirm modal at
`apps/nickstire/client/src/components/admin/ConfirmDialog.tsx`. Async,
promise-based, looks correct on mobile, respects iOS PWA. Pattern:

```tsx
import { confirmDialog } from "@/components/admin/ConfirmDialog";

onClick={async () => {
  const ok = await confirmDialog({
    title: "Delete invoice?",
    message: `${inv.invoiceNumber} — ${inv.customerName}. This cannot be undone.`,
    confirmLabel: "Delete",
    tone: "danger",
  });
  if (ok) deleteInvoice.mutate({ id: inv.id });
}}
```

Real-world fix: `apps/nickstire/client/src/pages/admin/RevenueSection.tsx`
(the "Delete this invoice?" path).

### Alert (notification, no input) — use `toast.error()`

```tsx
import { toast } from "sonner";

if (!formData.name || !formData.phone) {
  toast.error("Please fill in all required fields");
  return;
}
```

Real-world fix: `apps/nickstire/client/src/components/EmergencyMode.tsx`
(the missing-field handler in the customer emergency form).

### Text capture (prompt for input) — inline expandable component

There's no `promptDialog` primitive — and don't invent one for one
call site (YAGNI). Mirror the proven `FollowUpButton` pattern in
`apps/nickstire/client/src/pages/admin/CustomersSection.tsx`.

Self-contained component owns:
- its own `useState` for expanded + input value
- its own `useRef<HTMLInputElement>` for autofocus
- its own `trpc.X.useMutation` (so per-row `isPending` doesn't disable
  every other row)
- a `useEffect` that focuses the input on expand
- collapsed render = the trigger button
- expanded render = inline input + confirm + cancel buttons

Real-world fixes: `MarkContactedButton` and `LostReasonButton` in
`apps/nickstire/client/src/pages/admin/LeadsSection.tsx` (the
"Mark Contacted" + "Mark Lost" paths).

### Kanban / drag-drop callbacks — drop the prompt entirely

If text capture sits inside a drag-drop callback (no good place for
inline UI), drop the capture for that path. Move the capture to the
list-view button (which has an obvious inline-UI surface). The Kanban
operation just sets status without the optional reason.

Real-world reference: `LeadsSection.tsx` Kanban drag-to-lost path —
the prompt-suppression made the drag silently never persist on iOS
PWA. Now Kanban sets status only; the `LostReasonButton` in the
list view captures the reason.

## Recurring history (5+ waves)

| Wave | What was suppressed | Fix |
|---|---|---|
| wave-139 | `window.confirm()` across admin | Introduced `ConfirmDialog` singleton + migrated callers |
| wave-152 | `confirm()` in FollowUpsSection | Migrated to `confirmDialog` |
| wave-168 | `prompt()` for "FollowUp" trigger in CustomersSection | Introduced `FollowUpButton` inline-expandable pattern |
| wave-181.59 | `confirm()` in DeclinedEstimates | Migrated to `confirmDialog` |
| current (this commit) | `prompt()` × 2 in LeadsSection + `alert()` in EmergencyMode + `confirm()` in RevenueSection | `MarkContactedButton` + `LostReasonButton` + `toast.error()` + `confirmDialog` |

## After fixing — lock it with a regression test

Mirror the `LeadsSection` regression test in
`apps/nickstire/client/src/__tests__/admin.test.tsx` ("LeadsSection:
marking a lead contacted never calls window.prompt"). Pattern:

```tsx
const promptSpy = vi.spyOn(window, "prompt");
// render the component, click the button that USED to call prompt()
fireEvent.click(button);
expect(promptSpy).not.toHaveBeenCalled();
expect(screen.getByLabelText(/expected-inline-input-label/i)).toBeTruthy();
```

Then **revert-check**: temporarily put `prompt()` back in the source,
run the test, confirm it FAILS with a meaningful message. Restore
the fix. A regression test you haven't seen fail against the bug is
theater (see `smoke.test.tsx`'s vacuous "Admin renders").

## Why this skill exists

This bug class has cost the operator real money — leads silently never
marked contacted on the phone, invoices never deleted, emergency
submissions with no feedback. It will keep recurring as long as new
code can introduce `prompt|alert|confirm` calls without an automated
guard. Long-term fix: an ESLint rule that bans
`/\bwindow\.(prompt|alert|confirm)\b/` in `apps/nickstire/client/`,
forwarding to this skill's replacement patterns. Until then, run the
sweep periodically.
