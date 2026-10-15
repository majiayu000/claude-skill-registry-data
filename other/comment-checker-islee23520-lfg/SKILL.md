---
name: comment-checker
description: Use when GrokBuild needs to understand or respond to automatic comment-checker feedback emitted after an edit-like PostToolUse hook (lfg native hook).
---

# GrokBuild Comment Checker (lfg)

lfg registers a Grok `PostToolUse` hook for successful edit-like tools (`write`, `edit`, `multi_edit`, and equivalents).

When comment-checker reports a warning after a patch, the session receives bounded feedback and should fix or explain the flagged comment before moving on.

## Scope

- No MCP tool is required for the native Grok path.
- Non-edit tools are ignored.
- Missing checker binaries emit no hook output so normal GrokBuild work can continue.
- Fail-closed on malformed hook JSON (matches lfg hook discipline).

## Cross-host note

Upstream OMO may brand this as a Codex plugin skill. On GrokBuild the same skill is about **lfg native PostToolUse** feedback, not a Codex-only runtime.
