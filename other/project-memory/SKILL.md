---
name: epci:project-memory
description: >-
  Maintains project context, history, and learnings across sessions.
  Provides persistent memory for patterns, preferences, velocity metrics, and past decisions.
  Use when: recalling past implementations, applying project conventions,
  calibrating estimates, detecting code patterns, or accessing user preferences.
  Internal component for EPCI v6.0.
user-invocable: false
allowed-tools: Read, Write, Glob
---

# Project Memory

Internal component for project context and history across sessions.

## Overview

Persistent memory for:
- **Patterns** — Detected code patterns (API style, naming, tests, error handling)
- **Preferences** — User workflow and technical preferences
- **Velocity** — Estimation accuracy calibration per complexity level
- **Bugs** — Past bug fixes with root causes and solutions
- **Features** — Completed feature history with decisions and learnings

## Storage Structure

```
.claude/state/memory/
├── patterns.json         # Detected code patterns
├── preferences.json      # User workflow and technical preferences
├── velocity.json         # Estimation calibration by complexity
├── bugs.json            # Bug fix history
└── features/
    └── {slug}.json      # Completed feature history
```

> **Note:** Aligned with state-manager (`.claude/state/`). Memory is a sibling to `features/` and `sessions/`.

## API

### Core Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `init(project_root)` | Initialize/load memory for project | path: string | MemoryInstance |
| `get_patterns()` | Get detected code patterns | — | PatternsObject |
| `get_preferences()` | Get user preferences | — | PreferencesObject |
| `get_velocity()` | Get velocity calibration metrics | — | VelocityObject |

### Recall Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `recall(query)` | Search across all memory (features, bugs, patterns) | query: string | RelevantMemory[] |
| `recall_features(keywords)` | Find similar past features | keywords: string[] | FeatureMemory[] |
| `recall_bugs(keywords)` | Find similar past bugs | keywords: string[] | BugMemory[] |

### Store Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `store_feature(data)` | Save completed feature to history | FeatureData | void |
| `store_bug(data)` | Save bug resolution | BugData | void |
| `update_velocity(data)` | Update velocity calibration | VelocityUpdate | void |
| `update_preference(key, value)` | Learn/update a preference | key, value, confidence | void |

### Pattern Functions

| Function | Description | Input | Output |
|----------|-------------|-------|--------|
| `scan_patterns()` | Detect codebase patterns | — | PatternsObject |
| `is_pattern_stale()` | Check if rescan needed (>7 days) | — | boolean |

## Memory Types

| Type | File | Contents | Example |
|------|------|----------|---------|
| `patterns` | `patterns.json` | Code patterns detected | API style: REST, naming: camelCase |
| `preferences` | `preferences.json` | User workflow/tech preferences | TDD: guided, framework: vitest |
| `velocity` | `velocity.json` | Estimation calibration | SMALL avg: 1.5h, accuracy: 0.89 |
| `bugs` | `bugs.json` | Past bugs and fixes | OAuth redirect issue |
| `features` | `features/{slug}.json` | Completed feature history | auth-oauth implementation |

## Usage

### Initialization

```
memory = project_memory.init("/path/to/project")
# Loads or creates .claude/state/memory/ structure
```

### Pattern Detection

```
patterns = memory.get_patterns()
# Returns: { api_style: { type: "REST", confidence: 0.95 }, ... }

if memory.is_pattern_stale():
    memory.scan_patterns()
```

### Recall Similar Work

```
# Find similar features
similar = memory.recall_features(["authentication", "oauth"])
# Returns: [{ slug: "auth-basic", duration_minutes: 120, decisions: [...] }]

# Find similar bugs
bugs = memory.recall_bugs(["redirect", "callback"])
# Returns: [{ id: "oauth-redirect-fix", root_cause: "...", fix_summary: "..." }]
```

### Store Completed Work

```
# After completing a feature
memory.store_feature({
    slug: "auth-oauth-google",
    summary: "OAuth2 authentication with Google provider",
    complexity: "STANDARD",
    duration_minutes: 195,
    estimated_minutes: 180,
    keywords: ["auth", "oauth", "google"],
    files_modified: ["src/auth/oauth.ts", "src/auth/types.ts"],
    test_count: 12,
    decisions: [{ question: "Token storage?", choice: "httpOnly cookies", reasoning: "Security" }],
    learnings: ["Google requires verified redirect URIs"]
})

# After fixing a bug
memory.store_bug({
    id: "oauth-redirect-fix",
    description: "OAuth callback fails on production",
    root_cause: "Redirect URI mismatch between env configs",
    fix_summary: "Unified OAUTH_REDIRECT_URI across environments",
    keywords: ["oauth", "redirect", "callback", "production"],
    category: "integration"
})
```

### Velocity Tracking

```
# Update after completing work
memory.update_velocity({
    complexity: "STANDARD",
    estimated_minutes: 180,
    actual_minutes: 195
})

# Get calibration for estimates
velocity = memory.get_velocity()
# Returns: { STANDARD: { adjustment_factor: 1.08, accuracy: 0.92 } }
```

### Preference Learning

```
# Track user choice
memory.update_preference("tdd_preference", "guided", 0.85)
memory.update_preference("test_framework", "vitest", 0.95)

# Get preferences
prefs = memory.get_preferences()
# Returns: { workflow: { tdd_preference: { value: "guided", confidence: 0.85 } }, ... }
```

## Integration Points

| Skill | When | Actions |
|-------|------|---------|
| `/implement` step-00 | Init | `init()`, `get_patterns()`, `recall_features()` |
| `/implement` step-07 | Fin | `store_feature()`, `update_velocity()` |
| `/quick` | Init | `init()`, `get_patterns()` |
| `/quick` MEMORY | Fin | `update_velocity()`, optionally `store_feature()` |
| `/brainstorm` | Init | `get_preferences()`, `recall_features()` |
| `/debug` | Init | `recall_bugs()` |
| `/debug` | Fin | `store_bug()` |

## Pattern Detection

Automatically detects and stores:

| Pattern | Detection Method | Example Value |
|---------|------------------|---------------|
| `api_style` | Analyze endpoints, routes | REST, GraphQL |
| `error_handling` | Grep error patterns | try-catch, result-type |
| `naming.files` | File name analysis | kebab-case, camelCase |
| `naming.functions` | AST/grep analysis | camelCase, snake_case |
| `tests.framework` | Package analysis | vitest, jest, pytest |
| `tests.location` | File structure | tests/, __tests__/, *.spec.ts |
| `components.framework` | Package/imports | react, vue, svelte |
| `components.styling` | Config/imports | tailwind, css-modules, styled |

## Preference Learning

Tracks user choices with confidence scores:

| Category | Preferences |
|----------|-------------|
| **Workflow** | tdd_preference, breakpoint_frequency, verbosity |
| **Technical** | test_framework, css_approach, api_style |

Confidence increases with repeated observations:
- 1 observation: 0.5
- 3 observations: 0.75
- 5+ observations: 0.9+

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `MEMORY_NOT_INITIALIZED` | `init()` not called | Call `init(project_root)` first |
| `FILE_CORRUPTED` | JSON parse error | Backup corrupt file, create fresh |
| `PATTERN_SCAN_FAILED` | Access/parse issues | Log warning, return cached |
| `STORAGE_FULL` | Too many features | Archive old features (>6 months) |

## Reference Files

- [storage-format.md](references/storage-format.md) — Complete JSON schemas
- [migration-guide.md](references/migration-guide.md) — v5 to v6 migration

## Limitations

This component does NOT:
- Sync across machines (local file-based)
- Store sensitive credentials or secrets
- Replace version control history
- Provide real-time updates
- Share context between projects
