---
name: sdlc-design-review
description: Critically review architecture design for a TriStar feature. Challenges assumptions, validates patterns, scores quality, and makes gate decisions. READ-ONLY - does not modify source code.
allowed-tools: Read, Grep, Glob
---

# SDLC Design Review Skill

## Prime Directive

**"Challenge everything. Accept nothing at face value."**

This is a READ-ONLY skill. It produces a design review document but does NOT modify any source code or design artifacts. Its job is to find weaknesses, gaps, and risks in the architecture before implementation begins.

## Arguments

- `--feature=<name>` (required) - Feature name matching the design_spec.md artifact

## Prerequisites

- `docs/artifacts/<feature>/problem_spec.md` must exist
- `docs/artifacts/<feature>/design_spec.md` must exist

## Process

### Step 1: Load Artifacts

Read all available artifacts for the feature:
1. `docs/artifacts/<feature>/problem_spec.md` - Requirements baseline
2. `docs/artifacts/<feature>/design_spec.md` - Architecture to review
3. `docs/ARCHITECTURE.md` - System architecture baseline
4. `.claude/rules/` - Coding standards (react-19-standards.md, fastapi-standards.md, code-style.md, testing.md, security.md)

### Step 2: Determine Review Mode

- **Initial Review**: No existing design_review.md - full review of the design
- **Re-Review**: Existing design_review.md present - verify previous findings are addressed, check for new issues introduced by refinements

### Step 3: Codebase Validation

Scan the actual codebase to verify design assumptions:
- Do referenced files and directories exist?
- Do referenced components have the expected interfaces?
- Are there existing patterns that the design contradicts?
- React 19 patterns: Server Components default, React.use() for data fetching, no useEffect for fetching
- FastAPI patterns: async/await all routes, Depends() for DI, Pydantic v2 models
- Does the design follow the 3-layer architecture (Designer -> Hub -> Scout)?

### Step 4: Execute All Review Dimensions

Run all 6 review dimensions (see below). For each dimension, produce:
- **Findings**: Specific issues discovered (with severity: Critical / Major / Minor)
- **Questions**: Unresolved questions for the architect
- **Recommendations**: Suggested improvements

### Step 5: Score Quality

Calculate an overall quality score (0-100) based on findings:
- Start at 100
- Critical finding: -15 points each
- Major finding: -8 points each
- Minor finding: -3 points each
- Bonus: +5 for each dimension with zero findings (max +30)

### Step 6: Make Gate Decision

Based on the quality score:
- **APPROVE** (score >= 70): Design is ready for implementation planning
- **APPROVE_WITH_CONCERNS** (score >= 50, < 70): Design can proceed but concerns must be tracked
- **REJECT** (score < 50): Design needs significant rework before proceeding

### Step 7: Output design_review.md

Save the review to: `docs/artifacts/<feature>/design_review.md`

Include:
- Review summary
- All findings by dimension
- Quality score breakdown
- Gate decision with rationale
- Recommendations for improvement (if not APPROVE)

---

## Review Dimensions

### Dimension A: Codebase Validation

Verify the design is grounded in the actual codebase, not an idealized version.

**TriStar-Specific Checks:**
- React 19 Server Components are default (no unnecessary 'use client')
- FastAPI routes use async/await consistently
- Pydantic v2 models use `model_validator` and `field_validator` (not v1 `@validator`)
- OfferBrief shared type exists in `src/shared/types/` and is referenced correctly
- Hub state store abstraction supports both in-memory (dev) and Redis (prod)
- Context signal interfaces match what Scout actually processes

**Probing Questions:**
- Does component X actually exist at the referenced path?
- Does the existing interface match what the design assumes?
- Are there existing utilities that could replace proposed new components?

### Dimension B: Architectural Review

Verify the design maintains architectural integrity.

**TriStar-Specific Checks:**
- 3-layer separation maintained (no Designer->Scout bypass)
- Hub state machine transitions are valid (no invalid paths)
- All inter-layer communication flows through Hub
- ADRs have genuine alternatives (not strawman comparisons)
- Component responsibilities are single-purpose
- No circular dependencies between layers
- Fraud detection runs before approval (not after)
- Rate limiting enforced at Scout layer (not delegated to client)

**Probing Questions:**
- Could this component be split into smaller, more focused components?
- Is this the right layer for this responsibility?
- What happens if Hub is temporarily unavailable?

### Dimension C: Assumption Challenges

Challenge every assumption in the design.

**TriStar-Specific Challenges:**
- Context signal availability: GPS may not be available indoors. Weather API has downtime. Behavior data ages.
- Claude API reliability: What if latency is 5s instead of 200ms? What if rate limited?
- Redis reliability: What if Azure Redis Cache has an outage? Failover behavior?
- Member timezone accuracy: Is timezone data reliable for quiet hours enforcement?
- Segment data freshness: How recent must member segment data be?

**Probing Questions:**
- What evidence supports this assumption?
- What happens if this assumption is wrong?
- Has this been validated with production data?

### Dimension D: Complexity Concerns

Identify unnecessary complexity.

**Checks:**
- Is any component doing more than it should? (Essential vs accidental complexity)
- Are there simpler alternatives that meet the same requirements?
- Is the number of new components proportional to the feature scope?
- Are there over-engineered abstractions?
- Could existing patterns be reused instead of creating new ones?

**Probing Questions:**
- What is the simplest design that satisfies all P0 requirements?
- Which components could be eliminated without losing functionality?
- Is this abstraction earning its complexity cost?

### Dimension E: Alternative Approaches

Evaluate whether major decisions considered real alternatives.

**Checks:**
- Every ADR has at least 2 genuine alternatives (not strawmen)
- The chosen approach has clear advantages over alternatives
- Trade-offs are honestly documented
- The simplest approach that meets requirements was considered

**Probing Questions:**
- Why was the simpler approach rejected?
- What would change if we chose alternative B instead?
- Is the chosen approach the best fit for a 3-layer loyalty system?

### Dimension F: Missing Considerations

Identify what the design failed to address.

**TriStar-Specific Missing Items to Check:**
- Error handling: What happens when Claude API fails? Weather API? Redis?
- Observability: Is structured logging (loguru) addressed? Metrics? Audit trail?
- Rate limiting: 1/hr/member, 24h dedup, quiet hours (10pm-8am) all enforced?
- Fraud detection: All risk flags checked (over_discounting, cannibalization, frequency_abuse, offer_stacking)?
- PII protection: Only member_id in logs? No GPS coords in plaintext?
- Backward compatibility: Existing Hub state data preserved?
- Feature flags: Rollout strategy defined?
- Testing: Coverage targets set for all layers?

**Probing Questions:**
- What happens when [external dependency] is unavailable?
- Where are the monitoring hooks for production?
- How will this feature be tested end-to-end?

---

## Output Format

```markdown
# Design Review: <feature-name>

## Review Summary
- **Date**: <date>
- **Review Mode**: Initial / Re-Review
- **Score**: <N>/100
- **Decision**: APPROVE / APPROVE_WITH_CONCERNS / REJECT

## Findings

### Dimension A: Codebase Validation
- [CRITICAL] F-001: <finding>
- [MAJOR] F-002: <finding>
- [MINOR] F-003: <finding>

### Dimension B: Architectural Review
...

### Dimension C: Assumption Challenges
...

### Dimension D: Complexity Concerns
...

### Dimension E: Alternative Approaches
...

### Dimension F: Missing Considerations
...

## Score Breakdown
| Category | Count | Points |
|----------|-------|--------|
| Critical | N | -N*15 |
| Major | N | -N*8 |
| Minor | N | -N*3 |
| Clean Dimensions | N | +N*5 |
| **Total** | | **N/100** |

## Gate Decision
**<DECISION>**: <rationale>

## Recommendations
1. <recommendation>
2. <recommendation>
...
```

## Reference Files

- `references/review-dimensions.md` - Detailed criteria for each review dimension
