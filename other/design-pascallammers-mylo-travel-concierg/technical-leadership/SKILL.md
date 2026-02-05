---
name: technical-leadership
description: Provide technical leadership guidance for reviews, mentoring, and decisions
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 07-technical-leadership
bond_type: PRIMARY_BOND
last_updated: "2025-01"
---

# Technical Leadership Skill

## Purpose
Provide structured technical leadership guidance including architecture reviews, mentoring frameworks, and decision facilitation for engineering teams.

---

## Parameters

| Parameter | Type | Required | Validation | Default |
|-----------|------|----------|------------|---------|
| `context` | string | ✅ | min: 30 chars | - |
| `guidance_type` | enum | ⚪ | review\|mentoring\|decision\|standards | `review` |
| `team_size` | integer | ⚪ | 1-100 | 5 |
| `decision_stakes` | enum | ⚪ | low\|medium\|high\|critical | `medium` |
| `output_format` | enum | ⚪ | checklist\|narrative\|action_items | `action_items` |

---

## Execution Flow

```
┌──────────────────────────────────────────────────────────┐
│ 1. VALIDATE: Check context and guidance type             │
│ 2. ANALYZE: Understand leadership challenge              │
│ 3. FRAMEWORK: Select appropriate framework               │
│ 4. APPLY: Apply framework to context                     │
│ 5. SYNTHESIZE: Generate recommendations                  │
│ 6. STRUCTURE: Format output appropriately                │
│ 7. DELIVER: Return guidance with action items            │
└──────────────────────────────────────────────────────────┘
```

---

## Retry Logic

| Error | Retry | Backoff | Max Attempts |
|-------|-------|---------|--------------|
| `VALIDATION_ERROR` | No | - | 1 |
| `FRAMEWORK_ERROR` | Yes | 1s | 2 |
| `CONTEXT_UNCLEAR` | Yes | - | 2 |

---

## Logging & Observability

```yaml
log_points:
  - event: guidance_requested
    level: info
    data: [guidance_type, decision_stakes]
  - event: framework_applied
    level: info
    data: [framework_name, context_type]
  - event: guidance_delivered
    level: info
    data: [action_items_count, confidence]

metrics:
  - name: guidance_requests
    type: counter
    labels: [guidance_type]
  - name: response_time_ms
    type: histogram
  - name: action_items_generated
    type: counter
```

---

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `E501` | Missing context | Request specific situation |
| `E502` | Invalid guidance type | Show available types |
| `E503` | Conflicting requirements | Highlight trade-offs |
| `E504` | Stakes not specified | Default to medium |

---

## Unit Test Template

```yaml
test_cases:
  - name: "Architecture review"
    input:
      context: "Review microservices migration proposal"
      guidance_type: "review"
      decision_stakes: "high"
    expected:
      has_checklist: true
      has_findings: true
      has_recommendation: true

  - name: "Mentoring guidance"
    input:
      context: "Senior engineer wants to grow into tech lead"
      guidance_type: "mentoring"
    expected:
      has_grow_framework: true
      has_action_items: true
      has_timeline: true

  - name: "Decision facilitation"
    input:
      context: "Team split on REST vs GraphQL"
      guidance_type: "decision"
    expected:
      has_rapid_model: true
      has_decision_matrix: true
      has_recommendation: true
```

---

## Troubleshooting

### Common Issues

| Symptom | Root Cause | Resolution |
|---------|------------|------------|
| Vague recommendations | Context too broad | Narrow scope |
| No clear decision | Missing decision framework | Apply RAPID |
| Review bottleneck | Too many reviews | Delegate, set SLAs |

### Debug Checklist
```
□ Is the leadership challenge clear?
□ Is the appropriate framework selected?
□ Are stakeholders identified?
□ Are decision criteria explicit?
□ Are action items specific and actionable?
```

---

## Frameworks Quick Reference

| Framework | Use Case |
|-----------|----------|
| **RAPID** | Complex decisions with multiple stakeholders |
| **GROW** | Mentoring and coaching conversations |
| **RFC** | Technical design decisions |
| **ADR** | Architecture decision documentation |

---

## Integration

| Component | Trigger | Data Flow |
|-----------|---------|-----------|
| Agent 07 | Leadership request | Receives context, returns guidance |
| All Agents | Coordination | Synthesizes recommendations |

---

## Quality Standards

- **Actionable:** All guidance includes next steps
- **Fair:** Unbiased, considers all perspectives
- **Documented:** Decisions and rationale recorded

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade: RAPID, GROW, review checklists |
| 1.0.0 | 2024-12 | Initial release |
