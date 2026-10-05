---
name: tpp-orchestrate
description: Work through a queue of Technical Project Plans serially — delegate each to a TDD subagent, get a cross-model second opinion, empirically vet every finding, and make one coherent commit per plan. Use when executing a documented plan queue such as _todo/ or _feat-name/ for a port, migration, or multi-stage feature.
metadata:
  website: "https://photostructure.com/coding/claude-code-tpp/#tpp-orchestrate-drive-a-queue"
---

# TPP Orchestration

> Documented in depth: [Claude Code has amnesia. So do PRs, changelogs, and your future self.](https://photostructure.com/coding/claude-code-tpp/)

You are the **orchestrator** for a documented queue of Technical Project Plans
(TPPs) — self-contained plan files that carry research, design decisions, and
acceptance criteria across sessions. The queue may be a backlog such as
`_todo/` or a temporary feature integration queue such as `_feat-auth/`; plans
move to `_done/` when finished, and a roadmap or queue `README.md` defines the
order. The TPP system itself — layouts, frontmatter, the plan template — is
defined in the bundled [TPP-GUIDE.md](../tpp/TPP-GUIDE.md), or the project's own
`docs/TPP-GUIDE.md`, which wins. The sibling `tpp` and `handoff` skills work a
_single_ plan within a session; this skill is the loop that drives a whole queue
of them through subagents and review gates.

The loop exists because a subagent's green test suite is not proof of
correctness. [`../second-opinion/SKILL.md`](../second-opinion/SKILL.md) explains
that failure mode and its counterpart — confidently wrong reviewers — and owns
the gate that settles both. This skill owns the queue around it: delegate,
gate, record, commit, repeat.

## User direction

The review gates below are workflow defaults. If the user directs you to commit
the current work, follow that instruction without starting or resuming a review,
waiting for a reviewer verdict, or asking for approval again, unless the user
also requests review first. Use [stage](../stage/SKILL.md) to verify and commit
the understood scope. Record completed, skipped, and unfinished review work
accurately; do not mark unfinished implementation or acceptance criteria done.
An instruction about the current commit does not waive reviews for later TPPs.
When project instructions require review before every commit, a commit
instruction for changes that review has not finished on since they last
changed runs the review first, and only an explicit instruction to skip review
skips it.

## Before the first TPP

- Read the roadmap and every queued TPP's summary. Confirm dependency order.
- Identify the project's **ground truth** as the gate defines it, and write down
  the exact command to query it. Every TPP in the queue is vetted against it.
- Ask the user any clarifying questions **now** — scope ambiguities are cheapest
  to resolve before any code exists.

The run is finished when every queued TPP is in `_done/` with its commit and the
roadmap's status section matches.

## When to stop

Move from one step, and one TPP, to the next without checking in. Put status
notes in the same message as your next action. Stop the queue and ask the user
only when:

- a question would change what the TPP builds (steps 1 and 3);
- the review gate ends with a batch that the two reviewers did not both land,
  because its four passes are spent or you accepted a `DISCARD`;
- ground truth contradicts the TPP;
- the next action deletes data, force-pushes, or changes anything outside the
  repository.

## The loop, per TPP

Work **serially**: one TPP through the full loop before starting the next. Only parallelize TPPs within a wave when their file sets are provably disjoint _and_ neither depends on the other's decisions — review gates stay per-TPP either way.

### 1. Scope and clarify

Read the TPP and its sources of truth. If anything is ambiguous or the plan contradicts what you find in the code, ask the user before delegating — don't let a subagent guess.

### 2. Delegate with TDD

Launch an implementation subagent through the host's available collaboration
mechanism. Select the strongest available model and higher reasoning effort for
large, novel, security-sensitive, or weakly specified work. Use a faster model
or moderate reasoning effort only when the TPP, reference behavior, and existing
tests pin the implementation tightly. If the surface does not expose model
selection, keep the same risk-based scrutiny in the prompt and review gate.

The prompt must include:

- The TPP path and the sources of truth (spec files, reference implementation paths).
- **Tests first**: port or write the acceptance tests, run them and confirm they fail, then implement until they pass. Every test the change could affect must pass too, not just the new ones.
- Project pitfalls relevant to this TPP (from `AGENTS.md`, optional
  `CLAUDE.md`, or the TPP itself).
- "You cannot talk to the user. Record open questions, assumptions you made, and every intentional divergence from the plan in your final report."

### 3. Relay questions

Triage the subagent's open questions. Ask the user about decision-worthy ones
**before** the review gate — a review of code built on a wrong assumption is
wasted.

### 4. Run the review gate

Read and follow [../second-opinion/SKILL.md](../second-opinion/SKILL.md) on this
TPP's diff. The gate owns reviewer creation, adjudication, and pinning tests —
do not add reviewers here or restate its rules. Give it what its first step asks
for: the changed files and diff range, the proposed commit message, this TPP's
spec and reference paths, and the ground-truth command. Keep your own suspicions
out of it; the gate's reviewers read the code independently.

You are the gate's third reviewer, and the only one who knows the whole roadmap.
Read the new code yourself while the reviewers run.

### 5. Record the verdicts

Add a "Post-review fixes" section to the TPP listing every finding — accepted **and** vetoed — with the evidence for each verdict and which model raised it. Vetoes especially: the next session will see the same "bug" and must not re-litigate it.

### 6. Close out

Move the TPP to `_done/`, update the roadmap's status section, and make **one coherent commit per TPP** (implementation + tests + TPP move together), following the repo's commit conventions. Then start the next TPP.

## Guidelines

- **Run the review gate by default.** Passing tests do not replace review;
  explicit user direction can change or end the review workflow.
- **Rebuild before testing built artifacts.** CLI/dist tests against a stale build silently test old code.
- **Report honestly.** The per-TPP summary to the user starts with what needs
  the user — open questions and anything you diverged on — then lists what
  shipped and the findings accepted/vetoed (with one-line reasons).

## Adapting for your project

- **Name the ground truth explicitly** — e.g. "CPython 3.12 via `uv run python -c ...` in the reference submodule", "the staging API", "the RFC's test vectors". The vetting step is only as strong as this.
- **Reviewer choices and review focus** live in the gate — adapt [../second-opinion/SKILL.md](../second-opinion/SKILL.md), and this loop inherits it.
- **Tune the model heuristic** to your roster — the invariant is "risk decides the model", not the specific names.
- **Rename the file conventions** (`_todo/`, `_feat-<name>/`, `_done/`, and the roadmap or queue README) to whatever your plan system uses; the loop doesn't care about paths.
