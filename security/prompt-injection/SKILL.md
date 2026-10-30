---
name: prompt-injection
description: Detects LLM prompts built from user input or retrieved documents that let
  attackers hijack the model's instructions. Use when writing code that
  constructs LLM prompts from user input, builds system prompts, implements
  RAG pipelines, or processes external documents fed to a model. Also invoke
  when external data can influence LLM context.
---

# Prompt Injection Security Check (OWASP LLM01:2025)

## What this checks

Protects against attacker-controlled text that hijacks LLM instructions. Direct
injection arrives through user input; indirect injection arrives through retrieved
documents, emails, or tool outputs. Both can cause the model to exfiltrate data,
bypass guardrails, or execute unintended actions.

## Vulnerable patterns

- User input interpolated directly into the system-role message — user text lands in the instruction tier.
- Retrieved documents concatenated raw into the prompt with no delimiter or trust label.
- Email bodies, fetched web pages, or other external content passed into the prompt with no boundary markers separating data from instructions.
- No structural separation between developer instructions and untrusted data — everything is one string.
- Raw model response returned to the caller, rendered, logged, or used to trigger a downstream action with no validation step in between.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language and LLM
client library — use that library's documented role-separated message API rather
than mirroring an example from another stack.

1. **Trust tiers are structurally separate.** Developer instructions go in the
   system role; user input and retrieved documents go in the user role, wrapped
   in explicit delimiter tags that label the content as untrusted data. Never
   interpolate user text into the system prompt.
2. **Input is bounded and screened before the API call.** Apply a length cap
   and reject obvious injection markers (phrases like "ignore previous", "new
   instruction"). Screening is a denylist and will not catch everything, but it
   raises the bar.
3. **Output is validated before any downstream action.** Every code path that
   uses the model's response — returning it to the caller, rendering it,
   logging it, triggering a tool call — first routes it through a gate that
   enforces size bounds and rejects suspicious instruction language. A defined
   validator that is never called does not satisfy this.

## Verification

Confirm these properties hold:

- [ ] User input never appears in the system-role message
- [ ] Retrieved documents are wrapped in explicit delimiter tags, not concatenated raw into the prompt
- [ ] Input length and pattern validation runs before the API call
- [ ] The LLM response passes through a validation step at every call site before it is returned, rendered, logged, or used to trigger an action. A validator defined but never invoked does not count

## References

- CWE-77 ([Improper Neutralization of Special Elements in a Command](https://cwe.mitre.org/data/definitions/77.html))
- CWE-74 ([Improper Neutralization of Special Elements in Output](https://cwe.mitre.org/data/definitions/74.html))
- [OWASP LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
