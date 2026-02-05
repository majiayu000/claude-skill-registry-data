---
name: validate-design-coverage
description: Homeostatic sensor validating all requirements have design coverage. Checks for requirements without components, APIs, or data models. Quality gate before Code stage. Use to ensure design completeness.
allowed-tools: [Read, Grep, Glob]
---

# validate-design-coverage

**Skill Type**: Sensor (Quality Gate)
**Purpose**: Validate all requirements have design coverage
**Prerequisites**: Requirements exist, some design created

---

## Agent Instructions

You are a **Sensor** validating design coverage.

**Desired State**: `design_coverage = 100%` (all requirements have design)

Your goal is to **find requirements without design** and signal the gap.

---

## Workflow

### Step 1: Find All Requirements

```bash
# Extract all REQ-* from requirements docs
grep -rho "REQ-[A-Z-]*-[0-9]*" docs/requirements/ | sort -u
```

---

### Step 2: Check Design Coverage

**For each REQ-*, search design documents**:

```bash
# Check if requirement has design
grep -rn "<REQ-ID>" docs/design/ docs/adrs/

# Expected: At least 1 design doc mentions this requirement
```

**Coverage criteria**:
- ✅ **Covered**: REQ-* mentioned in design docs or ADRs
- ❌ **Not covered**: REQ-* not found in any design documentation

---

### Step 3: Validate Design Completeness

**For covered requirements, check if design is complete**:

```yaml
<REQ-ID>:
  ✓ Component: AuthenticationService (in architecture doc)
  ✓ API: POST /auth/login (in API spec)
  ✓ Data Model: User entity (in data model doc)
  ✓ Diagram: Figure 1 (in component diagram)
  Result: COMPLETE ✅

<REQ-ID>:
  ✓ Component: PaymentService (in architecture doc)
  ✗ API: No API spec found
  ✗ Data Model: No data model
  ✓ Diagram: Figure 3 (in component diagram)
  Result: PARTIAL ⚠️ (missing API spec, data model)
```

---

### Step 4: Calculate Design Coverage

**Coverage percentage**:

```
Total Requirements: 42

Requirements with Complete Design: 35/42 (83.3%)
Requirements with Partial Design: 5/42 (11.9%)
Requirements with No Design: 2/42 (4.8%)

Overall Design Coverage: 95.2% (40/42 have at least partial design)
```

---

## Output Format

**When gaps detected**:

```
[VALIDATE DESIGN COVERAGE - GAPS DETECTED]

Total Requirements: 42
Design Coverage: 95.2% (40/42) ⚠️

Requirements Without Design (2):
  ❌ REQ-F-NOTIF-001: Email notifications
     Missing: All design (no components, APIs, data models)

  ❌ REQ-F-EXPORT-001: Data export
     Missing: All design

Requirements with Partial Design (5):
  ⚠️ <REQ-ID>: Payment processing
     Has: Component (PaymentService), Diagram
     Missing: API spec, Data model

  ⚠️ REQ-F-CART-001: Shopping cart
     Has: Component (CartService)
     Missing: API spec, Data model, Diagram

  ... (3 more)

Requirements with Complete Design (35):
  ✅ <REQ-ID>: User login (complete)
  ✅ <REQ-ID>: Password reset (complete)
  ... (33 more)

Homeostasis Deviation:
  - 2 requirements without any design
  - 5 requirements with incomplete design
  - Target: 100% coverage

Recommendations:
  1. Design REQ-F-NOTIF-001 (email notifications)
  2. Design REQ-F-EXPORT-001 (data export)
  3. Complete API specs for 5 partial designs
  4. Complete data models for 5 partial designs

Quality Gate: ⚠️ PARTIAL PASS
  - Can proceed with 35 complete designs
  - Must design remaining 7 before full deployment
```

**When homeostasis achieved**:

```
[VALIDATE DESIGN COVERAGE - HOMEOSTASIS ACHIEVED]

Total Requirements: 42
Design Coverage: 100% (42/42) ✅

All Requirements Have:
  ✅ Component design
  ✅ API specifications
  ✅ Data models
  ✅ Component diagrams

Quality Gate: ✅ PASS
Ready for: Code Stage
Design Coverage: COMPLETE
```

---

## Prerequisites Check

Before invoking:
1. Requirements exist and are validated
2. Some design documents exist

---

## Configuration

```yaml
plugins:
  - name: "@aisdlc/design-skills"
    config:
      validation:
        require_all_req_have_design: true
        require_components: true
        require_api_specs: true
        require_data_models: true
        require_diagrams: false  # Optional
        minimum_coverage: 100
```

---

## Notes

**Why validate design coverage?**
- **Quality gate**: Ensure all requirements designed before coding
- **Complete specification**: Design + requirements = implementation guide
- **Architecture review**: Stakeholders review before expensive coding
- **Prevent rework**: Catch design gaps before implementation

**Design coverage vs Code coverage**:
- Design coverage: Requirements → Design documents
- Code coverage: Code → Test coverage

**Homeostasis Goal**:
```yaml
desired_state:
  design_coverage: 100%
  all_requirements_designed: true
  quality_gate: pass
```

**"Excellence or nothing"** 🔥
