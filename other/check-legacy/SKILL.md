---
name: check-legacy
description: Legacy Java code analysis for Spring Boot projects where the code cannot be trusted at face value — method names lie, variables contain unexpected values, transactions have wrong boundaries, and behavior has never been documented. Use this BEFORE modifying any legacy class, before fixing bugs in old code, before refactoring, or when a fix worked locally but broke in production. If the code predates Spring Boot 3.x, has no tests, or has methods longer than 50 lines, always use check-legacy first. Do not skip this in favor of a faster review — legacy code that looks simple is where the worst production bugs hide.
---

# Check Legacy Skill

Zero-trust analysis for legacy Java / Spring Boot code. Assumes nothing. Verifies everything.

## Core Principle

> In legacy code, the contract is what the code **does**, not what it **says**.

Method names, variable names, comments, and javadoc are hints — not specifications. The only truth is the execution path.

---

## Phase 1: Establish the Actual Contract

Before touching anything, document what the code *actually does* vs what it *claims to do*.

### For each class/method under analysis:

```
1. Read the method name and javadoc → write down the implied contract
2. Trace the actual execution path → write down the real behavior
3. Compare: are they the same?
```

**Common legacy lies to check for:**

```java
// "save" that actually updates
public User saveUser(User user) {
    return userRepository.save(user);  // JPA save() = INSERT or UPDATE — which one?
    // If user.id != null → UPDATE. Caller might not know this.
}

// "get" that has side effects
public Order getOrder(Long id) {
    Order order = orderRepository.findById(id).orElseThrow();
    order.setLastAccessed(LocalDateTime.now());  // ← side effect hidden in getter!
    return orderRepository.save(order);
}

// "validate" that also transforms
public void validateRequest(Request req) {
    if (req.getName() == null) req.setName("default");  // ← mutation, not just validation
    if (req.getAmount() < 0) req.setAmount(0);           // ← silent correction
}

// boolean that always returns true
public boolean isValid(String input) {
    try {
        validate(input);
        return true;
    } catch (Exception e) {
        log.error("Validation failed", e);
        return true;  // ← legacy bug: always true
    }
}
```

---

## Phase 2: Variable Trust Audit

In legacy code, variable names drift from their contents over time. Verify each key variable.

### Questions for every significant variable:

```
1. Where is this variable set? (constructor, setter, DB, external call?)
2. Can it be null? Is null handled everywhere it's used?
3. Has its meaning changed across method calls? (reused for different purposes)
4. If it's a collection — can it be empty? Is empty handled differently from null?
5. If it's a numeric ID — can it be 0 or -1? Does any code use those as sentinel values?
```

### Specific patterns to flag:

```java
// Sentinel values masquerading as real IDs
if (userId == 0) {  // ← 0 used as "no user" — but JPA might try to load id=0
    return defaultUser();
}

// Boolean fields used as enums
private boolean active;  // ← actually means: active=true, inactive=false, deleted=... null?
// Check: is there a third state hidden as null?

// Dates that aren't dates
private Date createdAt;  // ← is this UTC? local time? milliseconds epoch? check usages

// String fields with encoded state
private String status;  // ← "A", "I", "D", "P" — undocumented enum in a String
// Search the codebase for all comparisons against this field
```

---

## Phase 3: Transaction Reality Check

Legacy Spring code has the worst transaction problems because they accumulated over years.

### Check every `@Transactional` in the modified area:

```java
// Pattern 1: @Transactional on interface (doesn't work in Spring Boot 3.x)
public interface UserService {
    @Transactional  // ← has no effect — must be on implementation class
    void updateUser(User u);
}

// Pattern 2: self-invocation bypasses proxy
@Service
public class OrderService {
    @Transactional
    public void createOrder(Order o) {
        this.notifyStock(o);  // ← this.x() bypasses Spring proxy — @Transactional on notifyStock is IGNORED
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void notifyStock(Order o) { ... }
}

// Pattern 3: transaction opened too late
@RestController
public class UserController {
    @GetMapping("/{id}")
    public UserDTO getUser(@PathVariable Long id) {
        User user = userService.findById(id);  // transaction closes here
        return mapper.toDTO(user);             // LazyInitializationException if mapper touches lazy fields
    }
}

// Pattern 4: checked exception does NOT rollback by default
@Transactional
public void process() throws BusinessException {
    repo.save(entity);
    if (invalid) throw new BusinessException("error");  // ← does NOT rollback unless rollbackFor specified
}
// Fix: @Transactional(rollbackFor = BusinessException.class)
```

---

## Phase 4: Hidden Coupling Detection

Legacy code often has dependencies that are invisible from the method signature.

### Search for these patterns:

```java
// Static state
public class LegacyConfig {
    public static String currentEnvironment;  // ← global mutable state
}

// ThreadLocal leaks
private static final ThreadLocal<User> currentUser = new ThreadLocal<>();
// ← Is this cleaned up? In virtual threads (Java 21) this behaves differently

// Hardcoded dependencies
@Service
public class ReportService {
    private final String reportPath = "/var/reports";  // ← not configurable, breaks in containers
}

// Event listeners with unexpected ordering
@EventListener
@Order(1)
public void onOrderCreated(OrderCreatedEvent e) {
    // ← Does this depend on another listener having run first?
    // ← What if the event is published inside a transaction that rolls back?
}

// Scheduled tasks interacting with modified code
@Scheduled(fixedDelay = 60000)
public void cleanupExpiredOrders() {
    // ← This runs outside any HTTP context
    // ← SecurityContext is empty here
    // ← If it calls modified methods, does it still work?
}
```

---

## Phase 5: Database Reality Check

Legacy schema rarely matches the entity model perfectly.

```
For any entity touched by the change:
1. Check column nullable in DB vs @Column(nullable=false) in entity — mismatch causes silent failures
2. Check column length in DB vs @Column(length=X) — truncation at DB level, no exception in app
3. Check if there are DB triggers on the table — JPA doesn't know about them
4. Check if there are other applications writing to the same table
5. Check for orphan records that violate FK constraints the code assumes are clean
```

```java
// Common legacy mismatch:
@Column(nullable = false)
private String email;
// But in prod DB: ALTER TABLE users MODIFY email VARCHAR(255) NULL;
// Result: entity says not-null, DB allows null, Hibernate skips the check
```

---

## Output Format

```markdown
## Legacy Analysis: [ClassName / method]

### Contract Drift
| Claimed behavior | Actual behavior | Risk |
|-----------------|----------------|------|
| saveUser() saves a new user | saveUser() inserts OR updates based on ID | HIGH — callers assume insert-only |

### Variable Trust Issues
- `userId`: can be null (from optional query param), but used without null check on line 47
- `status`: String used as enum with undocumented values "A"/"I" — search found 6 different comparison patterns

### Transaction Issues
- Line 23: self-invocation — @Transactional(REQUIRES_NEW) on notifyStock() has no effect
- Line 45: BusinessException does not trigger rollback — @Transactional missing rollbackFor

### Hidden Couplings Found
- Called by ScheduledCleanupTask (runs without SecurityContext) — will fail after auth changes
- Writes to ORDERS table where a DB trigger exists (trigger_audit_orders) — not visible to JPA

### Safe to Modify: [YES / WITH CAUTION / NO]
Reason: [Specific risk that makes modification dangerous]

### Recommended approach before modifying:
1. Add characterization tests (capture current behavior, even if wrong)
2. Fix transaction boundary at line X before making any logic changes
3. Notify team that ScheduledCleanupTask is a caller — needs separate testing
```

---

## Characterization Test Template

When the legacy code has no tests, add characterization tests before changing anything:

```java
/**
 * Characterization test — captures CURRENT behavior, not desired behavior.
 * These tests exist to detect unintended behavior changes during refactoring.
 * If a characterization test fails after a change, it means behavior changed — evaluate if intentional.
 */
@Test
void characterize_saveUser_updatesExistingUser() {
    // Document what the code does TODAY, even if it seems wrong
    User existing = userRepository.save(new User("test@example.com"));
    User request = new User("test@example.com");
    request.setId(existing.getId());

    User result = userService.saveUser(request);

    // This assertion captures current behavior:
    assertThat(result.getId()).isEqualTo(existing.getId());  // UPDATE, not INSERT
}
```
