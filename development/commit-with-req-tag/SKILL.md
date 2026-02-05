---
name: commit-with-req-tag
description: Create final git commit with requirement traceability tags (REQ-*). Use after refactor-phase to finalize TDD cycle with proper requirement linkage for bidirectional traceability.
allowed-tools: [Read, Bash, Grep, Glob]
---

# commit-with-req-tag

**Skill Type**: Actuator (TDD Workflow)
**Purpose**: Create final commit with requirement traceability (REQ-* keys)
**Prerequisites**:
- RED, GREEN, REFACTOR phases complete
- Tests passing
- Code quality verified
- Requirement key (REQ-*) available

---

## Agent Instructions

You are creating the **final commit** for the TDD workflow with requirement traceability.

Your goal is to create a commit that:
1. **Links code to requirements** (forward traceability: REQ-* → code)
2. **Enables reverse lookup** (backward traceability: code → REQ-*)
3. **Provides clear context** for future developers
4. **Follows semantic commit conventions** (feat:, fix:, refactor:, etc.)

---

## Workflow

### Step 1: Gather Commit Information

**Collect details**:
- What requirement(s) were implemented? (REQ-*)
- What business rules were implemented? (BR-*)
- What constraints were implemented? (C-*)
- What files were created/modified?
- How many tests were added?
- What was the test coverage?

**Example**:
```yaml
Requirement: <REQ-ID>
Description: User login with email and password
Business Rules: BR-001, BR-002, BR-003
Files Changed:
  - src/auth/login.py (created, 87 lines)
  - tests/auth/test_login.py (created, 94 lines)
Tests: 5 tests, all passing
Coverage: 95%
```

---

### Step 2: Determine Commit Type

**Use semantic commit prefixes**:

| Prefix | When to Use | Example |
|--------|-------------|---------|
| `feat:` | New functionality (REQ-F-*) | feat: Add user login |
| `fix:` | Bug fix (remediation) | fix: Correct email validation |
| `refactor:` | Code restructuring (REQ-NFR-*) | refactor: Simplify login logic |
| `perf:` | Performance improvement (REQ-NFR-PERF-*) | perf: Optimize password hashing |
| `test:` | Adding/fixing tests | test: Add edge cases for login |
| `docs:` | Documentation only | docs: Update auth API docs |
| `build:` | Build system changes | build: Update dependencies |
| `ci:` | CI/CD changes | ci: Add auth tests to pipeline |

**For most TDD workflows**: Use `feat:` (new feature) or `fix:` (bug fix)

---

### Step 3: Write Commit Message

**Format**:
```
<type>: <subject> (REQ-<KEY>)

<body>

<footer>
```

**Components**:

1. **Subject line** (< 72 chars):
   - Prefix with type (feat:, fix:, etc.)
   - Brief description
   - REQ-* key in parentheses
   - Example: `feat: Add user login (<REQ-ID>)`

2. **Body** (detailed description):
   - What was implemented?
   - Why was it implemented?
   - Business rules/constraints implemented
   - Test coverage summary

3. **Footer** (metadata):
   - Requirement keys
   - Business rule keys
   - Test status
   - Coverage percentage
   - Co-authored-by (for AI pairing)

---

### Step 4: Create Full Commit Message

**Template**:

```
feat: Add user login (<REQ-ID>)

Implement user authentication with email and password validation.
Users can log in with valid credentials and will be locked out after
3 failed attempts for 15 minutes.

Business Rules Implemented:
- BR-001: Email validation (regex pattern)
- BR-002: Password minimum 12 characters
- BR-003: Account lockout after 3 failed attempts (15 minutes)

Implementation:
- Created LoginResult dataclass
- Implemented login() function with validation
- Added email validation helper
- Added lockout tracking per user

Tests:
- 5 tests added, all passing
- Coverage: 95% (38/40 lines)

Files:
- src/auth/login.py (created, 87 lines)
- tests/auth/test_login.py (created, 94 lines)

Implements: <REQ-ID>
Validates: BR-001, BR-002, BR-003
Tests: 5 tests, 100% passing
Coverage: 95%

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### Step 5: Optional - Squash Previous Commits

**If configured** (`squash_commits: true` in plugin config):

```bash
# Squash RED, GREEN, REFACTOR commits into final commit
git reset --soft HEAD~3  # Undo last 3 commits (keeps changes)
git commit -F commit_message.txt
```

**If not squashing**: Keep RED, GREEN, REFACTOR commits separate + final commit.

**Recommendation**: **Keep commits separate** for better git history:
- RED commit shows test-first approach
- GREEN commit shows minimal implementation
- REFACTOR commit shows quality improvements
- Final commit provides summary

---

### Step 6: Create Commit

**Execute git commit**:

```bash
git add .
git commit -m "feat: Add user login (<REQ-ID>)

Implement user authentication with email and password validation.
Users can log in with valid credentials and will be locked out after
3 failed attempts for 15 minutes.

Business Rules Implemented:
- BR-001: Email validation (regex pattern)
- BR-002: Password minimum 12 characters
- BR-003: Account lockout after 3 failed attempts (15 minutes)

Implementation:
- Created LoginResult dataclass
- Implemented login() function with validation
- Added email validation helper
- Added lockout tracking per user

Tests:
- 5 tests added, all passing
- Coverage: 95% (38/40 lines)

Files:
- src/auth/login.py (created, 87 lines)
- tests/auth/test_login.py (created, 94 lines)

Implements: <REQ-ID>
Validates: BR-001, BR-002, BR-003
Tests: 5 tests, 100% passing
Coverage: 95%

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
"
```

---

### Step 7: Verify Commit

**Check commit**:

```bash
git log -1 --stat
```

**Expected output**:
```
commit abc123def456
Author: Developer <dev@example.com>
Date:   Thu Nov 20 22:00:00 2025 +1100

    feat: Add user login (<REQ-ID>)

    Implement user authentication with email and password validation.
    ...

 src/auth/login.py       | 87 ++++++++++++++++++++++++++++++++++++++++++
 tests/auth/test_login.py | 94 ++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 181 insertions(+)
```

---

## Output Format

When you complete the commit, show:

```
[COMMIT Phase - <REQ-ID>]

Commit Type: feat (new feature)

Commit Message:
  Subject: feat: Add user login (<REQ-ID>)
  Body: Implement user authentication with email/password...
  Footer: Implements: <REQ-ID>, Validates: BR-001/002/003

Files Changed:
  + src/auth/login.py (87 lines)
  + tests/auth/test_login.py (94 lines)

Traceability:
  Forward: <REQ-ID> → commit abc123
  Backward: git log --grep="<REQ-ID>" → this commit

Commit SHA: abc123def456

✅ COMMIT Complete!
   Requirement traceability established
   Forward traceability: <REQ-ID> → code
   Backward traceability: code → <REQ-ID>
```

---

## Traceability Benefits

### Forward Traceability (REQ → Code)

**From requirement, find implementation**:
```bash
# Find all commits implementing <REQ-ID>
git log --grep="<REQ-ID>" --oneline

# Find files implementing <REQ-ID>
git log --grep="<REQ-ID>" --name-only
```

### Backward Traceability (Code → REQ)

**From code, find requirement**:
```bash
# Find requirement for src/auth/login.py
git log src/auth/login.py --grep="REQ-" --oneline

# Find business rules in file
grep "Implements: BR-" src/auth/login.py
```

### Impact Analysis

**When requirement changes**:
```bash
# Find all code implementing <REQ-ID>
git log --grep="<REQ-ID>" --name-only | grep -v "^commit" | sort -u

# Output:
# src/auth/login.py
# tests/auth/test_login.py
```

**Now you know exactly what to update!**

---

## Prerequisites Check

Before invoking this skill, ensure:
1. RED, GREEN, REFACTOR phases complete
2. All tests passing
3. Code quality verified (tech debt = 0)
4. Requirement key (REQ-*) available

If prerequisites not met:
- Tests failing → Go back to GREEN phase
- Tech debt detected → Go back to REFACTOR phase
- No REQ-* key → Cannot create commit (need traceability)

---

## Next Steps

After commit created:
1. **Push to remote** (if desired): `git push origin main`
2. **Move to next requirement**: Start new TDD workflow for next REQ-*
3. **Create pull request** (if using PR workflow)

---

## Configuration

This skill respects configuration in `.claude/plugins.yml`:

```yaml
plugins:
  - name: "@aisdlc/code-skills"
    config:
      tdd:
        squash_commits: false      # Keep RED/GREEN/REFACTOR separate
        commit_co_author: true     # Add Claude as co-author
        include_coverage: true     # Include coverage in commit message
        include_test_count: true   # Include test count in commit message
```

---

## Commit Message Examples

### Feature (REQ-F-*)

```
feat: Add password reset (<REQ-ID>)

Implement password reset via email with time-limited tokens.

Business Rules:
- BR-010: Reset token expires after 1 hour
- BR-011: Token usable only once

Implements: <REQ-ID>
Tests: 7 tests, 100% passing
Coverage: 92%
```

### Bug Fix (Remediation)

```
fix: Correct email validation regex (<REQ-ID>)

Fix email validation to reject invalid TLDs.

Issue: Email validation accepted invalid domains like user@example.c
Fix: Updated regex pattern to require minimum 2-char TLD

Fixes: <REQ-ID>, BR-001
Tests: 3 new tests added, all passing
```

### Performance Improvement (REQ-NFR-PERF-*)

```
perf: Optimize password hashing (REQ-NFR-PERF-001)

Switch from MD5 to bcrypt with cost factor 12.

Before: 5ms per hash (insecure)
After: 250ms per hash (secure, prevents brute force)

Implements: REQ-NFR-PERF-001, REQ-NFR-SEC-003
Tests: Performance tests added
```

---

## Notes

**Why requirement traceability?**
- **Compliance**: Regulations require proof of requirements → code mapping
- **Impact analysis**: Know what code to update when requirement changes
- **Audit trail**: Prove all requirements are implemented
- **Debugging**: Trace production issues back to requirements
- **Documentation**: Commits become living documentation

**Bidirectional traceability**:
```
Intent (INT-042)
  ↓ (forward)
Requirements (<REQ-ID>)
  ↓ (forward)
Design (AuthService component)
  ↓ (forward)
Code (src/auth/login.py)
  ↓ (forward)
Tests (tests/auth/test_login.py)
  ↓ (forward)
Runtime (Datadog metrics tagged with <REQ-ID>)
  ↓ (forward)
Alerts ("ERROR: <REQ-ID> - Auth timeout")
  ↑ (backward)
New Intent (INT-150: "Fix auth timeout")
```

**Homeostasis Goal**:
```yaml
desired_state:
  requirement_traceability: complete
  forward_traceability: REQ → code
  backward_traceability: code → REQ
  commit_contains_req_key: true
```

**"Excellence or nothing"** 🔥
