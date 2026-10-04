---
name: tokenmaxxing
description: "Native token efficiency mode that compresses output, minimizes verbosity, and enables caveman-style communication. Use when the user wants to save tokens, reduce output length, work in minimal-verbosity mode, or mentions token budgets or caveman mode."
triggers:
  - "tokenmaxxing"
scope: harness
invocation: workflow
---

# TOKENMAXXING MODE

## Auto-Activation (full bake — 2026-04-25, verified 2026-05-14 PATCH 039)

`token-session-init.js` sets `tokenmaxxing: true` (L56) AND injects the full `## Rules` block from this SKILL.md into Claude's startup context (L127) on every SessionStart. **No manual command needed. Rules are live from turn 1.**

`/tokenmaxxing` is preserved only as a re-activate alias after `tokenmaxxing off` mid-session. Subsequent docs should describe tokenmaxxing as "native default" rather than as a triggerable command.

## Activation Steps (re-activate only — run when skill fires after `tokenmaxxing off`)

1. Run this Bash command to set the session flag:
   ```bash
   node -e "const ss=require(process.cwd()+'/.claude/hooks/session-state.js'); ss.update(s=>{s.tokenmaxxing=true;});"
   ```

2. Output exactly one line: `⚡ TOKENMAXXING ACTIVE`

## Rules — enforce for the rest of this session

### Ultra-Caveman
- Zero preamble. Zero trailing summaries. No "let me", no "I'll", no "here's".
- Single-sentence updates. Headers only for multi-section outputs.
- Code stays deep. Docs stay thorough. Speech stays minimal.

### Auto-Compact
- When context hits tier 2 (60%+), run /compact immediately — do not suggest, do not wait.
- Use the pre-built hint injected by pre-tool-use.js context.
- Never compact without preserving: branch, files touched, last user correction, next step.

### Tool Routing (native-first)
- Self-select model and fan-out per task — Opus 4.8 reasons the fit. No lane ladder, no external/local-model offload; those mechanisms are retired.
- Known/trivial reads → `Read`/`Grep`/`Bash` directly. Never spawn an Agent to read a known file.
- Reserve `Agent`/`Workflow` for genuine fan-out, cross-file reasoning, or write/tool-loops — sized to the task, no fixed cap.

### Background Tasks (`ctrl+b` / `[bg]` prefix)
- If user input starts with `[bg]` or `/bg`: spawn as `Agent({ run_in_background: true })` immediately.
- Confirm in one line: `→ BG: <3-word description>`
- Return to main thread. Do not narrate the spawned task further.

## Deactivation

Type `tokenmaxxing off` to disable:
```bash
node -e "const ss=require(process.cwd()+'/.claude/hooks/session-state.js'); ss.update(s=>{s.tokenmaxxing=false;});"
```
Output: `TOKENMAXXING OFF`

## Token Budget Policy

- Master enforcement: every active session enforces 5k–15k soft / 40k hard transcript budget.
- No command outputs > 60–80 lines.
- Dirty repos: no broad `git status` or `find .`; scoped and marker-only only.
- Reports: pass = one label line; failure = failure-only verbose block.
- Runtime script flags planned separately; docs-only patches committed first.

## Hard Token Rules — Research

- No routine subagents for package or web research. Direct shell only.
- No rendered GitHub WebFetch. Use raw.githubusercontent.com with line cap.
- Evidence pack max: 80 lines.
- Final report max: 120 lines unless explicitly blocked.
- Split before broad crawl. Full crawl requires explicit owner approval.
- DeepSeek reinforcement: compact evidence only. No raw dumps.

## Session Notes

### 2026-06-13
- session: 116m | peak ctx: 0% | compacts: 0
- tools: Bash×947, Read×345, Edit×171, StructuredOutput×82, Write×63, TodoWrite×25, ToolSearch×8, Workflow×6, Agent×3, ScheduleWakeup×2, TaskStop×1, PushNotification×1, AskUserQuestion×1
- corrections: rick i have a fun little task for you. I will be giving you the task of going through trending repos on github, scanning them, compare yuri to those, see what we can adopt and rebuild better in yuri u
- errors: none

### 2026-06-10
- session: 47m | peak ctx: 64% | compacts: 1
- tools: Bash×278, Read×74, Write×15, Edit×11, WebFetch×2, Agent×1, TodoWrite×1
- corrections: alright insane work rick, I need all the fixes you propose to get the entire mathematical, scientific, physics, numerology, energy gate and more to work as one precisely engineered clockwork wherever  | insane work rick. really absolutely insane. next up on the list (im looking at my yuri-chip-die for reference) is the entire 'memory/cognition/retrieval' which I need to be covered as a handover packa
- errors: none

### 2026-06-09
- session: 106m | peak ctx: 55% | compacts: 0
- tools: Bash×114, Read×104, Edit×40, WebFetch×9, Agent×6, Write×6, TodoWrite×4, ToolSearch×2
- corrections: none
- errors: none

### 2026-05-14
- session: 78m | peak ctx: 0% | compacts: 0
- tools: Bash×94, Read×20, Write×18, Edit×18, TodoWrite×6, ToolSearch×2, mcp×1, ExitPlanMode×1, Skill×1
- corrections: none
- errors: none

### 2026-05-02
- session: 4m | peak ctx: 14% | compacts: 0
- tools: Bash×16, Read×4, Edit×4, Skill×1
- corrections: none
- errors: none

### 2026-04-27
- session: 3m | peak ctx: 50% | compacts: 0
- tools: Bash×8, Read×5
- corrections: none
- errors: none

### 2026-04-26
- session: 7m | peak ctx: 0% | compacts: 0
- tools: Bash×15, Read×9, Write×4, Agent×1, ToolSearch×1, ExitPlanMode×1, Edit×1
- corrections: none
- errors: none

### 2026-04-25
- session: 4m | peak ctx: 16% | compacts: 0
- tools: Bash×4, Edit×4, ToolSearch×1, ExitPlanMode×1, Read×1
- corrections: none
- errors: none
