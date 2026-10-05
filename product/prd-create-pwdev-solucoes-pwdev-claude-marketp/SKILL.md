---
name: prd-create
description: >
  Use when the user wants a new Product Requirements Document — 'criar um PRD', 'escrever os
  requisitos de', 'new PRD for', 'documento de requisitos' — through a 12-step interview, one
  question at a time, ending with an approval gate. Do NOT use to change an existing PRD (prd-
  refine) or to plan implementation.
metadata:
  version: 3.0.0
---

# Create a PRD

## Method (inline — you run in the MAIN context)
You are the PRD interviewer. Follow
`<plugin-root>/references/interview-method.md` end-to-end: persona,
principles, the 12-step process, smart defaults, consistency checks, opening
message. Never delegate the interview to a subagent — you interview the human, and
subagents cannot talk to the human.

## Input
The arguments: brief description of the feature or system (required).

## Pre-check

```bash
mkdir -p .planning/prds
```

## Flow

### STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

### STEP 1 — Determine PRD slug

From the arguments, generate a kebab-case slug (e.g., "user-authentication", "inventory-management").

Create directory:
```bash
mkdir -p .planning/prds/{slug}
```

### STEP 2 — Start Interview

Follow the 12-step interview process from `references/interview-method.md`:

1. Context and overview
2. Problem and opportunity
3. Objectives and success metrics
4. Scope
5. Functional requirements
6. Non-functional requirements
7. Architecture and approach
8. Decisions and trade-offs
9. Dependencies
10. Risks and mitigation
11. Acceptance criteria
12. Testing and validation

**Rules:**
- One question at a time
- Summarize at end of each step
- Confirm before moving on
- Mark unknowns as hypothesis

### STEP 3 — Consistency Checks

Before generating, run all consistency checks from `references/interview-method.md`.
Flag any issues and resolve with the user.

### STEP 4 — Generate PRD.md

Write to `.planning/prds/{slug}/PRD.md` following exactly the template in
`<plugin-root>/templates/PRD.template.md`.
Log: `sh "<plugin-root>/scripts/audit-log.sh" event create "" completed ".planning/prds/{slug}/PRD.md" ""`

### STEP 4.1 — Approval gate

Show a 3-line summary (feature, number of FRs, open hypotheses), then ask:

```
Approve this PRD? Approved PRDs can be turned into a roadmap.
(y = mark APPROVED / n = keep as DRAFT)
```

On yes → set the header line to `Status: APPROVED`. On no → keep `Status: DRAFT`.
Never set `APPROVED` without the user's explicit yes.

### STEP 5 — Ask about JSON export

```
The PRD has been generated in Markdown.

Would you also like a JSON export with English keys? (y/n)
```

If yes → generate `.planning/prds/{slug}/prd.json` following the canonical
JSON structure in `<plugin-root>/references/interview-method.md`.

### STEP 6 — Ask about commit

```
📋 PRD created: .planning/prds/{slug}/PRD.md

Would you like to commit this PRD to the repository? (y/n)
```

If yes:
```bash
git add .planning/prds/{slug}/
git commit -m "docs(prd): add PRD for {slug}"
```

### STEP 7 — Summary

```
✅ PRD created

📄 Files:
  .planning/prds/{slug}/PRD.md      ← Structured PRD
  .planning/prds/{slug}/prd.json    ← JSON export (if requested)

📊 Summary:
  Product: {product}
  Status: {DRAFT | APPROVED}
  Feature: {feature}
  Functional requirements: {N}
  Business rules: {N}
  Non-functional requirements: {N}
  Risks: {N}
  Acceptance criteria: {N}

👉 Next:
  /pwdev-prd:refine {slug}     → Update this PRD
  /pwdev-prd:roadmap {slug}    → Roadmap with dependency chain and draft stories (needs Status: APPROVED)
  /pwdev-prd:stories {slug}    → Evolve each feature: user stories, CA and RN
  /pwdev-prd:publish {slug}    → GitHub Project + issues from the roadmap (pwdev-github)
  /pwdev-prd:export {slug}     → JSON, or a single GitHub issue with the PRD
  /pwdev-feat:feat             → Create action plan from this PRD (if pwdev-feat installed)
  /pwdev-code:discover         → Start full workflow from this PRD (if pwdev-code installed)
```

## Prohibitions
- NEVER skip the interview — always ask questions
- NEVER invent requirements the user didn't provide
- NEVER include specific technology choices (PRDs are technology-agnostic)
- NEVER commit without asking

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
