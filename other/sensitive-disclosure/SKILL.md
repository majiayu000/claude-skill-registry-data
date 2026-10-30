---
name: sensitive-disclosure
description: Detects PII, credentials, and secrets passed to LLM APIs or embedded in system
  prompts. Use when writing code that passes sensitive data (PII, credentials,
  health data) to an LLM API, constructs system prompts containing secrets,
  returns LLM responses that could contain training data, or implements
  memory/context persistence.
---

# Sensitive Information Disclosure (OWASP LLM06:2025)

## What this checks

Prevents confidential data from leaking through LLM inputs or outputs. LLMs may memorize,
echo, or inference-time expose PII, credentials, and business secrets embedded in
prompts — to current users, future users, or via model extraction.

## Vulnerable patterns

- Whole user or account records interpolated into a system or user prompt
- API keys, database passwords, or other credentials baked into prompt strings
- Returning raw LLM responses to callers without an output-redaction gate — the response can echo data injected via retrieval or memory
- Conversation history or vector-store writes that mix multiple users' content without partitioning by user identity
- Logging or telemetry that emits prompts and completions unredacted

## Fix immediately

Flag the vulnerable code, explain the risk, and suggest a fix establishing these
properties. Translate to the language and framework of the audited file — use that
stack's secrets manager, logging library, and redaction helpers; do not import names
from a different stack.

1. **PII is redacted or pseudonymized before it reaches the model.** Replace raw records with opaque identifiers, or scrub values matching known sensitive patterns (SSN, email, card numbers, health identifiers). A prompt-level instruction like "don't repeat personal details" is not sufficient.
2. **No credentials appear in prompt strings.** Load them server-side from environment or a secrets manager and never interpolate into a system prompt — even "just for auth context".
3. **Every return site for an LLM response passes through an output-redaction gate** before the response leaves the process. This catches data that leaked in via retrieval or memory.
4. **If conversation history or a memory/vector store is persisted**, records are keyed or partitioned by user identity so one session's context cannot be retrieved by another.
5. **If prompts or completions are logged**, the same redaction helper runs before emission — otherwise logs become the leak.

## Verification

Confirm these properties hold for every relevant pattern present in the code under
review (each criterion applies only when its pattern is actually present):

- [ ] No PII field (SSN, DOB, email, phone, address, health record) reaches an LLM API call site without first passing through a redaction or pseudonymization step
- [ ] System prompts contain only constants loaded from a secrets-manager or environment-backed config, never hardcoded credential literals or interpolated secret values — only applies if the code references credentials near the prompt construction
- [ ] Every code path that returns an LLM response to a caller routes the response through an output-redaction helper before it leaves the process
- [ ] If the code persists conversation history or writes to a memory/vector store, records are keyed or partitioned by user identity so one session's context cannot be retrieved by another — skip when the code is a stateless single-request handler
- [ ] If the code contains logging or telemetry statements that receive a prompt or completion variable, the variable is passed through a redaction helper before emission — skip when the code has no logging of prompts or completions

## References

- CWE-200 ([Exposure of Sensitive Information](https://cwe.mitre.org/data/definitions/200.html))
- CWE-359 ([Exposure of Private Personal Information](https://cwe.mitre.org/data/definitions/359.html))
- [OWASP LLM06:2025 Sensitive Information Disclosure](https://genai.owasp.org/llmrisk/llm06-sensitive-information-disclosure/)
