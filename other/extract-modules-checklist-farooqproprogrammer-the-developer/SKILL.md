---
name: extract-modules-checklist
description: >
  Extract modules, seams, and ownership from the codebase (or a named area) and
  produce an actionable checklist. Use when surveying architecture, planning a
  refactor/migration, inventorying features, or when the user asks for a module
  checklist or invokes /extract-modules-checklist.
---

# Extract modules → checklist

Survey the codebase (or a scoped path the user names), identify **modules**, and emit a **checklist** the team can tick through. Prefer CodeGraph (`codegraph_explore`) for structural discovery before grep/Read loops. Use `codebase-design` vocabulary (module, interface, seam, depth).

## Inputs

- Whole repo (default), or a path / package / feature area the user names
- Optional focus: “checklist for migration”, “test ownership”, “public API surface”

If scope is unclear, ask once. Do not invent modules that are not evidenced in the tree.

## Process

```
Progress:
- [ ] 1. Scope confirmed
- [ ] 2. Structural map via codegraph_explore (fallback: package/dir layout)
- [ ] 3. List modules with purpose, seam, and key entry files
- [ ] 4. Emit checklist (template below)
- [ ] 5. Call out orphans, cycles, and missing seams
```

Rules:

- One checklist item per module (or per seam if the user asked for seams).
- Prefer existing package/folder boundaries over inventing new ones.
- Mark depth: deep (small interface, rich impl) vs shallow (leaky).
- Keep items actionable (`[ ]` markdown checkboxes).
- Ponytail: smallest useful inventory — no architecture essay.

## Output template

```markdown
# Module checklist — <scope>

## Summary
- Modules found: N
- Primary seams: …
- Notes: …

## Checklist

- [ ] **`<module-name>`** — <one-line purpose>
  - Seam / public interface: …
  - Entry: `path/…`
  - Depends on: …
  - Depth: deep | shallow
  - Owner / risk: …

(repeat per module)

## Cross-cutting
- [ ] Shared utils / platform kits inventoried
- [ ] Circular deps or leaky seams noted
- [ ] Orphan / dead modules called out (or “none”)

## Next actions
1. …
```

## Optional follow-ups

Only if asked: turn checklist into Spec Kit tasks, assign test seams (`tdd`), or deepen one module via `codebase-design`.
