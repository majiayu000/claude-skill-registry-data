---
name: delegate-to-ide
description: >-
  Delegate a task to another AI IDE's CLI (codex / claude / opencode /
  cursor-agent) through an isolated-context subagent. Use when the user says
  delegate to <ide>, have <ide> do <task>, or offload to <ide>. For one-shot
  relay use `ai-ide-runner`.
---

# Delegate to Another AI IDE

**You are NOT the courier — the `worker` subagent is.**
This skill exists to keep the child CLI's transcript out of your context. If
you shell out to `codex` / `claude` / `opencode` / `cursor-agent` yourself
from this parent session, you defeat the point — every byte of the child's
output then lands in your working context. Always invoke the subagent
instead.

## When to use this skill vs `ai-ide-runner`

- Use **this skill** (`delegate-to-ide`) when the user wants the other
  IDE to *do a task* on their behalf and only the final result needs to
  surface in the current chat. The child's intermediate work stays in the
  subagent's isolated context.
- Use **`ai-ide-runner`** when the user wants a *one-shot relay*
  (second opinion on a single question), a *fan-out comparison* across
  several IDEs, or a *cross-model comparison* within one IDE. There the
  child's full output IS the deliverable, and isolation buys nothing.

## Workflow

### Step 1 — Parse the user's intent

Extract:

- `{target_ide}` — `codex`, `claude`, `opencode`, or `cursor-agent`. If the
  user named only a vendor or a model, map to the vendor's native IDE
  (Anthropic / Claude → `claude`; OpenAI / GPT / o-series → `codex`;
  Cursor's own Composer → `cursor-agent`). Reach for OpenCode only when
  the user says "in OpenCode", asks for OpenRouter billing, or asks to
  fan out across providers (in which case `ai-ide-runner` is
  almost certainly the better skill).
- `{model}` — optional. If unspecified, leave to the worker (it uses the
  target's flagship alias).
- `{task_prompt}` — the actual task description the target IDE should
  execute. Strip routing scaffolding ("delegate to Codex:", "have Claude
  do …") so the worker passes a clean prompt to the child CLI.

### Step 2 — Invoke the worker subagent

Per-host invocation syntax:

- **Claude Code**: use the `Agent` / `Task` tool with
  `subagent_type=worker`.
- **OpenCode**: use the `@worker <task prompt>` mention
  syntax.
- **Codex**: use the `spawn_agent` tool with `agent_type="worker"` and
  `fork_turns="none"` (a full-history fork cannot carry an agent type),
  then collect the reply with `wait_agent`. The role is dispatchable only
  when `worker.toml` sits under the Codex home
  (`ls "${CODEX_HOME:-$HOME/.codex}/agents/"`); an empty listing means the
  role is not installed — say so, do not run the child CLI inline.
- **Cursor** (no native subagent dispatch): subagent invocation is
  unavailable on this host. Surface this limitation clearly to the user
  and route them to `ai-ide-runner` for one-shot relay. Do NOT
  silently fall back to running the child CLI inline — that would defeat
  the context-isolation point that motivates this skill.

Pass the worker a single block containing:

```
Target IDE: {target_ide}
Model: {model or "default"}
Task prompt:
{task_prompt}
```

### Step 3 — Relay the worker's reply

The worker returns a labelled, quoted block with the child CLI's output.
Surface that block to the user verbatim — do NOT add commentary *inside*
the quoted block, do NOT paraphrase the child's content, do NOT translate
or re-style. Brief framing outside the block (e.g. "Codex returned:") is
fine.

If the worker reports that the host has no subagent mechanism (see Step 2,
Cursor / Codex case), pass that message through and stop.

## Output contract

This skill's final message MUST consist of:

1. A short preface naming the target IDE (one line).
2. The worker's quoted block, byte-for-byte. The substantive content words
   inside the block come from the child runtime's stdout (or from the hook
   `reason` payload on sandbox runs), NOT from the parent model's weights.
3. (Optional) A short follow-up question to the user.

Do not, under any circumstances, run `claude -p` / `codex exec` /
`opencode run` / `cursor-agent -p` from this parent session. If you find
yourself drafting such a Bash call, STOP — go to Step 2 and invoke the
subagent instead.

## Scope boundaries

This skill covers **invocation routing**: parsing the user's intent,
choosing the worker as the execution vehicle, and surfacing the worker's
reply. It does NOT:

- compare runs across IDEs or models (use `ai-ide-runner`);
- fan out one prompt across multiple IDEs (also `ai-ide-runner`);
- install CLIs, run authentication flows, or persist transcripts;
- carry multi-turn delegated conversations (single-shot only — multi-turn
  via session resume is a future enhancement).
