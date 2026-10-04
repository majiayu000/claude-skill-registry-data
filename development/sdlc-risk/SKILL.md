---
name: sdlc-risk
description: Assess risks for a TriStar feature implementation. Analyzes technical, domain, and operational risks. READ-ONLY - produces risk assessment with ship recommendation.
allowed-tools: Read, Grep, Glob
---

# SDLC Risk Assessment Skill

## Prime Directive

**"Your job is to BREAK things."**

Think like an adversary. Find every way this feature could fail, cause data corruption, leak PII, spam members, or degrade the system. Then quantify the risk and recommend whether to ship.

This is a READ-ONLY skill. It reads artifacts and code but does not modify anything.

## Arguments

- `--feature=<name>` (required) - Feature name matching existing artifacts

## Prerequisites

- `docs/artifacts/<feature>/problem_spec.md` must exist
- `docs/artifacts/<feature>/design_spec.md` must exist
- `docs/artifacts/<feature>/verification_report.md` should exist (risk is higher without verification)
- Implementation code should exist

## Process

### Step 1: Load All Artifacts
Read problem spec, design spec, implementation plan, code review, and verification report. Build a complete picture of what was planned vs what was built.

### Step 2: Catalog Technical Risks
Scan implementation for:
- Unhandled error paths
- Missing input validation
- Concurrency issues (Hub state transitions)
- External dependency failures (Claude API, Weather API, Redis)
- Performance bottlenecks

### Step 3: Catalog Domain Risks
Reference `references/tristar-risk-catalog.md` for TriStar-specific risks:
- Loyalty fraud vectors
- PII exposure paths
- Rate limiting failures
- Context signal reliability
- Hub state corruption scenarios

### Step 4: Catalog Operational Risks
Assess deployment and runtime risks:
- Azure service failures
- Configuration errors
- Monitoring gaps
- Rollback complexity

### Step 5: Score Each Risk
For each identified risk:
- **Likelihood**: 1 (rare) to 5 (almost certain)
- **Impact**: 1 (negligible) to 5 (catastrophic)
- **Risk Score**: Likelihood x Impact (1-25)
- **Severity**: Low (1-6), Medium (7-12), High (13-18), Critical (19-25)

### Step 6: Assess Mitigations
For each risk:
- Is there a mitigation in place?
- Is the mitigation adequate?
- What is the residual risk after mitigation?

### Step 7: Identify Risk Clusters
Group related risks that could cascade:
- Example: Weather API down -> context score incomplete -> wrong activation decisions -> member spam

### Step 8: Calculate Overall Risk Score
Aggregate individual risk scores:
- Count of Critical risks
- Count of High risks
- Count of Medium risks
- Count of Low risks
- Any unmitigated Critical or High risks?

### Step 9: Make Ship Recommendation

| Recommendation | Criteria |
|---------------|----------|
| **ship** | 0 Critical, 0 unmitigated High, total risk score < 50 |
| **ship_with_monitoring** | 0 Critical, <= 2 High (all mitigated), total risk score < 100 |
| **fix_first** | 1+ Critical OR 3+ unmitigated High risks |
| **redesign** | 3+ Critical risks OR fundamental architectural flaw |

### Step 10: Write Risk Assessment
Save to: `docs/artifacts/<feature>/risk_assessment.md`

## TriStar-Specific Risk Considerations

### Loyalty Domain Risks
- Over-discounting: can this feature cause offers with >30% discount to bypass fraud detection?
- Member spam: can this feature send >1 notification per hour to a member?
- Quiet hours violation: can this feature trigger notifications between 10pm-8am?
- Offer stacking: can this feature allow >2 concurrent active offers for one member?
- Cannibalization: can this feature create competing offers for the same segment?

### Data Integrity Risks
- Hub state corruption: can concurrent requests leave Hub in an invalid state?
- OfferBrief schema mismatch: are Zod and Pydantic models in sync?
- Orphaned offers: can offers get stuck in approved state forever?

### Privacy Risks
- PII in logs: does any log statement contain member names, emails, addresses, or phone numbers?
- GPS data exposure: are raw coordinates stored or logged?
- Claude API prompt leakage: does the prompt contain member PII?

### External Dependency Risks
- Claude API: outage, rate limiting, cost overrun, model deprecation
- Weather API: outage, stale data, rate limiting
- Azure Redis Cache: eviction, failover, connection loss
- Azure Key Vault: access failure, secret rotation

## Output Format

```markdown
# Risk Assessment: <feature-name>

## Summary
- **Date**: <date>
- **Overall Risk Score**: <N>
- **Recommendation**: ship / ship_with_monitoring / fix_first / redesign
- **Critical Risks**: N
- **High Risks**: N
- **Medium Risks**: N
- **Low Risks**: N

## Risk Catalog

### Critical Risks
| ID | Risk | Likelihood | Impact | Score | Mitigation | Residual |
|----|------|-----------|--------|-------|------------|----------|
| R-001 | ... | 5 | 5 | 25 | ... | ... |

### High Risks
...

### Medium Risks
...

### Low Risks
...

## Risk Clusters
1. **<cluster name>**: R-001 -> R-003 -> R-007 (cascade path)

## Ship Recommendation
**<recommendation>**: <detailed rationale>

### If ship_with_monitoring:
- Monitor: <what to watch>
- Alert: <when to alert>
- Rollback trigger: <condition for rollback>

### If fix_first:
- Fix R-001: <what to fix>
- Fix R-002: <what to fix>
- Re-assess after fixes

### If redesign:
- Fundamental issue: <description>
- Suggested approach: <alternative>
```

## Reference Files

- `references/risk-process.md` - Detailed 10-step risk process
- `references/tristar-risk-catalog.md` - Domain-specific risk catalog
