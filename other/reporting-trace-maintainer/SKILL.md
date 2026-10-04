---
name: reporting-trace-maintainer
description: Maintain report-ready work traces while Codex executes tasks, research, repo changes, experiments, or project work. Use when the user asks to keep work logs, prepare future advisor/stakeholder reports, preserve meeting/update evidence, or when working in a repo with reporting trace conventions such as `reports/work-traces/`, task graph files, project indexes, evidence manifests, or decision logs. This skill records intermediate trace material; use `project-briefing-room` or another reporting skill later to write the outward-facing briefing.
---

# Reporting Trace Maintainer

Maintain a light trace layer that can later become an advisor update, stakeholder briefing, weekly report, or project status note. The trace is not the final report; it is the structured raw material behind one.

## Core Idea

During task execution, preserve the chain:

```text
last plan -> work done -> evidence -> interpretation -> next plan -> questions
```

This mirrors effective research/advisor update practice: make progress visible, expose blockers early, and leave clear next actions without turning every task into a polished report.

## Workflow

1. Locate the trace convention.
   - In a repo, first look for `reports/work-traces/README.md`, `codex/workflows/reporting-trace-contract.md`, project `INDEX.md`, task graph files, and `codex/project-map.md`.
   - If no convention exists and the user asked for durable traces, create or suggest a minimal `reports/work-traces/` structure.

2. Decide whether a trace is needed.
   - Write or update a trace when the task changes project state, produces evidence, resolves a blocker, creates a decision point, or will likely need advisor/stakeholder reporting.
   - Skip durable trace updates for trivial commands, private credentials, purely local cleanup, or work that the user explicitly wants to keep out of long-term notes.

3. Choose the trace location.
   - Prefer `reports/work-traces/<project>/<YYYY-MM-DD>-<task-id-or-slug>.md`.
   - If a project already has a local trace convention, follow it.
   - Keep bulky artifacts in the project/artifact repo and link them; do not copy large logs, PDFs, screenshots, datasets, or raw private material into the trace.

4. Record only report-useful facts.
   - Include previous plan, work performed, evidence links, interpretation, decisions or decision needs, blockers, next plan, and questions.
   - Separate facts, inference, user preference, and pending verification.
   - Use repo-relative paths when possible; use external paths only when the repo already permits them or the path is the execution boundary.

5. Keep source-of-truth files aligned.
   - If task state changed, update the task graph or project index according to the repo contract.
   - If a decision was made, route to `decision-record-writer` or add a decision pointer.
   - If evidence was collected, update the relevant evidence manifest or project evidence file.

6. Close each task with a trace delta.
   - Mention the trace path in the final response when you created or updated one.
   - Do not claim a final report exists unless you actually wrote one.

## Trace Sections

Use this compact shape by default:

```markdown
# Work Trace: <Task Title>

Updated: YYYY-MM-DD
Project: <project-id>
Task: <task-id or short slug>
Audience Future Use: advisor-update | stakeholder-status | weekly-review | project-briefing | internal
Status: active | paused | completed | blocked

## Last Plan

- ...

## Work Done

- ...

## Evidence

| Evidence | Path / Source | What It Supports | Confidence |
|---|---|---|---|

## Interpretation

- Fact:
- Inference:
- Uncertainty:

## Decisions / Open Decisions

- ...

## Next Plan

- [ ] ...

## Questions For Next Meeting

- ...
```

For detailed schema rules and examples, read `references/trace-schema.md`.

## Boundaries

- Do not store secrets, tokens, cookies, private raw transcripts, or sensitive personal details.
- Do not turn a trace into a polished outward-facing narrative unless the user asks.
- Do not invent work, evidence, or decisions to make a trace look complete.
- Do not duplicate bulky artifacts; link to their maintained location.
- Do not overwrite user-written project truth. Update narrowly and preserve existing wording when possible.

## Handoffs

- Use `project-briefing-room` when the user wants a stakeholder-facing project status briefing.
- Use `evidence-synthesis-docs` when many traces or evidence records need synthesis.
- Use `decision-record-writer` when a tradeoff or workflow choice should become durable.
- Use `codex-deep-interview` when the report audience, non-goals, or decision boundary is unclear.
