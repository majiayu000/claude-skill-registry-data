---
name: resuming-a-run
description: Use when picking up a delivery run whose context you do not have — a run halted at a gate, a run someone else started, a run from last month, or any cold session where the next step must be determined from disk rather than from chat history. Also use before opening a new run, to prove the previous one is actually closed. Operationalises the handoff protocol's statelessness property.
version: 0.1.0
---

# Resuming a Run

## Overview

The handoff protocol asserts **statelessness**: *any agent can be invoked cold and reconstruct
what it needs from the run workspace alone.* That is a property of the design, but it is only
true if someone actually performs the reconstruction rather than leaning on session memory.

This skill is that procedure. It answers four questions, in order:

1. Where does this run stand?
2. What is the next step?
3. Is anything blocking it?
4. What does the next agent need in its hands?

**Core principle: the workspace is the truth.** Chat history, session memory, and recollection
are not inputs. If a fact you need is not on disk, that is a finding — the previous handoff was
deficient — not a reason to reconstruct it from memory.

## When to Use

- Resuming a run after any break, or one you did not start.
- A cold session that must determine the next agent to dispatch.
- Before opening a new run — to prove the previous one is closed (§6.1).
- Auditing: reconstructing why a decision was made, without reading transcripts.

**Do NOT use for:** `standalone` invocations. A bounded direct task needs no run workspace at
all (`agent-invocation-contract.md` §4).

---

## Framework docs (precheck)

Every `process/…` and `templates/…` path in this skill resolves from the project root first,
then from `.agents-factory/` in the project, then from `~/.agents-factory/` (or
`$AGENTS_FACTORY_HOME`). Find `process/agent-handoff-protocol.md` in one of those before
anything else. If none has it, stop and tell the human to install the framework docs —
`scripts/install.sh --target docs` from an agents-factory checkout, or re-run their platform
install — and do not proceed from memory of what the documents say.

## Step 1 — Read `state.md` first

`runs/<run-id>/state.md` is the Orchestrator-owned digest, kept under ~100 lines. It is a
**digest, not a log** — it points; the detail lives in the handoff files. Read it for:

- current phase and active task
- open risks by ID
- open questions
- gate status
- the last five handoffs by number

Treat it as a claim to verify, not as the answer. `state.md` is maintained by hand and can lag
the handoffs; where the two disagree, **the handoff files win** — they are append-only and
sequentially numbered, so they cannot be quietly revised.

```bash
RUN=runs/<run-id>
cat $RUN/state.md
ls $RUN/handoffs/ | tail -5
ls $RUN/gates/
```

## Step 2 — Walk the handoffs backwards

Handoffs are sequential and never renumbered; a correction is a new handoff, not an edit. Read
the **last** one first — its frontmatter tells you almost everything:

| Field | What it tells you |
|---|---|
| `from` / `to` | who last worked, and who was next |
| `status` | `complete` · `blocked` · `needs-review` · `partial` |
| `gate_impact` | whether the run is standing at a gate |
| `outputs` | what exists on disk now |
| `open_questions` | human-blocked items |
| `next_recommended` | the producing agent's suggestion — advice, not a routing decision |
| `risks` | what is still live |

Then read backwards only as far as you need. You are looking for the boundary between finished
and unfinished work, not the whole history.

Two readings that change what you do next:

- **`status: complete`** requires listed verification commands and their results (§2.3). A
  `complete` handoff with an empty *Verification performed* section is not complete; treat it
  as `partial` and re-verify before building on it.
- **`status: blocked`** must name its blocker — either an `open_questions` entry (human-blocked)
  or a `next_recommended` agent (dependency-blocked). Never both empty. If both are empty, the
  handoff is malformed and the blocker has to be re-derived from the body.

## Step 3 — Establish gate status

Gates are the only hard stop, so this determines whether the run can move at all.

```bash
for g in $RUN/gates/*.md; do echo "== $g"; grep -E '^(decision|approver|conditions)' "$g"; done
```

| What you find | What it means |
|---|---|
| No record for the gate the playbook expects here | **The run is halted awaiting a human.** Do not proceed. Use the `conducting-a-gate` skill. |
| `decision: approved` | Proceed to the next playbook step. |
| `decision: approved-with-conditions` | Proceed, but every condition is a tracked risk that must be terminal before the release gate. Verify each appears in `state.md`. |
| `decision: rejected` | The run routes back to the producing agent as a new inbound handoff. Check whether that handoff was ever issued — a rejected gate with no follow-up handoff is a stalled run. |

## Step 4 — Locate the next step in the playbook

Identify the case from the packet or `state.md`, open `process/playbooks/<case>.md`, and find
the current position in **Run at a glance**. The next step is the next line — subject to:

- **Conditional steps `(~)`** fire only on their stated condition. Check whether it holds
  before dispatching, and record the reason if you skip.
- **Loop-backs `↺`** may send you backwards. An open blocking finding outranks forward progress.
- **Explicit non-use.** A playbook that says an agent is "not used" for this case means it;
  that is a decision, not an omission.

Cross-check the artifacts the completed steps should have produced. A step marked done in
`state.md` whose canonical output is missing from the workspace is the discrepancy most worth
catching here — it means either the step did not really finish or the artifact went somewhere
non-canonical.

```bash
ls -R $RUN/01-requirements $RUN/02-design $RUN/03-bundle 2>/dev/null
ls -R $RUN/findings 2>/dev/null
```

## Step 5 — Reconstruct the receiving agent's inputs

The next agent gets a **fresh, cold context window**. Assemble exactly what the protocol says
it reads (§5): its inbound handoff, the files named in that handoff's `inputs`, and `state.md`.
Nothing else — not prior handoffs, not chat.

Write the inbound handoff with a **context summary of at most 30 lines** carrying everything the
receiver needs that is not in its `inputs` files. If you cannot fit it in 30 lines, the scope of
the step is probably wrong.

If the agent could not do its job from the workspace alone, **fix the handoff** rather than
supplementing it conversationally. A supplement delivered in chat is invisible to the next
person who resumes this run — which is the failure this whole procedure exists to prevent.

## Step 6 — Or: prove the run is closed

Before opening a new run, verify **all four** closure criteria (§6.1). One run at a time is a
hard rule; the Orchestrator refuses handoff `0001` otherwise.

- [ ] `gates/gate-3-release.md` shows `decision: approved` — **or** a cancellation record exists
      with `decision: cancelled` (§6.4)
- [ ] Every risk ID is terminal: resolved by a handoff that references it, or formally accepted
      with the gate approver's name. **Zero open risks survive a closed run.**
- [ ] Every gate condition is closed (they became tracked risks, so this folds into the above)
- [ ] Zero unanswered `open_questions` in the final `state.md`

Then confirm canonical promotion happened (§6.3): requirements, glossary, architecture, and
contracts were promoted to `docs/`. Without it, the next increment has no baseline to diff
against.

An increment run's first handoff must **cite** that closure evidence — the prior Gate 3 record
and the final `state.md`. A citation-free increment handoff is invalid and the receiving agent
refuses it, exactly as it would refuse work with no inbound handoff at all.

Two carry-forward rules that are easy to miss:

- **Accepted risks do not transfer.** If the increment touches the area of a previously accepted
  risk, raise a **new** risk ID referencing the old one (`supersedes: R-011 @ <run>`), to be
  re-accepted or resolved at this run's gate (§6.5).
- **Cancellation does not waive risk closure.** A cancelled run still needs every risk resolved
  or accepted by name before the record is signed.

---

## Common findings

| Symptom | What it actually means |
|---|---|
| Run "stuck" for a long time | Almost always awaiting a human at a gate. Working as designed. |
| `state.md` disagrees with the handoffs | Trust the handoffs; `state.md` lagged. Correct it. |
| `status: complete` with no verification | Not complete. Re-verify before building on it. |
| A risk ID appears in no later handoff | Still open. It blocks closure regardless of age. |
| Rejected gate with no follow-up handoff | Stalled run — the loop-back was never issued. |
| Artifact missing at its canonical path | The step did not finish, or wrote somewhere non-canonical. |
| Handoff `0001` is not from the Orchestrator | An early-convention artifact; note it, don't retrofit it. |

## Reference

- `process/agent-handoff-protocol.md` — §1 workspace layout, §2 handoff schema, §3 gates,
  §5 context budget, §6 closure and increments
- `process/playbooks/<case>.md` — the step order for this case
- `conducting-a-gate` skill — when the run is halted at a gate
- `routing-a-step` skill — dispatching the step this procedure identified, on a platform
  where the Orchestrator cannot invoke the next agent itself
- `runs/2026-06-comedor-vecinal/` — a real halted workspace to practise on
