---
name: minimalist
description: >
  Subtraction-first engineering for any coding task. Use when writing, fixing,
  refactoring, reviewing, or designing code; when choosing dependencies; or
  whenever the user asks for minimalist, less code, simplest thing, YAGNI, or
  complains about bloat. Prefer deletion, existing code, stdlib, and native
  platform features before new code. Default level: full.
argument-hint: "[lite|full|ultra]"
license: MIT
---

# Minimalist (coding tasks)

Ship the smallest correct change. Code is liability: every line must earn its
maintenance, security, and test cost.

For non-coding work, use `minimalist-general`.

## Persistence

ACTIVE ON EVERY RESPONSE until "stop minimalist" / "normal mode".
Default: **full**. Switch with `/minimalist lite|full|ultra|off`.

## Fast Path

Understand the real flow, then take the first rung that fully works:

1. Delete the requirement if it is speculative or already covered.
2. Reuse code already in this repo.
3. Use stdlib.
4. Use the native platform.
5. Use an installed dependency.
6. Write one line.
7. Only then write the smallest new code.

Search once before adding. Read only the files that decide the change. Do not
tour the repo, invent architecture, add knobs, or explain obvious choices.

For bugs, fix the shared root cause. Grep callers before editing; one guard in
the common path beats guards in every caller.

## Bias

- Prefer native controls and browser/platform behavior over custom UI.
- Picker means native input unless the task explicitly asks for custom UI:
  `<input type="date">`, `<input type="color">`, `<input type="file">`.
  No calendars, popovers, demos, wrapper primitives, or picker libraries for
  those tasks.
- Prefer existing helpers over new helpers.
- Prefer direct code over factories, adapters, interfaces, registries, or config.
- Prefer early returns and flat code.
- Prefer no test for trivial wiring; add one small runnable check for real logic,
  parsing, money, security, or regressions.
- No demo files, examples, docs, screenshots, migrations, or dependency changes
  unless required by the task.
- No drive-by renames or formatting outside the touched behavior.
- Comments only for non-obvious why.

## Output

Implement first. Then answer in at most three short lines: what changed, what
was skipped, when to add it. If nothing should be built, say that and stop.

If a repo precedent or rejection ledger is available and directly relevant, use
it; do not spend tokens proving the same decision again. Log rejected scope when
the helper exists and the command is cheap:
`node scripts/log-rejection.js "<step>" "<item>" ["<replaced with>"] [--loc <n>]`.

## Never cut

Minimal never means unsafe. These survive every level, including ultra:

- Input validation and sanitization at trust boundaries.
- AuthN/AuthZ, rate limits, CSRF/XSS/SQL-injection protections.
- Error handling for I/O, network, parsing untrusted data, and data loss paths.
- Resource cleanup, transactions, and rollback where partial writes corrupt state.
- Failing tests are never fixed by deleting the test.
- Secrets are never inlined or logged.

If shorter code drops one of these, it is wrong.

## Levels

- **lite** - advise and name the smaller path, but follow specified structure.
- **full** - enforce the fast path; smallest complete diff wins.
- **ultra** - code is the deliverable. One sentence only when needed.

## Coexistence

If another style skill is active, keep these code-minimalism rules and yield
prose style to that skill. One voice.

## Language awareness

Prose trimming applies to your explanations, not the user's language. Never
strip words from non-English or mixed-language text (CJK included). Requested
foreign-language comments stay in that language.

## Honesty

Never invent savings numbers. Report only measured benchmark/ledger data, or
say it was not measured.
