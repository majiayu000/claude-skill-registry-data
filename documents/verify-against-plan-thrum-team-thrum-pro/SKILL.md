---
name: verify-against-plan
description: "Use after implementation is complete to verify the code covers every requirement from the plan / design spec - runs alongside code-review as the second pass in the Code Review Protocol. Takes an optional design= input so requirements that only the design doc states are checked too. Outputs structured findings - missing scope, unmet acceptance criteria, silent deviations from the spec, newly-introduced surprises."
---

# Verify Against Plan

## Inputs

Two inputs are required and one is optional. Missing a required input is a
pre-flight bail.

### 1. Plan or spec path (required)

A markdown plan or spec file — the authoritative reference the implementation is
checked against.

- Preferred: `dev-docs/plans/YYYY-MM-DD-<topic>-plan.md` (produced by
  `superpowers:writing-plans`)
- Fallback: `dev-docs/specs/YYYY-MM-DD-<topic>-design.md` if no plan exists

If both exist, prefer the plan — plans are tighter and already contain the
file-structure and acceptance-criteria anchors the skill compares against.

### 2. Implementation scope (required; one of three forms)

- **Branch name** — compare branch `HEAD` vs. merge-base with `main` (the common
  case). E.g. `feat/verify-against-plan`.
- **Commit range** — `start..end` for custom ranges. E.g. `d4943ce5..HEAD`.
- **Worktree path** — infer the branch and diff from the worktree's current
  state. E.g. `<workspace>/thrum/plugin-skills-slate`.

### 3. Design doc path (optional): `design=<path>`

A markdown design doc or spec the implementation must also honour. The plan
stays the authoritative anchor; the design is a second source of requirements.
Omit it and the skill behaves exactly as before (plan only). When supplied, the
skill also runs the **Design-doc pass** below.

Pass it when the plan implements all or part of a design: `design=<absolute path to the design spec>`. A path that is
missing, empty or unreadable is a pre-flight bail (check 1b), never a silent skip.

### Context-inferred defaults

When the caller supplies no explicit scope, infer:

- **Branch** from `git rev-parse --abbrev-ref HEAD`
- **File scope** from the plan's **File Structure** table — only files the plan
  claims to touch are in scope for verification

### Invocation examples

**Explicit args:**

```text
/verify-against-plan plan=dev-docs/plans/YYYY-MM-DD-topic-plan.md branch=feat/plugin-skills-slate
```

**With a design doc (requirements only the design states are checked too):**

```text
/verify-against-plan plan=<plan file> design=<design file> branch=feat/plugin-skills-slate
```

**Context-inferred (from current worktree):**

```text
/verify-against-plan plan=dev-docs/plans/YYYY-MM-DD-topic-plan.md
```

The second form uses the current branch as the implementation scope.

## Pre-flight checks

Before producing any findings, run these three checks. If any fails, bail with a
clear error — do not proceed with partial inputs.

1. **Plan/spec file exists and is readable.** Verify the path resolves and the
   file is non-empty markdown. Error message on failure names the path and the
   issue (missing / empty / unreadable).

   1b. **Design doc exists and is readable (only when `design=` is supplied).**
   Same shape as check 1: the path resolves and the file is non-empty markdown,
   and the error names the path and the issue. Unlike the plan, a design doc is
   not required to have a File Structure table or an Acceptance section.

2. **Implementation scope resolves to a non-empty diff.** For branch or
   commit-range inputs, `git diff` must produce at least one changed file. An
   empty diff means either the branch is at merge-base or the range is
   mis-specified — either way, there is nothing to verify.

3. **Plan's File Structure and Acceptance/Test-plan sections are extractable.**
   Parse the plan for a `## File Structure` (or equivalent) table and an
   `## Acceptance` / `## Test plan` section. These are the comparison anchors
   for the actual verification pass. If neither is present, bail — a plan with
   no acceptance criteria and no file table cannot be verified against.

4. **Authored-against drift check (informational; does not block on missing stamp).**
   Look for a stamp of this form near the top of the plan:

   Literal example: `**Authored-against:** \`a1b2c3d4e5\` target: \`<merge-target>\``

   Regex: `^\*\*Authored-against:\*\* \`([0-9a-f]+)\` target: \`([^\`]+)\``
   (sha → capture group 1, merge_target → capture group 2)

   (Canonical stamp definition: the /thrum:stamp-protocol skill. The
   stamp follows the same literal `grep -F` / fixed-field-order / case-sensitive /
   ASCII-only convention as the `THRUM-REVIEW` marker — see
   `coordinator-running-brainstorm-cycles` skill § "Footer → commit → stamp".)

   Three distinct outcomes, never conflated:

   - **UNVERIFIABLE — no stamp:** note as informational ("plan predates the
     Authored-against stamp convention, cannot check for drift") and continue
     — do not fail or block; this is an additive check for plans that carry the
     stamp.
   - **UNVERIFIABLE — stamp present, no cited files:** if the stamp is present
     but the plan's File Structure table cites zero files, check for this
     condition BEFORE constructing any `git diff` command — a bare
     `git diff <sha>..<target> --` with an empty pathspec produces a FULL-REPO
     diff rather than an empty one, which would wrongly land in the NEEDS-RECHECK
     branch with nothing to re-check. Go straight to reporting UNVERIFIABLE
     without running any diff. Report explicitly: "stamp present but no cited
     files to diff — cannot confirm currency." This is NOT reported as
     VERIFIED-CURRENT.
   - **Stamp found and cited files present:** run
     `git diff <sha>..origin/<merge_target> -- <files from the File Structure table>` (resolve `<merge_target>` through
     its remote-tracking ref, never a bare local branch name — a local branch of the same name can be stale or absent on
     the reader's machine), scoped only to the files the plan cites (never a full-repo diff). Two sub-outcomes:
     - **VERIFIED-CURRENT** — empty diff: report as a FALSIFIABLE NULL: "plan's
       cited files verified CURRENT as of `<merge_target>` — zero drift." (State
       a positive confirmed fact, not "no evidence of problems" — that
       distinction matters.)
     - **NEEDS-RECHECK** — non-empty diff: NOT automatically a blocking failure.
       Files moved since authoring — a signal to re-verify, not proof the plan
       is wrong. Proceed by: (a) listing exactly which cited files moved or were
       deleted/renamed; (b) re-checking every specific plan claim about those
       files (file:line anchors, function names, preconditions asserted); (c)
       assigning severity from THAT re-check, not from the diff being non-empty:
       - **BLOCKING** — only if a specific claim is now demonstrably false (a
         cited anchor rotted; a precondition the plan assumed no longer holds).
         A deleted or renamed cited file is automatically BLOCKING without
         further re-check nuance: the plan asserts the file exists and has
         certain content; a deleted file can never satisfy that assertion.
         (This routing — deleted/renamed cited file → NEEDS-RECHECK → BLOCKING
         — is intentional; future pathspec optimizations must not short-circuit
         past this branch for deleted or renamed files.)
       - **IMPORTANT** — if the cited files moved but every plan claim re-checks
         as accurate: "cited files moved since authoring, re-verified — claims
         still accurate."

5. **Read-time provenance re-derivation (informational; does not block on
   missing stamp).** Runs whenever check 4 found a stamp at all — both the
   "stamp present, no cited files" outcome and the "stamp and cited files
   present" outcome above, since this check only needs the stamp's
   `<sha>`/`<merge_target>`, not the plan's cited-files list. Run the
   ordered, short-circuiting two-check sequence defined canonically in
   `stamp-protocol.md` § "Read-time provenance re-derivation" (SHA-resolves
   first, then merge-status) against the stamp's `<sha>`/`<merge_target>` —
   the exact commands live there as the single source of truth; this section
   states outcomes and severity only:

   - **FABRICATED** — SHA-resolves fails: flag immediately and stop; the
     merge-status check is undefined for a SHA that doesn't exist.
   - **STALE** — SHA-resolves passes AND merge-status shows the SHA has
     already merged into `<merge_target>` AND the plan's own prose still
     describes that SHA's work as open/in-progress/awaiting-a-gate.

   These checks are re-derived at read time, every time this skill runs — not
   cached from a prior verification pass.

6. **Primitive Ledger row present and valid.** If the diff adds I/O or SQL under
   a hot root (`Handle*`/tick/sweeper/`SyncApplier`/boot — see
   `.thrum/hotpath-gate.json`'s `lenses.existing_primitive_bypass.hot_root_indicators`), confirm the implementer's
   report includes a ledger row (raw op -> callee package searched -> primitive
   adopted, or none exists + bounded cost formula at production scale). Absence
   of the row when one was required is a finding. Presence alone is not
   sufficient — verify the claim: if a primitive is named as adopted, confirm it
   is actually used at the cited call site; if "none exists" is claimed, spot-check
   that the callee package was actually searched and the cost formula uses
   realistic production scale, not a test-fixture number.

Only when checks 1–3 (and 1b, when `design=` is supplied) pass should the
comparison pass begin. Checks 4, 5, and 6
run alongside and contribute findings; a missing stamp never blocks, and check 6
only fires when the diff actually touches a hot root.

## Design-doc pass (only when `design=` is supplied)

Runs after the plan comparison and reports on the same scale. It exists because
a design doc can carry a requirement that no plan task mentions, and a plan-only
review can never see that gap.

**1. Extract requirements, mechanically.** Enumerate in DOCUMENT ORDER and number
them R1..Rn, recording `<design file>:<line>` and the verbatim quote for each.
Nothing is extracted by judgment; exactly these rules apply:

- **Section items.** Under any heading whose title contains (case-insensitive)
  `requirement`, `acceptance`, `success criteria`, `invariant`, `constraint`,
  `non-goal` or `out of scope`, EVERY bullet, numbered item or table row is one
  requirement. The section runs until the next heading of the same or a higher
  level. A nested sub-bullet is its own requirement only if it carries its own
  MUST/SHALL; otherwise it belongs to its parent item.
- **Standalone MUST sentences.** Outside those sections, every sentence that
  contains `MUST`, `MUST NOT`, `SHALL` or `SHALL NOT` in capitals is one
  requirement.
- **Non-goals.** Items under `non-goal` / `out of scope` headings are NEGATIVE
  requirements: the diff must not implement them.
- **Skipped, exactly:** everything else — background, motivation, alternatives
  considered, open questions, examples, and lowercase "must"/"shall"/"should"
  prose.

If the design has no extracted requirement, say so in one informational line
("design supplied but no extractable requirements") and continue plan-only;
never report that as design coverage. Let N be the number extracted.

**2. Scope them, mechanically.** A requirement Rk is CHECKED if and only if
EITHER of these holds; otherwise it is OUTSIDE:

- **(a) Name match.** Build the set of names from (i) every path segment and
  backticked token in the plan's File Structure table and (ii) every path
  segment of the diff's changed paths and every identifier on its added or
  removed lines. Drop generic names (`internal`, `src`, `cmd`, `pkg`, `lib`,
  `docs`, `test`, `tests`, `main`, `index`, `util`, `utils`, `common`) and names
  shorter than 4 characters. Rk is CHECKED when its text contains any remaining
  name as a whole word, case-insensitively (`export` matches `export/handler.go`;
  it does not match `exports`).
- **(b) Cited heading.** Rk sits under a design heading whose exact title also
  appears verbatim in the plan.

Requirements that are OUTSIDE are never flagged; they are counted so silence
cannot pass for coverage, and C + O must equal N:

```text
**Design scope:** <N> extracted: <C> checked, <O> outside this plan's scope, not checked
```

A checked Rk that the plan explicitly defers or excludes is not a finding; cite
the plan's exclusion instead.

**3. Compare.** Each checked Rk is MET, ABSENT or DEVIATED against the diff and
the branch-HEAD code (a requirement already satisfied by unchanged code is MET;
cite where). An Rk that a plan item also covers is reported once, under the plan
finding.

**4. Report.** Same four fields and the same BLOCKING / IMPORTANT / MINOR
buckets; the first field is labelled `Design reference` instead of
`Plan reference`, so consolidation is unchanged:

```markdown
### BLOCKING #2 — <short descriptor>

- **Design reference:** <design file>:<line> — "<verbatim requirement>"
- **Implementation state:** <code path>:<line> or "absent"
- **Why it matters:** <the design requirement or invariant this ties back to>
- **Suggested resolution:** <add the missing code, or flag the design/plan gap for the coordinator>
```

Severity: an unmet MUST, acceptance criterion or stated invariant is BLOCKING; a
silent deviation (different name, shape or behavior) or a violated non-goal is
IMPORTANT; a documentation or reference gap is MINOR.

**Example.** Design line 9 reads "The export endpoint MUST reject request bodies
over 1 MiB with HTTP 413." The plan lists only the audit-log task and its File
Structure names `export/handler.go` and `audit/audit.go`; the diff adds only
audit logging. Plan-only, nothing is flagged. With `design=`, that requirement is
extracted (it sits under a Requirements heading), CHECKED by name match (`export`
is a name from the File Structure and the diff), ABSENT from the code, and
reported as a BLOCKING finding quoting design line 9 with implementation state
`absent`. A second requirement in the same design, "The billing service MUST
retry failed charges three times", contains no name from the plan or the diff, so
it is OUTSIDE: counted in the `Design scope` line, never flagged, even though it
is a MUST that the diff does not implement.

## Output format

Findings go to stdout in this exact shape so the coordinator can consolidate the
dual-review batch without reformatting.

```markdown
## Verify-Against-Plan Findings

**Plan:** <path> **Implementation:** <branch> (<N> commits, <M> files changed)
**Design:** <path> (only when design= was supplied)
**Design scope:** <N> extracted: <C> checked, <O> outside this plan's scope, not checked (only when design= was supplied)
**Summary:** <N> BLOCKING, <N> IMPORTANT, <N> MINOR

---

### BLOCKING #1 — <short descriptor>

- **Plan reference:** <plan file>:<line> — "<verbatim requirement>"
- **Implementation state:** <code path>:<line> or "absent"
- **Why it matters:** <link back to acceptance criterion / invariant>
- **Suggested resolution:** <add code, update plan, or flag for coordinator>

### IMPORTANT #1 — …

### MINOR #1 — …
```

Every finding must include all four fields:

- **Plan reference** — exact `<file>:<line>` with the verbatim quote from the
  plan. No paraphrase.
- **Implementation state** — what's in the code now, or the literal string
  `absent` if the requirement has no corresponding code.
- **Why it matters** — the acceptance criterion or invariant this finding ties
  back to. Prevents findings drifting into style opinions.
- **Suggested resolution** — concrete next action (add the missing code, update
  the plan, or flag for coordinator judgment). "Review this" is not a
  resolution.

If there are no findings in a severity bucket, omit that bucket entirely — do
not write "### BLOCKING #0 — none".

## Severity criteria

- **BLOCKING** — a named acceptance criterion is unmet, or the implementation
  contradicts a stated invariant. Must be fixed before merge. Example: plan's
  File Structure claims `<path/to/file>` exists but no such file was
  added; plan's Test plan names a test that isn't present in the diff. Also:
  drift check found that a specific plan claim (file:line anchor, function name,
  or precondition) is now demonstrably false after cited files moved.
- **IMPORTANT** — a plan requirement is implemented but with silent deviation
  (different file path, different function name, different public shape) that is
  likely intentional but unverified. Should be fixed, or the deviation
  explicitly acknowledged by the implementer. Example: plan says
  `ResolveAgentID()` but code has `GetAgentID()` with the same behavior —
  probably fine, but nobody said so. Also: files or behavior present in the
  implementation diff with no corresponding entry in the plan's File Structure
  table — unplanned additions the coordinator should review for scope creep.
  Also: drift check found that cited files moved since authoring but all plan
  claims re-checked as accurate ("cited files moved since authoring,
  re-verified — claims still accurate").
- **MINOR** — missing documentation reference, commit-message format drift, or
  stylistic plan deviation that does not affect behavior. Example: plan calls
  for `Refs thrum-abc.3` in commit body, commit just has the title.

Drift-check-specific outcomes (step 4) and their severity mapping:

- **UNVERIFIABLE** — no stamp present, OR stamp present but plan cites zero
  files. Reported as informational; never promoted to VERIFIED-CURRENT. No
  bucket entry.
- **VERIFIED-CURRENT** — stamp present, at least one cited file, and the scoped
  diff against those files is empty. Reported as a FALSIFIABLE NULL, not a
  severity finding. No bucket entry.
- **NEEDS-RECHECK** — stamp present, at least one cited file, and the scoped
  diff is non-empty. Resolves to one of two severities after re-check:
  - **IMPORTANT** (NEEDS-RECHECK → claims-hold): cited files moved but every
    plan claim re-verified accurate ("cited files moved since authoring,
    re-verified — claims still accurate").
  - **BLOCKING** (NEEDS-RECHECK → claim-false): a specific plan claim is now
    demonstrably false after re-check. A deleted or renamed cited file is
    automatically BLOCKING — the plan asserts the file exists; deletion proves
    the assertion false without further nuance.

Read-time provenance re-derivation (check 5) severity mapping:

- **FABRICATED** — SHA-resolves failed: the stamped `<sha>` does not exist in
  the repo. **BLOCKING** — the stamp itself is untrustworthy; every downstream
  drift claim (check 4) built on this SHA is unverifiable.
- **STALE** — SHA-resolves passed, merge-status shows the SHA has already
  merged into `<merge_target>`, but the plan's prose still narrates that work
  as open/in-progress/awaiting-a-gate. **IMPORTANT** — the plan's narrative is
  out of date; the described gate has already resolved (or never needed to
  block), which the coordinator should reconcile before acting on the plan's
  stated pending state.

Primitive Ledger check (check 6) severity mapping:

- **BLOCKING** — the hot-root diff genuinely bypasses an available primitive
  (a primitive exists, was not adopted, and no ledger row accounts for the
  bypass) — a raw op standing where a callee-package primitive was reachable
  and unlogged. Also BLOCKING: a ledger row is present but the "adopted"
  primitive is not actually used at the cited call site, or a "none exists"
  claim is contradicted by an available primitive the implementer's own
  ledger row claims to have searched for and missed.
- **IMPORTANT** — the ledger row is missing but the raw op itself is
  harmless (no primitive exists, cost formula would clear at production
  scale) — the accounting step was skipped, not the substance. Also
  IMPORTANT: a "none exists" claim whose cost formula uses a test-fixture
  number instead of realistic production scale, pending a re-derived figure.

When choosing between BLOCKING and IMPORTANT, apply the test: _would a reader of
the merged code be surprised by this?_ BLOCKING = yes, definitely; IMPORTANT =
maybe, needs explanation.

## Invariant: stdout only, no inline edits

Findings go to stdout only. Do NOT:

- Create TodoWrite entries, beads issues, or worklog files inline —
  consolidation into the dual-review batch is the coordinator's job.
- Edit the code or the plan in response to findings — that is the implementer's
  next step after receiving the consolidated review.
- Modify git state (no commits, no stashes, no checkouts).

The skill reports; the coordinator decides; the implementer fixes. Keep those
three roles separate or the dual-review batch stops composing cleanly with
`feature-dev:code-reviewer`.

## Integration

When an implementer pushes back on a finding from this skill, apply the
pushback-and-verify protocol from
`~/.claude/CLAUDE.md § Verification Discipline` — re-read the cited file at the
cited lines, confirm the quoted plan requirement is verbatim, and confirm the
implementation state claim is accurate. Findings that don't survive that check
must be withdrawn or downgraded before the coordinator consolidates the
dual-review batch. Trace-corrections from the implementer are welcome signal,
not insubordination.

## Scope discipline

This skill has ONE job: does the code match what the plan (and the design doc,
when `design=` is supplied) said it would do?

It does NOT:

- **Judge code quality** — that's `feature-dev:code-reviewer`. Error handling,
  idioms, dead code, security patterns — not this skill's problem.
- **Perform security review** — that's `security-review`. SQL injection, XSS,
  auth bypass, secret handling — not this skill's problem.
- **Analyze test coverage** — coverage tools exist for that; this skill reports
  whether the plan's named test paths exist and pass, not whether they hit every
  branch.
- **Review the plan itself** — pre-implementation plan review is handled by
  `superpowers:writing-plans` (built-in reviewer). If the plan is wrong, that's
  a separate workflow. The same holds for the design doc: it is a source to
  check the code against, not something this skill critiques.

If a finding would belong in any of the above categories, omit it from
verify-against-plan output. Coordinator will pick up quality / security /
coverage gaps via the other skills running in parallel.
