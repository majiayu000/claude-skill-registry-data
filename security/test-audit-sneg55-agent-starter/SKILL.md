---
name: test-audit
description: Use when auditing, pruning or sweeping a test suite, when deciding whether a new or changed test earns its place, when a test passes but would not catch the bug it is named for, or when production exports exist only so tests can reach them.
user_invocable: true
allowed-tools:
  - Agent
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Test Audit

A test earns its place by failing on a credible regression that no stronger test
already catches. This skill has two uses: the **authoring gate** for every new or
changed test, and the **audit** for an existing suite.

## Authoring gate

Before adding or changing a test, answer all four:

1. Which observable behavior, invariant or independent contract does it protect?
2. Which credible regression makes it fail?
3. Why does existing proof miss it? Each contract has one primary owner at the
   strongest boundary. A second layer needs a distinct transport or lifecycle
   risk. Extend an existing table or fixture before writing a new file.
4. Does it need an export, flag, wrapper or injection hook that production never
   calls? Then move the proof to the real boundary instead.

A regression test must fail before the fix for the intended reason and pass after
it. A behavior-preserving refactor must not break it.

## Junk patterns

- Assertion-free probes, self-comparisons, expected values computed by the subject.
- Copied inventories of exports, routes, error ids or constants that the type
  checker already enforces.
- Private-predicate or call-shape tests that duplicate a boundary test; the same
  shared helper replayed at every layer it crosses.
- Mocks or fakes that implement the behavior being asserted.
- Fixtures that fabricate receipts, ordering or persistence the owner should produce.
- Negative tests that pass on an unrelated guard. Check what rejects the input:
  a request with a bad origin and a bad Sec-Fetch-Site header proves only the
  origin check.
- Parse-does-not-throw tests on a non-strict schema, where a dropped key passes.
- Fixed sleeps (`waitForTimeout(500)`) standing in for a produced state.
- Names promising behavior the inputs and assertions never exercise. Judge by
  assertions, not by name.

## Retention bar

Keep tests that guard public API, protocol, config, migration, storage, security,
permission, default values, cross-implementation parity, architecture boundaries
and observable ordering, even when they are slow, static or read source. A source
read stays when it is the cheapest guard of a user-facing key, byte or path and
survives an identifier-only rename. A test that fails at baseline is a possible
product bug: reproduce it and repair the owner, never delete the test for it.

## Hard rules

- **Mutation proof.** Every new, repaired or retargeted assertion: run it green,
  break the one production line it guards, confirm red for the intended reason,
  restore the file, confirm `git diff <file>` is empty. Record the mutation and
  the red message. An assertion that cannot be turned red protects nothing, so it
  does not go in, even when the ledger asked for it.
- **Missing evidence means no deletion.** If you cannot name the remaining proof
  by file and test name, the mark is R.
- **Keeper first.** Before deleting a test, its keeper exists and passes. Write or
  repair keepers before deleting anything near them.
- **Never optimize for deletion count.** A short list of verified findings beats
  a long list of leads.

## Audit workflow

### Phase 0: Setup

- Work in a fresh worktree from `origin/main`, never the shared checkout. Run
  commands from inside that worktree: the agent-starter `rm-scope-guard` hook
  blocks deletes outside the working directory. If you cannot, say up front that
  file deletions will be handed to the user as one `git rm` command.
- Record the baseline at the pinned SHA: test file count, test LOC, and the
  pass/fail state of every in-scope file. Baseline failures go on their own list.

### Phase 1: Inventory

- Run the finder from the repo root:
  `python3 -I <this skill's directory>/scripts/find-test-only-exports.py .`
  It prints `status, test-file refs, path, export, flag` per line:
  - `TEST-ONLY`: no production reference, at least one test reference.
  - `USED-IN-FILE`: used inside its own file plus tests; exported only so a test
    can reach a private helper.
  - `UNREFERENCED`: referenced nowhere outside docs.
  - `scaffold`: an agent-starter foundation template or a file named in
    `.claude/rules/starter-patterns.md`. These are installed ahead of use on
    purpose. Never mark one D; ask the owner.
  Word matches miss dynamic use, so verify every row by hand before it becomes a
  candidate.
- Split the suite into **lanes** along production owner boundaries (not file
  prefixes). Give each test file exactly one lane. When the suite is too large
  to read in full in one context, give each lane its own read-only agent; load
  `subagent-dispatch` to pick the tier.

### Phase 2: Ledger (read-only)

Each lane writes a ledger in the shape of
[references/ledger-template.md](references/ledger-template.md). Marks:

- `R` retain: name the contract and the bug it catches.
- `F` fix: keep the contract, repair the assertion. Say what is vacuous and what
  the repaired assertion checks.
- `C` consolidate: name the keeper that absorbs the assertion, by file, test
  name and line.
- `D` delete: name the remaining proof, or why no contract exists.

For each non-R candidate record: exact location, the failure it would or would
not detect, non-test callers of the seam, the keeper, the git history reason it
exists, which hook or CI stage runs it and its keeper, and confidence.

### Phase 3: Verify and decide

- Open each high-confidence candidate and its keeper yourself. Medium-confidence
  items are leads; report them as unverified.
- These are product decisions, so put them to the owner instead of deciding:
  - production code only tests call (an unbuilt feature, or dead code to delete?);
  - any `scaffold` row;
  - a schema column, dependency or config key that deletion leaves unused;
  - a deletion that moves a guard from a pre-commit hook to CI only.
- Present the report and wait for approval before any edit.

### Phase 4: Apply

- One worktree and branch per lane. Workers do not commit.
- Per lane: keepers and F repairs with mutation proof first, then deletions, then
  the test-only seams the deletions unlock.
- After removing production code: the type checker is clean, a grep finds no
  importer of any removed symbol, and support files and dependencies the deletion
  orphaned are removed too. Rerun the finder or the project's dead-code tool to
  catch them.
- Lint every changed file.

### Phase 5: Validate

- Run the full suite once, serially, from the orchestrator after every worker
  has finished. Parallel full-suite runs starve timing tests and produce false
  failures. Run long suites in the background; the default tool timeout kills them.
- A failure in a file the change did not touch: rerun it on clean `origin/main`
  and on an idle machine before attributing it. Report a timing flake as a
  follow-up instead of fixing it in the audit.

### Phase 6: Report

Lead with open owner decisions. Then: counts by mark, gaps closed with their
mutations, production versus test LOC removed, baseline failures, timing flakes
seen, and what was not covered (files only pattern-searched, skipped directories).

## Common mistakes

| Mistake | Correction |
|---|---|
| Deleting a test that fails at baseline | It is a bug report. Fix the owner in its own commit. |
| Trusting the ledger's keeper | Mutate the line the deleted test guarded and watch the keeper go red. If nothing goes red, the deleted cases protected nothing and need no replacement. |
| Deleting a starter template the finder flagged | `scaffold` rows go to the owner. |
| Each worker running the full suite | One serial run from the orchestrator. |
| Reporting ledger leads as findings | Verify by opening the test and keeper, or label as unverified. |

Adapted from openclaw's
[test-audit skill](https://github.com/openclaw/openclaw/tree/main/.agents/skills/test-audit).
