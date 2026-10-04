---
name: plan-review
description: Use when the user asks to review an implementation plan or asks what you think about a plan. Triggered by phrases like "review this plan", "what do you think about this plan", "check this plan", "plan review", "is this plan solid", or when the user links or pastes a plan and wants critique rather than execution.
---

# Plan Review

Announce at start: `Running plan review...`

Review plans like the engineer who has to implement this and will be paged when it fails. A plan
review is not a summary - stress the plan. Treat it as guilty until its contracts, failure coverage,
and scope discipline prove themselves.

A good plan is the simplest thing that satisfies the spec, names what can go wrong, and proves the
contracts hold. Complexity is earned, never assumed: for every non-trivial abstraction, the first
question is whether the spec asked for it or the planner added it.

Judge every planned module against the Four Rules of Simple Design, in priority order - passes
tests, reveals intention, avoids duplication, fewest elements. Failing #4 while satisfying #1–3 is a
YAGNI violation; failing #2 or #3 while claiming #4 is a different problem. Name which one you found.

## Lenses

Work through these in order.

### 0. Source spec alignment

If the plan references an upstream issue, ticket, or spec, fetch and read it first. To find the
tracker, check the repo's `AGENTS.md`/`CLAUDE.md` for a configured project-management system; if none
is configured, ask the user or work from the reference the plan already cites. Judge the plan against
the actual spec, never your interpretation of the task.

Flag: missed acceptance criteria, scope the task never asked for, a different problem being solved,
decisions claimed as settled that the spec does not support.

### 1. Repo rules and architecture

```bash
sed -n '1,220p' AGENTS.md 2>/dev/null
sed -n '1,220p' ~/AGENTS.md 2>/dev/null
```

Follow `AGENTS.md`'s **Context Map** for the areas the plan touches - the architecture index and the
decision log matter most. Read the decision log before calling any structural choice wrong: it
records what breaks if a decision is reversed.

Flag: explicit repo-rule violations, work placed in the wrong app/package/layer, structures that
conflict with current project patterns.

### 2. Codebase reality check

A plan review that doesn't open files is a theoretical exercise. For each planned file or subsystem:
confirm whether it exists, read the module that would change, and search for existing implementations
of the same concept.

Flag: re-creating something that exists, missing an obvious abstraction it should extend, targeting
the wrong file because the architecture settled elsewhere, assuming framework behavior that doesn't
match the current app setup.

### 3. YAGNI and complexity discipline

Every abstraction the spec didn't ask for is a finding.

Flag: abstractions generalizing fewer than 3 existing cases, generalization/extensibility/
configurability the spec did not require, design for out-of-scope future requirements, a new
dependency where the stack already handles it, multi-step architecture where a simpler one satisfies
the spec.

### 4. Contract integrity

For any plan touching more than one layer, inspect the boundary contracts it depends on. Every new
endpoint, job, or write path should name its preconditions (what the caller guarantees),
postconditions (what the callee guarantees on return), and invariants (what stays true throughout).
Unnamed, it is a hope rather than a contract.

Flag: one side of a contract changed without the other, a value assumed configurable that another
layer fixes, ordered behavior (pagination, retries, deduplication) without a tie-break or idempotency
rule, generated artifacts consumed without a refresh step, validation that only proves the build
passed.

### 5. Layer discipline

Flag pure logic mixed with imperative shell: business logic in a controller or route handler,
orchestration inside a domain helper, I/O inside a pure computation, database queries in the
presentation layer. The test: extract the logic from the I/O - does it become trivially
unit-testable? If not, the layering is wrong.

### 6. Security and exposure

Flag: admin/debug/ops endpoints without an explicit auth and authorization step, logging of secrets,
JWTs, headers, or PII, trusted user input at a webhook/callback/internal endpoint, sensitive values in
committed files, plan docs, fixtures, or example curl commands, surfaces opened that should stay
internal.

### 7. Delivery completeness

A complete plan lands safely, not just compiles. Flag missing: tests **and** the failure paths they
cover, env schema updates and downstream rebuilds, migrations, seed impacts, rollback steps,
observability (logs, metrics, error handling), CI/build implications.

### 8. Execution decomposition

Skip when the plan has no Task Ownership table. When it has one, the executing agent will run tasks
concurrently and pick model capability from it, so a wrong entry here becomes a wasted or corrupted
run - treat it as load-bearing, not bookkeeping.

Check independence against the code, not the table's own claims: open the files two supposedly
independent tasks own and confirm neither imports, re-exports, or registers the other's output.
Barrel files, route tables, schema indexes, migration lists, and DI containers are where false
independence hides.

Flag: a file owned by two tasks in the same phase, owned files that contradict the File Map, an
undeclared dependency where one task's text consumes what another produces, a task classified
`mechanical` or `standard` that Key Contracts or the Pre-mortem also names, a `contract` task large
enough that it should split, and fan-out with no named integration task or owner.

### 9. Pre-mortem coverage

The feature ships and fails silently 3 months later - what happened?

Flag: happy path only, "edge cases" named without specifics, no test covering the first realistic
failure, lint or build success treated as proof that stateful or ordered behavior is correct,
minimal-valid-input behavior described without a step that verifies it.

## Output

```markdown
---
date: YYYY-MM-DD
repo: <repo-name>
plan: <plan file path or ticket/spec URL>
issue: <issue key or task id, if any>
---

## Plan Review - <plan name>

### Blocking Findings
- 🔴 [section]: issue → why it matters → what the plan should do instead

### Non-Blocking Risks
- 🟡 [section]: issue → why it's risky → what to watch

### Missing Steps
- [section]: what's missing and why it matters for landing safely

### Open Questions
- Question that must be answered or explicitly accepted as a tradeoff

### Verdict
- `ready` - no blocking findings; minor risks only
- `needs edits` - workable direction, specific corrections required before execution
- `rewrite` - built on wrong assumptions, wrong layering, or major omissions
```

Every finding cites a plan section name or file path, leads with the problem, then why it matters,
then the correction. Only true blockers go in Blocking Findings. Omit any empty section except
`Verdict`. Say "the plan looks solid" only with zero findings; a plan carrying TBDs is never `ready`.

Save the full review to `~/.agents/plan-reviews/<repo>/<slug>-plan-review.md`, slug priority: issue
key or task id → plan filename → current branch name.

```
Plan review saved → ~/.agents/plan-reviews/<repo>/<slug>-plan-review.md
7 findings: 2 🔴, 3 🟡, 2 open questions
```

## Offer resolution

Skip this entirely when the verdict is `ready` with no open questions. Otherwise, read
`references/question-format.md` and follow its question format and rules - but replace its generic
Resolution Gates dispositions with these:

1. Grill one-by-one on ambiguous findings only, then apply all accepted corrections to the existing plan
2. Grill on every finding, then apply the accepted corrections to the existing plan
3. Apply best judgment on every finding, then edit the existing plan and summarize the amendments
4. Do nothing - leave the existing plan unchanged

Compute the recommendation: any architecture-level finding, finding crossing 3+ planned files, or
decomposition decision → recommend **1**, so the material tradeoff is resolved before amending.
Otherwise → recommend **3**.

The plan under review is the only plan artifact, and the saved review is its audit trail. Apply every
correction by editing that exact plan file in place, preserving its format and intent. This skill
never creates a new plan and never hands findings to the planning skill.

Wait for the answer. Record the gate answer and every per-finding decision in a `## Decisions` section
appended to the review file, preserving accepted tradeoffs and any rejected finding that materially
constrains implementation. After applying corrections, re-read the amended plan and report which
sections changed.
