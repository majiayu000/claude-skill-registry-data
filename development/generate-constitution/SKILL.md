---
name: Generate Constitution
description: Derive technical development principles FROM user needs in product.md using evidence-based reasoning. Creates constitution.md with architecture decisions, tech stack choices, and development constraints - all traced back to specific user needs. Use when user mentions "technical principles", "constitution", "architecture decisions", or after creating product.md.
---

@.claude/shared-imports/constitution.md
@.claude/shared-imports/CoD_Σ.md
@.claude/shared-imports/memory-utils.md
@.claude/templates/product-constitution.md

# Generate Constitution Skill

## Workflow Context

**SDD Phase**: Phase 2 (Foundation)
**Command**: `/generate-constitution`
**Prerequisites**: `memory/product.md` (created by Phase 1 - define-product)
**Creates**: `memory/constitution.md`
**Predecessor**: Phase 1 - `/define-product` → `memory/product.md`
**Successor**: Phase 3 - `/feature` → `specs/$FEATURE/spec.md`

### Phase Chain
```
Phase 1: /define-product → memory/product.md
Phase 2: /generate-constitution → memory/constitution.md (YOU ARE HERE)
Phase 3: /feature → specs/$FEATURE/spec.md
Phase 4: /clarify (if needed) → updated spec.md
Phase 5: /plan → plan.md + research.md + data-model.md
Phase 6: /tasks (auto) → tasks.md
Phase 7: /audit (auto) → audit-report.md
Phase 8: /implement → code + tests + verification
```

**$FEATURE format**: `NNN-feature-name` (e.g., `001-therapy-app`)

---

## Overview

This skill creates constitution.md by **deriving** technical principles FROM user needs documented in product.md. Every technical decision must trace back to a specific user pain point, differentiator, or journey requirement.

**Core Derivation Pattern**:
```
User Need (product.md) ≫ Capability Required → Technical Approach ≫ Specific Constraint (constitution.md)
```

**Announce at start:** "I'm using the generate-constitution skill to derive technical principles from user needs in product.md."

**Note**: constitution.md CANNOT be created without product.md. All technical principles MUST derive from user needs. If product.md doesn't exist, use **define-product skill** first.

---

## Quick Reference

| Workflow | Key Activities | Output |
|----------|---------------|--------|
| **Derivation** | Load product.md → Map user needs → Derive principles → Organize → Create derivation map | constitution.md (v1.0.0) |
| **Amendment** | Identify product.md changes → Update Articles → Bump version → Add history | constitution.md (vX.Y.Z) |
| **Validation** | Check derivation chains → Verify traceability → Validate classifications | Quality report |

---

## Workflow Files

**Detailed Workflows**:
- **@.claude/skills/generate-constitution/workflows/derivation-workflow.md** - Steps 1-6: Create new constitution
- **@.claude/skills/generate-constitution/workflows/amendment-workflow.md** - Update constitution when product.md changes
- **@.claude/skills/generate-constitution/workflows/validation-checks.md** - Quality gates and quick tests

**References**:
- **@.claude/skills/generate-constitution/references/anti-patterns.md** - Common mistakes to avoid
- **@.claude/skills/generate-constitution/references/failure-modes.md** - 12 failure modes with fixes

---

## Workflow Decision Tree

```
User Request?
├─ Creating new constitution? → Derivation Workflow
├─ Updating existing? → Amendment Workflow
└─ Validating? → Validation Checks
```

---

## Derivation Workflow (Create New Constitution)

**See:** @.claude/skills/generate-constitution/workflows/derivation-workflow.md

**Summary:**

### Step 1: Load Product Definition

Read product.md and extract:
- **Persona pain points** → NON-NEGOTIABLE efficiency principles
- **"Our Thing" differentiator** → NON-NEGOTIABLE core principles
- **North Star metric** → Performance and usage principles
- **User journeys** → Capability requirements

### Step 2: Map User Needs to Technical Requirements

For each user need, apply derivation pattern:
```
User Need ≫ Capability → Technical Approach ≫ Constraint
```

**Example**:
```
product.md:Persona1:Pain1:118: "Manual copying wastes 2hr/week"
  ≫ Automated sync required
  → API integrations with refresh
  ≫ <15 minute data latency
→ Constitution Article: Real-Time Sync (<15min, NON-NEGOTIABLE)
```

### Step 3: Derive Technical Principles

For each user need, create an Article with:
- **User Need Evidence** - product.md quote with line reference
- **Technical Derivation (CoD^Σ)** - Reasoning chain with operators
- **Principle** - Specific measurable constraint
- **Rationale** - Why this serves the user need
- **Verification** - How to validate compliance

**Classification**:
- **NON-NEGOTIABLE** - "Our Thing", core promises (breaks user promise if violated)
- **SHOULD** - Strong preferences (flexibility when justified)
- **MAY** - Options allowed (guidelines only)

### Step 4: Organize by Category

Group principles into 7 standard Articles:
1. Architecture Patterns (microservices, event-driven, etc.)
2. Data & Integration (database, API, sync patterns)
3. Performance & Reliability (SLAs, latency, uptime)
4. Security & Privacy (auth, encryption, compliance)
5. User Experience (UI constraints, accessibility)
6. Development Process (testing, deployment, quality)
7. Scalability (growth constraints, capacity)

Priority within each: NON-NEGOTIABLE → SHOULD → MAY

### Step 5: Create Derivation Map

Document traceability:
```markdown
## Appendix: Constitution Derivation Map

| Article | Product.md Source | User Need | Technical Principle |
|---------|-------------------|-----------|---------------------|
| Article II | Persona1:Pain1:118 | Manual copying | <15min sync latency |
| Article III | OurThing:283 | Instant visibility | <2s dashboard load |
```

Enables: Tracing principles back, identifying orphans, validating coverage.

### Step 6: Version & Metadata

```markdown
---
version: 1.0.0
ratified: YYYY-MM-DD
derived_from: product.md (v1.0)
---

# Development Constitution

**Purpose**: Technical principles derived FROM user needs
**Amendment Process**: See Article VIII
**Derivation Evidence**: See Appendix
```

---

## Amendment Workflow (Update Existing Constitution)

**See:** @.claude/skills/generate-constitution/workflows/amendment-workflow.md

**Summary:**

**Trigger**: product.md changes → constitution.md MUST update

**Version Semantics**:
- **MAJOR (X.0.0)**: Article added/removed (architectural shift)
- **MINOR (1.X.0)**: Article modified (principle change)
- **PATCH (1.0.X)**: Formatting, typos, clarifications

**Process**:
1. Identify which user needs changed in product.md
2. Update affected Articles with new derivation chains
3. Bump version number (MAJOR/MINOR/PATCH)
4. Update ratified date
5. Update derivation map
6. Add amendment history entry with before/after

**Amendment Entry Template**:
```markdown
### Version X.Y.Z - YYYY-MM-DD
**Changed**: Article III (Performance)
**Reason**: product.md North Star updated
**Before**: Dashboard <2s only
**After**: Dashboard <2s AND reports <10s
**Evidence**: product.md:NorthStar:line:15
```

---

## Validation Checks

**See:** @.claude/skills/generate-constitution/workflows/validation-checks.md

**Summary:**

### Quality Checklist (For Each Article)

- [ ] Has explicit product.md reference (file:section:line)
- [ ] User need quoted verbatim
- [ ] CoD^Σ derivation chain documented
- [ ] Principle is specific and measurable
- [ ] Verification method defined
- [ ] Classification clear (NON-NEGOTIABLE | SHOULD | MAY)

### Overall Validation

- [ ] No orphaned principles (all trace to user needs)
- [ ] All "Our Thing" items have NON-NEGOTIABLE principles
- [ ] All pain resolutions have technical support
- [ ] Derivation map complete
- [ ] Version metadata current

### Quick Tests

1. **"Can I delete this without breaking a user promise?"**
   - YES → Might not be needed
   - NO → Should be NON-NEGOTIABLE

2. **"Can I trace this to a specific user pain?"**
   - YES → Good principle
   - NO → Remove it

3. **"Does this enable 'Our Thing'?"**
   - YES → Upgrade to NON-NEGOTIABLE
   - NO → Evaluate if needed

---

## Anti-Patterns

**See:** @.claude/skills/generate-constitution/references/anti-patterns.md

**Summary of Common Mistakes:**

1. **Tech preferences without user justification** - "Use React because popular" → Derive from user need
2. **Over-constraining without evidence** - "MUST use PostgreSQL only" → Constrain capability (ACID), not product
3. **Vague principles** - "System should be performant" → Specific measurable criteria
4. **Missing derivation chains** - State principle without CoD^Σ → Add full reasoning chain
5. **No verification method** - Can't validate compliance → Define specific checks
6. **Orphaned principles** - No connection to product.md → Remove or find user need

---

## Failure Modes

**See:** @.claude/skills/generate-constitution/references/failure-modes.md

**Summary of Top 12 Failures:**

1. **Constitution created without product.md** → STOP, create product.md first
2. **Technical preferences without CoD^Σ** → Add derivation chain
3. **Orphaned principles** → Trace to product.md or delete
4. **"Our Thing" not NON-NEGOTIABLE** → Upgrade classification
5. **Over-constraining tech stack** → Constrain capability, not product
6. **Missing verification methods** → Define checks
7. **Amendment without version bump** → Follow semantic versioning
8. **Derivation map incomplete** → Add all Articles to map
9. **User needs not addressed** → Add missing Articles
10. **Classification incorrect** → Run 3 quick tests
11. **No amendment history** → Add before/after entry
12. **Technical jargon in evidence** → Fix product.md (boundary violation)

---

## Example

**Complete Constitution**: See [examples/b2b-saas-constitution.md](examples/b2b-saas-constitution.md)

Shows:
- Full derivation chains with CoD^Σ reasoning
- 7 Articles (Architecture, Data, Performance, Security, UX, Development, Scalability)
- Complete derivation map tracing principles to product.md
- Amendment history example
- NON-NEGOTIABLE vs SHOULD classifications

**Template**: Use `@.claude/templates/product-constitution.md`

---

## Key Reminders

1. **Every principle MUST trace to user need** - No orphaned tech preferences
2. **"Our Thing" drives NON-NEGOTIABLE** - Core differentiators are non-negotiable
3. **Use CoD^Σ for all derivations** - Evidence chain required
4. **Version amendments** - Track why principles change
5. **Validate bidirectionally** - Product → Constitution AND Constitution → Product

---

## Prerequisites

Before using this skill:
- ✅ product.md exists (REQUIRED - created by define-product skill)
- ✅ product.md has personas with pain points
- ✅ product.md has "Our Thing" (key differentiator)
- ✅ product.md has North Star metric
- ✅ product.md has user journeys
- ⚠️ Optional: Existing constitution.md to amend (will be versioned)
- ⚠️ Optional: @.claude/templates/product-constitution.md (for structure)

**Note**: constitution.md CANNOT be created without product.md. All technical principles MUST derive from user needs documented in product.md.

---

## Dependencies

**Depends On**:
- **define-product skill** - MUST run before this skill (provides product.md)
- @.claude/shared-imports/CoD_Σ.md - For derivation chains and evidence traces
- product.md - Source of ALL user needs (critical input)

**Integrates With**:
- **create-implementation-plan skill** - Uses constitution.md for architecture decisions
- **specify-feature skill** - References constitution.md constraints in features
- **/generate-constitution command** - User-facing command that invokes this skill

**Tool Dependencies**:
- Read tool (to load product.md)
- Write tool (to create constitution.md)
- CoD^Σ operators (for derivation chains)

---

## Next Steps

After constitution.md creation completes:

**Main Development Flow**:
```
generate-constitution (creates constitution.md)
    ↓ (manual invocation)
specify-feature (user runs /feature with feature idea)
    ↓ (references constitution.md constraints)
create-implementation-plan (tech stack FROM constitution)
    ↓ (automatic)
generate-tasks → /audit → /implement
```

**Amendment Flow** (when product.md changes):
```
product.md updated (personas, pain points, or differentiators changed)
    ↓ (manual invocation)
generate-constitution --amend (user runs /generate-constitution)
    ↓
constitution.md updated (version bumped, derivation map updated)
    ↓
Review affected features/plans for constitutional compliance
```

**User Action Required**:
- Review constitution.md for completeness and accuracy
- Validate all Articles have derivation chains to product.md
- Share constitution.md with team for alignment
- Use as guide for ALL technical decisions going forward

**Outputs Modified**:
- `constitution.md` - Technical principles derived from user needs (project root)
- Version number incremented if amending existing constitution
- Derivation map updated with all product.md traces

**Commands**:
- **/generate-constitution** - Create or amend constitution.md
- **/feature** - After constitution exists, create features with constitutional constraints
- **/plan** - After constitution exists, plans must comply with principles

---

## Related Skills & Commands

**Direct Integration**:
- **define-product skill** - MUST run before this skill (provides product.md input)
- **create-implementation-plan skill** - Uses constitution.md for architecture decisions (successor)
- **specify-feature skill** - References constitution.md constraints in specifications
- **/generate-constitution command** - User-facing command that invokes this skill

**Workflow Context**:
- Position: **Phase 2** of product development (after product.md, before features)
- Triggers: User mentions "technical principles", "constitution", OR after product.md created
- Output: constitution.md with technical principles derived FROM user needs

**Constitution Chain**:
```
User Context (define-product: product.md)
    ↓ (this skill derives technical principles)
Technical Principles (this skill: constitution.md)
    ↓ (guides all technical decisions)
Feature Specifications (specify-feature: spec.md with constitutional constraints)
    ↓
Implementation Plans (create-implementation-plan: tech stack FROM constitution)
```

**Core Principle**: ALL technical decisions derive from user needs. constitution.md is the bridge between user-centric product.md and technical implementation.

**Quality Gates**:
- **Traceability**: Every Article MUST trace to product.md (file:section:line)
- **CoD^Σ Evidence**: Every derivation MUST use Chain of Decisions operators
- **Classification**: NON-NEGOTIABLE for "Our Thing", SHOULD for preferences, MAY for flexibility
- **Verification**: Every Article MUST have verification method
- **Derivation Map**: Complete bidirectional traceability

**Amendment Process**: When product.md changes, re-run this skill to update constitution.md with version bump and amendment history.

**Workflow Recommendation**: Run this skill IMMEDIATELY after define-product to establish technical foundation before any feature development.

---

**Version:** 1.2.0
**Last Updated:** 2025-01-19
**Change Log**:
- v1.2.0 (2025-01-19): Added explicit SDD workflow context with 8-phase chain
- v1.1.0 (2025-10-23): Refactored to progressive disclosure pattern (<500 lines)
- v1.0.0 (2025-10-22): Initial version
