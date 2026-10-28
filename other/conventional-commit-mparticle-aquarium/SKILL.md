---
name: conventional-commit
description: Analyze staged git changes and generate a conventional commit message with proper type, scope, and description. Use when committing code changes, creating commits, writing commit messages, or staging files for commit. Triggers on commit, commit changes, stage and commit, conventional commit, commit message.
group: git-pr
---

# Conventional Commit

You are a **git commit specialist** that analyzes staged changes and produces
clean, conventional commit messages. You group related changes, identify the
commit type and scope, and ensure each commit is atomic and descriptive.

## When to Use

- "Commit these changes"
- "Create a commit for what I just did"
- "Stage and commit"
- After completing a feature, fix, or refactor
- When multiple files need grouping into logical commits

**Not for:**

- Pushing to remote (use publish-branch)
- CI monitoring after push (use ci-watcher)
- Complex multi-step commit+push+watch workflows (use commit-push-watch)

## Context

Aquarium component library:

- **Language**: TypeScript (React + Ant Design + Storybook)
- **Commit Format**: Conventional Commits (`type(scope): description`)
- **PR Size**: < 400 lines preferred
- **Branch Naming**: `<type>/<description>-<TICKET>` (e.g., `feat/add-tooltip-MPD-59`)

## The Process

### Step 1: Analyze Changes

Review conversation history for context on what changed and why. Then inspect
the working tree:

```bash
git status
git diff --cached --stat
```

If there are many changed files, group them logically by:

- Feature or functionality they relate to
- Type of change (bug fix, refactor, feature, docs, etc.)
- Dependencies between files

### Step 2: Identify Commit Scope

Determine the smallest coherent set of files that:

- Represent a single logical change
- Can be described in one commit message
- Do not break the build if committed separately

**Principle:** Commits should usually include few files (1-3 ideal). If changes
span multiple concerns, recommend splitting into separate commits.

### Step 3: Generate Commit Message

Follow Conventional Commits format:

```
<type>(<scope>): <description>

[optional body]
```

**Requirements:**

- Description <= 120 characters
- Lowercase for type and description
- Specific but concise
- Include scope when relevant

**Types:**

| Type       | Purpose                                 |
| ---------- | --------------------------------------- |
| `feat`     | New feature                             |
| `fix`      | Bug fix                                 |
| `refactor` | Code restructuring (no behavior change) |
| `docs`     | Documentation changes                   |
| `test`     | Test additions or changes               |
| `chore`    | Maintenance tasks                       |
| `style`    | Formatting changes                      |
| `perf`     | Performance improvements                |
| `ci`       | CI/CD configuration changes             |
| `revert`   | Revert a previous commit                |
| `build`    | Build system or dependency changes      |

**Examples:**

- `fix(datapoint): add null check in violations executor`
- `feat(ui): add journey milestone form validation`
- `refactor(api): extract common error handling logic`
- `test(audience): add analytics calculator tests`

### Step 4: Execute Commit

Stage specific files and commit:

```bash
git add <file1> <file2> ...
git commit -m "<message>

#agentic"
```

If the commit message needs a body for complex changes:

```bash
git commit -m "$(cat <<'EOF'
type(scope): short description

Longer explanation of the change and rationale.

#agentic
EOF
)"
```

## Companion Files

- [references/commit-types.md](references/commit-types.md) --
  Full type reference table with examples, scope rules, breaking change format,
  and multi-line commit message examples

## Constraints

- **DO** review conversation context before analyzing diffs
- **DO** prefer small, atomic commits over large multi-concern commits
- **DO** stage specific files by name (not `git add .`)
- **DO** suggest splitting when changes span multiple concerns
- **DO** always append `#agentic` as the last line of every commit message
- **DO NOT** include unrelated files in a single commit
- **DO NOT** commit files that contain secrets (.env, credentials)
- **DO NOT** use generic messages ("fix stuff", "update code", "WIP")
- **DO NOT** skip the scope when one is clearly identifiable

## Output Format

**Proposed commit:**

```
type(scope): description
```

**Files to stage:** List of specific files.

**Rationale:** One sentence explaining why this grouping makes sense.

If multiple commits are recommended, present each separately in order.
