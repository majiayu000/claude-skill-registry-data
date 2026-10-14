---
name: linting-inline-skill
description: >-
  In-session linting delegate — discovers the language linter, runs it scoped to
  touched files only, applies gate semantics from verification-loop-skill, and
  fixes or reports findings inline. Decision tree with skip rules, scope bounds,
  enforcement deltas, and output contract. Triggers: inline lint, lint
  in-session, plan-execution-inline-skill linting step.
license: Apache-2.0
compatibility: opencode
metadata:
  mirrors: linting-subagent
category: Code Quality
---

# Linting (inline)

You are executing the linting delegate's workflow **in this session**. The
subagent's isolation (fresh context, sandbox, tier model) is replaced by the
discipline below — advisory, but the gate's verdict depends on it.

## Decision tree

1. **Skip check:** no linter configured for the changed languages (no eslint/
   ruff/checkstyle/dotnet-format configs, no manifest scripts) → report
   "lint-inviable", stop. Never add a linter config unprompted.
2. **Discover:** linter + invocation from manifests/config per
   `language-linting-skill` (Ruff for Python, ESLint for TS/JS, Checkstyle/
   SpotBugs for Java, dotnet format for C#). Autoloaded by that skill where
   available.
3. **Scope (scoped-lint rule):** lint ONLY the files in the current diff
   (`git diff --name-only --diff-filter=AM`). Full-suite lint is the gate's
   job, not yours.
4. **Gate semantics** per `verification-loop-skill`: auto-fixable → fix and
   re-run once; remaining findings → report by severity with file:line.
5. **INCONCLUSIVE** (linter crashes, config broken) → report it as such; never
   declare green without a run.

## Scope bounds

- Fixes touch only the linted files and only the flagged findings.
- No config changes (adding plugins, disabling rules) — that is a finding.

## Enforcement deltas (vs linting-subagent)

| Subagent enforcement | Inline discipline (you) |
|---|---|
| Fresh context window | State the touched-file list before linting so scope drift is visible |
| Isolated fix sandbox | Fixes land in the working tree directly — list every file you changed in Output |
| Tier model | Same model as the caller — flag uncertainty instead of suppressing findings |

## Output contract

**Status:** [success | partial | failed | inconclusive]
**Output:** linter(s) run + files linted + findings (fixed vs reported, file:line)
**Summary:** ≤3 sentences
**Issues:** unfixable findings, config problems, or "None"
