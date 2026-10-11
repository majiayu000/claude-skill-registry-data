---
name: db
description: 'Parse models, migrations, or schema and generate an ERD diagram + DB documentation Arguments: (no arguments — auto-detects models).'
---

# Database Schema ERD

Analyze the database schema and generate an Entity-Relationship Diagram + documentation.

## Instructions

1. Read the primary skill:
   - `${CLAUDE_PLUGIN_ROOT}/skills/codemap-diagram/SKILL.md` — ERD generation rules
2. Read ERD-specific guidance from `${CLAUDE_PLUGIN_ROOT}/skills/codemap-diagram/references/diagram-types.md`

3. Ensure output directories exist: `docs/codemap/diagrams/` — create if missing.

4. Launch the **diagrammer** agent with a prompt to:
   - Auto-detect the ORM (SQLAlchemy, Prisma, TypeORM, Django, raw SQL migrations)
   - Parse all model definitions — tables, columns, types, foreign keys, relationships
   - Review schema quality (missing indexes, naming inconsistencies, missing constraints)
   - Generate ERD as mxGraph XML → save to `docs/codemap/diagrams/erd.drawio` → call drawio-mcp
   - Generate `docs/codemap/DB.md` with table details, relationships, and quality notes