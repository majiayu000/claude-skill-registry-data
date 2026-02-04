---
name: testing-standards
version: "1.0.0"
category: _internal
description: "Testing Standards Skill"
---

# Testing Standards Skill

> Version: 1.0.0
> Category: Standards
> Triggers: Setting up tests, test configuration, TDD

## Quick Reference

### Test Framework Selection

**Python:** pytest
```bash
uv pip install pytest pytest-cov pytest-mock pytest-asyncio
```

**JavaScript/TypeScript:** Jest
**Bash/Shell:** bats-core

### Coverage Requirements

| Level | Minimum | Target |
|-------|---------|--------|
| Line | 80% | 90% |
| Branch | 75% | 85% |
| Function | 85% | 95% |

CI/CD fails if <80%.

### Test Organization

```
tests/
├── unit/
│   └── test_module_name.py
├── integration/
│   └── test_module_integration.py
├── performance/
│   └── test_module_performance.py
├── fixtures/
│   └── sample_data.json
└── conftest.py
```

### TDD Workflow

1. **RED** → Write failing test
2. **GREEN** → Write minimal code to pass
3. **REFACTOR** → Improve while keeping tests green
4. **REPEAT** → For each feature

### Running Tests

**Python:**
```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html --cov-fail-under=80

# Specific type
pytest tests/unit/
pytest -m performance
pytest -k "test_specific_function"

# Watch mode
pytest-watch
```

**JavaScript:**
```bash
npm test -- --coverage
npm test -- --watch
```

## Test Types

### Unit Tests
- Single function/method
- Mock external dependencies
- Fast (<100ms per test)
- No I/O or network

### Integration Tests
- Component interaction
- Real dependencies where possible
- Data flow between modules
- Error propagation

### Performance Tests
- Time thresholds
- Memory usage
- Benchmarking (pytest-benchmark)
- Run on every commit

## Best Practices

### Clear Assertions
```python
# ✅ Good: Specific assertion with context
assert result["status"] == "success", f"Expected success, got {result['status']}"

# ❌ Bad: Generic assertion
assert result
```

### Parametrized Tests
```python
@pytest.mark.parametrize("input_data,expected", [
    ([1, 2, 3], [1, 2, 3]),
    ([None, None], []),
    ([1, None, 2], [1, 2])
])
def test_clean_data(input_data, expected):
    assert clean_data(input_data) == expected
```

### Fixtures
```python
@pytest.fixture
def database():
    db = Database(":memory:")
    db.create_tables()
    yield db
    db.close()

def test_with_fixture(database):
    result = database.query("SELECT * FROM users")
```

## Configuration

**Python (pytest.ini):**
```ini
[pytest]
minversion = 7.0
addopts = --cov=src --cov-fail-under=80
testpaths = tests
markers =
    performance: Performance tests
    slow: Tests taking >1 second
```

**JavaScript (jest.config.js):**
```javascript
module.exports = {
  collectCoverage: true,
  coverageThresholds: {
    global: {
      branches: 75,
      functions: 85,
      lines: 80,
      statements: 80
    }
  }
};
```

## Mock Data Guidelines

- Use realistic data matching production scenarios
- Include edge cases and boundary conditions
- Version control all test fixtures
- Document expected data formats
- Keep fixtures minimal but representative

## Performance Tests

```python
def test_sort_performance(benchmark):
    data = list(range(10000, 0, -1))
    result = benchmark(sort_large_dataset, data)
    assert len(result) == 10000
    assert benchmark.stats['mean'] < 0.5  # <500ms
```

## Compliance Checklist

- [ ] 80%+ line coverage baseline achieved
- [ ] Unit, integration, performance tests defined
- [ ] Tests run in CI/CD on every commit
- [ ] No skipped tests (@pytest.mark.skip)
- [ ] All new features have tests
- [ ] Edge cases tested
- [ ] Mocking strategy documented

## Full Reference

See: @docs/modules/standards/TESTING_FRAMEWORK_STANDARDS.md

---

*Use this when setting up test infrastructure, writing tests, or debugging test failures.*
