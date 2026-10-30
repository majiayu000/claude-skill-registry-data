---
name: insecure-output-handling
description: Detects unsafe rendering or execution of LLM output that enables XSS, command
  injection, or second-order injection. Use when writing code that renders LLM
  output to a UI, executes LLM-generated code or shell commands, or passes LLM
  responses to downstream APIs or databases. Also invoke when displaying
  markdown or HTML from an LLM response.
---

# Insecure Output Handling Security Check (OWASP LLM02:2025)

## What this checks

Protects against XSS, command injection, and second-order injection that arise when
LLM output is treated as trusted. The model may produce malicious content through
prompt injection or hallucination; downstream systems must sanitize it the same way
they would sanitize raw user input.

## Vulnerable patterns

- LLM response assigned to a raw-HTML sink (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`, server-side `mark_safe`) without sanitization
- LLM-generated code or shell string passed to `eval`, `exec`, or a subprocess call with shell expansion enabled
- LLM output interpolated into a SQL or NoSQL query string instead of bound as a parameter
- LLM-produced markdown rendered to HTML without an allowlist-based sanitizer
- LLM response forwarded to a downstream API or webhook without re-validating against the destination's schema

## Fix immediately

Flag the vulnerable code and explain the risk. Translate the principles below to the
audited file's language, UI framework, and database driver — use that stack's
documented escaping, sanitizer, and parameter-binding APIs.

For each finding, establish these properties:

1. **Treat LLM output as untrusted input at every consumption point.** The same
   escaping, parameterization, and allowlisting rules that apply to user input
   apply here — prompt injection makes the model a proxy for attacker content.
2. **HTML rendering uses a safe sink.** Plain-text sink or auto-escaping template
   for prose; an allowlist-based sanitizer for rich content. Never a raw-HTML
   sink with an unsanitized LLM string.
3. **Shell and code execution require an allowlist.** If the LLM picks an
   action, the handler validates it against a static set of permitted commands
   and invokes them with argv arrays — never with shell expansion enabled, never
   through a dynamic-evaluation primitive.
4. **Database queries are parameterized.** LLM output lands in bind variables,
   not string-interpolated into the statement. For injection details, see the
   `injection` skill.

## Verification

Confirm the response:

- [ ] No LLM string is assigned to a raw-HTML sink without going through an allowlist-based sanitizer
- [ ] Shell execution uses an allowlist; shell-expansion modes are never used with LLM-derived input
- [ ] If the code routes LLM output into a database query, the query uses parameterized placeholders — not string interpolation or concatenation with the LLM-derived value. Skip this criterion when the code does not execute any database query.
- [ ] LLM output is treated as untrusted user input at every consumption point

## References

- CWE-79 ([Cross-site Scripting](https://cwe.mitre.org/data/definitions/79.html))
- CWE-116 ([Improper Encoding or Escaping of Output](https://cwe.mitre.org/data/definitions/116.html))
- [OWASP LLM02:2025 Insecure Output Handling](https://genai.owasp.org/llmrisk/llm02-insecure-output-handling/)
