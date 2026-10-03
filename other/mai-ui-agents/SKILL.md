---
name: mai-ui-agents
title: "MAI-UI: Real-World Centric Foundation GUI Agents"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.22047
keywords: [agents, gui-automation, reinforcement-learning, real-world, multi-modal]
description: "Scale GUI agents to real-world complexity via extended action space (user interaction, tool calls) and device-cloud collaboration. Online RL supports 500+ parallel environments with asynchronous handling; local agent monitors trajectory alignment and handoffs to cloud when drift detected—achieving 41.7% MobileWorld success with privacy-preserving delegation."
---

## Overview

MAI-UI addresses critical limitations in existing GUI agents through pragmatic design choices: extended actions enable richer interactions, device-cloud collaboration preserves privacy, and online RL at scale improves agentic reasoning.

## Core Technique

**Extended Action Space:**
Beyond pure UI operations, agents can request clarification and invoke tools.

```python
class ExtendedActionSpace:
    # Actions: click, type, scroll, + new ones
    user_ask = "ask_user"      # Request clarification
    mcp_call = "mcp_call"      # Use external tools
```

**Device-Cloud Collaboration:**
Local agent monitors alignment; cloud only handles complex cases.

```python
class HybridAgent:
    def should_handoff_to_cloud(self, trajectory, instruction):
        deviation = self.alignment_monitor.evaluate(trajectory)
        if deviation > threshold:
            return True  # Handoff to cloud
        return False  # Continue locally
```

## Key Performance

- 73.5% grounding (ScreenSpot-Pro)
- 76.7% mobile navigation (AndroidWorld)
- 41.7% real-world tasks (MobileWorld)
- 500+ parallel environments

## References

- Extended action space design
- Device-cloud collaboration architecture
- Online RL with asynchronous parallelism
