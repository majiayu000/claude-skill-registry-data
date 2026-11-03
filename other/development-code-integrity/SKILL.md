---
name: development-code-integrity
description: |
  Integrity check on freshly-written code — proves the code does what its intent says by making the tests match that intent. It adds the tests that are missing and fixes any test that is wrong (always derived from the spec or the owner's expectations, never read off the implementation), runs them, and — when a test goes red — fixes the code (or the test, where a recorded call finds the test wrong) and makes it green. Before any of that, it moves new logic the change wrote outside the part that owns it in the product's parts table (docs/SDD.md § 3), in a commit of its own. It always writes a committed `code-integrity-report`, so even a clean pass leaves proof a review happened — for a product in its own repo the code commits land in the product's repo and the report in the change's own. Runs two ways with the same behaviour: as a step in the change pipeline on the code just implemented, and interactively when you point it at a file or a folder. Where the intent leaves a call open, the reviewer makes it — the reading most faithful to the intent — and records it in the report for its owner to confirm; it STOPs only when it cannot go on (no intent to read, interactively no way to tell how to run the tests, a fix or a placement move that would redesign the change, or a `Deferred:` line on the closing marker that is not real), and it never invents scope. In the pipeline it also accepts the developer's declared deferrals — one `Deferred:` line per blocked task — after checking each is real (not right), leaves everything inside a deferred task alone, and reports each line with its four check results.
  Use when: verifying that just-implemented code is correct against its intent, checking a file or a folder for integrity, "does this code actually do what it's meant to", or running the code-integrity step of the change pipeline.
  Do not use for: product-correctness sign-off (that is acceptance / QA), redesigning code, or authoring a change spec.
license: MIT
metadata:
  version: "2.9.0"
  category: execution
  risk: safe
---

# Development Code Integrity

## Purpose

Prove that a piece of code does what it is *meant* to do — not what it currently does.

The reference for "meant to" is the code's **intent**: the change's spec in the workflow, or the
owner's input→output expectations interactively. Every test this skill writes comes from that intent.
It never reads a test off the implementation — a test written from the code would lock the code's bug in
as green, which is the exact failure this skill exists to catch.

The shape of the work is fixed and small: put new logic in the part that owns it, make the tests match
the intent, run them and commit, and if a test is red fix the code until it is green. **Which repo takes which commit depends on where the
product lives:** code and tests go to the contract's `code_worktree`, the report to its
`pipeline_worktree` (§ *Commit*) — one repo for a product inside the instance, two for one in its own. **The reviewer is trusted with the calls the intent leaves
open.** Where the intent does not settle something — which of two readings it means, whether a red test
or the code is wrong, how far a fix should go — the reviewer decides, from the intent and never from what
the code happens to do, and writes the decision into the report so its owner can confirm or reverse it
later. It **STOPs** only when it cannot go on (§ *When to STOP*).

In workflow mode the developer may have **deferred** a task it could not land, and said so on the closing marker with a `Deferred:` line. This skill **accepts** a declared deferral after checking that it is *real* — never whether it is *right*, which is the owner's call — and it changes nothing inside a deferred task (§ *Deferrals*).

**Announce at start:** "I'm using the development-code-integrity skill to check this code against its intent."

## When to Use

- As the **code-integrity step of the change pipeline's workflow mode**, on the code a change just implemented.
- **Interactively**, when the owner points the skill at a file or a folder.

Both modes run the same behaviour below. Only the source of the intent and the commit target differ.

## Input

**Code — a single file or a folder.** In the workflow it is the code the change just implemented; in
interactive mode it is whatever the owner names.

## Where the intent comes from

The intent is the reference for every test. It is **never** the implementation.

**In the change pipeline's workflow mode** — read the change's own spec, in this order:

1. `tl_instruction.md` — the primary intent (what each task was meant to do).
2. `change_spec.md` — the behavioural spec behind it.
3. `docs/fdr.md` — extra context **only when it exists**. It is optional. A project with no FDR is the
   normal case, not an error — **never halt on a missing `fdr.md`** (same stance as `development-specs`).

These live with the change: the spec files under
`system/projects/<project>/journey/tobiishi/<key>/`, the project's `docs/` under the product path from
`project.md`.

**Interactively** — the intent is one of:

- the input→output expectations the owner gives ("for input A, expect B") — the owner is the spec; or
- an **ad-hoc plan** the owner supplies — an `ad_hoc_plan.md`. Its per-task
  stated intent and `#### Behaviours to verify` (plus any spec it embeds) are the reference, exactly as a
  `tl_instruction.md` would be. Read the plan for the intent — never the code it produced; or
- if the target maps to a known change, that change's `tl_instruction.md` / `change_spec.md`.

**If there is genuinely no intent to read** — no spec, and (interactively) no owner expectations — **STOP**
(§ *When to STOP*). Do not fall back to the code. A missing `fdr.md` alone is not this case; it is only a missing
piece of optional context.

## The work, in order

Same steps in both modes: Step 0, then Steps 1 to 3. Workflow mode reads the marker's deferrals first (§ *Deferrals*, below).

### Deferrals — read them, check them, leave them alone (workflow mode)

Read the closing marker's `Deferred:` lines off the instance branch: the body of the newest
`developer: <key> — implementation complete` commit (`git -C "$WORKTREE" log -1 main..<key> --grep='<key> — implementation complete' --format=%B`, run against the instance worktree even for an external product),
because a re-closed branch carries more than one marker and the newest supersedes the rest
(`development-implementation` § Step 3, *A re-close makes a new marker*). One bare line per blocked task —
`Deferred: task <N> — <the blocked case> — <record>` or `Deferred: task <N> — depends on task <M> — <record>`.
A marker with none has nothing to check; go on to Step 0. Interactive mode has no marker and skips this section.

**Accept a deferral after checking that it is real.** Each `Deferred:` line is accepted only when all four hold. This is a check that the deferral is real, never that it is right — whether the developer should have deferred is not this skill's call.

1. **The task exists.** Task `<N>` is a `### Task <N>` in `tl_instruction.md`.
2. **No delivered task is deferred.** Apply `development-implementation` § *A landing commit*, including its evidence check for a reopened task with an earlier landing subject. Read the per-task commits and current implementation in the contract's `code_worktree` (`<CORE>/tools/development_path.py resolve`) — the product worktree for an external product, the instance worktree otherwise; read the marker's correction evidence on the instance branch. A claimed correction without that evidence fails this check.
3. **The case is in the tree, or the dependency is itself deferred.** A blocked task's case is in the tree as `change_spec.md` and `tl_instruction.md` state it — its tests present, not deleted, weakened, skipped or marked expected to fail. A dependent task's `task <M>` is itself named by another `Deferred:` line.
4. **The record exists.** The `<record>` path (before any `§ <section>`) exists on the branch.

**Leave everything inside a deferred task alone.** Add no test, fix no test, fix no code and turn nothing green inside a deferred task. **Decide for yourself which task a failing case belongs to** — from the task's `#### Behaviours to verify` and the test's own location — and never from the marker's `Failing:` line alone: the chain trusts `Failing:` because it runs no tests, and this skill is where a list that lies is caught. A failing case that belongs to a real deferral is **not a finding**. Any other failing case is today's red (Step 2, Step 3).

**An unreal deferral is a STOP.** If any of the four checks fails for any `Deferred:` line, the verdict is `Integrity: stopped`, and the report names that deferral and the check it failed (§ *When to STOP*). Otherwise every deferral is real and the verdict is reached as today, with the exclusions above applied.

### 0. Put new logic in the part that owns it

Code that does the right thing in the wrong part is not done. The rule, and what *owning part* and
*misplacement* mean, are `<CORE>/doctrine/flow/development_flow.md` § *Code goes where the parts table
puts it*. This step applies it before any test is written, so Steps 1 to 3 review the code where it
will stay.

**Workflow mode.** Read the parts table, `docs/SDD.md` § 3 under the same product path as
`docs/fdr.md`. Walk every piece of logic the change's code commits added, and find its owning part.
A deferred task landed no code (§ *Deferrals*), so it has nothing to walk. For each misplacement:

- **Run the suite first**, before any move, and keep which cases are red and which green (the
  command is found as § *How the tests get run* says, under Step 2).
- **Move it** into the owning part's code and import it where it was called. Behaviour does not
  change. A new file inside a unit the design lists is layout and is allowed.
- **Run the suite again.** Every case is red or green exactly as in the first run. A test that imported the logic from its old place now
  imports it from the new one. Where any case changes, the move was not behaviour-preserving: undo
  it, and treat the case as a redesign.
- **Commit the moves** as one commit, `… — placement`, in the contract's `code_worktree`, before Step 1.
- **Record each one** in the report's **Placement** entry, and count it under **The finding**.

A misplacement is never left as a note or a later seed. A move that would need a unit the design does
not list, or an import `docs/nfdr.md` § 1.2 forbids and `change_design.md` § *Records this change makes false* does not allow, is a redesign: STOP (§ *When to STOP*). With no
parts table there is nothing to place against: skip the step and say so in the report.

**Interactive mode.** The step runs when the owner names the product's parts table. It walks the
target's own logic. Otherwise the report says the step did not run.

### 1. Make the tests match the intent

From what the code is *meant* to do, every behaviour in the intent should have a test. On a product with no code there is no test to write; see *How the tests get run* in Step 2.

- **Add** the tests that are missing.
- **Fix** any test that is wrong — one that asserts the buggy behaviour instead of the intended behaviour.

Write every test from the intent, never from reading the implementation. If a test already exists and
already matches the intent, leave it.

### 2. Run the tests and commit them as they stand — before any code fix

Run the suite, then commit the tests **in the state the run leaves them** — do not touch the code first.
This is the load-bearing rule of the whole skill:

- **A test is red** → this is a **red commit** (`… — red`). It captures the intent-derived test failing
  against the buggy code, which is the proof the test caught a *real* bug — not a test shaped to match
  whatever the code already did. Fixing the code before this commit destroys that proof and is exactly the
  failure this skill exists to prevent. Commit the red state on its own, then go to Step 3. (Where Step 3's
  call later finds the *test* wrong, this commit records the reading that was set aside instead.)
- **A red case that belongs to a real deferral** → not a red commit and not a finding: leave it as the developer committed it (§ *Deferrals*).
- **All green** (every case outside the real deferrals) → the code already matches its intent (a clean pass, no bug). Commit the tests; there is no
  red state to capture and no second commit after Step 0's. The `code-integrity-report` rides with this commit for an in-repo product; for a product in its own repo it is committed to the `pipeline_worktree` (§ *Commit*).

This mirrors the Prove-It (bug-fix) cycle in `test-driven-development` — *test fails → commit red → fix →
commit green* — and the per-task `red → green` cycle `development-implementation` runs. (Commit targeting
and message shape are in **Commit** below.)

**How the tests get run** — find the test command, don't guess it:

- **Workflow mode:** read it from `project.md` — the same
  source `development-implementation` uses — and issue it through the gate tool (§ *The full-card run goes through the gate tool*, below). A card reading `Test command: none` is a product with
  no code: there is no suite to run and no test file to write, so prove each claim of the intent by
  the command or reading it names and record each one in the report. On a preserving change those
  claims are the spec's invariants, each re-checked at its after-place by the plan's own checks, in
  their between-two-commits form (`change_classification.md` § *A product with no code*). Steps 2
  and 3 then have no test commit for the report to ride with: the report is committed on its own,
  in the same place an all-green run commits it, with a `code-integrity:` subject. An invariant
  that fails is the reclassification event the developer's run should have halted on
  (`change_classification.md` § *A product with no code*). It is not this skill's to correct: the
  report names it and reads `Integrity: stopped`. With every invariant holding, it reads
  `Integrity: pass`.
- **Interactive mode:** infer the project's test runner from the codebase (`pytest`, `npm test`, and the
  like). If you cannot determine how to run the tests, **STOP and ask the owner** — do not guess a command.

**Language packets — resolved every run, no exceptions.** Resolve per
`<CORE>/doctrine/engineering/languages/README.md`: workflow mode starts at `project.md` `Languages:`;
interactive mode takes the declaration from an ad-hoc plan the owner supplies when there is one
(§ Where the intent comes from, above), and falls through the same chain when there is not. Read the
Conventions, Quality gates and Testing entries — they are **the bar the code is reviewed against**, and
a packet's answer **binds over the surrounding file's own style**: where they disagree the packet wins,
the code changes, and the divergence from the file is recorded. No packet for the resolved language
means proceed on the floor. **Either way the resolution is recorded in the `code-integrity-report`** —
a missing packet is **never a STOP**, and a run that never resolved is a defective run. Until 2026-08-21 this read `as review context`
and required a note only when a packet was absent, so a review that never resolved owed nothing.

**The full-card run goes through the gate tool (workflow mode).** Every full run of the card's `Test command:` in workflow mode — Step 2's run, a run after a code fix, a run after a placement move — is issued by `<CORE>/tools/gate_suite.py` in the environment the product's CI calls for, never directly. Read `<CORE>/prompts/gate_suite.md`: it owns how the evidence is read, where the owner's ask comes from, and the three calls. This skill's own call, with the evidence file that recipe's Step 3 builds, is:

```sh invocation
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance change worktree>" --project "<project>" --key "<key>" \
  --gate code-integrity --inputs "<inputs file>" \
  > "<output file>" 2> "<error file>"
```

On a card reading `Test command: none` no evidence is read, and the call carries none:

```sh invocation-no-inputs
python3 "<CORE>/tools/gate_suite.py" run \
  --worktree "<instance change worktree>" --project "<project>" --key "<key>" \
  --gate code-integrity \
  > "<output file>" 2> "<error file>"
```

Where the owner's ask applies, the recipe's second call replaces the first, with `--gate code-integrity`. An interactive run keeps its own discovery of the test runner (above): only a run that issues the card's `Test command:` as a managed gate — the chain's own launch of this step — uses the tool.

- **Keep every run's `Environment:` lines.** Read them by `<CORE>/prompts/gate_suite.md` § *Reading the run's lines*. The run whose result the `Integrity:` verdict rests on — the last full-card run — has every `Environment:` line it printed copied whole into the report, each as a bare line (§ *Always write the `code-integrity-report`*). Each earlier run's lines go in the test evidence as bullets, one bullet per line, never as bare lines.
- **Failure is stated as a failure.** Whatever the environment, a refusal or an unreachable environment is `Integrity: stopped`, never `Integrity: pass`: no suite ran. The report carries the `Environment:` lines the tool printed and `The test command was not run. It reported: {reason}`, where `{reason}` is the first line the tool wrote to standard error. Note that a failed suite is Step 3's red, not a stop. Never run the card's command by hand to get a result. An environment that was not ready, including one whose test command exited 127, is `Integrity: stopped` too. The tool prints an `Environment: not-ready — …` line for it, and the report carries that line bare, copied whole with the tool's other `Environment:` lines. It is never Step 3's red, because a run whose environment was not ready is not a failed suite. The chain halts `environment-not-ready` on a report that carries such a line, ahead of `integrity-stopped`.
- **A card with no suite** takes `Environment: none — no suite`, with nothing probed or run.

### 3. Green or red

- **Green (clean pass)** — the code already does what its intent says. Cases of real deferrals are not part of this test. The Step 2 commit stands; write the
  `code-integrity-report` and commit it with those tests (in-repo product), or to the `pipeline_worktree` beside them (a product in its own repo, § *Commit*). Done — no red state.
- **Red** — a red test came from the intent, so the failure is presumed to be the *code's*. The red state
  is **already committed** (Step 2). Now fix the code, make it green, and commit that fix as a **separate
  green commit** (`… — green`), together with the `code-integrity-report` (in-repo product; for a product in its own repo the report is its own commit in the `pipeline_worktree`, § *Commit*). Two commits in the code repo after any Step 0 move: red, then
  green. **If the fix is not clear-cut** — the intent can be read more than one way, or it is not plain
  whether the *test* or the *code* is wrong — **make the call** (§ *Making a call*, below) and carry on:
  correct the test if the call says the test was wrong, fix the code if it says the code was. Only a fix
  that would redesign the change is a STOP (§ *When to STOP*). (The red commit stays either way; it is
  the record of what the test first asserted.)

### Making a call

A call is yours when the intent leaves a question open and the answer does not redesign the change.
Take it the way the change's own authors would have:

- **Read it from the intent.** Choose the reading the spec's words, the plan and the product's context
  support best — never "whatever the code already does", which is the one reading this skill exists to
  refuse.
- **Prefer the answer that keeps other documents meaning what they say.** A call that would change what
  an upstream document means (a spec step, a UX rule, a requirement) is weaker than one that fits it as
  written.
- **Prefer the smaller, easier-to-reverse fix** when two readings are equally supported.

Then record it in the report (§ *Always write the `code-integrity-report`*, **Calls made**). A recorded
call is not a STOP: the verdict is `Integrity: pass` — written as § *Always write the
`code-integrity-report`* says to write it — and the work goes on.

## Always write the `code-integrity-report`

Whatever the outcome, write a committed file named `code-integrity-report.md`. It records:

- **The verdict — directly under the title, on every outcome (a STOP included)** — the very first
  line after the title declares `Integrity: pass` or `Integrity: stopped`, never left for a later
  paragraph to imply. In workflow mode this is what the chain reads (`<CORE>/tools/chain_development.py`
  `_INTEGRITY_PREFIX`, and the `code-integrity` step of its step table) to decide whether
  to launch the audits at all, so it is never omitted: a clean pass declares `Integrity: pass`, and
  a run that STOPs (§ *When to STOP*, below) still writes the report, declaring `Integrity: stopped`.
  **Write it bare.** A machine reads this line by literal prefix, and the value it takes is what
  follows the colon — so `pass` and `stopped` are the only two values it knows, lower-case, and the
  words above are the whole line. The chain undresses `**bold**`, `*italic*`, `_underscores_` and
  `` `backticks` `` before it looks, so dressing the line no longer loses it, but nothing undresses
  a `>` blockquote marker, a `#` heading, a table cell or a bullet — a verdict written as any of
  those is a verdict the chain cannot find, and a report it cannot read is never a pass.
- **The environment the verdict rests on — directly under the verdict.** Workflow mode only. The report's opening lines are:

  ```
  # Code integrity report

  Integrity: <pass | stopped>
  Environment: <one line the verdict-producing run printed, copied whole; one bare line for each it printed, in the order printed>
  ```

  **Write them bare, each once.** The chain reads only the first block of consecutive `Environment:` lines in the report, and halts when any one of them fails. Write the lines of the run the verdict rests on as that block, one directly after another under `Integrity:`, because an `Environment:` line set apart from them is not read. No earlier run's line may stand as a bare line, because a bare one written above the block would start the block the chain reads. A card with no suite writes `Environment: none — no suite`. A run that stopped before it ran the test command writes `Environment: none — the run stopped before the test command ran` and says in the report why no suite ran; it never copies an environment from another record or another run. Every earlier full-card run goes in the test evidence with one bullet for each `Environment:` line it printed, each written `- An earlier run of the test command exited {status} and printed `{line}`.`, in the order the runs happened and, within a run, in the order it printed them. A run that was refused or could not reach its environment adds the line `The test command was not run. It reported: {reason}`.
- **The deferrals** (workflow mode) — each marker `Deferred:` line quoted verbatim, with the result of each of the four checks (task exists · no landing commit · case in the tree or dependency deferred · record exists). **None** when the marker carries none — written on every workflow run, so "no deferrals" reads differently from "never looked". An unreal deferral is named here with the check it failed.
- **What was reviewed** — the file or folder, and the code under it.
- **The intent it was checked against** — which spec files / owner expectations were the reference.
- **The tests added or fixed** — each one, and why.
- **The finding** — bugs found and fixed and misplacements moved, or **no issues** (if nothing was
  moved, every behaviour already had a correct test and everything passed, say so explicitly).
- **Calls made** — every question the intent left open that you settled (§ *Making a call*): the
  question, the readings you weighed, the one you took and why, whose document it belongs to (the seat
  that can confirm or reverse it), and what would change if they rule the other way. Written on every
  run — **none** when there were none — so a reader can tell "no calls" from "never recorded".
- **Placement** (Step 0) — each piece of logic walked, its owning part, and whether it was already
  there or was moved, with the `… — placement` commit. Logic no part owns is listed as **no owning
  part**, and a move that stopped the run as **stopped**, with why. **No new logic**, **no parts table**
  and (interactively) **not run** are the entry's other answers. It is written on every run, so "nothing misplaced" reads
  differently from "never looked".
- **The language resolution** — the language, which step of the chain answered, and the packet read (with
  its concern files) or the floor fallen to. Recorded on every run, including one that found no packet:
  a review that resolved and found nothing has something to say, one that never looked has nothing to
  say, and the two must not look the same on disk.

This runs in **both** modes, so even a clean pass leaves committed proof that a review took place.

**Where it lands:**

- **Workflow:** with the change, at
  `system/projects/<project>/journey/tobiishi/<key>/code-integrity-report.md` — the same place the
  change's other per-change artifacts live (e.g. `flow_findings/`).
- **Interactive:** alongside the target, or at a path the owner names.

## When to STOP

STOP only when the review **cannot go on** — not when a question is open, because an open question is a
call (§ *Making a call*):

- there is **no intent to read** — no spec, and (interactively) no owner expectations;
- (interactively) you **cannot determine how to run the tests**;
- the only fix that satisfies the intent, or the only placement move (Step 0), would **redesign the change** — new modules, a changed
  interface, a different approach — which is outside this skill (it does not redesign code);
- a `Deferred:` line on the closing marker is **not real** — it fails one of the four checks in
  § *Deferrals*. The report declares `Integrity: stopped` and names the deferral and the failed check.
  No new `Integrity:` value exists for it.
- in workflow mode, the test command was **refused or could not reach its environment**, so no suite ran and nothing supports a pass (§ *The full-card run goes through the gate tool*);
- on a product with no code, a preserving invariant **fails its after-check** (§ *How the tests get
  run*). The developer's run should have halted on it as a reclassification; the report declares
  `Integrity: stopped` and names the invariant.

Ambiguity, a fix that is not clear-cut, and a question another seat owns are **not** STOP conditions.
Neither is a missing `fdr.md` — it is optional context. Never invent scope, behaviour, or machinery the
intent does not ask for.

A run that STOPs still writes the `code-integrity-report`, declaring `Integrity: stopped` on its
own bare line — the STOP does not skip the report; it is what the report is for (§ *Always write
the `code-integrity-report`*, above, which owns how that line is written).

## Commit

Commit the report through the shared builder — read `<CORE>/doctrine/governance/commit_via_builder.md` and supply its variables: `<repo>` = per commit, the worktree it lands in (§ below: `code_worktree` for code and tests, `pipeline_worktree` = `$WORKTREE` for the report) in workflow mode / the current repo in interactive mode, `<staged file(s)>` = the files each commit carries (the table below), plus subject / body / **`--actor senior-engineer`** (the agent `launcher.md` launches this skill as — name it, never derive it) / `--skill development-code-integrity` (this skill's own name, so `Skill-Version:` records what ran) / directional. Never hand-write `git commit` or a trailer.

- **Workflow mode** — commit on the change's branch (the change ran in an isolated worktree; commit with
  `git -C "$WORKTREE"`, never from the main checkout), so the terminal merge carries the report and fixes
  to `main`. Resolve the change's path contract once, as `development-implementation` does
  (`<CORE>/tools/development_path.py resolve --format json --worktree "$WORKTREE" --project <project> --key <key>`):
  **the tests and the code fix are committed in the contract's `code_worktree`, and
  `code-integrity-report.md` in its `pipeline_worktree`.** For a product inside the instance repo the two
  are the same worktree and the commits below are as tabled; for a product in its own repo they are two
  repos, so **the report is a separate commit in the `pipeline_worktree`** — never staged with code in the
  other repo — and a repo with nothing to stage takes no commit.
- **Interactive mode** — commit on the current branch.

**A Step 0 move adds one commit, `… — placement`, ahead of every row below**, and the rows are
otherwise unchanged.

**Two commits on the red path, one on a clean pass, each plus Step 0's placement commit when it moved
anything — never fold the failing tests and the code fix into a
single commit.** A bundled commit cannot tell "the test caught a real bug" apart from "the test was shaped
to match the code," which defeats the whole check.

| Outcome | Commits |
|---|---|
| **Red, code wrong** (bug found) | **1. red** — the intent-derived tests only, failing against the buggy code (`… — red`). **2. green** — the code fix + `code-integrity-report.md`, all tests passing except the cases of real deferrals (`… — green`). *Own-repo product: red and green go to `code_worktree`, and the report is a third commit to `pipeline_worktree`.* |
| **Red, test wrong** (a call finds the test misread the intent) | **1. red** — as above. **2. green** — the test correction + `code-integrity-report.md`, all tests passing except the cases of real deferrals (`… — green`); the commit body names the **Calls made** entry that justifies the change, since a test changed after going red is exactly the shape this check guards against. Where both kinds occur, commit 2 carries both. *Own-repo product: as above, the report a third commit to `pipeline_worktree`.* |
| **Clean pass** (no bug) | **1** — the tests (already green, except the cases of real deferrals) + `code-integrity-report.md`. *Own-repo product: the tests to `code_worktree` (when any were added or fixed), and the report its own commit to `pipeline_worktree`.* |

Keep each commit legible — the reader should be able to see what was reviewed and what was found from
the log alone.
