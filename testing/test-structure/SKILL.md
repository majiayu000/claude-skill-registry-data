---
name: test-structure
description: Set up testing infrastructure including framework selection, directory organization, configuration files, and initial test scaffolding. Use when starting a.
---

# Test Structure Setup

Establish comprehensive testing infrastructure with optimal framework configuration, logical directory organization, efficient fixture management, and reusable test utilities. This skill is **Phase 1** of the 8-phase testing methodology and provides the foundation for all subsequent testing activities.

## When to Use This Skill

Use this skill when you need to:

- Start testing in a new project from scratch
- Add testing infrastructure to an existing codebase
- Restructure or improve existing test organization
- Configure a testing framework (pytest, Jest, JUnit, xUnit, Go testing)
- Set up test discovery, fixtures, and utilities
- Establish testing standards for a team
- Migrate from one testing framework to another

**Trigger phrases**: "set up tests", "configure testing", "create test structure", "initialize tests", "test infrastructure", "pytest setup", "Jest configuration", "JUnit setup", "testing framework"

## What This Skill Does

### For All Languages

1. **Framework Selection & Configuration**
   - Analyze project requirements for framework selection
   - Configure framework settings and plugins
   - Set up test discovery rules
   - Enable parallel test execution
   - Configure output formats and reporting

2. **Directory Structure Design**
   - Create standardized test directory layout
   - Separate test types (unit, integration, e2e)
   - Establish naming conventions
   - Set up resource directories for test data
   - Configure module initialization files

3. **Fixture Infrastructure**
   - Establish fixture hierarchy and scopes
   - Create fixture factories for complex objects
   - Implement shared fixtures across test modules
   - Document fixture usage patterns
   - Set up fixture cleanup and teardown

4. **Test Utilities & Helpers**
   - Create common assertion helpers
   - Implement test data generators
   - Define custom decorators/annotations
   - Establish shared base classes
   - Document utility functions

### Language-Specific Features

#### Python (pytest)
- **Framework**: pytest 8.x with plugins (pytest-cov, pytest-xdist, pytest-mock)
- **Configuration**: pyproject.toml or pytest.ini
- **Fixtures**: conftest.py hierarchy with scoped fixtures
- **Markers**: Custom markers for test categorization

```python
# pyproject.toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "-v",
]
markers = [
    "unit: Unit tests (fast, isolated)",
    "integration: Integration tests (may use external resources)",
    "e2e: End-to-end tests (full system)",
    "slow: Tests that take >1s",
]

# Directory structure
tests/
├── conftest.py              # Root fixtures
├── unit/
│   ├── conftest.py          # Unit-specific fixtures
│   ├── test_models.py
│   └── test_services.py
├── integration/
│   ├── conftest.py
│   └── test_api.py
└── e2e/
    └── test_workflows.py
```

#### JavaScript/TypeScript (Jest)
- **Framework**: Jest 29.x with TypeScript support
- **Configuration**: jest.config.js or package.json
- **Setup Files**: setupTests.js for global configuration
- **Mocking**: Built-in mock functions and module mocking

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: ['**/__tests__/**/*.ts', '**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80, statements: 80 }
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setupTests.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  }
};

// Directory structure
tests/
├── setupTests.ts            # Global setup
├── helpers/
│   ├── factories.ts         # Test data factories
│   └── mocks.ts             # Shared mocks
├── unit/
│   └── services.test.ts
└── integration/
    └── api.test.ts
```

#### Java (JUnit 5)
- **Framework**: JUnit 5 (Jupiter) with Mockito
- **Configuration**: pom.xml or build.gradle
- **Extensions**: Custom extensions for lifecycle management
- **Nested Tests**: Organized test hierarchies

```java
// pom.xml dependencies
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <version>5.7.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>

// Directory structure
src/
├── main/java/com/example/
│   └── service/
└── test/java/com/example/
    ├── unit/
    │   └── service/
    │       └── UserServiceTest.java
    ├── integration/
    │   └── api/
    └── fixtures/
        └── TestDataFactory.java
```

#### C# (xUnit/NUnit)
- **Framework**: xUnit 2.x or NUnit 3.x
- **Configuration**: .csproj with test settings
- **Fixtures**: IClassFixture for shared context
- **Theory**: Data-driven tests with InlineData

```csharp
// MyProject.Tests.csproj
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="xunit" Version="2.6.0" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.0" />
    <PackageReference Include="Moq" Version="4.20.0" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="coverlet.collector" Version="6.0.0" />
  </ItemGroup>
</Project>

// Directory structure
tests/
├── MyProject.Tests/
│   ├── Unit/
│   │   └── Services/
│   ├── Integration/
│   └── Fixtures/
│       └── DatabaseFixture.cs
```

#### Go (testing package)
- **Framework**: Built-in testing package with testify
- **Configuration**: go.mod for dependencies
- **Table-Driven**: Idiomatic table-driven tests
- **Subtests**: t.Run for organized test cases

```go
// go.mod
module example.com/myproject

require (
    github.com/stretchr/testify v1.8.4
    github.com/golang/mock v1.6.0
)

// Directory structure (tests alongside code)
pkg/
├── service/
│   ├── user.go
│   └── user_test.go          # Unit tests
├── integration/
│   └── api_test.go           # Integration tests
└── testutil/
    ├── fixtures.go           # Test fixtures
    └── mocks/                 # Generated mocks
```

#### C (Unity/CUnit)
- **Framework**: Unity or CUnit for embedded/systems
- **Configuration**: CMakeLists.txt or Makefile
- **Fixtures**: setUp/tearDown functions
- **Test Runners**: Custom or CTest integration

```c
// CMakeLists.txt
cmake_minimum_required(VERSION 3.14)
project(myproject C)

enable_testing()

# Unity test framework
add_subdirectory(vendor/Unity)

# Test executable
add_executable(test_runner
    tests/test_main.c
    tests/test_module.c
    src/module.c
)
target_link_libraries(test_runner unity)

add_test(NAME unit_tests COMMAND test_runner)

// Directory structure
project/
├── src/
│   └── module.c
├── include/
│   └── module.h
├── tests/
│   ├── test_main.c           # Test runner
│   ├── test_module.c         # Module tests
│   └── fixtures/
│       └── test_data.h
└── vendor/
    └── Unity/
```

#### C++ (GoogleTest/Catch2)
- **Framework**: GoogleTest (gtest) or Catch2
- **Configuration**: CMakeLists.txt with FetchContent
- **Fixtures**: Test fixtures with SetUp/TearDown
- **Parameterized**: INSTANTIATE_TEST_SUITE_P

```cpp
// CMakeLists.txt
cmake_minimum_required(VERSION 3.14)
project(myproject CXX)

set(CMAKE_CXX_STANDARD 17)
enable_testing()

include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
)
FetchContent_MakeAvailable(googletest)

add_executable(tests
    tests/test_main.cpp
    tests/test_module.cpp
)
target_link_libraries(tests gtest_main gmock)
include(GoogleTest)
gtest_discover_tests(tests)

// Directory structure
project/
├── src/
│   └── module.cpp
├── include/
│   └── module.hpp
├── tests/
│   ├── test_main.cpp
│   ├── unit/
│   │   └── test_module.cpp
│   └── fixtures/
│       └── test_fixtures.hpp
```

## Prerequisites

- Source code repository with clear module structure
- Build system configured (pip, npm, Maven, MSBuild, Go modules, CMake)
- Understanding of project architecture
- Decision on test types needed (unit, integration, e2e)

## Instructions

### Step 1: Analyze Project Structure

1. **Examine Source Code Organization**
   ```bash
   # Get directory structure
   tree -L 3 -I 'node_modules|venv|.venv|__pycache__|target|build|bin|obj'
   ```

2. **Identify Modules to Test**
   - List main source directories
   - Identify core business logic
   - Note external dependencies
   - Map API endpoints or interfaces

3. **Document Current Test State**
   - Check for existing tests
   - Review current test configuration
   - Note coverage gaps

### Step 2: Select and Configure Framework

1. **Choose Framework** (if not already decided)
   - Python: pytest (recommended)
   - JavaScript/TypeScript: Jest
   - Java: JUnit 5
   - C#: xUnit or NUnit
   - Go: testing + testify
   - C: Unity or CUnit
   - C++: GoogleTest or Catch2

2. **Install Framework and Plugins**

   **Python:**
   ```bash
   pip install pytest pytest-cov pytest-xdist pytest-mock pytest-asyncio
   ```

   **JavaScript:**
   ```bash
   npm install --save-dev jest @types/jest ts-jest
   ```

   **Java (Maven):**
   ```xml
   <dependency>
       <groupId>org.junit.jupiter</groupId>
       <artifactId>junit-jupiter</artifactId>
       <version>5.10.0</version>
       <scope>test</scope>
   </dependency>
   ```

3. **Create Configuration File**
   - Add framework-specific configuration
   - Configure test discovery patterns
   - Set up parallel execution
   - Define output formats

### Step 3: Create Directory Structure

1. **Create Test Directories**
   ```bash
   # Python/JavaScript/Go
   mkdir -p tests/unit tests/integration tests/e2e tests/fixtures

   # Java
   mkdir -p src/test/java/com/example/unit
   mkdir -p src/test/java/com/example/integration

   # C#
   mkdir -p tests/MyProject.Tests/Unit
   mkdir -p tests/MyProject.Tests/Integration
   ```

2. **Add Initialization Files**
   - Python: `__init__.py` in each test directory
   - JavaScript: `index.ts` exports if needed
   - Java: Package structure matching source

3. **Create Fixture Directories**
   - Test data files location
   - Mock response files
   - Configuration samples

### Step 4: Set Up Fixtures and Utilities

1. **Create Root Fixture File**

   **Python (conftest.py):**
   ```python
   import pytest
   from typing import Generator

   @pytest.fixture(scope="session")
   def app_config() -> dict:
       """Application configuration for tests."""
       return {
           "database_url": "sqlite:///:memory:",
           "api_key": "test-key",
           "debug": True
       }

   @pytest.fixture
   def sample_user() -> dict:
       """Sample user data for tests."""
       return {
           "id": 1,
           "name": "Test User",
           "email": "test@example.com"
       }
   ```

   **JavaScript (setupTests.ts):**
   ```typescript
   import { jest } from '@jest/globals';

   // Global test setup
   beforeAll(() => {
     process.env.NODE_ENV = 'test';
   });

   // Reset mocks between tests
   afterEach(() => {
     jest.clearAllMocks();
   });

   // Test utilities
   export const createMockUser = () => ({
     id: 1,
     name: 'Test User',
     email: 'test@example.com'
   });
   ```

2. **Create Test Data Factories**
   - Factory functions for complex objects
   - Random data generation
   - Consistent test data across tests

3. **Create Custom Assertions**
   - Domain-specific assertion helpers
   - Improved error messages
   - Complex validation shortcuts

### Step 5: Create Sample Tests

1. **Create First Unit Test**

   **Python:**
   ```python
   # tests/unit/test_example.py
   import pytest

   class TestExample:
       """Example test class demonstrating structure."""

       def test_addition(self):
           """Test basic addition."""
           # Arrange
           a, b = 2, 3

           # Act
           result = a + b

           # Assert
           assert result == 5

       @pytest.mark.parametrize("input,expected", [
           (1, 1),
           (2, 4),
           (3, 9),
       ])
       def test_square(self, input: int, expected: int):
           """Test square calculation with multiple inputs."""
           assert input ** 2 == expected
   ```

2. **Verify Test Discovery**
   ```bash
   # Python
   pytest --collect-only

   # JavaScript
   jest --listTests

   # Java
   mvn test -Dtest=*Test

   # Go
   go test -v -list '.*'
   ```

3. **Run Tests**
   ```bash
   # Python
   pytest -v

   # JavaScript
   npm test

   # Java
   mvn test

   # C#
   dotnet test

   # Go
   go test ./...
   ```

### Step 6: Document Testing Standards

1. **Create Testing Guide**
   - Naming conventions
   - Directory structure explanation
   - Fixture usage patterns
   - Running tests locally
   - CI/CD integration

2. **Define Quality Standards**
   - Minimum coverage requirements (80%+)
   - Test execution time limits (<1s for unit tests)
   - Required test types per feature
   - Review checklist for tests

## Output Structure

```
tests/
├── conftest.py / setupTests.ts / fixtures/     # Shared fixtures
├── unit/                                        # Unit tests
│   ├── test_models.py / models.test.ts
│   └── test_services.py / services.test.ts
├── integration/                                 # Integration tests
│   └── test_api.py / api.test.ts
├── e2e/                                         # End-to-end tests
│   └── test_workflows.py / workflows.test.ts
├── fixtures/                                    # Test data
│   ├── sample_data.json
│   └── mock_responses/
└── helpers/                                     # Test utilities
    ├── factories.py / factories.ts
    └── assertions.py / assertions.ts
```

## Quality Checklist

Before completing test structure setup, verify:

- [ ] Framework installed and configured correctly
- [ ] Configuration file created (pytest.ini, jest.config.js, etc.)
- [ ] Test directories created with proper naming
- [ ] Initialization files added where needed
- [ ] Root fixture/setup file created
- [ ] Sample test runs successfully
- [ ] Test discovery finds all test files
- [ ] Parallel execution configured (if applicable)
- [ ] Coverage reporting configured
- [ ] Testing guide documented
- [ ] CI/CD integration prepared

## Common Issues and Solutions

### Issue: Tests not discovered
**Solution**: Verify naming conventions match framework patterns. Python tests must start with `test_`, JavaScript tests must end with `.test.ts` or `.spec.ts`.

### Issue: Import errors in tests
**Solution**: Ensure proper package structure with `__init__.py` files (Python) or module resolution configured (JavaScript/TypeScript).

### Issue: Fixtures not found
**Solution**: Check fixture file location (conftest.py must be in tests/ or parent directory), verify fixture scope matches usage.

### Issue: Slow test execution
**Solution**: Configure parallel execution (pytest-xdist, Jest workers), separate slow tests with markers.

## Success Criteria

After using this skill, you should have:

- [ ] Complete test infrastructure configured
- [ ] Clear directory structure for all test types
- [ ] Reusable fixtures and utilities created
- [ ] Sample tests passing successfully
- [ ] Documentation for testing standards
- [ ] CI/CD-ready test configuration

## Related Skills

- `unit-tests` - Generate comprehensive unit tests (Phase 2)
- `test-cases` - Create integration and E2E tests (Phase 3)
- `mocks-fixtures` - Build test doubles and fixtures (Phase 4)
- `cicd-integration` - Configure test automation (Phase 6)

## Tools by Language

### Python
- **pytest**: Primary test framework
- **pytest-cov**: Coverage reporting
- **pytest-xdist**: Parallel execution
- **pytest-mock**: Mocking integration

### JavaScript/TypeScript
- **Jest**: Primary test framework
- **ts-jest**: TypeScript support
- **@testing-library**: DOM testing utilities

### Java
- **JUnit 5**: Primary test framework
- **Mockito**: Mocking framework
- **JaCoCo**: Coverage reporting

### C#
- **xUnit/NUnit**: Test frameworks
- **Moq**: Mocking framework
- **Coverlet**: Coverage collection

### Go
- **testing**: Built-in package
- **testify**: Assertions and mocking
- **gomock**: Interface mocking

### C/C++
- **Unity/CUnit**: C test frameworks
- **GoogleTest**: C++ test framework
- **CMake/CTest**: Build and test integration

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates tests_generation/test_structure/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
