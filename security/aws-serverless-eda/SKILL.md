---
name: aws-serverless-eda
description: AWS serverless/event-driven playbook for Lambda, API Gateway, EventBridge, SQS/SNS, Step Functions with IaC/observability/security.
---

# AWS Serverless & EDA (Concise)

Use for: designing or operating serverless APIs/EDA on AWS with Lambda + API GW + EventBridge/SQS/SNS + Step Functions.

## Architecture
- Entry: API Gateway HTTP/REST; auth via Cognito/IAM/Lambda authorizers; request validation.
- Compute: Lambda with smallest perms; cold-start reduction (provisioned concurrency for hot paths); keep packages slim; use ARM/Graviton.
- Events: EventBridge for routing/schemas; SQS for buffering/retries; SNS for fanout; DLQs; idempotency keys.
- Orchestration: Step Functions for sagas/timeouts/circuit breakers; prefer service integrations.
- Data: DynamoDB single-table patterns; TTL; GSIs sized; use streams for CDC; S3 for blobs with presigned URLs.

## IaC & release
- Use CDK/Terraform; versioned stages (dev/stage/prod); automated tests + `sam local`/`stepfunctions-local` for critical flows.
- Deploy with canaries/gradual; feature flags; rollback via previous version/alias.

## Observability
- OTel/Embedded metrics: request ids, correlation ids; structured logs to CloudWatch/OTel → OpenLIT; trace across API GW → Lambda → downstream.
- Alarms: 5xx, throttles, DLQ depth, iterator age, latency; synthetic canaries for key APIs.

## Reliability & performance
- Concurrency limits per function; reserved concurrency for noisy neighbors; retries/backoff; idempotent handlers.
- API GW: caching for hot GETs; WAF; proper timeouts; binary/media settings.

## Security
- Least-priv IAM per function; KMS for env vars and data; block public S3; WAF on APIs; secrets in SM/Parameter Store; audit logs on admin actions.

## Cutover checklist
- Run load test on canary; verify DLQ empty; alarms green; trace sample end-to-end; cost check on provisioned concurrency.

## References
- AWS Serverless Lens; Lambda Powertools; EventBridge/SQS/SNS best practices; Step Functions patterns.
