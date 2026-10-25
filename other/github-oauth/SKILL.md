---
name: exchange-github-oauth-code
description: >
  This skill covers the implementation of GitHub OAuth helper functions.
  Trigger: Load this skill when handling GitHub OAuth processes.
license: Apache-2.0
metadata:
  author: repoforge
  version: "1.0"
  complexity: medium
  token_estimate: 450
  dependencies: []
  related_skills: []
  load_priority: high
---

<!-- L1:START -->
# exchange-github-oauth-code

This skill covers the implementation of GitHub OAuth helper functions.

**Trigger**: Load this skill when handling GitHub OAuth processes.
<!-- L1:END -->

<!-- L2:START -->
## Quick Reference

| Task | Pattern |
|------|---------|
| Generate OAuth state | `generate_state()` |
| Validate OAuth state | `validate_state()` |

## Critical Patterns (Summary)
- **Generate OAuth state**: Create a unique state parameter for OAuth flow.
- **Validate OAuth state**: Ensure the state parameter matches the expected value.
<!-- L2:END -->

<!-- L3:START -->
## Critical Patterns (Detailed)

### Generate OAuth state

This function creates a unique state parameter to prevent CSRF attacks during the OAuth flow.

```python
from apps.server.app.services.github_oauth import generate_state

state = generate_state()
```

### Validate OAuth state

This function checks if the provided state matches the expected value to ensure the integrity of the OAuth process.

```python
from apps.server.app.services.github_oauth import validate_state

is_valid = validate_state(received_state, expected_state)
```

## When to Use

- When initiating the GitHub OAuth flow to generate a state parameter.
- When validating the state parameter after the user is redirected back from GitHub.

## Commands

```bash
docker-compose up
python repoforge/cli.py
```

## Anti-Patterns

### Don't: Use hardcoded state values

Hardcoding state values can lead to security vulnerabilities and CSRF attacks.

```python
# BAD
state = "fixed_state_value"
```
<!-- L3:END -->