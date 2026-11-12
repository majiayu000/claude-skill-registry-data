---
name: "speckit-analyze-deep"
description: "Thorough, read-only cross-artifact analysis of spec.md, plan.md, tasks.md and the design docs, checked against the current code, aiming to find every CRITICAL and HIGH issue in one pass. Use instead of /speckit-analyze when you want the analysis to converge in one or two runs."
argument-hint: "Optional focus areas, or 'delta' to re-check only what changed since HEAD"
user-invocable: true
disable-model-invocation: false
context: fork
agent: general-purpose
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Why this skill exists

`/speckit-analyze` (Spec Kit's own skill) is built to be token-efficient: it loads "minimal necessary
context", favours "high-signal" findings and offers fixes for the "top N". Each run therefore samples
the artifacts, and issues surface over several runs. This skill trades tokens for completeness: read
everything, check claims against the code, and report every finding, so one run (plus at most one
delta re-check after fixes) is enough. It is a project-local companion, so a Spec Kit upgrade won't
overwrite it.

## Operating constraints

- **STRICTLY READ-ONLY.** Do not modify any file. Output a report; the user decides what to apply.
- **Constitution authority.** `.specify/memory/constitution.md` is non-negotiable here; a conflict
  with a MUST is CRITICAL.
- **No sampling.** Read every artifact in full, not excerpts. Prefer one more tool call over one
  missed finding.
- **Ground every claim.** A finding that depends on the code (a file, prop, token, test, route)
  MUST be verified by reading that code, and cite `path:line`.

## Hooks

Check `.specify/extensions.yml` for `hooks.before_analyze` before step 1 and `hooks.after_analyze`
after the report, and output them exactly as `/speckit-analyze` does (see
`.claude/skills/speckit-analyze/SKILL.md`, "Pre-Execution Checks" and step 9). Skip silently if
there are none.

## Steps

### 1. Load everything

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` and parse
FEATURE_DIR and AVAILABLE_DOCS. Then read **in full**:

- `spec.md`, `plan.md`, `tasks.md`
- every other doc in FEATURE_DIR: `research.md`, `data-model.md`, `contracts/*`, `quickstart.md`,
  `checklists/*`
- `.specify/memory/constitution.md`
- `CLAUDE.md` (project conventions, gates, known pitfalls)

Abort with a clear message if spec, plan or tasks is missing.

If the argument is `delta`: also run `git diff HEAD -- <FEATURE_DIR>` and `git status --short`, and
run every pass below with extra attention on the changed passages and **everything that refers to
them** (step 3, pass K). Still read everything; delta changes the focus, not the coverage.

### 2. Build the models

- **Requirements**: every FR-### and SC-### (note gaps or duplicates in the numbering).
- **Stories**: each user story, its acceptance scenarios and independent test.
- **Decisions**: each research decision (R#), its chosen option and the alternatives it rejected.
- **Tasks**: ID, phase, story label, `[P]`, files touched, what it tests or builds, what it says must
  pass, and which IDs it references.
- **Code claims**: every concrete claim the docs make about existing code (paths, components, props,
  events, tokens, CSS values, test files and what they assert, routes, palette names, scripts).

### 3. Detection passes

Run **all** of these. Do not stop early, and do not cap the number of findings.

- **A. Duplication**: near-duplicate requirements, decisions or tasks.
- **B. Ambiguity**: vague terms without a measure; placeholders (TODO, ???, `<…>`); two readings of
  one sentence that would lead to different code.
- **C. Underspecification**: requirements without a measurable outcome; stories whose scenarios don't
  match their requirements; tasks that name a file, token, class or helper no doc defines; behaviour
  with no stated home (which file a rule lives in, which component owns a state).
- **D. Constitution**: every MUST/SHOULD principle against the plan and tasks (tests first, book
  entries and Brave checks for standalone components, real-page checks for pages, dependency pins,
  gates, layering).
- **E. Coverage**: every requirement and buildable success criterion has a task that builds it and
  one that verifies it; every edge case is exercised by a test, a book option or a Brave step.
- **F. Consistency**: terminology drift; values that differ between docs (limits, sizes, names,
  colours, IDs); the spec, data model, contract and tasks describing the same thing differently.
- **G. Code reality**: verify every code claim from step 2 by reading the code. Flag claims that are
  false, stale, or that will become false once an earlier task lands (for example, a test the plan
  says to "extend" whose current assertions the new design breaks).
- **H. Test–design contradictions**: for each test task, ask whether the test as written can pass
  against the design as written. Look especially at existing tests the feature touches, and at
  design changes added late (a new element, a renamed class, a moved rule) that an older test still
  counts or forbids.
- **I. Verifiability**: for each check (test, book option, Brave step), ask whether the thing can be
  observed where it is checked. Examples: a viewport `@media` rule can't be seen through the book's
  width control (which resizes a box, not the window); jsdom can't compute scoped styles, so a mount
  test can't check a colour; a Brave step on a page without an event log can't "see a log".
- **J. Task order and form**: each test task precedes the task that makes it pass, and is written to
  fail first; `[P]` only on tasks touching different files with no unmet dependency; each task names
  its files; dependencies between phases are stated.
- **K. Cross-references and ripple**: every task ID, R#, FR/SC ID, file path and finding reference
  cited in any doc exists and points at the right thing (renumbering is a common cause of breakage).
  For each recently changed passage (delta mode) or each decision, list what else depends on it, and
  check those still agree.
- **L. Project gates**: risks the project's gates will reject: files likely to pass the size limit
  (count planned test cases per file), exports with no production caller (knip), colour values
  outside the palette, raw form controls outside the exemptions, anything `CLAUDE.md` lists as a
  pitfall.

### 4. Severity

- **CRITICAL**: violates a constitution MUST; a core artifact missing; a baseline requirement with no
  task.
- **HIGH**: a task that can't be completed as written (a test that can't pass against the design, a
  check that can't observe what it checks, a false code claim a task depends on); conflicting
  requirements; an untestable acceptance criterion.
- **MEDIUM**: missing verification for a requirement or edge case; test-first order broken; behaviour
  with no stated home; drift that will confuse the implementer.
- **LOW**: wording, minor redundancy, stale references that don't change what gets built.

### 5. Recommend fixes with their ripple

For every finding, give a concrete fix **and its ripple**: what else must change for the fix to stay
consistent (other docs, tests, task IDs, references). A fix that would create a new finding is
not a fix. If a fix adds or splits a task, say how the later IDs and every reference to them shift.

### 6. Report

```markdown
## Deep Analysis Report: <feature>

| ID | Category | Severity | Location(s) | Summary | Fix | Ripple |
|----|----------|----------|-------------|---------|-----|--------|
```

Then:
- **Coverage**: one row per FR/SC: building task(s), verifying task(s), notes.
- **Code claims checked**: each claim from step 2 with ✓ or the finding ID.
- **Metrics**: requirements, tasks, coverage %, findings by severity.
- **Confidence**: what you could not verify, and why. Say so plainly rather than guessing.
- **Next actions**: if CRITICAL or HIGH remain, list them first. After the user applies fixes,
  recommend `/speckit-analyze-deep delta` once to confirm, not another full run.

End by asking: "Would you like me to apply all of these fixes?" (Do not apply them yourself.)
