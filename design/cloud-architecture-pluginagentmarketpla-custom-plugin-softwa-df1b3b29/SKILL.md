---
name: cloud-architecture
description: Design cloud-native architectures with service selection and cost optimization
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 04-cloud-architecture
bond_type: PRIMARY_BOND
last_updated: "2025-01"
---

# Cloud Architecture Skill

## Purpose
Design cloud infrastructure architectures with appropriate service selection, cost optimization, and deployment strategies across AWS, Azure, and GCP.

---

## Parameters

| Parameter | Type | Required | Validation | Default |
|-----------|------|----------|------------|---------|
| `workload` | string | ✅ | min: 30 chars | - |
| `provider` | enum | ⚪ | aws\|azure\|gcp\|multi | `aws` |
| `requirements` | object | ⚪ | valid JSON | `{}` |
| `budget_tier` | enum | ⚪ | startup\|growth\|enterprise | `growth` |
| `architecture_type` | enum | ⚪ | serverless\|containers\|vms\|hybrid | `containers` |

**Requirements Schema:**
```json
{
  "availability": "99.9%",
  "latency_ms": 100,
  "monthly_budget_usd": 5000
}
```

---

## Execution Flow

```
┌──────────────────────────────────────────────────────────┐
│ 1. VALIDATE: Check workload and requirements              │
│ 2. ANALYZE: Workload characteristics                      │
│ 3. SELECT: Cloud services for each component              │
│ 4. DESIGN: Architecture diagram                           │
│ 5. ESTIMATE: Cost projection                              │
│ 6. OPTIMIZE: Apply cost/performance optimizations         │
│ 7. DOCUMENT: Return architecture with IaC snippets        │
└──────────────────────────────────────────────────────────┘
```

---

## Retry Logic

| Error | Retry | Backoff | Max Attempts |
|-------|-------|---------|--------------|
| `PROVIDER_ERROR` | Yes | 2s, 4s | 3 |
| `COST_CALC_ERROR` | Yes | 1s | 2 |
| `VALIDATION_ERROR` | No | - | 1 |

---

## Logging & Observability

```yaml
log_points:
  - event: design_started
    level: info
    data: [provider, architecture_type]
  - event: cost_estimate_complete
    level: info
    data: [monthly_estimate_usd, services_count]
  - event: optimization_applied
    level: info
    data: [optimization_type, savings_percent]

metrics:
  - name: architectures_designed
    type: counter
    labels: [provider]
  - name: design_time_ms
    type: histogram
  - name: estimated_monthly_cost
    type: gauge
```

---

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `E201` | Invalid provider | Show supported providers |
| `E202` | Budget exceeded | Suggest lower-cost alternatives |
| `E203` | Conflicting requirements | Highlight trade-offs |
| `E204` | Service not available in region | Suggest alternatives |

---

## Unit Test Template

```yaml
test_cases:
  - name: "Web app on AWS"
    input:
      workload: "E-commerce web application with 10K daily users"
      provider: "aws"
      architecture_type: "containers"
    expected:
      has_services: true
      has_diagram: true
      has_cost_estimate: true
      services_include: ["ECS", "RDS", "CloudFront"]

  - name: "Serverless API"
    input:
      workload: "RESTful API with variable traffic"
      provider: "aws"
      architecture_type: "serverless"
    expected:
      services_include: ["Lambda", "API Gateway", "DynamoDB"]

  - name: "Budget exceeded"
    input:
      workload: "Enterprise data warehouse"
      requirements: { "monthly_budget_usd": 100 }
    expected:
      warning: "budget_exceeded"
      has_alternatives: true
```

---

## Troubleshooting

### Common Issues

| Symptom | Root Cause | Resolution |
|---------|------------|------------|
| High cost estimate | Wrong service tier | Right-size, use reserved |
| Single point of failure | Missing HA design | Add multi-AZ, redundancy |
| Vendor lock-in warning | Proprietary services | Use portable alternatives |

### Debug Checklist
```
□ Is provider selection appropriate?
□ Are availability requirements met?
□ Is cost within budget?
□ Are all components connected?
□ Is IaC syntax valid?
```

---

## Service Quick Reference

| Component | AWS | Azure | GCP |
|-----------|-----|-------|-----|
| Compute | ECS/Lambda | AKS/Functions | GKE/Cloud Functions |
| Database | RDS/Aurora | SQL Database | Cloud SQL |
| Storage | S3 | Blob Storage | Cloud Storage |
| Cache | ElastiCache | Cache for Redis | Memorystore |

---

## Integration

| Component | Trigger | Data Flow |
|-----------|---------|-----------|
| Agent 04 | Design request | Receives workload, returns architecture |
| Agent 05 | Security review | Provides security requirements |

---

## Quality Standards

- **Cost-aware:** Always include estimates
- **HA by default:** Multi-AZ unless specified
- **IaC-ready:** Include Terraform/CloudFormation snippets

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade: multi-cloud, cost estimation, IaC |
| 1.0.0 | 2024-12 | Initial release |
