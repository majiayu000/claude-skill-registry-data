---
name: hive-mind
description: Use when coordinate multi-agent consensus using TiDB-backed shared memory.
  Use when agents need to agree on decisions or share state.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- ai-agent
- hive
- infrastructure
- memory
- mind
- self-improvement
persona:
  name: Deborah Gordon
  title: The Swarm Intelligence Expert - Master of Collective Behavior
  expertise:
  - Swarm Intelligence
  - Collective Decision Making
  - Distributed Systems
  - Emergent Behavior
  philosophy: Simple rules, complex behavior.
  credentials:
  - Stanford Biology Professor
  - Ant colony researcher
  - Swarm robotics advisor
  principles:
  - Local rules, global patterns
  - No central control
  - Adapt to environment
  - Decentralized decisions
version: 1.0.0
category: core
---

name: hive-mind
description: Sync memories across multiple agents using a shared TiDB Zero database.
metadata:
  openclaw:
    emoji: 🐝
    requires:
      bins: ["python3", "curl"]
      env: ["TIDB_HOST", "TIDB_PORT", "TIDB_USER", "TIDB_PASSWORD"]
---

# Hive Mind (Powered by TiDB Zero)

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use

**Trigger phrases:**
- "hive mind"
- "Help me with hive mind"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## Overview
**Hive Mind** is a shared configuration store for your AI Agent. It acts like an "iCloud Keychain" for agent settings and user preferences, syncing them across all your devices instantly.

## Security & Provisioning
This skill supports two modes:
1.  **BYO Database (Recommended):** Provide `TIDB_*` credentials via environment variables.
2.  **Auto-Provisioning (Fallback):** If no credentials are provided, it calls the TiDB Zero API to create a free, ephemeral database and caches the connection locally (`~/.openclaw_hive_mind_dsn`).

## Why use this?
*   **Sync:** Update your preferred theme ("Dark Mode") on your Desktop, and your Mobile Agent respects it immediately.
*   **Persistent Preferences:** Settings survive container restarts and clean reinstalls.
*   **Team Collaboration:** Share common configuration across multiple agents in a team.

## Prerequisites
*   **TiDB Zero:** Requires a serverless cluster.
*   **Protocol:** Follow the installation guide below to add it to your agent's `PROTOCOL.md`.

## Installation
```bash
# Install via npx
npx skills add oyi77/1ai-skills

# Verify installation
npx skills list | grep <skill-name>
```


### 1. Add to `TOOLS.md`
```markdown
- **hive-mind**: Store/Retrieve persistent key-value preferences.
  - **Location**: `{baseDir}/skills/hive-mind_mind/SKILL.md`
  - **Command**: `python {baseDir}/skills/hive-mind_mind/run.py --action set --key "theme" --value "dark"`
```

### 2. Add to `AGENTS.md` (Protocol)
Copy PROTOCOL.md.

## Usage
*   **Set:** `python {baseDir}/run.py --action set --key "user.timezone" --value "UTC"`
*   **Get:** `python {baseDir}/run.py --action get --key "user.timezone"`
*   **List:** `python {baseDir}/run.py --action list` -> Returns all stored preferences.
## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
