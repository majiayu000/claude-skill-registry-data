---
name: replay
description: Replay fuzzer divergences to reproduce bugs, find root cause by comparing Ivy AST interpreter vs Boa bytecode execution
compatibility: opencode
metadata:
  domain: fuzzing
  workflow: debugging
---

# Replay Divergence Skill

## Overview
A **divergence** occurs when Ivy's AST interpreter produces a different result than Boa's bytecode execution for the same Vyper code. Divergences indicate bugs in either:
- **Ivy** (AST interpreter bug)
- **Vyper compiler** (codegen bug - bytecode doesn't match source semantics)
- **Boa/py-evm** (rare execution bug)

## Replaying Divergences
Use `src/fuzzer/replay_divergence.py` to reproduce a divergence:

```bash
source venv/bin/activate
PYTHONPATH=src python -m fuzzer.replay_divergence path/to/divergence.json
```

Exit codes:
- `0`: Divergence reproduced
- `1`: No divergence (Ivy and Boa now match)
- `2`: Usage error

## Divergence JSON Structure
See `trace-format.json` for full schema. Key fields:
```json
{
  "type": "deployment|execution|xfail",
  "step": 0,
  "divergent_runner": "boa:default",
  "ivy_call": {"success": true, "output": "0x..."},
  "boa_call": {"success": false, "error": "..."},
  "traces": [...]
}
```

## Finding Root Cause

### Step 1: Reproduce
```bash
PYTHONPATH=src python -m fuzzer.replay_divergence path/to/divergence.json
```

### Step 2: Extract Source Code
The divergence JSON contains `source_code` in the deployment trace. Extract it to understand what code is being tested.

### Step 3: Isolate the Bug
Create a minimal test case:
```python
def test_divergence_minimal(get_contract):
    src = """
    # Extracted/minimized source from divergence
    @external
    def foo() -> uint256:
        return 42
    """
    c = get_contract(src)
    # Test the specific behavior that diverges
    assert c.foo() == 42
```

### Step 4: Compare Ivy vs Boa
```python
# Test with Ivy (via get_contract fixture)
from ivy.frontend.loader import loads
ivy_contract = loads(src)
ivy_result = ivy_contract.foo()

# Test with Boa directly
import boa
boa_contract = boa.loads(src)
boa_result = boa_contract.foo()

print(f"Ivy: {ivy_result}, Boa: {boa_result}")
```

### Step 5: Determine Bug Location
- **If Ivy is wrong**: Fix in `src/ivy/` (interpreter bug)
- **If Boa is wrong**: Likely Vyper compiler bug (report to Vyper team)
- **If both differ from spec**: Check EVM semantics

## Related Skills
- Use **boa** skill to understand Boa's execution model
- Use **vyper** skill to inspect compiler internals
- Both boa and vyper source are in `venv/` for inspection

## Debugging Tips
1. Add debug prints in Ivy's visitor methods (`src/ivy/stmt.py`, `src/ivy/expr/expr.py`)
2. Compare storage dumps between Ivy and Boa
3. Check if the divergence is in deployment vs execution phase
4. Look for edge cases: overflow, empty arrays, default values
