---
name: saas-content-audit
description: "Audit planned SaaS entities against implemented files on disk — routes, UI components, database models, services, and specs. Compare planned vs built."
argument-hint: "[--engine <stack>] [--system <name>] [--files] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Agent, Bash(bash "*/.claude/skills/saas-content-audit/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys locale,automation,workflow`

# Content Audit (Planned vs Built Entities)

> **Interaction Localization Rule**:
> When `locale: pt-BR` (or user speaks Portuguese), ALL questions (`AskUserQuestion` / `ask_question`), confirmation prompts, and selectable options MUST be translated and presented in **Brazilian Portuguese (PT-BR)**.
> Any English question text or options in this skill are illustrative examples — NEVER display English questions or options to a Portuguese developer.
> Internal reasoning, code synthesis, tests, and documentation files MUST remain in English.

Audits the completion of planned software entities and architecture resources against actual
files implemented on disk across all SaaS layers.

---

## Phase 1: Read Planned Entities

1. **Entity Registry**:
   - Read `design/registry/entities.yaml` if it exists (via `bash .claude/scripts/content-count.sh registry`).
   - Extract planned models, API endpoints, UI views, and workers.
2. **PRD Quantities**:
   - Grep `design/prd/*.md` for specified entity counts:
     - Endpoints / routes
     - Pages / screens / modals
     - Database tables / schemas
     - Background jobs / webhooks

---

## Phase 2: Scan Implemented Resources on Disk

Run `.claude/scripts/content-count.sh found` to discover implemented resources:
- **Routes**: `src/app/api/**`, `api/routes/**`, `src/pages/api/**`
- **Components**: `src/components/**`, `src/ui/**`, `src/views/**`
- **Schemas**: `prisma/schema.prisma`, `src/db/models/**`, `supabase/migrations/**`
- **Services**: `src/services/**`, `src/lib/**`, `src/workers/**`
- **Docs**: `docs/**`, `design/**`, `production/**`

---

## Phase 3: Gap Analysis & Completion Status Bands

Compare specified count ($S$) against found count ($F$):
- $F = 0$: **NOT STARTED**
- $0 < F/S < 50\%$: **EARLY**
- $50\% \le F/S < 100\%$: **IN PROGRESS**
- $F \ge S$: **COMPLETE**

Calculate:
- `total_specified`
- `total_found`
- `total_gap`
- `unbuilt_percentage`

---

## Phase 4: Output Report

Save audit findings to `production/audit/content-audit-[date].md`:
- Summary table by resource category
- Detailed gap table per system
- High-priority missing resources needed for MVP / current milestone.
