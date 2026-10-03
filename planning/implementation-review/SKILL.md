---
name: implementation-review
description: "Pre-commit quality gate. Invoke before every git commit, after /flagrare:staleness-audit. Seven checks, plan gaps, use-case coverage gaps, missing test scenarios, test philosophy violations (Kent Dodds Testing Trophy), SOLID violations, Clean Code violations, and security vulnerabilities. Each check is delegated to a parallel subagent. Surfaces findings before they land in history. Also invoke when the user says review this, am I done, did I miss anything, or check the quality."
---

# Implementation Review

Run this before every commit, after `/flagrare:staleness-audit`. The goal: **what was planned is implemented, what is implemented is tested, and what is tested is correct**.

Each of the seven checks is run by a dedicated subagent. Spawn all seven in parallel, collect their reports, then synthesise into the output format below.

**REQUIRED BACKGROUND for Checks 2-4:** the test-related checks apply `/flagrare:testing-philosophy` (behavior over implementation, the Testing Trophy, the e2e necessity floor). Pass that skill's content into the Check 2, 3, and 4 subagent briefs so they judge against the same definition of "good test" the planning side uses.

**REQUIRED BACKGROUND for Check 7:** the security check applies `/flagrare:security-audit` (threat taxonomy, three-phase methodology, confidence gate, false-positive precedents, generic dependency audit). Pass that skill's content into the Check 7 subagent brief so it judges against the same security discipline a standalone `/flagrare:security-audit` run uses.

---

## Step 1: Gather inputs (main agent)

Before spawning subagents, collect in the main agent:

- `git diff --staged`, full diff (the primary input for all subagents)
- `git diff --staged --name-only`, file list
- The **active plan**: look in this order:
  1. Session context: did `/flagrare:atdd-plan` run earlier in this conversation? Use that output.
  2. `~/.claude/plans/*.md`, the most recently modified file, if the directory exists.
  3. The project's decision log (`docs/decisions/`, `docs/adr/`, RFCs, or equivalent), the foundational decision is always the mission/scope anchor.
  4. README roadmap, checked/unchecked items define what is in scope.
- Full content of test files touched or related to the staged changes.
- Full content of non-test source files in the staged diff.

If no plan is findable, say so explicitly and skip Checks 1-2 in the subagent briefs.

---

## Step 2: Dispatch seven subagents in parallel

Spawn all seven subagents simultaneously using `model: "sonnet"`. Each subagent receives the relevant slice of inputs (described in each brief below) and returns findings in the format `Check N · [name]: ✓ clean | ⚠ [finding] | ✗ [blocking finding]`.

Do not run checks sequentially in the main agent. Spawn → collect → synthesise.

**Rules every brief below inherits.** Paste these into each subagent's prompt ahead of its brief. They are adapted from the review prompts in alibaba/open-code-review; the teardown is at [`docs/research/2026-09-14-open-code-review-teardown.md`](../../../../docs/research/2026-09-14-open-code-review-teardown.md).

- **Report your coverage, in your check's unit.** Open your report with one line: what you were given, what you examined, what you skipped with a one-phrase reason each. Files for the code checks (3 through 7), plan items for Check 1, use cases for Check 2. A file whose hunks you did not read is skipped, not examined. Examining an implementation file does not cover its interface, its config, its type declarations, or its barrel export; the secondary file is where contract drift hides, and it is the one most often skipped.
- **Reading is unbounded, findings are not.** Read whatever you need to understand the change, including files outside the diff. The set of code you *evaluate* stays exactly as your brief says (Check 4 judges test files only, Check 5 non-test files only). File findings only against code inside the staged diff; deleted lines are reference context, not a target.
- **Write when the evidence is sufficient.** Once you can cite the construct and say what is wrong with it, write the finding and move on. Never call the same tool twice with the same arguments. There is no verification step behind you, so do not stop short of the evidence either.
- **Finding nothing is a result.** If a sweep turns up nothing real, report the check clean and finish. Do not keep probing for marginal findings, and do not manufacture one to prove you read the diff; your coverage line is that proof, and it is what makes a clean check credible. An invented finding costs more than a missed one, because it trains the reader to skim the whole report.
- **Every finding cites its construct.** File, line, and the code you are talking about. A finding without a citation is a hunch, and hunches do not leave the subagent.

---

### Subagent brief: Check 1: Plan gap analysis

**Inputs:** full `git diff --staged`, the active plan document.

Compare what the active plan said would be built against what the staged diff actually implements.

For each item in the plan's "Implementation Phases" or task list:
- Is it in the staged diff? → ✓ implemented
- Is it partially there? → ⚠ partial, what is missing
- Is it absent entirely? → ✗ gap, was it intentionally deferred, or forgotten?

Ask: would a reader of the plan consider this commit "phase complete"? If the plan defined a gate ("Phase N is done when ATs #1-4 pass"), does the commit satisfy it?

Flag every gap. A deferred item is not a gap, but it must be explicitly deferred, not silently absent.

---

### Subagent brief: Check 2: Use-case coverage

**Inputs:** full `git diff --staged`, the project's foundational scope document (ADR-0001, RFC-001, mission doc, or equivalent, whichever anchors what this project is for), README feature description.

For every **user-facing capability** in scope for this commit:
- Is there at least one test that exercises it through the public API?
- Is there a code path that implements it?
- **Is the critical happy path covered end-to-end through the real, assembled system?** Per the e2e necessity floor in `/flagrare:testing-philosophy`, a user-facing feature with unit + integration coverage but no e2e/full-stack proof that the layers connect is a gap. E2e generalizes by surface: a browser journey for a UI, running-service-over-HTTP-against-a-real-DB for a backend, a subprocess invocation for a CLI, public-API-as-a-consumer for a library. One or two critical paths suffice, but zero is a finding.

This is different from Check 1, use cases can be implicit in the product scope even if the plan did not spell them out. Ask: "what would a consumer of this code reasonably expect to be able to do?"

Flag any use case that has an implementation but no test, a test but no implementation, or a user-facing happy path with no end-to-end coverage.

---

### Subagent brief: Check 3: Missing test scenarios

**Inputs:** full `git diff --staged`, full content of changed test files.

For every behavior introduced or changed in the staged diff, work through this scenario checklist:

| Scenario type | Question to ask |
|---|---|
| Happy path | Is the basic success case tested? |
| Empty / nil / zero | What happens when the input is empty, null, zero, or absent? |
| Boundary | First item, last item, exactly one item, max capacity? |
| Invalid input | Malformed, out-of-range, wrong type, is the rejection tested? |
| Error path | For every success path, is the corresponding failure path tested? |
| Idempotency | If the operation can be called twice, is that safe? Is it tested? |
| Order sensitivity | Does the result depend on call order? Is that documented and tested? |
| Concurrent access | If the code will be called from multiple threads/tasks, is that safe? Is it tested? (Only if relevant.) |

Flag missing scenarios. Not every category applies to every change, exercise judgment, but don't skip a category without a reason.

---

### Subagent brief: Check 4: Test philosophy (Kent Dodds Testing Trophy)

**Inputs:** full content of changed test files only (do not check non-test files here).

For each test in the staged diff, check against the following rules. A violation is a finding. Apply the two acid tests from `/flagrare:testing-philosophy` to every test: **(1)** would it break under a behavior-preserving refactor (internal rename / restructure with the public contract unchanged)? **(2)** does it assert what a real user observes, or how the result was produced? A "yes" to (1) or a "no" to (2) is an implementation-detail test.

**Behavior over implementation**
- Does the test name describe a behavior ("rejects an out-of-range choice index with StoryChoiceRangeError") or an implementation detail ("calls ChooseChoiceIndex with the given index")?
- Does the test assert on the *observable result* or on *how the result was produced*?

**Public API only**
- Does the test access private fields, `_inner` objects, unexported functions, or internal state? → violation
- Does the test assert that an internal function/method *was called*, a spy or mock-call-count on a collaborator the code owns? → violation (asserts the mechanism, not the behavior)
- Does the test mock types it owns (its own classes, its own modules)? → violation
- Does it mock only at genuine external boundaries (network, disk, clock, OS process, third-party API)? → ✓

**Real collaborators where cheap**
- Is anything mocked that could be a real instance without significant cost? → flag
- Does the test spin up real collaborators rather than mocks? → ✓

**Refactor-proof**
- Would this test break if you renamed an internal method while keeping the public contract identical? → violation
- Would it break if you changed the internal data structure while keeping the return value identical? → violation

**Testing Trophy shape**: check *both* directions (most reviews only catch overuse):
- Does the commit add more unit tests than integration tests for behavior that crosses multiple units? → flag
- Is anything tested only at E2E level that could be tested cheaper at integration level? → flag (overuse)
- Conversely, is a user-facing critical path missing any e2e/full-stack test entirely? → flag (the e2e necessity floor, this is the quieter, more common gap; coordinate with Check 2 which has the scope inputs to confirm the feature is user-facing).
- Does any test reach for a snapshot that will be rubber-stamped on update? → flag (it asserts "it changed," not "it's correct")

**Test names**
- `it("works")`, `it("test 1")`, `it("should work correctly")`, `it("handles the case")` → violation
- `it("rejects a negative index with StoryChoiceRangeError carrying attempted=−1")` → ✓

---

### Subagent brief: Check 5: SOLID violations

**Inputs:** non-test source files from the staged diff only (do not check test files here).

Scan for these patterns:

**Single Responsibility**
- Does any new class or module have more than one reason to change? Look for: a class that both validates *and* persists, a module that both formats *and* dispatches.
- Flag if a class's methods cluster into two distinct concern groups.

**Open/Closed**
- Does the new code require callers to modify existing files to add a new variant? A `switch` or `if/else if` chain on a type tag in the caller is often the smell.
- Flag if extensibility requires modification of existing classes rather than addition of new ones.

**Liskov**
- Does any new subtype throw where its base doesn't? Does it silently ignore a method the base defines?
- Flag if a subtype's contract is narrower than the base type's.

**Interface Segregation**
- Does any new interface force its implementors to define methods they don't use?
- Flag fat interfaces.

**Dependency Inversion**
- Does new code `new` a concrete dependency inside a class rather than receiving it?
- Flag hardcoded `new ConcreteType()` inside class bodies where an abstraction or injection would be natural.

---

### Subagent brief: Check 6: Clean Code violations

**Inputs:** full `git diff --staged` (both test and non-test files).

Scan for:

| Issue | What to look for |
|---|---|
| Magic values | Bare literals with semantic meaning: `if (index >= 99)`, `setTimeout(fn, 3000)`, `"choice:made"` repeated in multiple files. Every meaningful literal must be a named constant. |
| Function does more than one thing | If "and" is required to describe what it does, it should be split. |
| Unqualified generic names | `data`, `info`, `result`, `value`, `temp`, `manager`, `handler`, `helper` without qualification. |
| Comments | Flag every comment in the diff that is not a trap-preventer: one where deleting or moving the code it sits on would look like a safe cleanup and break something the reader cannot see. What-comments, provenance ("on purpose", "the design says"), file headers, citations to tickets or docs, and test narration all fail that test, even when they read as a *why*. `/flagrare:wrap-up` Step 3 does the deleting; this check only reports. |
| Half-finished surfaces | Any exported symbol with `TODO`, a stub body `{ return null; }`, or "implement later". |
| Long parameter lists | More than 3-4 positional parameters, group into an options object. |

---

### Subagent brief: Check 7: Security

**Inputs:** full `git diff --staged`, file list, the lockfile diff if a lockfile changed.

Pull in the full content of `/flagrare:security-audit` and apply it to the staged diff. That skill carries the threat taxonomy, the three-phase methodology (understand the repo's security model, compare the change against it, trace data flow from source to sink), the confidence gate, the false-positive precedents, and the generic dependency audit.

The one rule: **only report a finding with a concrete exploit path, and only when over 80% confident it is actually exploitable.** A security check that flags theoretical issues gets ignored; keep it to what a security engineer would confidently raise. Review what the change *newly introduces*, not pre-existing issues the diff sits near.

When a lockfile changed, run the repo's native dependency auditor (scoped to the changed packages so the gate stays fast) and degrade gracefully to an advisory flag if the auditor is not installed.

Return findings in the house line format. HIGH and MEDIUM severity block; LOW is advisory.

---

## Step 3: Synthesise (main agent)

After all seven subagents return, merge their findings into this format:

```
Implementation review, [commit subject or staged file summary]

Coverage: N staged files. Per check: 3 N/N · 4 N/N · 5 N/N · 6 N/N · 7 N/N; Check 1 N/N plan items; Check 2 N/N use cases. Skipped: <item> (<check>, <reason>). Omit the skipped clause if none.

Check 1 · Plan gaps
  ✓ All phase items present  |  ✗ Gap: [item], [present/partial/absent]

Check 2 · Use-case coverage
  ✓ All use cases covered  |  ✗ [use case], no test / no implementation

Check 3 · Missing test scenarios
  ✓ Scenarios complete  |  ⚠ [behavior]: missing [scenario type]

Check 4 · Test philosophy
  ✓ Tests pass philosophy check  |  ✗ [test name]: [violation]

Check 5 · SOLID
  ✓ No violations  |  ✗ [file:line]: [principle], [finding]

Check 6 · Clean Code
  ✓ No violations  |  ✗ [file:line]: [issue]

Check 7 · Security
  ✓ No vulnerabilities in the diff  |  ✗ [file:line]: [category] ([severity]), [exploit in a phrase] + fix  |  ⚠ [lockfile moved / auditor unavailable]

Summary: [N findings, fix before committing / Clean, proceed]
```

If any check skipped an item without a reason, the Summary line says so and cannot read "Clean, proceed". Unexplained partial coverage is not a clean review.

If a finding is **blocking** (plan gap, philosophy violation on a public API test, SOLID violation that breaks extensibility, a HIGH or MEDIUM security vulnerability), fix it before committing unless the user explicitly overrides.

If a finding is **advisory** (a test name that could be clearer, a slightly long function), surface it but do not block.

---

## Commit-flow position

```
[code changes complete]
     ↓
/flagrare:staleness-audit    ← docs drift, TSDoc, export sync, stale markers
     ↓
/flagrare:implementation-review   ← THIS SKILL (7 parallel subagents)
     ↓
git commit
     ↓
/flagrare:release-check      ← is a release due?
```

---

## Anti-patterns

- Don't skip a check because "the change is small", that's when violations sneak through.
- Don't invent a plan if none is findable, skip Checks 1-2 and say so.
- Don't treat every advisory finding as blocking, use judgment.
- Don't run Check 4 on non-test files, or Check 5 on test files.
- Don't report a Check 7 security finding without a concrete exploit path, theoretical vulnerabilities are noise that trains the reader to skip the whole report.
- Don't fail Check 7 when the dependency auditor is missing, degrade to an advisory flag.
- Don't report "✓ clean" without the subagent actually reading the diff.
- Don't report a check clean when its coverage line shows unexplained skips. The coverage line is what makes clean credible.
- Don't invent a finding to prove the diff was read; the coverage line does that.
- Don't run checks sequentially, the point of subagents is parallel execution.
