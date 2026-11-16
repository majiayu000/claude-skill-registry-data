---
name: github--spec-kit
description: "Spec-Driven Development toolkit của GitHub — specs executable, không phải tài liệu. 5 core commands: constitution→specify→plan→tasks→implement. 30+ agent integrations."
allowed-tools: Bash, Read, Write
user-invocable: true
---

Spec Kit: methodology + toolkit của GitHub — thay vì vibe coding, write spec trước, spec generate implementation. Intent-driven: define "what" trước "how".

## Install

```bash
# Python 3.11+, Git, uv required
specify init my-project --integration claude-code
# hoặc cursor, copilot, codex, gemini-cli...
```

## 5 Core Commands (sequential)

```
/speckit.constitution  — governing principles + development guidelines
/speckit.specify       — requirements + user stories (WHAT & WHY, không TECH)
/speckit.plan          — technical implementation plan với architecture
/speckit.tasks         — actionable ordered task list từ plan
/speckit.implement     — execute tất cả tasks systematically
```

## Optional Commands

```
/speckit.clarify    — giải quyết underspecified areas
/speckit.analyze    — cross-artifact consistency check
/speckit.checklist  — custom quality validation
```

## 3 Development Scenarios

```
Greenfield (0→1)      — production app từ đầu
Creative Exploration  — parallel implementations, test nhiều tech stack
Brownfield            — add features, modernize legacy
```

## Customization Layers

```
Project-local overrides  — one-off adjustments
Presets                  — org-wide template customization
Extensions               — add new capabilities beyond core
Core templates           — default SDD commands
```

## Ví dụ workflow

```
/speckit.constitution   → "This project uses TypeScript strict, no anys..."
/speckit.specify        → "As a user, I can search items by name and filter by date..."
/speckit.plan           → "Use PostgreSQL full-text search, Redis cache 5min TTL..."
/speckit.tasks          → [1. Add search index migration, 2. Create search API endpoint, ...]
/speckit.implement      → execute task 1... task 2... task 3...
```

## Enterprise-Ready

- Organizational constraints + cloud requirements
- Design systems + compliance mandates
- Agile/Kanban/Waterfall/DDD extensions

## Source

https://github.com/github/spec-kit · Apache-2.0 · +398⭐/day
