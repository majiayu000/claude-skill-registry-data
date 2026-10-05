---
name: drawio
description: Apply when creating or reviewing architecture diagrams, Mermaid diagrams, or draw.io files.
license: MIT
version: 1.0.0
tokens_target: 1300
triggers:
  - architecture diagram
  - mermaid diagram
  - drawio file
loads_after: []
supersedes: []
---

# Sub-Skill: Diagrams (draw.io / Mermaid)

**Purpose:** Ensure diagrams are version-controlled as source, rendered consistently, and kept in sync with the system they describe.

---

## Rules

### Source Control

1. **Commit source, not just exports.** Always commit diagram source files (`.drawio`, `.mmd`, `.puml`) alongside or instead of rendered image exports. Reference: ERR-2026-027
2. **No binary-only diagrams.** Never commit only a PNG or SVG export without the editable source; reviewers cannot diff or modify a raster image.
3. **One source file per diagram.** Use a single canonical source file per diagram; avoid duplicating the same diagram in multiple formats.

### Format Selection

4. **Prefer diagram-as-code.** Prefer Mermaid or PlantUML over draw.io XML when the diagram fits a supported diagram type; text diffs are reviewable.
5. **Match diagram type to content.** Use `sequenceDiagram` for request flows, `flowchart` for decision logic, `C4Context`/`C4Container` for architecture, `erDiagram` for data models.
6. **Set layout direction explicitly.** Always declare layout direction (`LR`, `TD`) in Mermaid flowcharts; never rely on the default, which varies by renderer.

### Rendering Pipeline

7. **Document the render command.** Always include the render command or CI step in the repo README or Makefile so any contributor can regenerate exports.
8. **Regenerate exports in CI.** Ensure CI regenerates diagram exports from source and fails if the committed export differs from the generated one.
9. **Pin renderer version.** Always pin the Mermaid CLI or draw.io CLI version in CI to prevent silent rendering changes across upgrades.

### Quality & Consistency

10. **Use consistent node naming.** Always use the same label for the same system component across all diagrams in the repo; divergent names cause confusion.
11. **Add alt text to exported images.** Always add descriptive alt text to diagram images embedded in documentation for accessibility.
12. **Review diagrams in PRs.** Before merging, verify that any diagram change accurately reflects the system change described in the PR.

---

## See also

- `skills/svg-check/SKILL.md`
- `skills/error-log/SKILL.md`
