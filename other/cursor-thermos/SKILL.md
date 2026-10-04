---
name: cursor-thermos
description: "Launch both thermo-nuclear review subagents in parallel, then synthesize their findings. Use for thermos, double thermo review, or combined bug/security and code-quality branch audits."
---

## Codex runtime mapping

Pass the same scoped diff to two independent read-only native reviewers in parallel. Give the bug/security reviewer [its pinned role](references/bug-security-reviewer.md) and the code-quality reviewer [its pinned role](references/code-quality-reviewer.md); their full rubrics are `cursor-thermo-nuclear-review` and `cursor-thermos-thermo-nuclear-code-quality-review`. Follow the selected model/effort under `model-capability-router`. The coordinator verifies and synthesizes; if one lens fails, label the result partial.

# Thermos

Run the two thermo review passes as independent native read-only reviewers in parallel when available, then synthesize their results.

## Workflow

1. Determine the review scope from the user request, PR, current branch, or relevant changed files.
2. Gather the diff and any file/context excerpts needed for reviewers to evaluate the change without guessing.
3. Launch both native reviewers in parallel when available:
   - Give one the [bug/security role](references/bug-security-reviewer.md) and `cursor-thermo-nuclear-review` rubric for bugs, breakages, security, devex regressions, feature-flag leaks, and other branch-audit risks.
   - Give the other the [code-quality role](references/code-quality-reviewer.md) and `cursor-thermos-thermo-nuclear-code-quality-review` rubric for maintainability, structure, file-size growth, spaghetti, abstractions, and codebase-health risks.
4. Pass each subagent the same scoped diff/file context and ask it to return prioritized findings with file references and evidence.
5. After both finish, synthesize the results with findings first, deduplicated across reviewers. Weight overlapping findings more heavily, resolve disagreements with your own judgment, and keep summaries brief.

If individual background summaries are already visible to the user, do not restate them wholesale. Surface the unified verdict, the highest-signal findings, and any remaining uncertainty.
