---
name: do-adopt
description: Scan a project for missing best-practice areas and implement the top recommendation for each gap (linting, unit testing) — installs tools, writes configs, verifies, and commits. Pass 'recommend' to stop after writing recommendations without implementing (replaces the old do-recommend skill).
argument-hint: '[recommend] [topic] (optional — omit for all topics; ''recommend'' skips implementation)'
user-invocable: true
disable-model-invocation: false
context: fork
---

# Adopt Best-Practice Technologies

Scan the current project for missing best-practice areas and **implement the top recommendation** for each gap — or, in recommend mode, stop after producing recommendations without installing anything.

## Modes and Invocation

`$ARGUMENTS` may contain a topic name, the word `recommend`, or both:

- *(empty)* — adopt every gap topic in the table below.
- `<topic>` — adopt that one topic only.
- `recommend [<topic>]` — **recommend-only mode**: perform the same
  detection and analysis, write the recommendation as a
  `status: recommended` project skill (see step 5R), and implement
  nothing. This replaces the old standalone `do-recommend` skill.

Do not prompt the user for which topics to process.

## Topics

| Topic | Best-Practice Skill |
| ----- | ------------------- |
| linting | mav-bp-linting |
| unit-testing | mav-bp-testing |

Detection hints for each topic come from the shared registry —
`${CLAUDE_PLUGIN_ROOT}/skills/do-upskill/topics.json` (`scanHints` per
topic). Do not maintain a separate detection list here.

## Process

For each topic:

### 1. Check Whether the Practice Already Exists

Apply the topic's `scanHints` (dependencies, grep patterns, file globs)
plus a check for CI steps that run the tool. If the practice is
**already implemented** (configs exist, dependencies present, actively
used), skip the topic. Print: `<topic>: already implemented, skipping.`

### 2. Identify the Project's Tech Stack

Determine the primary language(s) and framework(s) by reading:
- `package.json` (Node/JS/TS, look at framework deps like react, vue, express, etc.)
- `pyproject.toml` / `requirements.txt` (Python)
- `go.mod` (Go)
- `Cargo.toml` (Rust)
- `build.gradle.kts` / `pom.xml` (JVM)
- Source file extensions and directory structure

### 3. Read the Best-Practice Skill

Read the corresponding best-practice skill
(`${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md`) to understand the
recommended tools and configuration standards for the detected stack.

### 4. Check for an Existing Recommendation

If `docs/maverick/skills/<topic>/SKILL.md` exists with
`status: recommended` frontmatter (written by `do-upskill`
or a prior recommend-mode run), read it and use its recommended stack —
do not re-analyse. There is exactly **one** recommendation artifact
format: the project-skill file. Never write a separate
`docs/maverick/recommendations/` document.

### 5R. Recommend-Only Mode — Write the Recommendation and Stop

Pick the best-fit tool for the stack (1 option when there is a clear
winner — e.g. Ruff for Python, ESLint for TypeScript; name up to 2
genuinely competitive alternatives and their trade-offs in the Patterns
section). Write it as a `status: recommended` project skill at
`docs/maverick/skills/<topic>/SKILL.md`, using
`do-upskill`'s mandatory output structure (Stack /
Configuration / Patterns / File Locations, prose only, under 100 lines).
Then stop — no installation, no commits.

### 5. Implement the Top Recommendation

Install and configure the recommended tool. Follow the best-practice skill's standards precisely.

**For linting — implement all of:**

1. **Install packages** — add the linter and formatter as dev dependencies using the project's package manager
2. **Create config file** — write the linter config at the project root using the recommended preset (e.g., `eslint.config.js` with flat config for TS/JS, `ruff.toml` for Python). Follow the error-only policy from the best-practice skill.
3. **Create formatter config** — if the formatter is a separate tool (e.g., Prettier for JS/TS), write its config. If the linter handles formatting (e.g., Ruff), configure it in the same file.
4. **Add ignore patterns** — exclude build output, generated code, and vendor directories
5. **Add package scripts** — add `lint` and `format` (or equivalent) scripts to the project's script runner (package.json scripts, Makefile, pyproject.toml scripts)
6. **Verify** — run the lint command and fix any initial errors in project source code. The goal is a clean lint pass, not a config that ignores existing issues.

**For unit testing — implement all of:**

1. **Install packages** — add the test framework and assertion library as dev dependencies
2. **Create config file** — write the test runner config at the project root with sensible defaults (e.g., `vitest.config.ts` for Vite projects, `jest.config.js` for other JS/TS, `pyproject.toml [tool.pytest]` for Python)
3. **Create a sample test** — write one example test file demonstrating the project's test conventions (file location, import pattern, describe/it structure). Place it alongside or mirroring an existing source file. The test should verify real behaviour, not be a trivial placeholder.
4. **Add package scripts** — add a `test` script (and `test:coverage` if the framework supports it)
5. **Verify** — run the test suite and confirm the sample test passes

### 6. Update the Project Skill

Rewrite `docs/maverick/skills/<topic>/SKILL.md` as a **factual** project
skill describing what is now implemented (drop the
`status: recommended` field), per `do-upskill`'s output
structure. This keeps the single artifact current.

### 7. Commit the Changes

Create a conventional commit for each topic adopted:

```
chore: adopt <tool-name> for <topic> (<topic>)
```

Follow the mav-git-workflow skill for commit conventions. Do not push — the user will review and push.

## Rules

- **Best-practice compliant** — every config choice must follow the corresponding best-practice skill. Do not deviate from the standards (error-only policy, separate linter/formatter, etc.).
- **Stack-specific** — install and configure tools that match the project's actual language and framework
- **Minimal and correct** — write the minimum config needed for a clean, working setup. Do not add rules or plugins beyond the recommended preset.
- **Verify before committing** — run the tool after installation. If it fails, fix the issue. Do not commit a broken setup.
- **Skip covered topics** — if the practice already exists, do not overwrite or reconfigure it
- **No branch creation** — commit directly to the current branch. The user is expected to be on an appropriate branch.
- **One commit per topic** — separate commits make it easy to review or revert individual adoptions
- **One recommendation format** — the `status: recommended` project skill; never a parallel recommendations document

<!-- maverick-plugin-version: 4.0.2-dev -->
