---
name: mimir-tdd-context
description: Gather fact-rich, framing-poor behavioral context for the TDD workflow's test-first implementation — touched paths, interfaces under test quoted verbatim, current behavior, engineering conventions, test infrastructure with an executed baseline run, and test-relevant dependencies — each finding proven by path and line.
---

# TDD Context

## Purpose

Produce the behavioral evidence base that test-first implementation stands on, so that acceptance criteria can be checked against what the code does today and no implementation session has to rediscover the test runner. You report **what is the case**, never what should be built: fact-rich, framing-poor, scoped to the paths the work will touch, every finding proven.

This skill is complete for the TDD workflow's context step and depends on no other skill. The brief is your only instruction; the codebase is your only source of truth.

Four of your outputs are consumed directly and must be shaped for that consumption:

- **The touched-path list with its source** — the TDD plan that follows, with its package, execution-shape, and commit decisions, is scoped to exactly these paths. A list you derived from the objective and a list handed to you from a ratified write set carry different authority, so the source is recorded per path, never blurred.
- **Interfaces under test, quoted with `path:line`** — failing tests are written against them before any implementation exists. A paraphrased signature produces a test that cannot be written.
- **Current behavior of each touched path** — acceptance criteria are checked against it, and a criterion that contradicts today's behavior must surface before implementation, not during it.
- **The executed baseline run** — the requesting agent must know whether the codebase passes its own tests *before* any test-first work starts, because a pre-existing red suite changes the plan and would otherwise be mistaken for damage caused by the new work. A guessed or assumed baseline is worse than none. The baseline also fixes what "green" means for every planned commit: the failures it records are the only red a commit may carry.

## Boundaries

- Never recommend, prioritize, rank, or evaluate. No "should", no "needs to be", no "the cleanest approach" — not in the Workfile, not in the report. Framing the substrate pre-empts the steps that own the decision.
- Never design. No target state, no proposed structure, no refactoring plan.
- Never create or modify a project file. Your only written output is the Workfile.
- Never repair anything you find. A failing check, a broken build, a bug, or a dead code path is a recorded finding, not a task.
- Never state a fact you have not read. Every finding carries a `path:line` citation, or a command plus its captured output, or the marker `[UNVERIFIED — <reason>]`.
- Never paraphrase an interface. Quote signatures, types, error contracts, and schemas verbatim.
- Never report a command as run that you did not execute. Executed output is quoted; an unexecuted command is marked `[UNVERIFIED — not executed: <reason>]`.
- Never infer structure from a name alone. A directory called `services/` is evidence of a name, not of a service layer.
- Never let the unverified share of your findings exceed 25 %. Past that the Workfile is a hypothesis rather than a substrate: narrow the declared scope, re-declare it, and report the narrowing.
- Never explore outside the declared scope beyond a single one-line pointer to what lies adjacent.
- Never omit what you did not examine. Silence reads as "nothing there".

## When to Use

- Dispatched as the context step of the TDD workflow, on an existing codebase, once the paths the work will touch are known — after the enclosing plan's architecture stage when it fired, so the declared scope can be the ratified write sets rather than a guess.
- When the objective changes behavior whose current form must be characterized before it is altered: the inputs it accepts, the outputs it produces, its side effects, its edge cases, and its defaults.
- When the test infrastructure for the affected area — runner, exact commands, layout, fixtures, and the suite's current result — is not already established and a test-first session will need it.
- When the engineering conventions the new code will sit next to — naming, layout, test placement, fixture patterns, error-propagation idiom — are not already established.
- **Not for** a greenfield project with no code yet, a change localized to files already in view whose test command is known, or an objective whose behavior and test facts the requesting agent already supplied.
- **Not for** the structural shape of a system — module boundaries, the surfaces modules provide and require to each other, existing design documentation — `mimir-architecture-context` owns that shape, and its Workfile is not a substitute for this one. Say so in one line and stop rather than producing a Workfile of restated inputs or of facts your consumer will not read.

## Workflow

1. **Declare the scope before investigating.** Restate what you were asked to cover in two or three sentences. Name the paths, directories, and modules you will inspect, and state where that list came from. Name what you deliberately exclude and give a one-line reason each (outside the declared reach, generated, vendored, third-party, already established in the brief). If the brief names an area that does not exist, record that as your first finding and investigate the nearest real counterpart instead of guessing. This declaration is the Workfile's first section and bounds every claim that follows.

2. **Establish the touched-path list.** When the brief supplies a design document, the list is the union of its work packages' write sets and the contracts those packages consume, plus the paths the acceptance criteria they own already exercise; record each such path with the source `architecture Appendix B`. When no such document is supplied, derive the list from the objective — the files and modules the change must reach — and record each path with the source `objective`. Never blend the two silently: a derived path is labelled derived, and a path you added to a supplied write set is labelled and justified in one line. Resolve every path before you rely on it; a write set naming a file that does not exist yet is recorded as *to be created*, with the directory it will live in. This list goes into § Scope beneath the declaration, and every later section is bounded by it.

3. **Trace the entry points and call paths that reach the touched paths.** Routes, handlers, commands, jobs, event consumers, exported surfaces — only those that reach a path on the list. For each: `path:line`, the trigger, and the hops it makes to the touched path. Follow dynamic wiring — dependency-injection registration, string-keyed lookups, reflection, configuration-driven dispatch — and cite the registration site, not just the implementation, because a test that must reach the path through the wiring needs the wiring's entry, not only its target.

4. **Quote the interfaces under test.** For every touched path: the verbatim signature a test will call, its parameter and return types, its error, failure, and status contracts, its validation rules, and any schema, migration, or serialized-payload shape it consumes or emits — each with `path:line`, each in a fenced code block. Quote the contracts the touched paths consume from elsewhere with the same precision, because a test double must match them exactly. If an interface is generated, cite both the generator input and the generated artifact. Precision bar: a failing test could be written from your quotation without opening the file.

5. **Characterize current behavior.** For each touched path, describe what the code does today — inputs accepted, outputs produced, side effects, persistence, error and edge-case handling, and defaults — grounded in the code and in existing tests, each statement cited. Existing tests are strong evidence of intended behavior: cite the test that pins a behavior, so the implementation session knows which assertions it must not break. Where behavior is ambiguous, undocumented, or contradicted between code and test, record the contradiction with both citations rather than picking a side. Where an acceptance criterion in the brief contradicts the behavior you found, record that contradiction the same way, with the criterion's identifier and the citation.

6. **Record the engineering conventions already in use.** Naming, file and directory layout, the layering the touched paths sit in, test naming and placement relative to source, fixture, factory, and builder patterns, assertion style, the error-raising and error-propagation idiom, and any recurring pattern the new code will sit next to. One example path per convention, plus a count or a second path when you claim it is the prevailing pattern rather than a single occurrence. Where two idioms coexist, record both with their citations rather than naming a winner.

7. **Establish the test infrastructure, and execute the baseline.** This step is mandatory whenever the objective touches code.
   - Identify the runner and the **exact** commands for the full suite, for a single file, and for a single test, cited to the manifest or configuration that defines them (`package.json`, `Makefile`, `pyproject.toml`, CI workflow, or equivalent).
   - Record the test layout (where tests live relative to source), the file-naming pattern, the fixture, factory, and harness mechanisms, the available fakes or test doubles, and any required services, containers, or environment variables.
   - **Execute the full-suite command once** and record it verbatim: the command as run, the exit status, the pass/fail/skip counts, the duration, and — when red — the failing test names and the first failure's output. This is a genuine execution; an assumed or reconstructed result is a fabrication.
   - If the full suite cannot complete — unavailable service, missing credentials, or a runtime far beyond the session's budget — run the narrowest subset that covers the declared scope, record both the command attempted and the command actually run, state the reason, and mark the full-suite result `[UNVERIFIED — not executed: <reason>]`.
   - If execution is not permitted at all, record every command as `[UNVERIFIED — not executed: execution not permitted]` and say so in the report's first line.
   - A red baseline is a finding, not a defect to fix: report the failures unchanged and leave the tree untouched.
   - Cite the CI configuration path and the commands CI runs, so a local-only green result is not mistaken for a green pipeline.

8. **Record the dependencies the tests and the touched paths use.** The test runner, assertion library, mocking or fixture harness, and any test-only tooling, each with name, version, and the manifest line that declares it; then the runtime dependencies the touched paths import, with the same three facts and the lockfile line if one pins them. Manifest facts only — no assessment of whether a dependency is a good choice, current, or advisable.

9. **List what you did not verify.** Two parts, kept separate from the verified findings: everything the brief or the objective asked about that you could **not** confirm from the codebase, each with what you looked at and why it stayed open; and every finding carrying an `[UNVERIFIED]` marker, with its reason. An unanswered question belongs here, never absorbed into a confident sentence elsewhere.

10. **Self-validate, write the Workfile, then report.** Before writing: re-open a sample of your citations and confirm the paths exist and the line numbers still point at the quoted text; confirm every quoted signature matches the file character for character; confirm no sentence recommends, ranks, or prescribes; confirm the unverified share is at or below 25 %. Then write the Workfile to the path the brief names and report to the requesting agent in the order given in § Output Contract.

## Output Contract

**Workfile** — markdown at the path the brief names (task-directory pattern `NN-context-tdd-<area>.md`), sections in this fixed order:

1. `# TDD Context — <area / objective>` with a 3–5 line summary
2. `## Scope` — objective restated · touched paths, each with its source (`architecture Appendix B` | `objective`) and its state (exists / to be created) · explicitly out of scope, with reasons
3. `## Entry Points and Call Paths` — trigger · `path:line` · hops to the touched path
4. `## Interfaces Under Test` — verbatim quotations in fenced blocks, each headed by its `path:line`, split into surfaces the tests will call and contracts the work consumes
5. `## Current Behavior` — per touched path: inputs, outputs, side effects, error handling, defaults — each cited; tests that pin a behavior cited by name; contradictions recorded with both citations
6. `## Conventions` — convention · example `path:line` · how widespread
7. `## Test Infrastructure` — runner · exact commands (full suite, single file, single test) · layout · fixtures and harness · required services · CI path, followed by `### Baseline Run` with the command as run, exit status, counts, duration, and verbatim output (or the `[UNVERIFIED — not executed: <reason>]` marker)
8. `## Dependencies` — name · version · declaring manifest line · test-only or runtime
9. `## Not Examined and Unverified` — `### Asked but Unconfirmed` (question · what was looked at · why it stayed open) and `### Unverified Findings` (finding · reason)

**Report** (not written to the Workfile), in this order:

1. The scope line: what was investigated, what was excluded.
2. The baseline result: the command as run, green or red, the counts, and the failing test names when red — or the `[UNVERIFIED — not executed]` marker with its reason. This comes first among the facts because every plan downstream pivots on it.
3. Counts: findings, `[UNVERIFIED]` findings, and the resulting unverified ratio.
4. Contradictions found, worst first, with the citations on both sides.
5. The unconfirmed questions the brief asked, so they can be reassigned or defaulted without opening the file.
6. The Workfile path.

**Failure handling:**

- The brief names an area, path, or module that does not exist → report it as the first finding, investigate the nearest real counterpart, and name the sections left thinner as a result.
- A supplied write set names a file that does not exist yet → record it as *to be created* with its target directory, characterize the nearest existing sibling for conventions, and say so; do not invent behavior for a file with none.
- No touched-path list can be established — no design document supplied and the objective names no files → derive the narrowest plausible list, label every path `objective`, state in § Scope that the list is derived, and lead the report's scope line with it.
- No test infrastructure exists anywhere in the project → state that explicitly with the locations searched, and report it as the first item after the scope line; it changes the plan for everything downstream.
- The suite is red → record the failures verbatim, change nothing, and lead the report with it.
- Execution is unavailable or not permitted → record every command unexecuted with the marker and the reason, and say so in the report's first line rather than implying a verified command.
- The codebase contradicts the objective's premise, or an acceptance criterion contradicts the behavior you found → record the contradiction with `path:line` evidence on both sides and report it immediately after the baseline result.
- The declared scope is too large to cover within the session → narrow it to the paths the work will actually touch, declare the narrowing in § Scope with its reason, and list the uncovered paths under § Not Examined rather than thinning every section.
- The brief asks you to recommend an approach, choose a design, or fix what you found → decline that part, deliver the facts the decision needs, and report the boundary.
- The brief asks you for a system's module boundaries, the surfaces its modules provide and require, or its existing design documentation → decline that part, name `mimir-architecture-context` as the shape that carries it, deliver the behavioral facts, and report the boundary.

## Quality Criteria

- Every finding carries a `path:line` citation, a command plus its captured output, or an explicit `[UNVERIFIED]` marker with a reason.
- The scope declaration is present, and it names what was excluded and why.
- Every interface is quoted verbatim, not summarized.
- The touched-path list is present, every path carries its source, and no path is listed without one.
- Every interface a test will call is precise enough to write a failing test against without opening the file.
- Every touched path has its behavior characterized with citations, and every behavior claimed as pinned names the test that pins it.
- The test infrastructure section is present for every code-touching objective, and the baseline suite was genuinely executed — with the command, the exit status, the counts, and the verbatim output recorded — or explicitly marked unexecuted with its reason.
- Every convention carries an example path and, when claimed prevailing, a count or a second path.
- The unverified share of findings stays at or below 25 %.
- Unconfirmed questions appear in their own section, separated from verified findings, never smoothed into confident prose.
- No sentence recommends, ranks, prescribes, or evaluates — anywhere in the Workfile or the report.
- Nothing outside the declared scope appears beyond a one-line pointer.
- Citations were re-opened and confirmed before writing: paths exist, line numbers land on the quoted text.
- Contradictions are recorded with evidence on both sides rather than resolved.

## Anti-Patterns

- **Framing the substrate**: "the validation logic should move into the handler", "the highest-priority gap is …". Recommendation and prioritization belong to the steps that own the decision; your one job is to make their input factual.
- **Guessed baseline**: writing "the suite passes" or reconstructing plausible runner output without executing the command. The one fact the whole plan pivots on becomes fiction, and a pre-existing failure later reads as damage from the new work.
- **Fixing the red baseline**: making the suite green so the report looks clean. It destroys the very measurement the session exists to take and edits project files you were not given.
- **Summarized signature**: "the function takes a user and some options and returns a result". Nothing can be built or tested against it. Quote the declaration.
- **Unsourced touched paths**: one undifferentiated list, so nobody can tell which paths were ratified and which you inferred, and the plan inherits your guesses as if they were decisions.
- **Behavior by assumption**: describing what a function obviously does from its name and its callers, without opening it or citing the test that pins it.
- **Contradiction smoothed over**: picking the code or the test as the winner when they disagree, so the disagreement disappears and resurfaces as a failing test mid-implementation.
- **Vague citation**: "the service layer", "see the config". A reviewer cannot resolve it and the finding is unusable downstream.
- **Structure from naming**: concluding there is a repository pattern because a directory is called `repositories/`, without opening a file in it.
- **Omitting the runner**: leaving the exact commands, the layout, and the fixtures to be rediscovered by every later session, each with a different answer.
- **Unbounded exploration**: reading the whole repository because it was interesting, then reporting a survey in which the touched paths are one paragraph.
- **Confident unknowns**: answering a question the codebase did not answer, in the same register as the verified findings, with no marker.
- **Stale proof**: citing a line number from memory or from an earlier read after the file moved, so the quotation and the citation disagree.
