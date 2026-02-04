---
name: gold-standards
description: "Mandatory best practices and gold standards for Kailash SDK development including absolute imports, parameter passing, error handling, testing policies (NO MOCKING in Tiers 2-3), workflow design, custom node development, security, documentation, and test creation. Use when asking about 'best practices', 'standards', 'gold standards', 'mandatory rules', 'required patterns', 'absolute imports', 'NO MOCKING', 'testing policy', 'error handling standards', 'security best practices', 'documentation standards', or 'workflow design standards'."
---

# Kailash Gold Standards - Mandatory Best Practices

Mandatory best practices and standards for all Kailash SDK development. These are **required** patterns that must be followed.

## Overview

Gold standards are **mandatory** practices for:
- Absolute imports (no relative imports)
- Parameter passing patterns
- Error handling strategies
- Testing policies (NO MOCKING in Tiers 2-3)
- Workflow design principles
- Custom node development
- Security requirements
- Documentation standards
- Test creation guidelines

**IMPORTANT**: These are not suggestions - they are **required standards** that prevent bugs, ensure consistency, and maintain code quality.

## Reference Documentation

### Code Organization

#### Absolute Imports (MANDATORY)
- **[gold-absolute-imports](gold-absolute-imports.md)** - Absolute import requirement
  - **Rule**: ALWAYS use absolute imports, NEVER relative
  - **Reason**: Prevents import errors, enables refactoring
  - **Pattern**: `from kailash.workflow.builder import WorkflowBuilder`
  - **Never**: `from ..workflow import builder`

#### Parameter Passing (MANDATORY)
- **[gold-parameter-passing](gold-parameter-passing.md)** - Parameter standards
  - **Rule**: Use 4-parameter connection format
  - **Pattern**: `workflow.add_connection(source_id, source_param, target_id, target_param)`
  - **Rule**: Access results with dict pattern
  - **Pattern**: `results["node_id"]["result"]`
  - **Never**: `results["node_id"].result`

### Testing Standards

#### NO MOCKING Policy (MANDATORY)
- **[gold-mocking-policy](gold-mocking-policy.md)** - NO MOCKING in Tiers 2-3
  - **Rule**: NO mocking in integration (Tier 2) or E2E (Tier 3) tests
  - **Reason**: Mocking hides real-world issues
  - **Required**: Use real databases, APIs, infrastructure
  - **Allowed**: Mocking ONLY in Tier 1 unit tests

#### Testing Standards (MANDATORY)
- **[gold-testing](gold-testing.md)** - Testing requirements
  - **Rule**: Follow 3-tier strategy (Unit, Integration, E2E)
  - **Rule**: Tiers 2-3 use real infrastructure
  - **Rule**: All tests must clean up resources
  - **Rule**: Tests must be deterministic

#### Test Creation (MANDATORY)
- **[gold-test-creation](gold-test-creation.md)** - Test creation standards
  - **Rule**: Write tests BEFORE implementation (TDD)
  - **Rule**: One assertion focus per test
  - **Rule**: Use AAA pattern (Arrange, Act, Assert)
  - **Rule**: Descriptive test names

### Error Handling

#### Error Handling (MANDATORY)
- **[gold-error-handling](gold-error-handling.md)** - Error handling requirements
  - **Rule**: Always handle errors explicitly
  - **Rule**: Never swallow exceptions silently
  - **Rule**: Provide actionable error messages
  - **Rule**: Clean up resources in finally blocks
  - **Rule**: Log errors with context

### Workflow & Node Design

#### Workflow Design (MANDATORY)
- **[gold-workflow-design](gold-workflow-design.md)** - Workflow standards
  - **Rule**: Always call `.build()` before execution
  - **Pattern**: `runtime.execute(workflow.build())`
  - **Rule**: Use string-based node API
  - **Rule**: Validate inputs before processing
  - **Rule**: Single responsibility per workflow

#### Custom Node Development (MANDATORY)
- **[gold-custom-nodes](gold-custom-nodes.md)** - Custom node standards
  - **Rule**: Extend BaseNode
  - **Rule**: Validate all inputs
  - **Rule**: Handle errors gracefully
  - **Rule**: Document parameters clearly
  - **Rule**: Return consistent output format

### Security & Documentation

#### Security (MANDATORY)
- **[gold-security](gold-security.md)** - Security requirements
  - **Rule**: NEVER hardcode secrets
  - **Rule**: Use environment variables for credentials
  - **Rule**: Validate all user inputs
  - **Rule**: Prevent SQL injection
  - **Rule**: Prevent code injection
  - **Rule**: Use HTTPS for API calls

#### Documentation (MANDATORY)
- **[gold-documentation](gold-documentation.md)** - Documentation standards
  - **Rule**: Document all public APIs
  - **Rule**: Include code examples
  - **Rule**: Keep docs updated with code
  - **Rule**: Use docstrings for all functions/classes
  - **Rule**: Explain WHY, not just WHAT

## Critical Gold Standards

### 1. Absolute Imports ALWAYS
```python
# ✅ CORRECT (Gold Standard)
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# ❌ WRONG (Violates Gold Standard)
from ..workflow.builder import WorkflowBuilder
from .runtime import LocalRuntime
```

### 2. NO MOCKING in Tiers 2-3
```python
# ✅ CORRECT (Gold Standard - Tier 2)
def test_dataflow_crud(db: DataFlow):  # Real database
    """Test with real PostgreSQL/SQLite."""
    workflow = db.create_workflow(...)
    results = runtime.execute(workflow.build())
    # Verify in actual database

# ❌ WRONG (Violates Gold Standard)
def test_dataflow_crud():
    """Test with mocked database."""
    db = Mock(spec=DataFlow)  # NO MOCKING in Tier 2!
    db.create_workflow.return_value = mock_workflow
```

### 3. 4-Parameter Connections ALWAYS
```python
# ✅ CORRECT (Gold Standard)
workflow.add_connection("node1", "result", "node2", "input_data")

# ❌ WRONG (Violates Gold Standard)
workflow.add_connection("node1", "node2")
```

### 4. Always Call .build()
```python
# ✅ CORRECT (Gold Standard)
results = runtime.execute(workflow.build())

# ❌ WRONG (Violates Gold Standard)
results = runtime.execute(workflow)
```

### 5. Dict-Based Result Access
```python
# ✅ CORRECT (Gold Standard)
value = results["node_id"]["result"]

# ❌ WRONG (Violates Gold Standard)
value = results["node_id"].result
```

### 6. Environment Variables for Secrets
```python
# ✅ CORRECT (Gold Standard)
import os
api_key = os.environ["API_KEY"]

# ❌ WRONG (Violates Gold Standard)
api_key = "sk-1234567890abcdef"  # Hardcoded!
```

### 7. TDD (Test-First Development)
```python
# ✅ CORRECT (Gold Standard)
# 1. Write test first
def test_user_creation():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"

# 2. Then implement
def create_user(email):
    return User(email=email)

# ❌ WRONG (Violates Gold Standard)
# Write implementation first, then add tests
```

### 8. Explicit Error Handling
```python
# ✅ CORRECT (Gold Standard)
try:
    results = runtime.execute(workflow.build())
except WorkflowExecutionError as e:
    logger.error(f"Workflow failed: {e}")
    raise
finally:
    cleanup_resources()

# ❌ WRONG (Violates Gold Standard)
try:
    results = runtime.execute(workflow.build())
except:  # Too broad, swallows errors
    pass  # Silent failure!
```

## Compliance Checklist

### Before Every Commit
- [ ] All imports are absolute
- [ ] All connections use 4 parameters
- [ ] Called `.build()` before execute
- [ ] No hardcoded secrets
- [ ] Error handling present
- [ ] Tests written (TDD)
- [ ] No mocking in Tier 2-3 tests
- [ ] Documentation updated

### Before Every PR
- [ ] Gold standards validator passed
- [ ] All tests passing
- [ ] Code reviewed for compliance
- [ ] Security validation passed
- [ ] Documentation complete

### Before Every Release
- [ ] Full gold standards audit
- [ ] All patterns compliant
- [ ] Security audit complete
- [ ] Documentation verified

## Enforcement

### Automated Validation
```bash
# Run gold standards validator
python -m kailash.validation.gold_standards validate-all

# Check specific standards
python -m kailash.validation.gold_standards check-imports
python -m kailash.validation.gold_standards check-mocking
python -m kailash.validation.gold_standards check-security
```

### Code Review Focus
- Check absolute imports
- Verify NO MOCKING policy
- Validate connection format
- Check error handling
- Verify TDD approach
- Review security patterns

## Why Gold Standards Matter

### Problems They Prevent

**Absolute Imports**: Prevent import errors during refactoring

**NO MOCKING**: Catch real database issues, API timeouts, race conditions

**4-Parameter Connections**: Prevent wrong data routing

**.build() Requirement**: Prevent TypeError at runtime

**Error Handling**: Prevent silent failures

**TDD**: Prevent bugs before they exist

**Security Standards**: Prevent credential leaks, injection attacks

## When to Use This Skill

Use this skill:
- **Before writing code** - Know the standards
- **During code review** - Validate compliance
- **When in doubt** - Check gold standards
- **Before deployment** - Ensure compliance
- **When onboarding** - Learn required patterns

## Related Skills

- **[16-validation-patterns](../16-validation-patterns/SKILL.md)** - Validation tools
- **[15-error-troubleshooting](../15-error-troubleshooting/SKILL.md)** - Error patterns
- **[12-testing-strategies](../12-testing-strategies/SKILL.md)** - Testing strategies
- **[01-core-sdk](../01-core-sdk/SKILL.md)** - Core patterns

## Support

For gold standards compliance, invoke:
- `gold-standards-validator` - Automated compliance checking
- `pattern-expert` - Pattern validation
- `testing-specialist` - Testing compliance
- `requirements-analyst` - Standards documentation
