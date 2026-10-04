---
name: aws-read-only
description: Read-only AWS resource inspection via CLI
activation_keywords: [aws, ec2, s3, rds, cloudwatch, amazon, cloud, instance]
execution_mode: server
---

# AWS Read Only Skill

Provides read-only AWS operations via AWS CLI:
- List EC2 instances and their status
- List S3 buckets
- List RDS instances
- Check CloudWatch alarms

Use `builtin_aws_readonly` tool with fields:
- `operation`: one of "ec2", "s3", "rds", "alarms", "regions"
- `region`: (optional) AWS region (default: us-east-1)

Note: Requires AWS CLI configured on the server. All operations are read-only.
