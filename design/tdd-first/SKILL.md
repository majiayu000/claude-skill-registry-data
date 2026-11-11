---
name: tdd-first
description: "Enforce a RED→GREEN→REFACTOR cycle for a feature. Writes failing tests BEFORE implementation, runs the test suite to confirm the red state, then invokes the implementer agent with the failing tests as authoritative input, then re-runs to confirm green. Use when: user says /tdd-first, 'do this test-first', 'TDD this feature', or before any safety-critical / migration / auth path change. Default for changes under any root named by the safety-critical.roots slot of .claude/project-profile.md, and anything touching a live external-action path."
user_invocable: true
---

# /tdd-first — Test-First Implementation Protocol

When invoked, enforce the RED→GREEN→REFACTOR cycle. **No implementation code is written until a test is red.** This skill complements (does not replace) `/design-first` — run the concept-contract phase first, then this skill for the code phase.

## Step 0: Preconditions

1. **Concept contract must exist** for non-trivial features. If the `concept-gate.py` hook is active and no contract path is supplied, halt and tell the user to run `/design-first` first.
2. **Scope must be testable** — if the change is purely visual (CSS tweak, template restructure) skip this skill and use `ui-ux-designer` directly.
3. **This skill is strongly recommended** (but not mandatory) for:
   - Any change under a root named by the `safety-critical.roots` slot of `.claude/project-profile.md` — read the slot, do not guess a path from a project name
   - Any change under a root named by the `auth.roots` slot
   - Any new EF Core migration or repository query
   - Any change to the domain's rule-evaluation pipeline — its evaluators, its field resolvers, or the component that sequences them

## Step 1: Identify the test surface

Ask the user (or infer from the contract):

- **What behavior is changing?** Name it as a single sentence.
- **What would a correct implementation produce that a broken one does not?** This is the test assertion.
- **What test project houses this?** Match the layer against the `test.roots` slot of `.claude/project-profile.md` — one backend suite per layer — or, for a frontend change, `src/app/**/*.spec.ts` under the owning `frontend.roots` entry.

Write the answers to a scratch file at `.claude/tdd-scratch-<timestamp>.md` so the subsequent agents can read it without losing context.

## Step 2: RED — write the failing test

Launch `senior-test-engineer` with this contract:

```
TASK: Write failing test(s) for <behavior>. DO NOT write implementation code.
  The implementation is intentionally absent or incorrect.
CONTEXT: <link to concept contract>
FILES_TO_ADD: <specific test file paths>
CONSTRAINTS:
  - Follow project test conventions (xUnit + Moq for .NET, Jasmine + signals testing for Angular)
  - Test must FAIL with a clear assertion message, not a null-ref or compile error
  - Cover: happy path + at least one edge case + one error path
  - If the behavior depends on the clock, on randomness, or on an external service client, mock those dependencies properly
PRIOR_FINDINGS:
  contract_path: <path>
  contract_status: approved
  phase: RED  # this field signals test-engineer NOT to suggest fixing the code
```

## Step 3: Run the test suite and confirm RED

Run the tests and verify they FAIL:

- **.NET:** `dotnet test <project-path> --filter "FullyQualifiedName~<test-class>"`
- **Angular:** `ng test <project-name> --include="<spec-path>" --watch=false --browsers=ChromeHeadless`

**Halt conditions:**
- Tests pass → you wrote the wrong test. Return to Step 2.
- Tests error-out (compile/DI failure) instead of failing-with-assertion → return to Step 2 and fix the test setup. A green-via-compile-error is not a valid RED state.
- Tests fail but the message is unclear ("Expected True but got False") → return to Step 2 and make the assertion message diagnostic.

Record the RED confirmation in the scratch file with the actual failing output.

## Step 4: GREEN — implement the minimum code

Launch the appropriate implementer agent (`dotnet-backend-architect`, `angular-senior-dev`, `ingestion-data-architect`) with:

```
TASK: Make the failing tests in <test-file-paths> pass. Write the MINIMUM code required.
CONTEXT: Tests were authored in the RED phase of a TDD cycle. Implementation must satisfy the test's assertion without over-engineering.
CONSTRAINTS:
  - Do NOT modify the tests (those are the contract)
  - Do NOT add features not covered by a failing test
  - If you find a test is wrong, HALT and report — do not "fix" the test silently
PRIOR_FINDINGS:
  contract_path: <path>
  contract_status: approved
  phase: GREEN
  failing_tests: <paths>
  red_output: <captured output from Step 3>
```

## Step 5: Run the test suite and confirm GREEN

Re-run the same test command. **All previously-red tests must now pass.** Other tests must still pass.

**Halt conditions:**
- Target tests still red → implementer failed. Return to Step 4 with the new red output.
- Target tests green BUT other tests red → implementer introduced a regression. Return to Step 4 with the regression output.
- Target tests green BUT build broken → return to Step 4.

Record the GREEN confirmation in the scratch file.

## Step 6: REFACTOR (optional but recommended)

Launch `fullstack-code-reviewer` **via the `Agent` tool** — never review the GREEN implementation inline in the main session. The implementer's reasoning from Step 4 is still primed in the main context; only a fresh agent instance can judge the code without that bias.

```
TASK: Review the GREEN implementation for quality issues — duplication, naming, error handling,
  project-convention violations — that can be refactored WITHOUT breaking any test.
FILES: <implementation files>
CONSTRAINTS:
  - No behavior change. The test suite must stay green.
  - Suggest refactors inline; do not auto-apply.
PRIOR_FINDINGS:
  phase: REFACTOR
  tests_green: true
```

If the reviewer suggests refactors, apply them one at a time and re-run the tests after each. Abort if any test goes red.

### Second-pass review = spawn fresh, never `SendMessage`

If a second review pass is needed after refactors land, spawn a **new** `fullstack-code-reviewer` instance — do NOT `SendMessage` to the Step 6 reviewer. Its prior findings prime the second pass with the implementer's context and defeat the isolation that makes the review valuable.

### Safety-critical paths: also spawn the domain reviewer

For changes under any root named by the `safety-critical.roots`, `auth.roots` or `migration.root` slots of `.claude/project-profile.md`, spawn the matching domain reviewer (the project's live-action safety reviewer, `security-auditor`, `migration-safety-reviewer`) as an **additional** Agent-tool invocation — not a replacement for `fullstack-code-reviewer`. Each reviewer is an independent isolated instance. Step 7's `/verify-before-done` Step 5.5 will refuse to PASS without these HANDOFFs in scope.

## Step 7: Final verification + cleanup

1. Run `/verify-before-done` (if available) or manually:
   - Build passes for all affected projects
   - Full test suite passes (not just the target tests)
   - No uncommitted auto-generated files (check `**/generated/` under `frontend.root-container`, and `migration.root`)
2. Delete the `.claude/tdd-scratch-<timestamp>.md` file or move it to `.claude/tdd-history/` if you want to keep the audit trail.
3. Report the HANDOFF for the calling context, including:
   - Final test count (red → green delta)
   - Refactors applied
   - Files changed

## Anti-patterns (halt and restart if you catch yourself doing these)

- **Writing tests AFTER implementation and calling it TDD** — that's test-last, not test-first. Doesn't count.
- **Making tests pass by weakening the assertion** — if `Assert.Equal(5, x)` becomes `Assert.True(x > 0)` to get green, you've bypassed the cycle.
- **Skipping Step 3 (RED confirmation)** — an unverified RED may already be GREEN by accident, making the implementer's work a no-op.
- **Implementing beyond the test** — "while I'm here I'll also add…" → new tests first, separate cycle.
- **Silently editing the test in the GREEN phase** — if the test is wrong, halt and escalate.
- **Reviewing the GREEN implementation inline in the main session** — the implementer's reasoning is primed in the main context. Inline review is biased review. Spawn `fullstack-code-reviewer` via the `Agent` tool.
- **`SendMessage`-ing the prior reviewer for a second pass** — the prior instance carries its own findings + the implementer's context. Spawn a new instance.

## Integration with the project's existing flow

This skill slots into the project's dev flow as follows:

```
/design-first → concept contract approved
   → /tdd-first (THIS SKILL)
       → senior-test-engineer (RED)
       → run tests → confirm red
       → dotnet-backend-architect OR angular-senior-dev (GREEN)
       → run tests → confirm green
       → fullstack-code-reviewer (REFACTOR, optional)
   → /verify-before-done
   → (domain-specific reviewers: security-auditor, trading-safety-reviewer, etc.)
   → commit
```

## When to NOT use this skill

- Pure visual / CSS / template polish — use `ui-ux-designer` directly.
- Single-line typo / config bump — trivial change, skip the protocol.
- Exploratory spike / proof-of-concept — TDD hurts when you don't know what you're building yet; use `design-first` brainstorming first, then TDD the concrete feature.
- External data-source integration where you can't mock the provider — fall back to integration tests with recorded fixtures; still test-first, just not unit-level.
