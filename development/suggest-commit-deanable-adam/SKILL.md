---
name: suggest-commit
description: Generate conventional commit message suggestions for staged git changes, aligned with the repository's commit style. Use when the user wants a commit message suggestion, asks what to commit, or says "suggest commit".
disable-model-invocation: true
---

# Suggest Commit

## Git Command Safety

NEVER use `cd <path> && git` compound commands — they trigger security approval prompts. Run `git` commands directly (the working directory is already the target repo), or use `git -C <path>` if you need to target a different directory.

## Critical Rules

**ALWAYS:**
- Run the git commands below EVERY time - never assume or remember previous state
- Base suggestions ONLY on the actual `git diff --cached` output from THIS invocation
- Only consider **staged** changes (`--cached`) — unstaged changes, untracked files, and working tree modifications are irrelevant

**NEVER:**
- Use conversation history, memory, or previously seen file changes as input for the suggestion
- Reference or incorporate any code changes you may have seen, made, or discussed earlier in this conversation — they are not the source of truth; only the staged diff output is
- Include the "Generated with Claude Code" footer, "Co-Authored-By: Claude" line, or any other Claude Code attribution text

These footers are for actual commits only, NOT for commit suggestions.

> **Why this matters:** The user may have viewed, edited, or discussed many files during the conversation. Only the files that appear in `git diff --cached` output are staged and relevant. Everything else must be ignored completely.

## Execution Steps

### Step 1: Gather Git Information

Run these commands every time this skill is invoked. **Do not rely on previous context, conversation history, or memory — the output of these commands is the ONLY source of truth:**

```bash
git diff --cached --stat           # Change overview with insertions/deletions
git diff --cached --name-only      # List of staged files
git log --oneline -15              # Recent commits for style reference
```

**Important:** If the `git diff --cached` commands return empty output, there are NO staged changes — report that to the user and stop. Do NOT fall back to unstaged changes or conversation context.

### Step 2: Analyze Change Scope

**If no staged changes:** Inform the user there is nothing to commit.

**If changes exist:** Determine if this is a small or large changeset:
- **Small** (1-5 related files): Suggest a single commit
- **Large** (6+ files OR multiple unrelated areas): Group into logical commits

For large changesets, also run:
```bash
git diff --cached                  # Full diff for understanding changes
```

### Step 3: Generate Commit Suggestions

#### Commit Message Format

Follow Conventional Commits format matching the repository's style:

```
type(scope): short description

- Bullet point explaining what changed
- Another bullet if needed
```

**Rules:**
- Use imperative mood ("add" not "added")
- No period at end of description
- Keep description under 50 characters (72 max)
- Scope is optional but recommended for clarity

#### Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | New functionality, features |
| `fix` | Bug fixes, correcting behavior |
| `docs` | Documentation only (.md files, comments) |
| `chore` | Maintenance, config, dependencies |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests |
| `perf` | Performance improvements |
| `style` | Formatting, whitespace (no logic changes) |
| `build` | Build system, CI configuration |
| `ci` | CI/CD pipeline changes |

#### Scope Heuristics

Determine scope from file paths:
- `plugins/azure-iot/` -> `azure-iot`
- `src/Services/Auth*` -> `auth`
- `docs/guides/` -> `docs` or omit scope
- Match existing scopes from repo history when possible

### Step 4: Grouping Rules for Large Changes

When suggesting multiple commits:

1. **Group by feature/domain first** - All auth-related files together, all API files together
2. **Group by type second** - All docs together, all tests together
3. **Never suggest the same file for multiple commits**
4. **Order commits logically** - Dependencies first, then dependents

### Step 5: Output Format

#### Single Commit Example

```
feat(api): add deviceType filter to GetDeviceIdentities endpoint

- Add optional deviceType query parameter to filter devices
- Add DevicesByType query for filtering without text filter
- Consolidate duplicate query methods
```

#### Multiple Commits Example

```
## Suggested Commits

### Commit 1
feat(auth): implement JWT token service

- Add JwtTokenService for token generation
- Add token validation logic

**Files:**
- src/Services/JwtTokenService.cs
- tests/JwtTokenServiceTests.cs

---

### Commit 2
feat(api): add authentication endpoint

- Add login endpoint with JWT response
- Add request/response models

**Files:**
- src/Controllers/AuthController.cs
- src/Models/LoginRequest.cs
- src/Models/LoginResponse.cs

---

### Commit 3
docs: add authentication setup guide

**Files:**
- docs/AUTHENTICATION.md
```

## Guidelines

- Always analyze the actual diff content to understand what changed
- Match the repository's existing commit style from recent history
- Never duplicate files across multiple commit suggestions
- If uncertain about grouping, prefer fewer, more comprehensive commits
- Include the commit body bullets only when changes need explanation
