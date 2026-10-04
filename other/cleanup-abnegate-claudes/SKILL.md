---
name: cleanup
description: Find and remove dead code, unused imports, and technical debt
argument-hint: "[module|all]"
---

# Code Cleanup

Systematic cleanup of dead code, unused imports, and technical debt.

**RULE: All tests must pass after cleanup. No behavior changes.**

## Arguments

- `$ARGUMENTS` - Module to clean up, or `all` for entire codebase

## Phase 0: Baseline (Parallel)

Detect the stack from the first manifest in this table's row order that exists at the repository root. `<pm>` is the package manager chosen by lockfile, as in the `skills:build` skill. Prefer the project's own scripts or Makefile targets when they exist. When tests run in Docker Compose (Appwrite), run the same command inside the service, for example `docker compose exec <service> vendor/bin/phpunit --filter Name`.

| Manifest | Stack | Test all | Test one | Build | Lint | Format | Static analysis | Coverage |
|---|---|---|---|---|---|---|---|---|
| build.gradle.kts / build.gradle | Gradle | `./gradlew test` | `./gradlew test --tests "*Name*"` | `./gradlew build` | `./gradlew spotlessCheck` (or `ktlintCheck`) | `./gradlew spotlessApply` (or `ktlintFormat`) | `./gradlew detekt` | `./gradlew koverReport` |
| pom.xml | Maven | `mvn test` | `mvn test -Dtest=Name` | `mvn package` | configured plugin | `mvn spotless:apply` if configured | — | `mvn jacoco:report` if configured |
| composer.json | PHP | `composer test` | `composer test -- --filter Name` | `composer install` | `composer lint` | `composer format` | `composer check` (PHPStan) | `vendor/bin/phpunit --coverage-text` (PCOV/Xdebug) |
| package.json | Node | `<pm> test` | `<pm> test -- -t "Name"` | `<pm> run build` | `<pm> run lint` | `<pm> run format` / `npx prettier --write .` | `<pm> exec tsc --noEmit` | `<pm> test -- --coverage` |
| Cargo.toml | Rust | `cargo test` | `cargo test name` | `cargo build` | `cargo clippy -- -D warnings` | `cargo fmt` | `cargo clippy -- -D warnings` | `cargo llvm-cov` if installed |
| go.mod | Go | `go test ./...` | `go test -run Name ./...` | `go build ./...` | `go vet ./...` | `gofmt -w .` | `golangci-lint run` if configured | `go test -cover ./...` |
| pyproject.toml / setup.py | Python | `pytest` | `pytest -k name` | `pip install -e .` | `ruff check .` | `ruff format .` | `mypy .` if configured | `pytest --cov` |

Commands in this skill name a column of this table. Give every agent the detected stack's commands, then **launch these agents in parallel:**

**Agent A** (`architect`): Run the full test suite with the stack's Test all command and capture the output.
Report pass/fail status and any existing failures. If tests do not pass, STOP. Do not proceed until all tests are green.

**Agent B** (`architect`): Run the stack's Lint and Static analysis commands (whichever it has) and capture current warning counts.
Report the total warning count and error count for each tool. These are the baseline numbers.

**Wait for both agents to complete.** If Agent A reports test failures, fix them before continuing. Record Agent B's baseline counts for comparison in the final summary.

## Phase 1: Detection Sweep (Parallel)

All detection work is read-only analysis. **Launch these agents in parallel:**

**Agent A - Unused Imports** (`Explore`): Scan all source files of the detected stack in the target module(s) for unused imports. Use IDE-style analysis: for each import statement, search the file body for usage of the imported symbol. Produce a list of files with unused imports and the specific import lines.

**Agent B - Dead Code** (`Explore`): Search for dead code across the target module(s). Look for:
- Unused private functions (private functions with zero call sites)
- Unused private classes (private classes never referenced)
- Unused parameters (parameters never read in the function body)
- Unreachable code (code after unconditional return/throw)
- Commented-out code blocks (3+ consecutive commented lines that look like code)
- `TODO`/`FIXME`/`HACK`/`XXX` comments

For each finding, note the file path, line number, symbol name, and why it appears dead.

**Agent C - Deprecated Code** (`Explore`): Search for all deprecation markers of the stack's languages across the target module(s):
- Annotations and attributes: `@Deprecated` (Kotlin, Java), `#[\Deprecated]` (PHP 8.4+), `#[deprecated]` (Rust), `@deprecated` decorators (Python 3.13+ `warnings.deprecated`)
- `@deprecated` doc-comment tags (PHPDoc, JSDoc, TSDoc, Javadoc) and Go `// Deprecated:` comments
- Calls to functions/classes that carry any of these markers

For each finding, note the file, the deprecated symbol, and whether a replacement is specified.

**Agent D - Technical Debt** (`Explore`): Search for technical debt indicators across the target module(s):
- Warning suppressions (`@Suppress`, `@SuppressWarnings`, `@phpstan-ignore`, `eslint-disable`, `@ts-ignore`, `#[allow(...)]`, `//nolint`, `# noqa`, `# type: ignore`); note what each one suppresses
- TODO/FIXME comments with context
- Known workarounds (comments mentioning "workaround", "hack", "temporary")
- Outdated idioms of the detected stack (patterns that its current language, framework or library versions replace)

For each finding, assess severity (High/Medium/Low) and estimated effort (Low/Medium/High).

**Agent E - Code Style** (`Explore`): Analyze code style consistency across the target module(s):
- Naming convention violations (inconsistent casing, abbreviations, Hungarian notation)
- Inconsistent error handling patterns (for example mixed try/catch, result types and error codes)
- Inconsistent logging patterns (mixed logger frameworks, inconsistent log levels)
- Section-header comments (`// ---`, `// ===`, `// ****`) that should be removed

**Agent F - Stale Documentation** (`Explore`): Scan for documentation issues across the target module(s):
- Comments that restate the code (e.g., `// increment counter` above `counter++`)
- Outdated comments that reference renamed/removed symbols
- TODO comments that reference completed work
- Doc comments whose parameter or return tags (`@param`/`@return` or the language's equivalent) don't match the current signature

**Wait for all six agents to complete.** Collect all findings into a unified cleanup manifest organized by file.

## Phase 2: Automated Fixes

### 2.1 Unused Imports

Run the stack's Format command, then remove the unused imports from Agent A's list that the formatter left. A linter autofix does this in bulk where one exists (for example `ruff check --fix .` or `cargo fix --allow-dirty`).

### 2.2 Verify Imports

Run the stack's Test all command.

## Phase 3: Manual Cleanup (Consolidation Pattern)

Commit the Phase 2 changes first (see Commit Strategy), because uncommitted work is not part of BASE. Then record BASE: the SHA `git rev-parse HEAD` prints in this checkout. Give each file group's `architect` agent the checkout's absolute path as the repo, BASE, its own branch and an absolute worktree path (explicit worktree mode: the architect follows its Worktree BASE protocol). Prompt the consolidator with this checkout as the integration worktree, BASE, and merge as the integration mode.

Using the unified manifest from Phase 1, partition the affected files into groups. Use the **consolidation pattern** — launch each file group as a parallel agent in its own worktree. Agents can freely edit overlapping files; the consolidator handles merges.

**Each worktree agent**: For its assigned file group, apply all queued fixes from the manifest:

1. **Dead code removal**: Delete confirmed unused private functions, classes, parameters. Remove commented-out code blocks. Clean up or remove stale TODO comments.
2. **Deprecated code migration**: Where a deprecation marker names a replacement, migrate callers to the replacement. Where we own the deprecated symbol and it has zero external callers, remove it.
3. **Technical debt quick wins**: Fix items that are High severity + Low effort or Low severity + Low effort. For High effort items, create a GitHub issue.
4. **Code style normalization**: Fix naming violations, remove section-header comments (`// ---`, `// ===`), standardize error handling within each file.
5. **Documentation cleanup**: Remove stale/obvious comments. Fix doc-comment tags that don't match the current signature.

Each agent commits its changes before finishing.

**After all worktree agents complete**, launch the **consolidator** agent (`subagent_type: "consolidator"`) to merge all branches and resolve any overlapping edits.

### 3.1 Review

Launch a **reviewer** agent (`subagent_type: "reviewer"`) to review the merged diff. Fix any critical/major issues found.

### 3.2 Verify

Launch a **verifier** agent (`subagent_type: "verifier"`) in post-verification mode with the stack's Test all, Lint and Build commands to confirm all tests pass, lint is clean, build succeeds, and no behavior changes occurred.

## Phase 4: Final Formatting

Run the stack's Format command.

## Phase 5: Final Verification

Launch a **verifier** agent (`subagent_type: "verifier"`) in post-verification mode. It runs the stack's tests, lint, static analysis and build. Compare warning counts against the Phase 0 baseline to quantify improvement.

## Phase 6: Summary

Create cleanup report:

```markdown
# Cleanup Report: [Module/All]

## Summary
- Files modified: X
- Lines removed: Y
- Warnings fixed: Z (before: B, after: A)

## Changes Made

### Unused Imports Removed
- X files had unused imports removed

### Dead Code Removed
- [file:symbol] - [why it was dead]

### Deprecated Code Migrated
- [file:symbol] - migrated to [replacement]

### Technical Debt Addressed
- [item] - [what was done]

### Code Style Fixed
- [description of patterns normalized]

### Documentation Cleaned
- [stale comments removed]

### Issues Created for High-Effort Items
- #NNN - [tech debt item]

## Remaining Items
- [items that need future attention]
```

## Commit Strategy

Delegate to the `skills:commit-all` command to produce atomic, logically-grouped commits from the cleanup changes:

```
Skill(skill="skills:commit-all")
```

`skills:commit-all` will partition the diff into groups like unused imports, dead code removal, deprecation migration, style normalization, etc. and commit each group with a `chore(<scope>): …` or `refactor(<scope>): …` message.

## Completion Criteria

- [ ] All unused imports removed
- [ ] Dead code removed
- [ ] Deprecations addressed or documented
- [ ] Quick-win tech debt fixed
- [ ] Code formatted and style consistent
- [ ] Stale documentation cleaned
- [ ] All tests pass
- [ ] Static-analysis/lint warning count reduced from baseline
- [ ] Cleanup report created
