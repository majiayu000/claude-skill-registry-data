---
name: mk:grill
preamble-tier: 3
version: 1.0.0
description: |
  Relentlessly interview the user about THEIR plan or design — one question at
  a time — resolving each branch of a decision tree until shared understanding.
  Claude is the interviewer; the user is the interviewee. Triggers on "grill me",
  "stress-test this plan", "get grilled on my design", "interrogate my plan".
  Checkpoints every answer to docs/knowledge/<slug>.md so progress survives a
  context-window reset. Flags knowledge the user cannot answer as a gap to chase.
  Do NOT use to PROPOSE solutions or compare approaches (→ mk:brainstorming).
  Do NOT use to validate "is this worth building?" (→ mk:office-hours).
  Do NOT use when Claude should ANSWER questions about the repo (→ mk:ask-me).
  Do NOT use for a one-shot review of an existing plan (→ mk:plan-ceo-review).
  Do NOT use to apply named reasoning lenses to findings (→ mk:elicit).
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
source: local
keywords:
  - grill
  - interview
  - stress-test
  - decision-tree
  - knowledge-extraction
  - one-question-loop
  - plan-interrogation
  - tacit-knowledge
  - shared-understanding
when_to_use: Use when the user wants to be relentlessly interviewed about their own plan or design, one question at a time, until every decision-tree branch is resolved. NOT for proposing solutions (see mk:brainstorming), product validation (see mk:office-hours), Claude answering repo questions (see mk:ask-me), or one-shot plan review (see mk:plan-ceo-review).
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# Grill

You are the **interviewer**. The user owns a plan or design; your job is to
relentlessly extract and resolve every unresolved branch in it — one question at
a time — until you both share the same understanding. You never propose the
solution; you interrogate the user's.

**Differentiator:** brainstorming = Claude proposes options; grill = Claude
interrogates the user's existing plan. office-hours = "should we build this?";
grill = "is this plan fully resolved?".

## When to Use

- User says "grill me", "stress-test this plan", "get grilled on my design", or
  "interrogate my plan / design".
- A plan or design exists (as a doc OR as a verbal idea) and the user wants every
  assumption, ambiguity, and unresolved choice surfaced and answered.
- Before handing a half-formed idea to `mk:skill-creator` or `mk:plan-creator` —
  grill front-loads the tacit context so the build starts ~90% resolved, not 70%.

## When NOT to Use

| Situation                                              | Use instead           |
| ------------------------------------------------------ | --------------------- |
| Propose / compare technical approaches                 | `mk:brainstorming`    |
| "Is this worth building?" — product validation         | `mk:office-hours`     |
| Claude should ANSWER questions about the repo          | `mk:ask-me`           |
| One-shot review of an existing plan                    | `mk:plan-ceo-review`  |
| Apply named reasoning lenses to existing findings      | `mk:elicit`           |
| Constitution derived from the CODEBASE (not the human) | `mk:project-context`  |

## Plan-First Gate

Grill produces a knowledge doc — it is a pre-planning elicitation step, the same
class as `mk:office-hours` and `mk:brainstorming`. Always skips Gate 1. It writes
ONLY `docs/knowledge/<slug>.md`; it never writes code or implementation files.

## Entry — resolve the input

Accept either entry mode:

1. **Doc path** (a plan / design / spec file): `Read` it. Seed the decision tree
   from its open branches — unresolved choices, stated-but-unjustified decisions,
   TODOs, "TBD"s, vague nouns, and any assumption presented as fact.
   **Read-only:** never edit the source doc (see Read-Only Constraint).
2. **Verbal idea / topic:** seed an empty tree and build it through questioning.

Then:

- Compute `<slug>` — a short kebab-case name for the plan/design (e.g.
  `payment-retry-flow`). For path routing of the output file, follow
  `mk:project-organization` (advisory mode): the canonical location is
  `docs/knowledge/<slug>.md`.
- Create `docs/knowledge/<slug>.md` from the Output Doc Template below (via
  `Write`). If it already exists, `Read` it and resume — append to the existing
  Q&A Log and tree rather than overwriting.

## Core Loop (the signature mechanic)

Run this loop. **Exactly ONE question per turn — never batch.** This is prose
interrogation, deliberately NOT `AskUserQuestion` multi-question batching. One
sharp question, wait, absorb, checkpoint, repeat.

1. **Pick** the single highest-leverage unresolved branch — the one whose answer
   unblocks or reframes the most downstream decisions.
2. **Ask** exactly one question about it. Be specific and concrete; quote the
   user's own words / the doc when challenging an assumption. No preamble, no
   multi-part questions, no menus.
3. **Wait** for the user's answer.
4. **Absorb** — restate the answer in one line to confirm you understood it.
5. **Checkpoint immediately** (see Checkpoint Protocol) — write before asking the
   next question, so a context reset never loses the answer.
6. **Re-evaluate the tree** — the answer may close branches, open new ones, or
   expose a contradiction with an earlier answer. Surface contradictions
   immediately ("earlier you said X; this implies not-X — which holds?").
7. **Repeat** from step 1 until Termination conditions are met. Five questions or
   an hour are both valid lengths — depth, not count, is the target.

### Question quality

Good grill questions:
- Target the binding constraint, the unstated assumption, or the fork the user
  has not actually decided ("you wrote 'cache it' — invalidated how, and when?").
- Force a concrete answer: inputs→outputs, an edge case, a number, a who/when.
- Probe the seam between two decisions that may conflict.

Bad grill questions (avoid):
- Proposing the answer ("should we use Redis or Memcached?" — that's brainstorming).
- Asking for something already stated in the doc or a prior answer.
- Vague ("any other thoughts?") or compound ("what about auth, and also caching?").

## Checkpoint Protocol

After EVERY answer, `Write`/`Edit` `docs/knowledge/<slug>.md`:

- **Append** the verbatim Q&A pair to the Q&A Log.
- **Update Decisions** — move any newly-resolved branch here with its chosen
  answer + one-line rationale.
- **Update Highlights** — capture any sharp insight worth re-reading.
- **Update Open Branches** — add branches opened by this answer, remove resolved
  ones.
- **Update Open Gaps** — if this answer was a can't-answer / thin answer, record
  it (see Gap Flagging).

The checkpoint-after-every-answer is the core safeguard: the doc is a valid,
useful artifact at any point, even if the session is cut off mid-grill.

## Gap Flagging

When the user cannot answer, answers thinly, or says "I don't own that" — do NOT
paper over it. Record it under **Open Gaps** with:

- The unresolved question.
- Why it's unresolved (not owned / not yet decided / needs data).
- **Who to ask** — the person or source that can close it.

Tell the user plainly: "You don't own this one — go ask whoever runs it, then
drop the detail back into the knowledge doc." A flagged gap is a valid outcome,
not a failure.

## Termination (hybrid — never silent, never infinite)

At each checkpoint, surface a readiness signal: list the remaining Open Branches
and your judgment of whether high-leverage questions are exhausted.

When the branches look drained (only low-leverage or gap-blocked items remain),
**propose wrap-up** — summarize what's resolved and what remains, then ask the
user to confirm "done" or "keep going". Never auto-terminate silently; never loop
forever. The user always holds the stop button.

On confirmed wrap-up, present the three handoffs:

1. **`mk:skill-creator`** — if the resolved design is a skill to build. Context is
   front-loaded, so the build starts ~90% resolved.
2. **`mk:plan-creator`** (or **`mk:brainstorming`** if approaches are still open) —
   if it's a feature/system to plan or still needs solution exploration.
3. **`mk:project-context`** — to merge the extracted human knowledge into the
   project constitution.

Offer all three; let the user pick. Grill itself does NOT auto-invoke the
downstream skill or generate its output — it only hands off.

## Read-Only Constraint

When grilling an existing plan/design doc, grill **never mutates that source
file**. `docs/knowledge/<slug>.md` is the only output. Corrections, decisions,
and new detail flow through the chosen handoff (e.g. `mk:plan-creator` updates the
plan) — not through grill editing the original.

## Output Doc Template

`docs/knowledge/<slug>.md`:

```markdown
# Knowledge: <Plan/Design Title>

**Source:** <doc path | "verbal idea">
**Started:** <date>  ·  **Status:** in-progress | wrapped

## Decisions
<!-- resolved branches: chosen answer + one-line rationale -->
- **<branch>:** <answer> — <why>

## Q&A Log
<!-- verbatim transcript; the checkpoint. Append after every answer. -->
1. **Q:** <question>
   **A:** <answer>

## Highlights
<!-- sharp insights worth re-reading -->
- <insight>

## Open Branches
<!-- unresolved choices/assumptions still to grill -->
- <branch>

## Open Gaps
<!-- can't-answer items + who to ask -->
- **<question>** — <why unresolved> → ask: <who/source>
```

## Gotchas

- **Batching questions** — the whole point is ONE question per turn. If you feel
  the urge to ask two, you have two turns, not one. Never reach for
  `AskUserQuestion` (it isn't in `allowed-tools` for exactly this reason).
- **Proposing instead of interrogating** — the moment you suggest the answer,
  you've drifted into `mk:brainstorming`. Ask about the user's choice; don't make it.
- **Skipping the checkpoint** — "I'll write it all at the end" loses everything on
  a context reset. Write after every single answer; that's the survival mechanic.
- **Papering over a gap** — a confident-sounding guess on something the user
  doesn't own is worse than a flagged Open Gap. Flag it and name who to ask.
- **Grilling forever** — without the hybrid wrap-up you fatigue the user. Surface
  the readiness signal each checkpoint and propose wrap-up when branches drain.
- **Editing the source doc** — grill is read-only on the plan/design; the only
  file it writes is `docs/knowledge/<slug>.md`.
