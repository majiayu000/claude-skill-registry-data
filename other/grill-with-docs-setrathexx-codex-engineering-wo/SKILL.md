---
name: grill-with-docs
description: Clarifies vague feature, refactor, or product plans against repo docs, domain language, ADRs, and current code. Use when a plan needs questioning, terminology alignment, trade-off discovery, or documentation-aware design before PRD, issues, prototype, or TDD work.
---

# Grill With Docs

Clarify a plan before implementation by checking what the repo already says, what the code already does, and what product decisions remain unresolved.

Do not interview blindly. Read first, ask only when the answer cannot be found in docs or code.

## Read First

Look for project context:

- `CONTEXT.md`
- `docs/agents/domain.md`
- `docs/adr/`
- `docs/agents/issue-tracker.md`
- `docs/agents/test-commands.md`
- relevant README, docs, specs, and plans
- code paths related to the user's idea

Use fast file search when possible:

```powershell
rg --files
```

If setup docs are missing, infer context from existing repo files and say what is missing.

## When To Use

Use this skill when the user has:

- a fuzzy feature idea,
- a refactor plan that may touch multiple modules,
- a product behavior that needs sharper language,
- a domain concept that may be overloaded,
- a plan that should be checked against existing ADRs,
- uncertainty about whether to write PRD, issues, prototype, or tests next.

Do not use it for already-approved implementation work unless a product or domain decision is still open.

## Workflow

### 1. Restate The Plan

Summarize the user request in project language.

Include:

- intended outcome,
- affected users or callers,
- likely modules or surfaces,
- known constraints,
- what is still unclear.

If the user's words conflict with existing domain terms, call that out.

### 2. Check Existing Docs

Read relevant docs before asking questions.

Look for:

- canonical domain terms,
- ADRs that constrain the plan,
- prior decisions that should not be relitigated,
- test commands that affect verification,
- issue tracker conventions if follow-up issues may be created.

If docs and code disagree, surface the disagreement as a decision point.

### 3. Check Code When Useful

If a question can be answered by reading code, read code.

Examples:

- Existing API shape.
- Current validation rules.
- How state changes are represented.
- What tests already exist.
- Whether a concept already has a name.
- Whether an ADR is still reflected in implementation.

Do not ask the user to explain facts that the repo can show.

### 4. Ask Focused Questions

Ask only questions that require product judgment, trade-off selection, or domain clarification.

Good question types:

- "Which actor owns this decision?"
- "Should this be allowed, rejected, or deferred?"
- "Is this term the same as an existing domain term or a new concept?"
- "Which failure mode matters most?"
- "Should this be a temporary prototype or production behavior?"

Ask one question at a time when the answer blocks the next step.

See `references/grilling-question-patterns.md` for question patterns.

### 5. Standardize Domain Language

When a fuzzy term appears, propose a canonical term.

Check:

- Is the term already defined in `CONTEXT.md`?
- Does code use a different name?
- Is the user describing a new concept?
- Is the term overloaded across modules?

When a new durable term emerges, suggest documenting it. Do not write or overwrite docs without approval.

See `references/domain-language-notes.md` for note shape.

### 6. Identify Decisions Worth Recording

Some decisions should become ADR notes. Suggest documentation only when the decision is durable enough to matter later.

Good ADR candidates:

- hard to reverse,
- surprising without context,
- chosen after real trade-off,
- likely to be questioned by a future maintainer,
- affects module boundaries, persistence, API contracts, or verification strategy.

Do not create ADR files without approval.

See `references/adr-note-format.md` for a compact note format.

### 7. Produce The Clarified Plan

End with a concise plan that can feed the next skill.

Use this shape:

```md
## Clarified Plan

Goal:
Actors:
Domain terms:
Affected surfaces:
Constraints from docs/ADRs:
Decisions made:
Open questions:
Out of scope:
Verification direction:
Recommended next skill:
```

Recommended next skill should be one of:

- `to-prd` for product/spec capture,
- `to-issues` for implementation slicing,
- `prototype` for uncertainty that needs a throwaway experiment,
- `tdd` for approved behavior ready to implement.

## Safety Rules

- Do not create or overwrite files without user approval.
- Do not publish anything remotely by default.
- Do not make destructive git or filesystem suggestions.
- Preserve existing docs and user edits.
- Keep Windows paths with spaces quoted when showing commands.

## Verification

Before finishing:

- State which docs and code areas were checked.
- List terms standardized or still ambiguous.
- List decisions made and decisions still open.
- Recommend the next skill and why.
- If documentation should be updated, list exact proposed paths and ask for approval before writing.
