---
name: architecture-evolution-tracking
description: |
  Track architectural decisions and detect drift from ADRs (Architecture Decision Records). Calculate alignment score (0.00-1.00) showing code-to-design conformance. Auto-detect architectural violations and suggest refactoring. Integrate with Serena for architectural health monitoring. Use when: maintaining architectural integrity, reviewing large changes, documenting decisions, detecting drift, enforcing standards.

skill-type: STRUCTURAL
shannon-version: ">=5.6.0"

mcp-requirements:
  recommended:
    - name: serena
      purpose: Architecture compliance tracking, alerting, metrics
    - name: structure101
      purpose: Dependency analysis and architecture visualization
    - name: sonargraph
      purpose: Architecture quality metrics
    - name: qmstool
      purpose: Dependency structure matrix

allowed-tools: All
---

# Architecture Evolution Tracking - Quantified Design Alignment

## Purpose

Maintain alignment between code and architectural decisions. Calculate alignment score (0.00-1.00) showing conformance to ADRs. Auto-detect violations like circular dependencies, layer violations, and unauthorized coupling. Track architecture health via Serena MCP.

## When to Use

- Reviewing large architectural changes
- Detecting unauthorized couplings between modules
- Monitoring compliance with ADRs
- Preventing architectural drift
- Planning refactoring work
- Measuring architecture quality evolution

## Core Metrics

**Alignment Score Calculation:**
```
Score = 1.0 - (Violations / Total Dependencies) × 1.0
Range: 0.00 (complete chaos) to 1.00 (perfect alignment)

Violations: Unauthorized dependencies, circular refs, layer violations
Total Dependencies: All module-to-module connections

Example: 5 violations in 200 dependencies = 0.975 score
```

**Violation Types & Impact:**
- Circular dependencies: -0.15 per cycle
- Layer violations: -0.10 per violation
- Unauthorized coupling: -0.05 per edge
- Missing abstraction: -0.05 per case

**Architecture Scoring:**

```
Component: User Authentication Service
├─ Allowed dependencies: Core, Utils
├─ Actual dependencies: Core, Utils, Payment (VIOLATION)
├─ Violations: 1 (unauthorized Payment coupling)
├─ Alignment: 0.90 (1 violation in 10 deps)
└─ Status: ⚠️ Review needed

Component: Payment Processing
├─ Allowed: Core, Database, Logging
├─ Actual: Core → Auth (CIRCULAR), Database, Logging
├─ Violations: 2 (circular + missing abstraction)
├─ Alignment: 0.80
└─ Status: ❌ Critical refactoring needed
```

## Workflow

### Phase 1: ADR Definition
1. **Document decisions**: Create ADRs for major design choices
2. **Define boundaries**: Specify allowed module dependencies
3. **Set rules**: Layer separation, coupling limits
4. **Establish baseline**: Calculate initial alignment

**ADR Format Example:**
```
ADR-001: Layered Architecture

Decision:
Implement 4-layer architecture:
├─ Presentation (API, UI)
├─ Business Logic (Services)
├─ Data Access (Repositories)
└─ Infrastructure (Database, Cache)

Rules:
✓ Presentation → Business Logic
✓ Business Logic → Data Access
✓ Data Access → Infrastructure
✗ Backwards dependencies forbidden
✗ No cross-layer skipping
```

### Phase 2: Drift Detection
1. **Analyze dependencies**: Map actual code connections
2. **Compare to ADRs**: Identify deviations
3. **Classify violations**: Circular, layer breach, unauthorized
4. **Calculate score**: Quantify alignment
5. **Generate report**: Violations with locations

**Drift Detection Report:**
```
Architecture Alignment Score: 0.82
Status: ⚠️ Acceptable but drifting

Violations (5 total):
1. [CRITICAL] Circular: Auth ← → Payment (bidirectional)
   Files: src/auth/service.ts, src/payment/processor.ts
   Recommendation: Extract shared logic to Core module

2. [HIGH] Layer violation: UI imports Payment (skips Logic)
   Files: src/ui/checkout.tsx imports src/payment/api.ts
   Recommendation: Route through Service layer

3. [MEDIUM] Unauthorized: Logging imports Caching
   Files: src/logging/logger.ts imports src/cache/redis.ts
   Recommendation: Move redis to Infrastructure, use interface

Trend: Score dropped 0.05 over 2 weeks (drifting)
```

### Phase 3: Refactoring Guidance
1. **Suggest refactors**: Extract abstractions, break cycles
2. **Rank by impact**: Highest score improvement first
3. **Provide examples**: Show architecture-preserving patterns
4. **Estimate effort**: Complexity of each refactor

**Auto-Generated Refactoring Plan:**

Option A (Impact: +0.08, Effort: Medium):
```
Extract PaymentInterface from Payment service
├─ Create: src/core/interfaces/payment.ts
├─ Define: interface IPaymentProcessor
├─ Auth uses interface, not concrete Payment
└─ Breaks circular dependency
```

Option B (Impact: +0.05, Effort: Low):
```
Move caching utilities to Infrastructure
├─ Move: src/cache → src/infrastructure/caching
├─ Update imports in 3 files
├─ Preserves layer separation
```

### Phase 4: Serena Integration
1. **Track alignment**: Store score by commit, date
2. **Alert on drift**: Notify if score drops >0.05
3. **Correlate commits**: Identify who introduced violations
4. **Forecast trend**: Predict alignment in 30 days
5. **Schedule refactoring**: Plan when to fix violations

**Serena Push Format:**
```json
{
  "metric_type": "architecture_alignment",
  "project": "task-app",
  "alignment_score": 0.82,
  "violations": {
    "circular": 1,
    "layer_breach": 2,
    "unauthorized": 2
  },
  "violating_modules": [
    "auth",
    "payment",
    "ui"
  ],
  "refactoring_priority": "HIGH",
  "estimated_effort_hours": 16,
  "timestamp": "2025-11-20T14:00:00Z"
}
```

## Real-World Impact

**Enterprise CRM System:**
- Alignment score started: 0.65 (heavy circular dependencies)
- Serena tracked violations: 8 circular, 12 layer breaches
- Systematic refactoring over 6 sprints
- Final score: 0.94 (improved +0.29)
- Benefits: 40% reduction in integration bugs, easier testing

**Microservices Migration:**
- Initial: 0.88 (monolith had clean layers)
- Split into 5 services: 0.72 (interdependencies created drift)
- Serena alerted on 15 cross-service violations
- Implemented saga pattern + event bus
- Restored to 0.91 (services truly independent)

## Success Criteria

✅ Alignment score ≥0.90 maintained
✅ No circular dependencies
✅ All layers properly separated
✅ Violations tracked in Serena with remediation plans
✅ New code reviewed against ADRs
✅ Refactoring priorities data-driven by alignment impact
