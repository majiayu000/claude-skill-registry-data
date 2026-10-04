---
name: aws-cost
description: AWS Cost Optimizer. Automated cloud infrastructure scanning to detect idle resources and expenditure anomalies.
version: 3.0.0
author: AgentBoost Enterprise
enterprise: true
category: Finance
---

### System Instructions
You are equipped with the `aws-cost` deterministic tool. This tool scans AWS infrastructure via IAM-secured read access to detect idle EC2 instances, unallocated EBS volumes, and billing anomalies. It generates one-click cost reduction scripts to align spending with actual utilization.

### Execution Protocol
Invoke the AWS engine by passing strictly formatted JSON:

```json
{
  "aws_account_alias": "AgentBoost_Production",
  "scanning_scope": ["EC2", "EBS", "RDS", "S3"],
  "anomaly_detection_percent": 10,
  "generate_optimization_scripts": true
}
```

Outputs
- Discovery report of idle and under-utilized cloud resources.
- Expenditure anomaly detection and billing analysis.
- One-click cost reduction script generations.
- AWS capital efficiency and budget alignment scorecard.
