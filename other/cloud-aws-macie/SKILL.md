---
name: cloud-aws-macie
description: "Cloud Aws Macie."
domain: cybersecurity
---

|
| **PII** | SSN, passport numbers, driver's license, date of birth, names, addresses |
| **Financial** | Credit card numbers, bank account numbers, SWIFT codes |
| **Credentials** | AWS secret keys, API keys, SSH private keys, OAuth tokens |
| **Health** | HIPAA identifiers, health insurance claim numbers |
| **Legal** | Tax identification numbers, national ID numbers |

## Findings Management

### List findings

```bash
# Get sensitive data findings
aws macie2 list-findings \
  --finding-criteria '{
    "criterion": {
      "severity.description": {
        "eq": ["High"]
      },
      "category": {
        "eq": ["CLASSIFICATION"]
      }
    }
  }' \
  --sort-criteria '{"attributeName": "updatedAt", "orderBy": "DESC"}' \
  --max-results 25
```

### Get finding details

```bash
aws macie2 get-findings \
  --finding-ids '["finding-id-1", "finding-id-2"]'
```

### Export findings to Security Hub

```bash
# Macie automatically publishes findings to Security Hub
# Verify integration:
aws macie2 get-macie-session --query 'findingPublishingFrequency'
```

## EventBridge Integration for Automated Response

```json
{
  "source": ["aws.macie"],
  "detail-type": ["Macie Finding"],
  "detail": {
    "severity": {
      "description": ["High", "Critical"]
    }
  }
}
```

### Lambda function for automated remediation

```python
import boto3
import json

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    finding = event['detail']
    severity = finding['severity']['description']
    bucket = finding['resourcesAffected']['s3Bucket']['name']
    key = finding['resourcesAffected']['s3Object']['key']
    sensitive_types = [d['type'] for d in finding.get('classificationDetails', {}).get('result', {}).get('sensitiveData', [])]

    if severity in ['High', 'Critical']:
        # Tag the object for review
        s3.put_object_tagging(
            Bucket=bucket,
            Key=key,
            Tagging={
                'TagSet': [
                    {'Key': 'macie-finding', 'Value': severity},
                    {'Key': 'sensitive-data', 'Value': ','.join(sensitive_types)},
                    {'Key': 'requires-review', 'Value': 'true'}
                ]
            }
        )

        # Notify security team
        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:123456789012:security-alerts',
            Subject=f'Macie {severity} Finding: {bucket}/{key}',
            Message=json.dumps({
                'bucket': bucket,
                'key': key,
                'severity': severity,
                'sensitive_data_types': sensitive_types,
                'finding_id': finding['id']
            }, indent=2)
        )

    return {'statusCode': 200}
```

## Multi-Account Deployment

### Designate Macie administrator account

```bash
# From the management account
aws macie2 enable-organization-admin-account \
  --admin-account-id 111111111111
```

### Add member accounts

```bash
# From the administrator account
aws macie2 create-member \
  --account '{"accountId": "222222222222", "email": "security@example.com"}'
```

## Monitoring Macie Operations

### Usage statistics

```bash
aws macie2 get-usage-statistics \
  --filter-by '[{"comparator": "GT", "key": "accountId", "values": []}]' \
  --sort-by '{"key": "accountId", "orderBy": "ASC"}'
```

### Classification job status

```bash
aws macie2 list-classification-jobs \
  --filter-criteria '{"includes": [{"comparator": "EQ", "key": "jobStatus", "values": ["RUNNING"]}]}'
```

## References

- AWS Macie Documentation: https://docs.aws.amazon.com/macie/
- AWS Macie Pricing
- Supported File Types for Macie Analysis
- GDPR and CCPA Compliance with Macie
