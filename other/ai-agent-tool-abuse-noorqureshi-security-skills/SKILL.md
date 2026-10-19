---
name: ai-agent-tool-abuse
description: >
  Abuse an LLM agent's tools/functions — coerce it to call tools with attacker-chosen args for
  SSRF, RCE, data exfil, or privilege abuse. Load when the target is an agent with tools/
  function-calling/plugins, MCP servers, code interpreters, or "the assistant can do X". Signals:
  function-calling, tool schemas, browse/email/query/exec tools, autonomous agents.
domain: ai-ml
type: technique
stability: learning
modes: [bugbounty, pentest, defense]
severity: critical
owasp_llm: [LLM06:2025-Excessive-Agency, LLM01:2025-Prompt-Injection]
cwe: [CWE-77, CWE-918]
tools: []
schema_version: 1
---

# LLM agent / tool abuse (excessive agency)

## When it applies
The target isn't just a chatbot — it can *act*: call functions, browse, run code, query
databases, send email, hit internal APIs, or chain MCP tools. Impact jumps from "bad text" to
real actions taken with the agent's privileges.

## Why it works
The model decides which tool to call and with what arguments, driven by text it can't fully trust
(user input or fetched content). If tools are over-permissioned or arguments aren't validated,
attacker text steers real actions — the classic "confused deputy".

## Method
1. **Enumerate the tools**: get the agent to reveal its tools/functions and schemas (often it
   just lists them), or read the app/MCP config.
2. **Coerce a call** (direct or via `ai-prompt-injection`/`ai-rag-poisoning`): craft input so the
   agent invokes a tool with your arguments.
3. **Route to impact**:
   - **SSRF/internal reach**: a browse/fetch tool → internal URLs, cloud metadata (→ `cloud-imds-ssrf`).
   - **RCE**: a code-interpreter/shell tool → command execution.
   - **Data exfil**: a query/email/file tool → dump data to you (markdown-image beacon, an email to your address).
   - **Privilege abuse**: an admin/action tool called on behalf of a victim (confused deputy).
4. **Chaining**: poisoned content the agent reads later triggers the tool call (indirect, multi-user).

## Gotchas
- The severity is the *action*, tied to the tool's real privilege — demonstrate the effect, not just intent.
- Guardrails on the model don't cover tool arg-validation — the bug is often at the tool boundary.
- Defenders: least-privilege tools, human-in-the-loop for sensitive actions, validate/allowlist args, isolate the browser/exec.

## Verify success
The agent performs an attacker-directed action via a tool — an SSRF hit, code execution, data
exfiltrated, or a privileged action taken — traceable to your input.

## References
OWASP LLM Top 10 (2025) LLM06/LLM01; MCP security guidance; agent "confused deputy" research.
