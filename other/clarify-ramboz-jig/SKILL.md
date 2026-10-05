---
name: clarify
description: >
  Lightweight spec clarification scan for jig projects — a six-category
  ambiguity audit that asks up to five prioritized questions and appends
  them to the spec's `## Clarifications` section. Auto-triggers when you
  say clarify this spec, audit this spec for ambiguities, is this spec
  ready for review, find unknowns in this scope, surface what's still
  unclear or unspecified, scan for unanswered questions, or what's
  missing from this spec. Do not use for:
  spec-compliance review of a finished slice (use
  `/jig:independent-review` instead); cross-artifact consistency
  analysis or drift detection (use `/jig:analyze` instead); project-vision
  or architecture elicitation (use `/jig:vision-elicitation` instead).
user-invocable: true
---

> Spec 023 introduces this skill as jig's **pre-spec ambiguity scan**. It
> is the sixth non-stub active jig skill that ships without a `.py`
> helper — clarify is fundamentally a judgment skill, and the
> determinism it needs (locate the target doc, find an existing
> `## Clarifications` section if any, append new entries) Claude can
> run inline via Read + Edit. The skill slots between
> `workflow.py new <slug>` (stub reservation) and the
> `READY_FOR_REVIEW` transition (spec body ready for first review).
>
> Per user direction on 2026-05-18, jig's clarify ships as a
> **standalone baseline**, not a deferral surface. Power users who
> want spec-kit's `/speckit.clarify` install spec-kit and invoke it
> explicitly under `/speckit.*`. There is no category-based deferral
> hint in this skill's description.

## What this skill does

Runs a structured ambiguity scan against a DRAFT-state spec document
across **six categories** aligned with jig's slice template (Scope &
Boundaries / Acceptance Criteria Testability / Dependencies & Blockers /
Non-functional Requirements / Edge Cases & Failure Modes / Terminology
Consistency). The skill rates each category Clear / Partial / Missing,
selects up to **five prioritized questions** (Partial/Missing weighted
above Clear), asks them one at a time recording the user's verbatim
answer, and appends a `## Clarifications` section to the target document
with the Q/A entries plus a coverage summary table.

The skill is **breadth over depth**: catch the obvious unanswered
questions across the six taxonomy categories in a few minutes, leave
deep domain-specific clarification (legal review, regulatory edges,
multi-stakeholder facilitation) to the dev's judgment or to a richer
team process. The five-question budget exists to keep the scan
lightweight enough to actually run before each `READY_FOR_REVIEW`
transition — not so heavy it becomes a chore the team skips.

## When to use vs. when to defer

There are four sibling skills people often confuse with this one. Pick
the right one:

- **`/jig:spec-workflow`** — sibling skill for **state transitions**
  (`workflow.py new`, `workflow.py transition`, status board regen).
  Spec-workflow moves a slice between DRAFT / READY_FOR_REVIEW /
  IN_PROGRESS / REVIEWED / RECONCILED / DONE; it does not elicit
  clarifications. Reach for `/jig:spec-workflow` when you want to
  reserve a new spec number or push a slice to the next state.
  Reach for this skill when the spec body has gaps you want surfaced
  *before* the next transition.
- **`/jig:analyze`** — sibling jig skill (spec 024, sequenced after
  this one) for **cross-artifact consistency analysis**. Analyze
  reads multiple specs + ADRs + docs and surfaces drift between
  them. This skill scans **one document** for internal ambiguities.
  Reach for `/jig:analyze` when you suspect a spec disagrees with
  another spec or with an ADR. Reach for this skill when one spec's
  body has unanswered questions in isolation.
- **`/jig:vision-elicitation`** — sibling skill that fills slots in
  `docs/product-vision.md` and `docs/architecture.md`. That's
  **project-scope elicitation**: who are the users, what's the
  problem, what's the architecture? This skill is **spec-scope
  elicitation**: what does this *one slice* mean, what are its
  ACs, what are its dependencies? Reach for vision-elicitation
  immediately after `scaffold-init`; reach for this skill when
  authoring or reviewing a single spec.
- **`/jig:independent-review`** — sibling skill that reviews a
  finished slice against its spec.md. Independent-review **assumes
  the spec is clear** — it checks the implementation against the
  ACs. This skill helps make the spec clear in the first place,
  so independent-review has something specific to review against.
  Reach for `/jig:independent-review` after the slice is
  implemented; reach for this skill before the slice has
  transitioned to `READY_FOR_REVIEW`.

Rule of thumb: **draft a spec → this skill. Transition a spec →
`/jig:spec-workflow`. Audit across specs → `/jig:analyze`. Review the
implementation → `/jig:independent-review`. Set up the project →
`/jig:vision-elicitation`.**

## Inputs

Two input modes, both supported by the MVP:

1. **Single `spec.md` (overview-level scan).** The user names a spec
   directory (`docs/specs/023-clarify/`) or its `spec.md` file
   directly. The scan covers the spec body's Overview / Why now /
   Goals / Non-goals / Decomposition / Open questions sections. The
   `## Clarifications` section gets appended to that `spec.md`.
2. **One `slice-NN-*.md` (slice-level scan).** The user names a
   specific slice file (`docs/specs/023-clarify/slice-01-clarify-skill-md.md`).
   The scan covers the slice's Goal / DoR / Acceptance Criteria /
   DoD / Anti-horizontal-phasing check. The `## Clarifications`
   section gets appended to that slice file (not to the parent
   spec.md).

**Mixed-mode ("scan the spec AND every slice") is explicitly NOT
supported by the MVP.** That requires per-doc bookkeeping and a
re-entry/resume protocol that's out of scope for this slice. If
the same friction surfaces three times across real usage, a future
slice 023-02 can ship a `.py` helper that orchestrates the loop.
Until then, the user re-runs the skill per document.

## Six-category taxonomy

For each category, the skill rates the target document Clear / Partial /
Missing. The scan is internal to the model — the rating is not shown
to the user unless an answer is sought. The categories below are aligned
with jig's slice template; spec-kit's nine-category taxonomy was slimmed
to six by dropping "Domain & Data Model" and "Interaction & UX Flow"
(which assume slots jig's slice template doesn't have) and folding
their substance into "Scope & Boundaries" where it applies.

### Scope & Boundaries

What is in-scope, what is out-of-scope, what is the boundary with
adjacent specs? Watch for unstated assumptions about which layer or
module the change touches.

What to check:

- Is the in-scope deliverable named in concrete terms (file paths,
  function names, observable outcomes)?
- Are non-goals enumerated? Or is the spec silent on what it explicitly
  won't do?
- Is the boundary with adjacent specs declared? E.g. "spec 022 covers
  external surfaces; this spec is internal-only."
- For multi-slice specs: does each slice's scope fit on its own without
  the parent overview?

### Acceptance Criteria Testability

Can each AC be turned into a passing test or a measurable observation
from outside the helper? Watch for vague verbs ("works correctly",
"handles edge cases") that hide unspecified behavior.

What to check:

- Does each AC name a measurable outcome (a file exists, a function
  returns X, an exit code is N)?
- Is each AC observable from outside the helper — testable without
  inspecting private state?
- Is the AC count reasonable for one slice (~3-10)? Too few suggests
  under-specification; too many suggests a horizontal phasing
  problem.
- Are ACs phrased imperatively ("the helper exits 0 on success")
  rather than aspirationally ("the helper should work well")?

### Dependencies & Blockers

What must be true before this slice can land? Watch for upstream work
that's silently assumed.

What to check:

- Are upstream slices listed in `dependencies:` frontmatter? Are they
  all DONE?
- Are referenced ADRs accepted (not still DRAFT)?
- Are external services / fixtures / sample data available?
- Are reviewer-side prerequisites named (e.g. "reviewer needs access
  to spec-kit reference text")?

### Non-functional Requirements

Performance / security / observability / backwards-compat / accessibility
/ regulatory constraints. Watch for the case where the spec body assumes
"normal" but never declares what abnormal looks like.

What to check:

- Are performance constraints named (latency budget, payload size
  limits)?
- Are security expectations named (auth required, secrets handling,
  PII boundaries)?
- Is observability declared (logs / metrics / events emitted)?
- Is the backwards-compat policy stated (semver bump? feature flag?
  silent migration?)?

### Edge Cases & Failure Modes

What can go wrong? What does the spec say about each failure path?
Watch for the happy path being the only path drawn.

What to check:

- Are explicit refusals enumerated (the helper exits N on condition X)?
- Are failure paths drawn — what the user sees when something goes
  wrong?
- Are race conditions / partial-state failures considered (e.g. file
  written but commit refused)?
- Is the empty-input case named (no slices yet, no ADRs yet, empty
  spec directory)?

### Terminology Consistency

Are domain terms used consistently? Watch for the same concept appearing
under two names, or two concepts collapsing under one name.

What to check:

- Are glossary terms used consistently with `docs/memory/glossary.md`?
- Do "slice" and "task" / "spec" and "issue" / "ADR" and "decision"
  mean exactly one thing each in this doc?
- Are skill names spelled the same throughout (`/jig:slice-land` vs
  `slice-land` vs "the land helper")?
- Are tier labels consistent (Tier 0 vs tier-0 vs "always-on")?

## Question-asking loop

The algorithm has four phases:

1. **Internal coverage scan.** The skill reads the target document and
   rates each of the six categories Clear / Partial / Missing. This
   rating is not shown to the user.
2. **Prioritized question selection.** The skill picks up to five
   questions to ask, weighted Partial > Missing > Clear. (Clear
   categories almost never yield useful questions; Partial means
   "the spec touches this but the answer is ambiguous"; Missing means
   "the category isn't addressed at all".) The five-question budget
   is hard: even if the spec has eight gaps, the skill asks five and
   stops.
3. **Sequential Q&A.** The skill asks one question at a time. After
   each answer, it records the user's verbatim words and moves to
   the next question. The user can answer, skip, or say "stop /
   skip remaining" to short-circuit.
4. **Stop conditions.** The loop ends when any of:
   - Five questions have been asked.
   - All six categories are now Clear or Skipped.
   - The user types "stop" or "skip remaining".
   - The user closes the session.

After the loop, the skill renders the Q&A entries and the coverage
summary table as a `## Clarifications` section appended to the target
document.

### Question phrasing

Questions are concrete, single-axis, and answerable in 1-3 sentences.
Bad: *"What about edge cases?"* (vague). Good: *"What happens if the
target directory already contains a `.claude/` folder with no
`scaffold.json` — refuse, merge, or overwrite?"* (concrete, three
named options, answerable directly).

When the model can offer a recommended default, it does — but the
user's verbatim answer is what gets written, not the default.

## Output: the `## Clarifications` section

After the Q&A loop, the skill appends a `## Clarifications` section to
the target document. The exact shape:

```markdown
## Clarifications

### Q1: <verbatim question>
_(category: <category-name>)_
_(provenance: [grounded: ADR-NNNN | path/to/doc] or [judgment])_

<verbatim user answer>

### Q2: <verbatim question>
_(category: <category-name>)_
_(provenance: [grounded: ADR-NNNN | path/to/doc] or [judgment])_

<verbatim user answer>

...

### Coverage summary

| Category | Status |
|---|---|
| Scope & Boundaries | Clear / Partial / Resolved / Outstanding / Skipped |
| Acceptance Criteria Testability | ... |
| Dependencies & Blockers | ... |
| Non-functional Requirements | ... |
| Edge Cases & Failure Modes | ... |
| Terminology Consistency | ... |
```

**Status taxonomy in the coverage summary table:**

- **Clear** — category was Clear before the scan; no question asked.
- **Resolved** — category was Partial or Missing; a question was asked
  and answered, closing the gap.
- **Partial** — category is partly clear after the scan; some questions
  remain unanswered (e.g. the five-question budget was hit before this
  category was reached).
- **Outstanding** — category is still Missing; a question was asked but
  the user deferred, or no question was reached.
- **Skipped** — the user explicitly skipped the question or the
  category.

**Provenance tag (measurement, non-gating).** Before writing each answered
question, self-assess whether it could have been answered from an
existing artifact already in the repo: `[grounded: ADR-NNNN | path]` when
the answer restates (or was clearly derivable from) a named ADR or doc
you could have read first, `[judgment]` when it's a genuine trade-off call
that needed the user's input. Best-effort and non-blocking — it exists so
a future rollup can measure whether clarify is asking already-answerable
questions before building a grounding pass (docs/refinement-todo.md
"Instrument the review→learnings→clarify loop before building it").

**Append-only behavior.** The skill does not modify any existing section
in the spec body above the `## Clarifications` heading. If
`## Clarifications` already exists (re-run case), the new entries
**append to the existing section** rather than starting a new one. Q
numbers continue from the highest existing number — Q4 becomes Q5,
Q5 becomes Q6, etc.

## Gotchas

- **Verbatim-answer rule.** The skill does not paraphrase, expand, or
  "improve" the user's answers. If the user says "refuse if .claude
  already exists," that's what gets written — not "the helper SHALL
  reject the operation when a .claude/ directory is present in the
  target." Same boundary as `/jig:vision-elicitation`: the user's
  voice in the final doc is what matters. Only two narrow exceptions:
  (a) markdown structure (rendering a list as a bullet list), (b)
  preserving the user's stated order (if Q3 lists three options in
  priority order, write them in that order).
- **Advisory, not a state-machine gate.** `workflow.py transition
  DRAFT → READY_FOR_REVIEW` does **not** refuse the transition if
  `## Clarifications` is absent. Clarify is recommended, not
  enforced. Same shape as `/jig:pr-review`: calling it is a workflow
  choice, not a step jig blocks on.
- **One-doc-at-a-time scope.** The MVP scans one document per
  invocation. Either the `spec.md` (overview-level) or one
  `slice-NN-*.md` (slice-level), never both. If the same friction
  surfaces three times across real usage, slice 023-02 can ship a
  helper that orchestrates the loop. Until then, re-run the skill
  per document.
- **No `.py` helper.** All section surgery via Read + Edit. The skill
  reads the target document inline, scans the body, asks questions,
  and appends the `## Clarifications` section by writing the
  rendered markdown via the Edit tool. No subprocess; no helper to
  invoke separately. The trade-off: the Q/A loop is conversational
  rather than batch-driven, and section detection is by visible H2
  heading rather than by frontmatter marker.
- **Re-runs append, not replace.** A second invocation against a doc
  that already has `## Clarifications` extends the existing section.
  Old Q/A entries stay; new Q/A entries follow with continuing Q
  numbers. The Coverage summary table is rewritten to reflect the
  union of both passes (a category that was Outstanding after pass 1
  and Resolved after pass 2 reads Resolved).
- **Five-question budget is a hard ceiling, not a target.** If the
  scan finds three gaps and the user answers them all in three
  questions, the skill stops at three. Don't pad the loop to five
  if the scan converges sooner.

## Relationship to other skills

- **`/jig:spec-workflow`** — sibling, different shape. Spec-workflow
  drives state transitions; this skill helps make a DRAFT spec
  ready for the first review-state transition. Two skills compose:
  this skill clarifies the spec body, spec-workflow transitions
  the slice forward.
- **`/jig:analyze`** — sibling (spec 024, sequenced after this
  spec). Analyze reads multiple specs + ADRs + docs and surfaces
  drift between them. This skill scans one document. Different
  scope, complementary purpose: clarify before READY_FOR_REVIEW,
  analyze after IN_PROGRESS to catch cross-artifact regressions.
- **`/jig:vision-elicitation`** — sibling, different scope. Vision-
  elicitation fills project-level slots in product-vision.md and
  architecture.md; this skill clarifies spec-level slots in a single
  spec.md or slice file. The two skills don't overlap.
- **`/jig:independent-review`** — sibling, downstream. Independent-
  review reviews a finished implementation against a written spec;
  this skill helps write a spec the reviewer can evaluate against.
  Without clarify, ambiguous ACs lead to reviewer findings that are
  really spec-clarity findings.
- **`/jig:adr-workflow`** — orthogonal. If a clarification answer
  amounts to a permanent decision ("we will use Python 3 stdlib only;
  no pip dependencies"), the user should also run
  `/jig:adr-workflow new` to capture the decision in an ADR. The
  `## Clarifications` entry shows the moment of resolution; the ADR
  is the durable record.
