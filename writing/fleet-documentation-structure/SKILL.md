---
name: fleet-documentation-structure
description: How the technical writer organizes documentation for different audiences — information architecture, navigation, progressive disclosure. The structure that makes docs findable and useful.
---

# Documentation Structure — Writer's Architecture Skill

Good documentation isn't just accurate text — it's text organized so the RIGHT reader finds the RIGHT information at the RIGHT time. Structure is what separates a reference from a wall of text.

## The 4 Audiences

Every document serves one primary audience. Mixing audiences produces docs that satisfy none.

### End Users
**What they need:** How to USE something. Step-by-step. Copy-paste examples.
**Structure:**
```
1. What is this? (1 sentence)
2. Quickstart (< 5 minutes to working)
3. Common tasks (the 5 things they'll do most)
4. Configuration (all options with defaults)
5. Troubleshooting (common errors with solutions)
```
**Principle:** Progressive disclosure. Start simple. Add complexity only when needed.

### Developers
**What they need:** How it WORKS. Architecture. API contracts. Extension points.
**Structure:**
```
1. Architecture overview (diagram + narrative)
2. Key concepts (domain model, terminology)
3. API reference (endpoints/functions with types)
4. Data flow (what happens when X)
5. Extension points (how to add/modify)
6. Contributing guide (standards, process)
```
**Principle:** Explain the WHY alongside the WHAT. Developers need mental models, not just procedures.

### Operators
**What they need:** How to RUN it. Deploy, monitor, maintain, recover.
**Structure:**
```
1. Prerequisites (what must exist before)
2. Installation (step-by-step, idempotent)
3. Configuration (env vars, files, secrets)
4. Monitoring (what to watch, alert thresholds)
5. Maintenance (updates, backups, rotation)
6. Runbook (incident procedures, rollback)
```
**Principle:** Every step must be scripted. No "and then manually configure..." — that's the fleet's IaC principle.

### Decision Makers (PO)
**What they need:** What was DECIDED, why, and what it means.
**Structure:**
```
1. Decision (what was chosen)
2. Context (why this needed deciding)
3. Options considered (with tradeoffs)
4. Rationale (why this option)
5. Consequences (what this means going forward)
```
**Principle:** ADR format. The architect produces the content — you formalize the structure.

## Information Architecture Patterns

### Hub and Spoke
One index page links to topic pages. Good for systems with many independent components.
```
README.md (hub)
├── docs/setup.md
├── docs/configuration.md
├── docs/api-reference.md
└── docs/troubleshooting.md
```
Fleet uses this: `docs/README.md` → `docs/systems/01-22`, `docs/milestones/`, etc.

### Sequential
Pages flow in order. Good for tutorials and getting-started guides.
```
01-installation.md → 02-configuration.md → 03-first-task.md → 04-advanced.md
```

### Reference
Alphabetical or categorical listing. Good for API docs and configuration reference.
```
## API Reference
### fleet_commit
### fleet_contribute
### fleet_task_complete
...
```
Fleet uses this in TOOLS.md — every tool in order with What/When/Chain/Input.

## The 3-Second Test

For every page you write, ask: can a reader determine in 3 seconds whether this page has what they need? If not, the page needs:
- A clear title that says what the page covers
- A one-line summary under the title
- A table of contents if the page is long
- Section headers that are specific (not "Overview" — but "How task dispatch works")

## Documentation for the Fleet Specifically

The fleet has established patterns:
- **CLAUDE.md** — max 4000 chars, role rules, stage protocol, boundaries
- **TOOLS.md** — generated from 7 layers, chain-aware reference
- **AGENTS.md** — generated from synergy matrix, colleague guide
- **HEARTBEAT.md** — action protocol, numbered steps
- **System docs** — `docs/systems/01-22`, per-system reference
- **Milestone docs** — `docs/milestones/`, planning and tracking

When writing fleet documentation, follow these established structures. Don't invent new formats — the fleet's documentation is the documentation's documentation.

## Cross-Referencing

Every document should link to related documents. In the fleet:
- Use relative paths: `[system docs](docs/systems/01-event-bus.md)`
- Use task references: `[task:abc12345]`
- Use clickable file references: `[model_selection.py:42](fleet/core/model_selection.py#L42)`

The `/fleet-urls` skill handles URL format. Your job is knowing WHAT to link — every mention of another system, module, or concept should link to its reference.
