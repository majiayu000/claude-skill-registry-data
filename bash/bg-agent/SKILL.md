---
name: bg-agent
description: Manage background subagents with tier-routed models, stripped tool contexts, lifecycle pruning, and zero-polling reactive execution to minimize token and credit usage.
version: 1.0.0
execution-mode: side_effecting
argument-hint: "<task | list | kill [id|all] | clean> [--tier flash_lite|flash|pro] [--type research|lean_scout|self] [--workspace inherit|branch|share]"
category: fleet-ops
status: candidate
---
# bg-agent | Background Agent & Usage Optimization Manager

Orchestrates background agents and subagents with strict usage-saving constraints: tier-routed models (`flash_lite` default for research), tool-context stripping (no MCP/write bloat), zero-polling event-driven resumption, and active lifecycle pruning.

## When to Use
- You want to run tasks in the background without burning high-tier model quota or tokens.
- Decomposing research, file auditing, or discovery across parallel lightweight workers.
- Checking status of running background agents or killing idle/stalled subagents.
- Offloading heavy scripts or command outputs to background tasks to keep context small.

---

## The Usage-Saving Matrix

| Strategy | Mechanism | Usage Impact |
|---|---|---|
| **Tier Routing** | Dispatch with `Model: 'flash_lite'` or `'flash'` rather than `'inherit'` / `'pro'` | **80–95% cost reduction** per run |
| **Tool Scoping** | Use `TypeName: 'research'` or custom `define_subagent` without MCP or write tools | **Eliminates 1,000s of tokens** of schema injection per turn |
| **Zero-Polling** | Rely on native reactive wakeup; never loop `manage_subagents(status)` | **Zero wasted API turns** while waiting |
| **Output Budget** | Enforce 300 words max + tool receipts in prompt | **Prevents context bloat** in parent context |
| **Lifecycle Pruning** | Call `manage_subagents(Action: 'kill')` as soon as subagent is `idle` | **Frees memory & sandboxes**, prevents stray notifications |
| **Task Offload** | Use `run_command` with `WaitMsBeforeAsync` for shell scripts/tests | **Prevents stdout spam** from poisoning the LLM context |

---

## Subcommands & Usage

### 1. Launch a Lean Background Subagent
```bash
[bg-agent] "Scan all files in src/ for deprecated API usages" --tier flash_lite --type research
```
**Execution Rules:**
- Select lowest capable model tier (`flash_lite` > `flash` > `pro`).
- Use `research` type for read-only tasks (strips write & MCP tools).
- Inject the Output Contract: 300 words max, lead with conclusions, raw tool receipts.
- Dispatch via `invoke_subagent`.
- **DO NOT POLL.** Stop tool calls and let reactive wakeup deliver the response.

### 2. Inspect Active Background Subagents
```bash
[bg-agent] list
```
**Execution Rules:**
- Calls `manage_subagents(Action: 'list')`.
- Displays table of active subagents: `conversationId`, `role`, `type`, `state` (`running`, `idle`, `waiting_for_input`), and transcript URI.

### 3. Harvest & Terminate (Read-Before-Kill)
```bash
[bg-agent] kill <conversation_id>
[bg-agent] kill all
[bg-agent] clean
```
**Execution Rules:**
- If cleaning up, check subagent transcript or output first (harvest-before-kill invariant).
- Terminate via `manage_subagents(Action: 'kill', ConversationIds: [...])` or `Action: 'kill_all'`.
- Report killed IDs and freed roles.

### 4. Dynamically Define a Custom Micro-Agent
```bash
[bg-agent] define <name> --prompt "<system_prompt>" [--read-only]
```
**Execution Rules:**
- Call `define_subagent` with:
  - `enable_mcp_tools: false`
  - `enable_write_tools: false` (unless explicitly requested)
  - `enable_subagent_tools: false` (enforce leaf execution, prevents recursion)
  - Minimal system prompt under 100 words.

---

## Output Contract (Mandatory Prompt Injection)

Every prompt dispatched through `bg-agent` MUST append:
```markdown
RETURN_FORMAT:
- Max 300 words.
- Lead with actionable conclusions.
- Include tool receipts (file paths, line counts, grepped patterns).
- Do not include narrative filler or internal chain-of-thought.
```

---

## Constraints & Fleet Invariants
- **Concurrency Cap**: Maximum 3 concurrent background subagents (per `subagent-quota-discipline.md`).
- **Complexity Gate**: Do not spawn a subagent for a single-file grep or read; do it directly.
- **Harvest First**: Never kill a subagent before its output has arrived or been inspected (per `background-subagent-policy.md`).
- **Depth Bound**: Subagents cannot spawn subagents (`enable_subagent_tools: false`).
