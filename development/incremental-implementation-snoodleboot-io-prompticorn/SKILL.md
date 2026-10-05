---
name: incremental-implementation
description: Comprehensive guide for implementing code incrementally following established patterns, conventions, and quality standards
languages: [python, typescript, javascript, go, rust, java, csharp, php, ruby]
subagents: [code/feature, code/bug-fix, code/refactor]
tools_needed: [edit, write, read]
---

## Instructions

When implementing features or changes, follow this incremental, quality-focused approach:

### Step 1: Follow Core Conventions Exactly

**Purpose:** Maintain codebase consistency and avoid introducing technical debt.

**How:**
- Read `core-conventions.md` (or equivalent project conventions) before starting
- Check language-specific conventions (Python, TypeScript, etc.)
- Follow established patterns for:
  - Naming (variables, functions, classes, files)
  - Error handling (throw vs return, typed errors)
  - Imports (ordering, absolute vs relative)
  - Testing (framework, coverage, structure)
  - Database (ORM, migrations, queries)

**Why this matters:**
- Inconsistent code confuses maintainers
- Deviations from conventions create review friction
- Following patterns reduces cognitive load when reading code

**Example:**
```python
# ✅ Good - follows Python conventions
def calculate_total_price(items: list[Item]) -> Decimal:
    """Calculate total price including tax."""
    subtotal = sum(item.price for item in items)
    return subtotal * Decimal("1.08")  # 8% tax

# ❌ Bad - violates conventions
def calcTotalPrice(items):  # camelCase (wrong for Python), no types
    sub = 0  # unclear variable name
    for i in items:
        sub = sub + i.price  # verbose when comprehension works
    return sub * 1.08  # magic number, float instead of Decimal
```

---

### Step 2: Match Existing Patterns in the Same Layer

**Purpose:** Keep similar code similar; don't introduce new patterns without reason.

**How:**
1. **Read 2-3 existing files** in the same layer before writing new code
   - Same layer = same part of architecture (e.g., all API routes, all services, all models)
2. **Identify patterns:**
   - How are functions/classes organized?
   - How are dependencies injected?
   - How are errors handled?
   - What naming patterns are used?
3. **Copy patterns, don't invent:**
   - If existing routes use `@router.get("/resource")`, use that
   - If existing services use constructor injection, use that
   - If existing models use `created_at`/`updated_at`, use that

**Why this matters:**
- Consistency makes code easier to navigate
- New patterns increase maintenance burden
- Patterns embody past decisions and domain knowledge

**Example:**

If existing API routes look like this:
```python
# Existing pattern in routes/user_routes.py
@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_model(user)
```

Then new routes should match:
```python
# ✅ Good - matches existing pattern
@router.get("/orders/{order_id}")
async def get_order(
    order_id: str,
    order_service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    order = await order_service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse.from_model(order)

# ❌ Bad - introduces new pattern without justification
@router.route("/orders/<order_id>", methods=["GET"])  # Different decorator style
def get_order_sync(order_id):  # Not async when others are
    service = OrderService()  # Direct instantiation, not dependency injection
    result = service.find(order_id)  # Different method name (find vs get_by_id)
    return jsonify(result)  # Different response pattern
```

---

### Step 3: Add Inline Comments for Non-Obvious Logic

**Purpose:** Explain the WHY, not the WHAT. Help future readers (including yourself) understand intent.

**When to add comments:**
- ✅ **Complex algorithms** - explain the approach
- ✅ **Magic numbers** - explain what they represent
- ✅ **Workarounds** - explain why the workaround is needed
- ✅ **Invariants** - explain assumptions callers must maintain
- ✅ **Performance optimizations** - explain why optimization is needed
- ✅ **External dependencies** - explain API quirks or limitations

**When NOT to add comments:**
- ❌ Restating what the code does (redundant)
- ❌ Explaining obvious standard library functions
- ❌ Translating code to English line-by-line

**Examples:**

```python
# ✅ Good comments (explain WHY)

# Use exponential backoff to avoid overwhelming the API during rate limit recovery
for attempt in range(max_retries):
    delay = 2 ** attempt  # 1s, 2s, 4s, 8s, 16s
    await asyncio.sleep(delay)
    
# 86400 = seconds in a day (cache expires daily at midnight)
cache_ttl = 86400

# Intentionally not awaited - fire and forget analytics event
asyncio.create_task(track_user_action(user_id, "login"))

# WORKAROUND: API returns 200 with error in body instead of 4xx/5xx
# Remove this check when API v2 is deployed (see JIRA-1234)
if response.status == 200 and "error" in response.json():
    raise APIError(response.json()["error"])
```

```python
# ❌ Bad comments (restate code)

# Get user by ID
user = await user_service.get_by_id(user_id)

# Check if user is None
if user is None:
    # Raise 404 error
    raise HTTPException(status_code=404)

# Return user response
return UserResponse.from_model(user)
```

---

### Step 4: Add TODO Comments for Judgment Calls

**Purpose:** Flag decisions that need user review or future attention.

**When to add TODOs:**
- ✅ **Temporary workarounds** - "This will break if X happens"
- ✅ **Incomplete implementations** - "Add validation for edge case Y"
- ✅ **Performance concerns** - "This is O(n²), optimize if dataset grows"
- ✅ **Missing error handling** - "Handle timeout case"
- ✅ **Unclear requirements** - "Confirm with user if this behavior is correct"
- ✅ **Technical debt** - "Refactor to use repository pattern"

**Format:**
```python
# TODO: [Category] Description (Owner, Date)
# TODO: Performance - Cache this query result (Alice, 2026-04-10)
# TODO: Security - Add rate limiting to this endpoint (Bob, 2026-04-10)
# TODO: Validation - Handle case where email is None (Charlie, 2026-04-10)
```

**Categories:**
- `TODO: Incomplete` - Feature not fully implemented
- `TODO: Bug` - Known issue to fix
- `TODO: Performance` - Optimization needed
- `TODO: Security` - Security concern
- `TODO: Refactor` - Code quality improvement
- `TODO: Validation` - Missing input validation
- `TODO: Testing` - Missing test coverage
- `TODO: Documentation` - Missing docs

**Examples:**

```python
def process_payment(amount: Decimal, card_token: str) -> PaymentResult:
    # TODO: Security - Add fraud detection check before processing (Alice, 2026-04-10)
    # TODO: Performance - This calls payment API synchronously; make async (Bob, 2026-04-10)
    
    result = payment_gateway.charge(amount, card_token)
    
    # TODO: Incomplete - Handle gateway timeout (returns None currently) (Charlie, 2026-04-10)
    if result is None:
        return PaymentResult(status="failed", error="Gateway error")
    
    return result
```

---

### Step 5: Implement One File at a Time

**Purpose:** Reduce context switching, make reviews easier, minimize merge conflicts.

**How:**
1. **Complete one file fully** before moving to the next
   - Write the implementation
   - Add inline comments
   - Add TODOs if needed
   - Verify it compiles/passes type checks
2. **Commit frequently** (optional, but recommended)
   - One commit per file or logical change
   - Makes rollback easier if needed
3. **Don't jump between files** during implementation
   - Finish what you started
   - Reduces mental context switching

**Why this matters:**
- **Easier to review:** Reviewers can focus on one file at a time
- **Fewer merge conflicts:** Changes are localized
- **Better focus:** Less context switching improves code quality
- **Easier rollback:** If one file has issues, only that file needs rework

**Anti-pattern:**
```
# ❌ Bad - jumping between files
1. Start implementing user_service.py
2. Realize you need UserRepository, switch to user_repository.py
3. Realize repository needs User model, switch to models.py
4. Go back to user_service.py, half-implement
5. Switch to user_routes.py to add API endpoint
6. Back to user_service.py to finish
```

**Good pattern:**
```
# ✅ Good - one file at a time
1. Implement models.py (User model) - COMPLETE
2. Implement user_repository.py (UserRepository) - COMPLETE
3. Implement user_service.py (UserService) - COMPLETE
4. Implement user_routes.py (API routes) - COMPLETE
5. Implement tests/test_user_service.py - COMPLETE
```

---

## Common Mistakes

### ❌ Mistake 1: Ignoring Existing Patterns

**Problem:** Introducing a new pattern when an existing one works.

**Example:**
```python
# Existing pattern (constructor injection)
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

# ❌ New code introduces different pattern (property injection)
class OrderService:
    @property
    def repo(self) -> OrderRepository:
        return get_repository()  # Global lookup instead of injection
```

**Fix:** Match the existing pattern (constructor injection).

---

### ❌ Mistake 2: Over-Commenting

**Problem:** Commenting what the code already says.

**Example:**
```python
# ❌ Bad
# Loop through items
for item in items:
    # Add item price to total
    total += item.price

# ✅ Good (no comment needed - code is self-explanatory)
for item in items:
    total += item.price

# ✅ Good (comment explains WHY, not WHAT)
# Sum prices excluding items marked as promotional (they're free)
for item in items:
    if not item.is_promotional:
        total += item.price
```

---

### ❌ Mistake 3: Implementing Multiple Files in Parallel

**Problem:** Jumping between files before completing any.

**Why it's bad:**
- Half-finished files are harder to review
- Increases merge conflict risk
- Harder to track progress
- More mental context switching

**Fix:** Finish one file completely before starting the next.

---

### ❌ Mistake 4: Not Reading Existing Code First

**Problem:** Writing code without understanding existing patterns.

**Example:**
- Writing sync code in an async codebase
- Using different error handling than the rest of the codebase
- Naming variables differently than existing conventions

**Fix:** Read 2-3 similar files before writing new code.

---

### ❌ Mistake 5: TODOs Without Context

**Problem:** Writing vague TODOs that don't explain what needs to be done.

**Bad:**
```python
# TODO: fix this
# TODO: improve
# TODO: check
```

**Good:**
```python
# TODO: Performance - Cache this query result to avoid N+1 problem (Alice, 2026-04-10)
# TODO: Security - Add rate limiting to prevent brute force (Bob, 2026-04-10)
# TODO: Validation - Check that email is not already registered (Charlie, 2026-04-10)
```

---

## Examples

### Example 1: Implementing a New Service

**Context:** Adding OrderService to an existing codebase

**Step 1: Read existing services**
```bash
# Read 2-3 existing services to understand patterns
cat services/user_service.py
cat services/product_service.py
cat services/payment_service.py
```

**Step 2: Match pattern**
```python
# ✅ Good - matches existing pattern
class OrderService:
    """Service for managing orders."""
    
    def __init__(self, repo: OrderRepository):
        """Initialize with repository dependency."""
        self.repo = repo
    
    async def create_order(self, user_id: str, items: list[OrderItem]) -> Order:
        """Create new order for user.
        
        Args:
            user_id: ID of user placing order
            items: List of items in order
            
        Returns:
            Created order
            
        Raises:
            ValidationError: If items list is empty
            UserNotFoundError: If user doesn't exist
        """
        if not items:
            raise ValidationError("Order must have at least one item")
        
        # TODO: Validation - Check that all items are in stock (Alice, 2026-04-10)
        
        # Calculate total (excluding promotional items per business rules)
        total = sum(item.price for item in items if not item.is_promotional)
        
        order = Order(
            user_id=user_id,
            items=items,
            total=total,
            status=OrderStatus.PENDING,
        )
        
        return await self.repo.create(order)
```

---

### Example 2: Adding Inline Comments

**Without comments (unclear intent):**
```python
def calculate_discount(price: Decimal, user: User) -> Decimal:
    if user.created_at < datetime.now() - timedelta(days=365):
        return price * Decimal("0.9")
    return price
```

**With good comments (intent is clear):**
```python
def calculate_discount(price: Decimal, user: User) -> Decimal:
    """Apply loyalty discount for long-term users.
    
    Users who joined > 1 year ago get 10% discount as loyalty reward.
    This is a business requirement from Product (see PRD-2024-Q3-05).
    """
    one_year_ago = datetime.now() - timedelta(days=365)
    
    if user.created_at < one_year_ago:
        return price * Decimal("0.9")  # 10% discount
    
    return price
```

---

## Summary

**Key Principles:**
1. **Consistency over cleverness** - Match existing patterns
2. **Explain why, not what** - Comment intent, not implementation
3. **One thing at a time** - Complete files before moving on
4. **Flag uncertainties** - Use TODOs for judgment calls
5. **Read before writing** - Understand context first

**Benefits:**
- Easier code reviews
- Fewer merge conflicts
- Better maintainability
- Higher code quality
- Reduced cognitive load

**Next Steps:**
- After implementing, use `post-implementation-checklist` skill
- Before implementing, use `feature-planning` skill
