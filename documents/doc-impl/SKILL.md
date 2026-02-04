---
name: doc-impl
description: Create Implementation Approach (IMPL) - Optional Layer 8 artifact documenting WHO-WHEN-WHAT implementation strategy
tags:
  - sdd-workflow
  - layer-8-artifact
  - shared-architecture
custom_fields:
  layer: 8
  artifact_type: IMPL
  architecture_approaches: [ai-agent-based, traditional-8layer]
  priority: shared
  development_status: active
  skill_category: core-workflow
  upstream_artifacts: [BRD,PRD,EARS,BDD,ADR,SYS,REQ]
  downstream_artifacts: [CTR,SPEC,TASKS]
---

# doc-impl

## Purpose

Create **Implementation Approach (IMPL)** documents - Optional Layer 8 artifact in the SDD workflow that documents WHO will implement WHAT by WHEN, providing implementation strategy and resource allocation.

**Layer**: 8 (Optional)

**Upstream**: BRD (Layer 1), PRD (Layer 2), EARS (Layer 3), BDD (Layer 4), ADR (Layer 5), SYS (Layer 6), REQ (Layer 7)

**Downstream Artifacts**: CTR (Layer 9), SPEC (Layer 10), TASKS (Layer 11), Code (Layer 13)

## Prerequisites

### Upstream Artifact Verification (CRITICAL)

**Before creating this document, you MUST:**

1. **List existing upstream artifacts**:
   ```bash
   ls docs/BRD/ docs/PRD/ docs/EARS/ docs/BDD/ docs/ADR/ docs/SYS/ docs/REQ/ 2>/dev/null
   ```

2. **Reference only existing documents** in traceability tags
3. **Use `null`** only when upstream artifact type genuinely doesn't exist
4. **NEVER use placeholders** like `BRD-XXX` or `TBD`
5. **Do NOT create missing upstream artifacts** - skip functionality instead


Before creating IMPL, read:

1. **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
2. **Upstream REQ**: Read atomic requirements to implement
3. **Template**: `ai_dev_flow/IMPL/IMPL-TEMPLATE.md`
4. **Creation Rules**: `ai_dev_flow/IMPL/IMPL_CREATION_RULES.md` (refer to template if not available)
5. **Validation Rules**: `ai_dev_flow/IMPL/IMPL_VALIDATION_RULES.md` (refer to template if not available)
6. **Validation Script**: `./ai_dev_flow/scripts/validate_impl.sh`

## When to Use This Skill

Use `doc-impl` when:
- Have completed BRD through REQ (Layers 1-7)
- Need to document implementation approach before coding
- Planning resource allocation and timeline
- Coordinating multiple developers or teams
- This layer is **OPTIONAL** - skip if not needed

### Create IMPL When

- Multi-component feature requiring 3+ SPEC files
- Phased rollout over multiple sprints/weeks
- Multiple teams coordinating on related components
- Complex dependencies between work packages

### Do NOT Create IMPL When

- Single SPEC implementation (use TASKS directly)
- Simple feature with no phase dependencies
- Work can be completed in one sprint by one team
- Documentation-only updates

## Reserved ID Exemption (IMPL-00_*)

**Scope**: Documents with reserved ID `000` are FULLY EXEMPT from validation.

**Pattern**: `IMPL-00_*.md`

**Document Types**:
- Index documents (`IMPL-00_index.md`)
- Traceability matrix templates (`IMPL-00_TRACEABILITY_MATRIX-TEMPLATE.md`)
- Glossaries, registries, checklists

**Rationale**: Reserved ID 000 documents are framework infrastructure (indexes, templates, reference materials), not project artifacts requiring traceability or quality gates.

**Validation Behavior**: Skip all checks when filename matches `IMPL-00_*` pattern.

## Element ID Format (MANDATORY)

**Pattern**: `IMPL.{DOC_NUM}.{ELEM_TYPE}.{SEQ}` (4 segments, dot-separated)

| Element Type | Code | Example |
|--------------|------|---------|
| Implementation Phase | 29 | IMPL.02.29.01 |

**Removed Patterns** (do NOT use):
- `PHASE-XXX` → Use `IMPL.NN.29.SS`
- `IP-XXX` → Use `IMPL.NN.29.SS`

**Fix**: Replace `### Phase-01: Setup` with `### IMPL.02.29.01: Setup`

**Reference**: `ID_NAMING_STANDARDS.md` — Cross-Reference Link Format

## IMPL-Specific Guidance

### 1. WHO-WHEN-WHAT Format

**Purpose**: Document implementation strategy with assignments

**Format**:
```markdown
## Implementation Approach

### WHO: Team/Developer Assignment
**Primary Developer**: @john.doe
**Code Reviewer**: @jane.smith
**QA Engineer**: @bob.johnson

### WHEN: Timeline and Milestones
**Start Date**: 2025-01-15
**Target Completion**: 2025-01-29
**Milestones**:
- Day 1-3: Interface implementation
- Day 4-7: Business logic
- Day 8-10: Error handling
- Day 11-14: Testing and validation

### WHAT: Implementation Scope
**Requirements**: REQ-data-validation-01, REQ-data-validation-02
**Deliverables**:
- Data validation service
- Data processing module
- Error handling middleware
- Unit tests (>80% coverage)
- Integration tests
```

### 2. Required Sections (4-PART Structure)

**Document Control** (MANDATORY - First section before all numbered sections)

**Document Control Fields** (10 mandatory):
| Field | Required | Format |
|-------|----------|--------|
| IMPL ID | Yes | IMPL-NN |
| Title | Yes | Non-empty string |
| Status | Yes | Draft/Planned/In Progress/On Hold/Completed/Cancelled |
| Version | Yes | X.Y.Z (semantic) |
| Created | Yes | YYYY-MM-DD |
| Author | Yes | Non-empty string |
| Owner | Yes | Non-empty string |
| Last Updated | Yes | YYYY-MM-DD |
| Related REQs | Yes | REQ-NN references |
| Deliverables | Yes | CTR/SPEC/TASKS list |

**4-PART Structure**:

**PART 1: Project Context and Strategy**
- 1.1 Overview: What system/feature is being implemented
- 1.2 Business Objectives: Requirements satisfied, success criteria
- 1.3 Scope: In-scope and out-of-scope boundaries
- 1.4 Dependencies: Upstream dependencies listed

**PART 2: Implementation Strategy (WHO-WHEN-WHAT)**
- 2.1 Phases and Milestones: Implementation timeline
- 2.2 Team and Responsibilities (WHO): Team assignments
- 2.3 Deliverables (WHAT): Per-phase outputs (CTR-NN, SPEC-NN, TASKS-NN)
- 2.4 Dependencies and Blockers

**PART 3: Project Management and Risk**
- 3.1 Resources: Team assignments and effort estimates
- 3.2 Risk Register: Project management risks with mitigation

**PART 4: Tracking and Completion**
- 4.1 Deliverables Checklist: [ ] checkboxes for each deliverable
- 4.2 Project Validation: Validation criteria
- 4.3 Completion Criteria: Definition of done
- 4.5 Sign-off: Sign-off table with roles

**Traceability**: Upstream/downstream references

### 3. Phase Content Rules

1. **Focus on WHO/WHAT/WHEN** - not technical details (HOW goes in SPEC)
2. **List specific deliverables** - CTR-NN, SPEC-NN, TASKS-NN
3. **Assign ownership** - team or person responsible
4. **Include timeline** - dates or sprint numbers
5. **Identify dependencies** - what blocks this phase

**Good Example**:
```markdown
### IMPL.02.29.01: Core Risk Engine

| Attribute | Details |
|-----------|---------|
| **Purpose** | Build foundation risk calculation engine |
| **Owner** | Risk Team (3 developers) |
| **Timeline** | Sprint 1-2 (4 weeks) |
| **Deliverables** | CTR-03, SPEC-03, TASKS-03 |
| **Dependencies** | Requires: Database schema (ADR-008) |
| **Success Criteria** | [ ] All deliverables created [ ] Tests passing |

**Key Risks**: Resource availability → Mitigation: Cross-train team
```

**Bad Example**:
```markdown
### Phase 1
- Build the risk engine
- Make it work
```

### 4. Dependencies Section

**Format**:
```markdown
## Dependencies

### Upstream Dependencies
- REQ-data-validation-01: Data validation requirements
- ADR-033: Database technology decision
- ADR-045: API design pattern

### External Dependencies
- PostgreSQL database instance (required before development)
- Authentication service (OAuth 2.0 provider)
- Market data feed (for price validation)

### Blockers
- [ ] Database schema approved by DBA team
- [ ] OAuth client credentials obtained
- [ ] Market data API access granted
```

### 5. Risk Assessment (Project Management Focus)

**Format**:
```markdown
## Risk Assessment

| Risk ID | Risk Description | Probability | Impact | Mitigation | Owner | Status |
|---------|------------------|-------------|--------|------------|-------|--------|
| R-001 | Resource unavailability | Medium | High | Cross-train team | PM | Open |
| R-002 | Timeline slippage | Medium | Medium | Scope buffer | PM | Open |
```

**Focus Areas** (Project management risks only - technical risks go in ADR/SPEC):
- Resource allocation risks
- Timeline management risks
- Scope control risks
- Dependency coordination risks

## Tag Format Convention (By Design)

The SDD framework uses two distinct notation systems for cross-references:

| Notation | Format        | Artifacts                               | Purpose                                                             |
|----------|---------------|----------------------------------------|---------------------------------------------------------------------|
| Dash     | TYPE-NN      | ADR, SPEC, CTR, IPLAN, ICON            | Technical artifacts - references to files/documents                 |
| Dot      | TYPE.NN.TT.SS | BRD, PRD, EARS, BDD, SYS, REQ, IMPL, TASKS | Hierarchical artifacts - references to elements inside documents |

**Key Distinction**:
- `@adr: ADR-033` → Points to the document `ADR-033_risk_limit_enforcement.md`
- `@brd: BRD.17.01.01` → Points to element 01.01 inside document `BRD-017.md`

## Unified Element ID Format (MANDATORY)

**For hierarchical requirements (BRD, PRD, EARS, BDD, SYS, REQ, IMPL)**:
- **Always use**: `TYPE.NN.TT.SS` (dot separator, 4-segment unified format)
- **Never use**: `TYPE-NN:NNN` (colon separator - DEPRECATED)
- **Never use**: `TYPE.NN.TT` (3-segment format - DEPRECATED)

Examples:
- `IMPL.02.29.01` ✅ (Implementation Phase element)
- `@brd: BRD.17.01.01` ✅
- `@brd: BRD.017.001` ❌ (old 3-segment format)


## Cumulative Tagging Requirements

**Layer 8 (IMPL)**: Must include tags from Layers 1-7 (BRD, PRD, EARS, BDD, ADR, SYS, REQ)

**Tag Count**: 7 tags (@brd through @req)

**Format**:
```markdown
## Traceability

**Required Tags** (Cumulative Tagging Hierarchy - Layer 8):
```markdown
@brd: BRD.01.01.03
@prd: PRD.01.07.02
@ears: EARS.01.25.01
@bdd: BDD.01.14.01
@adr: ADR-033, ADR-045
@sys: SYS.01.26.01
@req: REQ.01.27.01, REQ.01.27.02
```

**Upstream Sources**:
- [BRD-01](../BRD/BRD-01_platform.md#BRD-01)
- [PRD-01](../PRD/PRD-01_integration.md#PRD-01)
- [EARS-01](../EARS/EARS-01_risk.md#EARS-01)
- [BDD-01](../BDD/BDD-01_limits.feature)
- [ADR-033](../ADR/ADR-033_database.md#ADR-033)
- [SYS-01](../SYS/SYS-01_order.md#SYS-01)
- [REQ-data-validation-01](../REQ/REQ-data-validation-01_*.md)

**Downstream Artifacts**:
- CTR-NN (to be created) - Data contracts
- SPEC-NN (to be created) - Technical specifications
- TASKS-NN (to be created) - Task breakdown
```

## Scope Boundaries

### IMPL Contains (Project Management)

- **WHO**: Teams, people, assignments
- **WHAT**: Deliverables (CTR/SPEC/TASKS documents)
- **WHEN**: Timeline, milestones, phases
- **WHY**: Business objectives, success criteria

### IMPL Does NOT Contain (Technical)

- **HOW**: Technical implementation → SPEC
- **Code**: Implementation details → TASKS
- **Tests**: Test specifications → BDD/TASKS
- **Architecture**: System design → ADR

## Upstream/Downstream Artifacts

**Upstream Sources**:
- **BRD** (Layer 1) - Business requirements
- **PRD** (Layer 2) - Product features
- **EARS** (Layer 3) - Formal requirements
- **BDD** (Layer 4) - Test scenarios
- **ADR** (Layer 5) - Architecture decisions
- **SYS** (Layer 6) - System requirements
- **REQ** (Layer 7) - Atomic requirements (PRIMARY SOURCE)

**Downstream Artifacts**:
- **CTR** (Layer 9) - Data contracts (optional)
- **SPEC** (Layer 10) - Technical specifications
- **TASKS** (Layer 11) - Task breakdown
- **Code** (Layer 13) - Implementation

**Same-Type Document Relationships** (conditional):
- `@related-impl: IMPL-NN` - IMPLs sharing implementation context
- `@depends-impl: IMPL-NN` - IMPL that must complete first

## Creation Process

### Step 1: Read Upstream Artifacts

Focus on REQ (Layer 7) - atomic requirements to implement.

### Step 2: Reserve ID Number

Check `docs/IMPL/` for next available ID number (templates are in `ai_dev_flow/IMPL/`).

**ID Numbering Convention**: Start with 2 digits and expand only as needed.
- ✅ Correct: IMPL-01, IMPL-99, IMPL-102
- ❌ Incorrect: IMPL-001, IMPL-009 (extra leading zero not required)

### Step 3: Create IMPL File

**File naming**: `docs/IMPL/IMPL-NN_{slug}.md`

**Example**: `docs/IMPL/IMPL-01_position_validation.md`

### Step 4: Fill Document Control Section

Complete metadata and Document Revision History table. Verify all 10 mandatory fields.

### Step 5: Complete Implementation Overview

Summarize what will be implemented and why.

### Step 6: Document WHO-WHEN-WHAT

**WHO**: Assign team members
**WHEN**: Define timeline and milestones
**WHAT**: Specify scope and deliverables

### Step 7: Define Phases

Use unified Element ID format: `### IMPL.NN.29.SS: Phase Name`

- Each phase has Purpose, Owner, Timeline, Deliverables, Dependencies
- List specific deliverables: CTR-NN, SPEC-NN, TASKS-NN

### Step 8: Identify Dependencies

- Upstream artifacts
- External systems
- Blockers (if any)

### Step 9: Assess Risks

Document project management risks (not technical) with likelihood, impact, and mitigation.

### Step 10: Add Cumulative Tags

Include all 7 upstream tags (@brd through @req).

### Step 11: Create/Update Traceability Matrix

**MANDATORY**: Update `docs/IMPL/IMPL-00_TRACEABILITY_MATRIX.md` (create from `ai_dev_flow/IMPL/IMPL-00_TRACEABILITY_MATRIX-TEMPLATE.md` if not exists)

### Step 12: Validate IMPL

```bash
./ai_dev_flow/scripts/validate_impl.sh docs/IMPL/IMPL-01_*.md

python ai_dev_flow/scripts/validate_tags_against_docs.py --artifact IMPL-01 --expected-layers brd,prd,ears,bdd,adr,sys,req --strict
```

### Step 13: Commit Changes

Commit IMPL file and traceability matrix.

## Validation Checks

| Check | Description | Type |
|-------|-------------|------|
| CHECK 1 | Filename format (IMPL-NN_{slug}.md) | ERROR |
| CHECK 2 | Frontmatter validation (artifact_type: IMPL, layer: 8) | ERROR |
| CHECK 3 | Document Control fields (10 mandatory) | ERROR |
| CHECK 4 | Required Parts (PART 1-4 + Traceability) | ERROR |
| CHECK 5 | PART 1 subsections (1.1-1.4) | WARNING |
| CHECK 6 | Phases defined with deliverables | ERROR |
| CHECK 7 | Deliverables referenced (CTR/SPEC/TASKS) | ERROR |
| CHECK 8 | PART 3 risk register present | WARNING |
| CHECK 9 | PART 4 sign-off section present | WARNING |
| CHECK 10 | Traceability tags (7 required) | ERROR |
| CHECK 11 | Scope boundary validation (PM focus) | WARNING |
| CHECK 12 | Cross-reference validation | WARNING |
| CHECK 13 | Element ID format compliance | ERROR |

### Validation Tiers

| Tier | Type | Action |
|------|------|--------|
| **Tier 1** | ERROR | Must fix before commit |
| **Tier 2** | WARNING | Recommended to fix |
| **Tier 3** | INFO | No action required |

### Automated Validation

```bash
# Quality gates
./scripts/validate_quality_gates.sh docs/IMPL/IMPL-01_*.md

# Cumulative tagging
python ai_dev_flow/scripts/validate_tags_against_docs.py \
  --artifact IMPL-01 \
  --expected-layers brd,prd,ears,bdd,adr,sys,req \
  --strict
```

### Manual Checklist

- [ ] Document Control section with 10 required fields
- [ ] All 4 PARTS present
- [ ] Phases use unified ID format (IMPL.NN.29.SS)
- [ ] WHO-WHEN-WHAT framework completed
- [ ] Team assignments documented
- [ ] Timeline and milestones defined
- [ ] Deliverables listed (CTR-NN, SPEC-NN, TASKS-NN)
- [ ] Dependencies identified
- [ ] Blockers documented (if any)
- [ ] Risk assessment completed (project management focus)
- [ ] Cumulative tags: @brd through @req (7 tags) included
- [ ] Traceability matrix updated

### Diagram Standards
All diagrams MUST use Mermaid syntax. Text-based diagrams (ASCII art, box drawings) are prohibited.
See: `ai_dev_flow/DIAGRAM_STANDARDS.md` and `mermaid-gen` skill.

## Common Pitfalls

1. **Vague assignments**: WHO must specify actual people/teams
2. **Unrealistic timeline**: WHEN must account for dependencies
3. **Scope creep**: WHAT must align strictly with REQ scope
4. **Missing cumulative tags**: Layer 8 must include all 7 upstream tags
5. **No risk assessment**: Must document project management risks
6. **Technical risks in IMPL**: Project risks only (technical → ADR/SPEC)
7. **Legacy element IDs**: Use `IMPL.NN.29.SS` not `Phase-XXX` or `IP-XXX`
8. **Missing deliverables**: Each phase must list CTR/SPEC/TASKS IDs
9. **Skipping when not needed**: IMPL is optional - skip if not valuable

## Post-Creation Validation (MANDATORY - NO CONFIRMATION)

**CRITICAL**: Execute this validation loop IMMEDIATELY after document creation. Do NOT proceed to next document until validation passes.

### Automatic Validation Loop

```
LOOP:
  1. Run: python ai_dev_flow/scripts/validate_cross_document.py --document {doc_path} --auto-fix
  2. IF errors fixed: GOTO LOOP (re-validate)
  3. IF warnings fixed: GOTO LOOP (re-validate)
  4. IF unfixable issues: Log for manual review, continue
  5. IF clean: Mark VALIDATED, proceed
```

### Validation Command

```bash
# Per-document validation (Phase 1)
python ai_dev_flow/scripts/validate_cross_document.py --document docs/IMPL/IMPL-NN_slug.md --auto-fix

# Layer validation (Phase 2) - run when all IMPL documents complete
python ai_dev_flow/scripts/validate_cross_document.py --layer IMPL --auto-fix
```

### Layer-Specific Upstream Requirements

| This Layer | Required Upstream Tags | Count |
|------------|------------------------|-------|
| IMPL (Layer 8) | @brd, @prd, @ears, @bdd, @adr, @sys, @req | 7 tags |

### Auto-Fix Actions (No Confirmation Required)

| Issue | Fix Action |
|-------|------------|
| Missing @brd/@prd/@ears/@bdd/@adr/@sys/@req tag | Add with upstream document reference |
| Invalid tag format | Correct to TYPE.NN.TT.SS (4-segment) or TYPE-NN format |
| Broken link | Recalculate path from current location |
| Missing traceability section | Insert from template |

### Validation Codes Reference

| Code | Description | Severity |
|------|-------------|----------|
| XDOC-001 | Referenced requirement ID not found | ERROR |
| XDOC-002 | Missing cumulative tag | ERROR |
| XDOC-003 | Upstream document not found | ERROR |
| XDOC-006 | Tag format invalid | ERROR |
| XDOC-007 | Gap in cumulative tag chain | ERROR |
| XDOC-009 | Missing traceability section | ERROR |

### Quality Gate

**Blocking**: YES - Cannot proceed to next document until Phase 1 validation passes with 0 errors.

---

## Next Skill

After creating IMPL (or skipping this optional layer), use:

**`doc-ctr`** - Create Data Contracts (Layer 9, optional)

Or skip to:

**`doc-spec`** - Create Technical Specifications (Layer 10)

The SPEC will:
- Reference REQ (and optionally IMPL) as upstream source
- Include all 7-8 upstream tags
- Use YAML format
- Define implementation contracts
- Achieve 100% implementation-readiness

## Reference Documents

For supplementary documentation related to IMPL artifacts:
- **Format**: `IMPL-REF-NNN_{slug}.md`
- **Skill**: Use `doc-ref` skill
- **Validation**: Minimal (non-blocking)
- **Examples**: Resource planning guides, team capability matrices

## Related Resources

- **Template**: `ai_dev_flow/IMPL/IMPL-TEMPLATE.md` (primary authority)
- **IMPL Creation Rules**: `ai_dev_flow/IMPL/IMPL_CREATION_RULES.md`
- **IMPL Validation Rules**: `ai_dev_flow/IMPL/IMPL_VALIDATION_RULES.md`
- **IMPL README**: `ai_dev_flow/IMPL/README.md`
- **Shared Standards**: `.claude/skills/doc-flow/SHARED_CONTENT.md`
- **ID Naming Standards**: `ai_dev_flow/ID_NAMING_STANDARDS.md`

**Section Templates** (for documents >25K tokens):
- Index template: `ai_dev_flow/IMPL/IMPL-SECTION-0-TEMPLATE.md`
- Content template: `ai_dev_flow/IMPL/IMPL-SECTION-TEMPLATE.md`
- Reference: `ai_dev_flow/ID_NAMING_STANDARDS.md` (Section-Based File Splitting)

## Quick Reference

**IMPL Purpose**: Document WHO-WHEN-WHAT implementation approach

**Layer**: 8 (Optional)

**Tags Required**: @brd through @req (7 tags)

**Element ID Format**: `IMPL.NN.29.SS`
- Implementation Phase = 29

**Removed Patterns**: PHASE-XXX, IP-XXX

**Document Control Fields**: 10 required

**Format**: 4-PART Structure

**Key Parts**:
- **PART 1**: Project Context and Strategy (Overview, Objectives, Scope, Dependencies)
- **PART 2**: Implementation Strategy - WHO-WHEN-WHAT (Phases, Team, Deliverables)
- **PART 3**: Project Management and Risk (Resources, Risk Register)
- **PART 4**: Tracking and Completion (Deliverables Checklist, Sign-off)

**Scope Boundaries**:
- **IMPL Contains**: WHO/WHAT/WHEN/WHY (Project Management)
- **IMPL Does NOT Contain**: HOW (Technical details → SPEC)

**Optional**: Skip this layer if implementation approach is straightforward

**Next**: doc-ctr (optional) or doc-spec
