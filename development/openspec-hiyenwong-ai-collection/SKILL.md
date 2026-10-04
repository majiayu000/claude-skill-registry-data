---
name: openspec
description: Specification-driven development framework using Gherkin syntax. Use when user mentions openspec, open spec, spec-driven, gherkin, BDD, given-when-then, or needs to define requirements in structured human-readable format.
---

# OpenSpec

## Description
A lightweight specification-driven framework that helps define requirements in structured, human-readable format and track changes through spec deltas using Gherkin syntax. Bridges the gap between business requirements and implementation.

## Activation Keywords
- openspec
- open spec
- spec-driven
- specification
- gherkin
- scenario
- requirement
- bdd
- given when then
- spec delta

## Tools Used
- read: Read OpenSpec files
- write: Write and update OpenSpec files
- edit: Edit spec deltas
- memory: Store specifications for reference

## Installation

### Install OpenSpec CLI
```bash
npm install -g openspec
```

Or via project:
```bash
cd /path/to/project
npm install --save-dev openspec
```

### Verify Installation
```bash
openspec --version
```

### Initialize Project
```bash
# Create spec directory structure
openspec init

# Or create manually
mkdir -p openspec/{core,features}
touch openspec/README.md
```

## Usage Patterns

### Creating a New Spec

**Basic spec:**
```gherkin
### Requirement: User registration
The system SHALL allow users to register with email and password.

#### Scenario: Successful registration
GIVEN a new user with valid email "user@example.com" and password "SecurePass123"
WHEN the user submits registration form
THEN a new user account is created
AND a verification email is sent
AND the user is redirected to verification page

#### Scenario: Duplicate email
GIVEN a user with email "existing@example.com" already exists
WHEN a new user tries to register with same email
THEN registration fails
AND an error message "Email already registered" is displayed
```

**Spec delta (tracking changes):**
```gherkin
### Requirement: User authentication
- The system SHALL authenticate users with email and password.
+ The system SHALL authenticate users with email and password OR social login.

#### Scenario: Successful email login
GIVEN a registered user with email "user@example.com" and password "correct"
WHEN the user submits login credentials
THEN the user is authenticated
- AND the token expires in 1 hour
+ AND the token expires in 24 hours if "Remember me" is checked

+ #### Scenario: Social login
+ - GIVEN a user chooses to login with Google
+ - WHEN Google authentication is completed successfully
+ - THEN the user is authenticated
+ - AND a JWT token is returned
+ - AND token expires in 24 hours
```

### Using OpenSpec with AI Coding Agents

**With OpenCode:**
```
Implement the following OpenSpec requirements ultrawork:

### Requirement: User authentication
The system SHALL authenticate users with email and password.

#### Scenario: Successful login
GIVEN a registered user with email "user@example.com" and password "password123"
WHEN the user submits login credentials
THEN the user is authenticated
AND a JWT token is returned
AND the token expires in 1 hour
```

**With Claude Code:**
```
Implement the OpenSpec requirements in openspec/auth.spec.md. Create the necessary controllers, models, and tests.
```

### Generating Tests from Specs

**Create test files:**
```
Generate Jest test suites from the OpenSpec scenarios in openspec/core/auth.spec.md
```

**Use scenarios as test cases:**
```javascript
describe('User Authentication', () => {
  test('Successful login', () => {
    // GIVEN a registered user
    const user = { email: 'user@example.com', password: 'password123' }
    // WHEN the user submits login
    const result = authenticate(user)
    // THEN the user is authenticated
    expect(result.token).toBeDefined()
  })
})
```

### Code Review with Spec Deltas

**Reviewer perspective:**
```
Here's the spec delta:
- Old requirement: Token expires in 1 hour
+ New requirement: Token expires in 24 hours

Review the code changes against this delta. Does the implementation match?
```

## Instructions for Agents

When user mentions OpenSpec or specifications:

### 1. Read Existing Specs
Check for existing specifications:
```bash
# Find spec files
find openspec -name "*.spec.md"

# Read specific spec
read openspec/core/auth.spec.md
```

### 2. Understand Spec Syntax
OpenSpec uses Gherkin syntax:

**Requirement:**
```gherkin
### Requirement: [Name]
The system SHALL [requirement description].

SHALL for mandatory, MAY for optional.
```

**Scenario:**
```gherkin
#### Scenario: [Name]
GIVEN [initial state]
WHEN [action occurs]
THEN [expected outcome]
AND [additional outcome]
```

**Spec Delta:**
```gherkin
- Removed line (with - prefix)
+ Added line (with + prefix)
```

### 3. Create New Specs
When creating specifications:
1. Use clear requirement names
2. Write complete scenarios (GIVEN-WHEN-THEN)
3. Cover happy path, edge cases, errors
4. Make scenarios testable
5. Use SHALL for mandatory requirements

### 4. Update Specs with Deltas
When requirements change:
1. Identify what changed
2. Use `-` for removed items
3. Use `+` for added items
4. Keep both for comparison
5. Commit deltas to version control

### 5. Implement from Specs
When implementing:
1. Read the spec file
2. Break down by requirements
3. Implement each scenario
4. Create tests matching scenarios
5. Verify against spec deltas

### 6. Generate Tests
Convert scenarios to tests:
- Each GIVEN = test setup
- Each WHEN = test action
- Each THEN = test assertion

## Context Files

OpenSpec uses these context files:

### openspec/README.md
Overview of specification structure

### openspec/core/
Core system specifications (auth, users, etc.)

### openspec/features/
Feature specifications (dashboard, reports, etc.)

## Configuration

### Project Structure
```
project/
├── openspec/
│   ├── core/
│   │   ├── auth.spec.md
│   │   ├── users.spec.md
│   │   └── sessions.spec.md
│   ├── features/
│   │   ├── dashboard.spec.md
│   │   └── reports.spec.md
│   └── README.md
├── src/
├── tests/
└── package.json
```

### Spec Template
```markdown
# Feature: [Feature Name]

## Requirements

### Requirement: [Requirement Name]
The system SHALL [requirement description].

#### Scenario: [Scenario Name]
GIVEN [initial state]
WHEN [action occurs]
THEN [expected outcome]
AND [additional outcomes]

### Requirement: Another requirement
...
```

## Advanced Features

### Spec Validation
```
Validate that all tests in the test suite correspond to scenarios in the OpenSpec files. Report any missing or extra test cases.
```

### Spec Coverage
```
Calculate spec coverage: percentage of OpenSpec scenarios that have corresponding tests passing.
```

### Spec-Driven Refactoring
```
Analyze the codebase against openspec/ requirements. Identify areas where implementation doesn't match spec and suggest fixes.
```

## Common Patterns

### Authentication Spec
```gherkin
### Requirement: User authentication
The system SHALL authenticate users with email and password.

#### Scenario: Successful login
GIVEN a registered user with valid credentials
WHEN the user submits login
THEN authentication succeeds
AND a JWT token is returned

#### Scenario: Wrong password
GIVEN a registered user
WHEN the user submits wrong password
THEN authentication fails
AND an error is returned
```

### API Endpoint Spec
```gherkin
### Requirement: Get user profile
The system SHALL provide user profile data via API.

#### Scenario: Get own profile
GIVEN an authenticated user
WHEN the user requests /api/users/me
THEN user profile data is returned
AND status code is 200

#### Scenario: Unauthorized access
GIVEN an unauthenticated request
WHEN requesting /api/users/me
THEN status code is 401
AND error message is returned
```

### Data Validation Spec
```gherkin
### Requirement: Email validation
The system SHALL validate email addresses during registration.

#### Scenario: Valid email
GIVEN a user provides "user@example.com"
WHEN submitting registration
THEN email is accepted

#### Scenario: Invalid email
GIVEN a user provides "invalid-email"
WHEN submitting registration
THEN registration fails
AND "Invalid email" error is shown
```

## Error Handling

### Invalid Spec Syntax
```
If spec has syntax errors:
  1. Check each scenario has GIVEN-WHEN-THEN
  2. Verify proper indentation
  3. Ensure requirement descriptions are clear
  4. Use spec validation tool: openspec validate
```

### Missing Scenarios
```
If implementation doesn't match spec:
  1. Compare implementation against spec scenarios
  2. Identify missing functionality
  3. Add missing scenarios or update implementation
  4. Re-run tests
```

### Conflicting Deltas
```
If spec deltas have conflicts:
  1. Review the changes (- and + lines)
  2. Resolve conflicts by choosing correct state
  3. Update spec without conflicting lines
  4. Clear the delta once resolved
```

## Best Practices

### 1. Write Testable Scenarios
Each scenario should be:
- Specific and clear
- Testable via automation
- Independent of other scenarios
- Focused on single behavior

### 2. Use SHALL/MAY Correctly
- **SHALL:** Mandatory requirement
- **MAY:** Optional feature
- **SHALL NOT:** Forbidden behavior

### 3. Cover All Cases
For each requirement, cover:
- Happy path (success case)
- Edge cases (boundary conditions)
- Error cases (failure modes)

### 4. Keep Deltas Clean
- Clear deltas after implementation
- Use version control to track changes
- Document why changes were made

### 5. Use with AI Agents
- Provide specs as input to agents
- Use spec deltas to track changes
- Generate tests from scenarios
- Review code against specs

## Examples

### Example 1: Initial Spec
```gherkin
### Requirement: User registration
The system SHALL allow users to register with email and password.

#### Scenario: Successful registration
GIVEN a new user with valid email and password
WHEN the user submits registration
THEN account is created
AND verification email is sent
```

### Example 2: Spec Delta
```gherkin
### Requirement: User registration
The system SHALL allow users to register with email and password.
+ The system SHALL support optional phone number.

#### Scenario: Successful registration
GIVEN a new user with valid email and password
- WHEN the user submits registration
+ WHEN the user submits registration with optional phone number
THEN account is created
AND verification email is sent
```

### Example 3: Implementation Request
```
User: "Implement the OpenSpec spec for user authentication"

Agent:
1. Reads openspec/core/auth.spec.md
2. Identifies requirements and scenarios
3. Creates auth controller
4. Implements login endpoint
5. Adds validation
6. Creates tests for each scenario
7. Runs tests
8. Reports completion
```

## Limitations

- Doesn't generate code automatically (requires AI agent)
- Needs discipline to keep specs updated
- Can be verbose for simple features
- Learning curve for Gherkin syntax

## Resources

- **OpenSpec Website:** https://openspec.dev/
- **Gherkin Syntax:** https://cucumber.io/docs/gherkin/reference/
- **BDD Best Practices:** https://cucumber.io/docs/bdd/

## Related Skills
- **opencode:** OpenSpec integration for implementation
- **claude-code:** Can implement OpenSpec specs
- **obsidian:** For storing and organizing specs
- **reference workflow:** See `references/implementation-workflow.md` for a detailed manual implementation pipeline when AI coding agents are unavailable

## Notes

- OpenSpec is particularly effective when paired with AI coding agents
- The spec delta format makes changes easy to review
- Gherkin syntax is familiar to many developers and BDD practitioners
- Specs can live alongside code as documentation
- Perfect for TDD/BDD workflows
