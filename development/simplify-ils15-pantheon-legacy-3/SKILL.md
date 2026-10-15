---
name: simplify
description: "Behavior-preserving code simplification to reduce complexity while keeping outputs, side effects, and APIs unchanged."
context: fork
globs: []
alwaysApply: false
---

# Simplify Skill

Behavior-preserving code simplification. Reduce complexity, eliminate noise, and improve readability without changing what the code does.

---

## When to load this skill

Load when asked to:
- "Simplify this function/module"
- "Reduce complexity without changing behavior"
- "Clean up this code"
- "Refactor for readability"
- "Remove dead code / unused paths"

---

## Core Rule: Behavior Is Invariant

Every simplification MUST preserve observable behavior:
- Same inputs → same outputs
- Same side effects
- Same error conditions
- Same public API surface

If a simplification changes behavior, it is a bug, not a simplification.

---

## Simplification Checklist

Work through these categories in order. Stop at any category where a change risks behavior — flag it and ask before proceeding.

### 1. Dead Code Removal (zero-risk)
- [ ] Remove imports that are never used
- [ ] Remove variables assigned but never read
- [ ] Remove functions/methods never called (verify with usages search)
- [ ] Remove commented-out code blocks older than the last commit
- [ ] Remove `pass` statements in non-empty bodies

**Verification**: Run existing tests. If they pass, the removal was safe.

### 2. Redundancy Elimination (low-risk)
- [ ] Replace repeated literals with a named constant
- [ ] Collapse duplicate conditional branches with identical bodies
- [ ] Merge nested `if` chains into a single compound condition where intent is clearer
- [ ] Remove double negations (`not not x` → `bool(x)` or just `x` where truthy is enough)
- [ ] Replace `if x == True:` with `if x:` and `if x == False:` with `if not x:`

### 3. Standard Library Substitution (medium-risk — test after each)
- [ ] Replace manual loop patterns with built-ins (`any()`, `all()`, `sum()`, `min()`, `max()`)
- [ ] Replace `dict.get(key, None)` with `dict.get(key)` (same default)
- [ ] Replace string concatenation in loops with `"".join()`
- [ ] Replace manual null-checks on dict access with `dict.get()`
- [ ] Replace `len(x) == 0` with `not x` (only for types where falsy = empty)

### 4. Structural Flattening (higher-risk — require test coverage before touching)
- [ ] Extract repeated logic into a helper function (only if used 3+ times)
- [ ] Flatten deeply nested callbacks/try-except into early returns
- [ ] Convert `if/elif/elif/else` chains that are purely data into a lookup dict
- [ ] Break functions longer than ~50 lines into focused sub-functions

### 5. Naming Clarity (cosmetic — no behavior risk)
- [ ] Rename single-letter variables to descriptive names (except loop indices `i`, `j`, `k`)
- [ ] Rename boolean variables to `is_`, `has_`, `can_`, `should_` prefix
- [ ] Rename functions whose name contradicts what they do

---

## Process

```
1. Read the target file(s)
2. Run existing tests to establish a green baseline
   → If no tests exist: STOP and report — simplifying untested code is risky
3. Work through checklist categories 1 → 5
4. After each category: run tests again
5. If a test fails: revert the last change, flag it as unsafe, continue with next item
6. Report: what was simplified, what was skipped and why
```

---

## Output Format

```
## Simplification Report: <file>

### Applied
- Removed 3 unused imports (F401)
- Collapsed duplicate if-branch in `process_order()` (lines 45-60)
- Replaced manual loop sum with `sum()` in `calculate_total()`

### Skipped (behavior risk)
- `legacy_path()` — called from 2 external modules not in this repo; cannot verify safely
- Nested try-except in `parse_config()` — unclear if all error paths are covered by tests

### Test Results
- Before: 47 tests passing
- After: 47 tests passing (0 regressions)

### Lines changed: 312 → 247 (-21%)
```

---

## Anti-Patterns to Avoid

| Temptation | Why to avoid |
|---|---|
| "This logic can be a one-liner" | One-liners can obscure intent — only collapse if clarity improves |
| "This variable is obvious from context" | Removing names makes debugging harder; keep them |
| "Dead code — just delete it" | Always verify with `search/usages` first; it may be called via reflection |
| "The tests are slow, I'll skip them" | You have no evidence the simplification is safe without tests |
| "I'll simplify and add new behavior at the same time" | Never mix simplification with feature changes in one step |

---

## Integration Notes

- **Agents that use this skill**: Hermes (backend cleanup), Aphrodite (frontend cleanup), Talos (fast cleanup), Themis (refactor suggestions in review)
- **Always pair with**: existing test suite. No tests = no simplification.
- **Scope**: one file or one function at a time. Don't batch-simplify across many files in one pass.

---

## Appendix: AI Slop Detection

Use this section to detect and eliminate AI-generated code smells from files while preserving functionality.

### The Core Principle

> **Code should read like a senior wrote it, not an AI.**

AI-generated code tends to over-explain, over-handle, and over-engineer. These patterns catch those issues and guide you to replace them with clean, concise alternatives.

### AI Slop Patterns to Detect

#### 1. Verbose Comments ❌

Comments that explain what the code already says:

```python
# ❌ AI Slop
# This function hashes the user's password using bcrypt
# and returns the hashed password for storage in the database
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# ✅ Clean
def hash_password(password: str) -> str:
    """Hash password with bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

#### 2. Redundant Error Handling Comments ❌

Comments that describe obvious error paths:

```python
# ❌ AI Slop
# Try to fetch the user from the database
# If the user is not found, raise a 404 error
# If there is a database error, raise a 500 error
async def get_user(user_id: str):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404)

# ✅ Clean
async def get_user(user_id: str):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
```

#### 3. AI Filler Phrases ❌

Generic phrases that add no value:

```python
# ❌ AI Slop
# In this implementation, we handle the user authentication
# by checking the provided credentials against the database
# and returning a JWT token if successful

# ✅ Clean
# Authenticate user and return JWT token.
```

#### 4. Over-Engineered Patterns ❌

Unnecessary abstraction for simple tasks:

```python
# ❌ AI Slop — Factory pattern for a simple dict
class UserResponseFactory:
    @staticmethod
    def create(user: User) -> dict:
        return {"id": user.id, "email": user.email}

# ✅ Clean — Just a function
def user_response(user: User) -> dict:
    return {"id": user.id, "email": user.email}
```

#### 5. Self-Congratulatory Comments ❌

Comments that praise the implementation:

```python
# ❌ AI Slop
# This robust implementation ensures secure password handling
# with industry-standard bcrypt hashing

# ✅ Clean
# Bcrypt password hashing.
```

### Detection Rules

#### Comment Analysis

A comment is flagged as AI slop if it matches ANY of these patterns:

| Pattern | Example | Severity |
|---------|---------|----------|
| Starts with "This function/method/class" | "This function handles..." | High |
| Explains what code already says | "Check if user exists" before `if user:` | High |
| Uses "In this implementation" | "In this implementation, we..." | High |
| Uses "robust/comprehensive/elegant" | "This robust solution..." | Medium |
| Multi-line explanation of simple code | 3+ lines explaining 1-line code | Medium |
| Repeats function name in comment | "hash_password: hashes the password" | Low |

#### Code Analysis

Code is flagged as over-engineered if:

| Pattern | Example | Severity |
|---------|---------|----------|
| Factory/Builder for simple data | Factory class for dict creation | High |
| Abstract base class for single impl | ABC with one subclass | Medium |
| Strategy pattern for 2 options | Strategy class for if/else | Medium |
| Decorator for single-use logic | Decorator used once | Low |

### Replacement Guidelines

When AI slop is detected, replace with:

| AI Slop | Replace With |
|---------|-------------|
| "This function does X" | Docstring: `"""Do X."""` |
| Multi-line explanation | Single-line comment or docstring |
| "In this implementation..." | Remove entirely |
| Self-congratulatory language | Remove entirely |
| Redundant error comments | Keep only non-obvious context |

### Examples: Before and After

#### Before (AI Slop):
```python
# This class provides a comprehensive user management service
# that handles all CRUD operations for the User model
# with proper error handling and validation
class UserService:
    """User service for CRUD operations."""

    def __init__(self, db: AsyncSession):
        # Initialize the service with a database session
        # This allows us to perform database operations
        self.db = db

    async def create_user(self, email: str, password: str) -> User:
        # Create a new user with the provided email and password
        # First, we hash the password for security
        # Then, we create the user object and save it to the database
        # Finally, we return the created user
        hashed_pw = hash_password(password)
        user = User(email=email, password=hashed_pw)
        self.db.add(user)
        await self.db.flush()
        return user
```

#### After (Clean):
```python
class UserService:
    """User CRUD operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, email: str, password: str) -> User:
        """Create user with hashed password."""
        user = User(email=email, password=hash_password(password))
        self.db.add(user)
        await self.db.flush()
        return user
```

**Lines reduced:** 18 → 9 (50% reduction)
**Readability:** Significantly improved
