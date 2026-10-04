---
name: review
description: Review working changes - code quality, security, library correctness, and standards auto-fix
argument-hint: "[--fix] [--strict] [--standards-only] [--files file1.py file2.py]"
---

# /review - Code Review & Standards Check

Full code review of all working changes: regex correctness, backward compatibility, security analysis, logic review, and project standards. All rules are embedded below — no external files need to be read.

## Usage

```
/review                  # Full review (code review + standards) + auto-fix (ruff)
/review --fix            # Also attempt manual fixes beyond ruff
/review --strict         # All warnings become errors
/review --standards-only # Skip code review, only check project standards
/review --files f.py     # Review specific files only
```

## Workflow

### Step 1: Gather Changes

```bash
# Run in parallel
git status                    # All changed/untracked files
git diff --name-only          # Unstaged changes
git diff --cached --name-only # Staged changes
```

Combine into a single deduplicated file list. If `--files` was provided, filter to only those files.

### Step 2: Categorize Files

| Category | Pattern | Rules Applied |
|----------|---------|---------------|
| Parser Core | `user_agent_parser/parser.py` | PA01-PA06, P01-P06 |
| Advanced Engine | `user_agent_parser/advanced_engine.py` | EN01-EN04, P01-P06 |
| Analytics | `user_agent_parser/analytics.py` | AN01-AN02, P01-P06 |
| Constants | `user_agent_parser/constants.py` | C01-C02, P01-P06 |
| Devices | `user_agent_parser/modern_devices.py` | C01, P01-P06 |
| Public API | `user_agent_parser/__init__.py` | API01-API02, P01-P06 |
| Tests | `tests/**/*.py` | T01-T05 |
| Non-Python | `*.yml`, `*.toml`, `*.md`, etc. | Skip rule checks |

### Step 3: Auto-Fix (always runs)

Run ruff on all changed Python files:

```bash
poetry run ruff check --fix <changed_python_files>
poetry run ruff format <changed_python_files>
```

Report what was auto-fixed.

### Step 4: Apply Rule Checks (Standards)

Read each changed file and apply rules based on its category. Use the rule tables below.

**For each file:**
1. Read the file content
2. Determine its category from Step 2
3. Check every applicable rule
4. Record findings with rule ID, severity, file path, line number, and description

### Step 5: Code Review (skip if `--standards-only`)

For each changed file, perform an actual code review beyond standards. Read the **full diff** (`git diff` for unstaged, `git diff --cached` for staged) to understand what changed, then review for:

#### 5a. Security Review (SEC rules)

| ID | Category | What to Look For |
|----|----------|-----------------|
| SEC01 | Secrets | Hardcoded API keys, tokens, or credentials in any file |
| SEC02 | ReDoS | Regex patterns vulnerable to catastrophic backtracking (nested quantifiers, overlapping alternations) |
| SEC03 | Input Safety | User agent strings used in ways that could cause injection (e.g., passed to `eval`, `exec`, `subprocess`, format strings) |

#### 5b. Logic & Correctness Review (LG rules)

| ID | Category | What to Look For |
|----|----------|-----------------|
| LG01 | Regex Correctness | Patterns that don't match what they claim to (wrong escaping, greedy vs lazy, missing anchors, incorrect character classes) |
| LG02 | IndexError Guards | Accessing `self._token[n]` or list indices without checking `len()` first — the parser splits on `;` and `/` and indices vary by UA string |
| LG03 | Cache Mutation | `@lru_cache` returns mutable objects (list, dict) that callers could mutate, poisoning the cache. Return tuples or frozen types instead |
| LG04 | Off-by-One | Loop bounds, string slicing, version number extraction edge cases (e.g., version string with no dots) |
| LG05 | None Handling | `.get()` or regex `.group()` results used without None checks |
| LG06 | Thread Safety | Shared mutable state accessed from `ThreadPoolExecutor` in batch operations without locks |

#### 5c. Implementation Quality (IQ rules)

| ID | Category | What to Look For |
|----|----------|-----------------|
| IQ01 | Performance | Compiling regex on every call instead of caching, regex in hot loops, unnecessary re-parsing |
| IQ02 | Better Approach | Reinventing patterns that already exist in the codebase, duplicating logic across parser.py and advanced_engine.py |
| IQ03 | API Design | Inconsistent return types, breaking changes to `parse()` tuple or `AdvancedResult` fields |
| IQ04 | Scalability | Unbounded growth in analytics data structures, O(n*m) patterns in batch processing |

**How to review:**
1. Read the full diff to understand the change context
2. For each changed function/method, trace the data flow
3. Check surrounding unchanged code for context — the diff alone may miss interaction issues
4. Flag concrete issues with specific file:line references. Do NOT flag hypothetical/unlikely issues.

### Step 6: Generate Report

```markdown
## Review: Working Changes

**Files reviewed:** N | **Auto-fixed:** N issues (ruff)

### SECURITY (fix before commit)
- [ ] [SEC02] `user_agent_parser/parser.py:45` - Nested quantifier `(\w+)*` in browser regex — vulnerable to ReDoS
- [ ] [SEC01] `tests/test_utils.py:12` - Test file contains hardcoded API token

### CODE REVIEW (fix before commit)
- [ ] [LG02] `user_agent_parser/parser.py:78` - `self._token[2]` accessed without bounds check — will crash on short UA strings
- [ ] [LG03] `user_agent_parser/parser.py:34` - `_cached_parse_user_agent` returns mutable list via lru_cache — callers can poison cache
- [ ] [LG01] `user_agent_parser/parser.py:120` - Browser regex `Chrome/(\d+)` misses versions like `Chrome/120.0.6099.130`

### BETTER APPROACH
- [ ] [IQ02] `user_agent_parser/advanced_engine.py:90` - Duplicates browser detection logic from parser.py — reuse `browser_rules`
- [ ] [IQ01] `user_agent_parser/parser.py:56` - `re.compile()` called inside method — move to class-level constant

### STANDARDS: CRITICAL (must fix before commit)
- [ ] [PA01] `user_agent_parser/parser.py:45` - New regex pattern not tested with real UA strings
- [ ] [API01] `user_agent_parser/__init__.py:12` - `parse()` return tuple changed from 7 to 8 elements — backward compat break

### STANDARDS: WARNING (should fix)
- [ ] [P03] `user_agent_parser/advanced_engine.py:23` - Uses `match/case` syntax — requires Python 3.10+, project supports 3.8+
- [ ] [T03] `tests/test_user_agent_parser.py:45` - New browser detection has no parametrized test cases with real UA strings

### STANDARDS: SUGGESTION (nice to have)
- [ ] [P06] `user_agent_parser/parser.py:30` - Missing type hint on `get_browser()` return
```

If `--strict`: treat all WARNINGs as CRITICALs in the report.

### Step 7: Fix Mode (`--fix`)

When `--fix` is passed, attempt to fix these issues automatically **after** reporting:

| Rule | Auto-Fix Action |
|------|----------------|
| LG02 | Add `if len(self._token) > N` guard before index access |
| IQ01 | Move `re.compile()` calls to class-level or module-level constants |
| P03 | Replace `match/case` with `if/elif` chains |
| P04 | Replace `X \| Y` type unions with `Union[X, Y]` |

For each fix applied, show what changed. Do NOT auto-fix these (require human judgment): regex patterns (LG01), cache mutation (LG03), API changes (API01-API02), security issues (SEC01-SEC03).

---

## Embedded Rules

### CRITICAL Rules (must fix before commit)

#### Parser Rules

| ID | Rule | Check |
|----|------|-------|
| PA01 | Regex patterns must be tested | Any new or modified regex in `browser_rules` or device detection must have corresponding test cases using real UA strings |
| PA02 | browser_rules ordering preserved | New entries in `browser_rules` must not change the match priority of existing entries — earlier rules take precedence. Edge browsers must come before Chrome, etc. |
| PA03 | _token bounds checking | Every access to `self._token[n]` must be guarded by `len(self._token) > n` or equivalent. The `_token` list varies in length depending on the UA string |
| PA04 | parse() tuple shape stable | The `parse()` function must always return a 7-tuple: `(browser, browser_version, os, os_version, device_type, device_name, device_host)`. Any change to tuple length or element meaning breaks all downstream consumers |
| PA05 | Cached function purity | Functions decorated with `@lru_cache` must not return mutable objects (list, dict, set). Return tuples, frozensets, or dataclass instances instead |
| PA06 | Compiled regex caching | Regex patterns used in hot paths (`_browser_version_re`, `browser_rules`) must use cached compiled patterns, not `re.compile()` on every call |

#### Engine Rules

| ID | Rule | Check |
|----|------|-------|
| EN01 | AdvancedResult fields stable | Do not remove or rename fields in `AdvancedResult`, `BrowserCapabilities`, `SecurityFingerprint`, or `DeviceCategory` — these are public API |
| EN02 | Confidence scoring bounded | Confidence values must be in range [0.0, 1.0] — check arithmetic doesn't produce values outside this range |
| EN03 | DeviceCategory enum stable | Do not remove or rename existing `DeviceCategory` enum values — only add new ones |
| EN04 | ThreadPoolExecutor cleanup | Batch operations using `ThreadPoolExecutor` must properly shut down the executor (use `with` statement or explicit `shutdown()`) |

#### API Rules

| ID | Rule | Check |
|----|------|-------|
| API01 | Public API backward compatible | Functions exported in `__init__.py` (`parse`, `Parser`, `analyze`, `batch_analyze`, `generate_analytics`) must not change their signatures or return types in breaking ways |
| API02 | Import paths preserved | Do not move or rename public classes/functions that users import directly. Check that `__all__` is consistent with actual exports |

#### Constants Rules

| ID | Rule | Check |
|----|------|-------|
| C01 | Device code consistency | Entries in `MOBILE_DEVICE_CODE_NAME` must use consistent format: model code key → human-readable name value. No duplicate keys |
| C02 | Constant values immutable | `OS`, `DeviceType`, `DeviceName` class attributes must not be changed — only new attributes can be added |

### WARNING Rules (should fix)

#### Python Compatibility

| ID | Rule | Check |
|----|------|-------|
| P01 | No walrus operator in critical paths | `:=` (walrus operator) requires Python 3.8+ — acceptable but flag if used in untested code |
| P02 | No `match`/`case` statements | `match`/`case` requires Python 3.10+ — project supports 3.8+ |
| P03 | No `X \| Y` type union syntax | `X \| Y` type syntax requires Python 3.10+ — use `Union[X, Y]` or `Optional[X]` from `typing` |
| P04 | No `TypeAlias` annotation | `TypeAlias` requires Python 3.10+ — use plain assignment or `typing_extensions` |
| P05 | No `from __future__ import annotations` side effects | If using `from __future__ import annotations`, ensure no runtime type checks rely on string annotations being resolved |

#### Test Coverage

| ID | Rule | Check |
|----|------|-------|
| T01 | New parser features need parametrized tests | New browser/device/OS detection must have `@pytest.mark.parametrize` test cases with real-world UA strings |
| T02 | New source files need tests | Any new `.py` file in `user_agent_parser/` (excluding `__init__.py`) must have corresponding test coverage |
| T03 | Edge cases for parsing | Tests should cover: empty string, `None` input, extremely long UA strings, UA strings with no parentheses, single-token UA strings |
| T04 | Backward compatibility tests | Changes to `parse()` or `Parser` must include tests verifying the 7-tuple return format is preserved |
| T05 | Performance regression tests | Changes to hot paths (parser, regex, caching) should verify no performance regression via benchmark or timing assertions |

#### Library Quality

| ID | Rule | Check |
|----|------|-------|
| P06 | Type hints on public API | Public functions and methods should have parameter and return type hints |
| LQ01 | LRU cache key hygiene | Arguments to `@lru_cache` decorated functions must be hashable. Verify no lists, dicts, or sets are passed as arguments |
| LQ02 | Thread safety in batch ops | `batch_analyze()` and `BatchProcessor` must not share mutable state across threads without synchronization |
| LQ03 | Regex in hot loops | Regex compilation (`re.compile`, `re.search`, `re.match`) should not occur inside frequently-called methods — compile once at module/class level |
| LQ04 | CHANGELOG updated | Non-trivial changes (new features, bug fixes, API changes) should have a corresponding CHANGELOG.md entry |

### SUGGESTION Rules (nice to have)

| ID | Rule | Check |
|----|------|-------|
| SG01 | Docstrings on public API | Public functions/classes should have docstrings describing parameters and return values |
| SG02 | Type hints on internal methods | Internal methods benefit from type hints for maintainability |
| SG03 | Consistent naming | New constants/methods should follow existing naming patterns in the codebase |
| SG04 | Test organization | Tests should be grouped by feature area and use descriptive names |
| SG05 | Code reuse | Shared logic between `parser.py` and `advanced_engine.py` should be factored into common utilities rather than duplicated |

---

## Rule Detection Patterns

Quick-reference regex/string patterns for detecting violations:

```python
# PA03 - Unguarded _token access (CRITICAL)
r'self\._token\[(\d+)\]'  # Find all _token[N] accesses, verify bounds check exists

# PA04 - parse() return tuple (CRITICAL)
r'return\s*\(' # In parse() / _cached_parse_user_agent, count tuple elements

# PA05 - Mutable lru_cache return (CRITICAL)
r'@(functools\.)?lru_cache'  # Find cached functions, check if they return list/dict/set

# PA06 / LQ03 - Regex in hot path (CRITICAL/WARNING)
r're\.(compile|search|match|findall)\s*\('  # Inside methods called per-parse

# P02 - match/case syntax (WARNING)
r'^\s*match\s+\w'  # Python 3.10+ only
r'^\s*case\s+\w'

# P03 - Union syntax (WARNING)
r'\w+\s*\|\s*\w+'  # In type annotations: X | Y instead of Union[X, Y]

# EN02 - Confidence out of bounds (CRITICAL)
r'confidence\s*[=+\-*/]'  # Check arithmetic on confidence values

# API01 - Public API signature changes
# Diff __init__.py and check for removed/changed exports in __all__

# C01 - Duplicate device codes (CRITICAL)
# Check MOBILE_DEVICE_CODE_NAME dict for duplicate keys

# SEC02 - ReDoS patterns
r'(\.\*|\.\+|\w\+)\*'  # Nested quantifiers
r'(\.\*|\.\+).*(\.\*|\.\+)'  # Multiple greedy quantifiers in alternation
```

## Quick Reference: What to Check by File Type

| File Type | Key Rules |
|-----------|-----------|
| `parser.py` | PA01-PA06, LG01-LG06, SEC02 |
| `advanced_engine.py` | EN01-EN04, LG06, P02-P04 |
| `analytics.py` | AN01-AN02 (thread safety, export correctness), LQ02 |
| `constants.py` | C01-C02 |
| `modern_devices.py` | C01 (consistency) |
| `__init__.py` | API01-API02 |
| `tests/*.py` | T01-T05 |
| All `*.py` | P01-P06, SEC01-SEC03 |
