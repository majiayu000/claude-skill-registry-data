---
name: triage-report
description: 'Drain the `.review/` report queue. Resolves un-triaged scan/audit reports (producer-agnostic — check-docs-consistency and any other scanner), dispatches the `triage-report` subagent (Sonnet) one report at a time for per-finding dispositions (promote / patch / dup / needs-investigation / dismiss), then the gateway absorbs: promotes batch through /super-bootstrap:log, doc-mechanical patches land per CLAUDE.md § Dispatch, investigations route to /super-bootstrap:triage, report deleted at close-out once every finding holds a terminal verdict. Use when a report lands in `.review/` or the user asks to process review findings. Does NOT fix findings.'
tags: [triage, review, report, pipeline]
---

# Triage Report — Review-Queue Drain

The scanner answered *is this hit real by its own rule*; this lane answers *is it worth acting on, and where does it route*. Producer-agnostic — fires on artifact presence in `.review/`, regardless of which scanner wrote the report. The thinking runs in the `triage-report` subagent (`agents/triage-report.md`, `model: sonnet`); this skill is the dispatch shell + absorption protocol.

## Target resolution

Argument is an optional report path. Without one, resolve from the queue — the directory IS the queue:

| `.review/*.md` glob | Behavior |
|---|---|
| 0 reports | Report "review queue clean", exit. |
| 1 report | Dispatch it. |
| N reports | Sequential, oldest-first — one dispatch per report. Later runs dedup against the cards earlier runs just promoted; never merge reports into one dispatch. |

## Execution — per report

1. **Dispatch:** `Agent` tool, `subagent_type: "triage-report"`, prompt = the report path + scan date if known. Nothing else — no gateway priors on which findings matter.
2. **Review the sheet** (gateway): coverage line must hold (findings = verdicts). Dismiss is the lossy verdict — a dismissal whose rationale doesn't beat the scanner's stated reasoning bounces back as `needs-investigation`.
3. **Absorb:**
   - **promote** → one batched `/super-bootstrap:log` pass carrying the agent's draft claim blocks. Rows land raw; the pipeline rolls at normal pickup.
   - **patch** → doc-mechanical edits only, landed per CLAUDE.md § Dispatch (gateway inline, or dispatched by closure). Anything wider re-verdicts as promote.
   - **dup** → fold any new-fact into the `/super-bootstrap:log` batch — rides the log door's amend path (dedup surfaces for the user's pick; the Amendment lands on the owning card).
   - **needs-investigation** → the single question rides `/super-bootstrap:triage` when it names a card; otherwise an investigate-only probe dispatch. Verdicts return to step 2.
4. **Close out** — only after every finding holds a terminal verdict and every patch has landed: delete the report; the deletion + a dispositions summary ride the session's envelope commit (dismissal rationales survive in git log).

A session ending mid-triage needs no recovery state: report still present = still un-triaged; re-run is idempotent (dedup absorbs already-promoted rows).

## Rules

- **Dispatch, don't disposition.** The verdict judgment runs in the subagent's clean context — fresh-context audit value dies if the gateway pre-judges findings inline.
- **One report per dispatch.** Each report gets its own dispatch, verdict sheet, and close-out.
- **All writes are gateway lane.** The subagent returns text only. Rows via `/super-bootstrap:log`, patches per § Dispatch, deletion at close-out.
- **Out of lane:** fixing findings (→ the pipeline, after a row exists); card root-cause work (→ `/super-bootstrap:triage`).
