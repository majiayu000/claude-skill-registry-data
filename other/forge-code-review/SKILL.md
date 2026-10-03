---
name: forge-code-review
description: Forge code-review method — order, severity levels, Codex handoff. Use before any commit or when asked to review code — code review, check my code, PR review, before I commit.
---

# Forge playbook — Code review method

**Self-improvement substrate (wp-skill-evals, 2026-07-31):** before applying this skill, read
`learnings.md` in this skill's own folder and honor its corrections. After a run that produced a
genuine correction (an owner fix, a false assumption caught, a preference stated), append it to
`learnings.md` with a date and real evidence — never invent a lesson that didn't happen.

**Do not duplicate ECC skills — defer to:** `code-review-excellence` (the deep per-language review
reference: React/Vue/Angular/Svelte/Rust/TypeScript/Java/PHP/Python/Django/Go/C#/Kotlin/NestJS/C/C++).
This file is the Forge-specific orchestration wrapper: the fixed review order, the severity scale, and
how a finding becomes a rework item in the Forge pipeline.

## Hard rules
- Review the real diff/files directly — never review a self-report of the diff, and never approve on the
  strength of "tests pass" alone without reading the actual change.
- Every finding is specific and actionable (file + line/symbol + what's wrong + the fix), never a vague
  "looks off."
- CRITICAL/HIGH findings block completion; they are not "nice to have later."
- Feedback targets the code, not the person; explain the reasoning, don't just assert a preference.
- A review is not a rewrite-to-taste pass — flag genuine correctness/security/maintainability issues, not
  personal style preferences that don't match a real project convention.

## Review order (fixed sequence — don't skip ahead to style)
1. **Correctness** — does the logic actually do what it claims; are edge cases the happy path hides
   named, not assumed away.
2. **Security** — secrets, injected input, auth/authz boundaries, unsafe deserialization, path traversal,
   anything on the mandatory security checklist (`~/.claude/rules/ecc/common/security.md`) for
   security-sensitive changes.
3. **Tests** — does new behavior have a real test; do existing tests still pass; is coverage of the
   changed logic genuine (not just line-count coverage).
4. **Simplicity** — is this the simplest correct solution, or is there unnecessary abstraction/complexity
   for what the task needed (YAGNI).
5. **Performance** — any obvious N+1 queries, unbounded loops/queries, or missing pagination/caching on a
   hot path.
6. **Style** — naming, formatting, project convention consistency — reviewed last, and never blocking on
   its own unless it actively harms readability.

## Severity levels
| Level | Meaning | Action |
|-------|---------|--------|
| CRITICAL | Security vulnerability, data loss, or broken correctness in a real path | **BLOCK** — must fix before done |
| HIGH | Real bug or significant quality/maintainability issue | **BLOCK or WARN** — fix before done unless owner explicitly accepts the risk |
| MEDIUM | Maintainability concern, not currently harmful | **INFO** — should fix, doesn't have to block |
| LOW | Style or minor suggestion | **NOTE** — optional |

## Codex handoff (optional, never a blocker)
For security-sensitive, auth, payments, database-migration, or other high-risk changes, this review MAY
be followed by an independent `codex-reviewer` pass (`/codex:review` read-only, or
`/codex:adversarial-review` for the required-review areas in `CODEX_GLOBAL_POLICY.md` (an owner-level policy in `~/.claude` when present; on an install without it, the defaults stated in this skill apply — read-only, never a blocker)). If Codex is
unavailable, report that honestly — the review above still stands on its own.

**The model comes from the EFFECTIVE config, and it is NOT a detail you restate from memory.** Read
`.claude/config/orchestration/codex-review.json` — the SHIPPED, template-owned default (engine, model,
reasoning effort, sandbox) — merged with the optional, NEVER-shipped
`.claude/config/orchestration/codex-review.user.json` (one account's own override, same shape, only
`review.model`/`review.reasoning_effort` can ever win from that file; every other field always comes from
the shipped file). `.claude/forge-bin/forge-codexreview-config.cjs::effectiveConfig()` does that
merge; its `buildCommand()` derives the real command as an **argv ARRAY** — never a hardcoded or
hand-concatenated shell string.

**WP-S14 finding 3.1 (2026-09-26 independent review):** the user-override file is gitignored and never
reviewed, so it may weaken nothing beyond the model/effort pin. Both are validated — an invalid value is
ignored, with a warning, and the shipped value is kept, never passed through. **The review sandbox is
hard-coded read-only** in `buildCommand()` — it is never read from either config file, so no override can
loosen it.

**Validation rule (N3 fix, 2026-09-26 independent review):** `review.model` is usable only when it matches
`^[A-Za-z0-9][A-Za-z0-9._:-]{0,63}$` — it must START with a letter or digit, never `-` (a leading dash
would make the "model" look like a CLI flag once it lands after `-m`, e.g.
`--dangerously-bypass-approvals-and-sandbox`). `review.reasoning_effort` must be one of (case-insensitive):
`minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Anything else is invalid and the shipped value is kept.

**The runnable, no-shell route:** `node .claude/forge-bin/forge-codexreview-config.cjs run [--adversarial]
--prompt "<review prompt or focus text>"` — this reads the effective config, validates it, derives the
argv, and spawns the real `codex` binary directly with `spawnSync(codexBin, argv, { shell: false })`; no
shell ever parses the model/effort/prompt values. A real run needs `--prompt`, a prompt starting with `-` is
refused, and on Windows the npm install's `codex.js` behind `codex.cmd` is found on PATH automatically
(`FORGE_CODEX_BIN` overrides). `run --dry-run --json` inspects the exact argv without spawning anything. `commandToDisplayString(argv)` (used internally for the subcommand's non-JSON display
line) is for a report/log line only and must never be re-parsed or re-executed.

**Portable default (no user file, or one that leaves `review.model` unset):** no model/effort pin at
all — the review runs on the codex CLI's own current default, and is reported honestly as
**"Codex default model"**, never a fabricated name. **Pinned:** an account's `codex-review.user.json` sets
`review.model`/`review.reasoning_effort`, and the command passes exactly those as `-m <model>` /
`-c model_reasoning_effort=<effort>`. This repo's own maintainer account currently pins `gpt-6-astra` at
`model_reasoning_effort=xhigh` in its own user file (owner directive 2026-09-24; long thinking = xhigh;
history: gpt-5.6-sol 2026-08-04 → HTTP 400 on that account 2026-09-24) — that pin lives in the
never-shipped user file, never in this shipped skill text, so a different account never inherits it.
Before the shipped config existed at all the model was pinned nowhere, so `/codex:review` silently used
whatever default the plugin happened to carry; reaching a specific pinned model can still need a newer
Codex CLI (gpt-5.6-sol needed ≥ 0.146.0 — 0.142.3 got an HTTP 400 telling it to upgrade, measured
2026-08-03).

**Name the step for what it is.** The planned work package is the **Codex code-review**, not an "ECC
code-review". ECC `code-reviewer`/`security-reviewer` is the *fallback* you use when Codex genuinely
could not run, and it is always labelled
`FALLBACK (non-independent) review — Codex did not run because: <reason>`. Planning the fallback as
the step quietly downgrades an independent review into a second opinion from the same model family
that wrote the code.

**Never attribute a review to a model that did not run it.** If the pinned model is refused
(400 / CLI too old / not authenticated), say which model actually ran, or that the review was blocked
— a verdict stamped with the wrong provenance is a fabricated review.

## Relationship to Review Boss
`forge-code-review` is the **method** — the checklist and severity scale anyone applies when reviewing
code, including Build Boss self-reviewing before handoff. **Review Boss** (`.claude/agents/review-boss.md`)
is the **agent identity** that runs this method (plus `verification-before-completion`, `design-is`,
`requesting-code-review` — the first and last ship with Forge as pinned vendored skills) as the final QA gate before a task is ever reported done. Use this skill
directly for an in-flight self-review; dispatch Review Boss for the end-of-task gate.
