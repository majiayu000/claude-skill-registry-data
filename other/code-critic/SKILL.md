---
name: code-critic
description: >
  Code review checklist and coding standards, extended per project by
  whatever file AGENTS.md's Review & Planning Guidance section names
  (defaulting to docs/agent-rules/code-critic.md). Invoked as /code-critic
  for an ad-hoc review, or applied by the code-critic sub-agent in the
  /feature workflow. (Named code-critic so it does not shadow Claude Code's
  bundled code-review skill.)
---

# /code-critic — Code Review

Apply this skill to review code changes against project standards.

---

## Stance

Treat the implementation as a hypothesis under attack. Your default
assumption is that something is wrong; your job is to find what.

Confirmation bias is the dominant failure mode of AI code review — guard
against it by actively trying to disconfirm the implementation rather than
verifying that it looks reasonable. If you cannot find a fault after
genuine effort, that is itself a finding worth stating explicitly (see the
Output Format section).

---

## Before Reviewing

### Selecting the diff

In the `/feature` workflow the implementation is committed before review, so
a bare `git diff` (working tree) shows nothing — review the branch's
committed changes against its base, the default branch named in `AGENTS.md`
→ *Commands*: `git diff <default-branch>...HEAD` (or
`git log -p <default-branch>..HEAD`). Invoked ad-hoc on uncommitted work,
review the working-tree diff instead. If unsure what changed, check
`git status` and `git log --oneline` first.

Note for ad-hoc use: the push gate records a commit SHA
(`scripts/review-ok.sh`), so a review meant to unlock a push must cover the
committed state — commit first, then review.

### Architecture Decision Records

Check if a `docs/adr/` directory exists. If it does, list the ADRs you read by
number in the review output. If none seemed relevant
to the diff, say so explicitly — silence is not acceptable, since it is
indistinguishable from skipping the step.

If the diff contradicts an ADR, quote the contradicting ADR clause and the
offending diff line, and flag it as `FAIL`.

### Implementation Plan

If plan text was provided (inline in the prompt, or via a file path), use it
before reviewing. Use it as follows:
- **Approval Summary / Acceptance Criteria**: the human-approved contract.
  Verify every `AC-<slug>-n` has a committed test (via the `[AC-<slug>-n]`
  tags in Test Strategy) that would fail if the criterion were broken — a
  criterion without one is `FAIL`.
- **Contract** section (if present): cross-check the diff's routes, form
  fields/params, response shapes, error rendering, and schema changes
  against it. An undiscussed deviation from the approved Contract is `FAIL`.
- **Types anywhere in the plan** (Contract, Approach, Requirements — even
  when Contract is "None"): types (nullable vs non-null, optional vs
  required) are part of the contract, not just names and presence.
  Explicitly diff every parameter/field type the plan states against the
  diff's actual signature; do not infer the type from the inputs the tests
  use. A non-nullable parameter standing in for a plan-specified nullable
  one is `FAIL` even if every test passes, since a real caller carrying the
  untested value (e.g. an actual `null`) cannot satisfy the signature. The
  reverse (nullable/optional where the plan says non-null/required) is
  `FAIL` too, unless the review input documents an approved deviation.
- **Requirements** section: the source of truth for what should have been built —
  used to verify Plan Compliance and that all specified edge cases are handled.
- **Approach** section: the agreed implementation strategy — used to verify the
  code follows the intended design rather than an ad-hoc alternative.
- **Edge Cases** section: the enumerated scenarios that must be handled.
  Verify every `EDGE-<slug>-n` has a committed test (via the `[EDGE-<slug>-n]`
  tags in Test Strategy) that would fail if the handling strategy were
  broken — an edge case without one is `FAIL`.
- **Test Strategy** section: the agreed test coverage — cross-reference against
  the actual tests written.
- **Files** section: the planned file manifest — cross-check against the diff. A
  file in the diff that is not listed here (or listed but left untouched) is an
  undiscussed change; flag the mismatch and judge whether it is in scope.
- **Out of Scope** section: the explicit boundary — do NOT flag as missing
  anything listed here, and DO flag as scope creep any code that strays into it.

If no plan was provided, skip the Plan Compliance checklist section entirely.

**Test evidence.** The review verifies coverage statically; whether the
suite actually ran and passed on the reviewed state is separate evidence.
In the `/feature` workflow that evidence is passed in (the summary of the
latest full test-suite run). Treat that summary as a record of the run, not
independent proof — it is produced by the implementing agent, and this
review has no independent way to confirm it (whether the project's own CI
provides that is outside this skill's scope). If no evidence was provided
and you cannot (or may not) run the suite yourself, do not assume it is
green — raise an Open Question: "no evidence the test suite ran on the
reviewed state".

When flagging a plan compliance issue, **quote the exact line from the plan**
that the diff violates, alongside the diff line that violates it. Paraphrasing
the plan is not enough — the developer needs to see the literal mismatch.

### Reading Beyond the Diff

You may read any file in the repository. The diff is the unit under review,
but surrounding code, tests, configuration, and migrations are fair context —
and often necessary to judge whether the change is correct. Some
project-specific rules below may explicitly require it (cross-referencing a
sibling file, checking that a registration or annotation is present).

---

## Coding Standards

### Single Responsibility

**Functions:** A function should do one thing. If a function contains a
conditional branch that handles a fundamentally different concern (e.g. an
admin path bolted onto a regular-user path, or a parsing path inside a
persistence call), flag it. Severity:
- New function introduced with mixed concerns → `FAIL`
- Existing function extended with a clearly unrelated branch → `FAIL`
- Borderline case where extraction would hurt readability → `NEEDS_DECISION`

**Classes:** A class has too many responsibilities if you can identify more than
one independent reason it would need to change.

When reviewing new code that touches an existing class:
- If the new code **introduces** a class with too many responsibilities → `FAIL`
- If the new code **significantly worsens** an existing violation (e.g., adding
  several more methods to an already oversized class) → `FAIL`
- If the new code **extends** an already-oversized class without making it
  meaningfully worse → `NEEDS_DECISION`: flag the pre-existing debt and let the
  developer decide whether to refactor now, file tech debt, or accept it

### Error Handling
- In business logic, never use generic catch-all error handling. At process
  boundaries (top-level controllers, scheduled jobs, async task entry points)
  a catch-all that logs and translates to a domain error is acceptable —
  judge by *where* the catch lives, not just *what* it catches.
- Every error must include context about what operation failed and why.
- Errors in critical paths must be logged with structured fields.

### Naming
- Functions should describe what they do: `calculateShippingCost`, not `calc` or
  `process`.
- Boolean variables/functions should read as questions: `isValid`, `hasPermission`.

### Tests

You are responsible for both **test quality** (structure, naming, pattern) AND
**test completeness** (coverage of the spec AND beyond). The `/adversarial-qa` skill is
purely exploratory/adversarial in a running browser — it does not verify that
the committed tests cover the plan, so that responsibility lives here.

**Quality:**
- Every public function with non-trivial behaviour must have tests covering
  the happy path AND edge cases. Trivial delegators, generated code, plain
  data classes, and pure getters are exempt — but if you exempt a function,
  state which one and why in the review.
- Test names must describe the scenario: `test_order_fails_when_inventory_insufficient`,
  not `test_order_2`.
- Use the Given-When-Then pattern.
- Never test implementation details — test behaviour.
- The same disconfirmation stance applies to the tests themselves: check
  what a test's assertion actually compares, not what its name or comment
  claims — a test that would pass regardless of correctness (e.g. an
  expression compared to itself) proves nothing.
- Tests that encode the plan's Test Strategy (the `[AC-<slug>-n]`-tagged ones
  especially) are the contract, not implementation detail: a diff that
  weakens, loosens, or deletes one so the suite passes is `FAIL` unless the
  review input documents an approved plan deviation covering it.

**Completeness — against the plan:**
- Every Requirement and every enumerated Edge Case in the plan must have at
  least one test that would fail if the requirement were broken.
- Every branch introduced in the implementation (error paths, validation
  failures, authorization denials, empty/null handling) must be exercised.

**Completeness — beyond the plan (critical analysis):**

Read the implementation diff and actively try to break it. You are doing
this through static reading, not by running the code — for each branch in
the diff, mentally construct an input or sequence of events that would
exercise it, then ask whether a test covers that input. The plan is a
starting point, not a ceiling. For each category below, ask "given the
actual code in the diff, what would I do to make this fail?":

- **Implicit branches**: `if`, `when`/`switch`, `?:`, early returns, exception
  handlers introduced by the implementation but not called out in the plan.
  Each one is a behaviour worth testing.
- **Boundary values**: 0, 1, max, min, off-by-one, empty collections,
  single-element collections, exactly-at-limit vs just-over-limit. Plans
  rarely enumerate these exhaustively.
- **Input shapes the plan didn't mention**: null, blank strings, whitespace,
  unicode, very long strings, leading/trailing spaces, mixed case, duplicates,
  unsorted input.
- **State and concurrency**: stale reads, double submits, retries on the same
  resource, partial writes, what happens if the operation is invoked twice.
- **External dependency failure modes**: timeouts, 4xx vs 5xx responses,
  malformed payloads, slow responses — wherever the code calls out.
- **Security-adjacent gaps**: authz checks on every entry point, not just the
  one the plan mentioned; injection-shaped inputs on any field that hits a
  query, template, or shell.

If you find a gap of this kind, flag it as `FAIL` (or `NEEDS_DECISION` if it is
genuinely ambiguous whether the case is in scope) with a concrete description
of the missing test, not just "more tests needed".

### Privacy and Data Protection

Prefer build-enforced tests over prose here (same doctrine as the
build-enforced guidance below). Any project holding personal data should
implement these three fitness tests — until they exist, they are backlog
items, not per-PR checklist prose:

1. **Deletion by design** — every table with a user FK either cascades on
   account deletion or appears in an explicit, commented allowlist.
2. **Public-surface whitelist** — the model rendered on public/
   unauthenticated surfaces is a distinct type whose fields are asserted
   against a whitelist, so a sensitive field cannot be added silently. (If
   public pages currently render from the full domain object, that
   restructuring is the prerequisite — worth its own task.)
3. **No personal data in logs** — log statements must not reference
   sensitive/user-content field symbols or contact-detail fields.

For any of these that IS implemented, the reviewer's only duty is the
standard build-enforced check: the diff must not WEAKEN the enforcement
(deleting or disabling the test, adding an unexplained allowlist entry,
restructuring code out of the test's scan scope). A weakened enforcement
is `FAIL`. For any not yet implemented, check the corresponding invariant
by hand only on diffs that touch it (new user-FK tables; public-view
rendering; new/changed log statements).

Prose residue the tests cannot catch (diff-scoped, manual):

- **Indirect serialization into logs** — logging rich objects (`toString()`
  of an entity, dumped request params) that embed personal data. `FAIL`.
- **Personal data in URLs** — emails, phone numbers, or values embedding
  them in query params or path segments; URLs land in access logs and
  browser history. `FAIL`.

Consent, retention, and data-classification rules are deliberately NOT
per-PR review items — they are product flows to be built as tasks and then
protected by tests, not per-diff checklist prose.

---

## Project-Specific Rules

This skill is project-agnostic; each project extends it without editing it.
Check the repo-root `AGENTS.md` (not a module-level one) for a **Review &
Planning Guidance** section. If it has a
"Code review guidance" entry, read the file it names. If `AGENTS.md` has no
such section, or the section exists but has no "Code review guidance"
entry, fall back to checking `docs/agent-rules/code-critic.md` directly. If
an entry names a file that doesn't exist, treat it the same as "no file
found" below, but say so specifically (a named-but-missing file is a broken
pointer worth surfacing, not just an absent extension).

If a file is found, apply every constraint in it alongside the base
standards above: where it states a severity, use it exactly as stated
(including the don't-weaken doctrine for anything it marks as
build-enforced); where it states none — a pre-existing project doc without
this skill's format, such as a style guide, `CONTRIBUTING.md`, or an
engineering handbook — judge severity yourself using this skill's normal
`PASS`/`FAIL`/`NEEDS_DECISION` framework. Either way, treat any PRIVACY
anchors it contains as binding on the privacy rules above (sensitive
categories, public surfaces, existing fitness tests), regardless of
whether the rest of the file follows this skill's structure.

If no file is found either way, proceed with the base standards alone and
say so in the review output (one line) — the gap should be visible, not
silent.

---

## Review Checklist

Review every change against this checklist. For each item, state one of:

- `PASS` — the rule applies to this diff and the diff complies. Cite specific
  diff lines that demonstrate compliance for non-trivial items (test
  coverage, edge cases, error paths, security-adjacent code). Routine
  quality items (naming, readability) need only a brief explanation.
- `PASS (N/A)` — the rule does not apply to this diff (e.g., security checks
  on a CSS-only change). Briefly say why.
- `FAIL` — rule violated, and you can cite the line and the rule that breaks.
  Reserve `FAIL` for findings you are confident in. If unsure, prefer
  `NEEDS_DECISION` or **Open Question** — false `FAIL`s burn developer
  trust faster than missed issues.
- `NEEDS_DECISION` — the correct approach is ambiguous and requires
  developer input. State the options.
- **Open Question** — concerns where the diff *might* be wrong but you
  cannot verify from source alone (depends on runtime config, prod data
  shape, deployment topology, external service behaviour). State the
  question and what evidence would resolve it. Use this freely — it is
  better to surface a hypothesis the developer can dismiss in 10 seconds
  than to stay silent on a real risk.

### Architecture

_If a layer/architecture fitness test enforces boundaries (see the layer
rule in the AI Workflow plugin's own documentation), do NOT re-derive them
by hand — verify only that the diff does not **weaken** it: deleting or
disabling the test, widening a package glob, adding an unexplained
exemption, or moving code out of the scanned layer. A weakened enforcement
is `FAIL`._

- [ ] Changes respect service boundaries and existing ADRs
- [ ] No business logic in infrastructure or API layers
- [ ] No new dependencies introduced without justification

### Plan Compliance _(skip if no plan was provided)_
- [ ] Implementation follows the Approach described in the plan — no undiscussed
  design alternatives introduced
- [ ] All steps in the plan are accounted for in the changes
- [ ] Every acceptance criterion (`AC-<slug>-n`) in the Approval Summary
  maps to a committed test tagged `[AC-<slug>-n]` that would fail if the
  criterion were broken
- [ ] Every edge case (`EDGE-<slug>-n`) in the Edge Cases section maps to a
  committed test tagged `[EDGE-<slug>-n]` that would fail if the handling
  strategy were broken
- [ ] Diff matches the plan's Contract section — routes, fields, response
  shapes, error rendering, schema _(skip if Contract is "None")_
- [ ] Every parameter/field type the plan states anywhere (nullable vs
  non-null, optional vs required) matches the diff's actual signature
- [ ] All requirements from the Requirements section are addressed
- [ ] Files touched in the diff match the plan's Files manifest — no undiscussed
  files (a file in the diff but not in the manifest is an undiscussed change)
- [ ] No code introduced inside the plan's Out of Scope boundary

### Code Quality
- [ ] Every function has a single responsibility
- [ ] Classes have a single reason to change — new classes assessed per the Single
  Responsibility standard above; existing classes flagged if the change worsens
  the violation
- [ ] Error handling is specific, not generic catch-all
- [ ] Code is readable — a new team member could follow the logic without extra context
- [ ] No implicit assumptions that should be explicit (add comments or types)

### Edge Cases
- [ ] All edge cases identified in the plan (`EDGE-<slug>-n`) are explicitly
  handled _(if plan provided)_
- [ ] Null/empty/zero/negative inputs are handled where applicable
- [ ] Concurrent access scenarios are considered where applicable
- [ ] Failure modes of external dependencies are handled (timeouts, retries, fallbacks)

### Tests
- [ ] Tests cover the happy path
- [ ] Tests cover every Requirement and Edge Case identified in the plan _(if plan provided)_
- [ ] Every branch introduced by the implementation (error paths, validation
  failures, authorization denials, null/empty handling) is exercised
- [ ] Boundary values are tested where applicable (0, 1, max, min,
  off-by-one, empty/single-element collections, exactly-at-limit vs
  just-over-limit)
- [ ] Implicit input shapes are covered where applicable (null, blank,
  whitespace, unicode, very long, duplicates, mixed case)
- [ ] State/concurrency scenarios are covered where applicable (double
  submit, retry, partial writes, idempotency)
- [ ] External dependency failure modes are covered where the code calls
  out (timeouts, 4xx/5xx, malformed responses)
- [ ] Critical analysis performed: list any plausible scenarios the plan did
  not enumerate that should also be tested, and flag missing ones as `FAIL`
- [ ] Test names describe the scenario being tested
- [ ] Tests follow the Given-When-Then pattern
- [ ] No tests that only verify implementation details
- [ ] No tautological assertions — each test's assertion compares independent
  expressions and could fail if the behaviour were broken

### Project-Specific
- [ ] Every applicable item from the project's review guidance (via
  `AGENTS.md`'s Review & Planning Guidance section, or
  `docs/agent-rules/code-critic.md` if unspecified) evaluated — or its
  absence stated as one line in the output

### Privacy and Data Protection
- [ ] Privacy fitness tests not weakened — no deleted/disabled test, no
  unexplained allowlist entry, no code restructured out of scan scope
- [ ] Invariants without a backing test yet, checked by hand where the diff
  touches them: deletion-by-design (new user-FK tables), public-surface
  whitelist (public-view rendering), no personal data in logs (new/changed
  log statements)
- [ ] No indirect serialization of personal data into logs (rich-object
  `toString()`, dumped request params) and no personal data in URLs

### Security (general)
- [ ] No secrets or credentials in code
- [ ] Input validation on all external inputs
- [ ] Authorization checks where required

---

## Output Format

```
### Review Summary
[1-2 sentence overall assessment]

### PASS
- [item]: [explanation; for non-trivial items, cite diff lines like
  src/foo/Bar.ext:42-58]

### PASS (N/A)
- [item]: [why this category does not apply to this diff]

### FAIL
- [item]: [what's wrong, suggested fix, diff line reference]

### NEEDS_DECISION
- [item]: [the ambiguity and the options available]

### Open Questions
- [hypothesis]: [the question you cannot answer from source alone, and the
  evidence that would resolve it — runtime config, prod data, deployment
  topology, external service behaviour]

### ADRs Reviewed
[List ADR numbers you read, or state "none relevant" with one sentence why.]

### Disconfirmation Attempt
[REQUIRED if FAIL and NEEDS_DECISION are both empty]
Describe specifically what you tried in order to find issues — which
inputs you considered, which failure modes you probed, which edge
cases you inspected, which diff sections you examined. A bare
"looks good" or "no issues found" is not acceptable. State the methods
you applied (pre-mortem, boundary probe, dependency-failure probe,
adversarial input probe) and the specific outcomes.
```

If you find any `NEEDS_DECISION` items or **Open Questions**, clearly label
them so the orchestrating agent can surface them to the developer. Do not
make these decisions yourself.

Do NOT modify any code. Output only the review.
