---
name: auto-invoke
description: Meta-skill — defines when to apply other skills automatically without being asked
triggers:
  - which skill
  - what skill should i use
  - skill routing
  - auto-invoke
---

# Auto-Invoke

Apply the right skill automatically. Do not wait to be asked — recognize the situation and act.

## Skill Routing Table

| Situation | Skill to apply | When exactly |
|---|---|---|
| Building document/semantic search | **rag** | At task start, before writing any retrieval code |
| Changing a prompt or model | **eval** | Before the change ships; write eval first |
| Tool call or phase fails | **self-heal** | Immediately — diagnose before any retry |
| Any error, test failure, broken build | **debug** | Before touching code |
| Context ≥ 60% of limit | **context** | Proactively — don't wait for degradation |
| Session ending or key decision made | **memory** | At session end; also after any surprising gotcha |
| Before PR touching auth/payments/data | **secure** | Before `git push`, not after |
| Before claiming any phase done | **verify** | Every time, no exceptions |
| Picking model/agent for a task | **route** | At task assignment, before delegating |
| Long autonomous run | **loop** | At the start; defines phases and exit conditions |
| Coordinating multiple specialized agents | **multi-agent** | When task requires >1 agent with dependencies |
| Choosing or configuring an inference server | **model-serving** | Before selecting vLLM/TGI/Ollama or quantization |
| Proactive context cleanup at 45% capacity | **context-hygiene** | After completing a large phase or at 45-50% context |

## Decision Protocol

When you encounter a new task or event, ask in this order:

1. **Is there an error?** → `self-heal` (recovery) or `debug` (root cause)
2. **Does it involve LLM output or prompts?** → `eval` (before shipping)
3. **Does it involve document retrieval or vector search?** → `rag` (pipeline)
4. **Is context growing large?** → `context` (compress now)
5. **Is the session ending?** → `memory` (persist decisions)
6. **Is security-sensitive code changing?** → `secure` (checklist)
7. **Is a phase or PR about to be marked done?** → `verify` (evidence)
8. **Coordinating multi-agent work?** → `multi-agent` (DAG + failure handling)
9. **Choosing an inference server?** → `model-serving` (vLLM/TGI/Ollama decision tree)

## Rules

- Skills are **automatic responses to situations**, not optional enhancements
- Apply `verify` before EVERY PR — no exceptions, no shortcuts
- Apply `memory` at EVERY session end — do not let decisions live only in conversation
- Apply `self-heal` BEFORE retrying any failed tool call — diagnose first
- Apply `eval` BEFORE any LLM feature ships — write the measurement first
- Never apply multiple skills simultaneously; sequence them (heal first, then verify, then ship)

## What NOT to auto-invoke

- `plan` — only when starting a new multi-phase task, not on every subtask
- `research` — only when genuinely uncertain about external state (library, API, tool)
- `orchestrate` — only when spawning subagents for parallel work
- `rag` — only when the task involves external document retrieval, not general coding

## Usage

This skill itself is rarely invoked directly. It is loaded by the orchestrator at session start to calibrate routing decisions. Individual skills should be read when the routing table above points to them.
