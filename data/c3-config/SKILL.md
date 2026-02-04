---
name: c3-config
description: Use when configuring project preferences in .c3/settings.yaml - diagram tools, layer guidance, guardrails, and handoff steps
---

# C3 Config

## Overview

Create and refine `.c3/settings.yaml` for project-specific preferences through Socratic questioning.

**Announce at start:** "I'm using the c3-config skill to configure project settings."

## Quick Reference

| Section | Purpose |
|---------|---------|
| `diagrams:` | Diagram tool and usage patterns (global) |
| `context:` | Context layer configuration |
| `container:` | Container layer configuration |
| `component:` | Component layer configuration |
| `guard:` | Team guardrails and constraints |
| `adr:` | ADR and Implementation Plan settings |
| `handoff:` | Post-design handoff steps |
| `audit:` | Audit findings handoff preference |

## Settings Structure

```yaml
diagrams: |
  mermaid
  sequence: API interactions, request flows
  flowchart: decision logic, error handling

context:
  useDefaults: true
  guidance: |
    your context guidance
  include: |
    additional items to include
  exclude: |
    items to exclude
  litmus: |
    custom litmus test (optional)
  diagrams: |
    custom diagram guidance (optional)

container:
  useDefaults: true
  guidance: |
    your container guidance
  # Same keys as context

component:
  useDefaults: true
  guidance: |
    your component guidance
  # Same keys as context

guard: |
  discovered incrementally

adr:
  requirePlan: true
  coherenceCheck: true
  planGranularity: detailed  # detailed | summary

handoff: |
  after ADR accepted:
  1. create implementation tasks
  2. notify team
  target: vibe_kanban  # or: linear, jira, github, manual

audit: |
  handoff: tasks  # tasks | manual | agents
```

For merge logic details, see `references/settings-merge.md`.

## Socratic Refinement

Refine sections through targeted questions:

**Diagrams:**
- "What diagramming tool does your team use?"
- "What types of diagrams are most useful?"

**Layer Configuration (Context/Container/Component):**
- "Use default include/exclude rules, or customize?"
- "Items that should ALWAYS be at this layer?"
- "Items that should NEVER be at this layer?"

**Guardrails:**
- "Architectural decisions that should never be revisited?"
- "Technologies or patterns that are off-limits?"

**ADR Settings:**
- "Should Implementation Plan be required?" (default: yes)
- "Verify ADR-Plan coherence before handoff?" (default: yes)
- "Code Changes granularity?" (detailed: file:function, summary: file-only)

**Handoff:**
- "What happens after an ADR is accepted?"
- "How should tasks be tracked?" (GitHub, Jira, Linear, vibe_kanban, etc.)

**Audit:**
- "How should audit findings be handled?" (manual, tasks, agents)

## Process

### 1. Check Existing Settings

```bash
ls .c3/settings.yaml 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

- **EXISTS**: Load and show current settings
- **MISSING**: Create with defaults

### 2. Initialize or Load

If missing, create with sensible defaults. If exists, load and ask: "Which section would you like to refine?"

### 3. Socratic Refinement

Focus on gaps, one section at a time. User can skip any section.

### 4. Write Settings

Save to `.c3/settings.yaml` and verify sections exist.

## Invocation Contexts

| Context | Behavior |
|---------|----------|
| **Standalone** | Full Socratic refinement of all sections |
| **Via c3-adopt** | Create defaults, offer refinement |

## Key Principles

- **Sensible defaults** - Works out-of-box, customization optional
- **Incremental discovery** - Guardrails grow over time
- **Flexible format** - YAML with prose values
- **User-editable** - Human-readable/editable
- **Non-blocking** - Missing settings doesn't break other skills

## Checklist

- [ ] Checked for existing `.c3/settings.yaml`
- [ ] Initialized or loaded current settings
- [ ] Each section reviewed via Socratic questions
- [ ] Handoff steps configured
- [ ] Settings file saved and verified

## Related

- `references/settings-merge.md` - Merge logic details
- `c3-adopt` - Calls c3-config during initialization
- `c3-design` - Reads settings at start
