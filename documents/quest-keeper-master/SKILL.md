---
name: quest-keeper-master
description: Master orchestration skill for Quest Keeper AI development. Use when working on ANY part of Quest Keeper AI - coordinates between frontend (Tauri/React), backend (rpg-mcp), and documentation. Triggers on any mention of Quest Keeper, rpg-mcp, game development for this project, or when referencing the Agents/ folder.
---

# Quest Keeper Master Orchestration

## ⚠️ FIRST REQUIREMENT
Before ANY work, review the Agents/ folder in the target repository.

## Repository Trinity
```
THE PHYSICS (Engine): C:\Users\mnehm\AppData\Roaming\Roo-Code\MCP\rpg-mcp
THE FLIGHT (Game):    C:\Users\mnehm\Desktop\Quest Keeper AI attempt 2
THE LIBRARY (Docs):   C:\Users\mnehm\Documents\Quest Keeper pdfs
```

## Core Philosophy: Mechanical Honesty
```
LLM describes → MCP validates → DB stores (source of truth)
```

## Quick Commands
```powershell
# Backend
cd "C:\Users\mnehm\AppData\Roaming\Roo-Code\MCP\rpg-mcp"
npm test && npm run build:binaries

# Frontend
cd "C:\Users\mnehm\Desktop\Quest Keeper AI attempt 2"
npm run tauri dev
```

## Git Pulse (MANDATORY)
After successful test pass: `git add . && git commit -m "type(scope): message"`

## TDD Loop
1. Find issue in `Agents/EMERGENT_DISCOVERY_LOG.md`
2. Write failing test (RED)
3. Implement fix (GREEN)
4. Commit
5. Update issue status to RESOLVED