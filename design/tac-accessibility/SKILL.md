---
name: tac-accessibility
description: >-
  Load when building or reviewing UI components in tac-express. Ensures WCAG 2.1 AA compliance with Violet Grid design constraints — keyboard navigation, focus management, ARIA attributes, and Radix primitive accessibility wiring.
---

# TAC Express — Accessibility (A11y)

> Violet Grid (v5.0) is dark-first and high-contrast by design — but accessibility still requires explicit wiring. Radix does most of the heavy lifting; this skill covers what's left.

---

## Core Principle

Radix UI primitives ship with built-in accessibility. **Don't fight them — configure them.**

```tsx
// ✅ Radix Dialog handles focus trap, Escape key, ARIA roles
import * as Dialog from "@radix-ui/react-dialog"

// ❌ Don't build your own focus trap from scratch (LAW 14)
```

---

## Icon Accessibility

Every icon must be either decorative (aria-hidden) or labeled:

```tsx
// Decorative — hide from screen readers
<RiArrowRightLine className="size-5 text-muted-foreground" aria-hidden="true" />

// Meaningful — button with icon only needs a label
<button aria-label="Close panel">
  <RiCloseLine className="size-5" aria-hidden="true" />
</button>

// Icon + text — hide icon, text carries the meaning
<button>
  <RiAddLine className="size-4 mr-2" aria-hidden="true" />
  Add Shipment
</button>
```

---

## Interactive Element Requirements

Every clickable/focusable element must have:

```tsx
// 1. Visible focus ring (Violet Grid: violet signal glow — 1px ring + 8px bloom)
className="focus-visible:outline-none focus-visible:tac-signal-glow"

// 2. Keyboard activation (Enter + Space for buttons — native <button> handles this)
// Use <button> not <div onClick> for interactive elements

// 3. Descriptive label
<button aria-label="Delete shipment TAC-00012345">
  <RiDeleteBinLine aria-hidden="true" />
</button>
```

---

## Focus Management

```tsx
// Dialog: focus moves to first focusable element on open (Radix default)
// On close: focus returns to trigger (Radix default)

// Custom focus on open — use autoFocus or initialFocus ref:
<DialogContent>
  <Input autoFocus placeholder="Search..." />
</DialogContent>

// Programmatic focus after action (e.g., after form submit error):
const errorRef = useRef<HTMLDivElement>(null)
useEffect(() => {
  if (serverError) errorRef.current?.focus()
}, [serverError])

<div ref={errorRef} tabIndex={-1} role="alert" className="text-accent-danger">
  {serverError}
</div>
```

---

## Form Accessibility

```tsx
// Every input needs an associated label (via htmlFor + id, or FormLabel from shadcn)
<FormField
  control={form.control}
  name="awbNumber"
  render={({ field }) => (
    <FormItem>
      <FormLabel htmlFor="awb-input">AWB Number</FormLabel>
      <FormControl>
        <Input id="awb-input" aria-describedby="awb-hint awb-error" {...field} />
      </FormControl>
      <p id="awb-hint" className="text-xs text-muted-foreground">
        Format: TAC + 8–11 digits
      </p>
      <FormMessage id="awb-error" />
    </FormItem>
  )}
/>

// Required fields
<FormLabel>
  Sender Name
  <span className="text-accent-danger ml-1" aria-label="required">*</span>
</FormLabel>

// Loading state announced to screen readers
<button disabled={isSubmitting} aria-busy={isSubmitting}>
  {isSubmitting ? "Saving..." : "Create Shipment"}
</button>
```

---

## Status Badges & Live Regions

```tsx
// Status badges need semantic meaning, not just color
<span
  role="status"
  aria-label={`Shipment status: ${status}`}
  className="..."
>
  {status}
</span>

// Live region for async updates (scan events, realtime status changes)
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {lastScanResult && `Scanned: ${lastScanResult.awbNumber} — ${lastScanResult.status}`}
</div>

// Alert for errors (assertive — interrupts)
<div role="alert" aria-live="assertive">
  {criticalError}
</div>
```

---

## Data Tables

```tsx
<table role="table" aria-label="Shipments">
  <thead>
    <tr>
      <th scope="col">AWB Number</th>
      <th scope="col">Status</th>
      <th scope="col">
        <span className="sr-only">Actions</span>
      </th>
    </tr>
  </thead>
  <tbody>
    {shipments.map((s) => (
      <tr key={s.id}>
        <td className="font-mono">{formatAWB(s.awbNumber)}</td>
        <td>{s.status}</td>
        <td>
          <button aria-label={`View shipment ${formatAWB(s.awbNumber)}`}>
            View
          </button>
        </td>
      </tr>
    ))}
  </tbody>
</table>
```

---

## Color & Contrast (Violet Grid)

Violet Grid's dark-first palette is designed for high contrast. Verify:

```
bg-background + text-foreground      → AA pass (verify with devtools)
bg-card + text-foreground            → AA pass
bg-muted + text-muted-foreground     → check — muted pairs may be borderline

bg-accent-danger + text-foreground   → error text must be legible
bg-accent-success + text-foreground  → success text must be legible
```

**Never rely on color alone** to convey meaning:
```tsx
// ❌ Color only
<span className="text-accent-danger">Error</span>

// ✅ Color + icon + text
<span className="text-accent-danger flex items-center gap-1">
  <RiErrorWarningLine aria-hidden="true" />
  Invalid AWB format
</span>
```

---

## Keyboard Navigation Checklist

```
[ ] Tab order is logical (follows visual flow)
[ ] No keyboard trap (user can always escape)
[ ] All interactive elements reachable via Tab
[ ] Modals/sheets trap focus while open (Radix: automatic)
[ ] Escape closes modals/drawers (Radix: automatic)
[ ] Dropdown keyboard: Arrow keys navigate, Enter/Space select, Escape closes
[ ] Tables: Tab moves between cells, action buttons within cells accessible
[ ] Forms: Enter submits, Tab moves between fields
```

---

## Screen Reader Testing Checklist

```
[ ] All images have alt text (or alt="" for decorative)
[ ] All icons are either aria-hidden or have aria-label
[ ] Form fields have associated labels
[ ] Error messages are announced (role="alert" or aria-live)
[ ] Loading states are announced (aria-busy)
[ ] Status changes use aria-live="polite" (non-critical) or "assertive" (errors)
[ ] Page has a logical heading hierarchy (h1 → h2 → h3)
[ ] Skip-to-main-content link at top of page (for long navbars)
```

---

## Violet Grid–Specific Patterns

```tsx
// FUI blink animation — add prefers-reduced-motion guard
className="tac-blink motion-reduce:animate-none"

// Scanline animation — same
className="tac-scanline motion-reduce:hidden"

// globals.css already includes:
// @media (prefers-reduced-motion: reduce) { * { animation-duration: 0.01ms !important; } }
// but component-level override is defensive best practice
```
