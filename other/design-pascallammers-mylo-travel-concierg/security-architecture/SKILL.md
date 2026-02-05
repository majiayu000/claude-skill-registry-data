---
name: security-architecture
description: Design security architectures with threat modeling and zero trust
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 05-security-architecture
bond_type: PRIMARY_BOND
last_updated: "2025-01"
---

# Security Architecture Skill

## Purpose
Design and validate security architectures through threat modeling (STRIDE), zero trust implementation, and compliance alignment for enterprise systems.

---

## Parameters

| Parameter | Type | Required | Validation | Default |
|-----------|------|----------|------------|---------|
| `system` | string | ✅ | min: 50 chars | - |
| `analysis_type` | enum | ⚪ | threat_model\|zero_trust\|compliance\|review | `threat_model` |
| `threat_context` | enum | ⚪ | internal\|external\|both | `both` |
| `data_classification` | enum | ⚪ | public\|internal\|confidential\|restricted | `internal` |
| `compliance_frameworks` | array | ⚪ | valid frameworks | `[]` |

---

## Execution Flow

```
┌──────────────────────────────────────────────────────────┐
│ 1. VALIDATE: Check system description                     │
│ 2. CLASSIFY: Data and asset classification                │
│ 3. MODEL: Threat modeling (STRIDE)                        │
│ 4. DESIGN: Security controls                              │
│ 5. ALIGN: Map to compliance requirements                  │
│ 6. ASSESS: Risk assessment                                │
│ 7. DOCUMENT: Return security architecture                 │
└──────────────────────────────────────────────────────────┘
```

---

## Retry Logic

| Error | Retry | Backoff | Max Attempts |
|-------|-------|---------|--------------|
| `VALIDATION_ERROR` | No | - | 1 |
| `COMPLIANCE_LOOKUP_ERROR` | Yes | 1s | 2 |
| `THREAT_DB_ERROR` | Yes | 2s | 3 |

---

## Logging & Observability

```yaml
log_points:
  - event: analysis_started
    level: info
    data: [analysis_type, threat_context]
  - event: threats_identified
    level: info
    data: [threat_count, high_severity_count]
  - event: compliance_gaps_found
    level: warn
    data: [framework, gap_count]

metrics:
  - name: analyses_performed
    type: counter
    labels: [analysis_type]
  - name: threats_identified
    type: counter
    labels: [severity]
  - name: compliance_score
    type: gauge
```

---

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `E301` | Missing system context | Request architecture details |
| `E302` | Unknown compliance framework | Show supported frameworks |
| `E303` | Incomplete threat model | Flag missing threat categories |
| `E304` | Conflicting controls | Highlight conflicts |

---

## Unit Test Template

```yaml
test_cases:
  - name: "STRIDE threat model"
    input:
      system: "Web application handling customer PII"
      analysis_type: "threat_model"
      data_classification: "confidential"
    expected:
      has_threats: true
      stride_categories: 6
      has_mitigations: true

  - name: "Zero trust design"
    input:
      system: "Corporate application for remote workers"
      analysis_type: "zero_trust"
    expected:
      has_identity_model: true
      has_access_policies: true
      has_micro_segmentation: true

  - name: "Compliance gap analysis"
    input:
      system: "Healthcare patient portal"
      analysis_type: "compliance"
      compliance_frameworks: ["HIPAA"]
    expected:
      has_requirements: true
      has_gap_analysis: true
```

---

## Troubleshooting

### Common Issues

| Symptom | Root Cause | Resolution |
|---------|------------|------------|
| Incomplete threat model | Missing attack surface | Map all entry points |
| Compliance gaps | Missing controls | Map controls to requirements |
| Over-restrictive policies | Security vs usability | Balance with risk acceptance |

### Debug Checklist
```
□ Is system context complete?
□ Are all data flows documented?
□ Are all entry points identified?
□ Are threats mapped to mitigations?
□ Is compliance framework valid?
```

---

## STRIDE Quick Reference

| Threat | Mitigation Category |
|--------|---------------------|
| Spoofing | Authentication |
| Tampering | Integrity controls |
| Repudiation | Logging/Audit |
| Information Disclosure | Encryption |
| Denial of Service | Availability |
| Elevation of Privilege | Authorization |

---

## Integration

| Component | Trigger | Data Flow |
|-----------|---------|-----------|
| Agent 05 | Security request | Receives system, returns threat model |
| Agent 04 | Cloud security | Provides security requirements |

---

## Quality Standards

- **Defense in depth:** Multiple control layers
- **Privacy by design:** Data minimization
- **Least privilege:** Minimal access

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade: STRIDE, compliance mapping |
| 1.0.0 | 2024-12 | Initial release |
