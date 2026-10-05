---
name: create-run-gates
description: >
  Run all the CI code-analysis gates locally against a change, before opening a PR, so failures are
  caught in seconds instead of after a full pipeline cycle. Use when the user says "run the gates",
  "check before I push", "will CI pass", "run the CI checks locally", "did I break a gate", or
  "pre-PR check", or as the verification step at the end of a change. Do NOT use to evaluate a
  skill's quality (that is governance-validate-skills) or to validate only the artifact graph and
  docs wiki (that is governance-check-graph); this runs the whole gate set the pipeline runs.
---

# Run Gates

Usable by **any** persona, typically Developer or QE. Invoked as `/create-run-gates`.

Run the same gates the `code-analysis-pipeline.yml` runs, on the working tree, so a doc, skill,
graph, or house-style violation is found and fixed locally instead of failing CI after a PR is open.
This is the sibling of `create-verify-test-coverage`: that one verifies tests and coverage, this one
verifies the gates.

## Run it

```powershell
pwsh MindNova/toolsInvoke-LocalGates.ps1
```

- Add `-IncludeToolTests` to also run the gate scripts' own Pester tests.
- Add `-CoverageFile <merged opencover xml>` to include the C09 coverage gate (needs a test run first).
- The script exits non-zero if any BLOCKING gate fails, so it doubles as a scriptable pre-push check.

## Reading the result

Each gate is **Blocking** or **Advisory**:

- **Blocking** (docs line-citations C02, artifact graph, docs wiki + index C10, em-dash C11, skill
  hygiene, story-trait malformed keys): a failure fails CI. Fix before the PR.
- **Advisory** (LogMindNova C05, KQL escaping C04, PascalCase wire names C06, coverage C09): reported
  as findings, not yet blocking (pre-existing debt is being cleared). Do not add NEW advisory
  findings on changed code.

The summary table marks each PASS / FAIL / ADVISORY; the run exits non-zero only on a blocking FAIL.

## Enforce it on every push (optional, recommended)

A git pre-push hook runs the blocking gates automatically on `git push`, from any tool (terminal,
Claude Code, Copilot), because it is a git hook, not an agent feature. Enable once per clone:

```bash
git config core.hooksPath .githooks
```

Or run `pwsh MindNova/toolsInstall-GitHooks.ps1` once, which sets that config and checks for `pwsh`.
Bypass intentionally with `git push --no-verify`. Needs `pwsh` on PATH; if absent the hook warns and
allows the push rather than blocking on a tooling gap.

## Next steps

- `/create-verify-test-coverage` (QE) - verify tests and coverage alongside the gates before the PR.
- If a blocking gate fails, fix the listed issue and re-run; the gate output names the file and rule.
