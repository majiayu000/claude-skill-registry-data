---
name: test-writing
description: Skill for the Test Writer agent to create tests before implementation (TDD). Use when executing /sp.test to write tests for a feature or task. Provides test patterns, fixture templates, assertion strategies, and framework-specific guidance for pytest (backend) and vitest/jest (frontend).
---

# Test Writing

Skill for creating comprehensive tests following Test-Driven Development (TDD) methodology.

## Overview

This skill enables the Test Writer agent to:
1. Create tests BEFORE implementation (TDD Red phase)
2. Generate appropriate test patterns based on component type
3. Design effective fixtures and mocks
4. Ensure acceptance criteria coverage

## TDD Workflow

```
/sp.test invoked
      |
      v
Read spec + contracts
      |
      v
Identify testable requirements
      |
      v
Select test patterns
      |
      v
Write failing tests
      |
      v
Verify tests fail (RED)
      |
      v
Report to PM
```

## Test Pattern Selection

Choose patterns based on what you're testing:

| Testing | Pattern | Framework |
|---------|---------|-----------|
| Pure functions | Unit tests | pytest / vitest |
| API endpoints | Integration tests | pytest + httpx |
| Database operations | Integration tests | pytest + fixtures |
| React components | Component tests | vitest + testing-library |
| User flows | E2E tests | playwright |

## Test Structure

### Backend (pytest)

```python
"""
Tests for [FEATURE]: [COMPONENT]
Spec: specs/{feature}/spec.md
Task: [TASK_ID]
"""
import pytest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import App

class Test[ComponentName]:
    """Tests for [component] functionality."""

    @pytest.fixture
    def setup(self):
        """Test setup."""
        # Arrange common data
        return {"data": "value"}

    def test_should_[behavior]_when_[condition](self, setup):
        """[AC: acceptance criteria reference]"""
        # Arrange
        input_data = setup["data"]

        # Act
        result = function_under_test(input_data)

        # Assert
        assert result == expected_value

    def test_should_raise_error_when_invalid_input(self):
        """Test error handling."""
        # Arrange
        invalid_input = None

        # Act & Assert
        with pytest.raises(ValueError, match="expected error"):
            function_under_test(invalid_input)
```

### Frontend (vitest)

```typescript
/**
 * Tests for [FEATURE]: [COMPONENT]
 * Spec: specs/{feature}/spec.md
 * Task: [TASK_ID]
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';

describe('[ComponentName]', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('when [scenario]', () => {
    it('should [expected behavior]', () => {
      // Arrange
      render(<Component prop="value" />);

      // Act
      fireEvent.click(screen.getByRole('button'));

      // Assert
      expect(screen.getByText('result')).toBeInTheDocument();
    });
  });

  describe('error handling', () => {
    it('should display error when [condition]', () => {
      // Arrange & Act
      render(<Component invalidProp={null} />);

      // Assert
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
  });
});
```

## Fixture Patterns

### Factory Pattern

```python
# tests/fixtures/factories.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserFactory:
    """Factory for creating test users."""
    id: int = 1
    name: str = "Test User"
    email: str = "test@example.com"

    @classmethod
    def create(cls, **overrides):
        defaults = {"id": 1, "name": "Test User", "email": "test@example.com"}
        defaults.update(overrides)
        return cls(**defaults)
```

### Database Fixtures

```python
# tests/fixtures/database.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db_session():
    """Provide a clean database session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
```

## Mock Strategies

### External API Mock

```python
from unittest.mock import patch, MagicMock

@patch('module.external_api_client')
def test_api_integration(mock_client):
    mock_client.get.return_value = {"status": "success"}
    result = function_that_calls_api()
    assert result["status"] == "success"
```

### React Hook Mock

```typescript
vi.mock('./useApi', () => ({
  useApi: vi.fn(() => ({
    data: { items: [] },
    loading: false,
    error: null,
  })),
}));
```

## Edge Case Checklist

Always test these scenarios:

- [ ] Empty input (null, undefined, empty string, empty array)
- [ ] Maximum values (string length, array size, numeric bounds)
- [ ] Minimum values (zero, negative numbers)
- [ ] Invalid formats (wrong type, malformed data)
- [ ] Unauthorized access attempts
- [ ] Network/database failure scenarios
- [ ] Concurrent operation handling
- [ ] Boundary conditions

## Acceptance Criteria Mapping

Map each test to acceptance criteria from spec:

```python
class TestUserRegistration:
    """
    User Story: As a new user, I want to register an account
    Spec: specs/auth/spec.md#US1
    """

    def test_should_create_user_when_valid_data(self):
        """AC1: User can register with email and password."""
        pass

    def test_should_send_verification_email(self):
        """AC2: Verification email is sent after registration."""
        pass

    def test_should_reject_duplicate_email(self):
        """AC3: Duplicate emails are rejected with clear error."""
        pass
```

## References

For detailed guidance, see:
- `references/test-patterns.md` - Common testing patterns and examples
- `references/fixture-guide.md` - Fixture creation best practices

## Quality Checklist

Before completing tests:

- [ ] All acceptance criteria have tests
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Tests follow naming convention
- [ ] Fixtures are reusable
- [ ] Mocks are isolated
- [ ] Tests are independent (no order dependency)
- [ ] Tests fail correctly (TDD Red phase verified)

## Run Commands

```bash
# Backend
pytest tests/{feature}/ -v
pytest tests/{feature}/ -v --tb=short  # Shorter output
pytest tests/{feature}/test_file.py::TestClass::test_method -v  # Single test

# Frontend
npm test -- tests/{feature}/
npm test -- tests/{feature}/ --watch  # Watch mode
npm test -- --testNamePattern="should create"  # Pattern match
```
