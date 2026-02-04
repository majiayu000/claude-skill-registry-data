---
name: coding-python
description: When python, flask, or jinja are being written or edited.
---

# Python coding standards

## Mandatory Metadata
**Every** function or class you touch MUST have this comment header:
```python
# [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration]
# Example: # Modified by Claude-3.5-Sonnet | 2024-10-27_01
```
## Syntax & Style
Quotes: Enforce Double Quotes (") over Single Quotes (').
Good: x += "."
Bad: x += '.'
SQL: Always use Multi-line strings (""") for SQL queries.
Templates: Set language mode to jinja-html.
Spacing: Keep vertical spacing compact (no excessive blank lines).
Readability: Prioritize Readable Code over "clever"/compact [pythonic] one-liners.

## Comments
**Preserve comments**: Do NOT delete existing, still relevant comments.
**Comment liberally**: Explain why, not just what.

## Logic & Operations
**File Collisions**: If a file exists, append _[timestamp] to the new filename.
**Simplicity**: Choose the simplest working solution.

## Tooling Preference (Web)
Primary: browser_action (ALWAYS try this first).
Fallback: Other browser tools (Only if browser_action fails).
