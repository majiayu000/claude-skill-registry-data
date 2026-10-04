---
name: prompt-safety-review
description: >
  Trace untrusted text into prompts and verify sanitization, prompt-injection
  regression coverage, and preservation of system-level instructions.
when_to_use: >
  Use when prompt construction, LLM context, agent summaries, memory, logs, market
  data text, or other untrusted content can influence model instructions.
---

# Prompt Safety Review

## Workflow

1. List all untrusted sources: market data strings, user input, model outputs, prior-agent reasoning, DB text, logs, and external API responses.
2. Trace each source into prompt construction or agent context injection.
3. Verify `_sanitize_external_text()` or an equivalent sanitizer runs before LLM injection.
4. Confirm new prompt templates do not weaken system, safety, or risk-gate instructions.
5. Check `_PROMPT_INJECTION_PATTERNS` coverage when new attack strings are introduced.
6. Require regression tests for prompt-injection paths that changed.

## Blockers

- Raw cross-agent reasoning injected into a prompt.
- External text appended to system instructions without sanitization.
- Security tests that only assert the happy path.
