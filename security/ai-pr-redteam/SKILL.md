---
name: ai-pr-redteam
description: Use when reviewing AI-generated, Vibe Coding, or agent-authored PRs, diffs, commits, or merge requests for fake logic, fallback success, weak tests, contract drift, language-specific engineering quality, package boundaries, abstraction, reuse, and merge readiness.
---

# AI PR Redteam

Act as the skeptical reviewer for AI-assisted code before it merges. The job is to determine whether the PR is genuinely complete, maintainable, and proven, or whether it only looks finished because fake logic, fallback success, weak tests, or poor structure hides the risk.

## Scope

Use this skill for PR review, merge request review, branch diff review, AI-generated code review, Vibe Coding handoff review, and pre-merge engineering quality checks.

Do not use it as a full MLPS/等保 audit, broad architecture design, normal feature implementation, or post-failure rescue. Use `dengbao-code-audit` for compliance security audit, `internal-app-standards` for full internal-system standards/design review, and `vibe-coding-rescue` when the project is already failing and needs repair.

## Required Start

1. Protect the worktree with `git status --short --branch`.
2. Identify the review target: PR URL, base branch, current branch, commit range, staged diff, or working-tree diff.
3. Read the PR description, linked requirement/spec, README, package manifests, env templates, CI files, tests, and changed files. If the PR intent is missing, infer it from the diff and label the intent as inferred.
4. Detect the primary programming language(s) before judging engineering quality. Apply the language-specific conventions in [references/language-quality-rules.md](references/language-quality-rules.md).
5. Run the heuristic scanner when possible, writing output outside the reviewed repo unless the user asks for an artifact in the repo:

   ```bash
   python3 <skill-dir>/scripts/scan_ai_pr.py <repo-root> --base <base-ref> --format markdown --output <workdir>/ai-pr-redteam-scan.md
   ```

   If there is no base ref, omit `--base`; the script scans the working tree or repository files as a fallback. Treat scanner output as leads, not findings.

## Review Lenses

Read [references/fake-fallback-taxonomy.md](references/fake-fallback-taxonomy.md) before classifying fake/mock/fallback/default-success logic.

Read [references/language-quality-rules.md](references/language-quality-rules.md) before judging code splitting, package boundaries, abstraction, reuse, error handling, and testability.

Read [references/output-contract.md](references/output-contract.md) before producing the final review report.

## Hard Rules

- Findings lead the report. Do not bury blockers under summaries.
- A `fake`, `mock`, `sample`, `dummy`, `TODO`, `stub`, hardcoded value, or fallback is not automatically wrong; it becomes a finding only after checking whether it is reachable from production behavior, tests, docs, or deploy paths.
- Production-path fake data, fallback success, swallowed integration failure, or permission/tenant fallback defaults to `BLOCKER` unless the PR proves it is an intentional, observable degraded mode.
- Engineering quality findings must be language-aware. Do not apply Java package ideology to Python modules, React component concerns to backend services, or Go error-handling expectations to TypeScript exceptions.
- Do not call code "over-engineered" or "under-abstracted" without naming the concrete maintenance risk: duplication, leaky boundary, untestable logic, unclear ownership, dependency direction, data consistency, or change blast radius.
- Weak tests are findings when they cannot fail for the business behavior the PR claims. A test that only asserts HTTP 200, mocks the implementation under test, skips cases, or snapshots broad output is not proof by itself.
- Never claim merge-ready without fresh evidence: commands run, tests reviewed, contract checked, and remaining gaps stated.
- Do not fix the PR unless the user explicitly asks for repair. This skill produces review evidence and targeted optimization actions.

## Severity

| Severity | Meaning |
| --- | --- |
| `BLOCKER` | Merge would likely ship fake behavior, silent failure, security/data isolation risk, broken contract, data corruption, or unreviewable change scope. |
| `HIGH` | Must address before merge unless an owner accepts documented risk; usually missing tests, unsafe fallback, bad boundary, migration risk, or major maintainability issue. |
| `MEDIUM` | Should improve soon; does not obviously break the PR but raises maintenance, testability, or ownership cost. |
| `LOW` | Cleanup, clarity, or follow-up improvement with limited merge risk. |

## Review Flow

1. Build a PR intent map: claimed behavior, affected surfaces, data/contracts, permissions, runtime/env, tests, docs, and deployment.
2. Run the scanner and inspect its leads.
3. Trace fake/fallback leads to production reachability.
4. Review tests against claimed behavior. Ask: would the test fail if the implementation returned plausible but wrong data?
5. Review engineering quality by primary language and framework. Focus on module boundaries, package direction, reuse, abstraction, error handling, data flow, and testability.
6. Produce targeted actions: minimal fix, better design option, owner role, acceptance criteria, and proof command.
7. Decide merge status: `block`, `changes_requested`, `risky_but_mergeable`, or `pass`.

## Expected Output

Lead with:

```text
Redteam Verdict: block | changes_requested | risky_but_mergeable | pass
```

Then include PR intent, evidence read, findings sorted by severity, fake/fallback analysis, engineering quality scorecard, targeted optimization plan, verification gaps, and merge decision. Use the format in [references/output-contract.md](references/output-contract.md).
