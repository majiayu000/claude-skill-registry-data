---
name: "speckit-learn"
description: "Mine the current session for atomic instincts — one trigger, one action, evidence-backed — and record the ones the user approves under .specify/memory/instincts/. Use at the end of a session that produced a correction, a repeated mistake, or a convention nobody had written down, or when the user says 'remember how we did this'."
argument-hint: "Optional: a domain to focus on (testing, harness, git, spec-flow)."
compatibility: "Node 18+. Writes only under .specify/memory/instincts/, and only after explicit approval."
metadata:
  author: "speckit-demo"
  source: "adapted from ECC's continuous-learning-v2 (github.com/affaan-m/ECC)"
user-invocable: true
disable-model-invocation: false
model: sonnet
---

## User Input

```text
$ARGUMENTS
```

## What an instinct is

Atomic and small: **one trigger, one action**. Not a rule, not a spec, not a
skill — those are enforced; an instinct only suggests, carries a confidence
between 0 and 1, and fades if nothing reinforces it.

Good: *"when a `apps/server` test constructs a Nest provider → declare the
constructor parameter types explicitly, because vitest's transform emits no
`design:paramtypes` and DI resolves to `Object`."*
Bad: *"write good tests"* (not actionable), *"the repo uses vitest"* (already in
AGENTS.md), *"the user prefers concise answers"* (a preference, put it in memory
instead).

## Phase 1 — Mine this session

Look only at what actually happened in this conversation. Candidates come from:

- **A correction.** The user rejected an approach and named a different one.
  This is the strongest evidence there is.
- **A repeat.** The same mistake or lookup happened twice in one session.
- **A convention discovered the hard way.** A gate blocked, a tool behaved
  unexpectedly, a path only worked one way.

Do **not** mine: anything already written in CLAUDE.md, the constitution, or an
existing instinct (`node .claude/scripts/instincts.mjs list --all`); anything you
inferred but never saw; anything about a single file's contents.

## Phase 2 — Propose

Present at most 5 candidates as a numbered list, each one line:

```text
1. [testing, 0.6] when a test writes task data → point TASKR_DATA_DIR at a temp dir
   evidence: the suite wrote to the real store in this session and the user caught it
```

Confidence: 0.5 for a single clear observation, 0.6–0.7 when the user corrected
you explicitly, 0.8+ only for something observed repeatedly across sessions.
Say plainly that nothing is written until they pick.

## Phase 3 — Record what they picked

For each approved candidate:

```bash
node .claude/scripts/instincts.mjs add --id <slug> --domain <domain> \
  --trigger "<when>" --action "<do this>" --confidence <n> \
  --evidence "<date>: <what happened>"
```

Re-running `add` with an existing id merges: the evidence is appended and the
reinforcement count goes up. If the candidate restates an instinct that already
exists, use `reinforce` instead:

```bash
node .claude/scripts/instincts.mjs triggered --since <ref>   # which triggers this session actually hit
node .claude/scripts/instincts.mjs reinforce <id> --evidence "<date>: <what happened>"
```

Then show `node .claude/scripts/instincts.mjs list` and stop.

## Rules

- Never write an instinct the user did not approve, and never invent evidence.
- One instinct per behaviour. If a candidate needs "and", it is two.
- If a candidate is really a project rule (a gate should enforce it), say so and
  propose a constitution amendment or a hook instead — `/speckit-evolve` is the
  path for that. Instincts are the holding pen, not the destination.
- Nothing here is enforcement. An instinct that matters more than a suggestion
  belongs in a gate.
