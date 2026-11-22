---
name: dotnet-complexity
description: Report cyclomatic complexity of C#/.NET code — changed files by default. Uses Roslyn code metrics and falls back to lizard. Optional, model-invoked only.
user-invocable: false
disable-model-invocation: false
argument-hint: "[path, project, or glob — defaults to changed .cs files vs the base branch]"
---

# .NET cyclomatic complexity

Read-only report — writes no files into the repo. Ranks methods by cyclomatic
complexity so hotspots surface before review. **OPTIONAL: lives in
`.agentic/optional-skills/`; onboarding copies it into `.claude/skills/` only when
the repo is .NET and carries a `cyclomatic_complexity_max` gate in
`.agentic/quality-gates.yaml`.** This is the measuring tool that `/execute-plan`
step 4 runs to produce the actual value for that gate. Requires the .NET SDK —
check `dotnet --version`.

## Step 1 — Resolve scope

- **Argument given** (path, project, or glob): analyze exactly that. Done.
- **No argument**: analyze the changed `.cs` files vs the base branch. Build the
  set from committed, staged, and unstaged changes; drop generated files
  (`*.g.cs`, `*.Designer.cs`) and anything under `bin/`, `obj/`, `node_modules/`:

  ```sh
  BASE="${BASE_BRANCH:-main}"                 # the branch this work merges into
  MERGE_BASE=$(git merge-base HEAD "$BASE")
  { git diff --name-only --diff-filter=ACMR "$MERGE_BASE"...HEAD
    git diff --name-only --diff-filter=ACMR
    git diff --name-only --diff-filter=ACMR --cached
  } | sort -u | grep -E '\.cs$' | grep -vE '\.(g|Designer)\.cs$' | grep -vE '(^|/)(bin|obj|node_modules)/'
  ```

  If the set is empty, say so and stop — there is nothing to measure.

## Step 2 — Pick the tool (Roslyn metrics, fall back to lizard)

Roslyn metrics run per project/solution (not per file), so measure the owning
project(s) and post-filter to the changed files from Step 1.

- **Roslyn code metrics (primary)** — the official Microsoft path. Emits every
  method's cyclomatic complexity regardless of any threshold:

  ```sh
  # Run the built-in Metrics MSBuild target against the project/solution that owns
  # the changed files. It writes an XML report (path from the /p:MetricsOutputFile
  # value you pass, or the target's default location).
  dotnet build <project-or-solution> /t:Metrics /p:MetricsOutputFile=<scratchpad>/metrics.xml
  ```

  Parse the XML: each `<Method>` carries `CyclomaticComplexity`; keep the ones in
  changed files. If the Metrics target is unavailable (older SDK / not wired up),
  the project can reference `Microsoft.CodeAnalysis.Metrics` — resolve the version
  from the feed, never from memory (hard rule 4) — or use the fallback below.
  Write the XML to the session scratchpad, never into the repo tree.

- **lizard (fallback)** — a dedicated cross-language CC tool, when the Metrics
  target isn't available or you want a no-MSBuild read:

  ```sh
  pip install --quiet lizard          # once; or pipx run lizard
  lizard <files>                      # per-method CCN, takes explicit paths
  ```

State which path you took and why (one line) so the numbers are interpretable.

## Step 3 — Report

- A table ranked worst-first: file · method/line · cyclomatic complexity.
- **Threshold** comes from config, never memory (hard rule 3). Read
  `gates.cyclomatic_complexity_max` from `.agentic/quality-gates.yaml`.
  - If it exists: flag every method at or over it, and state the source.
  - If it does not exist: report raw numbers, state plainly that no cyclomatic gate
    is configured, and offer to add one to `quality-gates.yaml` (do not invent a
    pass/fail line from a hardcoded number).

**In THIS repo that key does not exist, and that is deliberate — do not "fix" it by
scoring against `cognitive_complexity_max` (ADR 0050).** Cyclomatic and cognitive
complexity are different metrics with different numbers: `ChatCoreAsync` measures 29
cyclomatic and 39 cognitive, and this repo's gate is the cognitive one, measured at
build time by SonarAnalyzer.CSharp rule S3776 — not by this skill. So this skill is
**informational here**, never the row `/execute-plan` step 4 renders. Report raw
cyclomatic numbers, say which metric they are, and leave the gate to the build.
- Keep it to the report. Refactoring is a separate, explicit ask.
