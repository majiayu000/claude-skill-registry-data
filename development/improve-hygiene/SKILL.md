---
name: improve-hygiene
description: Find and implement a valid quick-win improvement to codebase hygiene in the current project. Use when the user asks to improve hygiene, clean up maintenance debt, remove dead code, remove stale feature flags, prune unused dependencies, consolidate duplicated utilities, refresh outdated docs, or make a small cleanup that reduces confusion without broad refactoring. The skill must prioritize low-risk, evidence-backed changes that preserve intended behavior and must explain the completed change plus provide an accurate git commit message in the required format.
---

# Improve Hygiene

## Goal

Improve codebase hygiene with a small sensible change that reduces maintenance burden, stale surface area, or confusion. Prefer evidence-backed cleanup over speculative refactoring, and preserve intended behavior unless the discovered hygiene issue includes a tiny correctness fix.

## Workflow

1. Inspect the project structure, package manifests, scripts, documentation, test framework, lint/typecheck setup, and existing style before editing.
2. Search for quick-win hygiene opportunities such as dead code, unused imports or exports, unused dependencies, stale feature flags, duplicated utilities, obsolete config, outdated docs, unused assets, misleading comments, dead package scripts, or cleanup TODOs that are already resolved.
3. Choose one improvement that is valid on its own merits. Do not optimize for churn, broad deletion, formatter noise, or cosmetic cleanup that does not reduce real maintenance risk.
4. Confirm evidence before changing anything. Use the strongest practical signal available, such as static analysis, package-manager output, test/build errors, import searches, manifest references, documentation references, route or entrypoint checks, or current project conventions.
5. Treat public APIs, package exports, CLI commands, migrations, generated files, dynamic imports, and externally consumed config as higher risk. Change them only when the project provides clear evidence that the surface is internal or obsolete.
6. Make the smallest coherent edit that resolves the selected hygiene issue. Update nearby tests, docs, manifests, lockfiles, or config only when required to keep the project consistent.
7. Run the most relevant verification command, usually a focused test, lint, typecheck, build, dependency check, or docs-related check. Run broader verification only when the change touches shared helpers, package manifests, config, or cross-cutting behavior.
8. If verification fails, fix only failures directly related to the chosen hygiene improvement. Do not chase unrelated failures.
9. Review the diff before responding so the explanation and git message describe only actual changes.

## Good Quick Wins

Prefer improvements that:

- Remove unused local helpers, imports, variables, test fixtures, assets, or files when references and tooling show they are dead.
- Remove unused dependencies or dev dependencies when imports, config references, package scripts, and lockfile updates can be verified.
- Delete stale feature flags or obsolete branches when current code, config, tests, or docs clearly establish the active behavior.
- Replace a duplicated local utility with an existing shared helper when the semantics are identical and nearby coverage or focused verification protects the change.
- Simplify obsolete compatibility code when supported versions, package metadata, or project docs show it is no longer needed.
- Refresh docs, comments, examples, scripts, or environment samples that clearly contradict current code or commands.
- Remove dead package scripts, config entries, aliases, routes, or build artifacts that are no longer referenced by the project.
- Add or adjust a focused test only when it protects behavior affected by the cleanup or documents why the cleanup is safe.

Avoid:

- Broad refactors, mass formatting, large file moves, or cleanup campaigns.
- Removing public exports, CLI commands, routes, database migrations, generated files, or integration hooks without strong evidence they are unused.
- Guessing that a feature flag is stale because it looks old; require evidence from config, call sites, tests, docs, or product context.
- Treating a simple text search as conclusive for dynamic imports, reflection, plugin registration, generated code, or externally consumed packages.
- Updating dependencies for freshness alone, unless the task explicitly asks for upgrades.
- Deleting TODOs, comments, docs, or examples merely because they are old.
- Changing behavior under the label of hygiene unless the behavior is clearly accidental or directly tied to the cleanup.
- Weakening tests, disabling lint rules, lowering type strictness, deleting assertions, or ignoring verification failures.

## Reporting

After completing the change, tell the user:

- What hygiene change was made.
- Why it is a meaningful improvement and what maintenance burden, stale surface area, or confusion was reduced.
- Which verification command ran and whether it passed. If verification could not run, explain why.
- A git commit message that follows the exact format below and describes only the actual diff.

Use this commit message format exactly:

```text
<main message>

<explaining sentence 1>
<explaining sentence 2>
<explaining sentence 3 - optional>
```

Main message rules:

- Write one sentence that summarizes the whole change.
- Use imperative mood, such as `Add`, `Fix`, `Refactor`, or `Remove`.
- Keep it under about 60 characters where possible.
- Capitalize the first word and do not end with a period.
- Be specific about the component, feature, or behavior affected.

Description rules:

- Write 2 sentences, or 3 only when the change genuinely needs it.
- Explain what changed and why, not a line-by-line account of how.
- Make every sentence complete and grammatical, ending with a period.
- Mention side effects, behavioral changes, or anything a reviewer must know.

Accuracy rules:

- Describe only changes visible in the diff.
- Do not invent files, functions, motivations, or effects.
- If the reason is not evident, describe the effect rather than guessing intent.
- If the diff is too ambiguous to describe safely, say so in one line instead of fabricating.
