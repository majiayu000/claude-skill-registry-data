---
name: verify-against-source
description: "Use when verifying that a prose artifact (brainstorm, design spec, plan, or implementation prompt) honors its input/source artifact(s) - the prose counterpart to verify-against-plan. Runs as the conformance axis of the planning-skill review loop. Outputs structured findings - missing scope, silent deviations from the source, scope creep, misunderstandings."
---

# Verify Against Source

The prose counterpart to `verify-against-plan`. Where `verify-against-plan` asks
"does the CODE match the plan?", this asks "does this PROSE ARTIFACT honor its
SOURCE?" — e.g. does a plan honor every locked brainstorm decision, does an
implementation prompt faithfully translate the plan + bead descriptions.

Use it as the **conformance axis** of the planning-skill review loop, paired in
parallel with a prose-quality reviewer.

This skill is **MANDATORY at plan-lock, not optional** — `project-setup`'s
Phase 0 hard-gates on the `THRUM-REVIEW` stamp's `verify=` field as evidence
that this skill specifically ran on the plan (see `project-setup/SKILL.md`
Phase 0). Skipping it is not a soft-enforcement gap; it blocks downstream
dispatch.

## Inputs

Two inputs are required. Missing either is a pre-flight bail.

### 1. Artifact path (required)

The prose document under review — a markdown brainstorm, design spec, plan, or
implementation prompt.

### 2. Source path(s) (required; one or more)

The input artifact(s) the artifact must honor. The source changes per stage:

| Artifact under review | Source(s) it must honor                             |
| --------------------- | --------------------------------------------------- |
| brainstorm            | parent decisions, feature request, ticket, siblings |
| design spec           | the brainstorm (its locked Decision Summary)        |
| plan                  | the brainstorm + design spec                        |
| implementation prompt | the plan + the bead task descriptions               |

Multiple sources are allowed and common (a plan honors both a brainstorm and a
spec; a prompt honors both a plan and bead descriptions).

### Invocation examples

```text
/verify-against-source artifact=dev-docs/plans/YYYY-MM-DD-topic-plan.md source=dev-docs/brainstorms/YYYY-MM-DD-topic-brainstorm.md
/verify-against-source artifact=dev-docs/prompts/YYYY-MM-DD-topic-prompt.md source=dev-docs/plans/YYYY-MM-DD-topic-plan.md,/tmp/bead-acs.md
```

## Pre-flight checks

This skill reviews **prose against prose**. It deliberately does NOT inherit the
two pre-flight bails that make `verify-against-plan` unusable on prose artifacts
— a prose artifact has no code diff, and a brainstorm has no File-Structure or
Acceptance/Test-plan table. Only these two checks apply:

1. **Artifact path exists and is readable.** Verify the path resolves and the
   file is non-empty markdown. Error on failure names the path and the issue
   (missing / empty / unreadable).
2. **Source path(s) exist and are readable.** Every supplied source path
   resolves and is non-empty.

There is **no** non-empty-diff check and **no** File-Structure /
Acceptance-table requirement. If either input is missing or empty, bail with a
clear error. Only when both pass should the comparison begin.

## Comparison pass

For each requirement, decision, or commitment stated in the source(s), classify
how the artifact treats it:

- **honored** — correctly reflected; no finding.
- **missing** — a source requirement/decision the artifact dropped or
  contradicts.
- **misunderstood** — implemented but with a silent deviation (different shape,
  scope, or framing than the source decided) that is likely unintentional or
  unconfirmed.
- **extra (scope creep)** — the artifact introduces something the source did not
  decide and that materially changes scope.

Quote the source verbatim with a `<file>:§section` reference (cite by
section/heading or verbatim quote — never by line number, since line numbers
drift as documents are edited).

### Second comparison unit: prose vs CODE (required)

The classification above compares prose to prose. That cannot catch an artifact
that is wrong about the code. **For every requirement naming a field, struct,
column, table, RPC parameter, config key, or stored value, open the actual
definition at the authored-against SHA and diff the claim against it.**

Do not sample — **enumerate every such requirement** and record the satisfied
ones too, with the task that satisfies them. A map that lists only holes cannot
tell the reader what is safe to build on.

Three questions per requirement:

1. Is there a task for it?
2. Does the artifact include **every step** needed to make it true — **including
   creating substrate that does not exist yet**?
3. Would anything **fail** if it regressed?

**Verdicts:** `SATISFIED` · `PARTIAL` · `MISSING-STEP` · `NOT-ADDRESSED`.

🔴 **`IMPOSSIBLE` is not a verdict and must never be reported.** If the struct
lacks the field or the table lacks the column, that is a **MISSING-STEP in the
artifact — never a defect in the source.** The source is owner-ruled; the plan
is what is incomplete. Reporting `IMPOSSIBLE` points the next reader at scoping
down the spec, which is backwards.

**Callers must supply the code side.** If the invocation supplies only prose
sources, report it as a `BLOCKING` finding rather than silently running
prose-only — a conformance pass that never opened a source file should not
read as clean.

### Third comparison unit: Primitive Ledger (required when hot-root I/O/SQL is present)

For every I/O or SQL operation the code side introduces under a hot root
(`Handle*`/tick/sweeper/`SyncApplier`/boot — see `.thrum/hotpath-gate.json`'s
`lenses.existing_primitive_bypass.hot_root_indicators`), treat the implementer's Primitive Ledger row itself as
a requirement to be verified, exactly like the field/struct/column checks
above: raw op -> callee package searched -> primitive adopted (or none exists
and a bounded cost formula at production scale).

**Verdicts (same taxonomy as above):** `SATISFIED` — a valid ledger row exists
for the op and, if a primitive is named as adopted, it is actually used at the
cited call site. `PARTIAL` — a ledger row exists but is incomplete or
unverified (e.g. a "none exists" claim whose cost formula uses a test-fixture
number instead of production scale). `MISSING-STEP` — the op was introduced
under a hot root and no ledger row accounts for it. `NOT-ADDRESSED` — not
applicable to this artifact (no hot-root I/O/SQL was added).

## Output format

Findings go to stdout in this exact shape so the caller can consolidate the
dual-review batch without reformatting.

```markdown
## Verify-Against-Source Findings

- **Artifact:** <path>
- **Source(s):** <path[, path...]>
- **Summary:** <N> BLOCKING, <N> IMPORTANT, <N> MINOR

---

### BLOCKING #1 — <short descriptor>

- **Source reference:** <source file>:§<section> — "<verbatim requirement>"
- **Artifact state:** <artifact section> or "absent"
- **Classification:** missing | misunderstood | extra
- **Why it matters:** <link back to the source decision / locked invariant>
- **Suggested resolution:** <add the missing content, reconcile the deviation,
  or flag for the caller>

### IMPORTANT #1 — …

### MINOR #1 — …
```

Every finding must include all five fields. If there are no findings in a
severity bucket, omit that bucket entirely — do not write "### BLOCKING #0 —
none".

## Severity criteria

- **BLOCKING** — a locked source decision is dropped or contradicted. Must be
  fixed (or explicitly overridden) before the artifact propagates downstream.
  Example: the brainstorm's Decision Summary locked "X", the spec says "not X"
  or omits X entirely.
- **IMPORTANT** — a source decision is honored but with a silent deviation
  (different shape/scope/wording) that is probably intentional but unconfirmed,
  OR a partially-honored decision. Should be reconciled or explicitly
  acknowledged. Also: material additions the source never decided (scope creep
  the caller should review).
- **MINOR** — citation drift, wording mismatch, or a stylistic deviation that
  does not change meaning.

When choosing between BLOCKING and IMPORTANT, apply the test: _would a reader
who trusts the source be surprised by this?_ BLOCKING = yes, definitely;
IMPORTANT = maybe, needs explanation.

- **FEASIBILITY** — a requirement IS present in the source (honored in intent),
  but the reviewer judges it too hard, too risky, or impractical to implement
  as specified. This is a distinct routing signal, NOT a synonym for BLOCKING:
  a BLOCKING finding says "the artifact dropped or contradicted a locked
  decision"; a FEASIBILITY finding says "the artifact kept the decision, but
  implementing it as written may not be achievable." Do not fold a
  FEASIBILITY finding inline into the next revision as a silent scope cut —
  per `coordinator-running-brainstorm-cycles/SKILL.md` § Loop semantics, it
  MUST escalate to the coordinator/intent-owner for an explicit keep/cut/weaken
  ruling; only BLOCKING/IMPORTANT/MINOR findings are the researcher's to
  resolve inline.

## Invariant: stdout only, no inline edits

Findings go to stdout only. Do NOT:

- Create TodoWrite entries, beads issues, or worklog files inline —
  consolidation into the dual-review batch is the caller's job.
- Edit the artifact or the source in response to findings — that is the author's
  next step after receiving the consolidated review.
- Modify git state (no commits, no stashes, no checkouts).

The skill reports; the caller consolidates; the author fixes. Keep those three
roles separate or the dual-review batch stops composing cleanly with the
prose-quality reviewer.

## Scope discipline

This skill has ONE job: does the artifact honor its source?

It does NOT:

- **Judge prose quality** — internal consistency, clarity, ambiguity, gaps, and
  contradiction are the prose-quality reviewer's job (the parallel axis), not
  this skill's.
- **Review the source itself** — if the source is wrong, that is a separate
  workflow (re-open the prior stage's review).
- **Review code** — that is `verify-against-plan` (code vs plan) and
  `feature-dev:code-reviewer` (code quality).

If a finding would belong in any of the above categories, omit it from
verify-against-source output. The caller picks up quality gaps via the parallel
prose-quality reviewer.

## Integration

When an author pushes back on a finding from this skill, apply the
pushback-and-verify protocol from
`~/.claude/CLAUDE.md § Verification Discipline` — re-read the cited source at
the cited section, confirm the quoted requirement is verbatim, and confirm the
artifact-state claim is accurate. Findings that don't survive that check must be
withdrawn or downgraded before the caller consolidates the dual-review batch.
Trace-corrections from the author are welcome signal, not insubordination.
