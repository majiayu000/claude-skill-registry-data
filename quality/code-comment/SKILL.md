---
name: code-comment
description: Writes and updates terse, why-only code comments to house standard, and judges the comments in a diff via an isolated sub-agent (PASS/REWRITE/REMOVE/FIX_CODE). Use when writing or editing a code comment, or reviewing the comments in a change — loaded inline by /implement_plan (writer) and run as a review pass by /validate_plan (judge). Complements /code-review (bugs, documented standards) and /quality-control (Fowler design smells) with the comment-quality lens neither covers.
model: sonnet
effort: high
---

Single source of truth for the comment standard, in two modes. Free-prose comments
only (`//`, `/* */`, `/** */` prose, trailing end-of-line) in `src/**/*.{ts,tsx}`,
tests included. Structured JSDoc is out of scope — `.claude/rules/jsdoc-concise.md`
owns it.

## Writer mode — when writing or updating a comment

A comment earns its place only by carrying *why* the code cannot: intent, a
constraint, an external reference (spec / bug / gotcha), a non-obvious rationale.
Apply in order:

1. **Restates *what* the code does?** Don't write it (or delete it). The code
   already says how; a comment says why.
2. **Code needs a comment to be understood?** First make the code explain
   itself — rename, extract a function (a comment marking a block *is* the name
   of the function to extract), introduce an assertion for an assumed condition.
   Comment only what remains.
3. **Genuine why, or a contract a signature can't encode** (bound inclusivity,
   units, error/edge behaviour, an invariant)? Keep it — write it ELI5 and
   extremely concise, sacrifice grammar for concision. Two hard ELI5 rules:
   **no internal names** — not method names (`setBaggage`), not the literal keys;
   say what happens in plain words; and **1–2 lines** — if you reach for a third,
   cut. Prefer rot-resistant *why* (a business rule, an external-bug workaround)
   over volatile implementation narration; a comment you won't keep true is a
   future lie.
4. **Tests** (`*.test.ts`): structure self-documents (descriptive name +
   Arrange-Act-Assert). Hold "what" comments to a higher bar than production,
   but *why-this-case* — an edge-case rationale, a regression/ticket link, a
   magic constant in an assertion — is equally justified.

## Judge mode — review the comments in a diff

Adversarial pass an isolated sub-agent runs; surface-only, never edits. A fresh
critic beats the context that wrote the code (less self-justification bias).

### 1. Pin the diff

Use the fixed point the caller supplies (`/validate_plan` passes the plan base,
same as `origin/HEAD`); if unspecified, ask. Capture
`git diff --unified=5 <fixed-point>...HEAD` (three-dot; ±5 context so the judge
sees the code a comment sits in). Confirm the ref resolves and the diff is
non-empty before spawning.

### 2. The rubric — one verdict per in-scope changed comment

- `PASS` — genuine why-context (or a contract a signature can't encode), already
  concise. No output.
- `REWRITE` — genuine why-value but verbose/vague, **or stale/misleading** (the
  comment has drifted from the code — a wrong comment is worse than none).
  Return a tightened ELI5 replacement.
- `REMOVE` — restates *what* the code plainly says ("deodorant"); no why. Advise
  deletion.
- `FIX_CODE` — explains successfully, but *only because the code is confusing*.
  Advise the refactor (Extract Function / Rename / Introduce Assertion), then
  drop the comment.

**Critical boundary — KEEP/REWRITE vs FIX_CODE.** Reach for `FIX_CODE` only when
the complexity is *incidental* (bad naming, over-cleverness, tangled control
flow). *Essential* complexity is a legitimate KEEP/REWRITE, never a smell — do
not demand simplification of code that cannot be simplified. Protected:
**regex, legal/regulatory rule, browser/platform quirk or workaround, non-obvious
algorithm choice, performance hazard, units/bounds/invariant, edge-case
workaround.**

**Never flag a comment merely for existing.** A why / intent / constraint /
external-reference comment is a `PASS` even over otherwise-clear code — that is
the sweet smell, not a failure.

**Confidence-gate `FIX_CODE`.** It is the weakest verdict (no tool operationalizes
"needed comment ⇒ refactor"; LLM accuracy on the adjacent smell is low). Emit a
confidence score; downgrade a low-confidence `FIX_CODE` to an advisory note or
suppress it. A noisy judge gets ignored — false-positive rate is the trust metric.

**Exempt (never judged):** `import "server-only"` explainers (mandated by
`.claude/rules/server-only-boundary.md`); license/copyright headers; tooling
pragmas (`biome-ignore`, `eslint-disable*`, `@ts-expect-error`, `@ts-ignore`,
`v8 ignore`); marker comments (`TODO`, `FIXME`, `HACK`); structured JSDoc tags.

### 3. Spawn the judge sub-agent

One isolated `general-purpose` Agent at `sonnet` / high effort (worker-role
reviewer grading evidence against a rubric — an in-repo head-to-head tied
`sonnet@high` with `opus@high`, so the cheaper tier wins). Paste into
its prompt: the diff command + commit list; this rubric, scope, exempt list, and
the writer-mode ELI5 house style (no internal names, 1–2 lines) in full (it has no
other access); the brief — "per in-scope changed comment emit one verdict and quote
the hunk; a REWRITE replacement must follow the ELI5 house style; essential
complexity is protected; confidence-gate FIX_CODE; never edit; under ~400 words."

### 4. Report

Present the findings under `## Comment quality (judgement calls)`, verbatim or
lightly cleaned, with each `REWRITE`'s suggested replacement. End with a one-line
count and the worst verdict. The caller (or a follow-up) applies fixes.

## TODO — deferred

- **Eval-gated model+effort.** Ships on the `sonnet@high` hypothesis. Pin it on
  evidence before hardening: two-tier eval under `.claude/skills/code-comment/eval/`
  (Tier 1 golden set ~20–40 hunks incl. clean + synthetic injections, scored on
  clean-hunk false-positive rate; Tier 2 pairwise head-to-head via `subagent-eval`)
  across `{haiku,sonnet,opus} × effort`. Optimise recall subject to FP-rate <~10%.
- **Optional husky pre-push backstop** for comments written outside the workflows.
  Mechanics: pre-push (or per-turn Stop) hook → `git diff` the branch → extract
  in-scope changed-comment hunks (±5 context) → one batched `claude -p` (sonnet;
  `unset ANTHROPIC_API_KEY`, no `--bare` — both break subscription auth) with this
  rubric → per-hunk hash dedup in gitignored `.claude/state/` (judge each hunk
  once) → fail-open (any error/timeout ⇒ exit 0), surface-only (never edits).
