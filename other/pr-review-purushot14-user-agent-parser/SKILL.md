---
name: pr-review
description: Review PR changes against project standards and post feedback
argument-hint: "[PR number] [--comment]"
---

# /pr-review - Pull Request Review

Review PR changes against project standards for this user-agent parsing library.

## Usage

```
/pr-review              # Review current branch's PR
/pr-review 123          # Review PR #123
/pr-review --comment    # Post review as PR comment
```

## Workflow

### Step 1: Get PR Context (run in parallel)
```bash
# Detect repo
REPO=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/.*github.com[:/]\(.*\)/\1/')

gh pr view --json number,title,baseRefName,headRefName,files
git diff origin/main...HEAD --name-only
git diff origin/main...HEAD --stat
```

If a PR number was provided, use `gh pr view <number>` and `gh pr diff <number>` instead.

### Step 2: Categorize Changed Files

| Category | Patterns |
|----------|----------|
| Parser Core | `user_agent_parser/parser.py` |
| Advanced Engine | `user_agent_parser/advanced_engine.py` |
| Analytics | `user_agent_parser/analytics.py` |
| Public API | `user_agent_parser/__init__.py` |
| Constants/Devices | `user_agent_parser/constants.py`, `user_agent_parser/modern_devices.py` |
| Tests | `tests/**/*.py` |
| CI/Config | `.github/workflows/*`, `pyproject.toml`, `poetry.lock` |
| Docs | `*.md`, `CHANGELOG.md` |

### Step 3: Apply Review Checks

Read changed files and verify against these standards:

#### Regex & Parser Correctness
| Check | Standard |
|-------|----------|
| Regex tested | Every new/changed regex has real UA string test cases |
| browser_rules order | New entries don't break priority (Edge before Chrome, Chrome before Safari, etc.) |
| _token bounds | Every `self._token[n]` access has `len()` guard |
| Compiled patterns | Hot-path regex uses cached compiled patterns, not `re.compile()` per call |
| ReDoS safety | No nested quantifiers or overlapping alternations that cause catastrophic backtracking |

#### Backward Compatibility
| Check | Standard |
|-------|----------|
| parse() 7-tuple | `parse()` still returns `(browser, browser_version, os, os_version, device_type, device_name, device_host)` |
| Public API stable | Functions in `__init__.py` / `__all__` unchanged in signature |
| AdvancedResult fields | No removed/renamed fields in `AdvancedResult`, `BrowserCapabilities`, `SecurityFingerprint` |
| DeviceCategory enum | No removed/renamed enum values, only additions |
| Constants immutable | `OS`, `DeviceType`, `DeviceName` attributes not changed, only extended |

#### Python 3.8+ Compatibility
| Check | Standard |
|-------|----------|
| No match/case | `match`/`case` requires 3.10+ — use `if`/`elif` |
| No union syntax | `X \| Y` in types requires 3.10+ — use `Union[X, Y]` |
| No TypeAlias | Requires 3.10+ — use plain assignment |
| No ParamSpec | Requires 3.10+ — use `typing_extensions` if needed |

#### Cache Safety
| Check | Standard |
|-------|----------|
| lru_cache returns immutable | Cached functions return tuples, not lists/dicts/sets |
| Cache key hashable | All arguments to cached functions are hashable |
| No cache side effects | Cached functions are pure (no mutations, no I/O) |

#### Test Coverage
| Check | Standard |
|-------|----------|
| New features tested | New parser/engine features have parametrized test cases |
| Real UA strings | Tests use real-world user agent strings, not fabricated ones |
| Edge cases covered | Empty string, None, very long strings, missing parentheses |
| New source files | New `.py` files in `user_agent_parser/` have test coverage |

#### Thread Safety
| Check | Standard |
|-------|----------|
| Batch processing | `ThreadPoolExecutor` usage includes proper cleanup (`with` statement) |
| No shared mutation | Batch operations don't share mutable state across threads |

#### Code Quality
| Check | Standard |
|-------|----------|
| Type hints | Public functions have parameter and return type hints |
| CHANGELOG | Non-trivial changes have CHANGELOG.md entry |
| Device code format | `MOBILE_DEVICE_CODE_NAME` entries follow key→name format, no duplicates |
| Consistent naming | New methods/constants follow existing naming patterns |

### Step 4: Generate Report

Structure findings by severity:

```markdown
## PR Review: #<number> - <title>

**Files Changed:** N | **Additions:** +N | **Deletions:** -N

### 🔴 Critical (blocks merge)
- [ ] `user_agent_parser/parser.py:78` - `self._token[3]` accessed without bounds check
- [ ] `user_agent_parser/__init__.py:15` - `parse()` return changed from 7-tuple to 8-tuple — breaks all consumers
- [ ] `user_agent_parser/parser.py:45` - New browser regex `(Chrome|CriOS)(\d+)*` has nested quantifier — ReDoS risk

### 🟡 Standards (should fix)
- [ ] `user_agent_parser/advanced_engine.py:120` - Uses `match/case` — Python 3.10+ only, project supports 3.8+
- [ ] `tests/test_user_agent_parser.py` - New Brave detection has no parametrized test cases
- [ ] Missing CHANGELOG.md entry for new feature

### 🟢 Suggestions (nice to have)
- [ ] `user_agent_parser/parser.py:90` - Add type hint to `get_device_name()` return
- [ ] `user_agent_parser/advanced_engine.py:45` - Browser detection duplicates logic from parser.py — consider reuse

---
**Verdict:** APPROVE | REQUEST_CHANGES | COMMENT
*Review based on project standards in CLAUDE.md*
```

### Step 5: Determine Verdict

| Condition | Verdict |
|-----------|---------|
| No critical issues, 0-2 standards issues | **APPROVE** |
| No critical issues, 3+ standards issues | **COMMENT** |
| Any critical issues | **REQUEST_CHANGES** |

### Step 6: Post Comment (if --comment)

Based on verdict:

```bash
# Clean — approve
gh pr review <number> --approve --body "$(cat <<'EOF'
<review-report>
EOF
)"

# Suggestions only — comment
gh pr review <number> --comment --body "$(cat <<'EOF'
<review-report>
EOF
)"

# Critical issues — request changes
gh pr review <number> --request-changes --body "$(cat <<'EOF'
<review-report>
EOF
)"
```

## Quick Reference: What to Check by File

| File | Key Checks |
|------|------------|
| `parser.py` | Regex correctness, browser_rules order, _token bounds, lru_cache mutation, compiled pattern caching |
| `advanced_engine.py` | AdvancedResult field stability, confidence bounds [0,1], DeviceCategory enum stability, ThreadPoolExecutor cleanup |
| `analytics.py` | Thread safety in BatchProcessor, export format correctness |
| `constants.py` | No changed existing values, consistent MOBILE_DEVICE_CODE_NAME format, no duplicate keys |
| `modern_devices.py` | DeviceSpec format consistency |
| `__init__.py` | Public API unchanged, __all__ consistent, parse() 7-tuple preserved |
| `tests/*.py` | Parametrized with real UA strings, edge cases covered, backward compat verified |
| `CHANGELOG.md` | Entry exists for non-trivial changes |
| `.github/workflows/*` | Python version matrix includes 3.8–3.15, codecov integration intact |
| `pyproject.toml` | Python requirement still >=3.8, no incompatible dependency versions |
