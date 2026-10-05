---
name: repo-setup
description: One-time interactive setup to configure a repository for autonomous development. Use when setting up a new project for TDD-based autonomous development with Farseer.
disable-model-invocation: true
---

# Repository Setup Skill

One-time interactive setup to configure a repository for autonomous development. Scaffolds the per-repository configuration that our engineering skills assume:

- **Domain Context**: Where Farseer and project context, ADRs, and rules for reading them live
- **Issue Tracker**: Where issues live; (GitHub by default; then local Markdown)
- **Issue Labels**: The string labels used for canonical issue triage roles

This is a prompt-driven skill, not a deterministic script. It will inspect the code, ask questions, and make decisions based on your answers. It will not overwrite existing configuration files without explicit confirmation.

## Purpose

Create or modify `AGENTS.md` or `CLAUDE.md`. Create all Farseer configuration files in `.farseer/` through an interactive process with auto-detection.

## Asking the User

**Every question this skill puts to the user goes through the `AskUserQuestion` tool**. When presenting options, provide genuine alternatives, the recommended one should always be first and labeled "(Recommended)". An open-ended question still must go through the tool, whose built-in free-text path carries the user's own words. If a question is worth stopping for, it is worth making answerable in one click. A prose paragraph the user must answer by essay is the failure this rule ends.

**All multi-sentence output for user presentation** should trigger the Skill using `/farseer:deslop` to give a more human voice to the text.

## Execution Steps

### Step 1: Check for Existing Configuration

First, inspect the current repository and understand its starting state. Read what exists and DO NOT assume:

Is this a GitHub repository? Which one? -- `git remote -v` and check `.git/config`

Do we already have configuration files in place?

```bash
ls AGENTS.md CLAUDE.md .farseer/architecture.md .farseer/code-standards.md .farseer/domain.md .farseer/issue-labels.md .farseer/issue-tracker.md .farseer/testing.md 2>/dev/null
```

Are there any existing plans or ADRs?

```bash
ls .farseer/plans/ .farseer/adr/ .farseer/*/adr/ 2>/dev/null
```

Check for signs if a local-Markdown issue tracker is in place:

```bash
ls .farseer/scratch/ 2>/dev/null
```

If `AGENTS.md` or `CLAUDE.md` and all config files (`architecture.md`, `code-standards.md`, `domain.md`, `issue-labels.md`, `issue-tracker.md`, `testing.md`) exist, inform the user:

> Repository already configured. Config files exist in `.farseer/`. To reconfigure, delete `.farseer/` then run `/farseer:repo-setup` again.

Otherwise, continue with setup.

### Step 2: Auto-Detect Project Type

Scan the repository root for configuration files to detect the technology stack:

**Check for these kinds of files (in parallel):**

- `composer.json` → PHP/Magento/Laravel/Symfony
- `package.json` → Node.js/React/Vue/Next.js
- `Cargo.toml` → Rust
- `go.mod` → Go
- `pyproject.toml` or `requirements.txt` → Python
- `Gemfile` → Ruby/Rails
- `pom.xml` or `build.gradle` → Java
- `*.csproj` or `*.sln` → .NET

**For each detected file, extract:**

- Framework and version
- Linting/formatting tools
- Testing framework (from devDependencies or test config)

**Example auto-detection output:**

```markdown
Detected configuration:

- PHP Version: 8.4
- Framework: Laravel 11 (from composer.json)
- Linting: Laravel Pint (from composer.json require-dev)
- Testing: Pest PHP (from composer.json require-dev)
```

### Step 3: Confirm Detection

Ask user to confirm detected configuration:

> I detected the following. Is this correct? (y/n)
> [Show detected config]

If incorrect, ask clarifying questions about each incorrect item.

### Step 4: Gather Additional Information

Ask these questions in order using the `AskUserQuestion` tool. One question, one answer, then the next.

Lead each question with the recommended answer so the user can accept it easily. Give a one-line explainer only when the choice genuinely branches; skip the question entirely when exploration already detected it.

**Q1: Test Command**

> What command runs your tests?
> Detected: `./vendor/bin/pest` [Enter to confirm or type custom]

**Q1b: Parallel Test Command**

> Does your test runner support parallel execution? If so, what's the command?
> (e.g., `./vendor/bin/pest --parallel`, `npm test -- --parallel`, `pytest -n auto`, `go test ./... -parallel 4`)
> [Enter detected parallel command, type custom, or 'none' if not supported]

Auto-detect hints:

- `composer.json` has `brianium/paratest` or `pestphp/pest` → suggest `{test command} --parallel`
- `package.json` has `jest` → suggest `{test command} --runInBand` is serial, default is already parallel
- `package.json` has `vitest` → already parallel by default
- `pytest` with `pytest-xdist` → suggest `pytest -n auto`
- `go test` → suggest `go test ./... -parallel {num}`
- `cargo test` → already parallel by default

**Q2: Lint Command**

> What command runs your linter?
> Detected: `./vendor/bin/pint` [Enter to confirm or type custom]

**Q3: Architectural Patterns**

> Which patterns does this repository use? (select all that apply)
>
> - [ ] Repository pattern
> - [ ] Service classes
> - [ ] Form requests / DTOs
> - [ ] Event sourcing
> - [ ] CQRS
> - [ ] Other (specify)

**Q4: Code Standards**

> Any specific coding standards or style guides?
> Detected: PSR-12 [Enter to confirm or specify]

**Q5: Coverage Requirements**

> Minimum test coverage percentage? (e.g., 80)
> Default: 80

**Q6: Issue Tracker**

> Explainer: the issue tracker is where issues live for this repository. Additional skills will read from and write to the issue tracker.
>
> What issue tracker does this repository use? (e.g., GitHub Issues, local Markdown, etc.)
> Detected: [Enter detected issue tracker or 'none']

Default posture: this plugin and related skills were designed for GitHub. If a Git remote points at GitHub, propose that. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **Local markdown**: issues live as files under `.farseer/plans/{plan-name}/issues/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, beads, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `.farseer/issue-tracker.md`.

**Q7: Triage Vocabulary**

Skip this question entirely if the `/farseer:triage` skill IS NOT installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default issue labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `nofix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `/farseer:triage` applies existing labels instead of creating duplicates.

### Step 5: Open-Ended Project Dump

Offer the user a chance to provide additional context:

> **Tell me anything else about your repository I should know.**
>
> You can paste:
>
> - README content
> - Architecture decisions
> - Naming conventions
> - Special requirements
> - Team preferences
>
> (Paste below, then type 'done' on a new line when finished, or 'skip' to skip)

Parse the dump for:

- Directory structure descriptions
- Naming conventions
- Special patterns or rules
- Integration details

### Step 6: Create Configuration Files

Create the `.farseer/` directory and all config files:

```bash
mkdir -p .farseer
```

> **Note**: The templates below show the minimum required sections. Expand each file with additional relevant details based on project complexity. For example, a framework project might include extensive architecture docs, while a simple app might stick closer to the minimum.

**Create `.farseer/testing.md`:**

````markdown
# Testing Configuration

TDD is the red → green loop. This is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `.farseer/domain.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## Test Framework

{detected framework}

## TDD Methodology

Each issue follows strict Red → Green → Refactor:

1. Write ONE failing test for ONE requirement.
2. Write the MINIMUM but SUFFICIENT code to pass the current test.
3. Refactor the code while tests stay green.
4. Update the requirement as complete.
5. Repeat for the next requirement.
6. Commit when the issue is complete.

### Good Tests

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe what the system does, not how it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists and it survives refactors because it doesn't care about internal structure.

### Bad Tests

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

### Anti-Patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Commands

```bash
# Run all tests (parallel)
{parallel test command, or test command if parallelism not supported}

# Run all tests (sequential, for debugging failures)
{test command}

# Run specific test file
{test command} {path placeholder}

# Run with coverage
{test command with coverage flag}
```

## Parallel Execution

- **Default**: Always run tests in parallel unless debugging a specific failure
- Parallel command: `{parallel test command}`
- Sequential fallback: `{test command}` (use only when parallel causes flaky failures)

## Test File Locations

- Unit tests: `{detected or standard path}`
- Feature/Integration tests: `{detected or standard path}`

## Coverage Requirements

- Minimum: {specified}%
- New code must have tests

## Test Naming Convention

- Test files: `{Convention}Test.php` or `{convention}.test.ts`
- Test methods: `it {does something}` or `test {something}`
````

_Optional expansions: Testing principles, framework-specific features, common test patterns, mocking strategies, CI configuration._

**Create `.farseer/code-standards.md`:**

````markdown
# Code Standards

## Style Guide

{detected or specified - e.g., PSR-12, Airbnb, StandardJS}

## Linting

```bash
# Check for issues
{lint check command}

# Auto-fix issues
{lint fix command}
```

## Formatting

```bash
{format command if different from lint}
```

## Pre-commit Checks

- Run linter before commits
- All tests must pass
- {any additional checks}

## Naming Conventions

- Classes: {PascalCase}
- Methods: {camelCase}
- Variables: {camelCase}
- Constants: {SCREAMING_SNAKE_CASE}
- Files: {convention}
````

_Optional expansions: Code structure rules, attribute/decorator standards, documentation standards, pre-commit hooks, code review checklist._

**Create `.farseer/architecture.md`:**

```markdown
# Architecture

## Directory Structure

{Map out the key directories and their purposes}

Example:

- `app/Models/` - Eloquent models
- `app/Services/` - Business logic services
- `app/Http/Controllers/` - HTTP request handlers
- `app/Http/Requests/` - Form request validation
- `tests/Unit/` - Unit tests (mirror app/ structure)
- `tests/Feature/` - Integration/feature tests

## Patterns Used

{List from user selection}

- Repository pattern: {yes/no + brief description}
- Service classes: {yes/no + brief description}
- etc.

## Conventions

{From user dump or defaults}

- One class per file
- Tests mirror source structure
- {any other conventions}

## Key Integrations

{If mentioned in dump}
```

_Optional expansions: DI/IoC details, plugin/extension system, event system, routing, configuration, bootstrap process, error handling, versioning strategy._

**Create `.farseer/domain.md`, `.farseer/issue-tracker.md`, `.farseer/issue-labels.md`:**

Write these configuration files based on the collected user input and auto-detected information using the seed templates in this skill folder as a starting point.

- [domain.md](./domain.md): domain context
- [issue-labels.md](./issue-labels.md): label mapping
- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker

If the user selected "other" issue trackers, write `.farseer/issue-tracker.md` from scratch using the user's description.

**Pipeline enrollment (nothing to scaffold):**

Pipeline agents enroll via their own frontmatter (`phase:`), so a fresh setup already has a working pipeline from the plugin's bundled agents — nothing to scaffold here. `devils-advocate` runs at `post-plan`; `standards-enforcer` ships dormant (uncomment its `phase` to enable). See `HOOKS.md`. Running `hooks/discover-hooks.sh` prints exactly what is enrolled at each hook.

Tell the user:

> **Pipeline ready.** `devils-advocate` is enrolled at the `post-plan` hook via its own agent frontmatter, so it runs automatically when you create a plan. `standards-enforcer` ships with Farseer but is dormant — uncomment its `phase` key in the agent's frontmatter to enable code-standards enforcement on changed files.
> To add your own gate, drop an agent file in `.farseer/agents/` and give it a `phase` (one of the 8 hook points). A local agent with the same `name` overrides the plugin's. See `HOOKS.md` for the full hook list and frontmatter schema.
> To see what is currently enrolled at each hook, run `$(claude plugin path farseer)/hooks/discover-hooks.sh` — that is the fastest answer whenever an agent doesn't fire.

**Create AI configuration in project root:**

- If `CLAUDE.md` exists, edit it.
- Else If `AGENTS.md` exists, edit it.
- Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa); always edit the one that's already there.
- If neither exists, create `CLAUDE.md` (preferred) or `AGENTS.md` (if user prefers).

**If editing existing file**, check if an `## Agent Skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The `## Agent Skills` block should contain:

```markdown
## Agent Skills

Project configuration files are in `.farseer/`:

- `architecture.md` - Technical patterns and structure
- `code-standards.md` - Coding conventions
- `testing.md` - Test configuration and commands

### Domain Context

[summary of domain context]. See `.farseer/domain.md`.

### Issue Tracker

[one-line summary of where issues are tracked]. See `.farseer/issue-tracker.md`.

### Triage Labels

[one-line summary of the label vocabulary]. See `.farseer/issue-labels.md`.
```

**Otherwise if creating a new file**:

This file provides always-on context for every Claude session. Keep it concise (~30-50 lines).

````markdown
# {Project Name}

{Brief 1-2 sentence description of the project.}

## Feature Development

For any feature or change beyond a simple fix, use the `/farseer:planner` skill to trigger the autonomous development workflow. Never use Claude Code's built-in plan mode. After writing a plan, ask the user if they want to execute it, and provide the command to run it later with the `/farseer:orchestrate` skill.

Use this workflow for: new features, multi-file changes, anything requiring multiple steps or tests.

Skip for: quick bug fixes, single-line changes, questions, documentation. When skipped, still ensure appropriate tests exist for any added functionality.

## Asking the User

**Every question this skill puts to the user goes through the `AskUserQuestion` tool**. When presenting options, provide genuine alternatives, the recommended one should always be first and labeled "(Recommended)". An open-ended question still must go through the tool, whose built-in free-text path carries the user's own words. If a question is worth stopping for, it is worth making answerable in one click. A prose paragraph the user must answer by essay is the failure this rule ends.

## Tech Stack

- **Language**: {language} {version}
- **Framework**: {framework if applicable}
- **UI**: {framework if applicable}
- **Testing**: {test framework}
- **Linting**: {linter/formatter}

## Core Principles

{Extract 3-5 key principles from user input or your judgment. These should be always-true rules that affect how code is written.}

## Project Structure

{Brief 3-5 line summary of directory structure from architecture.md}

## Commands

```bash
# Run tests
{test command}

# Lint/format
{lint command}

# Start dev server (if applicable)
{start command or remove this line}
```

## Key Rules

{5-10 bullet points of critical coding rules extracted from code-standards.md and user input}

## Agent Skills

Project configuration files are in `.farseer/`:

- `architecture.md` - Technical patterns and structure
- `code-standards.md` - Coding conventions
- `testing.md` - Test configuration and commands

### Domain Context

[summary of domain context]. See `.farseer/domain.md`.

### Issue Tracker

[one-line summary of where issues are tracked]. See `.farseer/issue-tracker.md`.

### Triage Labels

[one-line summary of the label vocabulary]. See `.farseer/issue-labels.md`.
````

### Step 7: Confirm Completion

After creating all files, output:

```text
✓ Created (or Edited) AGENTS.md/CLAUDE.md
✓ Created .farseer/architecture.md
✓ Created .farseer/code-standards.md
✓ Created .farseer/domain.md
✓ Created .farseer/issue-labels.md
✓ Created .farseer/issue-tracker.md
✓ Created .farseer/testing.md

Project configured for autonomous development!

Next steps:
1. Review the generated files in `.farseer/`
2. Customize the pipeline by enrolling agents via frontmatter — set a `phase` on an agent in `.farseer/agents/` to add a gate, or remove a `phase` to drop one (see HOOKS.md)
3. Describe a feature to start planning: "Help me implement..."
4. The `/farseer:planner` skill will auto-trigger to help you plan
```

## Error Handling

- If unable to detect repository type: Ask user to specify manually
- If file creation fails: Report error and suggest checking permissions
- If user provides conflicting information: Ask for clarification

## Idempotency

- Check for existing `AGENTS.md`/`CLAUDE.md` and `.farseer/` config before running
- Never overwrite existing files without explicit confirmation
- Offer to update individual files if some exist
