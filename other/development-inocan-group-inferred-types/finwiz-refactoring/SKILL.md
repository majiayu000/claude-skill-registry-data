---
name: finwiz-refactoring
description: "Patterns for refactoring large files and reorganizing code in FinWiz while maintaining backward compatibility and test integrity. Use when splitting large files, moving code between modules, or reorganizing project structure."
allowed-tools: ["Read", "Edit", "Bash"]
---

# FinWiz Refactoring Patterns

Guidelines for refactoring large files and reorganizing code while maintaining backward compatibility and test integrity.

## File Organization Principles

### Schema Models Location

- **Rule**: All Pydantic models belong in `src/finwiz/schemas/`
- **Pattern**: Domain-specific subfolders mirror domain folders
  - `schemas/quantitative/` for quantitative models
  - `schemas/rebalancing/` for rebalancing models  
  - `schemas/tools/` for tool input/output models
- **Rationale**: Centralizes all data contracts for easy discovery and maintenance

### Business Logic Location

- **Rule**: Business logic stays in domain-specific folders
  - `quantitative/` for quantitative analysis logic
  - `tools/` for tool implementations
  - `orchestrators/` for orchestration logic
- **Rationale**: Keeps logic close to where it's used

### Helper/Utility Location

- **Rule**: Validators, defaults, and helpers stay with their domain
  - `quantitative/config_validators.py` for config validators
  - `quantitative/config_defaults.py` for default values
- **Rationale**: Keeps related code together for easier maintenance

## File Size Guidelines

### Size Limits

- **Hard limit**: 300 lines per file (MUST split)
- **Should split**: 250+ lines per file
- **Consider splitting**: 200+ lines per file
- **Ideal target**: 150-200 lines per file
- **Minimum**: 50 lines (avoid creating tiny files)

### Split Strategy

1. **Identify logical components** within the large file
2. **Extract to separate files** with single responsibility
3. **Create thin re-export layer** for backward compatibility
4. **Ensure no "monster classes"** (multiple responsibilities)

## Refactoring Process

### Pre-Refactoring Checklist

Before splitting any large file:

- [ ] **Identify patterns**: Check similar components in codebase
- [ ] **Plan structure**: Sketch out new file organization
- [ ] **Check schemas**: Do Pydantic models need to move to `schemas/`?
- [ ] **Size validation**: Ensure no file will exceed 300 lines
- [ ] **Test planning**: Identify which tests need updating
- [ ] **Backward compat**: Plan re-export layer if needed

### Execution Steps

1. **Create new files** with extracted components
2. **Move code** to appropriate locations
3. **Create re-export layer** in original location
4. **Update test imports** and mock paths
5. **Verify all tests pass**
6. **Update documentation** if needed

### Post-Refactoring Verification

- [ ] All existing tests still pass
- [ ] No new test failures introduced
- [ ] Mock paths updated to correct modules
- [ ] Backward compatibility maintained
- [ ] Re-export layer tested

## Test Maintenance During Refactoring

### Critical Rules

- **Never leave failing tests** after refactoring
- **Update test imports** when moving code
- **Fix mock paths** to point to actual import locations
- **Verify all tests pass** before marking task complete

### Mock Path Rules

Mock at the **source of import**, not the re-export:

```python
# If code imports from config_manager
from finwiz.quantitative.config_manager import get_config

# Mock at the import location
mocker.patch("finwiz.quantitative.config_manager.get_config")

# NOT at the re-export location
# mocker.patch("finwiz.quantitative.config.get_config")  # WRONG
```

## Backward Compatibility

### Re-export Pattern

```python
# Original location: src/finwiz/quantitative/config.py (670 lines)
# After refactoring:

# src/finwiz/schemas/quantitative/config_models.py (270 lines)
class BacktestConfig(BaseModel):
    # Pydantic models moved to schemas/

# src/finwiz/quantitative/config_manager.py (230 lines)  
class QuantitativeConfigManager:
    # Business logic stays in domain folder

# src/finwiz/quantitative/config.py (62 lines) - Re-export layer
from finwiz.schemas.quantitative.config_models import (
    BacktestConfig,
    QuantConfig,
    ScreenerConfig,
)
from finwiz.quantitative.config_manager import (
    QuantitativeConfigManager,
    get_backtest_config,
    get_quant_config,
)

__all__ = [
    "BacktestConfig",
    "QuantConfig", 
    "ScreenerConfig",
    "QuantitativeConfigManager",
    "get_backtest_config",
    "get_quant_config",
]
```

### Benefits of Re-export Layer

- **Existing code** importing from old location still works
- **No breaking changes** for consumers
- **Gradual migration** path for large codebases
- **Backward compatibility** maintained

## Example: Correct Refactoring

### Before: Monolithic File

```
src/finwiz/quantitative/config.py (670 lines)
├── Pydantic models (270 lines)
├── Manager class (230 lines)
├── Helper functions (100 lines)
└── Constants and enums (70 lines)
```

### After: Focused Files

```
src/finwiz/
├── schemas/quantitative/
│   └── config_models.py (270 lines) ← Pydantic models
├── quantitative/
│   ├── config.py (62 lines) ← Re-exports for backward compat
│   ├── config_manager.py (230 lines) ← Manager logic
│   ├── config_defaults.py (173 lines) ← Enums & defaults
│   ├── config_validators.py (66 lines) ← Validators
│   └── config_builders.py (32 lines) ← Backward compat helpers
```

**Result**: 6 focused files, all <300 lines, tests passing ✅

## Common Mistakes to Avoid

### ❌ Don't

- Create Pydantic models in domain folders (they belong in `schemas/`)
- Leave failing tests after refactoring
- Create files without checking existing patterns
- Forget to update test mock paths
- Create "monster classes" (>300 lines)
- Skip backward compatibility layer

### ✅ Do

- Follow existing codebase patterns
- Verify all tests pass before marking complete
- Create thin re-export layers for backward compatibility
- Update test imports and mock paths
- Keep files focused and under 300 lines
- Document lessons learned for future reference

## Refactoring Workflow

### Step-by-Step Process

1. **Analyze current file** structure and dependencies
2. **Plan new structure** following FinWiz patterns
3. **Create new files** with extracted components
4. **Move code** to appropriate locations
5. **Create re-export layer** in original location
6. **Update all test imports** and mock paths
7. **Run full test suite** to verify nothing breaks
8. **Update documentation** if needed
9. **Commit changes** with descriptive message

### Testing During Refactoring

```bash
# Run tests frequently during refactoring
make test

# Check specific test files that might be affected
uv run pytest tests/unit/quantitative/ -v

# Verify mock paths are correct
uv run pytest tests/unit/quantitative/test_config.py -v -s
```

## Quality Assurance

### Refactoring Checklist

- [ ] **File sizes**: All files <300 lines
- [ ] **Single responsibility**: Each file has clear purpose
- [ ] **Backward compatibility**: Re-export layer works
- [ ] **Tests pass**: All existing tests still work
- [ ] **Mock paths**: Updated to correct import locations
- [ ] **Documentation**: Updated if needed
- [ ] **Patterns**: Follows existing codebase conventions

Remember: **Refactoring is about improving structure without changing behavior**. If tests fail after refactoring, the refactoring isn't complete.