---
name: conducting-a-gate
description: Use when a delivery run reaches a human gate and someone must assemble the evidence, make the decision, and write the gate record — Gate 1 scope, Gate 2 design, Gate 3 release, or a case-specific variant. Also use when a gate was rejected or approved-with-conditions and the run has to resume correctly. Gates are the framework's only hard stop, and an unsigned or sloppily signed gate is how unreviewed scope reaches production.
version: 0.1.0
---

# Conducting a Gate

## Overview

A gate is a **named checkpoint where the run halts until a recorded human decision exists in
`gates/`**. It is the framework's only hard stop. Everything else — handoffs, findings,
loop-backs — moves work between agents; a gate is where a person takes responsibility.

Two consequences follow, and both are routinely got wrong:

1. **A run waiting at a gate is not stuck.** It is the framework working. Do not "unblock" it
   by proceeding.
2. **The record is the decision.** A verbal approval, a chat message, or an agent's belief that
   the approver would agree is not a gate. If `gates/gate-N-*.md` does not exist and name a
   person, the gate has not happened.

The Orchestrator assembles evidence and halts. **A human decides.** No agent may sign a gate,
and no agent may proceed past one on its own authority.

## When to Use

- A run has reached a gate and the evidence needs assembling and presenting.
- You are the approver and need to know what you are actually signing.
- A gate came back `rejected` or `approved-with-conditions` and the run must resume correctly.
- A mid-run scope change has arrived and you need to know which gate it re-opens.

**Do NOT use for:** informal checkpoints that gate nothing downstream by a signature — the
`defect` case's reproduction sign-off, for example. Those are confirmations, not gates, and
they produce no record.

---

## Step 1 — Identify which gate, and which variant

The three standard gates are the `greenfield` set (`agent-handoff-protocol.md` §3.1):

| Gate | Fires after | Approves |
|---|---|---|
| **1 — Scope** | Requirements Analyst | Requirements doc, glossary, **every** open question answered |
| **2 — Design** | Architecture Guardian's clean review | Architecture, stack, integration inventory, cost-relevant choices |
| **3 — Release** | Release evidence assembled | The production release itself |

A case may use fewer gates, or a **variant** (§3.4). Check your playbook's `gates:` frontmatter
first — the variant changes the trigger, the ordering, or the decision vocabulary, never the
requirement for a recorded human decision:

- **Release — emergency/retroactive** (`incident`, active-exploit `dependency-upgrade`) —
  mitigation deploys first under documented emergency authority; the gate is signed
  *retroactively* against the logged action timeline. Add `emergency_authorized_by` and attach
  the timeline as evidence. **No rigor is waived** — regression, review, and the post-incident
  report still happen, only after restore.
- **Behavior-parity** (`refactor`) — one gate, two checkpoints: the characterization suite was
  captured all-green *before* any code moved, and is green and identical test-for-test
  *after*. `approved` requires both halves.
- **Data-operation (pre-execution)** (`data-operation`) — fires **before** execution. The
  approver signs the operation plan and the rollback plan together, with the dry-run diff
  attached. Post-execution verification is a closure condition, not a second gate.
- **Findings / decision** (`spike`) — accepts a decision/findings record. `decision: accepted`,
  no deployment, and no canonical promotion.
- **Release — baseline-approval** (`brownfield-onboard`) — approves a reconstructed baseline
  rather than a deployment; on approval the baseline is promoted to canonical `docs/`.

## Step 2 — Assemble the evidence

The approver should not have to go looking. Assemble, from the run workspace:

- **The artifacts under review**, by path — not summaries of them.
- **The clean review** that qualifies the gate, where one applies (Gate 2 needs the
  Architecture Guardian's review to be *clean*, not merely to exist).
- **Every open risk**, with ID and severity. Risks are never deleted; they are resolved or
  formally accepted, and acceptance requires the approver's name.
- **Every open question.** For Gate 1 this is the substance of the gate — an unanswered
  question is an unapproved requirement.
- **Verification output** where the gate rests on it: test results, dry-run diffs,
  characterization suites, release evidence.
- **Cost- and legal-relevant choices**, surfaced explicitly. Gate 2 is where hosting, provider,
  and retention decisions become expensive to reverse.

A gate presented as "everything looks good" is not assembled. Name the paths.

## Step 3 — Write the gate record

`runs/<run-id>/gates/gate-<n>-<slug>.md`, in the §3.2 format:

```markdown
# Gate 2 — Design
run: 2026-06-comedor-mvp
decision: approved            # approved | approved-with-conditions | rejected
approver: <name from packet §16>
evidence_reviewed:
  - runs/.../02-design/architecture.md
  - runs/.../findings/architecture/review-002.md   (clean)
conditions: []                # binding; the Orchestrator tracks each as a risk
notes: ...
```

- **`approver` is a person named in packet §16.** Not a role, not an agent, not "the team".
- **`evidence_reviewed` lists paths**, each annotated where its state matters (`(clean)`).
- **`conditions` are binding.** Each one becomes a tracked risk that must be closed before
  Gate 3. An aspiration written into `notes` is not a condition and will not be tracked.
- The `spike` variant uses `decision: accepted`.

## Step 4 — Resume correctly

| Decision | What happens next |
|---|---|
| `approved` | The run proceeds to the next playbook step. |
| `approved-with-conditions` | The run proceeds; **each condition becomes a tracked risk**, registered in `state.md` with an ID, and must be terminal before Gate 3. |
| `rejected` | The run routes **back to the producing agent**, with the rejection notes issued as a new inbound handoff — not as chat. Re-review after the fix; the original gate record stands as history and a new one records the second decision. |

A rejected gate is not an edit to the existing record. Records, like handoffs, accumulate.

## Step 5 — Handle a mid-run scope change

A scope change **re-opens Gate 1** (§3.3). The flow is fixed:

```text
packet amendment → Requirements Analyst delta review → Gate 1 re-approval
                 → Bundle Compiler delta → Bundle Intake Validator
```

Three rules that get broken under time pressure:

- **Never edit the frozen packet** under `00-packet/`. A scope change is an amendment file
  beside it.
- **Implementers never absorb scope changes directly from chat.** A change that reaches an
  implementer without passing Gate 1 is untraceable by construction.
- **A request too large for an amendment queues as the next increment run** (§6.6). "Too large"
  is a judgement the approver makes, not the implementer.

---

## What a gate is not

- **Not a status meeting.** It approves specific artifacts against specific criteria.
- **Not an agent's decision.** The Orchestrator halts and presents; it never signs, and it
  never overrides a reviewer's blocking finding without explicit human approval.
- **Not retroactive** — except the one variant that says so, in writing, with an authorizing
  name and a timeline.
- **Not skippable when the run is "obviously fine".** The obvious-fine runs are the ones where
  skipping becomes habit.

## Checklist

- [ ] Correct gate and correct variant for this case's `gates:` frontmatter
- [ ] Every artifact under review named by path
- [ ] Qualifying review is present **and clean**, where the gate requires one
- [ ] Every open question answered (Gate 1) or explicitly deferred with a named owner
- [ ] Every risk ID listed with severity; accepted risks carry the approver's name
- [ ] Verification output attached where the gate rests on it
- [ ] Cost- and legal-relevant choices surfaced, not buried
- [ ] Record written to `gates/gate-<n>-<slug>.md` in the §3.2 format
- [ ] `approver` is a person named in packet §16
- [ ] Conditions registered as tracked risks in `state.md`
- [ ] Rejection routed back as a **new inbound handoff**, not as chat

## Reference

- `process/agent-handoff-protocol.md` — §3.1 standard gates, §3.2 record format, §3.3
  semantics and scope change, §3.4 case variants, §6 closure
- `process/playbooks/<case>.md` — which gates this case uses and where
- `templates/stakeholder-input-packet.md` — §16 names the approver
- `resuming-a-run` skill — reconstructing where a halted run stands
