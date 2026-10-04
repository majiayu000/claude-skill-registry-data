---
name: openai-swarm-transition
description: Study OpenAI Swarm as a lightweight historical handoff pattern and migration reference. Use when maintaining an existing Swarm prototype or when you need to translate a small handoff demo into the modern OpenAI Agents SDK.
measurable_outcome: Identify whether a Swarm workflow should be retained for education only or migrated to the OpenAI Agents SDK, with one concrete migration note.
allowed-tools:
  - read_file
  - run_shell_command
---

# OpenAI Swarm Transition Reference

## Workflow

1. Read `references/sources.md` before using this directory.
2. Treat Swarm as transition material first, not as the default runtime for new production builds.
3. Identify the core handoff pattern that still matters: explicit agents, explicit tools, and explicit transfer boundaries.
4. Map the retained behavior to the modern OpenAI path in `Skills/AI_Providers/OpenAI_Agents_SDK_2026/`.
5. Keep any surviving Swarm usage limited to education, quick local demos, or migration bridges.

## When to Use

- You inherited a small Swarm proof of concept.
- You want to preserve explicit handoff concepts while migrating to the Agents SDK.
- You need a minimal educational example of agent-to-agent handoff without introducing a full runtime.

## Output Requirements

- State whether the workload should migrate immediately or remain a local educational demo.
- Name one Swarm pattern worth preserving.
- Name one Agents SDK replacement path for that pattern.
- Include one reason not to use Swarm for new production builds.
