---
name: spec-convergence
description: >-
  Turn an ambiguous request into an agreed spec before implementation. When scope, exclusions, edge
  cases or acceptance behavior are undecided, ask fact-backed questions one concern at a time, name
  the test boundary and confirm the answers before writing. Not for define-goal.
metadata:
  revision: "6"
  areas: "software-development"
  targets: "runtime-agnostic"
  summary: "converge an unclear request into a confirmed spec: one root concern per round, a capped number of questions per round, every question backed by the fact that makes it real, explicit shared-understanding confirmation before writing"
  summary_zh: "把模糊需求收敛为已确认 spec：每轮一个根问题、每轮问题数有上限、每问附事实、写前显式确认共同理解"
  kind: "entry"
  produces: "spec"
---

# Spec Convergence

**Outcome:** a `spec` artifact at an announced path that the operator and the agent both agreed to:
decided boundaries, an observable acceptance list, and one named testing seam.

**Done:** every decision the work depends on was asked and answered by the operator, each answer is
recorded in the operator's own words, and the spec's Open questions section is empty.

**Safe failure:** an unanswered decision stays open. Say what is still open and who must decide it
instead of filling the gap with a plausible default.

## When to Use / Not For

Use when any of these is still undecided:

- What the request includes and, more often, what it excludes.
- What observable result counts as accepted, and at which public boundary it is observed.
- Whether the work should happen at all in the form requested.

Run this **before** `define-goal` when a request is both ambitious and boundaryless: ambition can be
restated cheaply, but a spec written on unstated boundaries is a plan for the wrong thing. `define-goal`
then sets the outcome and the appetite; it does not decide boundaries.

Not for work whose contract is already written: read the existing goal file or spec and stop. This
skill does not re-litigate decided questions, plan the implementation, or survey the codebase —
repository reading here only supplies facts that make a decision concrete.

## Order of Operations

### 1. Facts before questions

Read the repository before asking anything: the contract documents, the code the request touches, its
tests, and the configuration that governs it. Mark every fact with the `path` that holds it and quote
the line or symbol when the exact form matters.

Two things that look like answers are not answers, and each must be said explicitly in the question:

- **Current behaviour is not a decided boundary.** The repository shows what happens today; whether it
  should keep happening is a choice. An existing behaviour, a legacy default, a shipping limitation or
  a migration's current stopping point is a fact about the present, never the operator's decision about
  the future.
- **Absence is a fact.** When nothing in the repository addresses the point, name what you searched and
  what you found missing ("no test covers this shape; no config key exists"). A greenfield decision is
  legitimate as long as the search is visible instead of implied.

Never ask what the repository already answers. A question is only valid when its answer is a choice,
not a lookup.

### 2. Build the decision tree

Every undecided choice is a node; a node's prerequisites are the answers it depends on, so an edge means
"this answer changes what can be decided next". Keep one root per independent concern rather than
flattening the tree into a list: a question whose prerequisite is still open is not answerable yet, and
asking it produces a guessed answer that later answers invalidate.

Before the first round, list the roots you identified — one line each — and why the remaining concerns
are not roots. The operator can then reject the frame, not only the answers inside it.

### 3. Ask one root at a time, capped

A round is **one root concern's** frontier: every node under that root whose prerequisites are settled.
Sending the whole tree as one message turns the protocol into a form to rubber-stamp, so:

- **Cap:** `SPEC_ROUND_CAP` questions per round (default 5). If the root has more, send the ones that
  most block Scope or the Testing seam and state how many remain in this root.
- **Order inside a round:** questions that can change scope first, wording and naming last.
- Number them `Q1..Qn`. Each carries:
  - **Facts:** what the repository showed, with `path` and the symbol or line — or the visible absence.
  - **Options:** the genuinely available answers. Show what you excluded and the fact that excludes it,
    in one line each, so the exclusion itself can be challenged.
  - **Recommended:** one answer, the reason it wins, and the trade-off losing it costs.

**The testing seam is a question, not a closing note.** Ask at which public boundary acceptance will be
judged (command, endpoint, exported symbol, file format, user flow) as part of a round, with candidate
boundaries and the fact that makes each observable. A seam agreed inside the write-up was never agreed.

Ask the operator to answer by number and to correct any fact that is wrong. A recommendation is a
question with a suggested answer, not a decision.

### 4. Recompute the frontier after each answer

Record the answer against its node, drop the children's prerequisite, and rebuild the next round from the
settled set. A recommended answer nobody accepted is still open: never carry a default forward and never
let a later question assume it.

An empty frontier means step 5. A round that unlocks nothing and reveals no new fact is a stop
condition: name the missing decision or the missing evidence instead of asking the same level again.

### 5. Empty frontier means confirm

Present a short shared-understanding summary: the decisions in order, the non-goals, and the seam. Quote
the operator's own words for each decision — a paraphrase is a second decision nobody made. Ask for
non-goals instead of drafting them ("anything that should be explicitly out?").

Wait for an explicit affirmative in the operator's own language. Silence, a partial answer, or an
unaddressed recommendation is not confirmation, and the spec is not written before it.

### 6. Write the `spec` artifact

Announce the path before writing it. Resolution order and the config-file path are defined in
[references/configuration.md](references/configuration.md);
this skill does not restate them. The documented default:

```bash
mkdir -p "${SPEC_DIR:-docs/specs}"
# file name pattern: ${SPEC_FILE_PATTERN:-YYYY-MM-DD-<feature>.md}
```

Use these headings only. Do not add a design section, a task list or an implementation sketch.

- **Problem** — the request as now understood, one short paragraph.
- **Scope** — what the work changes, named at the level the decisions settled.
- **Out of scope** — the non-goals the operator confirmed.
- **Acceptance** — `AC-01`, `AC-02`, … each observable and checkable by someone who did not write the
  change. The ids are anchors for people and for review; they are not a machine contract.
- **Testing seam** — the public boundary confirmed in step 3.
- **Open questions** — must be empty. If one remains, the frontier was not empty; return to step 3.

### 7. Hand off

- Whatever plans or implements the work next consumes this spec. A plan may not re-decide what the
  spec settled; if it has to, the spec is incomplete — come back here rather than widening the plan.
- Implementation review reads the spec, when the plan names one, as an extra compliance standard.
- A goal file when the work is an outcome delivered end to end over a longer window.

## Rules

- One round per root concern, capped by `SPEC_ROUND_CAP`; a round that unlocks nothing is a stop
  condition, not a reason to ask again.
- Never decide on the operator's behalf. A decision made silently is a defect even when the guess turns
  out right.
- Current behaviour, legacy defaults and absence are facts to state — never answers to assume.
- Non-goals are asked, not drafted. An empty "Out of scope" is usually an unfinished answer, not a small
  one.
- The spec is the artifact: no plan, no implementation, no repository tour.
