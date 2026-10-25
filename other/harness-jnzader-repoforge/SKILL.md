---
name: extend-harness-module
description: >
  Add parent directory to path when running eval scripts directly.
  Trigger: when executing eval/harness.py as main script.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# extend-harness-module

Add parent directory to path when running eval scripts directly.

**Trigger**: executing eval/harness.py as main script or importing from repoforge/cli.py
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Add parent to sys.path | `sys.path.insert(0, '..')` |
| Run eval harness | `python -m eval.harness` |
| Execute scenario | `python -m eval.harness run_scenario --scenario model --verbose` |

## Critical Patterns (Summary)
- **Add parent to path**: Insert `'..'` into `sys.path` before importing harness modules when running scripts directly
- **Use run_scenario**: Call `run_scenario()` with scenario name to execute evaluation with optional LLM and verbose output
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Add parent to path

When running `eval/harness.py` directly, the module's parent directory must be added to `sys.path` to resolve sibling imports. This pattern uses `pathlib.Path` to dynamically resolve the project root and insert it into the path, ensuring all harness exports (`make_fastapi_crud_module`, `score_trigger_precision`, etc.) are accessible.

```python
import sys
from pathlib import Path

# Add parent directory to path for direct script execution
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Now imports from the module work
from eval.harness import make_fastapi_crud_module, run_scenario
```

### Use run_scenario to execute evaluations

The `run_scenario` function orchestrates a single evaluation run with optional LLM integration. It accepts a scenario name, optional LLM instance, verbose flag, and facts dictionary. The function returns an `EvalResult` containing scores for trigger precision, code concreteness, pattern detection, and multilang coverage, enabling automated evaluation of LLM outputs against expected module patterns.

```python
from eval.harness import run_scenario

result = run_scenario(
    scenario_name="model",
    verbose=True,
    facts=["extracted_fact_1", "extracted_fact_2"]
)
print(f"Trigger precision: {result.score_trigger_precision}")
print(f"Code concreteness: {result.score_code_concreteness}")
```

## When to Use

- Running `eval/harness.py` directly from any working directory
- Executing scenario-based evaluations with `python -m eval.harness`
- Importing harness functions from repoforge/cli.py or other modules
- Debugging module score outputs (`score_trigger_precision`, `score_code_concreteness`)

## Commands

```bash
# Run the harness with a specific scenario
python -m eval.harness run_scenario --scenario model --verbose

# Run all scenarios
python -m eval.harness run_all

# Execute from project root with parent path auto-resolved
python -m eval.harness --scenario auth --facts '["key=value"]'
```

## Anti-Patterns

### Don't: Skip sys.path modification when running directly

<Why it's wrong: Without adding the parent directory to `sys.path`, Python cannot resolve imports like `from eval.harness import ...`, raising `ModuleNotFoundError: No module named 'eval'. This breaks all harness functionality when running scripts outside the project package context.>

```python
# BAD: Running without path setup
import sys
# Missing: sys.path.insert(0, '..')
from eval.harness import run_scenario  # ModuleNotFoundError
```
<!-- L3:END -->