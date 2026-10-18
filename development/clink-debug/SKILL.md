---
name: clink-debug
description: The single home for delegating a bug hunt to clink agents — read it before sending any failure to clink-subagents or clink-brainstorm, not only a bug that already survived a pass. It routes a small bug to one cheap worker and escalates only what survives, defines the evidence that must travel with it, and enforces that no agent which produced a hypothesis may falsify or repair it. Use when a bug is about to be delegated, is still open after a worker looked at it, has two agents disagreeing about its cause, or came back after a fix landed.
---

# clink-debug

> **Requires the same PAL MCP setup as [`clink-subagents`](../clink-subagents/SKILL.md) and [`clink-brainstorm`](../clink-brainstorm/SKILL.md).** This skill adds no new call shape — it sequences those two and constrains who may sit in which phase. Read whichever of them you are about to use for its own rules; this file does not repeat them.

## Start cheap — most bugs end here

**One worker plus `debug-mantra` closes most bugs.** Delegate it through [`clink-subagents`](../clink-subagents/SKILL.md), give the worker `debug-mantra` and `karpathy-guidelines`, and send it the **failing command with its actual output** — never a description of them, because a worker handed a description diagnoses the description.

**Do not convene a panel for this.** Three senior agents tracing a one-file failure burns three lanes to answer what one worker can, and it is the most common way to waste an afternoon. It also gets the care backwards: if the discipline only rides along with a panel, it reaches only bugs big enough to justify one — and **the small bug is the one people guess at.**

Escalate past the cheap path only when one of these is true:

- a delegated pass returned and **the bug is still open**
- **two agents disagree about the cause**, or one produced a cause nobody reproduced
- a fix landed, and **the symptom came back**

What the cheap pass produced is the input the rest of this file needs anyway, so nothing is wasted by starting there.

## What this file owns, and what it deliberately does not

It owns exactly three things: **who may sit in which phase**, **what must pass between phases**, and **when to stop**.

It owns none of the debugging discipline itself. That is already written and is not restated here:

| For | Read |
|---|---|
| the reproduce → trace → falsify → fix discipline | `debug-mantra` |
| capturing a red-capable repro and a falsifiable prediction | `diagnosing-bugs` |
| root cause before fix, and the evidence registers | `t4-dev-workflow` |
| which model, which effort, which quota lane | the two clink skills — **this file contains no model or effort table, by design** |

## The phases, and who may sit in each

| Phase | Run it through | Seat rule |
|---|---|---|
| **Observe** — reproduce, minimise, trace | `clink-subagents`, workers in parallel over independent areas | any |
| **Promote** — admit a hypothesis | **you.** Never a subagent | — |
| **Falsify** — try to break the hypothesis | `clink-brainstorm` if it is contested or expensive to get wrong; one fresh worker otherwise | **fresh seats only** |
| **Decide** — did it survive | **you.** Panel agreement is not verification | — |
| **Repair** | `clink-subagents` with `tdd` | **fresh seat** |
| **Close** — re-run the repro, then the suite | **you** | — |

**Every seat in Observe and Falsify gets `debug-mantra`**, panel seats included. A panel asked to explain a failure without it returns confident causes nobody reproduced — and **the more seats agree on a wrong cause, the harder it is to reopen.** That is worse than no answer, because a plausible wrong cause ends the investigation.

**Promote, Decide and Close never leave you.** They are the three points where a wrong answer becomes the premise of everything after it.

## The provenance rule

**No agent session or model lineage that produced a hypothesis may occupy the falsify seat or the repair seat.**

A producer asked to attack its own hypothesis defends it — it has the reasoning that built the hypothesis in context, and that context is exactly what an outside check is supposed to lack. A producer asked to *implement* its own hypothesis is worse: the wrong theory gets written into the code by the one agent already convinced of it, and the diff then looks like evidence.

**The failure this prevents has a name: hypothesis laundering.** A worker's plausible explanation passes through a review that was never independent and comes back as panel-backed certainty. That is *worse* than one agent debugging alone, because the ceremony manufactures confidence that nothing in the process earned. Three agents failing to refute a claim is not evidence the claim is true.

Enforce it by seat, not by intention:

- **a new `continuation_id`** for every falsify and repair call — a fresh thread, not a follow-up
- **a different client where you can afford it** — `codex` produced it, so falsify on `cursor` or `antigravity`. Different lineage beats the same model twice
- the falsifier receives **the evidence and the testable prediction, never the producer's account of why it is right.** A persuasive causal narrative is the thing you are trying to test, so do not hand it over as the frame

## The handoff artifact

The same object moves between every phase. If it degrades into prose at any boundary, the next phase diagnoses the prose.

- the **failing command**, verbatim
- its **actual output**, not a summary of it
- the **`file:line`** the trace reached
- a **testable prediction** — what would be observed if the hypothesis were true, and what would be observed if it were false

**A hypothesis with no discriminating prediction is not ready to be promoted.** Send it back to Observe rather than to the falsifiers; there is nothing for them to test.

## Overriding `clink-brainstorm` — the one place these skills conflict

[`clink-brainstorm`](../clink-brainstorm/SKILL.md) runs its challenge loop and its forced adversarial round **by reusing each agent's own `continuation_id`**, so the probe reaches the seat that produced the position. **In its own file that is correct** — the round's subject is *"which approach do you favour"*, an opinion, and an agent revising its own opinion with full context is the point.

**Here it is wrong, and you must override it.** The subject is a claim about the world, not a preference. Run the falsify round with **fresh threads and, where possible, different clients**, and give them the evidence rather than the transcript.

The distinction generalises: **an opinion may be self-revised; a claim about the world needs an outside check.** That is `mechanisms over judgment` applied at the level of a seat.

## When to stop

- **Falsified** → back to Observe with what the falsifier found. This is progress, not a setback; you spent one round to avoid coding the wrong theory.
- **Survived** → Repair, fresh seat, `tdd`.
- **Neither** — it survived but nothing discriminating was tested → the prediction was too weak. Design a sharper experiment; do not run the same round again with more effort.
- **Two full cycles with no discriminating evidence** → stop delegating. The bug is telling you the instrumentation is missing, and no number of agents substitutes for a log line you have not added yet.

**Say which of these ended the hunt when you report it.** "Fixed" after a hunt that never falsified anything is a hypothesis wearing a verdict's clothes.
