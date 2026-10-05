---
name: routing-a-step
description: Use when a delivery run must advance one step on a platform where the Delivery Orchestrator cannot dispatch other agents itself — Cursor, Codex, Hermes, a Copilot or Roo build without agent-to-agent support, or any harness where you are the transport between agents. Turns "where the run stands" into the exact inbound handoff and the paste-ready invocation for the next agent. Also use to keep each step in its own clean context.
version: 0.1.0
---

# Routing a Step

## Overview

The framework assumes the Delivery Orchestrator (01) can invoke the other agents. Several
platforms cannot do that: Cursor has no multi-agent runtime, Codex and Hermes have no
agent-to-agent dispatch, and Copilot/Roo support depends on the build. On those platforms the
run does not become impossible — it becomes **manually transported**.

That works because the pipeline never depended on the harness for state. Run state lives on
disk (`runs/<run-id>/`), handoffs are append-only files, and every agent is required to work
from a cold context. The only thing the harness supplied was *carrying the payload from one
agent to the next*. This skill is you doing that carry, without losing anything the protocol
requires.

**Core principle: the file system is the bus.** Every fact that moves between agents moves as a
handoff file. Nothing important is allowed to exist only in a chat window — if it does, the run
stops being resumable and the whole audit chain is fiction.

## When to Use

- Advancing a governed run one step on a platform without agent-to-agent dispatch.
- Any run where you invoke each agent yourself and paste context between them.
- Whenever you want each agent step in a **fresh** context rather than a shared chat.

**Do NOT use for:**

- Claude Code — `/run-delivery <run-id>` already makes the main loop the Orchestrator and
  dispatches via `Task`. Use it instead; this skill would duplicate it by hand.
- `standalone` invocations. A bounded direct task needs no run workspace, no handoff, and no
  routing (`agent-invocation-contract.md` §4).
- Reconstructing an unfamiliar or long-dormant run — start with the `resuming-a-run` skill,
  then come back here to dispatch the step it identifies.

---

## Framework docs (precheck)

Every `process/…` and `templates/…` path in this skill resolves from the project root first,
then from `.agents-factory/` in the project, then from `~/.agents-factory/` (or
`$AGENTS_FACTORY_HOME`). Find `process/agent-handoff-protocol.md` in one of those before
anything else. If none has it, stop and tell the human to install the framework docs —
`scripts/install.sh --target docs` from an agents-factory checkout, or re-run their platform
install — and do not proceed from memory of what the documents say.

## Step 1 — Establish the position

You need four facts before choosing anything. All four come from disk.

```bash
RUN=runs/<run-id>
cat $RUN/state.md
ls $RUN/handoffs/ | tail -3
ls $RUN/gates/
```

| Fact | Source | Why it matters |
|---|---|---|
| Current phase / active task | `state.md` | Where the playbook cursor sits |
| Last handoff `status` and `next_recommended` | newest file in `handoffs/` | Whether the previous step actually finished |
| Gate status | `gates/` | A gate outranks everything below |
| Open risks and questions | `state.md`, last handoff | A blocking question means the next step is a human, not an agent |

Where `state.md` and the handoffs disagree, **the handoffs win** — they are append-only and
sequentially numbered. If you cannot answer all four from disk, stop and run `resuming-a-run`.

## Step 2 — Check for a gate before selecting an agent

If the playbook puts a human gate (`[H]`) at this position and `gates/` has no signed record,
**the run is halted.** Do not dispatch. Switch to the `conducting-a-gate` skill.

A `rejected` gate does not advance the run either — it routes back to the producing agent as a
new inbound handoff. An `approved-with-conditions` gate advances, but every condition must
already appear as a tracked risk in `state.md` before you continue.

## Step 3 — Select the next agent from the playbook

Open `process/playbooks/<case>.md` and find the current position in **Run at a glance**. The
next step is the next line, subject to three rules:

- **Blocking findings outrank forward progress.** An open blocking finding routes back (`↺`) to
  the owning implementer first.
- **Conditional steps (`~`)** fire only when their condition actually holds for this run. If you
  skip one, record the reason — a silent skip is indistinguishable from an oversight later.
- **`next_recommended` is advice.** The producing agent recommends; the playbook decides. Where
  they disagree, follow the playbook and note the divergence.

Confirm the step's upstream artifacts exist at their canonical paths. A step marked done in
`state.md` whose output is missing did not really finish.

## Step 4 — Write the inbound handoff

Write `runs/<run-id>/handoffs/NNNN-orchestrator-to-<agent>.md` **before** invoking anything.
Numbering is sequential and never reused. Use the protocol §2.1 frontmatter and §2.2 body.

This file is not paperwork — it is the entire input to the next agent. Everything the receiver
needs that is not inside its `inputs` files must be in the ≤30-line context summary. If it does
not fit in 30 lines, the step is scoped wrong.

```yaml
handoff: NNNN
run: <run-id>
from: delivery-orchestrator
to: <agent-name>
task: <one bounded outcome>
status: dispatched
gate_impact: <none | feeds gate N>
inputs:
  - <exact paths the agent should read — not "the design docs">
outputs: []
decisions: []
risks: []
open_questions: []
next_recommended: ''
```

## Step 5 — Invoke the agent, in a clean context

Open a **new chat / session** for the step. Not for hygiene — because the protocol's context
budget (§5) says the agent reads its inbound handoff, the files that handoff names, and
`state.md`, and nothing else. A reused chat silently feeds it the previous agent's reasoning,
which is exactly the leakage the handoff format exists to prevent.

Then invoke, per platform:

| Platform | How to invoke |
|---|---|
| Cursor | `@<agent-name>` (the rule), then paste the envelope below |
| Codex | "Use the `<agent-name>` skill." Match the posture with the sandbox flag stated in that skill |
| Hermes | "Load the `<agent-name>` skill." Or spawn it as a subagent, naming the skill in the subagent's prompt |
| Copilot | Invoke the `<agent-name>` agent |
| Roo / Zoo | Switch to the `<agent-name>` mode |
| Generic | Load that agent's definition as the system prompt |

The message you paste is only ever a pointer plus the mode. The content lives in the files:

```
mode: pipeline
run_id: <run-id>
inbound_handoff: runs/<run-id>/handoffs/NNNN-orchestrator-to-<agent>.md

Read your inbound handoff, the files it lists under `inputs`, and `state.md`.
Work only inside your ownership boundary. End with your closing handoff per
`process/agent-handoff-protocol.md` §2.
```

Do not paste the packet, the prior agent's output, or a chat summary. If the agent cannot work
from the workspace alone, the inbound handoff is deficient — **fix the file**, then re-invoke.
A supplement delivered in chat is invisible to whoever resumes this run next.

## Step 6 — Land the result

The agent returns its closing handoff content. You persist it — the platform will not.

1. Write it to `runs/<run-id>/handoffs/NNNN-<agent>-to-orchestrator.md` (next number).
2. Verify the artifacts it claims under `outputs` exist at their canonical paths.
3. A `status: complete` handoff with an empty *Verification performed* section is not complete.
   Treat it as `partial` and re-verify before building on it.
4. Update `state.md`: current phase, active task, open risks by id, open questions, gate status,
   last five handoffs. It points; it does not log. Keep it under ~100 lines.
5. Route findings per the playbook's loop-back table and protocol §4. A blocking finding becomes
   a new inbound handoff to the owning implementer. Anything untraceable to the packet or the
   approved design becomes an `open_questions` entry escalated to the human — never a guess.

Then return to Step 1 for the next step.

---

## What breaks when this is done sloppily

| Shortcut taken | What it costs |
|---|---|
| Invoking the agent without writing the inbound handoff first | The run has no record of what was asked; resuming reconstructs the wrong task |
| Pasting context into chat instead of into `inputs` | Invisible to the next session — the run stops being resumable |
| Reusing one chat for several agents | Boundary erosion: each agent inherits the last one's reasoning and scope |
| Not persisting the returned handoff | The step's decisions, risks, and open questions are lost entirely |
| Advancing past an unsigned gate | The one hard rule in the framework, broken |
| Renumbering or editing a handoff | Corrections are new handoffs; edits destroy the audit chain |

## Reference

- `process/agent-handoff-protocol.md` — §1 workspace layout, §2 handoff schema, §3 gates,
  §4 escalation, §5 context budget, §6 closure
- `process/agent-invocation-contract.md` — §3 pipeline mode, §4 standalone mode
- `process/playbooks/<case>.md` — the step order, conditional steps, and loop-backs
- `resuming-a-run` skill — when you do not yet know where the run stands
- `conducting-a-gate` skill — when the run is halted at a gate
- `PORTABILITY.md` — per-platform invocation and the orchestration caveat
