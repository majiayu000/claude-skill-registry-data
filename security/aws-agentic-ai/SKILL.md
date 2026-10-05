---
name: aws-agentic-ai
description: Concise AWS Bedrock AgentCore guide for deploying/operating Gateway, Runtime, Memory, Identity, MCP targets, and credentials.
---

# AWS Agentic AI (Bedrock AgentCore)

Use for: designing/running Bedrock AgentCore (Gateway/Runtime/Memory/Identity) and wiring MCP targets securely.

## Quickstart
- Identity: pick auth (Cognito/AuthN) + scope policies; store secrets in SM/KMS.
- Gateway: define tools + schemas; version APIs; enforce tracing + structured logs.
- Runtime: choose model, latency/SLA budgets; enable streaming; set guardrails/content filters.
- Memory: pick store (Vector/Redis/Dynamo) with TTL + encryption; segment per tenant; purge policies.
- MCP targets: least-priv IAM, scoped tokens, audit calls; test with staging keys first.

## Ops & observability
- Enable OTel (traces + metrics); ship to OpenLIT/SkyPilot backend; alerts on latency, 5xx, token surge.
- Canary flows per release; SLOs for p95 latency, failure rate, cost per request.

## Security
- KMS everywhere; SM for creds; rotate; no plaintext in logs.
- IAM least privilege; deny *:Update on prod agents except pipeline roles; break-glass separate.

## Release checklist
- Contract tests for tools; schema validation; red-team for prompt/PII leakage.
- Rollouts: staged + canary users; feature flags for tool enablement; rollback plan.

## References
- Bedrock AgentCore docs (Gateway, Runtime, Memory, Identity)
- AWS IAM & KMS best practices
- OTel + OpenLIT export patterns
