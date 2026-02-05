---
name: validate-architecture
description: Validate architecture document completeness and quality against comprehensive checklist. Checks required sections, technology justifications, NFRs coverage, and generates quality score with actionable recommendations. Use after architecture creation to verify completeness, quality, and NFR coverage before implementation begins.
acceptance:
  - validation_complete: "All checklist items evaluated"
  - quality_score_calculated: "Quality score (0-100) computed"
  - gaps_identified: "Missing elements and gaps documented"
  - recommendations_provided: "Actionable recommendations given"
inputs:
  architecture_file:
    type: string
    required: true
    description: "Path to architecture document (docs/architecture.md)"
  project_type:
    type: string
    required: false
    description: "frontend | backend | fullstack (auto-detected if not provided)"
  strict_mode:
    type: boolean
    required: false
    description: "Enforce stricter validation criteria (default: false)"
outputs:
  validation_passed:
    type: boolean
    description: "Whether architecture passed validation (score ≥70)"
  quality_score:
    type: number
    description: "Overall quality score (0-100)"
  gaps:
    type: array
    description: "List of missing or incomplete elements"
  recommendations:
    type: array
    description: "Prioritized improvement recommendations"
telemetry:
  emit: "skill.validate-architecture.completed"
  track:
    - quality_score
    - validation_passed
    - gaps_count
    - project_type
    - duration_ms
---

# Validate Architecture

## Purpose

Validate architecture documents for completeness, quality, and adherence to best practices. Generates comprehensive validation report with quality score, identified gaps, and prioritized recommendations for improvement.

**Core Principles:**
- **Comprehensive checklists:** Cover all architectural dimensions
- **Objective scoring:** Consistent, repeatable quality measurement
- **Actionable feedback:** Specific, prioritized improvements
- **Adapt to context:** Different criteria for different project types

---

## Prerequisites

- Architecture document exists (docs/architecture.md or specified path)
- Architecture follows standard structure (see create-architecture skill)

---

## Workflow

### 1. Load Architecture Document

**Action:** Read architecture document using bmad-commands

Execute:
```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path {architecture_file} \
  --output json
```

**Parse document to extract:**
- Present sections
- Technology stack components
- ADRs count and quality
- NFRs coverage
- Security considerations
- Scalability mentions

---

### 2. Detect Project Type

**Auto-detect from architecture content:**

**Frontend indicators:**
- Component architecture section
- State management discussion
- UI/routing mentions
- Frontend technologies (React, Vue, etc.)

**Backend indicators:**
- API design section
- Service layer architecture
- Database/data layer
- Backend technologies (Node, Python, etc.)

**Fullstack indicators:**
- Both frontend and backend sections
- Integration/API contract sections
- End-to-end authentication flow
- Full stack technologies (Next.js, etc.)

**If unable to detect:** Prompt for project_type parameter

---

### 3. Run Completeness Checklist

**Validate required sections based on project type:**

#### Universal Sections (All Types)
- ✅ System Overview (purpose, users, features)
- ✅ Technology Stack (with justifications)
- ✅ Deployment Architecture
- ✅ Security Architecture
- ✅ Architecture Decision Records (≥3)

#### Frontend-Specific Sections
- ✅ Component Architecture
- ✅ State Management Strategy
- ✅ Routing Design
- ✅ Styling Approach
- ✅ Build & Deployment Pipeline

#### Backend-Specific Sections
- ✅ API Design (REST/GraphQL/tRPC)
- ✅ Service Layer Architecture
- ✅ Data Architecture & Modeling
- ✅ Integration Patterns
- ✅ Error Handling Strategy

#### Fullstack-Specific Sections
- ✅ End-to-End Integration
- ✅ API Contracts/Type Safety
- ✅ Authentication & Authorization Flow
- ✅ Frontend-Backend Communication
- ✅ Unified Deployment Strategy

**Score:** +10 points per required section present

**See:** `references/validation-rules.md` for complete validation criteria and scoring rubrics

---

### 4. Validate Technology Stack

**Check that all technology choices:**
- ✅ Are documented (not just mentioned)
- ✅ Have justifications (why this choice?)
- ✅ List alternatives considered
- ✅ Explain trade-offs
- ✅ Are appropriate for project scale

**Scoring:**
- All choices justified: +15 points
- Most choices justified: +10 points
- Some justified: +5 points
- None justified: 0 points

**Flag unjustified technologies as gaps**

---

### 5. Assess NFR Coverage

**Verify Non-Functional Requirements addressed:**

| NFR Category | Required Elements |
|--------------|-------------------|
| Performance | Response time targets, optimization strategies |
| Scalability | User growth plan, bottleneck identification |
| Security | Auth/authz, encryption, compliance |
| Reliability | Availability targets, fault tolerance |
| Maintainability | Code organization, testing strategy |

**Scoring:**
- All NFRs addressed: +15 points
- Most NFRs addressed: +10 points
- Some NFRs addressed: +5 points
- Few/none addressed: 0 points

**See:** `references/validation-rules.md` for NFR validation criteria

---

### 6. Evaluate ADRs Quality

**Check Architecture Decision Records:**

**Quantity:**
- ≥10 ADRs: +10 points
- 5-9 ADRs: +7 points
- 3-4 ADRs: +5 points
- <3 ADRs: 0 points

**Quality (sample 3-5 ADRs):**
- ✅ Context clearly stated
- ✅ Decision explicitly stated
- ✅ Alternatives considered (≥2)
- ✅ Rationale provided
- ✅ Consequences documented

**Well-formed ADRs:** +5 points
**Partial ADRs:** +2 points
**Poor ADRs:** 0 points

---

### 7. Check Security Posture

**Validate security considerations:**
- ✅ Authentication mechanism defined
- ✅ Authorization strategy documented
- ✅ Data encryption (at rest, in transit)
- ✅ Input validation approach
- ✅ Security best practices mentioned
- ✅ Compliance requirements (if applicable)

**Scoring:**
- Comprehensive security: +10 points
- Basic security: +5 points
- Minimal security: 0 points

**Critical gap:** Missing security section

---

### 8. Assess Scalability Planning

**Check scalability considerations:**
- ✅ User growth projections
- ✅ Scaling strategy (horizontal/vertical)
- ✅ Bottleneck identification
- ✅ Load balancing approach
- ✅ Database scaling plan
- ✅ Caching strategy

**Scoring:**
- Detailed scalability plan: +10 points
- Basic scalability mentions: +5 points
- No scalability planning: 0 points

---

### 9. Validate Deployment Strategy

**Check deployment architecture:**
- ✅ Deployment platform specified
- ✅ Environment strategy (dev, staging, prod)
- ✅ CI/CD pipeline outlined
- ✅ Monitoring and observability
- ✅ Backup and disaster recovery

**Scoring:**
- Comprehensive deployment: +10 points
- Basic deployment: +5 points
- Missing deployment: 0 points

---

### 10. Calculate Quality Score

**Total possible points:** 100

**Score breakdown:**
- Completeness (sections): 30-40 points (varies by type)
- Technology justifications: 15 points
- NFR coverage: 15 points
- ADRs quantity & quality: 15 points
- Security posture: 10 points
- Scalability planning: 10 points
- Deployment strategy: 10 points

**Quality Grades:**
- **90-100:** Excellent (A)
- **80-89:** Good (B)
- **70-79:** Acceptable (C)
- **60-69:** Needs Improvement (D)
- **<60:** Insufficient (F)

**Validation passes if score ≥70**

---

### 11. Identify Gaps

**Categorize identified gaps:**

**Critical Gaps (blocking):**
- Missing security section
- No technology justifications
- Fewer than 3 ADRs
- Zero NFR coverage

**Major Gaps (important):**
- Missing key sections for project type
- Poor ADR quality
- Minimal security details
- No scalability planning

**Minor Gaps (nice-to-have):**
- Incomplete deployment details
- Missing diagrams
- Light monitoring discussion

**Priority:** Critical → Major → Minor

---

### 12. Generate Recommendations

**Based on identified gaps, provide actionable recommendations:**

**Recommendation format:**
```markdown
**Priority:** Critical | Major | Minor
**Gap:** [Specific missing element]
**Recommendation:** [Concrete action to take]
**Impact:** [Why this matters]
**Effort:** [Estimated time to address]
```

**Example:**
```markdown
**Priority:** Critical
**Gap:** Security architecture section missing
**Recommendation:** Add security architecture section covering authentication, authorization, encryption, and input validation
**Impact:** Security is fundamental for production readiness
**Effort:** 2-3 hours
```

**See:** `references/templates.md` for recommendation and report templates

---

### 13. Generate Validation Report

**Create comprehensive validation report:**

```markdown
# Architecture Validation Report

**Architecture:** [file path]
**Project Type:** [detected type]
**Validation Date:** [timestamp]
**Validation Result:** PASS | FAIL

---

## Quality Score: [score]/100

**Grade:** [A/B/C/D/F]

**Score Breakdown:**
- Completeness: [X]/40
- Technology Stack: [X]/15
- NFR Coverage: [X]/15
- ADRs: [X]/15
- Security: [X]/10
- Scalability: [X]/10
- Deployment: [X]/10

---

## Sections Present

✅ System Overview
✅ Component Architecture (Frontend)
✅ Technology Stack
❌ Security Architecture (MISSING)
⚠️  Scalability Plan (Incomplete)

---

## Gaps Identified

### Critical Gaps
1. Security architecture section missing
2. No NFR coverage

### Major Gaps
3. Only 2 ADRs (minimum 3 required)
4. Technology choices not justified

### Minor Gaps
5. Monitoring not discussed
6. Disaster recovery not mentioned

---

## Recommendations

### 1. Add Security Architecture (Critical)
**Gap:** Security section missing
**Action:** Document authentication, authorization, encryption, input validation
**Impact:** Production readiness blocker
**Effort:** 2-3 hours

### 2. Address NFRs (Critical)
**Gap:** Zero NFR coverage
**Action:** Add sections for performance targets, scalability plan, reliability targets
**Impact:** Architecture may not meet requirements
**Effort:** 1-2 hours

[... continue for all gaps ...]

---

## Summary

**Overall Assessment:** [Summary paragraph]

**Next Steps:**
1. Address all critical gaps
2. Address major gaps
3. Re-run validation
4. Proceed to implementation when score ≥70

---

**Validation Tool:** BMAD Enhanced validate-architecture skill
**Validated by:** Winston (Architect)
```

---

## Common Scenarios

### Scenario 1: High-Quality Architecture (Score 85+)
**Result:** PASS with minor recommendations
**Action:** Proceed to implementation, optionally address minor gaps

### Scenario 2: Acceptable Architecture (Score 70-79)
**Result:** PASS with major recommendations
**Action:** Address major gaps before implementation

### Scenario 3: Insufficient Architecture (Score <70)
**Result:** FAIL
**Action:** Address all critical and major gaps, then re-validate

### Scenario 4: Missing Critical Sections
**Result:** FAIL (auto-fail for missing critical sections)
**Action:** Add missing sections, re-validate

---

## Strict Mode

**When enabled (--strict):**
- Minimum score: 80 (instead of 70)
- All major gaps must be addressed
- ADR quality rigorously checked
- More detailed NFR validation

**Use strict mode for:**
- Production systems
- High-complexity projects
- Compliance-sensitive applications
- Enterprise deployments

---

## Best Practices

1. **Run early and often** - Validate during architecture creation, not after
2. **Address critical gaps immediately** - Don't proceed with critical gaps
3. **Iterate** - Re-validate after addressing gaps
4. **Use as checklist** - Reference validation checklist while creating architecture
5. **Don't over-optimize** - Score of 70-80 is usually sufficient for implementation

---

## Reference Files

- `references/validation-rules.md` - Comprehensive validation rules, scoring criteria, and rubrics for all dimensions
- `references/templates.md` - Validation report templates, recommendation formats, and output structures
- `references/examples.md` - Complete validation examples showing PASS (85/100), borderline PASS (72/100), and FAIL (42/100) scenarios

---

## When to Escalate

Escalate to user when:
- Architecture file not found or unreadable
- Unable to detect project type automatically
- Score is below 50 (major rework needed)
- Critical compliance issues detected
- Architecture deviates significantly from standards

---

*Part of BMAD Enhanced Quality Suite*
