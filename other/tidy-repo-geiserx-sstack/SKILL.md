---
name: tidy-repo
description: Tidy an established repo end to end without changing what it does. It audits, deletes, restructures, refreshes the living docs and leaves guards so the repo stays clean. Use only when invoked explicitly.
disable-model-invocation: true
argument-hint: "[REPO_PATH ...]"
---

# tidy-repo

Sweep one or more repos so that every file reads as plainly as the problem allows. The **contract** stays fixed: what users, callers and other systems can observe before the sweep is exactly what they observe after it. Everything behind the contract is open to change.

With no argument, work on the repo that contains the current directory. With several repos, give each one its own lane. A lane owns one repo, and no two lanes touch the same files.

Run it as a workflow. Pin every agent to the strongest model the session allows. Fixers work in isolated worktrees. The agent that writes a change never approves it.

## Steps

### 1. Map the repo

Read the repo's own `AGENTS.md`, `CLAUDE.md` and `CONTRIBUTING.md` first. They win over this skill where the two disagree. Then map:

- the entry points;
- the module boundaries;
- which module calls which;
- where state lives;
- how the repo is built, tested, linted and released.

Mark what is out of scope:

- vendored code;
- generated files;
- lockfiles, which change only through their tool;
- anything the repo's instructions protect.

Done when every source directory is either in the map or listed as out of scope, with a reason.

### 2. Lock the contract

1. **Record the baseline.** Run the full test suite, lint, type check and build, and record what passes. A red baseline is reported before you change anything. Fixing it becomes the first unit of work.
2. **Write the contract inventory** as a file in the lane's scratch dir. It lists everything observable from outside:
   - CLI commands, flags and exit codes;
   - public functions and types;
   - HTTP routes and their request and response shapes;
   - config keys and env vars;
   - file and wire formats;
   - log lines that other tools parse;
   - output that users or scripts read.
3. **Pin down current behaviour where tests don't.** Any code you plan to restructure that has no test covering its observable behaviour gets a test first. That test records what the code does today, even where today's behaviour looks wrong. It lands in its own PR before the restructure.

Done when the baseline is recorded, the contract inventory exists, and every part you plan to restructure is covered by a test that passes on the current code.

### 3. Audit

Run independent auditors in parallel, one per lens, across the whole mapped scope. Each finding states:

- the file and line;
- the problem;
- the evidence;
- whether its fix stays inside the contract;
- the smallest change that removes it.

A separate verifier tries to disprove each finding against the code, its callers, its tests and the git history. Only verified findings go forward, deduplicated by root cause. Keep auditing in rounds until two consecutive rounds find nothing new. That is the **dry** state.

The lenses are listed under "Audit lenses" below.

Done when the audit is dry, and every verified finding is tagged with its lens and with *inside the contract* or *changes the contract*.

### 4. Plan the units

Order the work so each step makes the next one smaller:

1. **Delete** dead code, dead files, dead flags, unused dependencies and stale config.
2. **Merge duplicates** into one implementation.
3. **Restructure** modules, boundaries and types.
4. **Polish** naming and the readability of individual files.

Cut the work into **units**. A unit is one theme, small enough to review in one sitting, and it ends in a passing check. Keep purely mechanical edits (moves, renames, formatting) in units apart from logic edits.

Sort findings that change the contract into two groups:

- **Clear bugs.** These are the only deliberate contract changes the sweep makes. Each gets its own unit, after the restructure units have landed. In that unit, change the behaviour-recording test from step 2.3 to the correct expectation, add a regression test, record the change in the contract inventory, and name it a bug fix in the PR title. Every other unit leaves the contract exactly as the inventory states it.
- **Decisions.** These need a product or design choice. They go to the report, unimplemented.

Done when every verified finding belongs to exactly one unit or the decisions list.

### 5. Execute

For each unit, in order:

1. Make the change in a worktree.
2. Run the baseline checks and the tests from step 2.3. The unit's pass count must be at least the baseline's.
3. A fresh reviewer reads the diff against the contract inventory and the unit's findings.
4. Open the PR with the problem first and the change second. Land it through the repo's own gate.
5. Rebase the remaining units on the new main.

Delete only on **two signals**. Before removing anything as dead, confirm it with at least two independent sources: a reference search, the git history, config and CI files, the test suite, the framework's conventions for things it loads by name, and the docs. Treat one signal alone as a lead, never as proof.

Done when every unit has merged or is listed in the report as blocked, with the reason.

### 6. Leave guards

For every class of problem the sweep removed, add the strongest check that keeps it from coming back. Strongest first:

1. a type that makes the bad state impossible to write;
2. a lint rule or CI step that fails the build;
3. a single shared helper that the surrounding code already calls;
4. a runtime check at the boundary.

Prove each guard can fail: run it once against the old pattern and watch it go red. Guards land as their own units. A formatter, a linter config, an unused-export or dead-file check, a file-length check, and dependency pinning are the usual candidates. Pick only the ones the sweep actually justified.

Done when every lens that produced verified findings either has a guard proven red, or is listed with the reason why no mechanical guard fits.

### 7. Refresh the docs

List every Markdown file, docstring set, CLI help text and example in the repo. Classify each as one of two kinds:

- **Living:** it describes the repo as it is now. README, CONTRIBUTING, `AGENTS.md` and `CLAUDE.md`, guides under `docs/`, API references, CLI help, examples, the changelog's unreleased section.
- **Historical:** it records a moment. Audits, incident reports, research notes, design records, dated plans, released changelog entries.

Run `docs-loop` over the repo in dry-run mode, and use its findings as the doc work list. Check each living doc against the code after step 5, not before. Confirm every path and link resolves. Run the commands a doc shows only when they only build, test, lint or read. Check any command that deploys, deletes, publishes or reaches outside the repo by reading it against the code instead of running it. Rewrite what changed, and fix readability in the same pass. Historical docs keep their text; only their broken links get repaired. A doc you cannot classify counts as historical and goes in the report.

Update the repo's agent instructions (`AGENTS.md`, `CLAUDE.md`) with the map from step 1 as it now stands, the real build and test commands, and the conventions the sweep settled on. The next agent then keeps the new shape without having to rediscover it.

Run `readable` over every doc you rewrote if it is installed. Otherwise reread each one and cut filler, repeated points and vague wording.

Make all of these edits before you open the PR. Then land the docs PR through the repo's gate, like any other unit.

Done when the docs PR has merged, every living doc on main matches the code, and every unclassified doc is in the report.

### 8. Report

Commit a report under the repo's docs folder, or wherever the repo keeps reports. It covers:

- the coverage: the map, the exclusions and the lenses run;
- every merged PR, with its link;
- the guards added, each with its red proof;
- the blocked units and the reason for each;
- the decisions list, with evidence and proposed acceptance criteria for each;
- the before and after contract inventories, plus a line saying they match.

Done when the report is pushed and its URL is in your reply.

## Audit lenses

- **Correctness.** Logic errors, off-by-ones, unhandled cases, races, resource leaks. Trace each bug to where it starts, fix it there, and search for the same pattern elsewhere.
- **Security.** Injection, path traversal, secrets in code or history, unsafe deserialisation, missing authorisation, permissive defaults, dependencies with known advisories.
- **Performance.** Repeated work in hot paths, N+1 queries, unbounded memory, blocking calls in async code. A claim needs a measurement or a clear complexity argument.
- **Dead weight.** Unreachable code, unused exports, parameters and flags, commented-out code, stale feature toggles, orphan files, unused dependencies.
- **Duplication.** Two implementations of one idea. Keep the better one, move every caller over, and delete the other in the same unit. Leave no compatibility shim for internal callers.
- **Structure.** Look first for a restructure that makes a whole branch, mode or layer disappear. That beats moving the same code around. A file over about 1000 lines gets split along its natural seam. Spread-out booleans and lifecycle checks become one state type or table. Choices made by branching across files become one registry or one discriminated type.
- **Reader load.** Count the hops between a question and its answer in the code. Inline wrappers that have one caller and adapters that have one implementation. Prefer return values to mutation and locals to shared state. Derive values instead of keeping two copies in sync.
- **Boundaries and types.** Parse and validate at the edges (CLI, config, network, files, external APIs) into typed values, and trust those types inside. Remove repeated internal checks the edge already guarantees. Replace casts that bypass the type checker with real narrowing. Make invalid states impossible to construct.
- **Error handling and logging.** One way to report errors per layer. Every error carries context. Nothing is swallowed silently. No PII or secrets reach a log.
- **Naming and consistency.** One name per concept across code, docs and config. Files, functions and modules follow the convention the repo already uses most.
- **Comments.** Keep comments that explain why. Delete comments that restate the code. A comment that guards a constraint ("do not reorder", "must match X") becomes a test or check where one fits.
- **Tests.** Tests that pass whatever the code does, tests of private internals that block restructuring, flaky tests, missing coverage of the contract. Every test must be able to fail.
- **Dependencies.** Unused, duplicated, unpinned or outdated packages. Read the full lockfile diff of every change, because one bump can quietly downgrade another package.
- **Build, CI and config.** Dead workflows, unpinned actions and images, steps that can never fail, config keys nothing reads, environment drift between local and CI.
- **Repo hygiene.** Committed build output, gaps in `.gitignore`, stray scripts at the root, stale TODOs with no owner, mismatched license headers, a README that has grown into a manual.
