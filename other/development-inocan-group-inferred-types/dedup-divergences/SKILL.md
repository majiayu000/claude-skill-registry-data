---
name: dedup-divergences
description: Batch analysis of hundreds of fuzzer divergences using parallel subagents - categorize, deduplicate, identify unique bugs, create summary reports
compatibility: opencode
metadata:
  domain: fuzzing
  workflow: batch-analysis
---

# Dedup Divergences Skill

## Overview
Analyze hundreds of fuzzer divergences, identify unique root causes, and create a summary report. Divergences are stored in `reports/YYYY-MM-DD/` directories.

## Prerequisites
```bash
source venv/bin/activate
```

## Divergence Structure
See `src/fuzzer/divergence_detector.py` for divergence types:
- `DivergenceType.DEPLOYMENT` - Contract deployment differs
- `DivergenceType.EXECUTION` - Function call result differs  
- `DivergenceType.XFAIL` - Expected failure didn't occur

## Workflow

### Step 1: List Divergences
```bash
ls reports/2025-12-28/*.json | wc -l  # Count divergences
```

### Step 2: Replay to Confirm
```bash
PYTHONPATH=src python -m fuzzer.replay_divergence reports/2025-12-28/divergence_001.json
```

### Step 3: Categorize by Root Cause
Bugs can be in:
- **Ivy** (`src/ivy/`) - AST interpreter bug
- **Vyper** (`venv/.../vyper/`) - Compiler codegen bug
- **Boa** (`venv/.../boa/`) - Execution framework bug

### Step 4: Create Summary Report
Create `MM_DD_minute_divergence_summary.md` with format:

```markdown
# Divergence Summary - YYYY-MM-DD

## Summary
- Total divergences: N
- Unique bugs: M
- Ivy bugs: X
- Vyper bugs: Y
- Boa bugs: Z

# path/to/divergence_001.json

## Root Cause
[Explanation of the bug]

## Location
- Component: ivy|vyper|boa
- File: path/to/file.py
- Function: function_name

## Suggested Fix
[How to fix the bug]

## Test to Confirm
```python
def test_divergence_001(get_contract):
    src = """..."""
    c = get_contract(src)
    assert c.foo() == expected
```

# path/to/divergence_002.json
...
```

## Parallel Analysis Strategy

### Phase 1: Quick Categorization Pass
Before spawning subagents, do a quick pass to categorize divergences by "fingerprint":
- Error type (revert, wrong output, storage mismatch)
- Function involved
- Storage pattern
- Source code patterns

This identifies clusters of likely-duplicate divergences.

### Phase 2: Filter Known Issues
Skip divergences matching these known patterns (group under "Known Issues" in report):
- **staticcall violation** - Static call mutability issues
- **venom StackTooDeep** - Venom pipeline stack depth errors
- **tuple with String storage** - Tuple containing String in storage
- **Bytes/String mapping keys** - HashMap with Bytes/String keys
- **struct field offsets** - Struct field offset calculation bugs

### Phase 3: Spawn Subagents
- **Process ALL divergences** (don't sample)
- Spawn **at least 10 subagents** for maximum parallelism

### Subagent Instructions
Pass to each subagent:
1. Batch of divergence file paths
2. Known issues list (to skip/categorize)
3. All relevant context (key files, replay command, skills)
4. **Output format requirement**: Structured markdown matching report format
5. **Test requirement**: Each subagent creates their own test file

### Subagent Response Format
Each subagent returns structured `.md`:
```markdown
# Batch Analysis Report

## Skipped (Known Issues)
- path/to/div1.json - staticcall violation
- path/to/div2.json - venom StackTooDeep

## Unique Divergences

### path/to/div3.json
**Root Cause**: [explanation]
**Component**: ivy|vyper|boa
**File**: path/to/file.py
**Suggested Fix**: [fix]
**Test File**: tests/test_batch_N_divergences.py

### path/to/div4.json
...
```

### Phase 4: Aggregation
Main agent:
1. Collects all subagent reports
2. Groups by root cause (deduplicates across batches)
3. Merges tests into appropriate files
4. Creates final summary with unique bugs only

## Key Files
- `src/fuzzer/divergence_detector.py` - Divergence detection logic
- `src/fuzzer/replay_divergence.py` - Replay utility
- `src/fuzzer/trace_types.py` - Trace data structures
- `trace-format.json` - Export schema

## Related Skills
- **replay** - How to replay and debug divergences
- **boa** - Understanding Boa execution
- **vyper** - Understanding Vyper compiler

## Deduplication Heuristics
Group divergences by:
1. Same source code pattern (e.g., all `slice()` bugs)
2. Same error message/type
3. Same function being called
4. Same Ivy code path (same visitor method)

## Output Requirements
1. Each unique bug gets one top-level heading: `# path/to/divergence`
2. Include explanation and suggested fix
3. Write pytest tests to confirm analysis
4. If multiple divergences have same root cause, list them together
