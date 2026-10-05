---
name: test-coverage-advisor
description: This skill should be used when the user asks to "write tests", "generate tests", "check coverage", "add test cases", or when completing features and saying "done", "finished", "ready for review". Suggests tests for 90%+ coverage.
---

# Test Coverage Advisor

Auto-suggests comprehensive test cases to achieve the 90%+ test coverage target.

## Activation Triggers

This skill activates when:
- Completing feature implementation
- Mentioning "done", "finished", "ready", "complete"
- Saying "review this code"
- Creating models, services, views, or APIs
- Asking about testing
- Before code is marked as complete

## Coverage Target (MANDATORY)

**90%+ test coverage required for ALL code.**

Test categories:
1. **Unit Tests** - Models, services, utilities (80%+ of tests)
2. **Integration Tests** - API endpoints, workflows (15%+ of tests)
3. **Edge Cases** - Error handling, validation (5%+ of tests)

## Auto-Analysis Process

### Step 1: Identify Untested Code

When feature implementation is complete, scan for:

```python
# models.py - Has tests? ❓
class User(models.Model):
    def activate(self):  # Needs test
        self.is_active = True
        self.save()

# services.py - Has tests? ❓
class UserService:
    @staticmethod
    def create_user(data):  # Needs test
        # ...business logic

# views.py - Has tests? ❓
class UserViewSet(viewsets.ModelViewSet):
    def create(self, request):  # Needs test
        # ...
```

### Step 2: Calculate Coverage Gap

```
Current coverage: X%
Target coverage: 90%
Gap: Y%
Missing: Z test cases
```

### Step 3: Generate Missing Test Cases

**For Model:**
```python
# users/tests/test_models.py
import pytest
import users.models as _users_models

@pytest.mark.django_db
class TestUserModel:
    """User model tests."""

    def test_create_user(self):
        """Test user creation with required fields."""
        user = _users_models.User.objects.create(
            email='test@example.com',
            first_name='Test'
        )

        assert user.id is not None  # UUID assigned
        assert user.email == 'test@example.com'
        assert user.created_at is not None
        assert user.is_deleted is False

    def test_user_str_representation(self):
        """Test __str__ returns email."""
        user = _users_models.User.objects.create(email='test@example.com')
        assert str(user) == 'test@example.com'

    def test_activate_user(self):
        """Test activate method sets is_active."""
        user = _users_models.User.objects.create(email='test@example.com')
        user.activate()

        assert user.is_active is True

    def test_soft_delete(self):
        """Test soft delete sets is_deleted flag."""
        user = _users_models.User.objects.create(email='test@example.com')
        user.soft_delete()

        assert user.is_deleted is True
        # User still in database
        assert _users_models.User.objects.filter(id=user.id).exists()
```

**For Service:**
```python
# users/tests/test_services.py
import pytest
from unittest.mock import Mock, patch
import users.models as _users_models
import users.services as _users_services

@pytest.mark.django_db
class TestUserService:
    """UserService tests."""

    def test_create_user_success(self):
        """Test successful user creation."""
        data = {'email': 'test@example.com', 'first_name': 'Test'}
        user = _users_services.UserService.create_user(data)

        assert user.email == 'test@example.com'
        assert user.first_name == 'Test'

    def test_create_user_duplicate_email(self):
        """Test creation fails with duplicate email."""
        _users_models.User.objects.create(email='test@example.com')

        with pytest.raises(ValidationError):
            _users_services.UserService.create_user({'email': 'test@example.com'})

    def test_create_user_invalid_data(self):
        """Test creation fails with invalid data."""
        with pytest.raises(ValidationError):
            _users_services.UserService.create_user({'email': 'invalid'})

    @patch('users.services.send_welcome_email')
    def test_create_user_sends_email(self, mock_send):
        """Test welcome email is sent on user creation."""
        data = {'email': 'test@example.com'}
        user = _users_services.UserService.create_user(data)

        mock_send.assert_called_once_with(user)
```

**For API Endpoint:**
```python
# users/tests/test_views.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
import users.models as _users_models

@pytest.mark.django_db
class TestUserViewSet:
    """UserViewSet API tests."""

    def setup_method(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = _users_models.User.objects.create(
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_users_authenticated(self):
        """Test authenticated user can list users."""
        response = self.client.get('/api/users/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_list_users_unauthenticated(self):
        """Test unauthenticated request is rejected."""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/users/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_user(self):
        """Test user creation via API."""
        data = {'email': 'new@example.com', 'first_name': 'New'}
        response = self.client.post('/api/users/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'new@example.com'

    def test_create_user_invalid_data(self):
        """Test creation fails with invalid data."""
        data = {'email': 'invalid'}
        response = self.client.post('/api/users/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_user(self):
        """Test user update via PATCH."""
        data = {'first_name': 'Updated'}
        response = self.client.patch(f'/api/users/{self.user.id}/', data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'

    def test_update_user_permission_denied(self):
        """Test user cannot update other users."""
        other_user = _users_models.User.objects.create(email='other@example.com')
        data = {'first_name': 'Hacked'}
        response = self.client.patch(f'/api/users/{other_user.id}/', data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_soft_delete_user(self):
        """Test user soft delete."""
        response = self.client.delete(f'/api/users/{self.user.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        self.user.refresh_from_db()
        assert self.user.is_deleted is True
```

### Step 4: Report Coverage Plan

Provide a detailed report:

> **Test Coverage Analysis**
>
> **Untested Code Detected:**
> - `User` model: 4 methods
> - `UserService`: 3 methods
> - `UserViewSet`: 5 endpoints
>
> **Suggested Tests: 23**
> - Model tests: 8 (unit)
> - Service tests: 10 (unit + integration)
> - API tests: 5 (integration)
>
> **Estimated Coverage:**
> - Current: 45%
> - After tests: 92%
> - Target: 90% ✅
>
> **Implementation:**
> I can generate all tests now. Should I proceed?

## Edge Case Checklist

For every function/method, suggest tests for:

### Input Validation
- ✅ Valid input (happy path)
- ✅ Invalid input (validation errors)
- ✅ Missing required fields
- ✅ Empty strings/None values
- ✅ Boundary conditions (min/max)

### Business Logic
- ✅ Expected behavior
- ✅ Side effects (emails sent, logs created)
- ✅ Database changes
- ✅ Return values correct

### Error Handling
- ✅ Exceptions raised correctly
- ✅ Database errors handled
- ✅ External service failures

### Permissions
- ✅ Authenticated access
- ✅ Unauthorized rejection
- ✅ Permission-based access
- ✅ Ownership validation

### Edge Cases
- ✅ Concurrent modifications
- ✅ Duplicate entries
- ✅ Soft-deleted records
- ✅ Large datasets

## Test File Organization

```
users/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── test_models.py           # Model unit tests
│   ├── test_services.py         # Service tests
│   ├── test_serializers.py      # Serializer tests
│   ├── test_views.py            # API integration tests
│   └── test_permissions.py      # Permission tests
```

## Pytest Configuration

Also suggest pytest setup:

```python
# conftest.py
import pytest
import users.models as _users_models

@pytest.fixture
def user():
    """Create test user."""
    return _users_models.User.objects.create(
        email='test@example.com',
        first_name='Test'
    )

@pytest.fixture
def authenticated_client(user):
    """Create authenticated API client."""
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    return client
```

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
python_files = tests.py test_*.py *_tests.py
addopts = --cov=. --cov-report=html --cov-report=term-missing
```

## Factory Pattern (factory_boy)

For complex test data, suggest factories:

```python
# users/tests/factories.py
import factory
import users.models as _users_models

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = _users_models.User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

# Usage in tests
def test_bulk_users():
    users = UserFactory.create_batch(100)  # Create 100 users
    assert len(users) == 100
```

## Integration with CI/CD

Suggest coverage enforcement in CI:

```yaml
# .github/workflows/tests.yml
- name: Run tests with coverage
  run: |
    pytest --cov=. --cov-fail-under=90
```

## Success Criteria

✅ 90%+ coverage achieved
✅ All models tested
✅ All services tested
✅ All API endpoints tested
✅ Edge cases covered
✅ Permissions tested
✅ Error handling tested

## Behavior

**Proactive enforcement:**
- Analyze coverage without being asked
- Suggest tests when code is complete
- Generate complete test files
- Explain what each test verifies
- Calculate coverage impact

**Never:**
- Require explicit "write tests" request
- Wait for coverage report
- Just list what to test without writing tests

**When user says "done" or "ready":**
- Immediately analyze test coverage
- Identify gaps
- Suggest (or write) missing tests
- Don't let code be "complete" without tests

This ensures 90%+ coverage is maintained from day one.
