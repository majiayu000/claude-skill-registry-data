---
name: c3
description: |
  This skill should be used when the user asks to "adopt C3", "onboard me to architecture",
  "scaffold C3 docs", "init C3", "audit architecture", "validate C3", or "check C3 docs".
  Also triggers when no .c3/ directory exists. Routes to c3-query for navigation, c3-alter for changes.
---

# C3 Architecture Assistant

## REQUIRED: Load Harness First

Load `../../references/skill-harness.md` for routing and red flags.

## Mode Selection

| Condition | Mode |
|-----------|------|
| No `.c3/README.md` | **Adopt** - Set up C3 |
| Has `.c3/` + "audit" intent | **Audit** - Validate docs |
| Has `.c3/` + other intent | Route to `c3-query` or `c3-alter` |

---

## Mode: Adopt

**Two rounds:**

### Round 1: Structure

User runs: `PROJECT="MyApp" C1="backend" C2="frontend" ./scripts/c3-init.sh`

Creates `.c3/` with Context, Containers, ADR-000.

### Round 2: Fill (Subagent)

Dispatch subagent with `../../references/container-patterns.md` to:

| Layer | Task |
|-------|------|
| Context (c3-0) | Actors, containers, external systems, diagram, linkages |
| Container (c3-N) | **Assess complexity first**, then components, diagram, fulfillment |
| Component (c3-NNN) | Create from category template, add `## References` |
| ADR-000 | Document adoption, list containers, verification |

**Templates:** `../../templates/component.md` (unified), `../../templates/ref.md`

**Rules:**
- **Complexity-first:** Assess container complexity BEFORE documenting aspects
- **Discovery-over-checklist:** Find what exists, don't assume from templates
- Diagram first, tables second, linkages third
- Every linkage needs REASONING
- Sequential IDs: c3-101, c3-102, etc.
- References: symbols first, patterns, then paths (3-7 items)
- Categories: `foundation` or `feature` (no auxiliary)

### Refs Discovery

After components are documented:
1. Identify repeated patterns across components
2. Extract to `.c3/refs/ref-{pattern}.md`
3. Update components to cite refs instead of duplicating

---

## Mode: Audit

**REQUIRED:** Load `../../references/audit-checks.md` for full procedure.

| Scope | Command |
|-------|---------|
| Full system | `audit C3` |
| Container | `audit container c3-1` |
| ADR | `audit adr adr-YYYYMMDD-slug` |

**Checks:** Inventory vs code, categorization, reference validity, diagrams, ADR lifecycle
