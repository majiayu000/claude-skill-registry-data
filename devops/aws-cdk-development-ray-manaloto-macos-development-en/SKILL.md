---
name: aws-cdk-development
description: AWS CDK quick-reference for designing, testing, and deploying stacks (TypeScript/Python) with IaC best practices.
---

# AWS CDK Development (Concise)

Use for: writing/reviewing CDK stacks, synth/deploy flows, IaC architecture decisions.

## Patterns
- Project shape: bin/<app>.ts, lib/<stack>.ts, constructs/; enable versioned pipelines.
- Stacks: keep focused; use constructs for reuse; avoid cross-stack refs when SSM/exports suffice.
- Env-aware: context defaults → SSM/SSO profiles; bootstrap with permissions boundary if required.
- Security: least-priv roles, KMS on data stores, no public S3 unless required; block wildcard principals.

## Testing
- Unit: assert resources/props with CDK assertions.
- Snapshot: synth diff; fail on unintended changes.
- Integration: deploy to ephemeral env; run contract tests; destroy on pass.

## CI/CD
- `cdk synth` → template lint → `cdk diff` → gated `cdk deploy --require-approval never` (only in CI with change control).
- Use pipelines/CodePipeline/GitHub Actions with self-mutation off unless needed.

## Ops
- Tags: costcenter, owner, env, app.
- Observability: enable CloudWatch logs/metrics/alarms by default; structure logs.
- Drift: periodic `cdk diff` vs deployed; consider Config/Drift detection for critical stacks.

## Cleanup
- RemovalPolicy: RETAIN for stateful/prod; DESTROY only for ephemeral/test.

## References
- AWS CDK best practices; CFN guardrails; OTel/OpenLIT for runtime telemetry.
