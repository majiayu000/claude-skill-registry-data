---
name: sdd-verify
description: |
  Verify SDD integrity and recover from gaps in web-playground.
  Use when: checking document integrity, fixing broken links, resolving gaps.
  Triggers: "verify sdd", "check integrity", "sdd verify"
---

# Web Playground SDD Verification

Verify integrity across SDD artifacts and recover from gaps.

## Verification Types

| Type | Question | Artifacts |
|------|----------|-----------|
| Alignment | Do REQs serve Foundation? | Foundation <-> Requirements |
| Traceability | Is design justified? | Requirements <-> Design |
| Consistency | No contradictions? | All artifacts |

## Instructions

### 1. Alignment Check (Foundation <-> Requirements)

For each requirement, verify:

| Check | Pass | Fail |
|-------|------|------|
| Coverage | Every anchor has >= 1 REQ | Create GAP for unaddressed anchor |
| Scope | REQ within Foundation scope | Escalate or remove REQ |
| Non-contradiction | Consistent with constraints | Escalate |
| Valid link | `@aligns-to` target exists | Fix link or escalate |

**Run check:**
```bash
# Extract all anchors from foundation
grep -E "^\*\*[A-Z]+-" spec/foundation.md

# Extract all @aligns-to from requirements
grep "@aligns-to:" spec/requirements.md
```

### 2. Traceability Check (Requirements <-> Design)

For each design item, verify:

| Check | Method |
|-------|--------|
| `@derives` exists | Parse design items |
| `@derives` target valid | REQ-ID exists |
| `@rationale` present | Check non-obvious choices |

### 3. Consistency Check

| Check | Vertical | Horizontal |
|-------|----------|------------|
| Non-contradictory | No conflict with source | No conflict with siblings |
| Terminology | Uses source's terms | Consistent across docs |

## Handling Results

### Pass

Update document status in frontmatter to `status: verified`.

### Fail - Self-Resolvable

| Failure | Action |
|---------|--------|
| Missing `@derives` | Add link to correct REQ |
| Missing `@aligns-to` | Add link to correct anchor |
| Typo in reference | Fix the typo |
| Terminology mismatch | Standardize terms |

After fix: re-verify, then mark `verified`.

### Fail - Requires Escalation

**Escalate when:**
- Foundation-level conflict
- Conflicting interpretations
- Missing artifact (not just link)
- User intent ambiguity

Create escalation in `.sdd/state.yaml`:
```yaml
escalations:
  - id: ESC-001
    type: interpretation  # or: scope_decision, contradiction
    description: "REQ-003 and REQ-005 appear to conflict"
    items_affected: [REQ-003, REQ-005]
    status: pending
```

Set affected items to `blocked` and transfer ownership to `human`.

## Gap Documentation

Add gaps to `.sdd/state.yaml`:

```yaml
gaps:
  - id: GAP-001
    severity: major          # critical | major | minor
    type: missing_requirement  # or: missing_design, broken_link, contradiction
    location: spec/foundation.md#QUALITY-MINIMAL
    description: "QUALITY-MINIMAL anchor has no requirements"
    blocking: [design.dependencies]
    owner: unassigned
    created: 2025-01-15
```

## Severity Definitions

| Severity | Definition | Response |
|----------|------------|----------|
| critical | Blocks implementation | Stop, resolve immediately |
| major | Blocks verification | Resolve before next checkpoint |
| minor | Cosmetic or deferred | Track, resolve when convenient |

## Recovery Procedures

### Orphan Design (missing @derives)

1. Find matching REQ in requirements doc
2. If found: add `@derives` link
3. If not found: create GAP for missing requirement, or remove design item

### Orphan Requirement (missing @aligns-to)

1. Find matching anchor in foundation
2. If found: add `@aligns-to` link
3. If not found: question if REQ belongs, escalate

### Broken Link

| Situation | Action |
|-----------|--------|
| Target renamed | Update link to new reference |
| Target deleted | Mark dependent as orphan |
| Typo | Fix the typo |
| Never existed | Find correct target or remove |

### Contradiction

1. Identify authority (Foundation > Requirements > Design)
2. If lower-level wrong: update lower-level
3. If higher-level wrong: escalate
4. Propagate: re-verify dependents

## State Update

After verification:
```yaml
documents:
  requirements: { status: verified, owner: human }
  design: { status: draft, owner: claude }
gaps:
  - { id: GAP-001, severity: major, description: "..." }
escalations:
  - { id: ESC-001, status: pending }  # if any
```

## Verification

- [ ] All anchors have coverage in requirements
- [ ] All REQs have valid `@aligns-to`
- [ ] All design items have valid `@derives`
- [ ] Non-obvious choices have `@rationale`
- [ ] Gaps documented with severity/type/owner
- [ ] State file updated with verification results

## Reference

For full details: `.claude/skills/sdd-guidelines/reference/guidelines-v4.4.md` sections 3, 6
