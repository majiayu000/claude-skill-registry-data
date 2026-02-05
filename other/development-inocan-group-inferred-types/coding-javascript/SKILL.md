---
name: coding-javascript
description: When javascript being written or edited.
---

# Javascript coding standards

## Mandatory Metadata
**Every** function or class you touch MUST have this comment header:
```javascript
// [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration]
```
Example: // Modified by Claude-4.5-Sonnet | 2026-01-27_01

## Syntax & Style
**Quotes**: Enforce Double Quotes (") over Single Quotes (').
Good: x += "."
Bad: x += '.'
**Vertical spacing**: Keep vertical spacing compact (no excessive blank lines).
**Readability**: Prioritize Readable Code over "clever" one-liners.
**In-line js**: Prefer including from functions in .js files to in-line js, unless explicitly justified.

## Comments
**Preserve comments**: Do NOT delete existing, still relevant comments.
**Comment liberally**: Explain why, not just what.

## Logic & Operations
**File Collisions**: If a file exists, append _[timestamp] to the new filename.
**Simplicity**: Choose the simplest working solution.

## Tooling Preference (Web)
Primary: browser_action (ALWAYS try this first).
Fallback: Other browser tools (Only if browser_action fails).
