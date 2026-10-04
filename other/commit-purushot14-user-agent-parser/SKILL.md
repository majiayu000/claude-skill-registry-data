---
name: commit
description: Create well-formatted git commits following project conventions with emoji, type, and scope
argument-hint: "[message hint]"
---

# /commit - Smart Git Commit

## Usage

```
/commit              # Auto-generate commit for staged/unstaged changes
/commit <message>    # Use provided message as starting point
```

## Workflow

### Step 0: Run /review (MANDATORY)

**Before any commit work, invoke the `/review` skill** to review and auto-fix all working changes.

- Run `/review` using the Skill tool
- If there are **CRITICAL** findings, **STOP** — report them to the user and do NOT proceed to commit
- If there are only **WARNING** or **SUGGESTION** findings, note them in the commit output but proceed
- The review auto-runs `ruff check --fix` and `ruff format`, so code is clean before commit

### Step 1: Gather Context (run in parallel)
```bash
git status              # Modified/untracked files
git diff --stat         # Summary of changes
git log --oneline -5    # Recent commit style
```

### Step 2: Analyze & Group
- Identify distinct features/contexts
- **Split ONLY for BIG unrelated features** (e.g., new browser detection + analytics rewrite + CI overhaul)
- **Keep together** all files for ONE feature (parser + constants + tests)

### Step 3: Stage, Commit, Verify
```bash
git add <specific-files>
git commit -m "$(cat <<'EOF'
<emoji> <type>(<scope>): <subject>

<body>

- <emoji> Change 1
- <emoji> Change 2
EOF
)"
git status              # Verify success
```

## Type Reference

| Type | Emoji | Use Case | Body Emojis |
|------|-------|----------|-------------|
| feat | ✨ | New feature | ✨ addition, 🔧 config |
| fix | 🐛 | Bug fix | 🐛 fix, 🛡️ validation |
| docs | 📝 | Documentation | 📝 docs |
| style | 💄 | Formatting only | 💄 format |
| refactor | ♻️ | Code restructure | ♻️ refactor, 🔥 removal |
| perf | ⚡ | Performance | ⚡ optimize |
| test | ✅ | Tests | ✅ test, 📋 logging |
| build | 📦 | Dependencies | 📦 deps |
| ci | 🌐 | CI/CD | 🌐 pipeline, 🚀 deploy |
| chore | 🔧 | Maintenance | 🔧 tooling |
| revert | ⏪ | Revert commit | ⏪ revert |
| remove | 🔥 | Remove code/files | 🔥 delete |

## Scope Priority (for multi-area changes)

When changes span multiple areas, use the **highest priority** scope:

| Priority | Scope | File Paths |
|----------|-------|------------|
| 1 | parser | `user_agent_parser/parser.py` |
| 2 | engine | `user_agent_parser/advanced_engine.py` |
| 3 | analytics | `user_agent_parser/analytics.py` |
| 4 | devices | `user_agent_parser/modern_devices.py`, `MOBILE_DEVICE_CODE_NAME` in constants |
| 5 | constants | `user_agent_parser/constants.py` |
| 6 | api | `user_agent_parser/__init__.py` (public API surface) |
| 7 | tests | `tests/*` |
| 8 | ci | `.github/workflows/*` |
| 9 | deps | `pyproject.toml`, `poetry.lock` |

## Rules

| Rule | Details |
|------|---------|
| Subject | Max 50 chars, imperative mood |
| Body | Wrap at 72 chars, explain what & why |
| Staging | Name specific files, never `git add -A` |
| Format | Always use HEREDOC (see Step 3) |
| Commits | Always NEW commits, never amend |
| Co-Author | **NEVER** add Co-Authored-By |

## Error Handling

| Error | Action |
|-------|--------|
| /review has CRITICAL findings | Report findings to user and **STOP** — do not commit |
| Pre-commit hook fails | Fix issue, re-stage, create **NEW** commit |
| Nothing to commit | Report to user and stop |
| Merge conflicts | Report to user and stop |

## Examples

**Single feature** (parser + constants + tests):
```bash
git add user_agent_parser/parser.py user_agent_parser/constants.py tests/test_user_agent_parser.py && \
git commit -m "$(cat <<'EOF'
✨ feat(parser): add Brave browser detection

Add regex pattern for Brave browser identification.

- ✨ Add Brave to browser_rules tuple
- 🔧 Add Brave to constants
- ✅ Add parametrized test cases
EOF
)"
```

**Split only for BIG unrelated features**:
```bash
# Commit 1: New device support
git add user_agent_parser/constants.py user_agent_parser/modern_devices.py && \
git commit -m "$(cat <<'EOF'
✨ feat(devices): add Galaxy S25 device specs

- ✨ Add SM-S93x model codes to MOBILE_DEVICE_CODE_NAME
- ✨ Add DeviceSpec entries for Galaxy S25 series
EOF
)"

# Commit 2: Unrelated analytics fix
git add user_agent_parser/analytics.py tests/test_advanced_engine.py && \
git commit -m "$(cat <<'EOF'
🐛 fix(analytics): correct device distribution percentages

- 🐛 Fix floating point rounding in distributions
- ✅ Add edge case tests for empty datasets
EOF
)"
```
