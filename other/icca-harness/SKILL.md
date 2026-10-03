---
name: icca-harness
description: >
  ICCA names the four separated roles that carry the method:
  Implementer, Checker, Control, Auditor. Mandatory development workflow
  for any task that changes production code, fixes a bug, adds a feature,
  performs a refactor, or creates a commit. MUST be loaded before
  implementation begins. Keeps the orchestrator's context lean (delegation
  to a cheaper implementer tier, index navigation, evidence ledger) and
  enforces Commit Contract, Red Proof, frozen acceptance tests, delegated
  implementation, independent verification, bounded repair loops, Commit
  Gate, and requirement-first audit via global hooks.
---

# icca-harness

## Part 0: The tool-calling decision (self-triage)

Before anything else, decide whether this task needs the harness at
all. The decision is explicit, recorded, and follows the measured
break-even of this repository's own benchmark, not a habit. The roles
are model-agnostic: "orchestrator" is whatever strong model runs the
session, "implementer" is a cheaper tier it delegates to. The measured
pairs were a frontier orchestrator delegating to a strong implementer
(the token split) and cheap implementer tiers under gates (the gate
value); other pairings, including local models as implementers,
inherit the mechanics but not the numbers.

Three tiers:

**solo** (no harness): implement directly in the session. Choose it
when ALL of these hold: the change is one file or trivially localized;
the expected diff is small enough to review in one glance; the failing
behavior fully specifies the fix; no public interface, persistence,
security, audit or idempotency surface is touched. Mechanics: still
run `RP exempt --reason "triage: solo - <why>"` so the hooks stay
honest and the decision is logged. Measured basis: on the small
one-module task (a greenfield module), delegation cost 7% MORE on the
expensive model and 119% more in total at the same outcome; and in the
paired benchmark on the small-task class, the inline arm lost no
hidden-suite passes against the delegated arm over 12 pairs, at 0.45x
its median total cost, all 24 runs hidden-green.

**light** (the default for real work): the full commit cycle of this
skill (contract, red, freeze, delegated implementation, targeted and
full suite, diff review, attest, commit gate) with NO extra `--require`
gates. Choose it when any of these hold: the change spans modules; the
requirements need interpretation; the implementation will involve much
searching, many tool calls, or long test runs. Measured basis: on an
implementation-heavy task the delegated cycle spent 28% fewer tokens
on the expensive model at an identical success rate (16,576 to 11,864),
while total tokens across both models rose 37%; you buy expensive-model
reach, not total economy.

**full** (light plus declared gates): add `--require static` (and
`quality`, `coverage` where the contract warrants), checker agents in
fresh contexts, and a final audit. Choose it when "tests green" is not
sufficient evidence: security, persistence, audit-trail, idempotency
or tenant-isolation surface; or when the implementer tier is weak
(cheap or local models) AND the spec is example-specified, so a
plausible near-miss would pass the visible tests. Measured basis: the
stage-1 gate converted real hidden failures only in exactly that
window (weak implementer, example-specified spec); with a frontier
implementer it measured nothing (net 0), and with the sonnet tier it
measured no support either (net -1 over 12 pairs).

Mutation and property gates are never a default: in the benchmark they
found the same rare blind-spot defect the cheaper gates missed, but
did not earn their cost (3.08x on stage 2). The quality-ceilings gate
exists but is unmeasured (its hypothesis is registered unfunded).
Declare such gates only on block-closing contracts of critical code,
deliberately. (All numbers from the development benchmark of this
workflow.)

## Part 1: Making the subscription go further (read this first)

The session's strong model is the most expensive and scarcest allowance
in the subscription. This setup is built so that the expensive model's
tokens go almost entirely into decisions rather than volume:

1. **Implementation is delegated.** Implementer subagents
   (`model: "opus"`) write the production code in their own fresh
   contexts. Long implementation transcripts, search runs, dead ends and
   test output consume the cheaper tier's allowance, not the
   orchestrator's window. The orchestrator sees only the compact
   structured return.
2. **Contract handoffs instead of carried history.** The handoff to the
   implementer is a small, self-contained commit contract. The codebase
   does not get re-explained every round, and the orchestrator's context
   never has to hold implementation detail.
3. **Index navigation instead of file dumps.** `codebase-memory-mcp`
   (`search_code`, `get_code_snippet`, `search_graph`, `trace_path`)
   returns targeted snippets. Full files are read only for the hunks that
   actually need review.
4. **An evidence ledger instead of reconstruction.** Each commit's
   evidence lives in one compact structured entry (300 to 800 tokens).
   Block and final audits navigate the ledger instead of re-reading old
   chats or agent transcripts.
5. **Bounded repair loops.** At most two repairs per defect, then
   re-plan. This closes the most expensive token sink in agentic
   development: an endless fix loop with a growing context.
6. **A fresh audit context.** Final acceptance runs in its own agent and
   costs nothing from the main window. It is also less anchored, since it
   never sees the "all done" summaries.
7. **Mechanical gates instead of model discipline.** Freeze and commit
   gates are checked deterministically by hooks and a CLI. The
   orchestrator does not have to hold or repeat the process state; it
   lives in `~/.claude/red-proof/state/`.

The effect: the orchestrator's window holds the plan, the contracts, the
diffs and the decisions. All the volume (implementing, searching, test
runs, audit) happens in delegated or fresh contexts.

## Part 2: The enforced commit cycle (red-proof)

### 0. First principle

Development follows a strictly separated maker-checker-auditor model:

- Orchestrator (the session's strong model, currently a Fable-class
  model): orchestration, deriving requirements, commit planning, test
  specification, red proof, review, verification, staging and the commit
  decision.
- Opus (implementer): implementation and repair of production code, and
  nothing else.
- Audit agent: independent completeness acceptance in a fresh context.
- Checker agents (stage gates): one fresh context per constraint check
  (static, coverage, and later stages), see 6.6.
- Control agent (optional per work package): an independent reviewer
  with fresh context that checks a finished cycle against its contract
  before the block audit; used in practice on larger plans.

Ground rules:

1. The implementer never decides on its own acceptance.
2. The implementer may not change the acceptance criteria.
3. A green test run proves conformance with the tests, not automatically
   the correctness of the specification.
4. The final claim is therefore never "the feature is correct" but "the
   feature demonstrably matches the specified requirements, to the extent
   audit and verification cover them".

### 1. Commit contract (orchestrator)

Before any implementation the orchestrator writes a small binding commit
contract.

Requirement provenance: every acceptance criterion is traced back to its
origin:

`original requirement -> commit goal -> acceptance criterion`

This is what stops a criterion from being back-derived from code that
already exists.

Contract contents:

- goal and expected behavior
- concrete acceptance criteria
- non-goals
- the relevant original requirements
- the permitted or expected change surface
- relevant existing invariants
- the new tests required
- immutable regression gates
- public or external interfaces
- relevant security, persistence, audit or idempotency invariants

The commit must be small enough to stay atomic, independently checkable,
understandable and revertible on its own.

A necessary scope extension goes back to phase 1. No silent scope
extension during implementation.

### 2. Red phase (orchestrator)

The orchestrator writes the binding acceptance and regression tests.
There are two legitimate kinds of red.

**A. Behavior red** (for interfaces that already exist): the test must
fail because of behavior that is wrong or missing in substance. Examples:
an expected status is absent; wrong validation; wrong audit result;
idempotency violation.

**B. Contract red** (for modules, classes, functions or methods the
contract deliberately introduces): here the expected failure may
explicitly be an `ImportError`, `ModuleNotFoundError` or `AttributeError`,
but only when exactly that missing symbol is part of the frozen commit
contract. A missing new API symbol is then the expected contract red and
not an invalid setup error. The orchestrator never writes production code
or interface skeletons.

**C. Scenario red** (for acceptance criteria written as Gherkin
scenarios): the expected failure is a failing scenario, either a
missing step definition or a failing step that corresponds exactly to
an acceptance criterion of the contract. Feature files are
specification, not production code: they may be written before the
freeze and are frozen together with their step skeletons.

**Invalid red**: unintended failures are not accepted, such as a syntax
error in the test, a wrong import path, broken test configuration, faulty
test data, accidental fixture problems, or any failure unrelated to the
commit contract.

**Red proof**: record the test ID, the kind of red (`contract`,
`behavior` or `scenario`), the expected failure reason, the actual failure reason, and
the outcome (expected red confirmed or not confirmed). Implementation may
begin only on a confirmed red proof. Red tests are never committed as a
lasting red intermediate state; the final commit must be green and
bisectable on its own.

### 3. Mechanical freeze (orchestrator)

**Ownership of the git index**: only the orchestrator may run `git add`,
change staging, or create commits. Opus may never stage, touch the index,
or commit.

Before delegating, the orchestrator stages the binding acceptance tests.
Before staging, the orchestrator runs the project linter over the
acceptance-test files it is about to freeze; a finding is fixed before
the freeze, never amended after. A freeze fingerprint is then taken
over the frozen test patch (test paths, test names, hash of the
acceptance-test patch, hash of the commit contract).

**Freeze rule**: during implementation Opus may not modify frozen tests.
Before acceptance this is checked mechanically: the staged test patch is
byte-identical; there are no working-tree changes to frozen tests; no
assertions were removed or altered; no `skip` or `xfail` was added. A
mismatch means automatic rejection, not a judgment call.

**Additional tests**: Opus may add tests in areas that are not frozen, as
long as they do not modify acceptance tests, do not weaken existing
expectations, and stay inside the commit scope.

### 4. Implementation (Opus)

Delegation through the Agent tool with `model: "opus"`. No sub-version is
pinned on purpose: `opus` means whichever Opus version is currently
provided.

The handoff prompt contains: commit contract, requirement provenance,
acceptance criteria, red proof, relevant test names, expected change
surface, hard project guardrails, explicit non-goals, immutable
invariants.

Codebase navigation: `codebase-memory-mcp` first, direct reading only for
the parts that matter. The index is a navigation source, never a
verification source.

Opus may: implement production code, add internal helpers, add tests
within the rules. Opus may not: modify acceptance tests; weaken
assertions; remove, skip or xfail tests; extend scope; do unrelated
refactorings; stage; commit.

### 5. Implementation return (Opus)

A compact structured return: files changed, acceptance criteria met,
design decisions, tests added, risks, uncertainties. The return is not
evidence, only a navigation index for the review.

### 6. Verification gate (orchestrator)

**6.1 Freeze gate** (first, mechanical): contract and acceptance-test
fingerprints unchanged, no test weakened. On failure, immediate rejection
with no further review work.

**6.2 Targeted verification**: new acceptance tests, directly affected
tests, relevant regression tests. All green.

**6.3 Impact review**: `detect_changes` establishes the impact surface,
then every hunk that actually changed is read directly. For changes to
public APIs, core code, persistence, audit, security, idempotency, tenant
isolation or lifecycle state, also check call and dependency paths
through the code graph. `detect_changes` never replaces reading the
hunks.

**6.4 Contract review**: for every acceptance criterion, one concrete
piece of evidence: `acceptance criterion -> code -> test or probe ->
result`. Not acceptable: "looks correct", "Opus says it is done", "the
suite is green" without a link to the criterion.

**6.5 Scope review**: changes outside the contract, unnecessary
refactorings, unintended API changes, new persistence, new copies of
personal data, audit, security and idempotency effects, freeze
invariants.

**6.6 Constraint gate (stage 1)**: static analysis, the quality ceilings
and coverage run in every commit cycle whose contract declares them
(`RP contract --require static,quality,coverage`). They are executed by
independent checker agents, never by the orchestrator and never by the
implementer.

**Checker-agent pattern**: a checker starts in a fresh context via the
Agent tool. It receives: the repository path, the exact check command
including its threshold, the acceptance criteria of the contract that
concern its gate, and the expected report format (PASS or FAIL, the
measured value, the top findings as file:line). It does not receive:
implementer transcripts, the implementer's return, earlier evidence,
or the orchestrator's opinions. The checker runs `RP check <name> ...`
itself, so the evidence is bound to the code fingerprint mechanically
and cannot be asserted into existence. Findings go back to the
orchestrator as input for defect contracts (section 7); the checker
never repairs.

Roles, restated: the machine reads unit tests and implementation
output; the human reads specifications and QA-level reports. The
implementer and the checkers share no context in either direction.

### 7. Repair loop

When the verification gate fails the orchestrator does not implement the
fix. It writes a defect contract: observed behavior, expected behavior, a
reproducing test, the affected acceptance criterion, the permitted fix
scope. The repair goes back to Opus.

**Repair verification** (in this order): 1. freeze gate; 2. the
reproducing defect test; 3. relevant acceptance tests; 4. directly
affected regression tests; 5. review of every hunk the repair changed.

A full suite per repair iteration is not mandatory, but it is run
immediately when the repair touches core code, public interfaces,
persistence, audit behavior, security or trust boundaries, idempotency or
lifecycle state, or when it exposed an unexpected regression. At the
commit gate the full suite is always mandatory.

**Repair escalation**: at most two repair cycles per defect contract.
After that: stop repairing, re-plan. Back to phase 1 (is the commit too
large? is the contract wrong? is an architectural decision missing?
should it be split?). No unbounded repair loops.

### 8. Commit gate (orchestrator)

Required: freeze gate green; all acceptance tests green; affected
regression tests green; full suite green; every evidence key declared in the contract's
required_evidence green and fresh (this is where project-specific
checks live);
the complete diff reviewed; the contract fully met; no scope creep; no
open regressions; no unexplained TODOs; the diff atomic and revertible.

Only then does the orchestrator stage the production code and commit.
Every commit in the main series is green, understandable, bisectable and
revertible on its own.

### 9. Evidence ledger

One compact structured entry per commit: `commit_id`, `contract_hash`,
`requirement_ids`, `frozen_test_hash`, `red_proof`, `changed_files`,
`targeted_tests`, `regression_tests`, `full_suite`, `project_gates`,
`review_status`, `known_risks`, `final_commit_hash`. The ledger is a
navigation and evidence index; it does not replace code, tests, git
history, or the audit agent running things itself.

### 10. Block gate

After each block defined in the plan: full suite; project-specific
reproduction gates; mutation hardening where the project declares it
(a `mutation` evidence key on the block-closing contract, executed by
its own checker agent; its evidence uses production staleness, so it
survives test-only and docs-only edits); block invariants; plan versus commit reconciliation;
a check for omitted scope; a check of the evidence ledger; and only then
a fast reindex, so that a known-bad intermediate state never becomes the
navigation basis for the next block.

### 11. Independent completeness acceptance

A fresh audit context. The audit agent receives: the overall plan, the
original user decisions, the guardrails, the final repository, the commit
series, the tests, the evidence ledger. It does not receive:
implementation discussions, repair justifications, self-assessments, or
"all done" summaries.

**Requirement first**: the auditor interprets the requirements itself and
builds `requirement -> commit -> implementation -> test or probe -> its
own evidence`. Outcomes: met and proven; partially met; not met; not
provable.

**Independent verification**: the auditor runs the relevant checks itself
(acceptance tests, full suite, project gates, end-to-end demos) and may
build its own adversarial probes. Findings go back to the orchestrator.

**Focus areas**: requirements without a test; tests without a
requirement; nominal rather than semantic implementation; untested
negative paths; silent scope gaps; unintended behavior changes;
idempotency errors; persistence of personal data; audit-trail gaps;
security and trust-model violations; documentation versus behavior. A
green test run is not proof of completeness.

### 12. Audit finding loop

The auditor describes the finding and its evidence; the orchestrator
identifies the affected requirement, writes a new commit contract, writes
the red regression test; the normal cycle runs; then the finding is
re-checked specifically. The auditor never implements.

### 13. Final release gate

After the audit is closed, each item where the project defines one: clean
repository state; full test suite; reproduction check; fresh-clone check;
the central end-to-end demos; headline benchmark unchanged; style and
character gates; attribution check; plan versus code reconciliation; test
count sync; no open audit finding.

## Part 3: Mechanical enforcement (the red-proof gate)

Global PreToolUse hooks block production-code edits without an active
cycle and `git commit` without a passed commit gate. The CLI produces the
states and the evidence itself and binds them to a content fingerprint
(HEAD plus the content of every changed file). `git add` does not change
the fingerprint, since it is content-based; any real code change
invalidates existing evidence automatically.

```
RP() { python3 ~/.claude/red-proof/red_proof.py "$@"; }

RP contract --file <contract.md>            # phase CONTRACT_CREATED, resets the cycle
RP contract --file <c.md> --require static,coverage   # declare stage gates for this cycle
RP red --test <name> --type contract|behavior|scenario --expected "<reason>" -- <testcmd>
git add <acceptance-tests> && RP freeze     # phase TESTS_FROZEN, patch fingerprint
# implementation by Opus
RP check freeze
RP check targeted -- <testcmd>
RP check full-suite -- <suitecmd>
RP check static -- <lintcmd>                # exit-code gate, run by a checker agent
RP check quality -- <ceilings cmd>          # exit-code gate: complexity and size ceilings
RP check deps -- <import-graph cmd>         # exit-code gate: cycles and layering
RP check e2e -- <scenario cmd>              # exit-code gate: the wired artifact end to end
RP check coverage --min 90 -- <covcmd>      # metric gate, threshold enforced mechanically
RP check mutation --min 80 -- <mutcmd>      # block-gate stage: survives test-only edits
RP check property -- <cmd with --hypothesis-seed=N>   # refuses to run unseeded
RP attest --diff-reviewed --contract-ok     # the only model-attested items
RP commit-gate                              # COMMIT_READY, bound to the fingerprint
git commit ...                              # allowed only now, exactly one commit per gate
RP status                                   # show state and fingerprints
RP exempt --reason "<why>"                  # classified exceptions only (4h, logged)
```

Note for zsh: a `$RP` variable is not word-split; use the `RP()` function
above. Each deny message from the hooks names the next required step.

A failed check arms a worktree snapshot guard: rerunning the same
check command on an unchanged tree is refused, the attempt still
counts, and `contract --max-attempts` (default 5, advisory) adds the
instruction to stop repairing and re-plan once the budget is reached.
A corrected command runs; the counter keeps its history.

Known limit: the hooks gate the Edit and Write tools and `git commit`.
Writes that bypass those tools (bash heredocs, `sed -i`, output
redirection) are not intercepted; the content fingerprint still
invalidates stale evidence, but the edit itself is not blocked. Treat
bash-level writes to production files as out of process.

## Part 4: Binding meta-rules

- Tests before implementation.
- A new API may start with an expected contract red; existing behavior
  requires a behavior red.
- The orchestrator writes no production code.
- Opus modifies no frozen acceptance tests.
- Only the orchestrator stages and commits.
- Freeze and commit gate are checked mechanically (hooks plus CLI).
- Implementer and acceptor are separate roles.
- Repair loops are bounded (at most two per defect contract).
- The full suite is mandatory before every main commit.
- `codebase-memory-mcp` is a navigation aid, not a source of proof.
- The actual diff, the tests and runtime behavior are the verification
  sources.
- No scope creep without a new contract.
- Every main commit is green and bisectable.
- A green test run is necessary but not sufficient.
- The audit agent interprets the original requirements independently and
  may run tests and demos itself.
- Constraint checks run in independent checker agents with fresh
  context; the implementer never sees checker reasoning, the checker
  never sees implementer transcripts.
- A checker agent never repairs; its findings become defect contracts.
- The method proves conformance with the specification that was checked,
  not absolute correctness of the specification.
