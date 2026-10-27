---
name: git-workflow
description: "Universal standards for atomic commits, Conventional Commits formatting, clean branch lifecycles, and pull request hygiene for autonomous coding agents."
---

# Git Workflow & Commit Discipline Protocol

When staging changes, authoring commits, managing branches, or creating pull requests, adhere strictly to this workflow.

---

## 1. Atomic Commits Discipline

1. **One Logical Change per Commit**:
   - Each commit must represent a single, coherent modification (e.g. one bug fix, one refactor, or one feature step).
   - Never combine unrelated changes (e.g. formatting the entire codebase in the same commit as a critical auth fix).
2. **Never Break the Build**:
   - Every individual commit on a shared branch must compile, pass linting, and pass automated tests.
3. **Clean Working Tree**:
   - Stage specific files explicitly with `git add <file>...`. Avoid blanket `git add .` unless every changed file has been deliberately inspected with `git diff`.

---

## 2. Conventional Commits Standard

Format all commit messages according to the Conventional Commits specification:

```
<type>(<scope>): <short imperative summary>

[optional body explaining rationale and blast radius]

[optional footer: Breaking changes or issue references]
```

### Standard Types
- `feat`: A new user-facing feature or capability.
- `fix`: A bug fix or error correction.
- `refactor`: Code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance or reduces latency.
- `test`: Adding missing tests or correcting existing tests.
- `docs`: Documentation only changes.
- `chore`: Maintenance tasks, dependency updates, or configuration adjustments.

### Rules for the Subject Line
- Use the imperative mood ("add", "fix", "update", not "added", "fixes", "updated").
- Do not capitalize the first letter after the colon.
- Do not place a period at the end of the subject line.
- Maximum 72 characters for the header.

---

## 3. Branch Lifecycle & Rebase Strategy

1. **Feature Branch Naming**:
   - `feat/<short-description>`
   - `fix/<issue-id>-<short-description>`
   - `refactor/<scope>`
2. **Linear History with Rebase**:
   - Before opening a PR or merging into the main branch, rebase on latest `main` to maintain a clean linear commit graph:
     ```bash
     git fetch origin main
     git rebase origin/main
     ```
   - Squash ephemeral checkpoint commits (`wip`, `temp`, `fix typo`) before merging.

---

## 4. Pull Request Hygiene

Every pull request description must provide:
1. **Summary of Changes**: Concise bullet list of modifications.
2. **Motivation & Context**: Why this change is necessary.
3. **Verification Evidence**: Literal command output demonstrating tests and linters pass (`exit code 0`).
4. **Blast Radius Assessment**: List of systems, routes, or database tables impacted.
