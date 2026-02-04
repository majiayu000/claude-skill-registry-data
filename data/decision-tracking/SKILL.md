---
name: Decision Tracking
description: ADR management and decision logging. Use when documenting architectural decisions, tracking technical choices, or creating decision records.
---

# Decision Tracking

**CRITICAL: The description field above controls when Claude auto-loads this skill.**

## Instructions

1. Provide templates and patterns for this skill
2. Execute helper scripts when needed
3. Reference documentation and examples

## Available Scripts

- **find-next-adr-number.sh** - Finds the next available ADR number for auto-numbering
- **create-adr.sh** - Creates new ADR with proper numbering and MADR template
- **update-adr-index.sh** - Updates ADR index/README with all ADRs grouped by status

## Templates

Templates ready in `templates/` directory for code patterns and configurations.

## Requirements

- Scripts should be mechanical helpers (deterministic operations)
- Templates should provide reusable patterns
- Documentation should be clear and actionable
