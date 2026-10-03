---
name: reviewer-audit
description: Address reviewer/editor comments by number with localized, traceable edits. Use when the user provides numbered reviewer concerns, editor proof queries, or revision lists and asks to "address comment N", "fix W1-W4", "respond to editor queries", etc. Complements review-response (rebuttal drafting) and paper-edit (style enforcement).
tags: [Writing, LaTeX, Academic, Review, Rebuttal]
---

# Reviewer Audit

Localized, traceable response to numbered reviewer/editor comments. The skill enforces scope discipline so a "fix comment 3" request never turns into a global restyle.

## When to Use

- User provides reviewer comments numbered (R1.W1, R2.O3, M1, A10, etc.) and asks to address them in the paper.
- Editor proof queries (e.g., MDPI 27-item list, IEEE editorial sheet).
- A revision document from advisor with itemized changes.
- Any "fix items 5-12" style request.

## Core Rules

1. **One comment, one localized change.** Each numbered item maps to specific lines in specific files. Do not propagate edits beyond the cited locations.
2. **Never globally restyle on a numbered request.** "Remove bold from §3.2 caption" is NOT permission to remove bold everywhere.
3. **Citations are sacred.** Format/style fixes do not delete or replace citations.
4. **Audit trail.** Every applied edit gets a LaTeX comment marker so it can be diffed and verified later.

## Workflow

### Step 1: Build the Item Table

Parse the user's input into a table:

| ID | Comment summary | Target file | Target section/lines | Action type |
|----|-----------------|-------------|----------------------|-------------|
| R1.W1 | clarify threat model | `sections/3-threat.tex` | §3.1, lines 12-18 | rewrite paragraph |
| M3 | shorten caption | `figs/main.tex` | Fig.4 caption | shorten |

If any row's target is unclear, ask the user before editing.

### Step 2: Group by File and Stage

If the audit touches 3+ files or 6+ items, present a stage plan:

```
Stage 1: items M1-M5 in sections/abstract.tex + intro.tex (compile after)
Stage 2: items R1.W1-W4 in sections/3-threat.tex (compile after)
Stage 3: items R2.O1-O3 in sections/5-method.tex (compile after)
```

Wait for approval per stage. Do not bundle.

### Step 3: Apply Edits with Audit Markers

For each edit, leave a LaTeX comment so the change is traceable:

```latex
% [REVIEWER R1.W1] clarified threat model: attacker has read access only
We assume the attacker observes ...
```

Marker format: `% [REVIEWER <ID>] <one-line summary>`

### Step 4: Verify Compilation

After each stage, the `latex-check.js` PostToolUse hook runs compilation automatically. Confirm:
- Page count delta vs. previous stage.
- Zero new compilation errors.
- BibTeX still resolves all `\cite{}`.

If compilation fails, stop and surface the error before proceeding to the next stage.

### Step 5: Generate Response Table

After all stages applied, produce a markdown table mapping each ID to:
- Comment summary
- Files/lines touched
- Brief description of the change
- Page in updated PDF where the change is visible

This table feeds directly into the cover letter or rebuttal document (use `review-response` skill for full rebuttal drafting).

## Anti-Patterns

- ❌ "While I'm in §3.2, let me also clean up some other awkward sentences"
- ❌ "The reviewer flagged one bold phrase, so I'll remove all bold in the paper"
- ❌ Applying all 27 items in one batch without staged compile checks
- ❌ Silent edits with no `% [REVIEWER ID]` marker
- ❌ Substituting a flagged citation with a different one without asking

## Cross-Skill References

- For free-form rebuttal text drafting: use `review-response` skill.
- For style enforcement after edits: use `paper-edit` skill.
- For BibTeX/citation issues found during audit: use `citation-verification` skill.
