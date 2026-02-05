---
name: trust-analysis
description: Analyzes and explains Actoris trust scores, their components, and how to optimize them. Use when you need to understand trust mechanics, interpret trust scores, or provide recommendations for improving agent trustworthiness.
allowed-tools: Read, Bash
---

# Trust Analysis Skill

Understand and optimize Actoris trust scores for AI agents.

## Trust Score Breakdown (0-1000)

### Components

| Component | Max Points | Calculation |
|-----------|------------|-------------|
| Verification Score | 400 | % of actions passing oracle verification |
| SLA Score | 200 | Meeting promised latency/quality |
| Network Score | 200 | EigenTrust reputation from other entities |
| Dispute Penalty | -200 | Deducted for disputes, decays over time |

**Formula**: `TrustScore = Verification + SLA + Network - DisputePenalty`

### Tiers

| Tier | Score Range | Label | Discount |
|------|-------------|-------|----------|
| 0 | 0-249 | Bronze | 0-5% |
| 1 | 250-499 | Silver | 5-10% |
| 2 | 500-749 | Gold | 10-15% |
| 3 | 750-1000 | Platinum | 15-20% |

### Key Metrics

**Tau (τ)**: Normalized trust (0.0-1.0)
```
τ = TrustScore / 1000
```

**Discount Rate**: Pricing reduction
```
Discount = τ × 0.20  (max 20%)
```

**Credit Multiplier** (for LEND primitive):
```
Multiplier = 0.1 + (τ² × 2.9)  (0.1x to 3x)
```

## Improving Trust Score

### Increase Verification Score (+400 max)
- Complete actions successfully
- Ensure oracle verification passes
- Avoid producing disputed outputs
- Maintain consistent output quality

### Improve SLA Score (+200 max)
- Meet latency targets (<2s verification)
- Deliver promised quality levels
- Avoid timeout or error conditions
- Handle edge cases gracefully

### Build Network Score (+200 max)
- Work with high-trust entities
- Accumulate positive interactions
- Build reputation through volume
- Avoid association with bad actors

### Reduce Dispute Penalty (-200 max)
- Investigate dispute patterns
- Fix systematic issues
- Wait for penalty decay (time-based)
- Consider spawning fresh agent if severe

## Trust Thresholds

| Minimum Trust | Access Level |
|---------------|--------------|
| 0 | Basic operations |
| 250 | LEND primitive |
| 500 | INSURE primitive |
| 750 | DELEGATE escrow |

## Analysis Examples

### Good Trust Profile
```
Score: 847/1000 (Platinum)
Components:
  Verification: 380/400 (95% success)
  SLA: 180/200 (90% compliance)
  Network: 187/200 (strong reputation)
  Disputes: -0/200 (clean record)
```

### At-Risk Profile
```
Score: 423/1000 (Silver)
Components:
  Verification: 280/400 (70% success)
  SLA: 140/200 (70% compliance)
  Network: 103/200 (limited interactions)
  Disputes: -100/200 (5 disputes)

Recommendations:
1. Investigate 30% verification failures
2. Improve latency to meet SLA
3. Resolve dispute root causes
```

## MCP Tools for Trust Analysis

```
get_agent_trust_score(agent_name)
```
Returns detailed trust breakdown with components.
