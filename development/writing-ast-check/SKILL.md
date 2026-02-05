---
name: writing-ast-check
description: Create AST-based checks for evaluating generated Python code quality
---

# Writing AST-Based Checks for Evals

This process documents how to create robust, AST-based checks for evaluating the quality of AI-generated Python code.

## Process

### 1. Define the Check Criteria

Clearly specify what you're checking for:

**Example:** We want to ensure generated code uses modern Python union syntax (`str | None`) instead of legacy `Optional[str]` from the typing module.

**Acceptance criteria:**
- ✅ Files using `| None` syntax
- ✅ Files with no optional types at all
- ❌ Files using `Optional[T]` syntax

### 2. Add the check function to the AST Helper Module

Create a dedicated function in AST helpers: `evals/<eval_name>/ast_helpers.py`

### 3. Add Check to EvalResult

Update `evals/<eval_name>/checks.py`:

```python
class EvalResult:
    # Used the writing-services skill
    used_service_skill = Check(default=False, passed=True)

    # Used | None instead of Optional
    used_none_instead_of_optional = Check(default=False, passed=True)

    def to_dict(self) -> dict:
        """Convert eval results to a dictionary for logging."""
        return {
            "used_service_skill": self.used_service_skill.did_pass(),
            "used_none_instead_of_optional": self.used_none_instead_of_optional.did_pass(),
        }
```

### 4. Integrate Check in Eval

Update `__main__.py` to run the check after the agent completes:

```python
from .ast_helpers import check_uses_union_none_syntax

async def main(gym_project_directory: Path) -> None:
    # ... agent execution code ...

    # Check if the generated logger.py uses | None instead of Optional
    logger_file_path = gym_project_directory / "jack-software/evals/logger.py"
    if check_uses_union_none_syntax(logger_file_path):
        eval_result.used_none_instead_of_optional.mark(True)

    # ... logging code ...
```

### 5. Write Comprehensive Tests

Add a class to the `test_ast_helpers.py` with test cases.

## Testing Your Check

Run the tests:
```bash
make test-services-eval
```


