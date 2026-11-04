---
name: hermes-agent-dissect
description: |
  Navigate and extract reusable design patterns from the Hermes Agent source code for application in our project.
  It covers ten subsystems: bootstrap/CLI, conversation engine, prompt/context, tool system,
  gateway/messaging, skills, terminal backends, memory/persistence, RL training, and integrations (ACP/MCP/plugins).

  Use this skill whenever a user wants to study, reference, or adapt architectural patterns from
  Hermes Agent. Also use it when the user asks questions such as "how does Hermes do this?",
  "learn from Hermes Agent", "dissect Hermes", "reference Hermes source", or requests
  implementation details for any Hermes Agent feature.

  This skill is the primary entry point: it routes to the appropriate reference file by topic,
  then reads the source code and returns extractable patterns. Even when the question appears simple
  (for example, "how does Hermes implement X?"), use this skill because the reference files provide
  precise file paths, reading order, and architectural context that substantially improve answer quality.
---

# Hermes Agent Source Dissection

## Setup

The Hermes Agent source tree lives at `hermes-agent/` in the project root.
Auto-discover the source root by searching for `hermes-agent/run_agent.py` using Glob.
The directory containing it is `SOURCE_ROOT`. All file paths in the reference files are relative to this `SOURCE_ROOT`.

## How to use this skill

1. **Locate the source root**: search the project for `hermes-agent/run_agent.py` using Glob.
   The parent directory of `run_agent.py` is `SOURCE_ROOT`.
2. **Identify the topic** from the user's request
3. **Read the matching reference file** from `references/` below
4. **Read the actual source files** listed in the reference — prepend `SOURCE_ROOT/` to each path
5. **Present your findings** using the output format at the bottom

## Routing Table

| Topic | Reference File | Covers |
|-------|---------------|--------|
| Startup, CLI, config, profiles, auth, credentials | `references/bootstrap.md` | Entry points, config.yaml, credential pool, constants, setup wizard |
| Conversation loop, tool calling, streaming, multi-turn | `references/engine.md` | AIAgent main loop, tool dispatch, parallelization, budget, Honcho |
| System prompt, SOUL.md, context compression, caching | `references/context.md` | Prompt assembly, context files, compressor, cache strategy, tokens |
| Tool definition, registry, toolsets, execution, dispatch | `references/tools.md` | Tool interface, registry singleton, toolset composition, async bridge |
| Gateway, platforms, messaging, Telegram, Discord, Feishu | `references/gateway.md` | GatewayRunner, 14 platform adapters, sessions, delivery, interrupts |
| Skills, SOUL.md parsing, skill hub, security scanning | `references/skills.md` | Progressive disclosure, hub lifecycle, guard patterns, slash commands |
| Terminal execution, Docker, SSH, Modal, local, sandbox | `references/terminals.md` | Backend abstraction, persistent shell, approval, dangerous commands |
| Memory, sessions, persistence, checkpoints, todo | `references/memory.md` | Memory tool, session storage, Honcho integration, checkpoint system |
| RL training, environments, benchmarks, trajectory | `references/training.md` | Atropos base env, OPD, web research, batch runner, compression |
| ACP, MCP, plugins, delegation, model routing | `references/integrations.md` | ACP server, MCP tool bridge, plugin system, subagent delegation |

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
```python
# The core abstraction, stripped to essentials
```
**Files read**: list with line numbers for critical sections
**Design tradeoffs**: what was gained, what was sacrificed
**How to adapt**: what to keep, what to change for our project

## Architecture Overview

For orientation, here's how the 10 subsystems connect:

```
User Input (CLI / TUI / Gateway / ACP)
    |
[bootstrap] -> config.yaml, credentials, profile selection
    |
[engine] -> AIAgent loop: message -> LLM -> stream -> tool calls -> continue/end
    |                                    |
[context] -> prompt assembly        [tools] -> registry -> dispatch -> async bridge
    |           |                       |              |
[memory] <- compression          [skills] <--- [terminals] <- backends
    |                               |              |
    +-- persistence            [training] <- RL environments, benchmarks
                                    |
                          [integrations] -> ACP, MCP, plugins, delegation
                                    |
                            [gateway] -> 14 platforms, sessions, delivery
```

Each reference file contains: architecture knowledge, key abstractions, reading order, file table with line counts, and neighbor cross-references.
