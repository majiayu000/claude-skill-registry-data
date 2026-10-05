---
name: reasoning-trace
description: "Persist reasoning and decisions to disk before returning. Use whenever a non-trivial method, parameter, or phase-boundary choice is made; on a surprising result; at a handoff; or anytime a chat summary would be the only record. A decision with no trace is non-reproducible — capture the answer, delete the shell."
license: MIT
---

# Reasoning-Trace Skill

Decisions made in chat and never written down are non-reproducible. This skill documents the format and discipline for capturing decisions and findings as durable, git-tracked notes.

## Why

A chat summary is ephemeral — the next session has no access to it. A `/tmp` one-liner that produces a key number is gone the moment the shell closes. The only durable record is one that lands in the repo.

**Capture the answer, delete the shell.** When an exploratory probe yields an insight, commit the insight to a trace note and discard the scaffolding. The probe itself is not the artifact — the answer is.

---

## Where traces live

The question's scope owns the note. A stage-scoped note uses the stem of its
`02_analysis/stages/NN_<stem>.*` file; work that spans or precedes stages uses `_project/`.

| Purpose | Path |
|---|---|
| Stage decision or finding | `docs/_internal/<stage-stem>/<topic>.md` |
| Cross-stage decision or finding | `docs/_internal/_project/<topic>.md` |
| Literature or web research | `docs/_internal/_project/<topic>.md` |
| Current work state | `docs/_internal/<stage-stem>/session.md` or `docs/_internal/_project/session.md` |
| Throwaway probes | `_scratch/` or `$TMPDIR` only — never committed |

Use a stable topic slug. `session.md` is always the live record; a handoff moves
the copy it supersedes into `session-history/<UTC timestamp>.md`.
Create the owning scope with its first real note if absent.

---

## The note format

```
# <Short descriptive title>

**Date:** YYYY-MM-DD  ·  **Role:** <who/what wrote this>  ·  **Project:** <project name>

## Scope
One sentence: what question or phase this note covers.

## Sources
- What was read, run, or consulted to reach the decisions below.
- Include stage paths, data file paths, or paper DOIs as applicable.

## Decision 1 — <short label>

**Evidence:** What the data, literature, or probe showed.

**Decision:** The choice made (parameter value, method, phase boundary, …).

**Why not (alternatives rejected):** Named alternatives considered and the reason each was rejected. At minimum one sentence per rejected option.

## Decision 2 — <short label>

[repeat the evidence → decision → why-not block]
```

Keep the note skimmable: one block per decision, no prose padding, no restating evidence already visible in the cited sources.

---

## No-ephemeral discipline

**Throwaway probes** — exploratory R/Python snippets, shell one-liners, scratch notebooks — live exclusively in `_scratch/` or `$TMPDIR`. They are never committed.

**Once a probe yields an answer**, the answer moves into a reasoning trace and the probe is deleted or left in `_scratch/`. The trace is what gets committed.

**Every `03_results/` artifact** must be reproducible from a committed `02_analysis/stages/NN_*` stage. A result traceable to no committed stage is a guess.

Do not write to `/tmp` and reference the path in a note. Write the *number*, *table*, or *conclusion* into the note directly; the shell that computed it can be deleted.

---

## When to write a trace

Write before proceeding whenever:

- A **non-trivial method or parameter choice** is made (e.g., resolution, normalization strategy, reference atlas, statistical test).
- A **phase boundary** is crossed (e.g., moving from QC to clustering, from clustering to annotation).
- A **surprising result** appears — record what was expected, what was observed, and the leading hypothesis.
- A **handoff** occurs — the note is the context packet for the next session or agent.

Routine operations (re-running a committed stage with no parameter changes) do not require a trace.

---

## Done when

- The decision and at least one rejected alternative are written to a topic note in the scope that owns it.
- Every `03_results/` artifact produced since the last committed stage has a committed `02_analysis/stages/NN_*` that reproduces it.
- No non-trivial reasoning lives only in chat or in a `/tmp` file.

---

## See also

- `scrna-pipeline-conventions`
- `figure-style`
