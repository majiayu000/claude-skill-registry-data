---
name: foundationagents--metagpt
description: "Multi-agent framework — assign roles (PM, architect, engineer) cho GPT team, build software từ 1 requirement. Dùng khi cần orchestrate multi-agent pipeline phức tạp."
allowed-tools: Bash, Read, Write
user-invocable: true
---

MetaGPT: `Code = SOP(Team)` — materialize software company SOPs thành LLM agent team.

## Core idea

Input 1 line requirement → output user stories, competitive analysis, requirements, data structures, APIs, code, docs.

Roles: Product Manager · Architect · Project Manager · Engineer · QA

## Install

```bash
pip install --upgrade metagpt
```

## Quick start

```python
import asyncio
from metagpt.team import Team
from metagpt.roles import ProjectManager, ProductManager, Architect, Engineer

async def main():
    team = Team()
    team.hire([ProductManager(), Architect(), ProjectManager(), Engineer()])
    team.invest(investment=3.0)
    team.run_project("Build a FastAPI CRUD app for task management")
    await team.run(n_round=5)

asyncio.run(main())
```

## MGX — production product

https://mgx.dev — #1 Product of the Week ProductHunt (Mar 2025)

## Source

https://github.com/FoundationAgents/MetaGPT · ⭐68K
