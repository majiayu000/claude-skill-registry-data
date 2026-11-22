---
name: ecc
description: Everything Claude Code (ECC) — agent harness configuration layer for Claude Code and other AI coding IDEs. Augments agents with skills, hooks, persistent memory, model routing, and quality gates without modifying the underlying model.
license: MIT
compatibility: yana-ai >= 1.3.54
metadata:
  origin: yana-ai — synthesized from affaan-m/ECC (MIT)
  version: 1.0.0
triggers:
  - "ECC"
  - "everything claude code"
  - "agent harness"
  - "agent harness optimization"
  - "claude code harness"
  - "coding agent harness"
  - "hook profile minimal strict"
  - "ECC_HOOK_PROFILE"
  - "agent skills hooks rules"
  - "autonomous loop quality gate"
  - "model route complexity"
  - "harness audit"
  - "loop-start loop-status"
do_not_use_for:
  - Multi-agent pipelines with inter-agent communication — use crewai or smolagents
  - Building LLM apps or chatbots — use langgraph or vercel-ai-sdk
  - Fine-tuning or training models
  - Teams needing Python-native agent framework with eval tooling — use smolagents + deepeval
see_also:
  - smolagents
  - crewai
  - langgraph
  - agent-safety-patterns
---

# ECC — Everything Claude Code Agent Harness

**Source:** affaan-m/ECC (MIT) — runtime configuration harness for AI coding agents

## What ECC Is

A drop-in configuration layer for Claude Code (and Codex, Cursor, Gemini CLI, Zed, Copilot).
It does not modify the model — it wraps the agent runtime with:
- Reusable **skills** (declarative SKILL.md docs auto-loaded into context)
- **Hook automations** (shell scripts on PreToolUse, PostToolUse, SessionStart, Stop)
- **Rules** (always-active guidelines injected every session)
- **Memory** (persistent facts across sessions)
- **Model routing** (send simple tasks to cheap model, complex to power model)

## Directory Layout

```
.claude/
  skills/          ← declarative "when/how to use" docs
  hooks/           ← trigger-based shell scripts
  rules/           ← always-active session guidelines
  memory/          ← persistent facts
  settings.json    ← hook registration + model routing
```

## Hook Profile Gating

```bash
# Control hook strictness without editing files
export ECC_HOOK_PROFILE=minimal    # only safety hooks
export ECC_HOOK_PROFILE=standard   # standard set (default)
export ECC_HOOK_PROFILE=strict     # all hooks, max enforcement

# In hook scripts — check profile:
[[ "${ECC_HOOK_PROFILE:-standard}" == "minimal" ]] && exit 0
```

## Key Built-in Commands

```
/learn           — persist lesson to session memory after solving hard problem
/harness-audit   — audit active hooks + skills, detect drift
/loop-start      — begin autonomous multi-turn iteration loop
/loop-status     — check loop progress and quality gate results
/quality-gate    — enforce coding standards + test coverage + security before commit
/model-route     — route task to cheapest capable model by complexity score
```

## Model Routing Pattern

```json
// .claude/settings.json
{
  "modelRouting": {
    "simple": "claude-haiku-4-5",
    "standard": "claude-sonnet-4-6",
    "complex": "claude-opus-4-8",
    "thresholds": {
      "simple_max_tokens": 200,
      "complex_min_tokens": 800
    }
  }
}
```

## Skill Registration Pattern

```markdown
---
name: my-skill
triggers:
  - "phrase that activates this skill"
do_not_use_for:
  - "overlapping use case — use other-skill instead"
---
# My Skill
...content...
```

## Yana AI Overlap

Yana AI already implements the ECC pattern natively.
Use this skill when:
- Referencing ECC-specific commands (`/harness-audit`, `/quality-gate`)
- Adapting ECC patterns from the affaan-m repo into Yana AI
- Comparing Yana AI's hook system against ECC's `ECC_HOOK_PROFILE` model
