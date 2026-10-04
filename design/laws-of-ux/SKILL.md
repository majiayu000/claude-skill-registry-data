---
name: laws-of-ux
description: >
  Comprehensive UX design companion based on all 30 Laws of UX from lawsofux.com. Analyzes components being built and recommends which laws apply with specific code-level fixes. Works as proactive advisor during frontend development and reactive auditor on demand.
  Use when building or reviewing UI/UX — designing layouts, choosing interactions, organizing information, evaluating interface decisions, or when user mentions "UX laws", "laws of ux", "lawsofux", "UX audit", "UX review", "UX checklist", "check UX", "apply UX", "design review", "UI review", "pre-ship check".
  Also triggers alongside the frontend-design skill.
  Do NOT trigger for: backend logic, API design, database schema, or non-visual code.
---

# Laws of UX — Actionable Design Companion

Apply the 30 Laws of UX (lawsofux.com) to every frontend decision with specific, code-level guidance.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/laws-of-ux` | Analyze what's being built → recommend relevant laws + code changes |
| `/laws-of-ux review` | Full audit of existing UI → score 0-60 + prioritized fixes |
| `/laws-of-ux checklist` | Quick 12-point pre-ship pass/fail check |

## Orchestration Logic

### Route Selection

```
IF user is building new UI or frontend-design skill is active:
  → Run PROACTIVE ADVISOR mode (this skill)
IF user says "review", "audit", "check UX", or points at existing code:
  → Route to /laws-of-ux-review
IF user says "checklist", "pre-ship", "ready to ship?":
  → Route to /laws-of-ux-checklist
```

## Proactive Advisor Mode

When the user is building UI, follow this process:

### Step 1: Detect Component Type

Read the code being written. Classify as one of:
- **Form** (inputs, validation, submission)
- **Dashboard** (metrics, charts, KPIs)
- **Navigation** (sidebar, navbar, tabs, breadcrumbs)
- **Wizard/Stepper** (multi-step flow)
- **List/Table** (data display, sorting, filtering)
- **Modal/Dialog** (overlay, confirmation)
- **Card Layout** (grid of items, feed)
- **Landing/Hero** (marketing, CTA-focused)
- **Empty/Error State** (zero data, failures)
- **Settings/Config** (toggles, preferences)

### Step 2: Surface Relevant Laws

Load `references/code-patterns.md` and extract the 5-8 laws mapped to that component type.

### Step 3: Give Actionable Guidance

For each relevant law, provide:

```
**[Law Name]** — [one-line rule]
→ DO: [specific CSS/JSX pattern to implement]
→ DON'T: [common violation to avoid]
```

Keep it to 5-8 laws maximum. Don't dump all 30 — that defeats the purpose (Hick's Law applies to you too).

### Step 4: Code-Level Recommendations

Provide actual code snippets. Not theory, not vague advice. Examples:

- "Add `gap: 0.5rem` between related fields, `gap: 2rem` between sections" (Proximity)
- "Primary CTA should be `min-h-11 min-w-[120px] text-base font-semibold`" (Fitts's Law)
- "Add `transition-all duration-200` to all interactive elements" (Doherty Threshold)
- "Max 5 items in this nav group — move the rest to 'More'" (Hick's Law)

## Critical Rules

1. **Never list all 30 laws at once** — surface only what's relevant to the current component
2. **Always provide code** — if you can't write a CSS/JSX fix, the advice is too vague
3. **Violations > Suggestions** — prioritize what's wrong over what could be better
4. **Respect the user's stack** — adapt patterns to their framework (React, Vue, Tailwind, CSS modules, etc.)
5. **Don't repeat yourself** — if a law was already applied in earlier components, skip it unless there's a new violation

## Reference Files

- `references/ux-laws-complete.md` — All 30 laws with definitions, applications, and violation signals (load on-demand)
- `references/code-patterns.md` — Component-type → law mapping table (load on-demand)

## Sub-Skills

- `laws-of-ux-review` — Full UX audit with 0-60 scoring and prioritized code fixes
- `laws-of-ux-checklist` — Fast 12-point pre-ship verification with pass/fail verdict
