---
name: persona-author
description: >-
  Author or improve an ADD-method persona file (a .add/personas/ slug.md) — the project-fit
  requirements LENS the ADD skill loads at the Direction, Build and Verify beats.
  Use when adding a domain expert to a project's personas, when no persona fits a task's kind
  and one should be drafted, or when folding a retrospective into an existing persona. Produces a schema-valid persona (Identity, Critical Rules, Default Requirement,
  Success Metrics, plus recommended frontmatter and Abilities/Anti-patterns/Playbook) that carries
  the judgment layer of strong agent design: earned-perspective identity, bold-lead rules, the
  qualification gate, read-before-you-assert, failure-mode-aware metrics, defended budgets, and
  per-flow stances. Seeds a first draft
  from the teacher library or a sample subagent when a near-fit source exists, instead of a blank page.
---

# Authoring an ADD persona

A persona is a **lens, not a voice** — a distilled slice of domain expertise the ADD skill
loads onto a beat so a generic agent becomes the specialist. Author for that seam and nothing
else: **tone belongs to the agent's own voice**, the **self-assessment lives in the agent**,
and the **deliverable's shape lives in the agent's Return contract**. A persona that duplicates
any of those is dead weight. What a persona owns is *judgment*: the rules it refuses to wave
through, the smells it suspects, the done-bar it measures against.

Two references and one worked example back this workflow — read them as you go:
- **`references/contract.md`** — the exact persona contract (required/recommended/optional
  sections, frontmatter field semantics, the flow values and task-kinds taxonomy). Read this
  FIRST; a persona that misses the contract is selected at no beat.
- **`references/patterns.md`** — the judgment layer distilled from a deep read of strong subagent
  files plus a diagnosis of the vendored teacher corpus, each pattern with a before/after. This is
  what separates an expert lens from a keyword list.
- **`references/seeding.md`** — how to SEED a first draft from an existing source (the teacher
  library at `.add/personas-teacher/`, or a `~/.claude/agents/*.md` subagent) instead of a blank
  page: the two source→schema mappings, and the columns a source never supplies (failure-aware
  Success Metrics, `not-when`, read-before-you-assert) that you must add yourself.
- **`assets/example-persona.md`** (an I/O lens), **`assets/example-design-persona.md`** (a design
  lens), and **`assets/example-architect-persona.md`** (a direction lens) — three fully-worked
  personas to imitate, not copy. Compare them: the I/O lens carries a design-for-failure ability AND
  Critical Rule; the design lens omits both (it touches no I/O) and leads with accessibility
  instead. Proof the patterns are *conditional* — matched to the surface. The architect lens is the
  only one of the three with an **`## Escalation`** section: a lens that owns the direction beat has
  stop-conditions (a frozen contract that would have to move, a reversibility call, an unmeasurable
  bar) that are distinct from its always-do rules and its guilty-until-proven smells.

## Decide the move

Most requests are NOT "write a new persona". Pick the path first:

1. **A sibling already fits** — its `use-when:` matches the task's `kind:` and domain → *select it,
   don't author*. A roster of near-duplicates is worse than one sharp lens.
2. **A sibling ALMOST fits** and the gap is a lesson worth keeping → *fold into it* (bump its
   `folded:` line), don't fork a near-twin.
3. **No lens owns this seam** → author a new one. Don't start blank: **seed** from the nearest
   teacher persona (`.add/personas-teacher/`) or a sample subagent (`~/.claude/agents/*.md`) per
   `references/seeding.md`, then run the Workflow below over the seeded draft.

When unsure, prefer (1) then (2). A new persona must earn its place by owning a seam no sibling does.

## Workflow

1. **ORIENT before drafting.** Read `.add/PROJECT.md`. Read the sibling personas
   in `.add/personas/*.md` (frontmatter alone is enough) and, if present, the teacher library at
   `.add/personas-teacher/`. You are placing ONE lens in a roster — know the neighbours so this
   persona has a distinct seam, not an overlap. If you'll author (no sibling fits), pick the
   nearest teacher persona or a sample subagent as a seed now and follow `references/seeding.md` —
   a head-start on structure beats a blank page (the judgment layer is still yours to add).

2. **Fix the seam (frontmatter).** Decide the apply-`flow:` (design · build · advisor · verify —
   comma-separate if more than one; NO other value is loaded), the `task-kinds:` it owns (from the
   closed taxonomy), and the `use-when:` / `not-when:` boundary that routes THIS persona over its
   siblings. See `references/contract.md` for exact semantics — these keys are the selection contract.
   Claiming more than one flow? Plan the **per-flow stance** now: one line per flow on what the
   lens leads with there (a verify stance defaults to NEEDS-WORK until the evidence cites the run).

3. **Write Identity with earned perspective.** One short paragraph: role, domain depth, and *what
   this lens has seen succeed or fail* that shapes its judgement. Scars, not a résumé.

4. **Write Critical Rules bold-lead.** Each rule leads with a `**bold clause** — then the why`.
   Keep 1–2 as the persona's signature non-negotiables (distil the teacher's, don't replace them),
   then the project's. Carry the two default stances: **surface tradeoffs** (name the choice + the
   cost, never silently pick) and the **qualification gate** (name the simplest baseline that meets
   the contract — if it wins, take it and stop; cleverness is a tax). Prefer a **named budget over
   an adjective** ("p95 < 200 ms", "44×44 px") — only a number the expert would defend and the lens
   can check in-session; fake precision is worse than none. Keep it to what it would refuse.

5. **List Abilities — concrete, anchored, checkable.** Lead with the ORIENT commands the lens runs
   on load (the task file · the suite · the diff). State each ability as something doable *now*,
   anchored to a real file/tool/command — never an aspiration. A persona that owns I/O/network/infra
   carries a **design-for-failure** ability (timeout · retry · circuit-breaker · rollback for every
   external call; an unbounded await or silent half-write is a defect).

6. **Name Anti-patterns — guilty-until-proven.** The asymmetric instincts this lens defaults to
   *suspecting* (distinct from always-do rules). The sharpest ones are the instincts the Identity's
   scars produced — attach the COST where you can ("PIL in prod → 3× slower than cv2"). Always
   include **read-before-you-assert**: a claim resting on a file/symbol not opened → open it or
   cut the claim — and no placeholder survives into a cited deliverable.

7. **Set Default Requirement + Success Metrics.** The one requirement in every deliverable, then
   MEASURABLE outcomes stated as INVARIANTS (true as the project grows, never a today-snapshot that
   rots). Sharpen each by **the failure it guards against** — a metric catches a specific way of
   being wrong — and keep every bar checkable in-session; an invented outcome statistic
   ("engagement +40%") is the signature rot of weak persona corpora.

8. **(Optional) Playbook.** Only if the lens carries executable know-how: a named methodology with
   its verbatim moves and why-they-work, a cheap→expensive intervention ladder, an ADR skeleton, a
   red→green loop — never a tutorial code dump. Tag each item `(teacher)` or `(ADD)` so provenance
   is honest.

9. **VALIDATE.** Save as `.add/personas/<slug>.md` (never overwrite; avoid `_`-prefixed names).
   Check the routing keys by hand against `references/contract.md` (every `flow:` and
   `task-kinds:` value from its closed set). Nothing lints quality: sweep bare `<…>`
   placeholders yourself; whether the lens fits this project remains your judgment.

## The one-line test

Before finishing, read the persona as its future self would: *"Given only this lens and a task of
my kind, would I make a sharper decision than a generic 15-year specialist?"* If not, the judgment
layer is too thin — deepen the Critical Rules, Anti-patterns, and failure-aware Metrics (that is
where expertise lives), not the prose.
