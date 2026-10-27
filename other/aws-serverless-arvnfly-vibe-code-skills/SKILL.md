---
name: aws-serverless
description: "AWS Lambda, API Gateway, DynamoDB single-table design, and EventBridge asynchronous decoupling."
---

# AWS Serverless Architecture Protocol

1. Keep Lambda function bundle sizes minimal (< 15MB) to reduce cold start latency.
2. Use IAM execution roles following the principle of least privilege.
3. Use EventBridge for decoupling microservice domains.
