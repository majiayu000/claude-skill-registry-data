---
name: strategic-comments
description: Add high-value comments explaining complex logic, business rules, design decisions, and non-obvious implementations. Use when clarifying code intent.
---

# Strategic Comments

Add meaningful comments that explain "why" not "what" - focusing on business logic, design decisions, non-obvious implementations, and technical debt.

## When to Use This Skill

Use this skill when you need to:

- Explain complex algorithms
- Document business rules
- Clarify design decisions
- Document workarounds and technical debt
- Add context that code alone cannot convey
- Mark areas for future improvement

**Trigger phrases**: "add comments", "explain code", "document why", "add TODO", "clarify logic", "document workaround"

## What This Skill Does

### Comment Categories

1. **Explanatory Comments** - Why the code exists
2. **Business Logic Comments** - Domain rules and requirements
3. **Decision Comments** - Why this approach was chosen
4. **Warning Comments** - Gotchas and edge cases
5. **Technical Debt Comments** - TODO, FIXME, HACK markers

## Instructions

### When to Comment

Comment when code alone cannot convey:

```python
# GOOD: Explains WHY
# Use binary search here because the list is always sorted
# by the data loader and can contain 100K+ items
index = bisect.bisect_left(sorted_items, target)

# BAD: Explains WHAT (obvious from code)
# Increment counter by 1
counter += 1
```

### Business Logic Comments

```python
def calculate_discount(order):
    # Business Rule: Orders over $100 get 10% discount,
    # but this doesn't stack with loyalty discounts.
    # See: JIRA-1234 for the original requirement.
    if order.total > 100 and not order.has_loyalty_discount:
        return order.total * 0.10
    return 0


def validate_transaction(transaction):
    # Regulatory Requirement (PCI-DSS 3.4):
    # Card numbers must be masked in logs and displays.
    # Only last 4 digits may be shown.
    masked = transaction.card_number[-4:].rjust(16, '*')
```

### Design Decision Comments

```python
# Design Decision: We use a LRU cache here instead of Redis because:
# 1. Data is request-scoped and doesn't need persistence
# 2. Latency requirements are <1ms (Redis adds 2-5ms)
# 3. Memory footprint is small (<10MB per instance)
# Revisit if we need cross-instance caching.
@lru_cache(maxsize=1000)
def get_user_preferences(user_id):
    pass


# Architecture Note: This service uses eventual consistency.
# Reads may return stale data for up to 5 seconds after writes.
# This is acceptable per product requirements (see ADR-007).
class UserProfileService:
    pass
```

### Algorithm Comments

```python
def find_optimal_path(graph, start, end):
    """Find shortest path using Dijkstra's algorithm.

    Algorithm choice rationale:
    - A* was considered but heuristic overhead not worth it
      for our small graphs (typically <1000 nodes)
    - Bellman-Ford not needed as we have no negative weights
    - Floyd-Warshall too expensive for single-source queries

    Time complexity: O((V + E) log V) with binary heap
    Space complexity: O(V) for distance tracking
    """
    # Priority queue ordered by distance
    # Using heapq with (distance, node) tuples
    heap = [(0, start)]

    # Track visited to avoid reprocessing
    # Important: Don't modify during iteration
    visited = set()
```

### Warning Comments

```python
# WARNING: This function is NOT thread-safe!
# Use with thread-local storage or external locking.
# See: https://github.com/project/issues/123
def update_global_state(new_value):
    global _state
    _state = new_value


# CAUTION: Order of operations matters here!
# Must validate before transform, as transform assumes
# valid input and will produce garbage otherwise.
def process_input(data):
    validate(data)  # Must be first
    transform(data)


# NOTE: This timeout value is tuned for production hardware.
# On dev machines, you may need to increase to 30s.
OPERATION_TIMEOUT = 10  # seconds
```

### Technical Debt Comments

```python
# TODO(username): Refactor to use new ConfigService
# when migration is complete (Q2 2025)
# Tracking: JIRA-5678
config = LegacyConfigLoader.load()


# FIXME: This query is O(n^2) and will be slow for large datasets.
# Need to add proper indexing or use a more efficient algorithm.
# Acceptable for MVP but must fix before launch.
def slow_search(items, criteria):
    pass


# HACK: Working around a bug in library v2.3.4
# The library doesn't handle null values correctly.
# Remove when we upgrade to v3.0+
# See: https://github.com/library/issues/999
if value is None:
    value = DEFAULT_VALUE  # Library bug workaround


# OPTIMIZE: This could be parallelized for better performance.
# Current implementation is ~500ms, target is <100ms.
# Consider using multiprocessing or asyncio.
def process_batch(items):
    pass
```

### Module/File Level Comments

```python
"""
User Authentication Module

This module handles all user authentication including:
- Password-based login
- OAuth2 (Google, GitHub)
- API key authentication

Security Considerations:
- All passwords are hashed with bcrypt (cost factor 12)
- Rate limiting applied to prevent brute force
- Sessions expire after 24 hours of inactivity

Dependencies:
- Requires Redis for session storage
- Requires PostgreSQL for user data

Maintainer: auth-team@company.com
Last Security Review: 2025-01-15
"""
```

### What NOT to Comment

```python
# BAD: Redundant comments
# Set x to 5
x = 5

# BAD: Obvious from the code
# Loop through users
for user in users:
    pass

# BAD: Comments that will become stale
# There are 3 cases to handle
if case == 1:
    pass  # What if we add case 4?

# BAD: Commented-out code (use version control)
# old_implementation()
new_implementation()

# BAD: Venting frustration
# This stupid API doesn't work properly
```

### Comment Style by Language

#### Python

```python
# Single line comment for brief notes

"""
Multi-line block comment for longer explanations.
Use for complex algorithms or important context.
"""
```

#### JavaScript/TypeScript

```javascript
// Single line comment

/*
 * Multi-line comment block
 * for longer explanations
 */

/** JSDoc for API documentation */
```

#### Java/C#

```java
// Single line comment

/*
 * Multi-line comment block
 */

/** JavaDoc/XML doc for API documentation */
```

#### Go

```go
// Single line comment (Go uses // for all comments)

// Multi-line comments just use
// multiple single-line comments
// This is idiomatic in Go
```

#### C/C++

```cpp
// Single line comment

/*
 * Multi-line comment block
 */

/** Doxygen documentation comment */
```

## Quality Checklist

- [ ] Complex algorithms explained
- [ ] Business logic documented
- [ ] Design decisions recorded
- [ ] Workarounds marked with tickets
- [ ] Technical debt tracked
- [ ] No redundant comments
- [ ] Comments match code
- [ ] TODO/FIXME have owners
- [ ] External references valid
- [ ] Comments reviewed with code

## Common Issues and Solutions

### Issue: Comments become stale
**Solution**: Review comments during code reviews and update alongside code changes.

### Issue: Too many comments cluttering code
**Solution**: Prefer self-documenting code. Only comment when the "why" isn't obvious.

### Issue: TODO comments never addressed
**Solution**: Add ticket numbers and owners. Review periodically.

## Related Skills

- `docstrings` - Function and class documentation
- `code-quality` - Code quality review
- `technical-documentation` - Architecture documentation

---

**Version**: 1.0.0
**Last Updated**: December 2025
**Based on**: AI Templates documentation_generation/comments/


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
