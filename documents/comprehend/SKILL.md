---
name: comprehend
category: knowledge
description: |
  Agent→human teach-to-mastery loop. Turns the agent into a wise,
  effective teacher whose single objective is that YOU deeply understand
  a body of work — the problem and why it existed, the solution and why
  it was resolved that way (design decisions, edge cases), and the
  broader context (why it matters, what it impacts). Stage-gated (confirm
  mastery before advancing), active-recall driven (you restate first; the
  agent fills gaps; quizzes via AskUserQuestion), and goal-bounded (the
  session does not end until your understanding is verified).
  Default subject = the current session/diff; pass a PR number, file, or
  subsystem to teach that instead.
  The pedagogical INVERSE of grill-me: grill-me stress-tests YOUR forward
  plan; comprehend transfers mastery of EXISTING work to you. Distinct
  from handoff (agent→agent narrative) and Bridge/Bookkeeping (agent→KG).
  Use when: (1) you want to deeply understand what was just built,
  (2) onboarding yourself or a teammate onto a PR / file / subsystem,
  (3) post-mortem learning after a complex session, (4) you say "teach
  me this", "help me understand", "walk me through", "make sure I get
  this", "I want to actually understand X".
  Triggers on "comprehend", "/comprehend", "teach me", "help me
  understand", "walk me through", "make me understand", "explain this so
  I get it", "make sure I understand", "onboard me", "I want to learn
  how this works".
---

# comprehend — teach-to-mastery loop

**Make the human deeply understand the work — verified, not assumed.**

Distilled from Thariq Shihipar's teaching prompt
(`research/entities/tool/thariq-teach-to-mastery-prompt.md`). This is a
**composition skill**: it fires native primitives (`AskUserQuestion`,
`/goal` P19, a persisted checklist doc P6) and adds only pedagogical
sequencing on top — no infrastructure reimplemented.

**Interactive-only.** comprehend depends on a live human to restate,
answer quizzes, and signal mastery. In an autonomous, background, or
piped run with no human responder, it must **abort** — never self-mark
checklist boxes or self-certify understanding. The verification signal
is the human's answer; without a human there is no signal.

## The one objective

Understanding is the success metric. A summary the human nodded along to
is a failure. The skill is complete only when the human has *demonstrated*
mastery of every item on the checklist — where "demonstrated" means a
correct, explained answer to a quiz, **not** the agent's own assessment
that it taught well.

## Subject resolution

| Invocation | Subject taught |
|---|---|
| `/comprehend` (bare) | The **current session / diff** — what we just did (recent `git diff`, the changes from this session). |
| `/comprehend PR <n>` | The diff + discussion of pull request `n`. |
| `/comprehend <path>` | A file or directory — its role, contracts, edge cases. |
| `/comprehend <topic>` | A subsystem / concept already present in the repo or KG. |

If a bare invocation has no obvious recent work to teach, ask **once**
what to teach, then proceed — do not guess into a vacuum.

## Procedure

### 1. Build the checklist (and persist it)

Create a running markdown checklist at
`docs/comprehend/YYYY-MM-DD-<subject-slug>.md` of everything the human
must understand, organized along three axes — teach **why**, then drill
into more whys, and cover **what** and **how**:

1. **The problem** — what it is, *why* it existed, the branches/alternatives that were on the table.
2. **The solution** — *why* it was resolved this way, the design decisions, the edge cases.
3. **The broader context** — *why this matters*, what the changes will impact downstream.

Each item is a checkbox. The doc is the shared artifact — update it live
as items are mastered (`- [x]`), so the human can see progress and resume
later. Persisting it (P6) is what separates this from an ephemeral chat.

### 2. Assess first — have them restate

**Before teaching anything**, proactively ask the human to restate their
current understanding of the subject. This calibrates where they are so
you teach the gaps, not the things they already know.

If the human has **no prior exposure** (common for the default subject —
a diff the agent just produced and the human hasn't read), skip the
restate: give a baseline teach of stage 1, then resume assess-then-fill
from stage 2 onward.

**Depth modes** — start at the level the restate implies; on request, or
on a missed quiz, drop one level simpler:

- **ELI14** — explain like they're fourteen (default for most code).
- **ELII** — explain like they're an intern (domain-naive but capable).
- **ELI5** — explain like they're five (last resort for a stuck concept).

### 3. Teach incrementally — one stage at a time

Do this **incrementally with each step, not all at once at the end.**
Walk the checklist stage by stage. Within each stage teach both:

- **High level** — motivation, the why, the shape of the thing.
- **Low level** — business logic, the actual code, the edge cases.

**Show, don't just tell.** Open the relevant code, point at the exact
lines, walk the debugger when it sharpens a point. Concrete beats
abstract.

### 4. Verify mastery before advancing — quiz

> **Hard gate:** do not move to the next stage until the human has
> demonstrated they've mastered the current one.

Probe with `AskUserQuestion` — open-ended or multiple-choice:

- **Randomize the position of the correct answer** across questions (don't always make it option A).
- **Do not reveal the answer until after they submit.**
- After they answer, explain *why* the right answer is right and the
  distractors are wrong — the explanation is where the learning lands.

If they miss, **re-teach one depth level simpler** (ELI14 → ELII → ELI5)
with a different frame — analogy, code, a worked example — and re-probe.
Mark the checklist item `- [x]` only once they've answered correctly
*and* can say why.

**The box-check is the gate.** A box goes `[x]` *only* on a correct,
explained human answer — never on the agent's judgment that it taught the
point well. The human's answer is the one signal causally independent of
the agent (the `h ⟂ U` rule in
`research/entities/concept/incantation-to-control.md`); marking your own
box without it is the open-loop failure this skill exists to prevent.

### 5. Close the loop — `/goal`

Set a goal condition tied to the **machine-checkable proxy** — checklist
boxes, not a vibe of understanding:

```
/goal Do not end until every checklist item in
docs/comprehend/<doc>.md is marked [x]. A box may be checked only after
the human answered a quiz on it correctly and explained why.
```

The `/goal` mechanism (P19, internal+in-session quadrant) keeps the loop
closed — the agent keeps teaching/quizzing until every box is checked,
instead of handing control back after one pass. The condition is checkable
(boxes in a file); the *meaning* of a checked box is enforced by step 4's
human-answer gate, so the agent cannot satisfy `/goal` by self-marking.

## What "done" looks like

- The checklist doc exists at `docs/comprehend/…` and **every box is checked**.
- For each box, the human answered a verification question correctly *and* articulated the why.
- The human could now explain the problem, the solution's design decisions, the edge cases, and the downstream impact unprompted.

If any box is unchecked, the skill is not done — keep going (the `/goal`
gate enforces this).

## Composition map

| Step | Composes |
|---|---|
| Persisted checklist | **P6** Bookkeeping (artifact under `docs/`) |
| Show the code / debugger | Read / Bash / repo tools |
| Quiz | `AskUserQuestion` (native) |
| Don't-end-until-verified | **`/goal`** (P19, internal+in-session) |
| Calibrate depth | ELI5 / ELI14 / ELII modes |

## Sibling skills (don't confuse)

| Skill | Direction | Goal |
|---|---|---|
| **comprehend** | agent → human | Transfer mastery of **existing** work |
| `grill-me` / `grill-with-docs` | agent → human | Stress-test the human's **forward** plan |
| `handoff` | agent → agent | Narrative bridge for the next context |
| `Bridge` (P1) / `Bookkeeping` (P6) | agent → KG | Persist knowledge to the graph |

## Anti-rationalization

| Excuse | Reality |
|---|---|
| "I'll just summarize everything at the end." | Dump-at-end is the failure mode this skill exists to kill. Teach incrementally, verify each stage. |
| "They nodded, so they get it." | Nodding ≠ mastery. Quiz it. Mark the box only on a correct, explained answer. |
| "I'll skip the quiz, it's slow." | The quiz IS the verification signal. Without it the agent is grading its own teaching — the exact open-loop failure bstack closes. |
| "I'll teach the what, the why is obvious." | The why is the point. Drill into whys recursively — that's where understanding (vs. memorization) forms. |
| "One pass is enough, I'll hand back control." | Set `/goal`. The session is not done until every checklist box is verified. |
