---
name: requirement-traceability
description: Provides REQ-* key pattern definitions, validation rules, and traceability operations. Use for understanding requirement key formats, validating keys, or tracing requirements through the SDLC lifecycle.
allowed-tools: [Read, Grep, Glob, Bash]
---

# requirement-traceability

**Skill Type**: Foundation (Knowledge Base)
**Purpose**: Define and validate requirement key patterns for traceability
**Prerequisites**: None (foundation skill)

---

## Agent Instructions

You provide the **foundational knowledge** for requirement traceability in AI SDLC.

Your role is to:
1. **Define** REQ-* key patterns
2. **Validate** requirement keys
3. **Trace** requirements through SDLC stages
4. **Support** other skills with traceability knowledge

---

## Requirement Key Patterns

### REQ-F-* (Functional Requirements)

**Pattern**: `REQ-F-{DOMAIN}-{ID}`

**Examples**:
- `<REQ-ID>` - Authentication functionality
- `<REQ-ID>` - Payment processing
- `REQ-F-PORTAL-001` - Customer portal features

**Naming Rules**:
- DOMAIN: Uppercase, 2-10 chars (AUTH, PAY, PORTAL, USER, ADMIN)
- ID: Zero-padded 3-digit number (001, 002, ..., 999)

**Validation Regex**: `^REQ-F-[A-Z]{2,10}-\d{3}$`

---

### REQ-NFR-* (Non-Functional Requirements)

**Pattern**: `REQ-NFR-{TYPE}-{ID}`

**Types**:
- `PERF` - Performance (response time, throughput)
- `SEC` - Security (authentication, authorization, encryption)
- `SCALE` - Scalability (load handling, horizontal scaling)
- `AVAIL` - Availability (uptime, SLA)
- `MAINT` - Maintainability (code quality, documentation)
- `USABIL` - Usability (UX, accessibility)

**Examples**:
- `REQ-NFR-PERF-001` - Response time < 500ms
- `REQ-NFR-SEC-001` - Password encryption required
- `REQ-NFR-SCALE-001` - Support 10,000 concurrent users

**Validation Regex**: `^REQ-NFR-(PERF|SEC|SCALE|AVAIL|MAINT|USABIL)-\d{3}$`

---

### REQ-DATA-* (Data Quality Requirements)

**Pattern**: `REQ-DATA-{TYPE}-{ID}`

**Types**:
- `CQ` - Completeness (mandatory fields, null handling)
- `AQ` - Accuracy (validation, range checks)
- `CONS` - Consistency (cross-field validation)
- `TIME` - Timeliness (freshness, latency)
- `LIN` - Lineage (provenance, transformation tracking)
- `PII` - Privacy/PII (encryption, masking, GDPR)

**Examples**:
- `REQ-DATA-CQ-001` - Email field mandatory
- `REQ-DATA-AQ-001` - Age between 0 and 150
- `REQ-DATA-PII-001` - Credit card numbers encrypted

**Validation Regex**: `^REQ-DATA-(CQ|AQ|CONS|TIME|LIN|PII)-\d{3}$`

---

### REQ-BR-* (Business Rules)

**Pattern**: `REQ-BR-{DOMAIN}-{ID}`

**Use Cases**:
- Complex business logic requiring separate requirement
- Multi-stage business processes
- Regulatory compliance rules

**Examples**:
- `REQ-BR-REFUND-001` - Refund eligibility rules
- `REQ-BR-DISC-001` - Discount calculation rules
- `REQ-BR-COMP-001` - GDPR compliance rules

**Validation Regex**: `^REQ-BR-[A-Z]{2,10}-\d{3}$`

---

## Subordinate Key Patterns

These are **nested within** requirements for disambiguation:

### BR-* (Business Rules - Nested)

**Pattern**: `BR-{ID}`

**Examples** (nested within <REQ-ID>):
- `BR-001`: Email validation (regex pattern)
- `BR-002`: Password minimum 12 characters
- `BR-003`: Account lockout after 3 attempts

**Use**: Disambiguate vague requirements into specific rules

---

### C-* (Constraints - Nested)

**Pattern**: `C-{ID}`

**Examples** (nested within <REQ-ID>):
- `C-001`: PCI-DSS Level 1 compliance
- `C-002`: Stripe API timeout 10 seconds
- `C-003`: Transaction idempotency required

**Use**: Acknowledge ecosystem E(t) constraints

---

### F-* (Formulas - Nested)

**Pattern**: `F-{ID}`

**Examples** (nested within <REQ-ID>):
- `F-001`: Stripe fee = (amount * 0.029) + 0.30
- `F-002`: Idempotency key = SHA256(merchant_id + timestamp + amount)

**Use**: Define precise calculations for code generation

---

## Traceability Workflow

### Forward Traceability (Intent → Runtime)

**Path**: Intent → Requirements → Design → Code → Tests → Runtime

```
INT-042: "Add user login"
  ↓ (Requirements stage)
<REQ-ID>: User login with email/password
  ↓ (Design stage)
AuthenticationService component
  ↓ (Code stage)
src/auth/login.py:23  # Implements: <REQ-ID>
  ↓ (Test stage)
tests/auth/test_login.py:15  # Validates: <REQ-ID>
  ↓ (Runtime stage)
Datadog metric: auth_success{req="<REQ-ID>"}
```

**Operations**:
```bash
# Find all artifacts for a requirement
git log --all --grep="<REQ-ID>"           # Commits
grep -rn "<REQ-ID>" src/                  # Implementation
grep -rn "<REQ-ID>" tests/                # Tests
grep -rn "<REQ-ID>" docs/requirements/    # Definition
grep -rn "<REQ-ID>" docs/design/          # Design
```

---

### Backward Traceability (Runtime → Intent)

**Path**: Alert → Metric → Code → Requirement → Intent

```
Datadog alert: "ERROR: auth_timeout"
  ↓ (tagged with)
Metric: auth_latency{req="<REQ-ID>"}
  ↓ (find code)
src/auth/login.py:23  # Implements: <REQ-ID>
  ↓ (find requirement)
docs/requirements/auth.md:15  # <REQ-ID>
  ↓ (find original intent)
INT-042: "Add user login"
```

**Operations**:
```bash
# From alert, find requirement
grep "req=" alert.json | grep -o "REQ-[^\"]*"    # Extract REQ key from alert

# From requirement, find original intent
grep -rn "<REQ-ID>" docs/requirements/ | grep "INT-"
```

---

## Validation Functions

### Validate REQ-* Key Format

**Rules**:
1. Must start with `REQ-`
2. Followed by type: `F`, `NFR`, `DATA`, `BR`
3. Followed by domain/type (2-10 uppercase chars)
4. Followed by hyphen and 3-digit ID
5. Total max length: 30 characters

**Valid Examples**:
- ✅ `<REQ-ID>`
- ✅ `REQ-NFR-PERF-001`
- ✅ `REQ-DATA-PII-001`
- ✅ `REQ-BR-REFUND-001`

**Invalid Examples**:
- ❌ `REQ-AUTH-001` (missing type: F/NFR/DATA/BR)
- ❌ `REQ-F-auth-001` (domain must be uppercase)
- ❌ `REQ-F-AUTH-1` (ID must be 3 digits)
- ❌ `REQ-F-A-001` (domain too short, min 2 chars)

---

### Extract REQ-* Keys from Text

**Search patterns**:
```python
import re

def extract_req_keys(text: str) -> list[str]:
    """Extract all REQ-* keys from text"""
    pattern = r'REQ-(F|NFR|DATA|BR)-[A-Z]{2,10}-\d{3}'
    return re.findall(pattern, text)

# Example
text = "Implements: <REQ-ID>, REQ-NFR-SEC-001"
keys = extract_req_keys(text)  # ['<REQ-ID>', 'REQ-NFR-SEC-001']
```

---

## Tagging Conventions

### Code Implementation Tags

**Format**: `# Implements: {REQ-KEY}`

**Examples**:
```python
# Implements: <REQ-ID>
def login(email: str, password: str) -> LoginResult:
    """User login functionality"""
    pass

# Implements: <REQ-ID>, BR-001
def validate_email(email: str) -> bool:
    """Email validation (BR-001)"""
    pass
```

**Multiple implementations**:
```python
# Implements: <REQ-ID>, REQ-NFR-SEC-001
# This function satisfies both authentication and security requirements
def secure_login(email: str, password: str, mfa_token: str) -> LoginResult:
    pass
```

---

### Test Validation Tags

**Format**: `# Validates: {REQ-KEY}`

**Examples**:
```python
# Validates: <REQ-ID>
def test_user_login_with_valid_credentials():
    """Test successful login"""
    result = login("user@example.com", "SecurePass123!")
    assert result.success == True

# Validates: BR-001
def test_email_validation():
    """Test email format validation (BR-001)"""
    assert validate_email("invalid") == False
```

---

### Commit Message Tags

**Format**: Include REQ-* in commit subject or footer

**Examples**:
```
feat: Add user login (<REQ-ID>)

Implements: <REQ-ID>
Validates: BR-001, BR-002, BR-003
```

**Search commits**:
```bash
# Find all commits for a requirement
git log --all --grep="<REQ-ID>"

# Find commits by requirement type
git log --all --grep="REQ-F-"      # All functional requirements
git log --all --grep="REQ-NFR-"    # All non-functional requirements
```

---

### Runtime Telemetry Tags

**Logs**:
```python
logger.info(
    "User login successful",
    extra={"req": "<REQ-ID>", "user_id": user.id}
)
```

**Metrics (Datadog)**:
```python
statsd.increment(
    "auth.login.success",
    tags=["req:<REQ-ID>", "env:production"]
)
```

**Metrics (Prometheus)**:
```python
auth_success_total{req="<REQ-ID>", env="production"}
```

---

## Traceability Matrix

### Structure

| REQ-* | Requirement Doc | Design | Code | Tests | Commits | Runtime |
|-------|----------------|--------|------|-------|---------|---------|
| <REQ-ID> | auth.md:15 | AuthService | login.py:23 | test_login.py:15 | 5 commits | Datadog ✅ |
| REQ-NFR-PERF-001 | perf.md:8 | CacheLayer | cache.py:45 | test_cache.py:22 | 3 commits | Prometheus ✅ |

### Query Operations

**Find coverage gaps**:
```bash
# Requirements with no code
grep -rh "^## REQ-" docs/requirements/ | \
  while read req; do
    grep -q "$req" src/ || echo "$req - NO CODE"
  done

# Requirements with no tests
grep -rh "^## REQ-" docs/requirements/ | \
  while read req; do
    grep -q "$req" tests/ || echo "$req - NO TESTS"
  done
```

---

## Usage in Other Skills

### In TDD Workflow

```python
# tdd-workflow skill uses requirement-traceability to:
1. Validate REQ-* key format
2. Extract REQ-* from user intent
3. Tag code with "# Implements: REQ-*"
4. Tag tests with "# Validates: REQ-*"
5. Include REQ-* in commit messages
```

### In Coverage Detection

```python
# check-requirement-coverage skill uses requirement-traceability to:
1. Find all REQ-* keys in requirements docs
2. Search for "# Implements: REQ-*" in src/
3. Search for "# Validates: REQ-*" in tests/
4. Report requirements without coverage
```

### In Code Generation

```python
# autogenerate-from-business-rules skill uses requirement-traceability to:
1. Extract BR-*, C-*, F-* from REQ-*
2. Tag generated code with REQ-* and BR-*
3. Generate tests tagged with "# Validates: BR-*"
```

---

## Configuration

Access via plugin configuration:

```yaml
plugins:
  - name: "@aisdlc/aisdlc-core"
    config:
      req_key_patterns:
        functional: "REQ-F-{DOMAIN}-{ID}"
        non_functional: "REQ-NFR-{DOMAIN}-{ID}"
        data_quality: "REQ-DATA-{DOMAIN}-{ID}"
        business_rule: "REQ-BR-{DOMAIN}-{ID}"

      coverage:
        minimum_percentage: 80
        require_req_tags: true

      propagation:
        auto_propagate_on_commit: true
        tag_format: "# Implements: {REQ-KEY}"
        test_tag_format: "# Validates: {REQ-KEY}"
```

---

## Traceability Operations

### Operation 1: Trace Forward (REQ → Artifacts)

**Input**: `<REQ-ID>`

**Output**:
```
<REQ-ID>: User login with email/password
│
├─ 📋 Requirements
│   └─ docs/requirements/authentication.md:15
│
├─ 🎨 Design
│   ├─ docs/design/auth-service.md:42
│   └─ docs/adrs/ADR-003-auth-approach.md:10
│
├─ 💻 Implementation
│   ├─ src/auth/login.py:23  # Implements: <REQ-ID>
│   ├─ src/auth/validators.py:67  # Implements: <REQ-ID>, BR-001
│   └─ src/auth/lockout.py:34  # Implements: <REQ-ID>, BR-003
│
├─ ✅ Tests
│   ├─ tests/auth/test_login.py:15  # Validates: <REQ-ID>
│   ├─ tests/auth/test_validators.py:22  # Validates: BR-001
│   └─ features/authentication.feature:5  # Validates: <REQ-ID>
│
├─ 📦 Commits
│   ├─ abc123 "feat: Add user login (<REQ-ID>)"
│   ├─ def456 "fix: Correct email validation (<REQ-ID>, BR-001)"
│   └─ ghi789 "perf: Optimize login query (<REQ-ID>)"
│
└─ 🚀 Runtime
    ├─ Logs: logger.info("Login", extra={"req": "<REQ-ID>"})
    ├─ Metrics: auth_success{req="<REQ-ID>"}
    └─ Alerts: "ERROR: <REQ-ID> - Auth timeout"

Coverage: ✅ Full traceability
```

**Implementation**:
```bash
# Grep across all files
grep -rn "<REQ-ID>" docs/ src/ tests/ features/

# Git log
git log --all --grep="<REQ-ID>" --name-only
```

---

### Operation 2: Trace Backward (Code → REQ)

**Input**: `src/auth/login.py`

**Output**:
```
src/auth/login.py implements:
├─ <REQ-ID> (line 23)
├─ REQ-NFR-SEC-001 (line 45)
└─ REQ-NFR-PERF-001 (line 89)

Tracing to requirements:
├─ <REQ-ID> → docs/requirements/authentication.md:15
│   └─ Intent: INT-042 "Add user login"
│
├─ REQ-NFR-SEC-001 → docs/requirements/security.md:8
│   └─ Intent: INT-043 "Secure authentication"
│
└─ REQ-NFR-PERF-001 → docs/requirements/performance.md:12
    └─ Intent: INT-050 "Optimize login performance"
```

**Implementation**:
```bash
# Extract REQ-* from file
grep "# Implements:" src/auth/login.py | grep -o "REQ-[^ ,]*"

# Find requirement definitions
for req in $(grep "# Implements:" src/auth/login.py | grep -o "REQ-[^ ,]*"); do
  grep -rn "^## $req" docs/requirements/
done
```

---

### Operation 3: Coverage Report

**Input**: All requirements

**Output**:
```
Requirement Coverage Report
═══════════════════════════════════════════

Total Requirements: 42

By Type:
├─ REQ-F-*    : 28 (Functional)
├─ REQ-NFR-*  : 8  (Non-Functional)
├─ REQ-DATA-* : 4  (Data Quality)
└─ REQ-BR-*   : 2  (Business Rules)

Coverage by Stage:
├─ Requirements → Design: 100% (42/42) ✅
├─ Design → Code: 86% (36/42) ⚠️
├─ Code → Tests: 100% (36/36) ✅
├─ Tests → Runtime: 25% (9/36) ⚠️

Requirements Without Code (6):
├─ REQ-F-PROFILE-001 - User profile editing
├─ REQ-F-PROFILE-002 - Avatar upload
├─ REQ-F-NOTIF-001 - Email notifications
├─ REQ-F-NOTIF-002 - Push notifications
├─ REQ-NFR-PERF-002 - Database query optimization
└─ REQ-DATA-LIN-001 - Data lineage tracking

Requirements Without Runtime Telemetry (27):
├─ <REQ-ID> (has code, no metrics)
├─ REQ-F-AUTH-003 (has code, no metrics)
├─ ... (25 more)

Recommendations:
1. Implement 6 requirements missing code
2. Add telemetry tags to 27 requirements
```

---

## Homeostasis Support

### Sensor Skills Use This Skill To:
- Validate REQ-* key format
- Extract REQ-* from files
- Check coverage gaps

### Actuator Skills Use This Skill To:
- Tag code with correct format
- Create properly formatted commit messages
- Generate traceability reports

---

## Output Format

When invoked for validation:

```
[REQUIREMENT TRACEABILITY]

Validating: <REQ-ID>

Format Check:
  ✓ Starts with "REQ-"
  ✓ Type: F (Functional)
  ✓ Domain: AUTH (valid, 4 chars)
  ✓ ID: 001 (valid, 3 digits)

Result: ✅ VALID

Pattern: REQ-F-{DOMAIN}-{ID}
Regex: ^REQ-F-[A-Z]{2,10}-\d{3}$
```

When invoked for tracing:

```
[TRACE: <REQ-ID>]

Forward Traceability:
  ✅ Requirements: docs/requirements/auth.md:15
  ✅ Design: docs/design/auth-service.md:42
  ✅ Code: src/auth/login.py:23 (+ 2 more files)
  ✅ Tests: tests/auth/test_login.py:15 (+ 1 more files)
  ✅ Commits: 5 commits found
  ⚠️ Runtime: No telemetry tags (needs setup)

Coverage: 83% (5/6 stages)
Missing: Runtime telemetry
```

---

## Notes

**Why requirement traceability?**
- **Compliance**: Regulations require proof of implementation
- **Impact Analysis**: Know what to change when requirement updates
- **Debugging**: Trace production issues back to requirements
- **Audit Trail**: Prove all requirements are implemented
- **Living Documentation**: Code comments link to requirements

**Key Principles**:
- REQ-* keys are **immutable** (content can evolve, keys never change)
- REQ-* keys are **unique** (no duplicates)
- REQ-* keys are **human-readable** (domain + sequential ID)
- REQ-* keys are **everywhere** (requirements → code → tests → runtime)

**Homeostasis Goal**:
```yaml
desired_state:
  all_requirements_have_unique_keys: true
  all_keys_follow_pattern: true
  all_artifacts_tagged: true
  full_traceability: true
```

**"Excellence or nothing"** 🔥
