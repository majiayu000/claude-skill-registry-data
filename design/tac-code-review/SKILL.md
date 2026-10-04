---
name: tac-code-review
description: "Use when completing a feature, before merging a PR, or after fixing a bug. Reviews for law compliance, TAC Express v5.0 Violet Grid adherence (Plus Jakarta Sans / IBM Plex Mono / Lora, 0rem radius, brutalist offset shadows, violet signal palette), architecture correctness, and code quality."
---

# TAC Express — Code Review

Invoke this skill before any merge to main, after completing a feature, or when a fresh perspective is needed.

> **Core principle:** Review early, review often. Catching violations at review is cheaper than in production.

---

## Review Checklist (Run in This Order)

### 1. Law Compliance (Hard Gates — Any Violation = Reject)

```
[ ] LAW 1: No color values outside globals.css
         grep -r "#[0-9A-Fa-f]{3,6}" packages/ui/src/components apps/
         Should return: nothing (except comments)

[ ] LAW 2: No lucide-react, react-icons, or other icon libs
         grep -r "from 'lucide-react'" .
         grep -r "from 'react-icons'" .

[ ] LAW 3: No framer-motion, gsap, @motionone
         grep -r "framer-motion\|gsap\|@motionone" .

[ ] LAW 4: No font declaration outside apps/*/app/layout.tsx
         grep -r "next/font" packages/ apps/web/components/ apps/dashboard/components/
         Should return: nothing

[ ] LAW 5: No reusable components in apps/ — packages/ui only
         Review any .tsx in apps/*/components/ — must be page-shells only

[ ] LAW 8: No supabase-js in apps/
         grep -r "@supabase/supabase-js" apps/
         Should return: nothing

[ ] LAW 10: No raw Tailwind color classes
          grep -r "bg-blue-\|bg-red-\|bg-green-\|text-blue-\|text-red-" .
          grep -r "bg-\[#\|text-\[#" .

[ ] LAW 11: No arbitrary Tailwind values
          grep -r "w-\[\|h-\[\|p-\[\|m-\[" apps/ packages/ui/
          Should return: nothing

[ ] LAW 12: No npm/yarn usage in scripts
          Check package.json scripts — pnpm only

[ ] LAW 13: No curves or wavy elements
          Check SVG paths for curve commands (C, S, Q, A)
          No rounded-full, no border-radius values outside var(--radius-*)

[ ] LAW 14: No shadcn primitives rebuilt from scratch
          Any new dialog/dropdown/tooltip must use shadcn primitive as base
```

### 2. Architecture Review

```
[ ] Data flow respected: UI → packages/services → packages/database
[ ] No business logic inside React components (only display/interaction logic)
[ ] No direct Supabase calls outside packages/database
[ ] All new types in packages/types (not inline in components)
[ ] Cross-package imports use @workspace/* aliases (not relative ../../../)
```

### 3. Violet Grid (v5.0) Design Compliance

```
[ ] All CSS variables used (not raw hex values or oklch() inline)
[ ] Semantic tokens used: bg-primary, text-foreground, bg-card, border-border, etc.
[ ] NO glass tokens: var(--glass-bg), --glass-border, --glass-highlight FORBIDDEN
[ ] NO glassmorphism: no backdrop-blur, no backdrop-filter anywhere
[ ] Solid surfaces only — dark bg-card panels, not translucent
[ ] Status colors via accent tokens: bg-accent-success, bg-accent-warning, bg-accent-danger
[ ] Animation uses tw-animate-css or motion/react (not inline keyframes in components)
[ ] Radius uses var(--radius-*) tokens (resolves to 0 — no rounded-lg, no rounded-full)
[ ] Typography uses font-sans (Plus Jakarta Sans) / font-serif (Lora) / font-mono (IBM Plex Mono)
[ ] Icons: @remixicon/react via @workspace/ui/icons, size-* class, aria-hidden
[ ] No legacy "TAC Orbital", "TAC Precision", "Indigo Mission-Control", "VELOX", "Wasteland", "cyan/orange" references in code or comments
[ ] No "Space Grotesk", "JetBrains Mono", "Fira Mono", "Inter", "Geist" font names in any file outside git history
[ ] Primary color is violet (oklch ~286° / ~291°) — NOT indigo (260°)
```

### 4. Component Quality

```
[ ] data-slot attribute on every component root element
[ ] Named exports only — no export default for components
[ ] CVA used for variants (not conditional className strings)
[ ] Exported from packages/ui/src/index.ts
[ ] Props interface extends HTML element types
[ ] asChild pattern implemented (using Radix Slot)
[ ] TypeScript — no `any` types
[ ] No TODO comments without TAC-XXX ticket reference
```

### 5. Test Coverage

```
[ ] Test file exists alongside implementation
[ ] Each CVA variant has a test
[ ] Interactive states tested (click, keyboard, focus)
[ ] Service tests mock at database boundary
[ ] Error states covered
[ ] All tests pass: pnpm test
```

### 6. Build & Lint Gates

```bash
pnpm lint --max-warnings 0     ← MUST be zero
pnpm typecheck                  ← MUST be zero errors
pnpm build                      ← MUST succeed
pnpm test                       ← MUST all pass
```

---

## Review Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **CRITICAL** | Law violation, security issue, data loss risk | Block merge immediately |
| **IMPORTANT** | Architecture violation, missing tests, type errors | Fix before merge |
| **MINOR** | Style preference, naming, micro-optimization | Fix if quick, else ticket |
| **NOTE** | Observation, future improvement | Ticket for later |

---

## Self-Review Template

Use this before requesting a human review:

```
### Self-Review: [Feature Name]
Date: YYYY-MM-DD

### Laws Compliance
[ ] LAW 1-14 verified via grep commands above

### Architecture
[ ] Data flow correct
[ ] No forbidden imports

### Violet Grid Design
[ ] Semantic tokens used correctly
[ ] No glassmorphism, no curves, sharp edges only
[ ] Primary is violet, fonts are Plus Jakarta Sans / IBM Plex Mono / Lora

### Tests
[ ] All new code has tests
[ ] pnpm test passes

### Build
[ ] pnpm build succeeds
[ ] pnpm lint --max-warnings 0 passes
[ ] pnpm typecheck passes

### Issues Found & Fixed
- [list any issues caught and resolved]

### Remaining Concerns
- [anything needing human review]
```

---

## Common Review Failures in This Codebase

| Pattern | Violation | Fix |
|---------|-----------|-----|
| `className="bg-[#11161C]"` | LAW 1 | Use semantic token: `className="bg-card"` |
| `import { X } from 'lucide-react'` | LAW 2 | `import { RiX } from "@workspace/ui/icons"` |
| `export default function Card` | Component standard | `function Card` + `export { Card }` |
| `import { createClient } from '@supabase/supabase-js'` in `apps/` | LAW 8 | Move to `packages/database` |
| `const db = await getUser()` in component body | LAW 6/7 | Move to service, pass as prop/hook |
| `rounded-2xl` or `rounded-full` in component | LAW 9/13 | `rounded-[var(--radius-lg)]` or sharp |
| `var(--glass-bg)` or `backdrop-blur` | Design violation | Remove — no glassmorphism (Violet Grid) |
| `Space Grotesk`, `JetBrains Mono`, `Fira Mono`, `Inter`, `Geist` in import/CSS | Design drift | Use Plus Jakarta Sans / IBM Plex Mono / Lora |
| `TAC Orbital`, `Indigo Mission-Control`, `VELOX`, `Wasteland`, `Precision` in comments | Design drift | Remove — dead system references |
| Primary hue at `260°` (indigo) | Color drift | Use violet `oklch(0.5393 0.2713 286.7462)` light / `oklch(0.6132 0.2294 291.7437)` dark |
