---
name: unit-tests
description: >
  Systematically add unit test coverage for existing source files in any project,
  tracked across sessions. Use ONLY when the user runs /unit-tests <scan|plan|write>
  — do NOT trigger on ordinary one-off requests to write a test.
---

# Unit Tests

## State files

- `.claude/skills/unit-tests/files.json` — source file inventory + project test config
- `.claude/skills/unit-tests/plan.md` — pending test cases and blockers

Outside of write mode, these two files are the ONLY files this skill may write.
Write mode may additionally create or edit test files in the configured test location.

## Constraints (all modes)

- Never modify production code. If a file is untestable as-is (hidden dependencies,
  static calls, no seams), record a blocker in `plan.md` and move on.
- No new dependencies without asking.
- Match existing test conventions: before writing anything, read 1–2 existing test
  files and mirror their naming, structure, and mocking style. If the project has
  no tests at all, ask the user which framework to use — do not pick one.
- The ONLY command this skill may run is the project's test command from
  `files.json` config, scoped to the test file just written. No git, no dev
  servers, no other commands.
- When editing an existing test file, append new tests only — never rewrite,
  rename, or delete tests that are already there.

## Mode selection

Argument `scan`, `plan`, or `write` selects the mode.
If the user names a specific file alongside the command, run plan mode then
write mode for that file only — skip the queue order.
No argument and no named file: ask which mode to run — do not read any files first.

## Mode: scan — build or update the file inventory

1. Detect project config (first scan only), store under `"config"` in `files.json`.
   If the repo has several testable projects (e.g., backend and frontend), ask
   the user which to include and store one config block per root. For each root:
   - Test framework and location: look for an existing test project or directory
     (`*Tests.csproj`, `__tests__/`, `*.test.ts` siblings, `tests/` + pytest config)
     and confirm the framework from `package.json` / `.csproj` / `pyproject.toml`.
   - Test command template with a placeholder, e.g.
     `dotnet test --filter "FullyQualifiedName~{TestClass}"` or
     `npx vitest run {testFile}` or `pytest {testFile}`.
   - Test file naming convention, taken from existing test files.
   - If anything is ambiguous or absent, ask the user.
2. Glob source files under each root and classify each by test value:
   - `high` — pure logic: utils, helpers, domain/service classes with injectable deps
   - `medium` — controllers, handlers, hooks with mockable dependencies
   - `skip` — config, generated code, type-only files, thin glue, markup-only
     components. Read a sample file when unclear from the name.
   Record `skip` files too — it stops later scans from re-classifying them, and
   plan mode never touches them.
3. For each `high`/`medium` file, record its existing test file (mapped by naming
   convention) or `null`.
4. Read `files.json` (missing → `{}`). Add new files, keep existing entries
   unchanged, delete entries whose file no longer exists. Write it, report changes.

Schema — paths relative to repo root:
```json
{
  "config": {
    "JobTrackerApi": {
      "framework": "xunit",
      "testDir": "JobTrackerApi.Tests",
      "testCommand": "dotnet test --filter \"FullyQualifiedName~{TestClass}\"",
      "naming": "{ClassName}Tests.cs"
    }
  },
  "files": {
    "JobTrackerApi/Services/LocalStorageService.cs":
      { "value": "high", "testFile": null, "planned": null, "tested": null }
  }
}
```

## Mode: plan — decide test cases, write no tests

1. Read `files.json`. If missing or empty, run scan mode first.
2. Process files with `"planned": null` one at a time, highest value first —
   at most 5 files per run. For each: read the file (and its existing test file,
   if any — plan only cases not already covered), append its test cases to
   `plan.md`, set the file's `planned` date.
3. Checklist for choosing cases:
   - Test public behavior only — never private implementation details.
   - Cover happy path, boundary values, and error/exception paths.
   - For each nondeterministic dependency (clock, network, filesystem, random,
     database) name the mock or seam to use.
   - One behavior per case; name by the project's convention
     (e.g. `Method_Scenario_ExpectedResult`).
   - Do not test framework code (EF, React, the test framework itself).
4. If the file cannot be tested without production changes, record a `BLOCKED`
   block explaining why instead of test cases.
5. Report what was planned and what remains.

Entry format in `plan.md` — one `##` block per source file:

```markdown
## JobTrackerApi/Services/LocalStorageService.cs
- Mocks: filesystem via temp directory; IConfiguration stub for UploadsPath
- [ ] SaveAsync_ValidFile_ReturnsStorageKey
- [ ] SaveAsync_EmptyFile_Throws
- [ ] DeleteAsync_MissingKey_DoesNotThrow
```

Blocked entry format — `BLOCKED` goes in the heading so write mode can skip it:

```markdown
## JobTrackerApi/Helpers/TimeHelper.cs — BLOCKED
- Calls DateTime.Now directly, no injectable clock; needs a production refactor first
```

## Mode: write — one source file per pass

1. Read `plan.md` with `limit: 30` — only enough to get the FIRST non-blocked block.
2. Read the source file and one existing test file for a similar target; mirror
   its structure and mocking style.
3. Create the test file per the naming convention (or append to the existing
   test file if one is recorded) and implement the listed cases. If a case no
   longer matches the source (member renamed or removed), drop or adjust it and
   say so in the report.
4. Run the test command from the config block for the file's root, scoped to
   this test file. On failure, fix the TEST code only — after 3 failed attempts
   on a case, mark it `FAILING:` in `plan.md` and move on. If a failure reveals
   a real bug in production code, report it, mark that case with a `BUG:` note,
   and leave the production code untouched.
5. When all cases pass: remove the block from `plan.md`, set the file's `tested`
   date and `testFile` in `files.json`. If `BUG:`/`FAILING:` cases remain: keep
   only those cases in the block, add `— BLOCKED` to its heading, and still
   record `testFile` for the tests that passed.
6. Report cases written and test results, state how many blocks remain, then
   STOP and wait for approval before the next file.
