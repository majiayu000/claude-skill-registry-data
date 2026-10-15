---
name: "speckit-harden"
description: "Quality gate for the code a feature produced: runs the mechanical audits, judges durability and bloat against a fixed rubric, fixes what it finds, and re-verifies. Runs between /speckit-implement and the spec review."
argument-hint: "Optional scope, e.g. a package name or 'skip mutation'"
compatibility: "Requires spec-kit project structure, the scripts in .claude/scripts, and a green suite"
metadata:
  author: "blastradius"
  source: "project-local — quality gate"
user-invocable: true
disable-model-invocation: false
model: opus
---


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). It
narrows scope (a package, a directory) or waives the expensive step
("skip mutation"). Empty means the whole branch, everything on.

## Goal

`/speckit-analyze` judges the artifacts. `spec-reviewer` judges the diff against
the spec. Neither asks the question this command exists for: **is the code that
shipped durable, and is any of it unnecessary?**

Those two are one question. Code nothing needs is code that will rot — an export
with no importer, a layer with one implementation, a test that passes with the
implementation deleted. Principle I is not a style preference here; it is the
cheapest reliability mechanism available, because the most reliable line is the
one that was never written.

## Operating Constraints

- **Fixes, not just findings.** Unlike `spec-reviewer`, this command edits. Every
  fix it makes is verified by the suite before it reports.
- **Never weaken a test to make a check pass.** Deleting a test, `.skip`ping it,
  loosening an assertion, or adding a suppression to clear a finding is the one
  thing this command must not do. If a finding cannot be fixed honestly, report
  it.
- **No new abstraction.** A quality pass that introduces a helper "for the next
  case" has failed at its own job.
- **Behavior stays put.** Every change here is a refactor, a deletion, or a test
  addition. If something needs a behavior change, that is a finding for the
  user, not an edit.

## Execution Steps

### 0. Size the job

```bash
git diff --stat $(git merge-base HEAD main)..HEAD -- apps libs e2e | tail -1
```

Under ~200 changed lines with no new files, the built-in `/simplify` skill is
the whole of step 3 and mutation is rarely worth its minutes — run steps 1 and
2a, then `/simplify`, then step 4. Above that, every step below.

### 1. Mechanical audits — and start the slow work now

Run the audits, and **in the same message** launch the `mutation-runner`
subagents from step 2b. Mutation runs in CI, never on this machine: each
runner dispatches the Mutation workflow (`.github/workflows/mutation.yml`,
every 3 days on `main` and on demand, sharded, one job per project or shard)
for the pushed branch head, or reads the run
that already finished, so the run's minutes pass while you work.

```bash
node .claude/scripts/artifact-lint.mjs      # spec/tasks defects + untestable/compound/uncovered FRs
node .claude/scripts/diff-audit.mjs         # dead surface, build-time traps + unjustified dependencies
npm run lint && npm run typecheck
```

Then, when the IDE is open, the second static analyzer this repo has and never
runs: `mcp__webstorm__get_file_problems` on each changed source file
(`projectPath` = repo root, `errorsOnly: false`). IntelliJ's inspections
overlap biome very little — unreachable code, suspicious promise handling,
redundant awaits, unused type parameters. An MCP connection error means the
IDE is closed; note "inspections: IDE not running" and continue, never retry.

If the diff touches `libs/contracts`, anything under `auth`, secret material,
or an input boundary (HTTP, filesystem, env), run the built-in `/security-review`
skill here and fold its findings in. This repo stores crypto inventory with a
`CHECK` constraint against persisting secret values; a feature near it earns
the pass.

`diff-audit.mjs` covers only what biome and tsc structurally cannot see:
cross-file dead exports, the per-app relative-import extension rule (which fails
at build time, not typecheck), new dependencies, added suppressions,
parameter-property DI in `apps/server`, and new source files no test mentions.
Fix every ERROR. Judge each WARN — several are legitimate by design (a test seam,
a deliberate Stryker disable on an equivalent mutant); say which you kept and
why.

### 1b. Design audit

```bash
git diff --name-only <base>..HEAD -- apps/web libs/ui-cockpit
```

When that lists a file, run the `design-audit` skill on the changed component
folders and on `libs/ui-cockpit/src/styles/cockpit.css`, with its `scan.mjs`
and `contrast.mjs` helpers. Fix every high finding, run it again, and list
what is left on a "Design audit" line in the report. When it lists nothing,
the line reads "Design audit: skipped, no web file changed".

### 2. Attack, then measure

**2a. Adversarial tests.** Invoke the `test-adversary` subagent (Agent tool,
`subagent_type: test-adversary`) with the feature directory and the diff's
public surface. It has not seen the implementation and must not; it writes the
tests the author's model of the code did not suggest. Every failing test it
leaves is either a defect or a spec gap — you decide which, and a defect is
fixed here while a spec gap goes to "Needs you". Its report is not shown to the
user; relay the failing rows.

**2b. Mutation score.** Collect the `mutation-runner` results launched in
step 1 (one per touched Nx project with a `stryker.config.json`; `npx nx show
projects --affected --with-target test:mutation` lists the touched ones). Each is a survivor table of at most
twenty-five lines read from the workflow's reports, or a `partial` line naming
the Mutation run still going: re-invoke the runner once that run has finished
(waited for in the background, never in a sleep loop). Relay the score line
per project. If the user waived mutation, you launched none.

The configured `break` threshold is the floor, and it is the only test-quality
measure in this repo that a passing green suite cannot fake: line coverage says
a line ran, mutation says a test would have noticed if that line were wrong.

A surviving mutant is one of three things, and saying which is the whole value
of this step:

1. **A missing assertion** — the common case. Add it.
2. **Untested behavior** — a branch, an error path, a boundary no test reaches.
   Add the test.
3. **A genuinely equivalent mutant** — the mutation cannot change observable
   behavior. Only then, a Stryker disable, on the line, saying which mutant and
   why it is equivalent.

Reaching the floor by disabling mutants is the failure mode this step exists to
prevent. Quote the before and after score.

### 3. Durability read

Invoke the `code-reviewer` subagent (Agent tool, `subagent_type:
code-reviewer`) with the diff range. It applies the rubric below with no memory
of why the code was written that way — which is the bias this step exists to
remove; the context that made a decision is the worst judge of whether it was
necessary. Its report is not shown to the user; every CRITICAL and HIGH is
fixed in step 4, and so is every MEDIUM/LOW whose fix is small or medium,
pre-existing or adjacent included. Only a large fix (the size test in
AGENTS.md, "Technical debt a review defers") is relayed as a `defer` bullet
for `specs/<feature>/deferred.md`; an adversary defect or a mutation survivor
is routed the same way.

The rubric it applies, so you can judge its findings:

- **Boundaries**: does every value crossing a process boundary — HTTP, the
  database, the filesystem, an env var — get validated where it enters, against
  the shared contract rather than a local cast? A type assertion at a boundary
  is a lie the compiler cannot catch.
- **Failure**: what happens when the dependency is down, the file is missing,
  the input is empty, the number is zero, the array is huge? Each answer is
  either in a test or it is a guess.
- **Resource discipline**: is every handle, transaction and temp directory
  closed on the failure path as well as the happy one?
- **Concurrency and order**: does anything assume an order it does not enforce,
  or mutate shared state a second caller could see?
- **Bloat**: an abstraction with one implementation, a parameter every caller
  passes the same value for, a wrapper that only forwards, a config knob nothing
  sets, a comment restating its own code. Each is a deletion.

### 4. Fix, verify, repeat

Apply the fixes in one pass, then:

```bash
npx jest --onlyChanged && npm run lint && npm run typecheck
```

Each of these: run it into a log and read only the exit code, the summary and the failures (AGENTS.md "Agent replies": `tail -n 40`, then `grep -nE '✕|●|FAIL|Error'` on a failure).

Re-run the audits from step 1. Loop at most twice; a third round means the
finding needs the user, not another attempt.

### 5. Report

```
## Harden: <feature> (<range>)

| Check | Before | After |
|-------|--------|-------|
| diff-audit errors | n | n |
| artifact-lint errors | n | n |
| mutation score (<pkg>) | n% | n% |
| tests | n | n |

Design audit: <high n → 0, medium n | skipped, no web file changed>
Fixed: <one line each>
Kept deliberately: <finding — why it is correct as it stands>
Needs you: <finding this command must not decide>
```

## Done When

- [ ] `diff-audit.mjs` and `artifact-lint.mjs` report zero ERRORs, or each survivor is explained in the report
- [ ] Mutation score at or above the configured floor for every touched package, with no disable added to get there (or the step explicitly waived by the user)
- [ ] Durability read done, with each of its five questions answered for the diff
- [ ] `jest --onlyChanged`, `lint` and `typecheck` green after the last edit
- [ ] Every fix is a refactor, deletion, or added test — no behavior changed, no test weakened
- [ ] Report delivered with before/after numbers, not adjectives

## Agent Execution Rules: harden deltas

The constitution's Agent Execution Rules apply in full. Specific to this command:

- A finding you cannot fix honestly is reported, never suppressed. "Needs you"
  is a legitimate and expected section of the report.
- No internal identifiers in anything you write — no FR ids, task ids, or ticket
  keys in comments or test titles (Constitution II). The one allowed form is a
  whole-line `// @traces <feature>-FR-<n>` comment in a test file.
- Deletion is the preferred fix. Reach for it before refactoring, and refactor
  before adding.

## The repair loop has a cap

Every fix-and-re-verify lap is counted:

```bash
node .claude/scripts/run-state.mjs repair
```

It exits 1 at the tenth lap (`SPECKIT_MAX_REPAIR_ITERATIONS`) and leaves
`.specify/run-state.json` at `status: blocked`, `blocking_condition:
repair-loop-exceeded`. Borrowed from BMAD's autonomous build, whose blocking
conditions include "review repair loop exceeded 5 iterations".

When it fires, stop and report. A cycle that has not converged in ten laps is
not one lap from converging: either a finding is wrong, or the requirement is,
and both are decisions rather than another edit.
