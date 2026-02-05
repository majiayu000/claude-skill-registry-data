---
name: code-smell-detection
description: Use when reviewing code quality, before refactoring, when complexity increases, when code feels "hard to change", during code review, or when onboarding to unfamiliar code - systematic identification of code smells with specific refactoring recipes
---

# Code Smell Detection

**Persona:** Code quality auditor who catalogs issues without judgment, focusing on objective metrics.

**Core principle:** Detect smells early, refactor incrementally, prevent accumulation.

## Should NOT Attempt

- Refactoring while detecting (separate concerns)
- Flagging style preferences as smells (smell != dislike)
- Reporting smells without refactoring recipes
- Detecting smells in generated or vendored code

## Smell Categories

### Bloaters (Too Big)

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Long Method | >20 lines, multiple indents | Extract Method |
| Large Class | >300 lines, many responsibilities | Extract Class |
| Long Parameter List | >3 parameters | Introduce Parameter Object |
| Primitive Obsession | Strings for IDs, ints for money | Value Object |
| Data Clumps | Same 3+ fields appear together | Extract Class |

### Change Preventers (Hard to Modify)

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Divergent Change | One class changed for many reasons | Extract Class per reason |
| Shotgun Surgery | One change requires many file edits | Move Method, Inline Class |

### Couplers (Too Connected)

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Feature Envy | Method uses another class more than own | Move Method |
| Message Chains | a.b().c().d() | Hide Delegate |

### Dispensables (Remove)

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Dead Code | Unreachable, unused | Delete |
| Duplicate Code | Same logic in multiple places | Extract Method/Class |
| Comments | Explaining bad code | Refactor code to be clear |

## Detection

```bash
# Long methods/Large files
find ./src -name "*.py" -exec wc -l {} \; | awk '$1 > 300'

# Feature Envy: Count method's references to own vs other class
# If other > own, method belongs elsewhere
```

## Refactoring Recipe: Extract Method

```python
# Before: Long method with comment sections
def process_order(order):
    # Validate order
    if not order.items: raise ValueError("Empty order")
    # Calculate totals
    total = sum(item.price for item in order.items) * 1.1
    # Notify
    send_email(order.customer.email, f"Total: {total}")

# After: Extracted methods
def process_order(order):
    validate_order(order)
    total = calculate_total(order)
    notify_customer(order.customer, total)
```

## Prioritization

| Severity | Smells | Action |
|----------|--------|--------|
| High | Duplicate code, Feature envy, God class | Fix immediately |
| Medium | Long methods, Long params, Data clumps | Fix when touching file |
| Low | Comments, Lazy class | Fix during cleanup |

## Output Format

```markdown
## Code Smell Report: {path}

### High Priority
| File:Line | Smell | Evidence | Refactoring |
|-----------|-------|----------|-------------|
| user.py:45 | Long Method | 67 lines | Extract Method |
```

## Escalation Triggers

| Condition | Action |
|-----------|--------|
| >10 High severity smells | Escalate to `orchestrator` agent for planning |
| God class (>1000 lines) | Use `batch-editor` agent for systematic extraction |
| Circular dependencies | Escalate to architecture review |
| No test coverage | STOP. Add tests before ANY refactoring |

## Failure Behavior

If detection cannot complete:
- Report smells found so far with file:line references
- State reason for incomplete analysis (e.g., "Circular imports prevented full analysis")
- Recommend next steps (e.g., "Break circular dependency A→B→A first")

## Red Flags

- "It works, don't touch it" - Smells accumulate
- Refactoring without tests - Recipe for regression

## Related Skills

- **receiving-code-review**: Both focus on code quality improvement
- **verification-before-completion**: Verify fixes don't introduce new smells

## Integration

- **orchestrator** agent - Plan safe refactoring after detecting smells
- **code-reviewer** agent - Find dead code during review
- **test-driven-development** skill - Write tests before refactoring
