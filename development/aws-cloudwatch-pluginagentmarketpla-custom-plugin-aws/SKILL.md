---
name: aws-cloudwatch
description: Implement monitoring, alerting, and observability with CloudWatch
sasmp_version: "1.3.0"
bonded_agent: 08-aws-devops
bond_type: SECONDARY_BOND
---

# AWS CloudWatch Skill

Set up comprehensive monitoring and alerting for AWS resources.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | CloudWatch |
| Complexity | Medium |
| Est. Time | 15-30 min |
| Prerequisites | Resources to monitor |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| namespace | string | Metric namespace | AWS/* or custom |
| metric_name | string | Metric name | Valid metric |
| resource_id | string | Resource identifier | Valid ARN or ID |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| period | int | 300 | Evaluation period (seconds) |
| statistic | string | Average | Average, Sum, Min, Max, p99 |
| threshold | float | varies | Alert threshold |
| evaluation_periods | int | 3 | Consecutive periods |

## Essential Alarms

### EC2 Alarms
```yaml
- name: HighCPU
  metric: CPUUtilization
  threshold: 80
  period: 300
  evaluation_periods: 3

- name: StatusCheckFailed
  metric: StatusCheckFailed
  threshold: 1
  period: 60
  evaluation_periods: 2
```

### ECS Alarms
```yaml
- name: HighCPU
  metric: CPUUtilization
  threshold: 80

- name: HighMemory
  metric: MemoryUtilization
  threshold: 85

- name: RunningTaskCount
  metric: RunningTaskCount
  threshold: 1
  comparison: LessThan
```

### RDS Alarms
```yaml
- name: HighCPU
  metric: CPUUtilization
  threshold: 80

- name: LowFreeStorage
  metric: FreeStorageSpace
  threshold: 10737418240  # 10GB
  comparison: LessThan

- name: HighConnections
  metric: DatabaseConnections
  threshold: 100
```

## Implementation

### Create Alarm
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name prod-ec2-high-cpu \
  --alarm-description "EC2 CPU > 80% for 15 minutes" \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 3 \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:alerts \
  --ok-actions arn:aws:sns:us-east-1:123456789012:alerts \
  --treat-missing-data notBreaching
```

### Dashboard Template
```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "title": "EC2 CPU Utilization",
        "metrics": [
          ["AWS/EC2", "CPUUtilization", "InstanceId", "i-xxx"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1"
      }
    },
    {
      "type": "metric",
      "properties": {
        "title": "ECS Service Memory",
        "metrics": [
          ["AWS/ECS", "MemoryUtilization", "ServiceName", "my-service"]
        ]
      }
    }
  ]
}
```

### Custom Metrics
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# Publish custom metric
cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[
        {
            'MetricName': 'RequestLatency',
            'Dimensions': [
                {'Name': 'Service', 'Value': 'API'},
                {'Name': 'Environment', 'Value': 'prod'}
            ],
            'Value': 150.5,
            'Unit': 'Milliseconds'
        }
    ]
)
```

## Log Insights Queries

### Error Rate
```sql
fields @timestamp, @message
| filter @message like /ERROR/
| stats count() as error_count by bin(5m)
```

### Latency Analysis
```sql
fields @timestamp, latency
| stats avg(latency) as avg_latency,
        pct(latency, 95) as p95_latency,
        pct(latency, 99) as p99_latency
  by bin(1h)
```

### Top Errors
```sql
fields @timestamp, @message
| filter @message like /Exception|Error/
| parse @message /(?<error_type>\w+Exception)/
| stats count() as count by error_type
| sort count desc
| limit 10
```

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| No data | Metric not emitting | Check CloudWatch Agent |
| Alarm stuck | Insufficient data | Check treat_missing_data |
| Dashboard empty | Wrong namespace | Verify metric source |
| High costs | Too many metrics | Use metric filters |

### Debug Checklist
- [ ] CloudWatch Agent installed and running?
- [ ] IAM role allows cloudwatch:PutMetricData?
- [ ] Correct namespace and dimensions?
- [ ] Metric has data in expected period?
- [ ] Alarm threshold reasonable?
- [ ] SNS topic has subscriptions?

## Test Template

```python
def test_cloudwatch_alarm():
    # Arrange
    alarm_name = "test-alarm"

    # Act
    cw.put_metric_alarm(
        AlarmName=alarm_name,
        MetricName='CPUUtilization',
        Namespace='AWS/EC2',
        Statistic='Average',
        Period=300,
        EvaluationPeriods=1,
        Threshold=80,
        ComparisonOperator='GreaterThanThreshold'
    )

    # Assert
    response = cw.describe_alarms(AlarmNames=[alarm_name])
    assert len(response['MetricAlarms']) == 1

    # Cleanup
    cw.delete_alarms(AlarmNames=[alarm_name])
```

## Assets

- `assets/alarm-config.yaml` - Common alarm configurations

## References

- [CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/)
- [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
