---
name: mocks-fixtures
description: Build test doubles (mocks, stubs, spies, fakes), data factories, and fixtures for test isolation. Use when tests need external dependency isolation.
---

# Mocks & Fixtures

Create effective test doubles and fixtures for isolating units under test from external dependencies. This skill implements **Phase 4** of the 8-phase testing methodology.

## When to Use This Skill

Use this skill when you need to:

- Isolate code from external dependencies
- Mock API calls and HTTP responses
- Create consistent test data
- Build complex object hierarchies for tests
- Share setup code across tests
- Test error scenarios from external services
- Speed up tests by avoiding real I/O

**Trigger phrases**: "create mocks", "mock API", "test fixtures", "stub service", "fake database", "test data factory", "pytest fixtures", "Jest mocks", "Mockito"

## What This Skill Does

### Test Doubles Overview

| Type | Purpose | Returns | Verifies Calls |
|------|---------|---------|----------------|
| **Stub** | Provide canned responses | Predefined values | No |
| **Mock** | Verify interactions | Configurable | Yes |
| **Spy** | Wrap real implementation | Real + tracking | Yes |
| **Fake** | Simplified implementation | Computed values | No |

### Language-Specific Examples

#### Python (pytest + unittest.mock)

```python
import pytest
from unittest.mock import Mock, MagicMock, patch, AsyncMock
from myapp.services import UserService, EmailService
from myapp.models import User

# ==================== FIXTURES ====================

@pytest.fixture
def sample_user():
    """Basic user fixture."""
    return User(id=1, name="John Doe", email="john@example.com")

@pytest.fixture
def user_factory():
    """Factory for creating users with custom attributes."""
    def _create_user(**kwargs):
        defaults = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "is_active": True
        }
        defaults.update(kwargs)
        return User(**defaults)
    return _create_user

@pytest.fixture
def users_batch(user_factory):
    """Create multiple users."""
    return [
        user_factory(id=i, name=f"User {i}", email=f"user{i}@example.com")
        for i in range(1, 6)
    ]

# ==================== MOCKS ====================

@pytest.fixture
def mock_email_service():
    """Mock email service."""
    mock = Mock(spec=EmailService)
    mock.send_email.return_value = {"status": "sent", "message_id": "123"}
    return mock

@pytest.fixture
def mock_http_response():
    """Mock HTTP response object."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"data": "test"}
    mock.headers = {"Content-Type": "application/json"}
    return mock

@pytest.fixture
def mock_database_session():
    """Mock database session with common operations."""
    session = MagicMock()
    session.query.return_value.filter.return_value.first.return_value = None
    session.add = Mock()
    session.commit = Mock()
    session.rollback = Mock()
    return session

# ==================== ASYNC MOCKS ====================

@pytest.fixture
def mock_async_client():
    """Mock async HTTP client."""
    mock = AsyncMock()
    mock.get.return_value.json.return_value = {"result": "success"}
    mock.post.return_value.status_code = 201
    return mock

# ==================== USING FIXTURES & MOCKS ====================

class TestUserService:
    """Tests demonstrating fixture and mock usage."""

    def test_create_user_sends_welcome_email(
        self, user_factory, mock_email_service
    ):
        """Verify welcome email is sent when user is created."""
        # Arrange
        user = user_factory(email="new@example.com")
        service = UserService(email_service=mock_email_service)

        # Act
        service.create_user(user)

        # Assert
        mock_email_service.send_email.assert_called_once_with(
            to="new@example.com",
            template="welcome",
            data={"name": user.name}
        )

    def test_get_user_from_api(self, mock_http_response):
        """Test fetching user from external API."""
        mock_http_response.json.return_value = {
            "id": 1,
            "name": "API User"
        }

        with patch("myapp.services.requests.get", return_value=mock_http_response):
            service = UserService()
            user = service.get_user_from_api(1)

        assert user["name"] == "API User"

    @pytest.mark.asyncio
    async def test_async_user_fetch(self, mock_async_client):
        """Test async user fetching."""
        mock_async_client.get.return_value.json.return_value = {
            "id": 1,
            "name": "Async User"
        }

        with patch("myapp.services.httpx.AsyncClient", return_value=mock_async_client):
            service = UserService()
            user = await service.fetch_user_async(1)

        assert user["name"] == "Async User"

    def test_database_error_handling(self, user_factory, mock_database_session):
        """Test handling of database errors."""
        mock_database_session.commit.side_effect = Exception("DB Error")
        user = user_factory()
        service = UserService(db=mock_database_session)

        with pytest.raises(Exception, match="DB Error"):
            service.save_user(user)

        mock_database_session.rollback.assert_called_once()
```

#### JavaScript/TypeScript (Jest)

```typescript
import { jest } from '@jest/globals';
import { UserService } from '../src/services/UserService';
import { EmailService } from '../src/services/EmailService';
import { User } from '../src/models/User';

// ==================== FACTORIES ====================

const createUser = (overrides: Partial<User> = {}): User => ({
  id: 1,
  name: 'Test User',
  email: 'test@example.com',
  isActive: true,
  createdAt: new Date(),
  ...overrides
});

const createUsers = (count: number): User[] =>
  Array.from({ length: count }, (_, i) =>
    createUser({ id: i + 1, name: `User ${i + 1}`, email: `user${i + 1}@example.com` })
  );

// ==================== MOCKS ====================

const createMockEmailService = (): jest.Mocked<EmailService> => ({
  sendEmail: jest.fn().mockResolvedValue({ status: 'sent', messageId: '123' }),
  sendBulkEmail: jest.fn().mockResolvedValue({ sent: 5, failed: 0 }),
  validateEmail: jest.fn().mockReturnValue(true)
});

const createMockHttpClient = () => ({
  get: jest.fn().mockResolvedValue({
    data: { result: 'success' },
    status: 200
  }),
  post: jest.fn().mockResolvedValue({
    data: { id: 1 },
    status: 201
  }),
  put: jest.fn().mockResolvedValue({ status: 200 }),
  delete: jest.fn().mockResolvedValue({ status: 204 })
});

const createMockDatabase = () => ({
  query: jest.fn().mockResolvedValue({ rows: [] }),
  insert: jest.fn().mockResolvedValue({ insertId: 1 }),
  update: jest.fn().mockResolvedValue({ affectedRows: 1 }),
  delete: jest.fn().mockResolvedValue({ affectedRows: 1 }),
  transaction: jest.fn().mockImplementation(async (callback) => callback())
});

// ==================== TESTS ====================

describe('UserService', () => {
  let userService: UserService;
  let mockEmailService: jest.Mocked<EmailService>;
  let mockDb: ReturnType<typeof createMockDatabase>;

  beforeEach(() => {
    mockEmailService = createMockEmailService();
    mockDb = createMockDatabase();
    userService = new UserService(mockEmailService, mockDb);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    it('sends welcome email after creating user', async () => {
      const user = createUser({ email: 'new@example.com' });

      await userService.createUser(user);

      expect(mockEmailService.sendEmail).toHaveBeenCalledWith({
        to: 'new@example.com',
        template: 'welcome',
        data: expect.objectContaining({ name: user.name })
      });
    });

    it('rolls back on email failure', async () => {
      mockEmailService.sendEmail.mockRejectedValue(new Error('SMTP Error'));
      const user = createUser();

      await expect(userService.createUser(user)).rejects.toThrow('SMTP Error');
    });
  });

  describe('getUserById', () => {
    it('returns user from database', async () => {
      const expectedUser = createUser({ id: 42 });
      mockDb.query.mockResolvedValue({ rows: [expectedUser] });

      const result = await userService.getUserById(42);

      expect(result).toEqual(expectedUser);
      expect(mockDb.query).toHaveBeenCalledWith(
        expect.stringContaining('SELECT'),
        [42]
      );
    });

    it('returns null when user not found', async () => {
      mockDb.query.mockResolvedValue({ rows: [] });

      const result = await userService.getUserById(999);

      expect(result).toBeNull();
    });
  });
});

// ==================== MODULE MOCKING ====================

jest.mock('../src/services/ExternalApi', () => ({
  ExternalApi: {
    fetchData: jest.fn().mockResolvedValue({ data: 'mocked' }),
    postData: jest.fn().mockResolvedValue({ success: true })
  }
}));
```

#### Java (Mockito)

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private EmailService emailService;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Captor
    private ArgumentCaptor<Email> emailCaptor;

    // ==================== FACTORIES ====================

    private User createUser() {
        return createUser(1L, "Test User", "test@example.com");
    }

    private User createUser(Long id, String name, String email) {
        User user = new User();
        user.setId(id);
        user.setName(name);
        user.setEmail(email);
        user.setActive(true);
        return user;
    }

    private List<User> createUsers(int count) {
        return IntStream.rangeClosed(1, count)
            .mapToObj(i -> createUser((long) i, "User " + i, "user" + i + "@example.com"))
            .collect(Collectors.toList());
    }

    // ==================== TESTS ====================

    @Test
    void createUser_SendsWelcomeEmail() {
        // Arrange
        User user = createUser(1L, "John", "john@example.com");
        when(userRepository.save(any(User.class))).thenReturn(user);
        when(emailService.sendEmail(any())).thenReturn(true);

        // Act
        userService.createUser(user);

        // Assert
        verify(emailService).sendEmail(emailCaptor.capture());
        Email sentEmail = emailCaptor.getValue();
        assertThat(sentEmail.getTo()).isEqualTo("john@example.com");
        assertThat(sentEmail.getTemplate()).isEqualTo("welcome");
    }

    @Test
    void createUser_RollsBackOnEmailFailure() {
        User user = createUser();
        when(userRepository.save(any())).thenReturn(user);
        when(emailService.sendEmail(any())).thenThrow(new RuntimeException("SMTP Error"));

        assertThatThrownBy(() -> userService.createUser(user))
            .isInstanceOf(RuntimeException.class)
            .hasMessageContaining("SMTP Error");

        verify(userRepository).delete(user);
    }

    @Test
    void getUserById_ReturnsUserFromRepository() {
        User expected = createUser(42L, "Found User", "found@example.com");
        when(userRepository.findById(42L)).thenReturn(Optional.of(expected));

        User result = userService.getUserById(42L);

        assertThat(result).isEqualTo(expected);
    }

    @Test
    void getUserById_ReturnsNullWhenNotFound() {
        when(userRepository.findById(anyLong())).thenReturn(Optional.empty());

        User result = userService.getUserById(999L);

        assertThat(result).isNull();
    }

    // ==================== SPY EXAMPLE ====================

    @Test
    void processUsers_CallsRealMethodsWithTracking() {
        UserService spyService = spy(userService);
        List<User> users = createUsers(3);

        doReturn(users).when(spyService).getAllUsers();

        spyService.processAllUsers();

        verify(spyService, times(3)).processUser(any());
    }
}
```

## Prerequisites

- Test structure established (Phase 1)
- Understanding of code dependencies
- Knowledge of external services being mocked

## Instructions

### Step 1: Identify Dependencies

1. **List External Dependencies**
   - Database connections
   - HTTP clients
   - Message queues
   - File systems
   - External APIs

2. **Determine Mock Strategy**
   - What needs to be mocked vs real
   - Scope of mocks (test, class, module)

### Step 2: Create Fixtures

1. **Data Factories**
   - Create factory functions
   - Support customization via parameters
   - Generate realistic test data

2. **Shared Fixtures**
   - Place in conftest.py / setupTests.ts
   - Define appropriate scopes
   - Document usage

### Step 3: Implement Mocks

1. **Service Mocks**
   - Mock at interface level
   - Configure return values
   - Set up error scenarios

2. **HTTP Mocks**
   - Mock responses for all endpoints
   - Include error responses
   - Set appropriate status codes

## Quality Checklist

- [ ] All external dependencies mockable
- [ ] Factories create realistic data
- [ ] Mocks verify expected calls
- [ ] Error scenarios covered
- [ ] Fixtures properly scoped
- [ ] No shared mutable state

## Related Skills

- `unit-tests` - Unit testing (Phase 2)
- `test-cases` - Integration tests (Phase 3)
- `test-structure` - Test infrastructure (Phase 1)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/mocks_fixtures/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
