---
name: to-plan
description: Synthesize a decisions record and the current codebase into a
  pure implementation plan written to disk. Use when the user asks to turn a
  plan, spec, or set of decisions into an implementation plan, or says
  "to-plan this", "write a plan", "make a plan from this".
disable-model-invocation: true
license: MIT
metadata:
  version: "1.0.0"
  author: "bitcoin21ideas"
---

# to-plan

Turn a settled decisions record into a **pure implementation plan** on disk: file paths, modules, sequencing, verification. The output is sized and structured to survive adversarial critique by `plan-clash`.

Every claim you write must be grounded in the real codebase or in the decisions context you were given. Write only what you can stand behind.

## 1. Collect the decisions context

Accept the input from whichever source is available, in this order of preference:

- the **live conversation** — if any planning discussion just ran in this session, read it directly;
- a **`.decisions.md` file** — if the user gives a path, read it;
- **pasted prose** — if the user pastes a plan or set of decisions, use that.

## 2. Explore the repo

Read the codebase to establish:

- existing modules and files relevant to the plan, by **repo-relative path**;
- patterns to follow — naming, structure, conventions;
- the **test directory layout, the test command, and 1–2 exemplar test files** you will anchor every slice's verification to;
- any ADRs or architectural decisions already on record.

Verify the claims in the decisions context against the real code. Where the context contradicts what the repo actually shows, **note the contradiction** — do not silently paper over it.

## 3. Confirm module boundaries — the gate

Before writing anything, present the proposed architecture and stop:

- which modules will be built or modified;
- the **interface** (the test surface) for each;
- the key integration points and seams.

Then ask:

**"Do these module boundaries look right before I write the plan?"**

Do not proceed to writing until the user confirms or redirects. A wrong boundary here
propagates into every slice and then into `plan-clash`'s critique — one cheap
confirmation prevents expensive downstream correction.

## 4. Write the plan

Write a single Markdown file to disk at `./<slug>.plan.md`, where `<slug>` is derived
from the feature name. Use this template exactly:

```markdown
---
plan: <slug>
from-decisions: ./<slug>.decisions.md   # omit this line if no decisions file exists
code-root: <repo-relative-path> @ <git-sha>
---

# <slug> — implementation plan

## 1. Overview
1–2 sentences: the user-visible behavior delivered, and how to observe it.

## 2. Settled decisions
Each decision from the decisions record, one line each, with a one-line rationale.
List intentionally-deferred items explicitly, prefixed `deferred:`. This tells
plan-clash's critic these trade-offs are already settled, so it does not re-open
them as findings.

## 3. Context & orientation
Current state of the relevant code: existing modules with repo-relative paths,
patterns to follow, test file locations, the test command, and 1–2 exemplar test
file references. This proves the repo was read and establishes the vocabulary the
slices inherit.

## 4. Architecture
Modules and interfaces to build or modify. For each: repo-relative path +
fully-qualified symbol name. Integration points and seams. No code bodies.

## 5. Implementation slices
2–6 ordered vertical tracer bullets. **Each slice is one session gate.** Size each
slice to complete comfortably within a single focused session (~150k tokens of
execution headroom). If a slice touches more than 4–5 files or covers multiple
distinct behaviors, split it.

For each slice:

### Slice N — <title>
- **What:** the end-to-end behavior delivered, through every layer.
- **Files & symbols:** repo-relative paths + fully-qualified names; where any new
  files go.
- **Depends on:** slice ids, or `none`.
- **Done when:** observable behavior + the exact test(s), anchored to the repo's
  test pattern (a new test that fails before the change and passes after) + the
  exact command + expected output. **Verify this gate fully before starting the
  next slice.**

## 6. End-to-end verification
A single check proving the whole feature works: exact command, expected observable
output.

## 7. Out of scope
Explicit negative boundaries — what this plan deliberately does NOT cover.

## 8. Risks & open questions
Known unknowns. Flag any external claim that cannot be verified from the repo as
"unverified — cannot inspect" (this mirrors plan-clash's critic language, so it does
not resurface as a surprise finding).

## 9. Idempotence & recovery   <!-- INCLUDE ONLY for destructive/migrational steps -->
Retry-safe paths, rollback, backups. Omit this section entirely for additive-only
plans.
```

## 5. Confirm the plan

After writing, tell the user:

- the file path it landed at;
- how many slices, and the total scope;
- whether any deferred items from the decisions record should be resolved before
  `plan-clash` is run.

Close with:

**"Ready to harden with plan-clash, or do you want to adjust the plan first?"**

## Hard rules

- **Never interview the user.** Synthesize from the input. Reserve questions for genuine gaps only the user can fill: intent, priority, business constraints.
- **Never implement anything.** The plan is the deliverable.
- **Never mutate the original decisions file** if one was provided.
- **Every file path in the plan must exist in the repo, or be explicitly marked as a new file to create.** Invented paths are P0 findings for plan-clash.
- **No code snippets or function bodies** — interfaces and signatures only.

## Where this fits

`pressure-test` (elicit) → **`to-plan`** (synthesize) → `plan-clash` (harden).
