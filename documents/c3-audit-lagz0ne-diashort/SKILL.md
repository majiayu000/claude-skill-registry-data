---
name: c3-audit
description: Use when verifying C3 documentation quality - checks methodology compliance (layer rules, structure, diagrams) and implementation conformance (docs vs code drift)
---

# C3 Audit

## Overview

Verify C3 documentation from two angles:

1. **Methodology Compliance** - Do docs follow C3 layer rules?
2. **Implementation Conformance** - Do docs match code reality?

**Announce:** "I'm using the c3-audit skill to audit documentation."

## Audit Modes

| Mode | Purpose | When |
|------|---------|------|
| **Methodology** | Verify layer rules | After doc changes |
| **Full** | All docs vs code | Periodic health check |
| **ADR** | Verify ADR implemented | After ADR work |
| **ADR-Plan** | ADR ↔ Plan coherence | Before handoff |
| **Container** | Single container audit | After container changes |
| **Quick** | Inventory check only | Fast sanity check |

## Mode 0: Methodology Audit

### Phase 1: Load Layer Rules

Load rules from `references/layer-audit-rules.md` (or layer skill defaults).

### Phase 2: Structure Check

Verify IDs, paths, frontmatter per `references/v3-structure.md`.

### Phase 3: Layer Content Audit

For each doc, verify content matches layer rules:
- Context: Has container inventory, protocols. NO component lists.
- Container: Has component inventory, tech stack. NO step-by-step algorithms.
- Component: Has flow, dependencies. NO sibling relationships.

### Phase 4: Diagram Audit

Verify diagram types appropriate per layer (see `references/layer-audit-rules.md`).

### Phase 5: Contract Chain

Check for orphans (undocumented) and phantoms (documented but missing).

### Phase 6: Load Layer Skills

Load c3-context-design, c3-container-design, c3-component-design for suggestion generation.

### Phase 7: Generate Report

Use template from `references/audit-report-templates.md`.

## Mode 1: Full Audit

1. Load all C3 docs (inventory)
2. Explore codebase (Task tool, Explore agent)
3. Compare: inventory drift, technology drift, structure drift, protocol drift
4. Generate drift report

## Mode 2: ADR Audit

1. Load ADR, extract Changes Across Layers + Verification Checklist
2. Verify each doc change was made
3. Verify code matches (use verification items)
4. **Update Audit Record** in ADR file:
   - Append row to "Audit Runs" table:
     ```
     | YYYY-MM-DD | [layers checked] | PASS/FAIL | [drift found or "None"] |
     ```
   - If PASS: Update "Lifecycle" table row for Implemented
5. If all pass: transition status to `implemented`, rebuild TOC

---

## 📋 ADR STATUS ENFORCEMENT (MANDATORY)

**This applies to Mode 2 (ADR Audit) and any audit that touches ADRs.**

### Status Workflow

```
proposed → accepted → implemented
                   ↘ superseded
                   ↘ deprecated
```

### Status Transition Rules

| Transition | Requirement | Who |
|------------|-------------|-----|
| `proposed` → `accepted` | Design reviewed, approach approved | Human decision |
| `accepted` → `implemented` | All doc changes made, code matches, verification passes | **Audit verifies** |
| Any → `superseded` | New ADR replaces this one (link required) | Human decision |
| Any → `deprecated` | Decision no longer relevant | Human decision |

### Audit Verification for `implemented` Status

**BEFORE transitioning to `implemented`, verify ALL:**

| Check | How to Verify |
|-------|---------------|
| All "Changes Across Layers" made | Each doc modified as specified |
| Verification checklist passes | Each item checked and passes |
| Code matches docs | Implementation conforms to documented changes |
| Implementation Plan complete | All Code Changes done, Acceptance Criteria met |

### TOC Filtering

**Only `status: implemented` ADRs appear in TOC.**

After transitioning to `implemented`:
```bash
# Rebuild TOC using build-toc.sh from plugin
./build-toc.sh
```

### Red Flags - STOP and Fix

🚩 ADR with `implemented` status but verification items unchecked
🚩 ADR in TOC but status is `proposed` or `accepted`
🚩 `superseded` ADR without link to replacement
🚩 Missing `status` field in frontmatter
🚩 Skipping `accepted` (going straight from `proposed` to `implemented`)

### Audit Checklist for ADR Status

- [ ] ADR has `status` field in frontmatter
- [ ] Status is valid (`proposed`, `accepted`, `implemented`, `superseded`, `deprecated`)
- [ ] If `implemented`: all verifications pass
- [ ] If `superseded`: links to replacement ADR
- [ ] TOC only includes `implemented` ADRs

## Mode 3: ADR-Plan Coherence

1. Extract ADR sections + Implementation Plan
2. Verify: Layer Changes → Code Changes (all mapped)
3. Verify: Verifications → Acceptance Criteria (all mapped)
4. Check for orphans, vague locations, untestable criteria

## Mode 4: Container Audit

Focus on single container: technology match, component coverage, pattern compliance.

## Mode 5: Quick Audit

```bash
# Inventory counts only
grep -c "| c3-[0-9]" .c3/README.md
ls -d .c3/c3-[0-9]-*/ 2>/dev/null | wc -l
```

## Checklist

See `references/audit-report-templates.md` for full checklists per mode.

## Related

- `references/layer-audit-rules.md` - Layer compliance rules
- `references/audit-report-templates.md` - Report formats
- `references/v3-structure.md` - ID/path patterns
