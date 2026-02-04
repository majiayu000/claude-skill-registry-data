---
name: testing-requirements
description: Use when writing tests - test structure, mocking patterns, pre-commit checks
---

# Testing Requirements

Use this skill when writing tests for features or fixing bugs.

## Checklist

### Test Structure
- [ ] Mirror `app/` structure in `tests/` directory
- [ ] Place test files in matching directory (e.g., `app/features/generators/service.py` → `tests/app/features/generators/test_service.py`)
- [ ] Use `test_` prefix for all test files and test functions

### Testing Patterns
- [ ] Use `pytest.mark.asyncio` decorator for async tests
- [ ] Mock external dependencies (database, GPU, network, file I/O)
- [ ] Use fixtures for common test setup
- [ ] Avoid test interdependencies (each test should be independent)

### Coverage Requirements
Cover all three paths:
- [ ] **Happy path** - Normal execution with valid inputs
- [ ] **Error cases** - Known failure conditions (invalid input, missing resources)
- [ ] **Edge cases** - Boundary conditions, empty values, None handling

### Example Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from app.features.generators.service import GeneratorService

@pytest.mark.asyncio
async def test_generate_image_success():
    """Test successful image generation (happy path)."""
    mock_db = Mock()
    config = GenerateConfig(prompt="test", model_id=1)

    with patch('app.cores.model_manager.load_model'):
        result = await GeneratorService.generate(config, mock_db)
        assert result.success is True

@pytest.mark.asyncio
async def test_generate_image_invalid_model():
    """Test error handling for invalid model (error case)."""
    mock_db = Mock()
    config = GenerateConfig(prompt="test", model_id=999)

    with pytest.raises(ValueError, match="Model not found"):
        await GeneratorService.generate(config, mock_db)

@pytest.mark.asyncio
async def test_generate_image_empty_prompt():
    """Test handling of empty prompt (edge case)."""
    mock_db = Mock()
    config = GenerateConfig(prompt="", model_id=1)

    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        await GeneratorService.generate(config, mock_db)
```

### Pre-Commit Checks
Before marking work complete, run all checks:
- [ ] Type check modified files: `uv run ty check app/path/to/modified.py tests/path/to/test.py`
- [ ] Lint and fix: `uv run ruff check --fix app/ tests/`
- [ ] Format code: `uv run ruff format app/ tests/`
- [ ] Run tests: `uv run pytest -q`
- [ ] Verify all checks pass (pre-commit hook will block commits if they fail)

### Quality Gates
- [ ] All tests pass
- [ ] No type errors (ty clean)
- [ ] No lint errors (ruff clean)
- [ ] Code is formatted (ruff format applied)
- [ ] Test coverage includes happy path, error cases, and edge cases

## Reference

- **Testing framework:** pytest + pytest-asyncio
- **Pre-commit hook:** Runs ruff format, ruff check, ty check on staged files
- **Coverage goal:** 80%+ (SonarQube quality gate)
