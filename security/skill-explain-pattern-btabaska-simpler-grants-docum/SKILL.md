---
name: Explain Pattern
description: "Explain a specific code idiom, function, decorator, hook, or snippet in-place, with references to the governing convention rules or ADRs. Triggers on 'explain this', 'what does this do', 'why is this written this way'. Output is a terse explanation with rule/ADR citations."
model: inherit
---

## Purpose

Provide a focused in-place explanation of one idiom or snippet, grounded in the project's rules and decisions, rather than a generic language tutorial.

## When to Invoke

- A reviewer or onboarding engineer asks about a single function, decorator, hook, or block.
- Before copying a pattern into a new place, to confirm it is the blessed pattern.
- When a rule lint flags something and the author wants to know why.

## When NOT to Invoke

- For whole-subsystem walkthroughs (use `/skill-explain-codebase-area`).
- For language-general questions unrelated to this codebase.
- For design alternatives (use an ADR flow).

## Inputs

- **target**: file + line range or a pasted snippet.
- **question** (optional): narrow the explanation (e.g. "why `@flask.g`?").

## Procedure

1. Read the target block with surrounding context (+/- 20 lines).
2. Identify the idiom category: decorator, hook, context manager, mixin, SQLAlchemy query, Pydantic validator, etc.
3. Search `documentation/rules/*.md` and `documentation/decisions/adr/` for references to the idiom.
4. Compose a 3–5 sentence explanation: what it does here, why this pattern is used, which rule/ADR governs it.
5. If no governing rule exists, label as "convention in practice, not documented" and cite two other occurrences.

## Outputs

```
Pattern: @with_api_logging decorator
File: api/src/api/opportunities_v1/search.py L42

What: Wraps the handler in an audit log entry and correlation-id context.
Why: api-logging.md MUST: all v1 handlers emit audit log on entry and exit.
Citations:
  - documentation/rules/api-logging.md §"Handler audit logging"
  - ADR-0014 (API observability)
Other usage: api/src/api/applications_v1/submit.py L31
```

## Safety

- Read-only.
- Never invents rule citations; if none exist, says so.
- Never guesses about runtime behavior; sticks to static inspection.
- FedRAMP: flags security-sensitive patterns (auth decorators, audit logging) with a reminder not to bypass.

## Examples

**Example 1 — Decorator.** `@require_scope("opportunity:read")` — cites the auth rule and the ADR introducing scopes.

**Example 2 — React hook.** `useFeatureFlag("new_search")` — cites the feature flag convention and the ops runbook.

**Example 3 — Undocumented idiom.** A SQLAlchemy `.execution_options(yield_per=100)` pattern that has no rule; skill flags "convention in practice" and links two other uses.

## Related

- `.cursor/skills/skill-explain-codebase-area/` — for broader tours.
- `.cursor/skills/skill-check-conventions/` — if the pattern turns out to violate a rule.
