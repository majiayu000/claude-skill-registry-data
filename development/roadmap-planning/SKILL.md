---
name: roadmap-planning
description: Use when planning strategic roadmaps across the autonomous startups.studio ecosystem - creates hierarchical beads issues across repos/submodules from top-level vision down to component sub-roadmaps for business-as-code, services-as-software, and related packages
---

# Roadmap Planning

Strategic planning for the autonomous startups.studio ecosystem, manifesting vision into actionable beads issues across multiple repos and submodules.

## Overview

**Vision**: An autonomous startups.studio generating millions of profitable startups - permutations solving every occupation × industry × process × task × tool × tech × business model combination through Business-as-Code and AI-delivered Services-as-Software.

**Critical Path**: Platform → Products → Sales-Builder (autonomous 1-to-n demand-gen for profitability)

## When to Use

- Planning quarterly/annual roadmaps
- Aligning work across repos (db.sb, ui, platform)
- Creating strategic epics from vision
- Reviewing progress against vision
- Onboarding to understand the ecosystem

## Ecosystem Architecture

```
startups.studio (Vision Layer)
    ↓
┌───────────────────────────────────────────────────────┐
│ Platform Core                                          │
│ ├── db.sb      (AI-powered backend)                   │
│ ├── api.sb     (TypeScript client & schemas)          │
│ └── ui         (mdxui component system) [submodule]   │
├───────────────────────────────────────────────────────┤
│ Business Logic                                         │
│ ├── business-as-code    (Business definition DSL)     │
│ ├── services-as-software (AI-delivered services)      │
│ └── autonomous-agents   (Agent orchestration)         │
├───────────────────────────────────────────────────────┤
│ Builders (Value Creation)                              │
│ ├── startup-builder    (Create startups from specs)   │
│ ├── services-builder   (Create service products)      │
│ └── sales-builder      (Autonomous demand-gen) ★      │
└───────────────────────────────────────────────────────┘
    ↓
Millions of Autonomous Profitable Startups
```

**★ sales-builder is critical** - requires solid platform + amazing products first, but is the key to autonomous scalable profitability.

## Multi-Repo Beads Strategy

### Repo Prefixes
| Repo | Prefix | Scope |
|------|--------|-------|
| db.sb (main) | `db.sb-xxx` | Platform, API, integrations |
| ui (submodule) | `ui-xxx` | Components, templates, design |
| platform | `platform-xxx` | Core ontology, agents |

### Hierarchy Pattern
```
Vision Epic (db.sb)
├── Platform Epic (db.sb)
│   ├── Component Epic (ui submodule)
│   │   └── Tasks (ui)
│   └── Tasks (db.sb)
├── Product Epic (db.sb)
│   └── Tasks (db.sb)
└── Sales Epic (db.sb)
    └── Tasks (db.sb)
```

### Cross-Repo Dependencies
Use issue IDs across repos:
```bash
bd dep add db.sb-sales-epic db.sb-product-epic  # Sales depends on Products
bd dep add db.sb-product-epic ui-components     # Products depend on UI
```

## Roadmap Planning Workflow

### Phase 1: Vision Analysis
1. Read existing vision documents (research/, growth/, notes/)
2. Identify strategic themes
3. Map to ecosystem components

### Phase 2: Current State Assessment
```bash
# Main repo
bd stats
bd list --status=open --type=epic

# Each submodule
cd ui && bd stats && bd list --status=open --type=epic && cd ..
```

### Phase 3: Gap Analysis
Compare vision themes against existing epics:
- What's missing?
- What's blocked?
- What's the critical path?

### Phase 4: Create Roadmap Structure

**Create epics in parallel using subagents when possible:**

```bash
# Top-level strategic epics (main repo)
bd create --title="Q1: Platform Foundation" --type=epic --priority=0
bd create --title="Q2: Product Excellence" --type=epic --priority=1
bd create --title="Q3: Sales Automation" --type=epic --priority=1

# Component epics (submodules)
cd ui
bd create --title="mdxui Complete Type System" --type=epic --priority=1
cd ..
```

### Phase 5: Decompose Epics to Tasks

Each epic should have 5-15 concrete tasks:
```bash
bd create --title="Implement business-as-code DSL parser" --type=task --priority=2
bd dep add <task-id> <epic-id>
```

### Phase 6: Map Dependencies
```bash
bd dep add <downstream-task> <upstream-task>
bd blocked  # Verify dependency graph
```

## Priority Framework

| Priority | Meaning | Use For |
|----------|---------|---------|
| P0 | Critical path blocker | Platform foundations, security |
| P1 | Strategic milestone | Product features, integrations |
| P2 | Important | Quality, DX improvements |
| P3 | Nice to have | Polish, optimization |
| P4 | Backlog | Ideas, future consideration |

## Strategic Themes

### 1. Platform Foundation
- db.sb collections and API completeness
- api.sb type safety and SDK
- Authentication, payments, communications

### 2. Business-as-Code
- DSL for defining businesses declaratively
- MDX-based business definitions
- Git-native business management
- Bidirectional sync (code ↔ database)

### 3. Services-as-Software
- AI-delivered professional services
- Function types: Code, Generative, Agentic, Human
- GDPval framework implementation
- Service templates and patterns

### 4. UI/UX Excellence (ui submodule)
- mdxui type system (SiteComponents, AppComponents)
- Zero components integration
- Auto-wiring to Payload collections
- Visual regression testing

### 5. Autonomous Demand-Gen (sales-builder)
- Template-based campaign generation
- 1-to-n scaling (one template → millions of variations)
- ICP targeting via O*NET × NAICS matrix
- Autonomous outreach and conversion

## Session Protocol

### Starting a Roadmap Session
```bash
# 1. Sync all repos
bd sync
cd ui && bd sync && cd ..

# 2. Review current state
bd stats
bd ready
bd blocked
```

### Creating Cross-Repo Roadmap
```bash
# Use subagents for parallel epic creation across repos
# Main thread coordinates, subagents create in each repo
```

### Ending a Roadmap Session
```bash
# 1. Verify all issues created
bd list --status=open

# 2. Sync changes
bd sync
cd ui && bd sync && cd ..

# 3. Git commit and push
git add -A
git commit -m "roadmap: create Q1 strategic roadmap"
git push
```

## Common Patterns

### Quarterly Planning
1. Review previous quarter's epics
2. Close completed, carry forward in-progress
3. Create new quarter's strategic epics
4. Decompose into monthly milestones
5. Create initial tasks for month 1

### Adding New Submodule
1. `bd init` in new submodule
2. Create roadmap epic linking to main vision
3. Add cross-repo dependencies
4. Document prefix in this skill

### Reviewing Progress
```bash
bd stats                    # Overall health
bd list --status=in_progress # Active work
bd blocked                  # Bottlenecks
bd show <epic-id>           # Epic detail with deps
```

## Anti-Patterns

**DON'T:**
- Create issues without connecting to vision
- Skip cross-repo dependency mapping
- Let epics grow beyond 15 tasks (split them)
- Forget to sync beads before/after sessions
- Plan sales-builder before platform/products ready

**DO:**
- Start from vision, decompose down
- Use parallel subagents for multi-repo creation
- Keep critical path visible (sales-builder dependencies)
- Review and prune regularly
- Celebrate closed epics

## Quick Reference

| Command | Purpose |
|---------|---------|
| `bd stats` | Project health overview |
| `bd ready` | Tasks with no blockers |
| `bd blocked` | Blocked issues |
| `bd dep add A B` | A depends on B |
| `bd create --type=epic` | Strategic milestone |
| `bd close <id1> <id2>...` | Close multiple |
| `bd sync` | Sync with git remote |
