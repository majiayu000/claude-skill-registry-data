---
name: aws-cost-optimization
description: Optimize AWS costs through resource rightsizing and savings strategies
sasmp_version: "1.3.0"
bonded_agent: 01-aws-fundamentals
bond_type: SECONDARY_BOND
---

# AWS Cost Optimization Skill

Reduce AWS spending while maintaining performance and reliability.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Services | Cost Explorer, Budgets, Trusted Advisor |
| Complexity | Medium |
| Est. Time | 30-60 min analysis |
| Prerequisites | Cost & Usage Reports access |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| time_period | string | Analysis period | last_30_days, last_90_days |
| scope | array | Service types | ["EC2", "RDS", "S3"] |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| savings_target | float | 20 | Target savings % |
| include_recommendations | bool | true | Include AWS recommendations |
| tag_filter | object | {} | Filter by tags |

## Cost Optimization Framework

```
┌─────────────────────────────────────────────────────────┐
│                  COST OPTIMIZATION                       │
├─────────────────────────────────────────────────────────┤
│ 1. RIGHT SIZE     │ Match resources to actual usage     │
│ 2. SAVINGS PLANS  │ Commit for 30-72% savings           │
│ 3. SPOT/RESERVED  │ Use discount pricing models         │
│ 4. STORAGE TIER   │ Move data to cheaper storage        │
│ 5. CLEANUP        │ Remove unused resources             │
└─────────────────────────────────────────────────────────┘
```

## Savings Strategies by Service

### EC2 Optimization
| Strategy | Effort | Savings |
|----------|--------|---------|
| Right-sizing | Low | 10-50% |
| Graviton (arm64) | Medium | 40% |
| Spot Instances | Medium | 60-90% |
| Savings Plans | Low | 30-72% |
| Reserved Instances | Low | 30-60% |
| Scheduled scaling | Medium | 20-40% |

### RDS Optimization
| Strategy | Effort | Savings |
|----------|--------|---------|
| Right-sizing | Low | 10-40% |
| Reserved Instances | Low | 30-60% |
| Aurora Serverless | Medium | Variable |
| Multi-AZ review | Low | 50% (if not needed) |
| Storage optimization | Low | 10-30% |

### S3 Optimization
| Strategy | Effort | Savings |
|----------|--------|---------|
| Intelligent-Tiering | Low | 20-40% |
| Lifecycle policies | Low | 40-80% |
| Glacier transition | Low | 80-95% |
| Cleanup old versions | Low | 10-30% |
| Compression | Medium | 20-50% |

## Implementation

### Cost Analysis Query
```bash
# Get cost by service
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# Get rightsizing recommendations
aws ce get-rightsizing-recommendation \
  --service EC2 \
  --configuration '{
    "RecommendationTarget": "SAME_INSTANCE_FAMILY",
    "BenefitsConsidered": true
  }'
```

### Budget Alert
```bash
aws budgets create-budget \
  --account-id 123456789012 \
  --budget '{
    "BudgetName": "Monthly-Total",
    "BudgetLimit": {"Amount": "1000", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [{
      "SubscriptionType": "EMAIL",
      "Address": "alerts@company.com"
    }]
  }]'
```

### Savings Plan Analysis
```bash
# Get Savings Plans recommendations
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT \
  --lookback-period-in-days SIXTY_DAYS
```

## Cost Checklist

### Quick Wins (Low Effort, High Impact)
- [ ] Delete unattached EBS volumes
- [ ] Release unused Elastic IPs
- [ ] Remove old EBS snapshots
- [ ] Delete unused load balancers
- [ ] Terminate stopped EC2 instances
- [ ] Clean up old AMIs
- [ ] Review NAT Gateway data transfer

### Medium-Term (Medium Effort)
- [ ] Right-size EC2 instances
- [ ] Implement S3 lifecycle policies
- [ ] Migrate to Graviton instances
- [ ] Use Spot for fault-tolerant workloads
- [ ] Purchase Savings Plans
- [ ] Implement auto-scaling

### Long-Term (High Effort, Strategic)
- [ ] Modernize to serverless
- [ ] Optimize data transfer architecture
- [ ] Implement FinOps practices
- [ ] Tag everything for cost allocation

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| Unexpected costs | Unused resources | Enable Cost Anomaly Detection |
| Data transfer spike | Cross-region/AZ | Use VPC endpoints |
| Storage growth | No lifecycle rules | Implement policies |
| NAT Gateway costs | Heavy outbound | Use VPC endpoints |

### Cost Anomaly Detection
```bash
aws ce create-anomaly-monitor \
  --anomaly-monitor '{
    "MonitorName": "cost-anomalies",
    "MonitorType": "DIMENSIONAL",
    "MonitorDimension": "SERVICE"
  }'

aws ce create-anomaly-subscription \
  --anomaly-subscription '{
    "SubscriptionName": "alert-subscription",
    "MonitorArnList": ["arn:aws:ce::...:anomalymonitor/..."],
    "Subscribers": [{
      "Type": "EMAIL",
      "Address": "alerts@company.com"
    }],
    "Threshold": 100
  }'
```

## Monthly Review Checklist

```yaml
weekly:
  - Check Cost Anomaly alerts
  - Review Trusted Advisor recommendations

monthly:
  - Run rightsizing analysis
  - Review Savings Plans utilization
  - Check Reserved Instance coverage
  - Analyze data transfer costs
  - Clean up unused resources

quarterly:
  - Evaluate Savings Plans purchase
  - Architecture optimization review
  - Tag compliance audit
```

## Test Template

```python
def test_cost_optimization_compliance():
    # Check for unattached EBS volumes
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'status', 'Values': ['available']}]
    )
    assert len(volumes['Volumes']) == 0, "Unattached EBS volumes found"

    # Check for unused Elastic IPs
    addresses = ec2.describe_addresses()
    unattached = [a for a in addresses['Addresses'] if 'InstanceId' not in a]
    assert len(unattached) == 0, "Unused Elastic IPs found"
```

## Assets

- `assets/cost-checklist.yaml` - Cost optimization checklist

## References

- [AWS Cost Optimization](https://aws.amazon.com/pricing/cost-optimization/)
- [Well-Architected Cost Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)
