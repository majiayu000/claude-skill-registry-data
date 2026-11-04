---
name: claude-code-dissect
description: |
  Navigate and extract reusable design patterns from the Claude Code 2.1.88 source code for application in our project.
  It covers nine subsystems: startup/bootstrap, conversation engine, context compaction, tool system,
  permissions, hooks, multi-agent orchestration, memory, and extensions (MCP/plugins/skills/UI).

  Use this skill whenever a user wants to study, reference, or adapt architectural patterns from
  Claude Code. Also use it when the user asks questions such as "how does Claude Code do this?",
  "learn from Claude Code", "dissect Claude Code", "reference Claude Code source", or requests
  implementation details for any Claude Code feature.

  This skill is the primary entry point: it routes to the appropriate reference file by topic,
  then reads the source code and returns extractable patterns. Even when the question appears simple
  (for example, "how does Claude Code implement X?"), use this skill because the reference files provide
  precise file paths, reading order, and architectural context that substantially improve answer quality.
---

# Claude Code Source Dissection

## Setup

This skill requires the Claude Code source extracted from its sourcemap. To obtain it:

1. `npm pack @anthropic-ai/claude-code` → get the tarball
2. Extract `cli.js.map` from the tarball
3. Run the extraction script (see `extract-sources.js` in the repo) to restore source files

The extracted source tree should live somewhere in your project. The skill will auto-discover
it by searching for `restored-src/src/Tool.ts` (a unique marker file).

## How to use this skill

1. **Locate the source root**: search the project for `restored-src/src/Tool.ts` using Glob.
   The directory containing it (minus `/Tool.ts`) is `SOURCE_ROOT`.
   All file paths in the reference files are relative to this `SOURCE_ROOT`.
2. **Identify the topic** from the user's request
3. **Read the matching reference file** from `references/` below
4. **Read the actual source files** listed in the reference — prepend `SOURCE_ROOT/` to each path
5. **Present your findings** using the output format at the bottom

## Routing Table

| Topic | Reference File | Covers |
|-------|---------------|--------|
| Startup, init, bootstrap, state, session storage, git | `references/bootstrap.md` | Boot sequence, global state singleton, session JSONL, git worktree |
| Conversation loop, API call, streaming, retry, messages | `references/engine.md` | Query loop, streaming generator, retry strategies, message normalization |
| System prompt, CLAUDE.md, compaction, prompt cache, tokens | `references/context.md` | 5-level prompt assembly, summarizer agent, cache strategy, token budget |
| Tool definition, execution, schema, deferral, Bash parser | `references/tools.md` | Tool interface, lazy schema, execution pipeline, ToolSearch, Bash AST |
| Permission, allow/deny, classifier, safety, rules | `references/permissions.md` | 10-step pipeline, rule matching, YOLO classifier, filesystem guards |
| Hooks, PreToolUse, PostToolUse, lifecycle events | `references/hooks.md` | Hook definition, matching, execution, permission hooks |
| Agent, subagent, teammate, swarm, fork, multi-agent | `references/agents.md` | 3 spawn modes, fork cache optimization, swarm backends, file mailbox |
| Memory, MEMORY.md, extraction, session memory | `references/memory.md` | 3-layer memory, auto extraction, session summary, team sync |
| MCP, plugin, skill, marketplace, IDE bridge, UI, Ink | `references/extensions.md` | MCP client, plugin lifecycle, skill format, IDE bridge, Ink render engine |

If the topic spans multiple areas, read the primary reference first, then follow its **Neighbors** section to related files.

If no topic matches, grep the source root for relevant keywords before giving up.

## Output Format

Structure your response like this:

**Pattern**: one-line name
**Why it exists**: 2-3 sentences on the problem it solves
**Data flow**:
```
ASCII diagram showing runtime flow
```
**Key code** (from the source, simplified):
```typescript
// The core abstraction, stripped to essentials
```
**Files read**: list with line numbers for critical sections
**How to adapt**: what to keep, what to change for our project

## Architecture Overview

For orientation, here's how the 9 subsystems connect:

```
User Input
    ↓
[bootstrap] → init, state singleton, session restore
    ↓
[engine] → query loop: message → API → stream → tool execution → continue/end
    ↓                                    ↓
[context] → prompt assembly        [tools] → validate → permission → hooks → call
    ↓           ↓                       ↓              ↓            ↓
[memory] ← compaction            [agents] ←──── [permissions] ← [hooks]
    ↑                               ↓
    └──── extraction ←────── [extensions] → MCP, plugins, skills, UI
```

Each reference file contains: architecture knowledge, key abstractions, reading order, file table with line counts, and neighbor cross-references.
