---
name: sub-agents
description: Spawn and coordinate sub-agent sessions for parallel work. Use when delegating tasks (research, code, analysis), routing to appropriate models, or managing multi-agent workflows. Trigger on "spawn", "sub-agent", "delegate", "parallel tasks", or when a task would benefit from a different model.
---

# Sub-Agent Orchestration

Spawn isolated sessions to execute tasks in parallel with appropriate model routing.

## Critical: Sub-Agents Are Context-Blind

Sub-agents **do not** see AGENTS.md, SKILL.md, SOUL.md, MEMORY.md, or any workspace context files. They only see:
1. The `task` string you provide
2. Whatever files you tell them to read (via paths in the task)
3. Inline `attachments` you pass at spawn time

**Everything the sub-agent needs must be in the task spec or explicitly referenced as a file path.** This includes output instructions, announce behavior, constraints, and domain knowledge.

## When to Spawn

**Spawn when:**
- Task benefits from a specialized model (code → Codex, research → Sonnet)
- Work can run in parallel while you continue
- Task is self-contained with clear success criteria
- Will block you for >10 seconds (the 10-Second Rule)

**Don't spawn when:**
- Trivial one-liner (just do it yourself)
- Task requires real-time conversation with the user
- Heavy coordination overhead exceeds benefit

## Model Selection

| Task Type | Model (alias) | Full path | Notes |
|-----------|---------------|-----------|-------|
| **Browser automation** | `gpt54` | `openai-codex/gpt-5.4` | **Default for all browser tasks.** Native computer-use. thinking: high auto-applied. |
| Code implementation | `codex` | `openai-codex/gpt-5.3-codex` | Optimized for code gen |
| Quick code/bugs | `codex` | `openai-codex/gpt-5.3-codex-spark` | Faster, simpler tasks |
| Research, writing, quick tasks | `gpt5` | `openai-codex/gpt-5.2` | **Unlimited on Codex sub.** Replaces sonnet/haiku for most work. |
| Complex reasoning | `opus` | `anthropic/claude-opus-4-6` | Deep analysis (expensive) |
| Huge context (>200K tokens) | `sonnet` | `anthropic/claude-sonnet-4-5` | 1M context window fallback |

Use aliases when available. GPT-5.2 is unlimited on the Codex subscription — prefer it over Sonnet/Haiku for sub-agents unless you specifically need Sonnet's 1M context window.

## sessions_spawn Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `task` | ✅ | — | The full task description (only context the sub-agent gets) |
| `model` | — | parent model | Model alias or full provider/model path |
| `thinking` | — | — | `off \| low \| medium \| high` |
| `label` | — | — | Label for logs/UI tracking |
| `runTimeoutSeconds` | — | config default or `0` | Abort after N seconds |
| `cleanup` | — | `keep` | `delete \| keep` — delete removes session after completion |
| `thread` | — | `false` | Thread-bound routing (Discord/Slack) |
| `mode` | — | `run` | `run \| session` — defaults to `session` when `thread=true` |
| `sandbox` | — | `inherit` | `inherit \| require` — require rejects if child isn't sandboxed |
| `agentId` | — | current agent | Spawn under another agent (must be in allowlist) |
| `attachments` | — | — | Inline files: `[{ name, content, encoding?, mimeType? }]` |

### Key behaviors
- **Always non-blocking.** Returns `{ status: "accepted", runId, childSessionKey }` immediately.
- **Sub-agents cannot spawn sub-agents.** No nested spawning. Plan accordingly.
- **Sub-agents get all tools EXCEPT session tools** (no sessions_list/history/send/spawn). Configurable via `tools.subagents.tools`.
- **Auto-archive:** Sessions archive after `agents.defaults.subagents.archiveAfterMinutes` (default: 60).

## Announce Mechanism

After a sub-agent completes, OpenClaw runs an **announce step** that posts results to the requester's chat channel.

- Announce replies are normalized to **Status / Result / Notes** format
- **Status** comes from runtime outcome (success/failure/timeout), not model text
- If the assistant's final reply is empty, the latest `toolResult` is used as Result
- Include a stats line (runtime, tokens, sessionKey, cost)

### Controlling announce behavior

| Sub-agent replies with... | Effect |
|---------------------------|--------|
| Normal text | Posted to requester's channel as the announce |
| `ANNOUNCE_SKIP` | Announce is suppressed — nothing posted |
| Empty reply | Latest toolResult becomes the Result |

**⚠️ Use `ANNOUNCE_SKIP`, not `NO_REPLY`.** `ANNOUNCE_SKIP` is the specific mechanism for sub-agent announce suppression. `NO_REPLY` is a general silent-reply convention that may not suppress the announce step.

## Task Specification — Structured Handoff Protocol

Every spawn should follow this template. Remember: this is the **only context** the sub-agent receives.

### Required Fields

1. **Objective** — One sentence. What the sub-agent must accomplish.
2. **Context** — Structured facts. File paths, API endpoints, constraints, relevant decisions. Not narrative — a reference sheet.
3. **Inputs** — What files/data to read before starting. Be specific: paths, line ranges, sections.
4. **Success criteria** — How to verify done. Testable, not subjective.
5. **Output contract** — Where and how to deliver results. File path, format, schema.

### Optional Fields

6. **Constraints** — What NOT to do. Boundaries, things that already failed.
7. **Domain knowledge** — Project-specific context files to load (e.g., `projects/foo/CONTEXT.md`).
8. **Decisions already made** — Prevent re-litigating settled questions.

### Announce instructions (include in every task)

For silent sub-agents (results consolidated by parent):
```
Write your full analysis to [path].
Your final reply after writing the file should be ONLY: ANNOUNCE_SKIP
```

For sub-agents that should announce their own results:
```
Write results to [path].
Your final reply should summarize what you found — this will be posted to the chat.
```

### Example (Good)
```
OBJECTIVE: Analyze time-of-day patterns in Kalshi BTC spread bot single-fill losses.

CONTEXT:
- Bot code: projects/kalshi-arb/bot/spread_bot.py
- Trade log: projects/kalshi-arb/data/trades.csv (columns: timestamp, action, side, price, fill_type, pnl)
- Key finding: single-fills have 1.8% win rate vs ~83% for dual-fills
- Volume gate already exists at 150K trailing-1

INPUTS:
- Read trades.csv, filter to fill_type="single"
- Read spread_bot.py lines 180-220 (gating logic)

SUCCESS CRITERIA:
- Statistical breakdown of single-fill losses by hour (ET)
- Identify if specific time windows have >2x the loss rate
- Chi-squared or equivalent significance test

OUTPUT:
- Write analysis to projects/kalshi-arb/time-gating-analysis.md
- Include raw data table + recommendation

CONSTRAINTS:
- Don't modify bot code, analysis only
- Flag if sample size < 30 per bucket

Your final reply after writing the file should be ONLY: ANNOUNCE_SKIP
```

### Example (Bad — Don't Do This)
```
Look at the Kalshi bot trades and figure out if time of day matters
for single fills. The bot is in the projects folder somewhere.
Write up what you find.
```

The bad example forces the sub-agent to guess file locations, decide its own success criteria, and has no announce instructions.

## Monitoring & Management

### `subagents` tool (primary orchestration)
```
subagents(action="list")                              // List active sub-agents
subagents(action="steer", target="<id>", message="...") // Send follow-up instructions
subagents(action="kill", target="<id>")               // Kill a running sub-agent
```

### Session tools (for history/cross-session)
```
sessions_list({ kinds: ["other"], activeMinutes: 60 })  // Sub-agents are kind "other"
sessions_history({ sessionKey: "...", limit: 5 })        // Check output
sessions_send({ sessionKey: "...", message: "..." })     // Send to any session
```

### Discovery
```
agents_list()  // Discover which agentIds are allowed for sessions_spawn
```

**Don't poll in loops.** Check on-demand, when prompted, or for debugging.

## Fallback Rules

If a model is rate-limited:
1. **Codex/GPT-5.2 limited** → Use `sonnet` for code/research tasks
2. **Sonnet limited** → Use `gpt5` for research tasks
3. **All limited** → Use `opus` directly (last resort, expensive)

Rate limits typically reset in 30-90 minutes.

## Anti-Patterns

❌ **Spawning for trivial tasks** — Just do simple things yourself
❌ **Vague task specs** — "Look into X" without success criteria or output contract
❌ **Over-parallelization** — Too many concurrent spawns = memory pressure
❌ **Forgetting announce instructions** — Every task must specify ANNOUNCE_SKIP or what to say
❌ **Assuming sub-agents have context** — They don't see your workspace files
❌ **Using `kinds: ["isolated"]`** — The correct kind for sub-agents is `"other"`
❌ **Using `NO_REPLY` for announce suppression** — Use `ANNOUNCE_SKIP`
❌ **Expecting sub-agents to spawn their own sub-agents** — They can't
