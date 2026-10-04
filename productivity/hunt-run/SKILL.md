---
name: hunt-run
description: Execute a hunt phase with parallel telemetry work, query logging, receipt generation, and optional wave targeting
argument-hint: "<phase> [--wave N] [--gaps-only] [--interactive]"
allowed-tools: Read, Bash, Write, Task, AskUserQuestion, WebSearch
---

<objective>
Execute a hunt phase.

Documented flags are available behaviors, not implied active behaviors.
Treat `--wave N`, `--gaps-only`, and `--interactive` as active only when the literal token appears in `$ARGUMENTS`.
If none of these tokens appear, run the standard full-phase execution flow.

The execution boundary is the shared THRUNT runtime contract:
- each material hunt action is shaped as a `QuerySpec`
- connectors return one normalized result envelope
- query logs and receipts are emitted from runtime metadata, not connector-specific ad hoc blobs
- connector-backed execution can be inspected locally with `thrunt-tools runtime list-connectors`, `thrunt-tools runtime doctor`, `thrunt-tools runtime smoke`, `thrunt-tools pack render-targets`, and `thrunt-tools runtime execute`

`--wave N` executes only a single wave and must not mark the whole phase complete until no incomplete plans remain.

**Creates or updates:**
- `.planning/QUERIES/*.md`
- `.planning/RECEIPTS/*.md`
- Phase `SUMMARY.md`
- `.planning/STATE.md`
- `.planning/HYPOTHESES.md` when new pivots emerge
- `.planning/HUNTMAP.md` when phase status changes

**After this command:** Run `/hunt-validate-findings <phase>`.
</objective>

<context>
Available optional flags (documentation only):
- `--wave N` — run only Wave `N`
- `--gaps-only` — run only gap-closure plans
- `--interactive` — stop after each wave for operator review

Active flags must be derived from `$ARGUMENTS`.
Do not infer that a flag is active just because it is documented in this prompt.
`--interactive` is active only if the literal `--interactive` token is present in `$ARGUMENTS`.
If none of these tokens appear, run the standard full-phase execution flow.
</context>

<execution_context>
@.github/thrunt-god/workflows/hunt-run.md
@.github/thrunt-god/templates/query-log.md
@.github/thrunt-god/templates/receipt.md
@.github/thrunt-god/templates/summary-standard.md
</execution_context>

<process>
Execute the hunt run workflow from @.github/thrunt-god/workflows/hunt-run.md.
Every non-trivial claim must cite receipts. Parallelize by telemetry domain when it helps.
When query execution occurs, treat `/hunt-run` as a `QuerySpec` producer and normalized-result consumer.
If the requested phase has not been planned yet, stop and instruct the operator to run `/hunt-plan <phase>` first instead of improvising execution.
Keep query-log `related_receipts` and receipt `related_queries` links exact and bidirectional for artifacts created in the run.
Before closing out, update `HYPOTHESES.md`, `STATE.md`, and `HUNTMAP.md` so hypothesis confidence and phase completion match the receipts actually collected.
When updating `HUNTMAP.md`, sync all affected surfaces: phase checkbox, per-plan checklist entries, and the progress table row for the executed phase.
When onboarding or debugging a real connector, use `thrunt-tools runtime doctor [<connector-id>]` before running hunts, and use `thrunt-tools runtime smoke [<connector-id>]` for a live read-only certification query.
When a phase is explicitly pack-backed, prefer `thrunt-tools runtime execute --pack <id>` or inspect the generated specs with `thrunt-tools pack render-targets <id>` before running.
</process>
