---
name: end-of-week
description: >-
  Run a seven-day governance review for an XYZ Forge or XYZ-vendored repository:
  check GitHub default-branch reconciliation, compare RebalanceOS HiQS and git
  activity with PDDA/RELEASES/XYZ metadata, file a ranked umbrella issue, correct
  verified metadata, and refresh the configured project kanban through its
  canonical writer. Use for End of Week, /end-of-week, or a weekly governance
  and kanban refresh. Governance script changes are recommendations only.
---

# End of Week

Own two outcomes: an accurate Project Kanban board and an evidence-backed start to
**governance automation script recalibration**. This skill is for capable reasoning
models across providers; it requires no particular model, CLI vendor or model install.

A user-requested End of Week run authorizes additive GitHub issue creation/update,
verified project-metadata corrections and configured board updates through existing
writers. Show the concrete intended changes, then apply them without another approval
round. Follow the target repo's publication policy. Reading this skill for authoring,
review or explanation does not invoke its operational write scope.

## Recite the contract

Print this block at **startup**, **after compaction/resume**, and **once at initial
completion**. Do not repeat it at every response or tool call.

> **End of Week — six tasks**
> 1. Check that reconciliation on origin's primary branch, as configured in GitHub, is clean/green.
> 2. Run supported reconciliation if needed and verify the result.
> 3. Compare RebalanceOS HiQS signal, local git activity and origin git activity; diagnose process and script gaps in PDDA, RELEASES SQLite (PRS), and XYZ metadata.
> 4. File an umbrella GitHub issue with the top ten evidenced gaps/changes, their diagnosis, prognosis, recommendations, and potential governance-script updates.
> 5. Correct verified project metadata through its canonical writers.
> 6. Update the Project Kanban board from authoritative metadata and verify it by reading it back.
>
> **Two goals:** Update Project Kanban; begin governance automation script recalibration.

The first completion recital is a **single evidence audit**, not a restart: compare
all six tasks and both goals against their receipts, finish missing in-scope work,
and report remaining blockers honestly. Do not refile issues, replay completed writes
or repeat completion indefinitely. Save the resolved repo identity, window, issue URL,
base/result SHAs, evidence pointers, intended/applied changes and next action in the
repo's existing run/issue record and compaction handoff. Mark whether the completion
audit has already occurred. A resume re-reads these and revalidates current state.

## Scope and operating boundaries

Default review window: **the last seven days**, ending at the run's recorded UTC start.
Record both boundaries. Inspect current governance state too: an ongoing blocker does
not disappear because its first incident is older. A weekly ranking snapshot is not
a seven-day history. Respect a user-supplied window and keep it fixed on resume.

Use the installed debug-mantra and recon skills for diagnosis and source tracing when
available. Their core protocol is sufficient if a downstream install lacks them:
observe the actual mismatch, trace its reader/writer path, test the strongest contrary
explanation, and retain the evidence. For each recommendation, name what would prove
it wrong and a falsifiable acceptance check. Do not turn a weekly review into a refactor.

Do not implement governance script changes, migrate/install missing infrastructure,
change GitHub's default branch, merge unrelated PRs, force-push, discard local work,
clear kill switches, or invent completion/release evidence. Preserve operator ratings,
overrides and deliberate board mappings. No automatic model switching or scheduler.

**Before every metadata writer, including reconciliation and umbrella intake/rating:**
establish connector containment. Suppress post-write connectors for all unmerged or
task-clone writes using the documented per-process `XYZ_WORK_CONNECTORS=0` control.
Even on an authoritative store, permit dispatch only after the effective configuration,
repo identity and kill-switch checks in task 6 have passed. Otherwise keep dispatch
suppressed for the write and retain the pending events for the verified board step.
This rule applies from the first write; reaching task 6 is not the first time it applies.

## Workflow

1. **Resolve the target and establish reconciliation health.**
   Read the target's ROUTER/AGENTS/SOP and relevant PDDA/RELEASES contracts. Resolve
   the **consumer repo root** separately from the **installed harness root**. The
   current checkout or a vendored `.xyz` directory is not automatically the consumer.
   Use the installed `harness_paths` resolver/locator where available, then verify
   origin and the target identity. Inspect the selected tool's help before invoking it.

   Query GitHub's current `defaultBranchRef.name`/`default_branch` for that origin
   repository (for example, `gh repo view --repo "$REPO" --json defaultBranchRef`).
   Fetch and record that branch's current SHA; do not infer it from local HEAD, a stale
   origin/HEAD or a hardcoded main/development name. Read checks and reconciliation
   runs for the relevant SHA, including the actual workflow's target and resulting
   reconciliation commit. Verify lineage when the workflow creates a new commit;
   an older successful run does not establish current health.

   Inventory local dirty files, stashes, local-only refs/commits and registered task
   clones/worktrees read-only, plus origin issues, PRs and commits. Scope extra clone
   discovery to the user's configured roots/registry and verified matching origins;
   never sweep arbitrary personal directories. Preserve active sessions and local-only
   work. Use an isolated full clone when the repo requires one for writes or tests.
   Run applicable deterministic metadata checks, recording errors, warnings and skips
   separately. Missing evidence is **unknown**, not green.

2. **Reconcile only through a supported path.**
   Prefer the repo's existing hosted reconciliation owner; inspect active runs before
   dispatching a needed catch-up. Otherwise use the documented local writer on a fresh
   snapshot with its branch/cleanliness/rollback guards intact. Review the proposed
   changes before applying and verify the resulting metadata and origin state.

   In XYZ versions whose `wave_reconcile.py` and hosted workflow still assume
   development, a different GitHub default branch is an **unsupported-target gap**.
   Do not substitute development, pass skip-branch guards or alter scripts to get green.
   Continue independent evidence collection and supported metadata corrections on the
   intended branch; report the missing reconciliation capability in the umbrella issue.

   Allow at most two attempts for the same failed operation; retry only after new
   evidence or a recoverable condition changes. Wait for hosted jobs in bounded polls
   and use their documented timeout. Do not override an in-flight writer lock. A
   failed check remains failed until new evidence establishes recovery.

3. **Triangulate activity and rank the gaps.**
   Resolve Rebalance through the user's installed MCP connection/configuration first.
   Prefer `index_status()`, `get_next_actions()` and `list_watched_repos(since_days=7)`.
   The relevant HiQS signal is the **persisted ranked-next-actions cache**, not the
   separate `HiQS/hiqs` search package. Retain `computed_at`, cache row count and source
   ingestion timestamps. Correlate actions using exact repo URLs/issue/PR IDs or verified
   registry mappings; semantic similarity or a nickname alone cannot authorize a write.

   Supporting retrieval may use `ask(..., since_days=7, skip_synthesis=True)` or the
   installed `semantic_query` with repo/date filters where its current schema supports
   them. Semantic top-k is not exhaustive; record caps and uncovered pages. Inspect
   git/origin evidence independently of Rebalance's cached GitHub data, deduplicating
   the same incident/commit across sources. A local commit is not a landed commit, a
   closed issue is not necessarily a shipped release, and an open PR is not a merge.

   If MCP is unavailable, use the user's configured installed Rebalance Python runtime
   and existing readers: `rebalance.paths.resolve_database_path`,
   `rebalance.ingest.next_actions.load_ranked_next_actions` and `get_ranked_meta`.
   Verify the resolved DB exists and is the intended configured store; do not create
   an empty replacement or silently accept another DB when an explicit path is wrong.
   Discover paths from existing configuration/registry or ask for the missing location.
   Do not embed an author's filesystem path, recompute rankings, or refresh unrelated
   personal sources. Missing/unreadable/stale/empty HiQS is a coverage gap; continue
   the independent git/governance checks and qualify the conclusion.

   Compare observed work with PDDA lifecycle/status/next steps and issue pointers;
   RELEASES release/roadmap/manifest state, ratings and evidence; XYZ work events,
   receipts, connector cursors and relevant metadata. Trace each mismatch to the
   responsible process and script before recommending changes. Distinguish observation,
   root-cause hypothesis and prognosis. Rank by consequence, blockers, recurrence and
   evidence confidence. Produce **up to ten substantive gaps**, fewer when warranted.
   Do not pad the list or invent severity to satisfy a quota.

4. **Proactively file the weekly umbrella issue.**
   Search the target repo for the same reporting window/run and related open issues.
   Resume/update the same-window umbrella instead of duplicating it. A new week's
   umbrella links prior unresolved work; it does not clone existing remediation issues.
   Title: `End of Week: governance gaps — <start> to <end>`, prefixed **Critical** for
   substantiated corruption/data-stability threats or **High priority** for blockers.
   Explain the qualifying finding and use matching existing labels where available.
   Routine findings retain an ordinary title. Do not label uncertain speculation as
   confirmed corruption.

   Include scope/default branch/SHA/window; source freshness and coverage; the ranked
   gaps grouped into meaningful segments; and, for each gap, evidence, diagnosis,
   prognosis if left unresolved, recommendation, candidate script/entry point,
   proposed acceptance check and confidence. Distinguish metadata fixes to apply now
   from **script updates recommended for follow-up**. Even a clean week may have a
   truthful zero-gap review record; never claim full coverage when a source was missing.
   Follow the target's issue/PDDA/RELEASES intake and rating rules through their writers.
   Read back the issue and registration. Only publish target-repo evidence and sanitized
   summaries: exclude private HiQS source text, credentials, local settings and personal
   filesystem paths. Keep detailed local evidence in the repo's ignored scratch area
   unless sanitized and deliberately promoted under its provenance contract.

5. **Correct verified metadata and publish it normally.**
   Record each affected stable ID/path, old value, intended value, supporting evidence
   and undo action. Re-read before mutation; changed evidence or a concurrent edit needs
   reassessment, not overwrite. Edit human-owned PDDA fields narrowly; use RELEASES CLI
   verbs for its DB/dump/events and established generators for derived views. Never
   hand-edit SQLite, SQL dumps, work-event history, cursors or generated board state.

   Follow the target's commit/PR/publication policy. Preparing a correction in a task
   clone does not make it authoritative: suppress its post-write connectors with the
   documented per-process `XYZ_WORK_CONNECTORS=0` control where needed, without changing
   persistent user settings. Do not project unmerged task-clone state onto the live board.
   If landing requires a merge outside this run's authorization, publish the correction
   PR and report **pending landing**; refresh only independently verified authoritative
   state. Preserve deliberate overrides. Re-run the relevant checks after applying;
   stop a failed write sequence, retain its partial state, and use supported compensating
   corrections rather than overwriting a whole shared checkout. Record before/after
   evidence and unresolved items in the weekly issue.

6. **Refresh the configured kanban and prove the outcome.**
   Inspect the consumer's existing `.xyz` settings/wiring, then use the installed
   canonical resolver. In current XYZ, `device_config.get_device_config_path()` reads
   `XYZ_DEVICE_CONFIG_PATH` or the user's `.xyz/device_config.json`; a repo-local file
   applies only when existing wiring/that override selects it. These locations are not
   interchangeable. Do not add a new settings store or copy machine config into git.

   Resolve `work_connectors.github_board` plus its `board_sync` fallback settings and
   runtime overrides. `board_sync.py config` helps inspect the fallback, but is not
   the complete effective connector configuration. Verify enabled state, owner/project,
   repo scope and `status_map`; discover field/option IDs through the existing writer.
   The current writer targets `repos[0]`: require it to match the consumer origin.
   Missing/ambiguous settings require only the missing clarification; do not guess a
   board or create columns. Disabled connectors stay disabled and are reported as such.

   Use the RELEASES **work** path for issue lifecycle kanban. With `HARNESS_ROOT` and
   `REPO_ROOT` resolved and verified at this invocation, current command shapes are:

   ```bash
   python3 "$HARNESS_ROOT/utils/py/releases_app.py" --root "$REPO_ROOT" work backfill --dry-run
   python3 "$HARNESS_ROOT/utils/py/releases_app.py" --root "$REPO_ROOT" work reconcile --connector github_board
   ```

   `work reconcile` is a write, not a preview. Inspect pending events, target config and
   authoritative metadata first. Apply `work backfill` without `--dry-run` only when
   historical metadata needs projection events and the preview is correct; it can
   dispatch enabled connectors, so account for that before invoking it. Do not use
   `board_sync.py touch/reconcile` as lifecycle repair: those represent work starts.
   `releases project sync` updates release cards, not issue lifecycle kanban.

   Reconcile pending batches; current dispatch caps a batch at 500 events. Stop on a
   failed batch or no cursor progress; at most ten batches per invocation before an
   explicit partial handoff. Use `--reset` only for evidenced projection drift that
   requires replay, never routinely. Re-read current source/help if these capabilities
   differ in the installed version; missing functionality becomes a script proposal.
   Honor both board/work connector kill switches rather than assuming the two CLI
   paths enforce the same one. Keep unrelated connectors/cards outside the correction.

   A zero exit does **not** prove success: connector dispatch is deliberately fail-soft.
   Inspect FAILED/skipped diagnostics and cursor/pending-event state, then fetch a fresh,
   fully paginated board snapshot through the established reader (or read-only GitHub
   tooling). Compare each intended repo-qualified card/status with the configured map.
   Report corrected, already current, pending landing, disabled, failed and unverified
   outcomes distinctly. Do not publish a new board writer or bypass the canonical one.

## Completion report

Perform the one-time completion recital/audit above. Return the umbrella issue link,
up to ten ranked gaps, metadata corrections made, recommended governance-script changes,
board verification result, source-coverage limits and the next unresolved action.
State both goals separately: a filed issue begins recalibration; it does not mean scripts
were fixed. A successful writer call without matching read-back does not mean the board
is updated. Preserve a resumable record for anything incomplete.
