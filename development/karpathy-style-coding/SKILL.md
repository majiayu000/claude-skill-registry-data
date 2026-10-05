---
name: karpathy-style-coding
description: Use when writing, reviewing, or modifying code and the user wants small, direct, well-verified changes inspired by Karpathy-style engineering principles.
---

# Karpathy-style Coding Principles for Codex

Use this skill when editing code, reviewing code, debugging, or making implementation decisions.

## 适用场景

- Writing, reviewing, or modifying code.
- Fixing bugs with a limited scope.
- Making small product or refactor changes where maintainability matters.
- Reviewing code and prioritizing real defects over style preferences.

## 不适用场景

- The user asks for pure brainstorming with no code changes.
- The task requires a domain-specific workflow that should use a more specific skill first.
- The user explicitly asks for a large redesign or architecture proposal before implementation.

## 工作流

1. Think before editing.
   - Understand the goal, existing code, constraints, and likely failure modes.
   - Read relevant files before changing them.
   - If the task is ambiguous but a safe assumption is possible, proceed and state the assumption briefly.

2. Prefer simple, direct solutions.
   - Choose the smallest solution that correctly solves the problem.
   - Avoid unnecessary abstractions, frameworks, cleverness, or speculative generalization.
   - Write code that a competent engineer can quickly read and modify later.

3. Make precise, minimal changes.
   - Keep edits tightly scoped to the user request.
   - Do not refactor unrelated code.
   - Do not change formatting, naming, dependencies, or architecture unless needed.
   - Preserve existing project style and conventions.

4. Work with the existing codebase.
   - Reuse local helpers, patterns, types, APIs, and tests before inventing new ones.
   - Match surrounding style even if it differs from your default preference.
   - Treat unexplained existing changes as user work; do not revert them unless explicitly asked.

5. Verify the result.
   - Run the most relevant tests, type checks, linters, or app-level checks when feasible.
   - If verification cannot be run, say exactly what was not run and why.
   - Prefer evidence from code or tools over confidence.

6. Optimize for the user actual goal.
   - Keep explanations concise and practical.
   - Surface important tradeoffs, risks, or assumptions.
   - In code review, prioritize bugs, regressions, edge cases, and missing tests over style opinions.

7. Avoid overengineering.
   - Do not add new abstractions just because duplication exists once or twice.
   - Do not make broad architectural changes for a narrow bug.
   - Do not introduce new dependencies unless they clearly reduce risk or complexity.

8. Be transparent while working.
   - Briefly explain what you are checking and why.
   - Before editing files, state what you are about to change.
   - After finishing, summarize what changed and how it was verified.

## 验证方式

- Run the most relevant test, type check, lint, build, or smoke check when feasible.
- Prefer narrow verification for narrow changes and broader verification for shared behavior.
- If verification cannot be run, state exactly what was not run and why.

## 安全边界

- Do not revert user changes unless explicitly asked.
- Do not introduce new dependencies or broad refactors without a clear need.
- Do not claim code is fixed without evidence from tests, tools, or direct inspection.
