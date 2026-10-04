---
name: dev-cycle
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-06-13
description: "8-phase development cycle: Feature requests, current state, functional planning, frontend, backend planning, backend code, tests, use cases. Iterative framework for systematic software development."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="dev-cycle banner">

> **English** — Official English version of `dev-cycle`.


# Development Cycle (Dev Cycle) (English)

> **Goal:** Structured process from feature request to validated system.
> Every development goes through these 8 phases.

---

## Overview & Purpose

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                         |
  +--------------------------------------------------------------+
  |                                                              |
  |  Phase 1   Feature Requests (functional requirements)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 2   Check Current State (What already exists?)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 3   Functional Planning                               |
  |            (Workflows, Agents, Experts, Skills, Services)    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 4   Implement Functional Frontend                     |
  |            (Skill files, workflow markdown, agent profiles)   |
  |     |                                                        |
  |     v                                                        |
  |  Phase 5   Plan and Align Backend                            |
  |            (CLI handlers, DB schema, API endpoints)          |
  |     |                                                        |
  |     v                                                        |
  |  Phase 6   Implement Backend Tasks                           |
  |            (Python code, tools, DB migrations)               |
  |     |                                                        |
  |     v                                                        |
  |  Phase 7   Technical Tests and Bugfixes                      |
  |            (B/O/E tests, bugfix protocol)                    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 8   Functional and Feature Test: USE CASES            |
  |            (End-to-end validation from user perspective)      |
  |                                                              |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
```

---

## Phase 1: Feature Requests (Functional Requirements)

**What:** Collect and formulate functional requirements.

**Input:**
- User wishes, ideas, problems
- Partner suggestions (LLM assistants)
- Insights from use cases (feedback loop!)

**Output:**
- Tasks in the task system (e.g., as issue, ticket, or TODO list)
- Requirements describe WHAT is desired, not HOW

**Rules:**
- Always formulate requirements functionally ("User can do X")
- Not technically ("Implement REST endpoint for X")
- Use use cases as requirement source (Phase 8 -> Phase 1)

---

## Phase 2: Check Current State

**What:** Inventory existing functionality.

**Checklist:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**Output:**
- Documentation of what exists, what's missing, what needs extension
- Avoidance of duplicates

---

## Phase 3: Functional Planning

**What:** Plan at the functional level - do NOT write code immediately.

**Planning Levels:**

| Level | Question | Artifact |
|-------|----------|----------|
| Workflow | WHEN/HOW is coordination done? | workflows/*.md |
| Agent | WHO executes? | agents/*.txt |
| Expert | WHO has domain knowledge? | experts/*/ |
| Skill | WHAT is done? | skills/*.md |
| Service | HOW is it done technically? | services/*/ |

**Rules:**
- Think functionally first, then technically
- Workflows describe processes, not implementation details
- Every agent needs a clear profile
- Services must work without user data

---

## Phase 4: Implement Functional Frontend

**What:** Create skill files, workflow markdown, agent profiles.

The "frontend" here is the functional description layer:
- Workflow files (.md)
- Agent profiles (.txt)
- Expert knowledge
- Service descriptions
- Help files

**Output:**
- All functional descriptions exist
- An LLM partner could read and understand the workflow
- The functional layer is fully documented

---

## Phase 5: Plan and Align Backend

**What:** Align technical architecture to the functional frontend.

**Planning Areas:**

| Area | Question | Location |
|------|----------|----------|
| CLI Handlers | Which commands? | handlers/*.py |
| DB Schema | Which tables/columns? | schema/*.sql |
| API Endpoints | Which GUI endpoints? | server.py |
| Tools | Which Python scripts? | tools/*.py |

**Output:**
- Technical plan aligned with the functional frontend
- DB schema design
- CLI command structure

---

## Phase 6: Implement Backend Tasks

**What:** Write Python code, DB migrations, CLI handlers.

**Checklist (per task):**
```
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## Phase 7: Technical Tests and Bugfixes

**What:** Ensure technical correctness.

**Test Types (B/O/E):**

| Type | Perspective | Description |
|------|-------------|-------------|
| B-Tests | External/Automated | Automated tests, CI/CD |
| O-Tests | Functional (Input->Output) | Manual functional verification |
| E-Tests | Subjective/Experience | UX evaluation, ergonomics |

**On bugs:**
- Apply the bugfix protocol
- Observe the 20-minute rule (change approach after 20 min)
- Document lessons learned

---

## Phase 8: Functional and Feature Test - USE CASES

**What:** End-to-end validation from user perspective.

**Use cases serve BOTH purposes:**
1. **Feature indicators** - What is desired? What should be possible?
2. **Test scenarios** - Does it actually work from A to Z?

**Use Case Format:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**Feedback Loop:**
- Failed use cases -> new tasks in Phase 1
- Successful use cases -> validated features
- New use case ideas -> capture as tasks

---

## Summary: The Cycle

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                               .    v
       +──────────────────── Phase 5 (Backend Planning)
```

The cycle is a loop: Use cases validate features and simultaneously
generate new requirements.

---

## Phase-specific skills

| Phase | Specialized skill | Trigger |
|-------|-------------------|---------|
| Phases 1-3 | Project bootstrapper (if available) | Create a new project (greenfield) |
| Phase 2 | [project-onboarding](../../project-onboarding/SKILL.en.md) | Take on an existing project |
| Phases 2-3 | [docs-analysis](../../docs-analysis/SKILL.en.md) | Check requirement documents against code |
| Phases 5-6 | [pipeline-optimizer](../../pipeline-optimizer/SKILL.en.md) | Renovate existing structures |
| Phase 7 | [bugfix-protocol](../../bugfix-protocol/SKILL.en.md) | Systematic 6-phase debugging |
| Phases 7-8 | [bugsweep](../../bugsweep/SKILL.en.md) | Converging bug sweep before a release |

If your skill collection has a skill index, search it for further phase-specific skills.

---

## Change Log

### 1.1.0 (2026-06-13)
- New "Phase-specific skills" table with references to project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol, and bugsweep

### 1.0.0 (2026-03-12)
- Ported from BACH (dev-zyklus v1.0.0)

---

*Created: 2026-01-28 | Ported: 2026-03-12*
