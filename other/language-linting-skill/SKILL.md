---
name: language-linting-skill
description: "Per-language linting rules reference — Python Ruff, JS/TS ESLint, Java Checkstyle/PMD/SpotBugs, C# dotnet format/Roslyn/StyleCop: rules, configs, error guidance. Triggers: ruff rules, eslint config, checkstyle. Loaded by linting-workflow-skill and linting-subagent (the executor); gate semantics live in verification-loop-skill."
license: Apache-2.0
compatibility: opencode
category: Language-Specific
---

## What I do

Per-language lint execution and error resolution on top of `linting-workflow-skill` (which owns the generic detect→fix loop and delegation). This file maps languages → linters, detection commands, and the fix guidance that actually needs saying.

## When to use me

Linting a polyglot codebase; decoding a specific linter error; configuring lint in CI.

**Language detection**: file extensions + manifests (`.py`/pyproject → Ruff; `.ts/.tsx/.js/.jsx`/package.json → ESLint; `.java`/pom.xml|build.gradle → Checkstyle+PMD+SpotBugs; `.cs`/`.csproj` → dotnet format + Roslyn analyzers). Orchestration + subagent delegation → `linting-workflow-skill`.

## Command matrix

| Language | Linter(s) | Commands |
|---|---|---|
| Python | Ruff | `ruff check .` · `ruff check --fix` · `ruff format .` (config in pyproject `[tool.ruff]`) |
| JS/TS | ESLint (+Prettier) | `npx eslint . --ext .ts,.tsx,.js,.jsx` · `--fix` for autofixables; package manager via lockfile (pnpm-lock/yarn.lock/package-lock); Prettier for formatting, ESLint for correctness |
| Java | Checkstyle (style) + PMD (design) + SpotBugs (bytecode bugs) | Maven: `mvn checkstyle:check pmd:check spotbugs:check` · Gradle: `./gradlew checkstyleMain pmdMain spotbugsMain` |
| C# | dotnet format + Roslyn/StyleCop analyzers | `dotnet format --verify-no-changes` (CI) · `dotnet format` (fix); severity via `.editorconfig` |

## House rules

- **Fix semantics**: autofix for mechanical issues (`--fix`, `ruff format`); manual review for semantic findings (PMD design, SpotBugs correctness, Roslyn analyzers) — never blanket-suppress.
- **Zero NEW errors on changed files** is the gate (pre-existing noted, not blocked) — matches `plan-execution-skill` --gate semantics.
- Suppressions carry a reason and scope (`// noqa: E501 # long URL in docstring`), never bare `// eslint-disable-next-line`.
- Error-code decoding: match the code to the rule family (Ruff `E/F/I/N/UP/B/SIM/C4`, ESLint plugin prefixes, Checkstyle module names) and fix the pattern, not the instance.
- Spring Boot: enable Bean Validation + actuator health checks as part of the lint pass config (house standard for Java services).

**Related:** `security-audit-skill` (security scanning, not lint) · `linting-workflow-skill` (generic loop).

> Removed 2026-09: per-linter config file listings, per-error-code explanation tables, package-manager detection walkthroughs, Spring/Gradle XML config dumps, worked fix transcripts — each linter's rule catalog is model-known; the matrix + fix semantics + suppression discipline are the durable content.
