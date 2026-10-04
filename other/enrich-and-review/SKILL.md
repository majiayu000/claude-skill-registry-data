---
name: enrich-and-review
description: "Runs the enrichment pipeline over plan chunk directories."
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Agent"]
argument-hint: "[stub-ids|directory-path|'all']"
---

# Enrich and Review — Enrichment Pipeline for Plan Stubs

Run the enrichment-review pipeline on a chunk directory: dispatch Sonnet enricher agents, then
Opus reviewers, sequentially. Nothing computes this pipeline for you yet — every phase below is a
manual EM procedure over theoretically computable facts (stub discovery, independence
verification, status transitions); worked detail and phase archaeology: wiki.

Not an EM step on the M/L four-turn loop — this skill runs for backlog runs and hands-on re-plans
(`em-loop-factfind.md` §1, census rows 7 and 8).

<!-- Negative-spec: this block is single-sourced at snippets/project-rag-preamble.md and kept in
     sync across every consumer (this file, the plan-writing doctrine wiki, enricher/executor
     dispatch prompts, scout templates) by an automated gate —
     `bin/verify-snippet-sync project-rag-preamble --check/--fix`, wired into /workday-start
     Step 1.7. Do not fold or hand-edit this block independently — edit the source and let the
     gate sync. -->
<!-- BEGIN project-rag-preamble (synced from snippets/project-rag-preamble.md) -->

**Code lookup: project-rag first.**
`ToolSearch("select:mcp__project-rag__project_staleness_check,mcp__project-rag__project_symbol,mcp__project-rag__project_symbol_callers,mcp__project-rag__project_symbol_references,mcp__project-rag__project_symbol_brief,mcp__project-rag__project_referencers,mcp__project-rag__project_semantic_search,mcp__project-rag__project_rag_instructions")`
`project_staleness_check`; callers `project_symbol_callers`/`_references`; impact `project_referencers`; else `project_rag_instructions`.
If a project-rag call errors or its tools are absent (daemon down), fall back to Grep/Read and carry on.
Friction: memo `project-rag-em` / `gh issue create -R dbc-oduffy/project-rag`.
<!-- END project-rag-preamble -->

## Arguments

`$ARGUMENTS`: a directory path → chunk directory; specific stub IDs ("2A 2B 2C") → enrich only
those; "all" → enrich everything at "Pending enrichment"; `--reviewers "name1,name2"` → explicit
reviewer override, dispatched in listed order (first = domain pass, second =
architectural/generalist), replacing Phase 5 routing-table auto-detection — the mechanism for
PM-directed dual-review setups.

## Phase 0: Plan Review Gate

HALT before enriching anything unless the source plan's header carries a `**Review:**` line
matching "Reviewed by [name] on [date]", "Skipped per PM direction", or the byte-exact marker
string pinned at `coordinator/skills/staff-session/SKILL.md` Step 8, item 2 (produced by
`/staff-session --mode plan` Step 8 — read it from there, never hand-type a second copy). No match
→ "This plan has not been through review. Route it through `/review` first, or confirm PM override
to skip." Prevents wasting enrichment cycles on a structurally unreviewed plan.
<!-- engine-gap: field=plan.review_marker_present producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->

## Phase 1: Discover Stubs

Read the tracker README/chunk index, identify stubs at "Pending enrichment" or equivalent,
classify each survey-type (external assets, unfamiliar codebases), plan-type (known codebase, file
paths + steps), or manual (non-delegatable) — an EM judgment over the stub text. Report the split.

## Phase 2: Independence Verification

Before parallel dispatch, read each stub's Files-Affected/Scope, build a file→stub map, force
sequential enrichment for stubs sharing a file. Report the parallel/sequential split.
<!-- engine-gap: field=tracker.stub_file_overlap producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->

## Phase 2.5: Write-Ahead Status Update

Before dispatching any enrichers: `tracker.advance_status`
(`coordinator_core/ops/tracker/advance_status.py`) with `tracker_path=<tracker README>`,
`stub_ids=<about-to-be-enriched>`, `to_status="Enrichment in progress"` — flips status atomically,
does NOT self-commit. **Commit the tracker README change immediately after, before any enricher
launches** (scoped commit) — the commit is what makes the WAL record durable, not the op call.

**Negative-spec:** this op's write target (a caller-supplied tracker README path) carries no
ratified DR carve-out — check the op's own "Provisional classification" docstring note before
treating its authority here as settled.

## Phase 3: Dispatch Enrichers

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

Optional task-scoped repo map via `misc-session-and-guards.py rag-freshness-gate` when the stub's
file scope benefits from one — pass its path in the dispatch prompt (judgment call, not every
dispatch needs it). Scan enabled plugins for root-level `enricher-pre-pass.md` fragments — these
run in the EM's own context (full tool access, MCP) to gather what the enricher's tools can't reach
(e.g. live Blueprint property surfaces); include their companion-artifact paths in enricher
prompts. Separately scan for `enricher-survey.md` fragments matching `project_type` and fold into
the survey-type dispatch prompt (fall back to the enricher's generic protocol if none match).

Independent stubs → parallel Sonnet enricher dispatch (`Task`, `subagent_type: "enricher"`,
`model: "sonnet"`, `run_in_background: true`, single message). Dependent stubs → sequential,
waiting for each to complete. Manual stubs → report to PM/Coordinator.

## Phase 4: Resolve Coordinator Flags

Read each enriched stub for `NEEDS_COORDINATOR:` flags, decide from project context/design
docs/PM direction, write the resolution back replacing the flag. Escalate if uncertain.

## Phase 4.5: Pre-Review Status Update

Same op as Phase 2.5 with `stub_ids=<enriched stubs>`, `to_status="Under review"`; commit
immediately after.

## Phase 5: Dispatch Reviewers

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

Selection: explicit `--reviewers` override, or auto-detect (classify enriched-stub work type,
merge this plugin's `routing.md` with every enabled plugin's root-level `routing.md` fragment,
match). **Persist findings to the provisioned sidecar, no EM pre-scaffold** — each reviewer's
dispatch brief carries its `state/subagent-share/<session>/<provision_key>.md` path
(`provision_report`-injected); reviewer writes ReviewOutput there and returns `DONE: <sidecar-path>
| verdict: <OK|WARN|BLOCKED> | findings: <N>` (detail: wiki).

Sequential dispatch with fix-application gate: dispatch Reviewer 1 (scope = all enriched stubs)
→ STOP, Reviewer 1 applies and verifies its ledger against the returned sidecar path (every
finding, spot-checked diff) → only then dispatch Reviewer 2 on the corrected stubs (fresh sidecar
path, no injection needed) → STOP, Reviewer 2 applies and verifies its ledger the same way.
Single-reviewer case skips the second pass but keeps the fix-application step. Conflicting
feedback: apply unless it conflicts with stated requirements or PM direction, document overrides
with rationale in the stub, escalate genuine uncertainty.

**The enriched-artifact duty is contract, not brief text.** The contract is injected at dispatch
for every `REVIEWER_ROSTER` member. A resolved reviewer whose `contract_blocks:` row in
`coordinator/subagent-sandbox-policy.yaml` does not list `enriched-artifact-review-contract`, or
that has no row, gets the **path** `coordinator/snippets/enriched-artifact-review-contract.md` in
its dispatch, never a paraphrase. No brief restates the duty's text: a duty retyped per dispatch
is the duty this ceremony already lost once. Tripwire: `A-DUTY-ONLY-A-BRIEF-CARRIES-DISAPPEARS-WITH-THE-EM`.

## Phase 6: Update Tracker

Same op with `stub_ids=<reviewed stubs>`, `to_status="Enriched and reviewed"`, commit immediately
after. Note manual-flagged stubs and any needing PM decision.

## Completion

Report: stubs enriched, stubs reviewed (and by whom), outstanding flags/PM decisions, which stubs
are ready for executor dispatch, and — when this ran unattended — the accepted losses at
`state/audits/2026-09-07-em-carried-obligations-census/accepted-losses.md`, named, not summarised.
Four duties on this path have no carrier once no EM is in the loop; the run did not perform them,
and the report is where an operator finds that out rather than inferring it.
