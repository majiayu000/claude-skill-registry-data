---
name: learn
description: "Access CTO system documentation and learn how components work. Use when user asks 'how does X work', 'show me how to', 'explain the', 'what is', 'learn about', '/learn', or needs help understanding the system."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# System Learning & Documentation

## Setup
Before starting: check `.handoff/sessions/` for active sessions, read context `status.yaml`, run `git status`. Follow `.rules/universal.md` (Plan -> Approve -> Execute).

<!-- Rules loaded from .rules/universal.md -->

Provide access to CTO system documentation.

## Commands

- `/learn` - Show documentation index
- `/learn skills` - List all skills and commands
- `/learn contexts` - Context system overview
- `/learn sops` - List all SOPs
- `/learn {topic}` - Learn about a specific topic

## System Overview

### Context System

All work lives under `contexts/`. Each context has: `AGENTS.md`, `status.yaml`, `projects/`, `plans/`, `docs/`.

| Shortcut | Context | Type |
|----------|---------|------|
| `@work`, `@company` | work | Employment |
| `@client-a` | client-a | Consulting |
| `@personal`, `@learn` | personal | Personal |

### Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Auto-loaded session memory |
| `AGENTS.md` | Full system architecture |
| `pos.yaml` | All context definitions |

## Skills Quick Reference

| Category | Skills |
|----------|--------|
| Session/Context | `/ctx`, `/session`, `/dashboard`, `/time` |
| Development | `/code-review`, `/plan-generation`, `/security-audit`, `/frontend-design`, `/verification` |
| Team Management | `/status`, `/sprint`, `/team`, `/project`, `/repo` |
| Cross-Agent | `/handoff`, `/work-log`, `/deploy` |
| Reporting | `/dashboard`, `/rollup`, `/projects` |
| Personal | `/curriculum`, `/schedule`, `/draft` |
| Marketing | `/product-marketing` |

## Process for `/learn {topic}`

1. Check skills: `Read: .skills/{topic}.md`
2. Check SOPs: `Read: docs/system/sops/{topic}.md`
3. Search broadly: `Grep(pattern="{topic}", path=".")`

## Key Locations

| Resource | Path |
|----------|------|
| Skills | `.skills/*.md` |
| SOPs | `docs/system/sops/*.md` |
| Context registry | `pos.yaml` |

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
