---
name: expert-usage
description: This skill should be used when the owner asks to "use the expert plugin", "use expert-dev-tools", "run the expert workflow", "run this through /expert", "build this with the expert lifecycle", or invokes `/expert`. It explains what the plugin does, how to start and resume a lifecycle, what each owner gate means and what answering one does, what must never be done while a lifecycle is live, and how to report a defect in the plugin itself. Read it before invoking `/expert` for the first time in a session.
version: 0.1.0
---

# Using expert-dev-tools

This plugin runs engineering work through a gated lifecycle: **spec → architecture →
plan → implement → review → ground truth → closeout**. A workflow script drives the
whole chain and dispatches a typed agent for each phase. Each artifact is reviewed by
an independent agent before the next phase starts, and the owner is consulted only at
gates.

The value is that no phase advances on an unverified claim. That property holds only
when the workflow drives the work. Running the phases by hand produces the shape of
the lifecycle with none of its guarantees.

## What runs where

| Component | Role |
|---|---|
| `/expert` (this agent) | hears the owner, invokes the workflow, presents what comes back |
| `workflows/expert-lifecycle.js` | drives every phase, dispatches every agent, operates every gate |
| `agents/expert-*` | do the phase work; the workflow dispatches them |
| `skills/expert-*` | the disciplines the phase agents follow — dispatched agents load these, not this agent |

Do not read the other `expert-*` skills to run a lifecycle. They are for the agents the
workflow dispatches.

## Starting a lifecycle

Invoke `/expert <what to build>`.

Two things happen before any phase runs. First, classify the owner's turn: a question
gets an answer and starts nothing; only an instruction to do work opens a lifecycle.
Second, copy the owner's turn text verbatim into the ledger's `task_verbatim` field —
unedited, unsummarized, unnormalized. That text is the authoritative statement of the
request, and every downstream phase receives it. A restatement is not a substitute.

One invocation runs until the workflow returns — either at a gate or complete.

## What comes back, and what to do with it

The workflow cannot pause. When it needs the owner, it **ends its run** and returns an
owner gate. Nothing is lost: the ledger holds the state.

The outcomes:

- **`owner_gate`** — present it to the owner in plain language: what happened, the
  options, and the recommendation. Take the answer. Resume with `/expert resume`.
- **`complete`** — the work is verified and closed out. A CORE ingestion message is
  drafted for the owner's approval; present it and never ingest without explicit
  approval.
- **A halt inside a phase** — the workflow already routes these; present what it returns.

Resuming continues from the ledger. It does not restart the lifecycle and does not
re-run finished phases.

There are seven gate types, and that list is exhaustive — the owner is interrupted for
exactly these and nothing else. See `references/gates.md` for what each one means, what
the answer decides, and which ones indicate a defect rather than a decision.

## While a gate is open

Write authority narrows to the ledger, review records, and STATUS. Discussing a gate
with the owner is not authorization to change an artifact. If the discussion produces a
decision, record it and resume the lifecycle — the change happens through the phase
that owns it, not inline.

## Never do these

**Never patch the plugin to get past a problem.** A workflow that misbehaves is a defect
to report, not an obstacle to route around. Editing the plugin mid-run invalidates every
guarantee the run was producing and leaves the defect in place for the next project.

**Never edit an upstream artifact directly.** A spec, architecture, or plan changes only
through the amendment path the workflow operates. On finding a defect in one, record the
discrepancy and let the gate route it.

**Never hand-run the phases.** Dispatching phase agents directly, or writing dispatch
prompts, replaces fixed contracts the workflow owns with improvisation. The workflow's
dispatch text is identical every round by design; that is what makes rounds comparable.

**Never answer a gate on the owner's behalf.** A gate exists because the workflow
determined it could not decide. Choosing an option to keep things moving discards the
one input the gate was built to collect.

## When the plugin itself is the problem

Symptoms: the workflow crashes or contradicts itself; a gate asks for something
impossible; a phase demands an artifact that cannot exist; the same failure recurs after
a clean re-run.

Read before filing. The plugin carries its own defect queue at `docs/defects/`, with a
generated index at `docs/defects/README.md`; the deployment preflight reports the open
count on every run. A problem already recorded there is usually already diagnosed, and
what looks like a new failure is often a known one — check first.

If it is not there, do not patch and do not invent a location for notes. File it in the
machine-wide defect store, which is reachable from every project, survives plugin
updates, and is already read by the recurrence machinery that decides whether a problem
is a one-off or systemic:

```
~/.claude/plugins/data/expert-dev-tools/defect-history.json
```

The record format, the fields that matter, and how recurrence is judged are in
`references/defect-reporting.md`. Report the observed behavior and the evidence for it.
Do not propose a fix in the report — diagnosis is a dispatched role with its own
verification duties, and a guessed fix in the store becomes the next session's false
premise.

## Additional resources

- **`references/gates.md`** — the seven gate types: what each means, what answering
  decides, and which ones signal a defect rather than a decision.
- **`references/defect-reporting.md`** — the defect record format, where it goes, and
  what makes a report actionable.
