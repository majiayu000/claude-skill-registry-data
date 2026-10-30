---
name: rag-security
description: Detects RAG pipelines that ingest external documents into LLM context without
  sanitization or trust gating. Use when building RAG pipelines, ingesting
  external documents into vector stores, or retrieving content from external
  sources to include in LLM context. Also invoke when writing code that
  fetches URLs or parses documents for LLM prompts.
---

# RAG Pipeline Security (OWASP LLM01:2025)

## What this checks

Prevents prompt injection through retrieved documents and uncontrolled content flooding
into LLM context. Attacker-controlled documents can override system instructions,
exfiltrate data, or manipulate model behavior when injected without guardrails.

## Vulnerable patterns

- Retrieved document concatenated into the system prompt — retrieved content can override developer instructions.
- HTTP fetch of a caller-supplied or document-supplied URL with no domain allowlist — SSRF surface and attacker-controlled content into context.
- No length or token cap on retrieved content, allowing one document to consume the entire context window.
- Retrieved content mixed into the prompt with no delimiter or trust label distinguishing it from developer instructions.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language, HTTP
client, and LLM API — use the documented secure primitives of that stack.

1. **Retrieval sources are validated against a domain allowlist before fetch.**
   Arbitrary URLs from user input or from another document's links lead to SSRF
   and to attacker-controlled documents landing in the context; the allowlist
   is the same property enforced by the `ssrf` skill for outbound HTTP.
2. **Retrieved content is truncated to a fixed character or token cap** before
   injection into the prompt. Unbounded retrieval lets a single document eat
   the context window — either denial of service or a vehicle for flooding
   instructions.
3. **Retrieved content is wrapped in explicit delimiters that label it as
   untrusted data**, and lives in the user role — never concatenated into the
   system prompt. The model is more likely to treat it as data rather than
   instructions when the framing is structural. See the `prompt-injection`
   skill for the trust-tier pattern.
4. **Every retrieval is logged** with source URL and content length — useful
   for incident response and for detecting poisoning attempts (sudden spikes
   in retrieved size or novel sources).

## Verification

Confirm the response:

- [ ] Retrieved URLs validated against an explicit domain allowlist
- [ ] Content truncated to a fixed character or token limit before injection
- [ ] Retrieved content wrapped in clear delimiters that mark it as untrusted
- [ ] Every retrieval logged with source URL and content length

## References

- CWE-77 ([Improper Neutralization of Special Elements in Commands](https://cwe.mitre.org/data/definitions/77.html))
- CWE-20 ([Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html))
- CWE-284 ([Improper Access Control](https://cwe.mitre.org/data/definitions/284.html))
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
