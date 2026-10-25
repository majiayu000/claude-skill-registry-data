---
name: test-adapters-strip-yaml-frontmatter
description: >
  This skill covers testing the _strip_yaml_frontmatter helper.
  Trigger: test_adapters.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: low
  token_estimate: 350
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# test-adapters-strip-yaml-frontmatter

This skill covers testing the _strip_yaml_frontmatter helper.

**Trigger**: test_adapters.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Get users | `get_users()` |
| Sample skills | `sample_skills` |

## Critical Patterns (Summary)
- **Get Users**: Retrieve user data for testing.
- **Sample Skills**: Access predefined skills for validation.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Get Users

This pattern retrieves user data for testing purposes using the `get_users` function.

```python
users = get_users()
```

### Sample Skills

This pattern accesses predefined skills for validation in tests.

```python
skills = sample_skills
```

## When to Use

- When validating user data in tests.
- When checking the integrity of sample skills.

## Commands

```bash
pytest tests/test_adapters.py
```

## Anti-Patterns

### Don't: Use hardcoded values

Hardcoded values can lead to brittle tests that fail with changes in data.

```python
# BAD
assert user['name'] == 'John Doe'
```
<!-- L3:END -->