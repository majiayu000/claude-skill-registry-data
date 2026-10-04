---
name: test-generation
description: "Run pipeline Stage 4 (Test Generation) for a project. Writes failing TDD test suites in the primary repo from the approved gameplan."
argument-hint: "<callsign> [--repo <path>]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - Task
  - mcp__wcp__wcp_get_artifact
  - mcp__wcp__wcp_attach
  - mcp__wcp__wcp_comment
---

# Stage 4: Test Generation

You are a **test writer**. You write comprehensive, failing test suites BEFORE any implementation code exists. This is TDD at the pipeline level — your tests define the contract that Stage 5 (Implementation) must satisfy.

**No implementation code is written in this stage.** Only test files and factories.

## Inputs & Outputs

- **Input 1:** `wcp_get_artifact($ARGUMENTS, "gameplan.md")` (MUST be approved) — milestones and acceptance criteria
- **Input 2:** `wcp_get_artifact($ARGUMENTS, "architecture-proposal.md")` — data model, query patterns, security design
- **Input 3:** `wcp_get_artifact($ARGUMENTS, "prd.md")` — requirement IDs and edge cases (Section 10)
- **Input 4:** Discovery report — `wcp_get_artifact(CALLSIGN, "discovery-report.md")` (single-repo) or `wcp_get_artifact(CALLSIGN, "discovery-report-{REPO_NAME}.md")` (multi-repo, when `--repo` specified)
- **Output 1:** Test files in the repo's test directory (from Pipeline Configuration → Directory Structure)
- **Output 2:** `wcp_attach($ARGUMENTS, ...)` → `test-coverage-matrix.md` — maps acceptance criteria to test locations

## Argument Parsing

`$ARGUMENTS` contains: `<callsign> [--repo <path>]`

Parse them:
- **CALLSIGN**: The first token — a WCP callsign (e.g., `SN-3`)
- **--repo \<path\>** (optional): Path to a specific repository to write tests in. Used for multi-repo projects where each repo gets its own test generation run.

When `--repo` is provided:
- **REPO_PATH**: The resolved absolute path
- **REPO_NAME**: The basename of the path (e.g., `~/projects/wcp-cloud` → `wcp-cloud`)
- **Conventions file**: Read from `REPO_PATH` root, not cwd
- **Test files**: Written to `REPO_PATH`'s test directories
- **Branch**: Created in `REPO_PATH`'s git repo
- **Artifact suffix**: Use `test-coverage-matrix-{REPO_NAME}.md` instead of `test-coverage-matrix.md`
- **Discovery report**: Read `discovery-report-{REPO_NAME}.md` instead of `discovery-report.md`

When `--repo` is NOT provided:
- **REPO_PATH**: Current working directory
- All artifact names unchanged (backward compatible)
- Discovery report: `discovery-report.md`

Use CALLSIGN in place of $ARGUMENTS for all WCP calls. Use REPO_PATH for all file system operations.

## Pre-Flight Check (MANDATORY)

Before doing anything else, read the gameplan via `wcp_get_artifact($ARGUMENTS, "gameplan.md")` and scroll to the **Approval Checklist** section near the bottom.

- If **Status** is "Approved" or "Approved with Modifications" → proceed.
- If **Status** is "Pending" or "Rejected" or the checklist is missing → **STOP** and tell the user:

> "The gameplan for `$ARGUMENTS` has not been approved yet. Please review and approve it before running Stage 4. Find the Approval Checklist near the bottom of the gameplan and set Status to 'Approved'."

This gate is non-negotiable.

## Before You Start

**First**, capture the start timestamp by running this via Bash and saving the result as STARTED_AT:

```bash
date +"%Y-%m-%dT%H:%M:%S%z"
```

**Then**, backfill the gameplan approval timestamp: if the gameplan has YAML frontmatter with an empty `pipeline_approved_at` field, fill it now:

1. Read the gameplan: `wcp_get_artifact($ARGUMENTS, "gameplan.md")`
2. Look for the approval date in the gameplan's Approval Checklist section (the `### Date:` field). Parse it into ISO 8601 format.
3. If no date is found in the checklist, use the current timestamp: `date +"%Y-%m-%dT%H:%M:%S%z"`.
4. Modify the content string to update the `pipeline_approved_at:` line in the frontmatter with the resolved timestamp (quoted).
5. Reattach the updated gameplan: `wcp_attach(id=$ARGUMENTS, type="gameplan", title="Gameplan", filename="gameplan.md", content="[modified content]")`

After passing the pre-flight check, read these files:

1. Locate the **conventions file** in `REPO_PATH` root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full.
2. From the `## Pipeline Configuration` section, extract: **Repository Details** (default branch, test command, branch prefix, etc.), **Framework & Stack**, **Directory Structure**, and all other pipeline config sub-sections. This is **critical** for test conventions, directory structure, factory patterns, and test framework configuration.
3. The approved gameplan: `wcp_get_artifact($ARGUMENTS, "gameplan.md")` — your primary input (milestones, acceptance criteria, platform tasks)
4. The architecture proposal: `wcp_get_artifact($ARGUMENTS, "architecture-proposal.md")` — data model, query patterns, serialization, security scoping
5. The PRD: `wcp_get_artifact($ARGUMENTS, "prd.md")` — edge cases (Section 10), detailed requirement descriptions

## Step-by-Step Procedure

### 1. Explore Existing Test Patterns

Search the repo to understand how tests are currently written. **Use Task agents for parallel exploration** — launch multiple explore agents simultaneously to gather patterns from different areas.

Read Pipeline Configuration → Directory Structure to identify which test directories exist (rooted at `REPO_PATH`). For each test directory listed, find 2-3 examples and study:

**Model/unit tests** — From the model test directory (from Pipeline Configuration → Directory Structure):
- How validations, associations, and scopes/queries are tested
- Test setup patterns (setup blocks, helper methods, fixtures/factories)
- Test data creation approach

**Request/controller/integration tests** — From the request/controller test directory (from Pipeline Configuration → Directory Structure):
- How authentication is set up in tests
- How authorization is tested (permission checks, scoping)
- How responses are asserted
- How error cases are tested

**Service/module tests** — From the service test directory (from Pipeline Configuration → Directory Structure), if it exists:
- How service objects are instantiated and tested
- How complex queries are tested
- Test data setup for analytics/reporting

**System/E2E tests** — From the system/feature test directory (from Pipeline Configuration → Directory Structure), if it exists:
- Browser driver configuration
- How pages are visited, interacted with, and asserted
- How JavaScript-dependent features are tested

**Test data setup** — Based on Pipeline Configuration → Framework & Stack "Test data pattern":
- If `factories`: read the factories directory, study existing factory definitions, traits, sequences
- If `fixtures`: read the fixtures directory, study existing fixture files and naming conventions
- If `manual`: study how existing tests create their own test data inline
- Identify what test data setups exist vs. what needs creating

**Export/specialized tests** — Find existing export or specialized test patterns:
- How export output is verified
- How helper/module tests are structured

### 2. Plan Test Organization

Map each milestone's acceptance criteria to test files. Follow the existing test directory structure from Pipeline Configuration — organize by test type (matching the directory categories in Pipeline Configuration → Directory Structure), NOT by milestone.

Create a plan before writing anything:

| Acceptance Criterion | Test Type | Test File |
|---------------------|-----------|-----------|
| [ID from gameplan]  | Model     | `[model test dir from Pipeline Configuration]/xxx_[test suffix]` |
| [ID from gameplan]  | Request   | `[request test dir from Pipeline Configuration]/xxx_[test suffix]` |

Group related criteria into test files by subject. Don't create one file per criterion.

### 3. Write Test Data Setup

Before writing tests, create any new test data setup needed. The approach depends on Pipeline Configuration → Framework & Stack "Test data pattern":

**If `factories`:** Create new factory files in the factories directory (from Pipeline Configuration → Directory Structure) following existing naming conventions. For each new model in the architecture:
- Create a factory with reasonable defaults
- Add traits for common test variations
- Reference existing factories for associated models — **do not redefine them**
- Check existing factories first with `Glob`. Never create a factory for a model that already has one.

**If `fixtures`:** Create new fixture files in the fixtures directory (from Pipeline Configuration → Directory Structure) following existing naming conventions. For each new model in the architecture:
- Create fixture entries with realistic test data
- Reference existing fixtures for associated models
- Check existing fixtures first with `Glob`. Never duplicate existing fixture definitions.

**If `manual`:** Skip this step — test data will be created inline in each test.

### 4. Write Test Files — Milestone by Milestone

Work through milestones in order (M1, M2, ...). For each milestone, write the test files covering that milestone's acceptance criteria.

**For each acceptance criterion, write tests covering:**

1. **Happy path** — the criterion is met under normal conditions
2. **Authorization** — unauthorized users get the correct error/redirect
3. **Account/tenant scoping** — if Pipeline Configuration has a Multi-Tenant Security section, data from other tenants is never visible
4. **Edge cases** — from the PRD's edge case table and gameplan acceptance criteria
5. **Backwards compatibility** — if the architecture specifies compat requirements

**Test writing rules:**

- **Match existing style exactly.** Use the same test structure syntax (e.g., `describe`/`context`/`it` for RSpec, `test`/`class` for Minitest, `describe`/`test` for ExUnit) as found in step 1. Match the same setup patterns, data creation style, and assertion style.
- **Use descriptive test names.** `it "returns only deficient items for the current account"` not `it "works"`.
- **Reference requirement IDs** where helpful: `context "ENT-001: summary cards"`.
- **Tests MUST be syntactically valid** in the project's language (from Pipeline Configuration → Framework & Stack). They should load and parse, but FAIL because the implementation doesn't exist yet.
- **Don't stub what doesn't exist.** If a class/module doesn't exist yet, the test should fail with the language-appropriate error for missing definitions (e.g., `NameError` in Ruby, `UndefinedFunctionError` in Elixir, `ImportError` in Python) — that's expected TDD behavior.
- **Don't over-test.** One test per behavior. Don't test framework behavior (e.g., that built-in validation mechanisms work in general).
- **Keep setup minimal.** Only create the test data needed for each specific test.
- **Don't create shared helpers, shared contexts, or support modules** unless the existing codebase already uses them for similar patterns.

### 5. Apply Test Quality Heuristics

Before finalizing each test file, review it against these heuristics. These are common antipatterns observed across pipeline projects that cause false failures or Stage 5 friction.

| Heuristic | Rule |
|-----------|------|
| **Use block-form job matchers** | Use `expect { action }.to have_enqueued_job(X).with(args)` instead of `have_been_enqueued`. The cumulative form (`have_been_enqueued`) checks all jobs enqueued across the entire describe block, causing false failures when run with other examples. |
| **Verify route helper names** | Before using route helpers (e.g., `new_import_path` vs. `imports_path`), check `config/routes.rb` to determine whether the route uses `resource` (singular) or `resources` (plural). Singular and plural resources produce different helper names. |
| **Test behavior, not implementation** | Assert on observable outcomes (return values, database state, response body, enqueued jobs) — not on internal method calls, SQL structure, or private method behavior. Stage 5 may implement the same behavior differently than expected. |
| **Use flexible string matching** | For flash messages, error text, and UI copy, use `include("key phrase")` instead of exact string matching — unless the exact wording is part of an acceptance criterion. This prevents false failures when Stage 5 uses slightly different phrasing. |
| **Isolate each example** | Each `it` block must set up its own state via `let` and `before`. Never rely on database records or side effects from a prior example. Use `let!` when records must exist before the example runs. |
| **Stub at boundaries, not internals** | Stub external HTTP calls, file I/O, and third-party APIs. Don't stub internal service methods with assumed signatures — Stage 5 may implement them with different parameter names or return types. |
| **Don't assert on count after create** | Instead of `expect { action }.to change(Model, :count).by(1)`, prefer asserting on the created record's attributes. Count-based assertions are fragile when callbacks or associated records also create rows. |

If any test file violates these heuristics, fix it before proceeding.

### 6. Handle Platform Level

Check the PRD header for the project level:

- **Level 1** (small project): Primary platform tests only. Minimal scope.
- **Level 2** (primary platform only): Primary platform tests only. Mark other platforms as N/A in the coverage matrix.
- **Level 3** (all platforms): Also write tests for additional active platforms per the stage spec. (repo paths from Pipeline Configuration → Related Repositories)

### 7. Write the Coverage Matrix

Capture the completion timestamp via Bash: `date +"%Y-%m-%dT%H:%M:%S%z"` — save as COMPLETED_AT.

Prepend YAML frontmatter to the coverage matrix content before writing:

```yaml
---
pipeline_stage: 4
pipeline_stage_name: test-generation
pipeline_project: "$ARGUMENTS"
pipeline_started_at: "<STARTED_AT>"
pipeline_completed_at: "<COMPLETED_AT>"
---
```

Attach to the work item via WCP:

```
wcp_attach(
  id=CALLSIGN,
  type="test-matrix",
  title="Test Coverage Matrix[ — REPO_NAME]",
  filename="[test-coverage-matrix.md or test-coverage-matrix-{REPO_NAME}.md]",
  content="[full matrix content with frontmatter]"
)
```

The matrix content should follow this format:

```markdown
# Test Coverage Matrix — [Feature Name]

> Generated by Pipeline Stage 4 (Test Generation)
> Maps every gameplan acceptance criterion to its test location(s).

| Milestone | Criterion ID | Description | Test File | Test Block |
|-----------|-------------|-------------|-----------|------------|
| M1 | AC-001 | ... | `[test dir from Pipeline Configuration]/...` | `[test block description]` |
```

**Every acceptance criterion from every milestone must appear in this matrix.** If a criterion can't be tested (rare), document why.

### 8. Verify Tests Parse Correctly

Run a syntax check on every file you created using the syntax check command from Pipeline Configuration → Framework & Stack (replacing `{file}` with the actual path):

```bash
<syntax-check-command from Pipeline Configuration> [path/to/new_test_file]
```

Fix any syntax errors before finishing.

**Do NOT run the full test suite or the test runner.** The tests are expected to fail (TDD). Just verify they parse as syntactically valid code.

## What NOT To Do

- **Do not write implementation code.** No models, controllers, services, migrations, views. Tests and test data setup only.
- **Do not modify existing test files.** Only create new files.
- **Do not modify existing test data files** (factories, fixtures). Only create new ones.
- **Do not modify any non-test files in the primary repo.** Nothing outside the test directory (from Pipeline Configuration → Directory Structure).
- **Do not write tests that pass.** If a test would pass against the current codebase, it's testing existing behavior — remove it.
- **Do not invent test patterns.** Match the existing codebase style exactly.
- **Do not use mocks/stubs for code that doesn't exist yet.** Let the tests fail with real errors. These errors become Stage 5's implementation checklist.
- **Do not skip security/scoping tests.** Every data access path needs authorization tests. If Pipeline Configuration has a Multi-Tenant Security section, also include tenant-scoping tests.
- **Do not modify test configuration or support files** (e.g., test helpers, configuration files, support modules).

## Working in the Repository

### Branch Management

**Before writing any files**, create a dedicated branch (in `REPO_PATH`):

1. Verify the working tree is clean (`git -C REPO_PATH status`). If there are uncommitted changes, **STOP** and ask the user how to proceed.
2. Fetch the latest from origin: `git -C REPO_PATH fetch origin`
3. Create and check out a new branch: `git -C REPO_PATH checkout -b <branch-prefix>CALLSIGN <default-branch>` (branch prefix and default branch from Pipeline Configuration → Repository Details)

If the branch `<branch-prefix>CALLSIGN` already exists, **STOP** and ask the user whether to overwrite it or use a different name. Do not delete existing branches without explicit approval.

### Pre-Write Verification

**Before writing any files**, verify:
1. You're on the correct branch (`<branch-prefix>CALLSIGN`)
2. You're writing to the correct test directories (from Pipeline Configuration → Directory Structure — use `ls` and `Glob` to check structure)
3. No existing file will be overwritten (use `Glob` to check)
4. New test data files don't conflict with existing ones

**Files you MAY create:** Only files in directories listed as test-related entries in Pipeline Configuration → Directory Structure:
- Model/unit test directory — model/unit tests
- Request/controller test directory — integration tests
- Service test directory — service tests
- System/feature test directory — E2E tests
- Test data directory (factories, fixtures) — new test data definitions

**Files you may NOT create or modify:**
- Anything outside the test directory from Pipeline Configuration
- Existing test files
- Existing test data files (factories, fixtures)
- Test configuration and support files (helpers, configuration, support modules)

## When You're Done

### Commit the Test Files

Commit all new files on the `<branch-prefix>CALLSIGN` branch:

1. `git add` each new file by name (do NOT use `git add .` or `git add -A`)
2. Commit with message: `Add Stage 4 test suite for CALLSIGN`
3. Do NOT push unless the user asks you to

### Log Completion

```
wcp_comment(
  id=CALLSIGN,
  author="pipeline/test-generation",
  body="Stage 4 complete — Test suite committed on branch `<branch-prefix>CALLSIGN`[ in REPO_NAME], coverage matrix attached as [ARTIFACT_NAME]"
)
```

### Report to User

Tell the user:
1. The branch name: `<branch-prefix>CALLSIGN`
2. List every file created with a brief description of what it tests
3. The coverage matrix has been attached to `CALLSIGN` as `[ARTIFACT_NAME]`
4. How many acceptance criteria are covered and by how many test cases total
5. Any acceptance criteria that couldn't be fully tested (and why)
6. Results of the syntax check (syntax check command from Pipeline Configuration)
7. **Remind them:** "All tests are expected to FAIL — they're written before implementation (TDD). You can verify they parse with `[syntax check command from Pipeline Configuration] [test file path]`. Next step: review the tests, then run `/implementation $ARGUMENTS M1` to make them pass."

## Success Criteria

- [ ] Every acceptance criterion has at least one test per affected platform
- [ ] Security tests exist (auth, scoping, permissions)
- [ ] Edge case tests exist
- [ ] Tests follow existing project patterns exactly
- [ ] Tests use exact API payloads from architecture proposal
- [ ] All tests FAIL (no implementation yet — TDD)
- [ ] Tests are deterministic (no flakiness)
- [ ] Coverage matrix is complete — every criterion mapped to a test location
