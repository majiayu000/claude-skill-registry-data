---
name: workflow_kanban
description: AUTO-ACTIVATE on keywords (workflow, kanban, regras de negócio, transição, processo, estado, automação, patterns, agents, dashboard). Provides comprehensive knowledge and practical tools for developing the Kanban-Workflow system in VibeCForms v4.0. Covers workflow architecture, implementation phases, AI agents, pattern analysis, visual editors, business rules, auto-transitions, and analytics. Use when user mentions workflow-related concepts or business logic.
---

# Workflow Kanban - Sistema de Workflow para VibeCForms

## Overview

Enable development of a complete Kanban-Workflow management system for VibeCForms v4.0. The system combines visual Kanban boards with dynamic forms that automatically generate workflow processes, featuring AI-powered pattern analysis, automated transitions, and comprehensive analytics.

This skill provides five progressive knowledge levels (fundamentals → implementation), three functional Python scripts (validator, template generator, implementation assistant), and pre-configured templates ready for use.

## When to Use This Skill

**AUTOMATIC ACTIVATION**: This skill should be automatically invoked when the user mentions ANY of these keywords or related concepts:

**Primary Keywords:**
- `workflow` / `workflows` / `fluxo` / `fluxos`
- `kanban` / `kanbans` / `quadro kanban`
- `regras de negócio` / `business rules` / `lógica de negócio`
- `transição` / `transições` / `transitions` / `auto-transition`
- `processo` / `processos` / `process` / `workflow process`
- `estado` / `estados` / `state` / `states` / `status`

**Secondary Keywords:**
- `pré-requisito` / `prerequisite` / `prerequisites`
- `automação` / `automation` / `automatic`
- `padrões de workflow` / `workflow patterns`
- `agente` / `agentes` / `AI agents` / `workflow agents`
- `análise de padrões` / `pattern analysis`
- `anomalia` / `anomaly detection`
- `editor visual` / `visual editor` / `kanban editor`
- `dashboard` / `analytics` / `métricas de workflow`
- `audit` / `auditoria` / `timeline`
- `forced transition` / `transição forçada`
- `cascade` / `cascata` / `progressão em cascata`

**Context-Based Activation:**
- Questions about "como implementar" + any workflow-related term
- References to workflow architecture or design
- Discussion of business logic tied to form states
- Planning or reviewing workflow features
- Troubleshooting workflow issues
- Creating or validating kanban configurations

Use this skill when:
- Planning or implementing kanban workflows in VibeCForms
- Creating kanban JSON definitions
- Validating kanban configuration files
- Implementing auto-transition logic
- Developing AI agents for workflow analysis
- Building visual editors or analytics dashboards
- Reviewing workflow architecture decisions
- Planning implementation phases and testing strategy
- Discussing business rules and workflow automation
- Analyzing workflow patterns or anomalies
- Designing state machines or process flows

Do NOT use for:
- General form management (not related to workflows)
- Basic CRUD operations without workflow
- Non-workflow VibeCForms features
- Simple data persistence questions
- UI/UX improvements unrelated to kanban boards

## Progressive Disclosure Knowledge Levels

The skill organizes documentation in five progressive levels. Start at Level 1 and advance as needed:

### Level 1: Fundamentals (Novice)
**Target**: Developers new to the project
**Content**: Core concepts, Kanban-Form architecture (1:N), pluggable persistence
**File**: `references/level_1_fundamentals.md`
**Use when**: Understanding project basics, first time on the project

### Level 2: Engine (Competent)
**Target**: Developers implementing core features
**Content**: AutoTransitionEngine, AI Agents, PatternAnalyzer, complete user flows
**File**: `references/level_2_engine.md`
**Use when**: Implementing transitions, automation, pattern analysis

### Level 3: Interface (Proficient)
**Target**: Developers working on UI/UX
**Content**: Visual Editor, Analytics Dashboard, Exports, Audit Interface
**File**: `references/level_3_interface.md`
**Use when**: Building visual interfaces, dashboards, user-facing features

### Level 4: Architecture (Advanced)
**Target**: Architects and tech leads
**Content**: Complete technical architecture, component diagrams, directory structure
**File**: `references/level_4_architecture.md`
**Use when**: Planning architecture, reviewing technical decisions, integrations

### Level 5: Implementation (Master)
**Target**: Project managers and implementers
**Content**: Complete example (Order Flow), 5 implementation phases (50 days), testing strategy (150+ tests)
**File**: `references/level_5_implementation.md`
**Use when**: Planning implementation, defining schedules, creating tests

## Core Principles

**"Warn, Not Block" Philosophy**: Prerequisites NEVER block transitions. They warn users and require justification for forced transitions, but maintain user autonomy.

**Key Concepts:**
- **Kanban = Workflow Definition**: Kanbans define business rules and workflow logic
- **1:N Kanban-Form Relationship**: One kanban can generate processes from multiple forms
- **Automatic Process Generation**: Saving a form automatically creates a workflow process
- **3 Transition Types**: Manual (user), System (automatic), Agent (AI-suggested)
- **Pluggable Persistence**: TXT (default), SQLite, MySQL, PostgreSQL, MongoDB

## Practical Tools

The skill includes three Python scripts for immediate use:

### 1. Kanban Validator (`scripts/kanban_validator.py`)

Validate kanban JSON files for correctness and completeness.

**Usage:**
```bash
python3 ~/.claude/skills/workflow_kanban/scripts/kanban_validator.py <kanban.json>
```

**Validates:**
- JSON schema correctness
- Required fields (id, name, states, transitions)
- Transition consistency (from/to states exist)
- Prerequisite types (4 valid types)
- Infinite cycle detection in auto-transitions
- Generates detailed error/warning report

**Example:**
```bash
python3 ~/.claude/skills/workflow_kanban/scripts/kanban_validator.py /home/rodrigo/VibeCForms/src/config/kanbans/pedidos.json
```

### 2. Template Generator (`scripts/template_generator.py`)

Generate pre-configured kanban templates ready to use.

**Usage:**
```bash
# List available templates
python3 ~/.claude/skills/workflow_kanban/scripts/template_generator.py --list

# Generate template
python3 ~/.claude/skills/workflow_kanban/scripts/template_generator.py --template order_flow --output pedidos.json
```

**Available Templates:**
- `order_flow` - Complete order workflow (quote → order → delivery → completed)
- `support_ticket` - Support ticket management (new → analysis → resolved)
- `hiring` - Hiring process (candidate → interviews → hired)
- `approval` - Generic approval flow (pending → review → approved/rejected)

**Example:**
```bash
python3 ~/.claude/skills/workflow_kanban/scripts/template_generator.py --template order_flow --output /home/rodrigo/VibeCForms/src/config/kanbans/pedidos.json
```

### 3. Implementation Assistant (`scripts/implementation_assistant.py`)

Guide implementation phase by phase with checklists and progress tracking.

**Usage:**
```bash
# View overview of all phases
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py

# View detailed checklist for Phase 1
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py --phase 1

# Check implementation progress
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py --check
```

**Shows:**
- Checklist of tasks per phase/day
- Deliverables for each phase
- Test counts and targets
- Implementation progress (which files created)

**Example:**
```bash
# View Phase 2 (AutoTransitionEngine) checklist
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py --phase 2
```

## Common Workflows

### Workflow 1: Create New Kanban

```bash
# Step 1: Generate template
python3 ~/.claude/skills/workflow_kanban/scripts/template_generator.py --template order_flow --output my_kanban.json

# Step 2: Customize JSON as needed (edit file)

# Step 3: Validate configuration
python3 ~/.claude/skills/workflow_kanban/scripts/kanban_validator.py my_kanban.json

# Step 4: If valid, copy to VibeCForms
cp my_kanban.json /home/rodrigo/VibeCForms/src/config/kanbans/
```

### Workflow 2: Plan Implementation

```bash
# Step 1: Review overall roadmap
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py

# Step 2: View current phase checklist
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py --phase 1

# Step 3: Check progress regularly
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py --check
```

### Workflow 3: Learn the System

```bash
# Step 1: Read Level 1 for fundamentals
cat ~/.claude/skills/workflow_kanban/references/level_1_fundamentals.md

# Step 2: Progress to Level 2 for engine details
cat ~/.claude/skills/workflow_kanban/references/level_2_engine.md

# Step 3: Consult other levels as needed
# Level 3 for UI, Level 4 for architecture, Level 5 for implementation
```

### Workflow 4: Validate Existing Kanban

```bash
# Validate a kanban file
python3 ~/.claude/skills/workflow_kanban/scripts/kanban_validator.py /path/to/kanban.json

# If errors found, consult Level 1 for structure reference
# Fix errors and re-validate
```

## System Architecture Quick Reference

**Layers:**
- **Presentation**: Kanban Board, Visual Editor, Analytics Dashboard
- **Application**: VibeCForms.py routes, FormTriggerManager, AutoTransitionEngine
- **Business**: ProcessFactory, AI Agents, PatternAnalyzer, PrerequisiteChecker
- **Persistence**: RepositoryFactory → WorkflowRepository → Adapters (TXT/SQLite/MySQL)
- **Storage**: .txt files, SQLite DB, or external databases

**Key Components:**
- **KanbanRegistry**: Bidirectional Kanban↔Form mapping
- **FormTriggerManager**: Detects form saves, triggers process creation
- **ProcessFactory**: Creates workflow processes from form data
- **AutoTransitionEngine**: Handles automatic state transitions
- **PrerequisiteChecker**: Validates prerequisites (4 types: field_check, external_api, time_elapsed, custom_script)
- **AI Agents**: Analyze context and suggest intelligent transitions
- **PatternAnalyzer**: Identifies frequent transition patterns
- **AnomalyDetector**: Detects stuck processes and anomalies

## Implementation Phases Summary

**Phase 1 (10 days)**: Core Kanban-Form Integration
- KanbanRegistry, FormTriggerManager, ProcessFactory
- Basic Kanban Board, Manual transitions
- 30 tests

**Phase 2 (10 days)**: AutoTransitionEngine
- Auto-transitions, Prerequisites (4 types), Timeouts
- Cascade progression, Forced transitions
- 40 tests

**Phase 3 (10 days)**: Basic AI
- PatternAnalyzer, AnomalyDetector
- AI Agents (Base + 3 concrete), UI suggestions
- 40 tests

**Phase 4 (10 days)**: Visual Editor + Dashboard
- Visual Kanban Editor (admin)
- Analytics Dashboard, CSV export
- 30 tests

**Phase 5 (10 days)**: Advanced Features
- Audit timeline, PDF/Excel export
- ML models, Notification system
- 10 tests

**Total**: 50 days, 150+ tests, 80%+ coverage target

## Example Kanban Structure

```json
{
  "id": "pedidos",
  "name": "Fluxo de Pedidos",
  "states": [
    {
      "id": "orcamento",
      "name": "Orçamento",
      "color": "#FFA500",
      "is_initial": true,
      "auto_transition_to": null
    },
    {
      "id": "pedido",
      "name": "Pedido Confirmado",
      "color": "#9370DB",
      "auto_transition_to": "em_entrega",
      "timeout_hours": 48
    }
  ],
  "transitions": [
    {
      "from": "orcamento",
      "to": "pedido",
      "type": "manual",
      "prerequisites": [
        {
          "type": "field_check",
          "field": "valor_total",
          "condition": "not_empty",
          "message": "Valor deve estar preenchido"
        }
      ]
    }
  ],
  "linked_forms": ["pedidos", "pedidos_urgentes"]
}
```

## Quick Reference

**Most Common Commands:**
```bash
# Generate and validate a kanban
python3 ~/.claude/skills/workflow_kanban/scripts/template_generator.py --template order_flow --output kanban.json
python3 ~/.claude/skills/workflow_kanban/scripts/kanban_validator.py kanban.json

# View implementation roadmap
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py

# View phase checklist
python3 ~/.claude/skills/workflow_kanban/scripts/implementation_assistant.py --phase 1
```

**Progressive Learning Path:**
1. Read `references/level_1_fundamentals.md` - Understand concepts
2. Generate example kanban with `template_generator.py`
3. Validate example with `kanban_validator.py`
4. Consult higher levels as needed (2-5)
5. Use `implementation_assistant.py` when implementing

---

**Original Documentation Source:** `VibeCForms/docs/planning/workflow/workflow_kanban_planejamento_v4_parte*.md`
