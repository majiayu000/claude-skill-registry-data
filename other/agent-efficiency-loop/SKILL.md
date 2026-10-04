---
name: agent-efficiency-loop
type: Skill
title: "agent-efficiency-loop — take over a running agent and make it efficient, correct, self-improving"
description: "The watch-fix-rerun method for making an existing platform agent or automated process efficient and correct: baseline its ledger, run one unit yourself, fix the class behind every wasted call, rerun, record. Use when asked to improve, optimize, watch, or 'make efficient' an agent, a sandbox session, a sync job, or any recurring automated process."
tags: [agents, efficiency, operations, doctrine, self-improvement]
timestamp: 2026-09-12T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/agent-efficiency-loop/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# agent-efficiency-loop — take over a running agent and make it efficient, correct, self-improving

**What this reproduces.** The AI Model Config Sync agent, 2026-09-11/12: first run broke on a
missing model registration, cost $2.40 and re-fetched results it had already read. Eleven runs
later a provider sync costs $0.70, has zero tool errors, resolves cases the agent had never seen
(dropped models, naming gaps across vendors), and the loop shipped nine platform fixes that every
other agent inherits. Worked example and seed lessons:
[`systems/intelligence/agent-iteration/projects/agent-efficiency-loop/LESSONS.md`](/systems/intelligence/agent-iteration/projects/agent-efficiency-loop/LESSONS.md).

**The one-sentence version:** you are the operator AND the builder — run the thing yourself, read
the ledger not the agent's story, fix the class behind every wasted call in the layer that owns it,
rerun on a different unit, and write down what you learned where the next agent will find it.

Companions — read the one your step reaches:
- [launch-prompt.md](launch-prompt.md) — the prompt the owner pastes to start a loop (fill the blanks).
- [ledger-queries.md](ledger-queries.md) — the SQL for baseline, per-run cost, waste census, run polling.
- [`systems/intelligence/agent-iteration/projects/agent-efficiency-loop/LESSONS.md`](/systems/intelligence/agent-iteration/projects/agent-efficiency-loop/LESSONS.md) — the
  shared lessons register: read at the start of every loop, append at the end of every round.

## 0. Standing rules (the owner's, verbatim in spirit)

- **You run it. Nobody else.** Trigger every run yourself (`agent_run`, the endpoint, the script).
  Never ask the owner to rerun, release, hand you a token, or "try it and tell me". If a run needs
  a secret or a permission you lack, say plainly that a permission rule is the only unblock, then
  keep working on everything else.
- **Automation stays OFF until you can guarantee it.** A schedule turns on only after enough
  clean runs that you would put your name on it; the report that recommends it names the runs.
- **One unit per run.** One provider, one sandbox task, one document, one customer. Every run
  is a fresh sample; never batch until the single unit is boringly clean.
- **Fix the class** (law 3): a wasted call's owner is the tool, the prompt, the model, or a missing primitive.
- **Run counts are yours only.** Other sessions run the same agent for their own reasons
  (repairs, quarantines). Count only runs you launched; identify them by launch time and message.
- **Talk like a person.** Every status to the owner is plain English with a small table of
  numbers, ends with a pending list, and never points him at a file or a code name.

## 1. The round — what one iteration is

Every round is the same seven steps. A round that skips a step is not a round.

**A round is planned only when it has a round card**, written before the first run — it is the
first thing in your plan and the first line of your status:

```
Round <n> — expose on: <unit A>   →   fixes: <levers>   →   prove on: <unit B, a different unit>
```

No unit B named = no round. The launch prompt, the status, and the completion criterion all
carry both units.

**The first six actions of every efficiency plan are fixed** — write them in this order, with
the lane for anything you dispatch; a plan whose first actions differ is answering a different
question:

1. Round card: unit A and unit B named (§1 above).
2. Baseline table from the ledger (`ledger-queries.md` §1), shown to the owner before any change.
3. Model check + end-of-run report clause on the agent (§2, Model and Prompt rows).
4. Run unit A yourself; poll its ledger rows to the real end (`ledger-queries.md` §5).
5. Waste census of unit A's calls (§2) → fixes in the owning layer, each with a guard, pushed.
6. **Run unit B yourself** — the different unit from the card — and add its row to the table.
   This is a separate action from 4, never folded into it.

1. **Baseline.** Pull the last N runs from the ledger (`ledger-queries.md` §1): cost, turns,
   tool calls, errors, cache-hit ratio, wall time, stuck rows, outcome. Write the table down before
   touching anything — it is the only thing that makes "better" a fact.
2. **Run unit A yourself, with unit B already on the card.** Same lane the product uses. Start a poll that watches the run's
   own ledger rows (running tool calls, message count stable) — the launcher's timeout is not
   the run's end.
3. **Read both stories.** (a) The agent's final message — it is a *lead*. (b) The ledger: every
   tool call's arguments, output size, error text, and every request's tokens. The agent's report
   said "no public prices" while the ledger showed it read a 200-byte HTML stub; the ledger wins.
4. **Census the waste.** Every call that was unfiltered, repeated, retried, oversized,
   misleading, or replaced reasoning the platform could have done goes in a list with its lever
   (§2). Include what the agent did *right* that the prompt does not yet say — that is a rule to
   write down before it is forgotten.
5. **Fix the class.** For each lever, the smallest change in the owning layer, pushed to main
   with its guard. Prompt edits ship as ONE update at the end of the round (cache). Provider-,
   customer-, or task-specific lore goes on the subject's own data row, never in the prompt.
6. **Rerun on unit B — the one step every plan skips** (0 of 6 proof reps did it until the round
   card existed). Unit B is a different provider, a different sandbox task, a different document. A fix proven on the unit that
   exposed it proves nothing, and "N consecutive clean runs" is the automation gate (§5), not a
   substitute for this step. Same metrics; the table grows one row.
7. **Record.** Append the round's lessons to `LESSONS.md` (§4 format). A lesson that generalizes
   beyond your subject becomes a candidate rule here, through `skill-authoring`.

Completion criterion for a round — all four, checkable:
- the metrics table has a new row for a unit **different from** the one that exposed the fixes;
- every waste item has a shipped fix (commit or agent version) or a filed defect with an owner;
- LESSONS.md has the round;
- the status to the owner names the next unit.

## 2. The four levers — where a wasted call actually lives

| Lever | You are looking at it when… | The move |
|---|---|---|
| **Model** | The agent hedges, retries reasoning, or fails a case a stronger model handles first try; or the agent is on a model that is no longer the best for its class | Move it to the best current model for the job (the owner moved the sync agent Sonnet→Opus and the failure class vanished). Check `agent.ai_model` against the catalog primary at the start of every loop. |
| **Prompt** | Right tool, wrong shape: unfiltered reads, one-row writes in a loop, guessed column names, a docs URL that returns nothing, lore from a previous run re-discovered | Write the rule in the prompt (recipe + example call, not advice). Add the **worker-into-builder clause**: at the end of every run the agent reports what was efficient, what was not, which tools worked, which did not. Subject-specific lore → the subject's data row. |
| **Tool** | The tool refused a shape the agent reasonably sent (a list where it wanted one id), returned a misleading error ("access level" for a missing registration), lost its result from context, sorted NULLs first, or made the agent do two calls for one fact | Fix the tool and add the test. A prompt rule that works around a tool bug is a defect with a longer life. |
| **Platform primitive** | The agent reasons over raw data every run (diffs two lists, classifies rows, re-derives a policy) | Precompute it: a view, a snapshot job, a policy column, a reverse diff. The agent's first read should already be the answer. |

Heuristics that found real waste every time:
- **Output size per call** — a read over 8k chars that the agent uses two fields of.
- **Same `data`, N calls** — a batch primitive is missing or unknown to the agent.
- **Retries of the same call** — the error text is misleading; fix the classification.
- **`status='pending'` after the run** — a completion write was lost; that is a platform bug.
- **Cache-hit ratio dropping mid-run** — a prompt/instruction edit landed mid-conversation; move
  it to the last call.
- **Cost of an equivalent run in a different session** — a ×5 jump is a join or a loop, never
  "the model got expensive". Verify with per-request rows before believing a sum.

## 3. Measuring — numbers, not adjectives

Per run: cost, turns, tool calls, tool errors, running/pending rows at the end, output chars per
call, cached vs uncached input tokens, wall time, the outcome in one line. Per loop: the table of
all your runs, newest last. Report deltas *and* levels. A run that costs less but did less is not
an improvement; write the outcome column first.

Health of a run you can call clean: zero tool errors, zero stuck rows, no unfiltered reads, no
repeated writes, the agent's report agrees with the ledger, and the outcome is verified on the
live surface (the row exists, the price is right, the model answers).

## 4. Where lessons go (so we learn from each other)

Three homes, chosen by who needs the lesson:

| Lesson is about… | Home | Format |
|---|---|---|
| One subject (this provider, this sandbox image, this customer) | The subject's own data row (`sync_policy.notes`, the sandbox profile, the org setting) | Dated bullet; the agent reads it before working that subject |
| This loop's method for its agent | The agent's prompt, ONE edit per round, last call | Rule + example call |
| Any efficiency loop on any agent | [`LESSONS.md`](/systems/intelligence/agent-iteration/projects/agent-efficiency-loop/LESSONS.md) | One row: date · loop · lever · symptom · fix (with commit or version) · metric before → after |
| Every agent on the platform | This skill, via `skill-authoring` (RED/GREEN proof) | A rule in §1–§3 |

Read `LESSONS.md` top to bottom before your first round. Append after every round — never rewrite
another loop's rows.

## 5. The guarantee report — when to recommend turning automation on

Recommend a schedule only when you can write this table honestly:

| Question | Evidence required |
|---|---|
| How many consecutive clean runs, by your definition in §3? | List them with ids and cost |
| What does a run cost and what does a day of automation cost? | Numbers, and whether the automated part spends AI money at all |
| What can the automation break, and how would we know? | The failure surface and where it screams |
| What is still manual and why? | The residue list |

Recommend the cheapest automation first (a snapshot job that spends nothing before an LLM sweep
that spends dollars). The owner decides cadence; you decide readiness.

## Rationalizations (observed 2026-09-11/12)

| Excuse (verbatim) | Reality |
|---|---|
| "It's just deployment timing, the fix isn't live yet" | The model class was never registered; the error text was misleading. Check the code path before blaming the train. |
| "The agent says the provider has no public prices" | It read an HTML stub. The ledger showed 200 bytes. Read the output, not the summary. |
| "The run finished — the launcher returned" | The launcher timed out; the run continued server-side for six minutes. Poll the ledger. |
| "I'll ask Arman for the token / to rerun it / to release" | Every one of those is the operator's job. A missing permission is stated once, then you keep going. |
| "This run cost $15 — the model got expensive" | A join multiplied the sum. Per-request rows said $0.75. |
| "Let me add a prompt rule to avoid the tool error" | The tool refused a list match. The tool got fixed; the prompt rule would have outlived the bug. |

## Red flags

- You are about to explain a number instead of pasting the table that produced it.
- You are about to write a provider's quirks into the prompt.
- You are reading the agent's summary and have not opened its tool calls.
- Your fix is "tell the agent not to do that" and the tool still accepts the bad shape.
- You are counting runs another session launched.
- You are about to schedule it and cannot name the clean runs.
- Your plan says "rerun" without naming a different unit than the one that broke.
