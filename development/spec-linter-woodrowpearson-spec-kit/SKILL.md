---
name: "Spec Linter"
description: "Validates specs have required frontmatter, links, and compliance. Use before commits or during code review."
---

# Spec Linter Skill

## Purpose
Validate:
- Frontmatter completeness
- Test-to-spec traceability
- ADR requirements for architectural changes
- PR template compliance

## Validation Rules
1) Frontmatter required fields by type
2) Test IDs (TC-XXX) present near Swift test methods
3) ADR required when key components/frameworks change
4) Acceptance criteria present for new features
5) PR template sections completed

## Usage
- Pre-commit: `python3 scripts/lint-specs.py`
- CI: see `.github/workflows/spec-lint.yml`
