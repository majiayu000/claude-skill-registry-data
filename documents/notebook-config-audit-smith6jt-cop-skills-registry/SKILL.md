---
name: notebook-config-audit
description: "Audit Jupyter notebooks for hardcoded values that contradict configuration cells. Trigger when: (1) notebook behavior differs from documented settings, (2) updating notebook version, (3) finding inconsistent values across cells."
author: Claude Code
date: 2024-12-31
---

# Notebook Configuration Audit Pattern

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-31 |
| **Goal** | Find and fix hardcoded values in notebooks that contradict configuration |
| **Environment** | Jupyter notebooks with configuration cells |
| **Status** | Success |

## Context

**Problem**: Training notebooks often have configuration cells at the top (e.g., `LOOKBACK_DAYS = 1460`), but later cells may have hardcoded values that contradict these settings (e.g., `lookback_days=365`).

**Symptoms**:
- Notebook behavior doesn't match documented configuration
- Different cells use different values for the same setting
- Comments say one thing, code does another

## Verified Audit Workflow

### Step 1: Extract All Notebook Cells

```python
import json
with open('notebooks/training.ipynb') as f:
    nb = json.load(f)

# Search for specific patterns
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if 'lookback' in src.lower():
        print(f'Cell {i}: {src[:200]}...')
```

### Step 2: Search for Key Configuration Patterns

Common patterns to audit:

```python
patterns = [
    # Lookback/timeframe settings
    'lookback', 'LOOKBACK', 'days=', 'years',
    '365', '252', '1460', '1000',
    'timeframe', 'TIMEFRAME', '1Hour', '1Day', '1Min',

    # Slippage/cost settings
    'slippage', 'cost', '0.001', '0.002', '0.0025',

    # Version references
    'v2.', 'v3.',

    # Multi-asset settings
    'crypto', 'equity', 'enabled'
]

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    for pattern in patterns:
        if pattern.lower() in src.lower():
            # Check if it's a hardcoded value vs config reference
            lines = src.split('\n')
            for j, line in enumerate(lines):
                if pattern.lower() in line.lower() and '=' in line:
                    if not line.strip().startswith('#'):
                        print(f'Cell {i}, Line {j}: {line.strip()[:100]}')
```

### Step 3: Cross-Reference Configuration Definitions

Find where config values are defined vs used:

```python
# Find definitions (cell with CONFIG_NAME = value)
definitions = {}
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if 'LOOKBACK_DAYS =' in src or 'TIMEFRAME =' in src:
        definitions[i] = src

# Find usages (cells using config or hardcoded values)
usages = {}
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if 'lookback_days=' in src:  # lowercase = function parameter
        usages[i] = src
```

### Step 4: Fix Inconsistencies

Replace hardcoded values with config references:

```python
# Fix: lookback_days=365 -> lookback_days=LOOKBACK_DAYS
cell_src = nb['cells'][17]['source']
fixed = []
for line in cell_src:
    if 'lookback_days=365,' in line:
        line = line.replace('lookback_days=365,', 'lookback_days=LOOKBACK_DAYS,')
    fixed.append(line)
nb['cells'][17]['source'] = fixed

# Save
with open('notebooks/training.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
```

## Common Issues Found

| Issue | Example | Fix |
|-------|---------|-----|
| **Hardcoded lookback** | `lookback_days=365` | Use `LOOKBACK_DAYS` constant |
| **Wrong comment** | `"(2 years)"` when config is 4 years | Update comment to match |
| **Stale print statement** | `print(f'value=0.002')` when actual is 0.0025 | Update print to match code |
| **Version mismatch** | Comment says v2.5 but using v2.7 settings | Update version references |

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Manual cell-by-cell review | Too slow, missed issues | Use automated pattern search |
| Only check config cells | Missed hardcoded values in later cells | Search ALL cells |
| Trust comments | Comments were outdated | Verify comments match code |
| Fix without testing | Broke other functionality | Always run tests after fixes |

## Verification Checklist

After fixing, verify:

```python
# 1. Check config definitions
print(f'LOOKBACK_DAYS = {LOOKBACK_DAYS}')  # Should be 1460

# 2. Check all usages reference config
# Search for hardcoded values that should use config:
grep -n "lookback_days=[0-9]" notebooks/training.ipynb

# 3. Check comments match config
# Search for year references:
grep -n "years" notebooks/training.ipynb

# 4. Run notebook smoke test
python -c "exec(open('notebooks/training.ipynb').read())"
```

## Automation Script

Save this as `scripts/audit_notebook_config.py`:

```python
#!/usr/bin/env python
"""Audit notebook for configuration inconsistencies."""
import json
import sys

def audit_notebook(path: str) -> list:
    """Find potential configuration issues in notebook."""
    issues = []

    with open(path) as f:
        nb = json.load(f)

    # Known config patterns to check
    checks = [
        ('lookback_days=365', 'Should use LOOKBACK_DAYS'),
        ('lookback_days=252', 'Should use LOOKBACK_DAYS'),
        ('(2 years)', 'Should say (4 years) if LOOKBACK_DAYS=1460'),
        ('slippage_cost_crypto=0.002', 'Should be 0.0025 per Alpaca fees'),
    ]

    for i, cell in enumerate(nb['cells']):
        src = ''.join(cell.get('source', []))
        for pattern, message in checks:
            if pattern in src:
                issues.append(f'Cell {i}: {message} (found: {pattern})')

    return issues

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'notebooks/training.ipynb'
    issues = audit_notebook(path)
    if issues:
        print('Configuration Issues Found:')
        for issue in issues:
            print(f'  - {issue}')
        sys.exit(1)
    else:
        print('No configuration issues found.')
```

## Related Skills

- `private-function-shim-export`: Related shim/import issues
- `codebase-consolidation-pattern`: Module organization patterns

## References

- Commit `160ebff`: Fixes for training.ipynb hardcoded values
- Cell 12: Configuration definitions (LOOKBACK_DAYS, TIMEFRAME)
- Cell 17: Symbol selection (was using hardcoded 365)
- Cell 30: Data loading (comment said 2 years)
- Cell 33: Training loop (print statement had wrong slippage)
