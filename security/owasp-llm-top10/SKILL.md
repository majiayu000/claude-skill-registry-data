---
name: owasp-llm-top10
description: This skill should be used when the user mentions "prompt injection", "jailbreak", "owasp llm", "llm security", "guardrails", "data exfiltration", "insecure output", "tool abuse", "indirect injection", or "is this agent safe". It provides the OWASP Top 10 for LLM Applications mapped to code-level signals, plus a library of concrete attack strings to test against.
---

# OWASP LLM Top 10

## Purpose
Provide a standardized, code-level lens for auditing LLM applications against the OWASP Top 10 for LLM Applications, so a security review of prompt construction and tool wiring is consistent and grounded in the source, not hand-waved. The recurring, highest-impact failure is **LLM01 prompt injection**: untrusted content (user text, retrieved documents, tool outputs, fetched web/email) is concatenated into a prompt and then read as instructions, driving the model, and any tool it can call, to do the attacker's bidding. This skill maps each risk to the code pattern that causes it, the mitigation, and a concrete attack to test with.

## The core mental model
An LLM has no reliable boundary between "instructions" and "data." Everything in the context window is a candidate instruction. Security follows from three questions asked at every call site:
1. **Provenance**: is this text trusted (developer-authored) or untrusted (from a user, a document, a tool result, the web)?
2. **Capability**: what tools can the model call, and what can each tool do (read secrets? send data? mutate state?)?
3. **Reachability**: can untrusted text change the instructions in a way that reaches a dangerous capability?

If untrusted text and a dangerous capability meet with nothing between them, you have an exploitable path.

## Risk-to-signal quick map

| ID | Risk | Code-level signal |
|---|---|---|
| LLM01 | Prompt injection | Untrusted input interpolated into a prompt with no delimiting/labeling; RAG docs or tool outputs re-fed unfenced |
| LLM02 | Insecure output handling | Model output → HTML/SQL/shell/redirect/URL with no filtering |
| LLM03 | Training-data / data poisoning | Untrusted content ingested into the index or fine-tune set without provenance checks |
| LLM04 | Model denial of service | Unbounded output/context, recursive agent loops, no `max_tokens`/step limit |
| LLM05 | Supply-chain | Unpinned models, untrusted plugins/tools, unverified third-party prompts |
| LLM06 | Sensitive information disclosure | Secrets/PII in the prompt or reachable by a tool; model can echo them out |
| LLM07 | Insecure plugin/tool design | Over-broad tool (shell, arbitrary HTTP), no input validation, no least privilege |
| LLM08 | Excessive agency | Model can take irreversible/high-impact actions with no confirmation gate |
| LLM09 | Overreliance | App trusts model output as fact with no verification/grounding |
| LLM10 | Model theft | Unprotected model endpoints, prompt/weight leakage |

## Defense patterns (apply at the call site)
- **Delimit and label untrusted input**: fence it, mark it explicitly as data, and instruct the model to treat fenced content as information to analyze, never as commands.
- **Establish an instruction hierarchy**: system/developer instructions outrank anything in user/tool/document content; state this and keep operator instructions in the privileged channel, not concatenated into user text.
- **Least-privilege the tool belt**: expose only the tools a task needs; scope credentials tightly.
- **Gate side effects**: require confirmation (or policy checks) before irreversible or high-impact tool calls (send, delete, pay, deploy).
- **Break exfiltration pairs**: never let a read-secret capability and a send-data capability be reachable from the same injected instruction; block model-emitted URLs/images that can carry data out.
- **Filter output**: validate/encode model output before any sink (escape HTML, parameterize SQL, never `eval`).
- **Bound the loop**: cap output tokens, agent steps, and tool-call depth (LLM04).

## Additional Resources
### Reference Files
- **`references/attack-templates.md`**: concrete prompt-injection and jailbreak strings to test with: direct override, indirect/RAG-poisoning payloads, tool-abuse and exfiltration probes, and encoding/obfuscation variants, each with what a pass/fail looks like.
- **`references/llm-top10-catalog.md`**: LLM01–LLM10 in depth: the exact code pattern that causes each risk (across raw SDKs, LangChain/LlamaIndex, and agent frameworks), the mitigation, and the residual risk to note.
