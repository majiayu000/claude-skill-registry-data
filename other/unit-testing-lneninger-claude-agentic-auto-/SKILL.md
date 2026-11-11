---
name: unit-testing
description: "How to write, run and report unit and integration tests in this repository: the test conventions for .NET (xUnit) and Angular (Vitest), the RED-first workflow, the rule that every resource a test run creates is removed afterwards whether the run passes or fails, and the format of the detailed result report. Use when: writing or running tests, the senior-test-engineer agent starts work, or the user says /unit-testing, 'run the tests', 'write the unit tests', or 'clean up after the tests'."
user_invocable: true
---

# /unit-testing: write, run and report tests without leaving anything behind

This skill holds the responsibilities of the `senior-test-engineer` agent. The agent keeps one boundary: it writes tests and never production code. Everything else lives here.

Read the `test.roots` slot of `.claude/project-profile.md` before placing or searching for a test. Never guess a path from a project name.

## 1. Conventions

**.NET** (suites named by `test.roots`)
- xUnit 2.9, Moq 4.20, FluentAssertions 6.12, EF Core InMemory 9.0.
- Arrange / Act / Assert. Every assertion carries a `because:` clause naming the invariant.
- InMemory databases get a per-test `Guid.NewGuid().ToString()` name. The test class implements `IDisposable` and disposes the context. Ignore `InMemoryEventId.TransactionIgnoredWarning`.
- Real-SQL constraints (unique indexes, cascade) use a LocalDB integration test. Get the database from the project's test resource owner (see section 3, "One owner for every resource"), never from a hand-built connection string and never from the development connection string. If the project has no owner yet, create one first, following `references/resource-owner.md`.
- Class names: `<Sut><MethodOrScenario>Tests`. Prefer narrow-shape DTOs over broad object graphs in assertions.

**Angular** (Vitest)
- Vitest through `@angular/build:unit-test`, TestBed, snake_case test names, signal-aware assertions.

## 2. RED first

Write the test that proves a behavior is missing, run the exact command from the plan (`dotnet test --filter ...` or the Vitest command), and confirm it fails for the right reason: an assertion failure or a missing-symbol error that reflects absent behavior, never an unrelated environment error. Then hand off. Do not implement.

## 3. Cleanup: nothing created by a run survives the run

A run is the whole span from the first resource created to the last result recorded. Every resource the run creates is removed afterwards, **whether the tests pass, fail, error or are aborted**.

What counts as a resource: disposable databases, temp directories and files, scratch fixtures, spawned processes, bound ports, containers, generated output folders, background watchers.

Rules:
1. **Own only what you created.** Track each resource at the moment it is created. Remove only tracked resources. Never remove anything that existed before the run, and never a database the application configuration points at (the destructive-database rule applies: disposable names only, with a suffix such as `_Test_<hex-guid>`).
2. **Remove in a guaranteed path.** In test code use the framework's teardown: `IDisposable` or `IAsyncLifetime.DisposeAsync` in xUnit, `afterEach` or `afterAll` in Vitest, and `try/finally` in scripts. Cleanup that runs only after a pass is a defect.
3. **Remove before reporting.** The shell command that runs the tests is followed by the cleanup in the same command, so a failed test command still cleans up: run the tests, keep the exit code, run the cleanup, then exit with the kept code.
4. **A cleanup failure is a finding, not a silent skip.** If a tracked resource cannot be removed, name it and the reason in the report's Problems section, and leave the test verdict unchanged.
5. **Verify the result.** After cleanup, confirm the tracked resources are gone: the directory is absent, the process has ended, the database no longer lists.
6. **One owner for every resource.** A single object, the test resource owner, creates, names, sets up and removes the resources a run needs: a database, a file, a container, a process or a queue. Each kind is one implementation behind the owner. Callers never do any of those steps by hand.

   The owner follows fixed code standards and six learned rules: the disposable-name rule, remove first when a setup fails, always dispose the owner, no step after the owner's setup in a test class's own setup, a failed removal named and never skipped, and no removal by pattern.

   Two checks keep it honest. The source-scan guard is a test that fails any file outside a closed, justified allow-list that creates, names or removes a resource by hand. The runtime leftover check counts this run's resources after the suite and fails the suite if any remain.

   The full contract, the reason for each standard, what each check cannot see, and what to do when the project has no owner yet are in `references/resource-owner.md`. Read it before writing code that creates a resource.

## 4. The report: results, not resources

The user needs the detailed report. The temporary resources are an implementation detail and **must not be listed in the report**, except as a Problems entry when one could not be removed (rule 4).

Report these, quoting real output and never summarizing from memory:
- **Command run**, exactly as executed.
- **Totals**: passed, failed, skipped, duration.
- **Per test**: name and outcome. For each failure, the assertion message, expected versus actual, and the file and line.
- **Behavior pinned down** by each new test, in one sentence.
- **RED verdict** when in the RED phase: "this is RED for the right reason" with the quoted failure, or a flag when it failed for an unexpected reason.
- **Problems**: anything unexpected, including a resource that could not be removed.
- **Cleanup**: one line only: "all resources created by this run were removed", or the Problems entry.

## Anti-patterns
- Cleanup placed after the assertion in the same method, so a failing assertion skips it.
- Reporting a table of created databases, folders or ports in place of results.
- Removing a resource by pattern or wildcard instead of by the tracked handle.
- Running a destructive command against a name that lacks a disposable suffix.
- Creating, naming or removing a database, folder, container, process or queue inside a test instead of asking the project's test resource owner.
