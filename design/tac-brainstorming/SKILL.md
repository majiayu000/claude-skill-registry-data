---
name: tac-brainstorming
description: >-
  MANDATORY before any new feature, component, or architectural change in tac-express. Runs design approval, surfaces trade-offs, confirms architecture fit, and produces a written spec before a single line of code is written.
---

# TAC Express — Brainstorming & Design Approval

> **Load before tac-ui-authoring, tac-data-layer, or tac-tdd for any new feature.**
> Code starts ONLY after this skill produces a written approval.

---

## Why This Skill Exists

Skipping design approval is the #1 source of rework in this codebase. Features built without upfront agreement diverge from Violet Grid (v5.0), violate the architecture flow, or duplicate something already in `packages/ui/src/components/`.

---

## Phase 1 — Clarify Before Anything Else

Before proposing any solution, answer these questions. If you can't answer them, ASK.

```
1. What is the user's exact goal? (not the implementation — the outcome)
2. Which app is this for? (apps/web landing? apps/dashboard logistics?)
3. Does a similar component/service already exist in the codebase?
4. Which packages will change? (packages/ui? packages/services? packages/types?)
5. Does this touch auth, RLS, or user roles? (→ load tac-auth)
6. Does this require a DB schema change? (→ load tac-supabase-schema)
7. What is the failure mode if this breaks?
```

**Stop and ask if two or more questions are unclear.**

---

## Phase 2 — Existing Component Check

Before designing anything new, verify it doesn't already exist:

```bash
# Search components
ls packages/ui/src/components/
ls packages/ui/src/components/primitives/
ls packages/ui/src/components/composed/

# Search for related patterns
grep -r "ComponentKeyword" packages/ui/src/components/ --include="*.tsx" -l
```

If a similar component exists: **extend it, don't create a new one.**

---

## Phase 3 — Architecture Fit Check

Map the feature to the architecture before designing:

```
UI Layer:       packages/ui/src/components/ (new component needed?)
Service Layer:  packages/services/src/ (new service or extend existing?)
Type Layer:     packages/types/src/ (new types needed?)
DB Layer:       packages/database/ + supabase/migrations/ (schema change?)
App Shell:      apps/web/ or apps/dashboard/ (page/route needed?)
```

Check: does this follow `UI → packages/services → packages/database → Supabase`?

---

## Phase 4 — Violet Grid (v5.0) Design Fit

All new UI must align with the design identity. Answer each:

```
[ ] Dark-first: Does it use bg-card / bg-background / bg-muted? No white panels.
[ ] Sharp: No rounded-full, no rounded-lg with non-zero radius. var(--radius) = 0.
[ ] Shadows: Brutalist offset only — shadow-sm/shadow/shadow-md (1–6px sharp offsets) or aliases shadow-[var(--shadow-brutal-sm)] / shadow-[var(--shadow-brutal)].
[ ] Fonts: font-sans (Plus Jakarta Sans) for labels, font-mono (IBM Plex Mono) for AWBs/IDs/numbers, font-serif (Lora) for blockquotes/prose only.
[ ] Signal palette: violet = primary (CTAs, focus). Green = success. Amber = warning. Red = danger.
[ ] No glassmorphism: No backdrop-blur, no translucent surfaces, no glass tokens.
[ ] Icons: @remixicon/react only. aria-hidden on decorative icons.
[ ] FUI utilities available: .tac-fui-panel, .tac-mono-label, .tac-hazard-stripes, .tac-scanline, .tac-blink, .tac-signal-glow, .tac-hero-bleed
[ ] Premium type scale: prefer .t-display / .t-h1..h4 / .t-data / .t-overline over ad-hoc text-* classes for branded surfaces.
```

---

## Phase 5 — Write the Feature Spec

Produce this document before writing code. Keep it short — clarity over completeness.

```markdown
## Feature: [Name]

### Goal
[One sentence: what problem does this solve for the user?]

### Scope
- Packages changed: [list]
- New components: [list or "none"]
- New services/hooks: [list or "none"]
- DB changes: [list or "none"]

### Component Tree (if UI)
[Rough sketch of parent → child relationships]

### Data Flow
[Service(s) → database query → returned type]

### Design Notes
- Variant: [default | signal | ghost | etc.]
- Key tokens: [list the CSS token classes]
- FUI utilities: [if applicable]

### Non-Goals
[What this feature explicitly does NOT do]

### Definition of Done
[ ] Types in packages/types
[ ] Service in packages/services
[ ] Component in packages/ui
[ ] Tests written (tac-tdd)
[ ] pnpm typecheck && pnpm lint && pnpm test all pass
```

---

## Phase 6 — Approval Gate

Do not write code until:

1. The feature spec above is written
2. The user has confirmed the approach (or you've resolved all open questions)
3. You've confirmed no Law violations in the plan
4. The relevant specialist skill is loaded (`tac-ui-authoring`, `tac-data-layer`, etc.)

**If the user says "just build it" without spec:** Briefly state the plan (2–4 bullet points), confirm, then build.

---

## Trade-Off Vocabulary

Use this vocabulary when surfacing options:

| Pattern | Use When |
|---------|----------|
| Extend existing component | Similar component exists, only variant needed |
| New composed component | Unique domain composition, no base to extend |
| New primitive | Truly new base UI element not covered by shadcn |
| Server Component (RSC) | Display-only, no interactivity, no useState |
| Client Component | Interactivity, hooks, event handlers |
| Server Action | Form mutation, data write from the UI |
| Service function | Reusable business logic called from multiple places |
| Hook | Client-side async state management |

---

## Anti-Patterns to Catch in Planning

```
❌ "I'll add the filter logic in the component" → LAW 7 — move to packages/services
❌ "Let me use Tailwind's bg-indigo-500" → LAW 10 — use bg-primary
❌ "I'll add a new rounded-2xl card" → LAW 13 — zero radius, sharp corners
❌ "Add the component to apps/dashboard/components/" → LAW 5 — goes in packages/ui
❌ "Let me create a quick modal from scratch" → LAW 14 — wrap shadcn Dialog
❌ "We can use framer-motion for this transition" → LAW 3 — use motion/react or tw-animate-css
```
