---
name: Global Commenting
description: Write meaningful code comments that explain WHY rather than WHAT, focusing on business logic, non-obvious solutions, workarounds, and complex algorithms while keeping code self-documenting. Use this skill when adding comments to explain rationale, documenting complex business logic, explaining workarounds or temporary solutions, describing performance optimizations, writing function documentation (JSDoc, docstrings, XML docs), or reviewing code for appropriate commenting. Apply when working on any code file that contains logic requiring explanation, public API functions, complex algorithms, security-critical code, or architectural decisions. This skill ensures comments explain rationale not implementation (WHY not WHAT), self-documenting code through clear naming (refactor unclear code instead of commenting), concise and evergreen comments (no who/when dated comments - Git tracks this), links to external resources for context, proper function documentation format (JSDoc for TS/JS, docstrings for Python, XML docs for .NET), no TODO/FIXME in committed code (use issue tracking system instead and reference ticket), and deletion of dead commented-out code (Git history preserves it).
---

# Global Commenting

## When to use this skill:

- When explaining business logic or domain-specific rules with ticket references
- When documenting non-obvious implementation decisions
- When describing workarounds for browser bugs or library limitations with bug report links
- When explaining performance optimizations and their trade-offs with profiling data links
- When documenting complex algorithms or calculations with Wikipedia/paper links
- When noting security considerations or sensitive operations (OWASP recommendations)
- When explaining data flow or architectural patterns (e.g., function called from multiple places)
- When writing JSDoc comments for TypeScript/JavaScript public API functions
- When writing docstrings for Python public functions (Google style)
- When writing XML documentation for .NET public methods
- When documenting public API functions or library interfaces
- When reviewing code to determine if comments should be added or removed
- When deciding whether to comment or refactor unclear code (prefer refactoring)
- When replacing TODO/FIXME with issue tracker references

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle global commenting.

## Instructions

For details, refer to the information provided in this file:
[global commenting](../../../agent-os/standards/global/commenting.md)
