---
name: portfolio-agent-authorship-disclosure
description: "Use when a portfolio or CV project was built mostly by AI agents but its copy implies hand-authorship, when a build_note fails to parse with 'bad indentation of a mapping entry', or when an owner calls a project 'AI driven', 'agent built' or says they are 'more the director than the author'."
---

# Portfolio agent-authorship disclosure

For the owner who says a project is "AI driven" or "agent built" while the existing copy
implies they typed every line.

The goal is NOT an apology. A senior who can architect, direct and *verify* multi-agent
output at scale is a rarer hire than a fast typist. Say it plainly, high up, with the
verification floor attached - that turns the admission into the argument.

## 1. Model it as data, not prose

Hedged wording ("built with modern tooling") reads as evasion and rots. Add schema fields
so every consumer renders it consistently:

```ts
build_mode: z.enum(['Hand-written', 'Agent-directed']).default('Hand-written'),
build_note: z.string().optional(),
```

Render in two places:
- A **label on the card** (`Agent-directed`) next to domain/year chips, and in the detail
  header - so the disclosure is visible *before* anyone clicks.
- A **"How it was built" block** in the detail overview carrying `build_note`.

Default must be the honest majority case so unmarked entries are not silently
mislabelled.

## 2. Write a different note per project

A single boilerplate note is the same lie in new clothes. For each project state:

- **The trajectory** - "started hand-written, moved to harness-directed as it grew" is a
  much stronger claim than either pole, and is usually the truth.
- **What is unambiguously the owner's** - design, architecture, the judgement calls
  (which factors to weight, which cut feature to restore, where the abstraction boundary
  sits), and the verification.
- **What the agents did** - implementation against that spec.
- **The verification floor** - test counts, CI guards, in-emulator/on-device
  confirmation. Frame it as *the thing that workflow requires*, not a boast.

## 3. Sweep the rest of the copy

The schema field does nothing if `role:` still reads "Solo developer." Grep every surface
for authorship-implying phrasing: `role`, `summary`, markdown body, CV bullets. Same pass:
fix any project the owner calls unfinished - demote its category, kill "Shipped ..."
outcome lines, and say "never completed" in the outcome itself. Keep the entry; the
experience is the point.

Changed CV bullets mean a reprint; prove it still fits one page with
`portfolio-cv-pdf-from-site-content`.

## 4. The trap: YAML plain scalars break on `": "`

A `build_note` containing `... every line: I decide the design ...` fails with
`bad indentation of a mapping entry` at a column deep inside the string (js-yaml,
re-checked 2026-09-24). Use a block scalar:

```yaml
build_note: >-
  Long prose with: colons and "quotes", all safe here.
```

## 5. Verify on the built site

Not the dev server, not the source. Load the built output and assert:
- which cards carry the label (expect exactly the declared set),
- the detail header chip list,
- that the "How it was built" block exists in the overview panel,
- the unfinished project's copy contains the honest phrase.
