---
name: analyze
description: >
  Cross-artifact consistency report for jig specs — a non-destructive
  six-category audit at CRITICAL/HIGH/MEDIUM/LOW severity, covering
  duplication, ambiguity, underspecification, principle violations,
  coverage gaps, and terminology drift. Auto-triggers when you say
  analyze this spec, check for inconsistencies, audit ADR vs spec drift,
  check whether the decision records still agree with the spec,
  cross-artifact alignment, find drift in this spec, or audit this spec
  for principle violations. Do not use for: pre-DRAFT ambiguity scanning
  (use `/jig:clarify` instead); structural frontmatter or slice-numbering
  validation (use `spec_lint.py` instead); spec-compliance review
  of a finished slice (use `/jig:independent-review` instead).
user-invocable: true
---

> Spec 024 introduces this skill as jig's **cross-artifact consistency
> auditor**. It is the seventh non-stub active jig skill that ships
> without a `.py` helper — analyze is fundamentally a judgment skill,
> and the determinism it needs (locate the spec, walk siblings, read
> the principles list, sort findings by severity) Claude can run inline
> via Read + Glob. The skill slots between `READY_FOR_REVIEW` (spec body
> ready for first review) and `IN_PROGRESS` (slice already in flight),
> giving the spec author one more pass to catch cross-artifact drift
> before the first review verdict.
>
> Per user direction on 2026-05-18, jig's analyze ships as a
> **standalone baseline**, not a deferral surface. Power users who
> want spec-kit's richer `/speckit.analyze` install spec-kit and invoke
> it explicitly under `/speckit.*`. There is no category-based
> deferral hint in this skill's description.

## What this skill does

Produces a **non-destructive** cross-artifact consistency report for a
single spec across the six-category taxonomy at CRITICAL/HIGH/MEDIUM/LOW
severity. **Reporter only — no file writes.** The skill reads one
`spec.md` plus its sibling `slice-NN-*.md` files, plus a small set of
read-only cross-reference docs (`docs/product-vision.md` for principles,
`docs/decisions/*.md` for ADR resolution, `docs/memory/glossary.md` for
terminology, `docs/architecture.md` for architecture-drift checks), and
emits a markdown report to stdout: a findings table sorted by severity,
a per-category coverage summary, and actionable next steps.

The skill is **breadth over depth**: surface the obvious cross-artifact
drift within a few minutes, leave deep manual auditing to the spec
author's judgment or to a richer downstream tool. The 50-findings
ceiling exists to keep the scan scannable; if a spec generates more
than 50 findings, the spec needs structural surgery, not a longer
report.

## When to use vs. when to defer

There are four sibling skills people often confuse with this one. Pick
the right one:

- **`/jig:clarify`** — sibling skill for **pre-DRAFT ambiguity scans**.
  Clarify asks questions to the user and appends a `## Clarifications`
  section to the target doc. It is prospective: "what's unanswered in
  this spec?" Analyze is retrospective: "where do these artifacts
  disagree?" Reach for `/jig:clarify` before the spec hits
  READY_FOR_REVIEW; reach for this skill once the spec body is stable
  enough to cross-check against ADRs, architecture.md, and the
  principles list.
- **`spec_lint.py`** — structural linter (frontmatter shape,
  slice numbering, file naming). Lint is **structural**; this skill is
  **semantic**. Lint catches "slice file missing `status:` frontmatter";
  this skill catches "slice contradicts ADR-0003" or "spec proposes a
  fourth subagent type". The two layers are complementary — run
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/spec_lint.py"` first to fix
  structural issues, then run this skill to find semantic drift.
- **`/jig:independent-review`** — sibling skill for **spec-vs-implementation
  reviews**. Independent-review reads a finished slice's deliverables
  and verifies they meet the ACs. This skill reads the spec body and
  ADRs/architecture and surfaces intra-spec drift. Different axis:
  independent-review evaluates implementation against spec; this skill
  evaluates spec against the project's other artifacts. Reach for
  `/jig:independent-review` after the slice is implemented; reach for
  this skill while the spec body is being finalized.
- **`/jig:pr-review`** — sibling skill for **diff-shape reviews**. PR
  review reads a git diff and surfaces blockers / nits / strengths.
  This skill reads a spec doc, not a diff. Different artifact shape:
  PR review evaluates a code change; this skill evaluates a spec
  document. Reach for `/jig:pr-review` after the slice's PR is open;
  reach for this skill while the spec body is being authored or
  refined.

Rule of thumb: **draft a spec → `/jig:clarify`. Structural lint → `spec_lint.py`.
Cross-artifact drift → this skill. Review the implementation → `/jig:independent-review`.
Review the PR diff → `/jig:pr-review`.**

## Inputs

The MVP scans **one spec at a time**.

**Primary input:**

- One `spec.md` (e.g., `docs/specs/024-analyze/spec.md`) **plus all
  sibling `slice-NN-*.md` files** in the same directory. The skill
  walks the spec directory and treats every `slice-*.md` file as
  part of the audit scope.

**Read-only secondary inputs** (for cross-referencing):

- `docs/product-vision.md` — the seven principles for the Principle
  Violations finding category.
- `docs/decisions/*.md` — accepted ADRs for resolving `ADR-NNNN`
  references in the spec body.
- `docs/memory/glossary.md` — canonical glossary terms for the
  Terminology Drift finding category.
- `docs/architecture.md` — declared architectural decisions for
  architecture-drift checks.

**Cross-spec input is explicitly NOT supported by the MVP.** Auditing
all of `docs/specs/` for drift (e.g. "spec 010's ADR-0003 reference
resolves to an ADR that's been superseded") is the territory of a
future slice 024-02 if signal emerges. If the same friction surfaces
three times across real usage, that slice can land. Until then, the
user re-runs the skill per spec.

## Six finding categories

The skill scans the target spec across six categories. Each finding
gets a severity (CRITICAL / HIGH / MEDIUM / LOW). All findings are
collected, sorted by severity, and rendered in the output. If a
category produces zero findings, it still appears in the coverage
summary table with `0` so the reader can verify the scan ran.

### Duplication

Two or more places in the spec body (or across sibling slice files)
say the same thing in subtly different ways. Watch for near-duplicate
ACs, repeated constraints with conflicting phrasing, and ADR-NNNN
restatements that re-declare a decision already captured in an ADR.

What triggers a finding:

- Two ACs in the same slice whose normalized text overlaps >70% (likely
  duplicate or near-duplicate).
- The same constraint stated in both `spec.md` and a sibling
  `slice-NN-*.md` file with conflicting phrasing (one says "exit 2",
  the other "exit 3").
- An ADR-NNNN restated as an AC in the spec body (the decision should
  live in the ADR; the AC should reference it, not duplicate it).
- A non-goal stated in `## Non-goals` that is also implicit in a
  Goals bullet (e.g., "Goal: ship feature X" + "Non-goal: do not ship
  feature X immediately").

### Ambiguity

Vague terms, placeholders, and unresolved TODOs that make the spec
non-actionable. Watch for unbounded qualifiers and copy-pasted "TBD"
markers that should have been resolved before READY_FOR_REVIEW.

What triggers a finding:

- Vague qualifiers without bounds: "fast", "scalable", "lightweight",
  "configurable" (without naming what knobs).
- Literal `TBD` / `_TBD_` / `<TBD>` placeholders in non-Overview
  sections (Overview can stay TBD during DRAFT; ACs and Goals cannot).
- Unresolved `TODO` bullets in ACs or DoD checklists.
- Pronouns or demonstratives with no clear antecedent ("the helper",
  "this slice", "the user" — when multiple candidate referents exist).
- A `## Clarifications` section exists but one Q entry has no answer
  yet (the question was asked but unanswered).

### Underspecification

ACs without measurable outcomes; slices without dependencies declared;
clarifications missing when the spec is non-trivial. Watch for the
case where the spec gestures at a deliverable without saying how
"done" is observed.

What triggers a finding:

- An AC without a measurable outcome verb — no "returns", "writes",
  "refuses", "logs", "exits", "creates", "raises". Aspirational ACs
  like "the helper should work well" trigger this.
- A slice with empty `dependencies: []` frontmatter when prose
  references a precedent slice (e.g., "follows 022-02's pattern" but
  no `dependencies: [022-02]`).
- A spec with ≥5 ACs but no `## Clarifications` section (suggests
  the spec didn't go through `/jig:clarify` despite non-trivial
  scope).
- A DoD checkbox referencing an artifact never produced anywhere in
  the spec body or slice files.

### Principle Violations

The spec contradicts one or more of the seven principles in
`docs/product-vision.md` § Design principles. **This is the
constitution-gate category** — it codifies the same check
`independent-review` now runs on every slice review (per slice 024-01
AC #6).

What triggers a finding:

- Spec proposes a fourth subagent type or a new role beyond
  `implementer` / `reviewer` / `architect` (principle 3 — three
  subagents, no more).
- Spec describes a new skill that duplicates an existing skill's
  responsibility without an ADR justification (principle 6 — no
  shims, also principle 4 — dogfooding).
- Spec assumes a context-window above 40% fill is fine (principle 2 —
  stay below the dumb zone).
- Spec describes a workflow rule that should be a hook but ships as a
  skill, or vice versa (principle 1 — hooks deterministic, skills
  judgment).
- Spec ships scaffolded files as plugin-internal-only with no
  scaffolding-mode equivalent (principle 7 — owning scaffolding beats
  renting).

### Coverage Gaps

ACs without corresponding tests in the repo (or no test plan
documented); slices that claim a hard decision without an ADR
back-link; APIs introduced without a contracts-skill recommendation.
Watch for ACs that ship without verification surface.

What triggers a finding:

- An AC mentions a behavior with no corresponding test path in the
  spec's test plan, and no test file matching the implied path exists
  in `tests/` or `skills/<name>/test_*.py`.
- A slice claims an architectural decision ("we chose X over Y because
  Z") with no `adr-NNNN-*.md` back-link.
- An AC mentions a public API surface (HTTP endpoint, JSON schema,
  CLI output) without a `/jig:contracts` recommendation or a
  declared `## Contract surfaces` entry in `docs/architecture.md`.
- A DoD checkbox names a verification step (e.g., "dogfood runs
  clean") with no instructions for how the dogfood is performed.

### Terminology Drift

Glossary terms used inconsistently with `docs/memory/glossary.md`;
ADR-NNNN references that don't resolve; dependency references naming
non-existent slices. Watch for the same concept under two names, or
two concepts collapsing under one.

What triggers a finding:

- A glossary term defined in `docs/memory/glossary.md` is used with a
  synonym interchangeably in the spec (e.g., glossary says "slice"
  but spec also uses "task" for the same concept).
- An ADR-NNNN reference (`ADR-0003`, `adr-0003`, `decision 0003`)
  doesn't resolve to an existing `docs/decisions/adr-NNNN-*.md` file.
- A dependency reference like `dependencies: [050-01]` names a slice
  that doesn't exist (no `docs/specs/050-*/` directory).
- A skill name spelled inconsistently across the spec body (e.g.,
  `/jig:slice-land`, `slice-land`, and "the land helper" all in one
  doc).
- A tier label spelled inconsistently (Tier 0 vs `tier-0` vs
  "always-on" all in the same doc).

## Severity scoring

Findings are scored against a four-level severity ladder. The model
judges each finding case-by-case using these definitions:

- **CRITICAL** — the spec is internally contradictory or violates a
  load-bearing principle in a way that blocks READY_FOR_IMPLEMENTATION.
  Example: spec proposes a fourth subagent type (principle 3
  violation). Example: an AC and a Non-goal directly contradict.
- **HIGH** — significant gap that should be resolved or explicitly
  accepted before merge. Example: an AC has no measurable outcome
  verb. Example: an ADR-NNNN reference doesn't resolve.
- **MEDIUM** — material drift that ships if explicitly accepted in
  the spec body or tracked in `docs/inbox.md`. Example: glossary term
  inconsistency. Example: ambiguous qualifier without bounds.
- **LOW** — minor stylistic or near-duplicate finding; can ship
  silently if the rest of the spec is clean. Example: same constraint
  restated in two adjacent bullets.

**Principle-violation severity defaults**: principles 1-3 (Hooks/skills,
context economy, three subagents) map to **HIGH** by default —
violating these undermines jig's core architecture. Principles 4-7
(dogfooding, deferral, no-shims, scaffolding-not-renting) map to
**MEDIUM** by default — these are load-bearing but allow more
case-by-case judgment. The model can override either default based
on context (e.g., a principle-7 violation that strands all migrating
users gets bumped to HIGH).

## Output format

The skill emits a markdown report to **stdout**. **No file writes.**
The exact shape:

```markdown
# Analyze: <spec-id> — <spec-slug>
_Scanned 2026-MM-DD; <N> findings._

## Findings (sorted by severity)

| # | Severity | Category | Location | Finding |
|---|---|---|---|---|
| 1 | CRITICAL | Principle Violations | spec.md:42 | Spec proposes a 4th subagent type, violating principle 3. |
| 2 | HIGH | Coverage Gaps | slice-01-foo.md:18 | AC #2 has no corresponding test path. |
| ... | ... | ... | ... | ... |

## Coverage summary

| Category | Findings |
|---|---|
| Duplication | 0 |
| Ambiguity | 3 |
| Underspecification | 2 |
| Principle Violations | 1 |
| Coverage Gaps | 1 |
| Terminology Drift | 0 |

## Next steps

- Address the CRITICAL finding before READY_FOR_IMPLEMENTATION.
- HIGH findings should be resolved or explicitly accepted in
  the spec body before merge.
- MEDIUM/LOW findings can ship if tracked in `docs/inbox.md`.
```

**Shape rules:**

- Findings sorted CRITICAL → HIGH → MEDIUM → LOW. Within a severity
  band, ordering is by category (the six-category order in this
  document).
- If a category produces zero findings, it still appears in the
  Coverage summary table with `0` so the reader can verify the scan
  ran across all six.
- **Max 50 findings per run.** If the scan exceeds this, the
  findings table emits "(truncated at 50)" as a final row and the
  Coverage summary reflects the truncated count plus a parenthetical
  note ("Coverage shown; underlying scan was truncated at 50
  findings — the spec needs structural surgery, not a longer
  report.").

**Surfaced, never auto-resolved (issue #125).** The report *reports drift and
hands off* — it names each finding for the spec author to resolve. When two
canon artifacts disagree, analyze does **not** adjudicate which one wins or
write the resolution: picking a winner and amending a closed record is a
separate, owner-authorised act (see the `spec-workflow` reconciliation
checklist's closed-spec-drift gate). This posture is stronger than "no file
writes", which only says the skill's own process is read-only; the point here
is that a discovered conflict is *escalated, not decided*.

## Gotchas

- **Non-destructive — the skill never writes to disk.** Even when the
  scan finds a CRITICAL drift, the skill does not edit any spec, ADR,
  or architecture file. It emits findings; the spec author resolves
  them. Same shape as `/jig:pr-review` and `/jig:arch-review`:
  reporter only.
- **One-spec-at-a-time scope.** The MVP scans one spec per invocation.
  If the same friction surfaces three times across real usage, slice
  024-02 (deferred) can ship a cross-spec auditor. Until then, the
  user re-runs the skill per spec.
- **Principle-violation severity is subject to judgment.** The
  defaults (principles 1-3 → HIGH, principles 4-7 → MEDIUM) are
  starting points. The model can and should override based on
  context — a principle-7 violation that strands all migrating users
  gets bumped to CRITICAL; a principle-2 violation in a deliberately
  context-heavy dev tool gets demoted to LOW. The severity column is
  not a deterministic table lookup.
- **No `.py` helper for analyze itself** (no helper, judgment-only
  skill). Spec 024-01 explicitly ships SKILL.md only. The
  reviewer-prompt principles-check (AC #6) is a separate code change
  in `skills/independent-review/review.py` (a new
  `_principles_check_block()` helper appended unconditionally to
  both prompt builders), not part of analyze's runtime. If
  determinism friction surfaces three times — the model misses
  systematic drift across runs — slice 024-03 (deferred) can ship
  `analyze.py gather` to aggregate findings.

## Relationship to other skills

- **`/jig:clarify`** — sibling (spec 023, sequenced before this skill).
  Clarify is prospective: it asks questions to fill gaps before the
  spec hits READY_FOR_REVIEW. Analyze is retrospective: it surfaces
  drift across artifacts that should already be aligned. The two
  compose: run `/jig:clarify` early in DRAFT, run this skill before
  or during READY_FOR_REVIEW.
- **`spec_lint.py`** — structural lint (frontmatter shape,
  slice numbering, file naming). Complementary, not overlapping.
  Lint catches "slice file missing `status:` frontmatter"; this
  skill catches "slice contradicts ADR-0003". Run lint first to
  fix structural issues, then run this skill to find semantic drift.
- **`/jig:independent-review`** — sibling, orthogonal axis.
  Independent-review evaluates implementation against spec; this
  skill evaluates spec against the project's other artifacts. They
  are not redundant: independent-review assumes the spec is
  internally consistent, this skill verifies it is.
- **`/jig:pr-review`** — sibling, orthogonal artifact.
  PR review reads a diff and surfaces blockers / nits / strengths.
  This skill reads a spec doc, not a diff. Different shape,
  different reading material.
- **`/jig:adr-workflow`** — downstream. Some analyze findings
  ("this AC restates an ADR — move it to the ADR body") will route
  the spec author to `/jig:adr-workflow new` or `/jig:adr-workflow
  resolve-todo`. Analyze surfaces the gap; adr-workflow fills it.
- **`/jig:contracts`** — downstream for Coverage Gaps findings.
  When analyze flags an AC that mentions an external API surface
  with no contract recommendation, the spec author runs
  `/jig:contracts` to add an OpenAPI / JSON Schema / etc.
  declaration.
