---
name: sonar
description: Run SonarQube analysis locally against this repo and interpret results against .agentic/quality-gates.yaml before pushing.
user-invocable: true
disable-model-invocation: true
---

# Local SonarQube analysis

Transformed from the workspace `/sonar` skill: repo-root scan instead of the
`repos/<service>/` multi-repo indirection; thresholds compared against
`.agentic/quality-gates.yaml` instead of prose. **OPTIONAL: lives in
`.agentic/optional-skills/`; onboarding copies it into `.claude/skills/` only when
the repo has a SonarQube gate.**

## Step 0 — Pre-flight

`SONAR_HOST_URL` and `SONAR_TOKEN` must be set. If missing, ask the user for them
(AskUserQuestion) and offer to persist to their shell profile. Find the project key
in `sonar-project.properties` or the CI config.

## Step 1 — Tests + coverage first

Sonar without coverage lies. Run the repo's coverage command (from
`quality-gates.yaml` `coverage_tooling` / CLAUDE.md Commands) so the report exists
before scanning.

## Step 2 — Scan (stack-dependent)

- **.NET:** `dotnet sonarscanner begin /k:<key> /d:sonar.host.url=$SONAR_HOST_URL /d:sonar.token=$SONAR_TOKEN /d:sonar.cs.opencover.reportsPaths=<coverage>` → `dotnet build` → `dotnet sonarscanner end /d:sonar.token=$SONAR_TOKEN` (needs Java 17+).
- **Node:** `npx sonarqube-scanner` with `sonar-project.properties` (lcov path set).

## Step 3 — Fetch & interpret

Query the server REST API: `/api/qualitygates/project_status`, `/api/issues/search`
(new code period), `/api/measures/component` (coverage, duplication, complexity).
Render the gate table: metric | threshold (from `.agentic/quality-gates.yaml`) |
actual | PASS/FAIL.

## Step 4 — Report

For each failing condition, list the concrete issues (file:line, rule, message) and
propose fixes ordered by effort. Distinguish "new code" failures (merge-blocking per
`enforcement.ci`) from overall-code noise.
