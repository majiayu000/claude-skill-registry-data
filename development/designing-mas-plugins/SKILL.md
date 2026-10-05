---
name: designing-mas-plugins
description: Design evaluation plugins following 12-Factor + MAESTRO principles
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
  argument-hint: [component-name]
  stability: stable
  content-hash: sha256:44f931b696bbfe8ea3acf1d6d3e979d90b86144040f596acd7bf9e865f228627
  last-verified-cc-version: 1.0.34
---

# Designing MAS Plugins

**Target**: $ARGUMENTS

## When to Use

Trigger this skill when:

- Designing agent plugins or evaluation components
- Planning pipeline architecture
- Architecting new metrics or evaluation tiers
- Refactoring engines into plugin patterns

## Core Principles

Plugins follow six principles. For worked code examples of each, see
`references/core-principles-with-examples.md`.

1. **Stateless Reducer** — `evaluate(context) -> result` as a pure function; no side effects, no shared state
2. **Own Context Window** — plugin manages its own context; no global state access
3. **Structured Outputs** — all data uses validated models, no raw dicts
4. **Own Control Flow** — plugin handles its own errors and timeouts
5. **Compact Errors** — structured partial results, not exceptions
6. **Single Responsibility** — one metric or tier per plugin

## Plugin Design Checklist

Before implementing a plugin, verify:

- [ ] **Stateless**: No class attributes, no global state
- [ ] **Own Context**: All inputs via `evaluate()` parameter
- [ ] **Typed I/O**: Validated models for inputs and outputs
- [ ] **Own Errors**: Returns error results, doesn't raise
- [ ] **Own Timeout**: Respects configured timeout
- [ ] **Single Responsibility**: One metric or tier
- [ ] **Explicit Context**: Filters output for next stage
- [ ] **Env Config**: All config via env vars / settings
- [ ] **Observable**: Emits structured logs for debugging
- [ ] **Graceful Degradation**: Partial results on failures

## Anti-Patterns

- Shared State: `self.cache = {}` (breaks stateless)
- Raw Dicts: `return {"score": 0.5}` (use models)
- Raising Exceptions: `raise ValueError()` (return error)
- Global Access: `config.get_global()` (use settings)
- Implicit Context: Passing entire result to next tier
- Multiple Responsibilities: One plugin, 3 metrics

## Implementation Template

See `references/plugin-implementation-template.md` for the full `EvaluatorPlugin` abstract base class and a worked `MyPlugin` example with typed context/result models, error handling, and next-tier context filtering.

## Testing Strategy

See `references/plugin-testing-strategy.md` for isolation test patterns — happy path and structured-error-handling tests using mocked context.

## References

- `references/mas-design-principles.md` — foundational design principles (existing)
- `references/core-principles-with-examples.md` — code examples for each of the six core principles
- `references/plugin-implementation-template.md` — full `EvaluatorPlugin` + `MyPlugin` template
- `references/plugin-testing-strategy.md` — isolation test patterns

## Further Reading

- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)
- [Anthropic Harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [PydanticAI Patterns](https://pydantic.dev/articles/building-agentic-application)
- [NIST AI RMF 1.0](https://www.nist.gov/artificial-intelligence/executive-order-safe-secure-and-trustworthy-artificial-intelligence)
- [ISO/IEC 42001:2023 — AI Management System](https://www.iso.org/standard/81230.html)
