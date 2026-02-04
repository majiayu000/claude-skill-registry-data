---
name: docs-structure-maintainer
description: Understand and maintain HuleEdu documentation and task documentation structure. Guides placement, naming, and validation using the canonical specs and management scripts.
---

# Documentation Structure Maintainer

Compact skill for reasoning about HuleEdu documentation layout and TASKS structure, and for invoking the right scripts to keep them compliant.

## When to Use

Activate when the user:
- Creates, moves, or renames documentation under `documentation/` or `TASKS/`
- Asks where a doc should live (operations vs decisions vs how-to vs tasks)
- Wants to validate or migrate documentation structure
- Mentions `validate_docs_structure.py`, `migrate_docs_structure.py`, `task_mgmt`, or doc/TASKS specs

## Core Capabilities

- Classify content type and map it to the correct directory:
  - `documentation/overview|architecture|services|operations|how-to|reference|decisions|product|research`
  - `TASKS/` domain taxonomy: `programs/`, `assessment/`, `content/`, `identity/`, `frontend/`, `infrastructure/`, `security/`, `integrations/`, `architecture/`, `archive/`
- Suggest compliant filenames and directory names (kebab-case, no spaces; id-based filenames in `TASKS/`)
- Ensure required frontmatter for:
  - Runbooks and ADRs (per `documentation/DOCS_STRUCTURE_SPEC.md`)
  - Task and programme docs (per canonical TASKS spec)
- Propose concrete commands for:
  - `python scripts/docs_mgmt/validate_docs_structure.py [--strict]`
  - `python scripts/docs_mgmt/migrate_docs_structure.py ...`
  - `python scripts/task_mgmt/new_task.py ...`
  - `python scripts/task_mgmt/validate_front_matter.py ...`
  - `python scripts/task_mgmt/index_tasks.py ...`

## Quick Workflow

1. Identify doc intent (architecture, runbook, ADR, how-to, product, task, programme).
2. Map to the correct directory using `DOCS_STRUCTURE_SPEC.md` and the TASKS structure spec.
3. Choose or normalize filename and directory name to match naming rules.
4. Ensure or suggest correct frontmatter for the doc type.
5. Recommend validation/migration commands using `scripts/docs_mgmt` and `scripts/task_mgmt`.

## Reference Documentation

- **Detailed Workflows & Patterns**: See `reference.md` in this directory
- **Real-World Usage Examples**: See `examples.md` in this directory
- **Normative Rules**: `.claude/rules/090-documentation-standards.md`
