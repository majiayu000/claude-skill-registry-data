---
name: design-with-traceability
description: Create technical solution architecture from requirements with REQ-* traceability. Designs components, APIs, data models, and interactions. Tags all design artifacts with requirement keys. Use after requirements are validated, before coding starts.
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# design-with-traceability

**Skill Type**: Actuator (Design Stage)
**Purpose**: Transform requirements into technical solution architecture
**Prerequisites**: Requirements validated (REQ-*), quality gate passed

---

## Agent Instructions

You are creating **technical solution architecture** from requirements.

Your goal is to design:
1. **Components** (services, modules, classes)
2. **APIs** (endpoints, contracts, protocols)
3. **Data Models** (schemas, entities, relationships)
4. **Interactions** (sequence diagrams, data flows)

**All tagged with REQ-* keys** for traceability.

---

## Workflow

### Step 1: Discover and Review Requirements

**Find all requirement files**:

```bash
# Discover requirements from folder
REQUIREMENTS_DIR="${REQUIREMENTS_DIR:-.ai-workspace/requirements}"
requirements=$(find "$REQUIREMENTS_DIR" -type f \( -name "*.md" -o -name "*.yml" -o -name "*.yaml" \))

echo "Found requirements:"
for req in $requirements; do
  echo "  - $req"
done
```

**Read and understand requirements**:

```markdown
requirements/functional/user-login.md:
  Title: User Login Feature
  Content: User wants to log in with email/password
  Priority: P0

requirements/functional/password-reset.md:
  Title: Password Reset
  Content: User can reset forgotten password via email
  Priority: P1

requirements/non-functional/security.yml:
  encryption: bcrypt
  session: JWT (30min timeout)

requirements/non-functional/performance.yml:
  login_response: <500ms
  db_timeout: 100ms

requirements/business-rules/email-validation.md:
  regex: RFC 5322 compliant
  normalization: lowercase

requirements/business-rules/password-policy.md:
  minimum_length: 12
  max_attempts: 3
  lockout_duration: 15min
```

---

### Step 2: Design Components

**Identify components needed**:

```yaml
# docs/design/authentication-architecture.md

# Implements:
#   - requirements/functional/user-login.md
#   - requirements/functional/password-reset.md
#
# References:
#   - requirements/non-functional/security.yml
#   - requirements/non-functional/performance.yml
#   - requirements/business-rules/email-validation.md
#   - requirements/business-rules/password-policy.md

## Components

### AuthenticationService
**Implements**:
  - requirements/functional/user-login.md
  - requirements/functional/password-reset.md

**Purpose**: Handle user authentication and password management

**Responsibilities**:
- User login (requirements/functional/user-login.md)
- Password reset (requirements/functional/password-reset.md)
- Session management (requirements/non-functional/security.yml)

**Methods**:
- `login(email, password)` → LoginResult
- `request_password_reset(email)` → ResetResult
- `reset_password(token, new_password)` → ResetResult

**Dependencies**:
- EmailValidator (requirements/business-rules/email-validation.md)
- PasswordValidator (requirements/business-rules/password-policy.md)
- LockoutTracker (requirements/business-rules/password-policy.md: lockout)
- PasswordHasher (requirements/non-functional/security.yml: bcrypt)
- SessionManager (requirements/non-functional/security.yml: JWT)

---

### EmailValidator
**Implements**: requirements/business-rules/email-validation.md
**Purpose**: Validate email format and normalization
**Methods**:
- `validate(email)` → bool
- `normalize(email)` → str (lowercase)

---

### PasswordValidator
**Implements**: requirements/business-rules/password-policy.md
**Purpose**: Validate password requirements
**Methods**:
- `validate_length(password)` → bool (minimum 12 chars)
- `validate_complexity(password)` → bool

---

### LockoutTracker
**Implements**: requirements/business-rules/password-policy.md (lockout section)
**Purpose**: Track failed login attempts and manage lockouts
**Methods**:
- `record_failed_attempt(user_id)` → bool (is_locked)
- `is_locked(user_id)` → bool
- `get_remaining_time(user_id)` → int (minutes)
- `reset(user_id)` → void

---

### PasswordHasher
**Implements**: requirements/non-functional/security.yml (encryption)
**Purpose**: Hash and verify passwords using bcrypt
**Methods**:
- `hash(password)` → str
- `verify(password, hash)` → bool

---

### SessionManager
**Implements**: requirements/non-functional/security.yml (session management)
**Purpose**: Manage JWT sessions with 30min timeout
**Methods**:
- `create_session(user_id)` → str (JWT token)
- `validate_session(token)` → bool
- `refresh_session(token)` → str (new token)
```

---

### Step 3: Design APIs

**Define API contracts**:

```yaml
# API Design (tagged with requirement files)

## POST /api/v1/auth/login
**Implements**: requirements/functional/user-login.md

**Request**:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

**Response (Success - 200)**:
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "user_123",
    "email": "user@example.com"
  }
}

**Response (Error - 400)**:
{
  "success": false,
  "error": "Invalid email format"
  # requirements/business-rules/email-validation.md
}

**Response (Error - 401)**:
{
  "success": false,
  "error": "Invalid credentials"
}

**Response (Error - 429)**:
{
  "success": false,
  "error": "Account locked. Try again in 12 minutes"
  # requirements/business-rules/password-policy.md (lockout)
}

**Validation**:
- Email: requirements/business-rules/email-validation.md (regex validation)
- Password: requirements/business-rules/password-policy.md (minimum length)
- Lockout: requirements/business-rules/password-policy.md (3 attempts, 15min)

**Performance**: requirements/non-functional/performance.yml (< 500ms response)

---

## POST /api/v1/auth/password-reset-request
**Implements**: requirements/functional/password-reset.md

**Request**:
{
  "email": "user@example.com"
}

**Response (Success - 200)**:
{
  "success": true,
  "message": "If email exists, reset link sent"
}
```

---

### Step 4: Design Data Models

**Define schemas and entities**:

```yaml
# Data Model Design

## User Entity
**Implements**:
  - requirements/functional/user-login.md
  - requirements/functional/password-reset.md

**Schema**:
{
  "id": "uuid",
  "email": "string (unique, lowercase, max 255)",
  "password_hash": "string (bcrypt hash)",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}

**Constraints**:
- email: UNIQUE index, NOT NULL
- password_hash: NOT NULL (requirements/non-functional/security.yml: bcrypt)

**Requirements Satisfied**:
- requirements/functional/user-login.md: Stores credentials
- requirements/business-rules/email-validation.md: Email unique and normalized
- requirements/non-functional/security.yml: Password hashed with bcrypt

---

## LoginAttempt Entity
**Implements**: requirements/business-rules/password-policy.md (lockout tracking)

**Schema**:
{
  "id": "uuid",
  "user_id": "uuid (foreign key to User)",
  "timestamp": "timestamp",
  "success": "boolean",
  "ip_address": "string"
}

**Indexes**:
- (user_id, timestamp) - For querying recent attempts

**Requirements Satisfied**:
- requirements/business-rules/password-policy.md: Track failed attempts
- requirements/business-rules/password-policy.md: Calculate lockout expiry from timestamps

---

## Session Entity
**Implements**: requirements/non-functional/security.yml (session management)

**Schema**:
{
  "id": "uuid",
  "user_id": "uuid (foreign key to User)",
  "token": "string (JWT)",
  "created_at": "timestamp",
  "expires_at": "timestamp",
  "last_activity": "timestamp"
}

**Constraints**:
- token: UNIQUE
- expires_at: created_at + 30 minutes (requirements/non-functional/security.yml)

**Requirements Satisfied**:
- requirements/non-functional/security.yml: JWT sessions with 30min timeout
```

---

### Step 5: Create Component Diagram

**Visualize architecture**:

```
┌─────────────────────────────────────────────┐
│ Client (Web/Mobile)                         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │ API Layer           │
        │ /api/v1/auth/*      │
        └─────────┬───────────┘
                  │
                  ▼
        ┌──────────────────────────────────────┐
        │ AuthenticationService                │ ← requirements/functional/
        │ - login()                            │    user-login.md,
        │ - request_password_reset()           │    password-reset.md
        │ - reset_password()                   │
        └───┬──────────────────────────────┬───┘
            │                              │
            ▼                              ▼
    ┌───────────────┐             ┌──────────────────┐
    │ Validators    │             │ LockoutTracker   │
    │ - Email       │ ← email-    │                  │ ← password-policy.md
    │ - Password    │   validation │                  │   (lockout)
    └───────────────┘   .md       └──────────────────┘
            │                              │
            ▼                              ▼
        ┌─────────────────────────────────────┐
        │ Database (PostgreSQL)               │
        │ - User table                        │
        │ - LoginAttempt table                │
        │ - Session table                     │
        └─────────────────────────────────────┘

References:
- requirements/non-functional/security.yml: bcrypt, JWT
- requirements/non-functional/performance.yml: <500ms, 100ms DB timeout
- requirements/business-rules/email-validation.md
- requirements/business-rules/password-policy.md
```

---

### Step 6: Tag All Design Artifacts

**Reference requirement files in all design documents**:

```markdown
# .ai-workspace/designs/authentication-architecture.md

# Implements:
#   - .ai-workspace/requirements/functional/user-login.md
#   - .ai-workspace/requirements/functional/password-reset.md
#
# References:
#   - .ai-workspace/requirements/non-functional/security.yml
#   - .ai-workspace/requirements/non-functional/performance.yml
#   - .ai-workspace/requirements/business-rules/email-validation.md
#   - .ai-workspace/requirements/business-rules/password-policy.md

## Architecture Overview

This design implements user authentication and password reset.
```

---

### Step 7: Create Traceability Matrix

**Map requirement files to design components**:

| Requirement File | Component | API | Data Model | Diagram |
|-----------------|-----------|-----|------------|---------|
| requirements/functional/user-login.md | AuthenticationService | POST /auth/login | User, LoginAttempt, Session | Fig 1 |
| requirements/functional/password-reset.md | AuthenticationService | POST /auth/password-reset | User, PasswordResetToken | Fig 1 |
| requirements/business-rules/email-validation.md | EmailValidator | - | - | Fig 2 |
| requirements/business-rules/password-policy.md | PasswordValidator, LockoutTracker | - | LoginAttempt | Fig 2, 3 |

---

### Step 8: Commit Design

```bash
git add .ai-workspace/designs/
git commit -m "DESIGN: Create architecture for authentication

Design technical solution for user authentication and password reset.

Implements:
  - .ai-workspace/requirements/functional/user-login.md
  - .ai-workspace/requirements/functional/password-reset.md

References:
  - .ai-workspace/requirements/non-functional/security.yml
  - .ai-workspace/requirements/non-functional/performance.yml
  - .ai-workspace/requirements/business-rules/email-validation.md
  - .ai-workspace/requirements/business-rules/password-policy.md

Components:
- AuthenticationService (user-login.md, password-reset.md)
- EmailValidator (email-validation.md)
- PasswordValidator (password-policy.md)
- LockoutTracker (password-policy.md: lockout)
- PasswordHasher (security.yml: bcrypt)
- SessionManager (security.yml: JWT)

APIs:
- POST /api/v1/auth/login
- POST /api/v1/auth/password-reset-request
- POST /api/v1/auth/password-reset

Data Models:
- User entity (email, password_hash)
- LoginAttempt entity (lockout tracking)
- Session entity (JWT tokens)

Traceability:
- requirements/functional/user-login.md → AuthenticationService → login()
- requirements/functional/password-reset.md → AuthenticationService → reset()

Design Coverage: 100% (all requirements have design)
"
```

---

## Output Format

```
[DESIGN WITH TRACEABILITY - Authentication]

Requirements Implemented:
  - requirements/functional/user-login.md
  - requirements/functional/password-reset.md

Requirements Referenced:
  - requirements/non-functional/security.yml
  - requirements/non-functional/performance.yml
  - requirements/business-rules/email-validation.md
  - requirements/business-rules/password-policy.md

Design Created:

Components (6):
  ✓ AuthenticationService (user-login.md, password-reset.md)
  ✓ EmailValidator (email-validation.md)
  ✓ PasswordValidator (password-policy.md)
  ✓ LockoutTracker (password-policy.md: lockout)
  ✓ PasswordHasher (security.yml: bcrypt)
  ✓ SessionManager (security.yml: JWT)

APIs (3):
  ✓ POST /api/v1/auth/login (user-login.md)
  ✓ POST /api/v1/auth/password-reset-request (password-reset.md)
  ✓ POST /api/v1/auth/password-reset (password-reset.md)

Data Models (3):
  ✓ User entity (email, password_hash)
  ✓ LoginAttempt entity (lockout tracking)
  ✓ Session entity (JWT tokens)

Diagrams:
  ✓ Component diagram (architecture-overview.png)
  ✓ Sequence diagram (login-flow.png)
  ✓ Data model diagram (authentication-erd.png)

Files Created:
  + .ai-workspace/designs/authentication-architecture.md (287 lines)
  + .ai-workspace/designs/diagrams/authentication-components.png
  + .ai-workspace/designs/api-specs/auth-api.yml (OpenAPI spec)

Traceability:
  ✓ All components reference requirement files
  ✓ All APIs reference requirement files
  ✓ All data models reference requirement files
  ✓ Traceability matrix created

Design Coverage: 100% (2/2 requirements have complete design)

✅ Design Complete!
   Ready for ADRs and implementation
```

---

## Prerequisites Check

Before invoking:
1. Requirements validated and approved
2. Requirements have BR-*, C-*, F-* (from disambiguation)

---

## Notes

**Why design with traceability?**
- **Impact analysis**: Know what design changes when requirements change
- **Complete specification**: Design + requirements = full implementation guide
- **Architecture review**: Stakeholders review tagged design
- **Code generation**: Design provides structure, BR-*/C-*/F-* provide logic

**Homeostasis Goal**:
```yaml
desired_state:
  all_requirements_have_design: true
  all_design_tagged_with_req: true
  design_coverage: 100%
```

**"Excellence or nothing"** 🔥
