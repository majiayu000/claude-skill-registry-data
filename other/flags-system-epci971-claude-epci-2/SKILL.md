---
name: flags-system
description: >-
  Universal flags system for EPCI workflows. Defines flag categories (Thinking,
  Compression, Workflow, Wave), auto-activation rules, and precedence logic.
  Use when: evaluating complexity, displaying active flags, resolving conflicts.
  Not for: flag persistence or custom user flags (out of scope).
---

# EPCI Flags System

## Overview

The flags system provides fine-grained control over EPCI workflow behavior through
4 categories of flags that can be explicitly set or auto-activated.

## Flag Categories

### Thinking Flags

Control analysis depth and token budget.

| Flag | Budget | Trigger | Use Case |
|------|--------|---------|----------|
| `--think` | ~4K | 3-10 files | Multi-file analysis |
| `--think-hard` | ~10K | >10 files, refactor | System-wide analysis |
| `--ultrathink` | ~32K | Never auto | Critical decisions |

### Compression Flags

Manage output verbosity.

| Flag | Effect | Trigger |
|------|--------|---------|
| `--uc` | 30-50% reduction | context > 75% |
| `--verbose` | Full detail | Never auto |

### Workflow Flags

Control execution safety and hooks.

| Flag | Effect | Trigger |
|------|--------|---------|
| `--safe` | All validations | Sensitive files |
| `--no-hooks` | Disable hooks | Never auto |

### Wave Flags

Control multi-wave orchestration.

| Flag | Effect | Trigger |
|------|--------|---------|
| `--wave` | Enable waves | score > 0.7 |
| `--wave-strategy` | progressive/systematic | With --wave |

## Auto-Activation Logic

### Evaluation Order

```
1. Count impacted files
2. Detect refactoring/migration patterns
3. Check sensitive file patterns
4. Calculate context usage
5. Compute complexity score
6. Apply thresholds
```

### Thresholds

| Condition | Threshold | Flag |
|-----------|-----------|------|
| Files impacted | 3-10 | `--think` |
| Files impacted | >10 | `--think-hard` |
| Refactoring detected | true | `--think-hard` |
| Migration detected | true | `--think-hard` |
| Context usage | >75% | `--uc` |
| Sensitive patterns | any match | `--safe` |
| Complexity score | >0.7 | `--wave` |

### Sensitive File Patterns

```
**/auth/**
**/security/**
**/payment/**
**/password/**
**/api/v*/admin/**
**/credentials/**
**/secrets/**
```

### Complexity Score

```
score = (files × 0.3) + (LOC × 0.3) + (deps × 0.2) + (risk × 0.2)

Normalized to 0-1 scale:
- files: count / 20
- LOC: estimate / 2000
- deps: external_deps / 5
- risk: 0 (none), 0.33 (low), 0.66 (medium), 1 (high)
```

## Precedence Rules

### Resolution Order

1. Explicit flags override auto-activation
2. Safety flags take precedence over speed
3. Higher thinking levels win over lower
4. Explicit verbosity overrides auto-compression

### Conflict Matrix

| A | B | Result |
|---|---|--------|
| `--uc` | `--verbose` | B wins if explicit |
| `--think` | `--think-hard` | B wins |
| `--think-hard` | `--ultrathink` | B wins |
| `--wave` | `--safe` | Both (compatible) |
| `--no-hooks` | Any | Both (always compatible) |

### Conflict Error Format

```
ERROR: Flags {A} and {B} are incompatible.
       {A} enforces {effect_A}
       {B} enforces {effect_B}

       Choose one or omit both for default behavior.
```

## Flag Display Format

### Header Format

```
┌─────────────────────────────────────────────────────────────────────┐
│ 🚀 EPCI Workflow — {feature_name}                                   │
├─────────────────────────────────────────────────────────────────────┤
│ FLAGS: {flag1} ({source}) | {flag2} ({source}) | ...               │
└─────────────────────────────────────────────────────────────────────┘
```

### Source Indicators

- `(auto)` — Auto-activated by context
- `(explicit)` — User-specified
- `(alias)` — Expanded from alias (e.g., `--large`)

## Legacy Compatibility

### `--large` Alias

```
--large → --think-hard --wave
```

When `--large` is detected:
1. Expand to equivalent flags
2. Mark as `(alias)` in display
3. Process normally

## Integration Points

### Commands

| Command | Flag Support |
|---------|--------------|
| `/brief` | Evaluate and suggest flags |
| `/epci` | Full flag support, display in breakpoints |
| `/quick` | Limited (--uc, --no-hooks) |
| `/brainstorm` | Thinking flags, --no-security, --no-plan |

### Hooks

Flags are passed to hooks via `HookContext.active_flags`:

```json
{
  "phase": "phase-2",
  "active_flags": ["--think-hard", "--safe"],
  "flag_sources": {
    "--think-hard": "auto",
    "--safe": "explicit"
  }
}
```

## Best Practices

1. **Let auto-activation work** — Only override when necessary
2. **Prefer explicit for critical** — Use `--ultrathink` explicitly
3. **Combine safely** — Check compatibility before combining
4. **Document choices** — Note flag rationale in Feature Document
