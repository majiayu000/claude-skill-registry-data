---
name: yana-ai
version: "0.40.0"
description: "Sovereign-grade safety OS for AI coding agents. 66 hooks, 2,035 skills, L1 memory, circuit breakers, and cross-engine enforcement — blocks rm -rf, force push, pipe-to-shell, and 40+ attack vectors before they reach your repo."
argument-hint: "yana-ai status | yana-ai audit | yana-ai hooks | yana-ai memory"
allowed-tools: Bash, Read, Write
homepage: https://yanacuti1121.github.io/yana-ai/
repository: https://github.com/yanacuti1121/yana-ai
author: yanacuti1121
license: Apache-2.0
user-invocable: true
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      env: []
      optionalEnv: []
      bins:
        - bash
        - python3
        - jq
        - openssl
    homepage: https://yanacuti1121.github.io/yana-ai/
    tags:
      - safety
      - hooks
      - memory
      - agents
      - gates
      - guards
      - circuit-breaker
      - sovereign
      - claude-code
      - codex
      - cursor
      - audit
      - ai-agent
      - agent-os
---

# Yana AI — Sovereign Safety OS

Yana AI is an agent operating system layered on top of Claude Code (and other AI coding agents). It intercepts dangerous commands, enforces safety rules, manages persistent memory, and provides 2,025+ reusable skills.

## What Yana AI does

When loaded, Yana AI automatically:

- **Blocks 40+ attack vectors** via 60 pre/post hooks — `rm -rf`, force push, pipe-to-shell, path traversal, supply chain attacks, and more
- **Enforces rules** across all agent actions using a 9-layer middleware pipeline (injection scan → blast radius → permission check → egress → sanitize → PII scrub → size cap → audit log)
- **Persists memory** in a 2-tier system: L1 Atomic (permanent, hash-chained) and L2 session facts
- **Provides 2,035 skills** covering frontend, backend, IaC, AI/LLM, security, multi-agent, K8s, WebAssembly, and more

## Install

```bash
# Install via skills CLI
npx skills add yanacuti1121/yana-ai

# Or install directly into .claude/
curl -L https://github.com/yanacuti1121/yana-ai/releases/latest/download/yana-ai-latest.zip -o yana-ai.zip
unzip yana-ai.zip -d .claude/
```

## Quick commands

| Command | What it does |
|---------|-------------|
| `/status` | Show hooks, memory, and gate status |
| `/audit` | Run full security audit on repo |
| `/quick-commit` | Safe commit with gate checks |
| `/session-wrap` | Persist session state to L1 memory |
| `/smart-fix` | Auto-fix with feedback loop |
| `/code-review` | Multi-agent code review |

## Safety hooks overview

Yana AI hooks fire on every tool call:

```
PreToolUse:
  - safe-run.sh         — blocks 40+ dangerous command patterns
  - scope-guard.sh      — enforces declared file scope
  - risk-scorer.sh      — rates action risk 0–100
  - token-budget-guard  — prevents runaway token usage

PostToolUse:
  - session-checkpoint  — saves state every 5 tool calls
  - audit-logger        — appends to Merkle hash-chain log

Stop:
  - truth-gate.sh       — warns on completion claims without evidence
```

## Memory system

```bash
# Save a fact to L1 (persists across sessions)
bash core/scripts/add-fact.sh "tag" "fact content" "high"

# Search L1 memory
bash core/scripts/search-facts.sh "tag"

# View session memory
bash core/scripts/list-session-facts.sh
```

## Hard-blocked commands

Yana AI will always block these regardless of context:

```
rm -rf          git push --force     eval "$user_input"
curl ... | bash  DROP TABLE           chmod 777 core/
```

## Cross-engine enforcement

Yana AI enforces safety on all AI coding agents via a shared `safe-run.sh` proxy:

- **Claude Code** — native hooks
- **Codex** — `CODEX_SHELL_EXEC_HOOK` → safe-run.sh
- **Cursor** — `.cursor/rules/` enforcement
- **Aider** — `--before-exec` hook
