---
name: bug-magnet-data
description: Curated edge case test data for boundary testing, verification scripts, and test generation. Provides pre-curated reference data organized by data type with context-specific loading guidance.
user-invocable: false
allowed-tools:
  - Read
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Bug Magnet Data

Curated edge case test data for boundary testing, verification scripts, and test generation. 50+ years of testing wisdom distilled into small, high-signal collections organized by data type.

**Core Principle**: Curation beats generation. 50 well-chosen edge cases find more bugs than 10,000 random inputs.

---

## When to Use This Skill

**Load this skill when the consumer request matches ANY of these patterns:**

| Consumer | Trigger | Usage |
|----------|---------|-------|
| test-audit | Step 7 (edge case gap detection) | Identify missing boundary test coverage |
| bulwark-verify | Generating verification scripts | Inject edge cases into test scenarios |
| bulwark-fix-validator | Validating a fix | Test fix against boundary conditions |

**DO NOT use for:**
- Encrypted/compressed data (edge cases won't penetrate wrapping)
- Pure unit tests with fully mocked dependencies (edge cases need real execution)
- Performance/load testing (use dedicated load testing tools)

---

## Pre-Flight Gate (BLOCKING)

**STOP. Before providing ANY edge case data, you MUST follow the three-phase workflow.**

This skill provides **curated data** through a **deterministic workflow**. You must execute all phases.

### What You MUST Do

1. **Phase 1: Component Detection** - Identify component type and load context file
2. **Phase 2: Data Loading** - Load T0 + T1 data files (REQUIRED), T2 if specified by context
3. **Phase 3: Edge Case Application** - Apply edge cases and report what was loaded

### What You MUST NOT Do

- **Do NOT generate edge cases from your own knowledge** - use the curated data files
- **Do NOT skip loading context files** - they determine which categories apply
- **Do NOT skip the safety filter** - patterns marked `safe_for_automation: false` must be excluded
- **Do NOT return partial data** - all applicable tiers must be loaded

### Why This Matters

The curated data exists because:
- **Curation beats generation** - 50 well-chosen edge cases find more bugs than 10,000 random inputs
- **Reproducibility** - Same component type = same edge cases every time
- **Safety** - Destructive patterns are explicitly marked and filtered

**If you find yourself thinking "I know some good edge cases" - STOP. Use the data files.**

### Completion Checklist

Before returning to consumer, verify ALL items:

- [ ] Phase 1: Component type detected
- [ ] Phase 1: Context file loaded for component type
- [ ] Phase 2: T0 data files loaded (boundaries, booleans, collections)
- [ ] Phase 2: T1 data files loaded (unicode, special-chars, injection, special numbers)
- [ ] Phase 2: T2 data files loaded (if specified by context file)
- [ ] Phase 2: Safety filter applied (excluded manual_only and safe_for_automation: false)
- [ ] Phase 3: Edge cases applied to test/verification scenario
- [ ] Phase 3: Report includes categories loaded and patterns excluded

**Do NOT return to consumer until all checkboxes can be marked complete.**

---

## Dependencies

This skill provides data files and context guidance. Understanding what to load ensures deterministic execution.

| Category | Files | Requirement | When to Load |
|----------|-------|-------------|--------------|
| **Context files** | `context/{component-type}.md` | REQUIRED | Always load for detected component type |
| **T0 data (boundaries)** | `data/strings/boundaries.yaml`, `data/numbers/boundaries.yaml`, `data/booleans/boundaries.yaml`, `data/collections/arrays.yaml` | REQUIRED | Every edge case injection |
| **T1 data (common)** | `data/strings/unicode.yaml`, `data/strings/special-chars.yaml`, `data/strings/injection.yaml`, `data/numbers/special.yaml` | REQUIRED | Most edge case injections |
| **T2 data (context-specific)** | `data/dates/*.yaml`, `data/encoding/*.yaml`, `data/formats/*.yaml`, `data/concurrency/*.yaml` | CONDITIONALLY REQUIRED | If context file specifies → MUST load |
| **Language-specific** | `data/language-specific/{language}.yaml` | CONDITIONALLY REQUIRED | If testing language-specific behavior → MUST load |
| **External references** | `references/external-lists.md` | REQUIRED | For source attribution and update checking |

**Fallback behavior:**
- If component type detected → Loading `context/{type}.md` is REQUIRED
- If context file specifies a category → Loading that category is REQUIRED
- If a referenced file is missing → Note in output, continue with available data

---

## Data Tiers

| Tier | Categories | When to Load |
|------|------------|--------------|
| **T0 (Always)** | Boundaries (empty/single/max), Null handling | Every edge case injection |
| **T1 (Common)** | Basic injection, Unicode basics, Numeric edges | Every edge case injection |
| **T2 (Context)** | Date/time, Encoding, Formats, Concurrency | When context file specifies |
| **T3 (Manual)** | Patterns marked `manual_only: true` | NEVER for automated runs |

**Safety Filtering**: Patterns with `safe_for_automation: false` or `manual_only: true` MUST be excluded from automated test runs.

---

## Three-Phase Workflow

**CRITICAL**: All three phases are REQUIRED. Do not skip any phase.

```
Phase 1: Component Detection (Deterministic)
├── Identify component type from code under test
├── Map to context file: context/{cli-args|http-body|file-contents|db-query|process-spawn}.md
└── Load context file → get applicable categories list

Phase 2: Data Loading (Deterministic)
├── Load T0 data files (REQUIRED - always)
├── Load T1 data files (REQUIRED - always)
├── Load T2 data files specified by context file (CONDITIONALLY REQUIRED)
├── Load language-specific file if applicable (CONDITIONALLY REQUIRED)
└── Apply safety filter: exclude patterns with safe_for_automation: false

Phase 3: Edge Case Application
├── Inject loaded edge cases into test scenarios
├── Report which categories were loaded
└── Report any patterns excluded due to safety filtering
```

---

## Component Type Detection

Map code under test to component type. **Detection determines which context file to load.**

| Code Pattern | Component Type | Context File |
|--------------|----------------|--------------|
| CLI argument parsing, process.argv, argparse | CLI | `context/cli-args.md` |
| HTTP request/response, req.body, fetch, axios | HTTP | `context/http-body.md` |
| File I/O, fs.read, open(), file parsing | File | `context/file-contents.md` |
| Database queries, SQL, ORM operations | Database | `context/db-query.md` |
| Child process, spawn, exec, subprocess | Process | `context/process-spawn.md` |

**If multiple types apply**: Load context files for each applicable type.

---

## Category Reference

### Strings (T0/T1)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `strings/boundaries.yaml` | Empty, single char, long strings, whitespace | NullPointerException, buffer overflow, off-by-one |
| `strings/unicode.yaml` | Multi-byte, normalization, emoji, RTL | Encoding errors, length calculation bugs |
| `strings/special-chars.yaml` | Quotes, escapes, control characters | Escape sequence handling, delimiter confusion |
| `strings/injection.yaml` | SQL, XSS, command injection, path traversal | Security vulnerabilities |

### Numbers (T0/T1)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `numbers/boundaries.yaml` | 0, -1, 1, MAX_INT, MIN_INT | Integer overflow/underflow, off-by-one |
| `numbers/special.yaml` | NaN, Infinity, -0 | Special value handling, NaN propagation |
| `numbers/precision.yaml` | 0.1+0.2, large/small floats | Floating point comparison failures |

### Booleans (T0)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `booleans/boundaries.yaml` | true, false, null, truthy/falsy | Null reference, truthy/falsy confusion |

### Collections (T0)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `collections/arrays.yaml` | Empty, single, large, nested, sparse | Index out of bounds, empty collection crashes |
| `collections/objects.yaml` | Empty, nested, circular, prototype pollution | Null reference, prototype pollution |

### Dates (T2)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `dates/boundaries.yaml` | Epoch, Y2K38, leap year | Y2K38 overflow, leap year bugs |
| `dates/timezone.yaml` | DST transitions, UTC offsets | DST errors, timezone conversion |
| `dates/invalid.yaml` | Feb 30, invalid formats | Date parsing failures |

### Encoding (T2)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `encoding/charset.yaml` | ASCII, UTF-8, BOM | Encoding detection, mojibake |
| `encoding/normalization.yaml` | NFC, NFD, overlong | Normalization mismatches |

### Formats (T2)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `formats/email.yaml` | Valid/invalid patterns | Overly strict/lenient validation |
| `formats/url.yaml` | Valid/invalid patterns | URL parsing errors |
| `formats/json.yaml` | Valid/invalid patterns | JSON parsing errors |

### Concurrency (T2)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `concurrency/race-conditions.yaml` | Double submit, concurrent edit | Race conditions, lost updates |
| `concurrency/state-machines.yaml` | Invalid transitions | State corruption |

### Language-Specific (Conditional)

| File | Contents | Bugs Caught |
|------|----------|-------------|
| `language-specific/javascript.yaml` | == vs ===, truthy/falsy | Type coercion bugs |
| `language-specific/python.yaml` | None vs False, mutable defaults | Python-specific gotchas |
| `language-specific/rust.yaml` | Ownership, borrowing | Memory safety issues |

---

## Data File Format

All data files use this YAML structure:

```yaml
metadata:
  version: "1.0.0"
  last_updated: "2026-02-01"
  source_urls: []

category: strings
subcategory: boundaries
tier: T0

values:
  identifier:
    value: "actual value"
    bugs_caught: ["Bug type 1", "Bug type 2"]
    safe_for_automation: true
    manual_only: false
```

**Safety flags to check:**
- `safe_for_automation: false` → Exclude from automated runs
- `manual_only: true` → NEVER include in automated runs

---

## Integration Examples

### test-audit (Step 7)

```
1. Detect component type from test file
2. Load context file for component type
3. Load T0 + T1 data files
4. Load T2 files specified by context
5. Compare test coverage against loaded edge cases
6. Report missing edge case coverage
```

### bulwark-verify

```
1. Detect component type from code under verification
2. Load context file for component type
3. Load T0 + T1 data files
4. Load T2 files specified by context
5. Filter out patterns with safe_for_automation: false
6. Inject applicable edge cases into verification script
```

### bulwark-fix-validator

```
1. Detect component type from fix
2. Load context file for component type
3. Load T0 + T1 data files
4. Test fix against loaded edge cases
5. Report any edge cases that break the fix
```

