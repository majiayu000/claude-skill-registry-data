---
license: Apache-2.0
name: aws-cdk-builder
description: "AWS CDK infrastructure builder using TypeScript with L2/L3 constructs and Well-Architected patterns. Activate on: AWS CDK, CDK construct, CDK stack, CDK pipeline, AWS infrastructure as code TypeScript, L2 construct, CDK patterns. NOT for: Terraform IaC (use terraform-module-builder), Kubernetes manifests (use kubernetes-manifest-generator), serverless framework (use devops-automator)."
allowed-tools: Read,Write,Edit,Bash(docker:*,kubectl:*,terraform:*,npm:*,npx:*)
category: DevOps & Infrastructure
tags:
  - aws
  - cdk
  - iac
  - typescript
pairs-with:
  - skill: terraform-iac-expert
    reason: Alternative IaC approach for multi-cloud; CDK is AWS-native
  - skill: terraform-module-builder
    reason: Terraform modules solve the same reusability problem CDK constructs solve
---

# AWS CDK Builder

Expert in building AWS infrastructure using CDK with TypeScript, leveraging L2/L3 constructs and Well-Architected Framework patterns.

## Activation Triggers

**Activate on:** "AWS CDK", "CDK construct", "CDK stack", "CDK pipeline", "AWS IaC TypeScript", "L2 construct", "CDK patterns", "cdk deploy", "cdk synth"

**NOT for:** Terraform IaC → `terraform-module-builder` | Kubernetes manifests → `kubernetes-manifest-generator` | Serverless Framework → `devops-automator`

## Quick Start

1. **Initialize CDK app** — `npx cdk init app --language typescript`
2. **Design stack structure** — separate stateful (databases, buckets) from stateless (compute, APIs)
3. **Use L2 constructs** — prefer high-level constructs over L1 CloudFormation resources
4. **Add CDK Nag** — automated Well-Architected compliance checking
5. **Deploy with CDK Pipelines** — self-mutating CI/CD pipeline

## Core Capabilities

| Domain | Technologies |
|--------|-------------|
| **CDK Core** | CDK 2.180+, Constructs library, CDK CLI, cdk.json |
| **L2/L3 Constructs** | aws-lambda, aws-apigateway, aws-ecs-patterns, aws-rds |
| **Compliance** | cdk-nag (AwsSolutions, NIST, HIPAA, PCI packs) |
| **CI/CD** | CDK Pipelines, CodePipeline, CodeBuild, self-mutation |
| **Patterns** | ECS Fargate patterns, API Gateway + Lambda, S3 + CloudFront |

## Architecture Patterns

### Stack Organization (Stateful vs Stateless)

```typescript
// bin/app.ts — top-level app with environment separation
const app = new cdk.App();

// Stateful stack — rarely changes, careful with updates
const dataStack = new DataStack(app, 'Data-Prod', {
  env: { account: '123456789', region: 'us-east-1' },
});

// Stateless stack — frequently deployed, safe to destroy/recreate
const apiStack = new ApiStack(app, 'Api-Prod', {
  env: { account: '123456789', region: 'us-east-1' },
  database: dataStack.database,
  bucket: dataStack.bucket,
});

// Pipeline stack — self-mutating CI/CD
new PipelineStack(app, 'Pipeline', {
  env: { account: '123456789', region: 'us-east-1' },
});
```

### L2 Construct with Best Practices

```typescript
// lib/api-stack.ts
export class ApiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ApiStackProps) {
    super(scope, id, props);

    const handler = new lambda.Function(this, 'Handler', {
      runtime: lambda.Runtime.NODEJS_22_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda/'),
      memorySize: 256,
      timeout: cdk.Duration.seconds(30),
      tracing: lambda.Tracing.ACTIVE,       // X-Ray
      insightsVersion: lambda.LambdaInsightsVersion.VERSION_1_0_229_0,
      environment: {
        TABLE_NAME: props.table.tableName,
        POWERTOOLS_SERVICE_NAME: 'api',     // Lambda Powertools
      },
    });

    props.table.grantReadWriteData(handler); // Least privilege

    const api = new apigw.RestApi(this, 'Api', {
      deployOptions: {
        tracingEnabled: true,
        metricsEnabled: true,
        throttlingRateLimit: 1000,
        throttlingBurstLimit: 500,
      },
    });

    api.root.addResource('items').addMethod('GET',
      new apigw.LambdaIntegration(handler));
  }
}
```

### CDK Pipelines (Self-Mutating)

```
Source (GitHub) → Synth (cdk synth) → Self-Mutate
    │                                      │
    ▼                                      ▼
UpdatePipeline ─── Deploy Staging ─── Manual Approval ─── Deploy Prod
                        │                                      │
                    Integration Tests                    Smoke Tests
```

## Anti-Patterns

1. **L1 constructs everywhere** — using `CfnBucket` instead of `s3.Bucket`. L2 constructs encode best practices (encryption, logging, access control) by default.
2. **Monolithic stacks** — one stack with 200+ resources hits CloudFormation limits and deploys slowly. Split into stateful/stateless stacks with cross-stack references.
3. **Missing cdk-nag** — deploying without compliance checks. Add `Aspects.of(app).add(new AwsSolutionsChecks())` to catch security issues pre-deploy.
4. **Hardcoded account/region** — `account: '123456789'` in construct code. Use `cdk.json` context or `cdk.Environment` lookup for portability.
5. **No snapshot tests** — CDK generates CloudFormation templates that change unexpectedly. Add `expect(template).toMatchSnapshot()` tests to detect unintended changes.

## Quality Checklist

```
[ ] Stacks separated: stateful (data) vs stateless (compute)
[ ] L2/L3 constructs used (not raw CloudFormation L1)
[ ] cdk-nag enabled with AwsSolutions pack
[ ] Snapshot tests for all stacks
[ ] CDK Pipelines for self-mutating CI/CD
[ ] Least privilege IAM via grant methods (grantRead, grantWrite)
[ ] cdk synth produces valid CloudFormation
[ ] Cross-stack references use exported outputs
[ ] Removal policies set (RETAIN for production data, DESTROY for dev)
[ ] Tags applied via Aspects for cost allocation
[ ] cdk diff reviewed before every deployment
[ ] Lambda functions use Powertools for observability
```
