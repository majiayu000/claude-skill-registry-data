---
name: anti-tool-sprawl
description: Prevents over-tooling, tool spam, context bloat, and convergence failure. Enforces lean tool selection, deduplication, step limits, and progress detection.
---

# Anti-Tool Sprawl Skill

## Problem

Four linked failure modes from tool misuse:

**Over-tooling** — Beyond ~10-20 tools per context, selection accuracy collapses. More tools make the agent *worse*, not better. Tool descriptions compete with the user's task for attention.

**Tool spam** — Repeating the same tool call with the same arguments, getting the same result, trying again. The agent stays busy but makes no progress.

**Context bloat** — Every turn adds full history + raw tool outputs. Tool definitions alone can consume 60%+ of context before work begins. A 4-turn conversation can burn 288K tokens on tool definitions.

**Convergence failure** — No built-in stopping criterion. The agent doesn't know when it has enough information. Without convergence logic, it's an expensive polling function.

## Detection triggers

Activate when:
- More than 10 tools are available for a single task
- The same tool gets called 3+ times with similar arguments
- Tool output is large (logs, HTML, JSON dumps, binary)
- The conversation has been running for many turns
- The agent keeps retrieving without synthesizing

## Protocol

### 1. Tool selection discipline
Before calling a tool, ask:
- Do I actually need this tool, or do I already know the answer?
- Is there a more specific tool that does only what I need?
- Am I calling this because I'm in a loop, or because it's genuinely useful?

Limit visible tools to the minimum needed for the current subtask.

### 2. Deduplicate before calling
Before calling any tool:
- Check if you've already called it with these exact arguments
- If yes, use the previous result instead of calling again
- If the previous result was empty/error, try a different approach — not the same call harder

### 3. Compress tool output
When a tool returns large data:
- Extract only what's needed for the current task
- Summarize verbose output before adding to context
- Do NOT dump raw logs, HTML, or full JSON payloads into the conversation

### 4. Convergence checks
After each tool call, ask:
- Did I learn something new, or is this the same information from a different angle?
- If the marginal gain is near zero, STOP. Synthesize the answer with what you have.

### 5. Hard limits
- Maximum tool calls per subtask: 5
- If you've called 3+ tools with no clear progress, admit it and ask the user for guidance
- If you're repeating the same call pattern, STOP and change approach

## When NOT to use
- First call to understand the problem (always gather initial context)
- Sequential operations that genuinely need different tools
- User explicitly asks to retry or dig deeper

## Bundled Script

Copy `check-tool-usage.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/anti-tool-sprawl/scripts/check-tool-usage.ps1 .ai_scripts/
```

Analyzes a session log for excessive or redundant tool calls:

```powershell
.ai_scripts\check-tool-usage.ps1 -LogFile session.log -MaxToolCalls 20 -MaxUniqueTools 8
```

## Cross-references

- **dont-kill-tokens** — Both reduce unnecessary context consumption.

- **anti-premature-termination** — Tool sprawl causes wasted context leading to premature termination.

- **self-validate** — Validation after operations catches failures caused by over-tooling.
- **skill-loader** — Loading cross-referenced skills is a tool call. Batch them to avoid sprawl.
- **context-engineering** — Tool sprawl wastes context. Context engineering helps select the right tools for the current task.
