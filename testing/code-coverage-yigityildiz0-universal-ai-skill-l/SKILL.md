---
name: code-coverage
description: Analyze test coverage, identify gaps, and implement strategies for achieving 80%+ coverage targets. Use when measuring test effectiveness, identifying.
---

# Code Coverage Analysis

Measure, analyze, and improve test coverage to ensure comprehensive testing of your codebase. This skill implements **Phase 7** of the 8-phase testing methodology.

## When to Use This Skill

Use this skill when you need to:

- Measure current test coverage
- Identify untested code paths
- Meet coverage requirements (80%+)
- Generate coverage reports
- Configure coverage in CI/CD
- Improve test effectiveness
- Find dead code through coverage

**Trigger phrases**: "code coverage", "test coverage", "coverage report", "coverage gaps", "untested code", "80% coverage", "coverage threshold", "coverage analysis"

## What This Skill Does

### Coverage Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Line Coverage** | % of lines executed | 80%+ |
| **Branch Coverage** | % of branches taken | 75%+ |
| **Function Coverage** | % of functions called | 90%+ |
| **Statement Coverage** | % of statements executed | 80%+ |

### Language-Specific Tools & Examples

#### Python (pytest-cov / coverage.py)

```python
# pyproject.toml configuration
[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/migrations/*",
    "*/.venv/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
fail_under = 80
show_missing = true

[tool.coverage.html]
directory = "htmlcov"

# Running coverage
# pytest --cov=src --cov-report=html --cov-report=xml --cov-fail-under=80

# Coverage commands
# coverage run -m pytest tests/
# coverage report -m
# coverage html
# coverage xml
```

```python
# Example: Adding tests to improve coverage
# Before: 65% coverage in user_service.py

class UserService:
    def create_user(self, name: str, email: str) -> User:
        if not name:
            raise ValueError("Name is required")
        if not self._validate_email(email):
            raise ValueError("Invalid email")

        user = User(name=name, email=email)
        self.repository.save(user)

        # UNCOVERED: Email notification branch
        if self.config.send_welcome_email:
            self.email_service.send_welcome(user)

        return user

    def _validate_email(self, email: str) -> bool:
        # UNCOVERED: This method wasn't tested
        return "@" in email and "." in email.split("@")[1]


# Tests to improve coverage
class TestUserService:
    def test_create_user_sends_welcome_email_when_enabled(
        self, user_service, mock_email_service
    ):
        """Cover the email notification branch."""
        user_service.config.send_welcome_email = True

        user = user_service.create_user("John", "john@example.com")

        mock_email_service.send_welcome.assert_called_once_with(user)

    def test_create_user_skips_email_when_disabled(
        self, user_service, mock_email_service
    ):
        """Cover the else branch."""
        user_service.config.send_welcome_email = False

        user_service.create_user("John", "john@example.com")

        mock_email_service.send_welcome.assert_not_called()

    def test_validate_email_with_valid_email(self, user_service):
        """Cover _validate_email method."""
        assert user_service._validate_email("test@example.com") is True

    def test_validate_email_with_invalid_email(self, user_service):
        """Cover invalid email path."""
        assert user_service._validate_email("invalid") is False
        assert user_service._validate_email("no@domain") is False
```

#### JavaScript/TypeScript (Jest/c8)

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts',
    '!src/**/index.{js,ts}',
    '!src/**/*.test.{js,ts}'
  ],
  coverageThreshold: {
    global: {
      branches: 75,
      functions: 90,
      lines: 80,
      statements: 80
    },
    './src/services/': {
      branches: 80,
      functions: 95,
      lines: 85
    }
  },
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],
  coverageDirectory: 'coverage'
};

// package.json scripts
{
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage",
    "test:coverage:check": "jest --coverage --coverageThreshold='{\"global\":{\"lines\":80}}'",
    "coverage:open": "open coverage/lcov-report/index.html"
  }
}

// c8 (Node.js native coverage)
// c8 --check-coverage --lines 80 npm test
```

```typescript
// Example: Improving coverage for UserService
class UserService {
  async createUser(name: string, email: string): Promise<User> {
    if (!name) throw new Error('Name is required');
    if (!this.validateEmail(email)) throw new Error('Invalid email');

    const user = new User(name, email);
    await this.repository.save(user);

    // UNCOVERED BRANCH
    if (this.config.sendWelcomeEmail) {
      await this.emailService.sendWelcome(user);
    }

    return user;
  }

  private validateEmail(email: string): boolean {
    // UNCOVERED METHOD
    const parts = email.split('@');
    return parts.length === 2 && parts[1].includes('.');
  }
}

// Tests to achieve coverage
describe('UserService', () => {
  describe('createUser', () => {
    it('sends welcome email when enabled', async () => {
      mockConfig.sendWelcomeEmail = true;
      await userService.createUser('John', 'john@example.com');
      expect(mockEmailService.sendWelcome).toHaveBeenCalled();
    });

    it('skips welcome email when disabled', async () => {
      mockConfig.sendWelcomeEmail = false;
      await userService.createUser('John', 'john@example.com');
      expect(mockEmailService.sendWelcome).not.toHaveBeenCalled();
    });

    it('throws on empty name', async () => {
      await expect(userService.createUser('', 'test@example.com'))
        .rejects.toThrow('Name is required');
    });

    it('throws on invalid email', async () => {
      await expect(userService.createUser('John', 'invalid'))
        .rejects.toThrow('Invalid email');
    });
  });

  describe('validateEmail', () => {
    it.each([
      ['valid@example.com', true],
      ['user@domain.co.uk', true],
      ['invalid', false],
      ['no@domain', false],
      ['@example.com', false]
    ])('validates %s as %s', (email, expected) => {
      expect(userService['validateEmail'](email)).toBe(expected);
    });
  });
});
```

#### Java (JaCoCo)

```xml
<!-- pom.xml JaCoCo configuration -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <id>prepare-agent</id>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                            <limit>
                                <counter>BRANCH</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.75</minimum>
                            </limit>
                        </limits>
                    </rule>
                    <rule>
                        <element>CLASS</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.70</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>

<!-- Excluding files from coverage -->
<configuration>
    <excludes>
        <exclude>**/model/*</exclude>
        <exclude>**/dto/*</exclude>
        <exclude>**/*Config.*</exclude>
    </excludes>
</configuration>
```

#### Go (go test -cover)

```go
// Running coverage in Go
// go test -coverprofile=coverage.out ./...
// go tool cover -html=coverage.out -o coverage.html
// go tool cover -func=coverage.out

// Coverage with race detection
// go test -race -coverprofile=coverage.out ./...

// Example: Coverage improvement
// Before: 70% coverage

func (s *UserService) CreateUser(name, email string) (*User, error) {
    if name == "" {
        return nil, errors.New("name is required")
    }

    if !s.validateEmail(email) {
        return nil, errors.New("invalid email")
    }

    user := &User{Name: name, Email: email}
    if err := s.repo.Save(user); err != nil {
        return nil, fmt.Errorf("save failed: %w", err)
    }

    // UNCOVERED BRANCH
    if s.config.SendWelcome {
        s.emailService.SendWelcome(user)
    }

    return user, nil
}

// Tests to improve coverage
func TestUserService_CreateUser(t *testing.T) {
    tests := []struct {
        name        string
        userName    string
        email       string
        sendWelcome bool
        wantErr     bool
        errMsg      string
    }{
        {
            name:     "creates user successfully",
            userName: "John",
            email:    "john@example.com",
            wantErr:  false,
        },
        {
            name:    "fails with empty name",
            email:   "test@example.com",
            wantErr: true,
            errMsg:  "name is required",
        },
        {
            name:     "fails with invalid email",
            userName: "John",
            email:    "invalid",
            wantErr:  true,
            errMsg:   "invalid email",
        },
        {
            name:        "sends welcome email when enabled",
            userName:    "John",
            email:       "john@example.com",
            sendWelcome: true,
            wantErr:     false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            svc := NewUserService(
                mockRepo,
                mockEmailSvc,
                &Config{SendWelcome: tt.sendWelcome},
            )

            user, err := svc.CreateUser(tt.userName, tt.email)

            if tt.wantErr {
                require.Error(t, err)
                assert.Contains(t, err.Error(), tt.errMsg)
                return
            }

            require.NoError(t, err)
            assert.Equal(t, tt.userName, user.Name)

            if tt.sendWelcome {
                mockEmailSvc.AssertCalled(t, "SendWelcome", user)
            }
        })
    }
}
```

## Prerequisites

- Tests already written
- Testing framework configured
- Coverage tool available
- Understanding of codebase

## Instructions

### Step 1: Configure Coverage Tool

1. **Install Coverage Tool**
   ```bash
   # Python
   pip install pytest-cov coverage

   # JavaScript
   npm install --save-dev jest c8

   # Java - add JaCoCo plugin to pom.xml

   # Go - built-in
   ```

2. **Configure Exclusions**
   - Generated code
   - Migrations
   - Configuration files
   - Type definitions

### Step 2: Generate Initial Report

1. **Run Coverage**
   ```bash
   # Python
   pytest --cov=src --cov-report=html

   # JavaScript
   npm test -- --coverage

   # Java
   mvn test jacoco:report

   # Go
   go test -coverprofile=coverage.out ./...
   go tool cover -html=coverage.out
   ```

2. **Analyze Results**
   - Identify low-coverage files
   - Find untested branches
   - Note complex functions

### Step 3: Improve Coverage

1. **Prioritize High-Impact Areas**
   - Core business logic
   - Critical paths
   - Error handling

2. **Write Missing Tests**
   - Branch coverage
   - Error paths
   - Edge cases

### Step 4: Set Thresholds

1. **Configure Minimums**
   - Global: 80% lines
   - Critical: 90% branches
   - Per-file: 70% minimum

2. **Fail CI on Threshold**
   - Add to CI/CD pipeline
   - Block merges below threshold

## Quality Checklist

- [ ] Coverage tool configured
- [ ] Exclusions properly set
- [ ] Initial baseline measured
- [ ] Critical paths at 90%+
- [ ] Overall coverage at 80%+
- [ ] CI/CD threshold enforced
- [ ] Reports generated and accessible

## Related Skills

- `unit-tests` - Unit testing (Phase 2)
- `mutation-testing` - Test quality validation (Phase 8)
- `cicd-integration` - CI/CD setup (Phase 6)

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/code_coverage/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
