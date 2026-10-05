---
name: aws-cdk
description: Use when defining AWS infrastructure with the CDK. Covers construct design, stack organization, environment configuration, testing infrastructure code, and safe deployment.
metadata:
  category: devops
  version: 1.0.0
  tags: [aws, cdk, iac, typescript, cloudformation]
---

# AWS CDK

## Purpose

Define AWS infrastructure in a real programming language without losing the reviewability of a plan. The CDK's power — abstraction, loops, conditionals — is also its risk: a small code change can generate a large and destructive CloudFormation diff.

## When to Use

- Defining AWS infrastructure with the CDK.
- Structuring stacks and reusable constructs.
- Testing infrastructure code.
- Reviewing a CDK deployment before it runs.

## Capabilities

- Construct levels: L1 (raw CloudFormation), L2 (curated), L3 (patterns).
- Stack organization and cross-stack references.
- Environment and account configuration.
- Snapshot and fine-grained assertion testing.
- `cdk diff` review and safe deployment.

## Inputs

- The infrastructure to define, and the environments it targets.
- Existing resources, if adopting or importing.
- Deployment permissions and boundaries.

## Outputs

- Stacks organized by lifecycle, not by service type.
- Reusable constructs with a narrow, typed interface.
- Snapshot tests that make an unintended diff fail the build.

## Workflow

1. **Organize stacks by lifecycle** — Things that change together belong together. A stack containing both the VPC (changes yearly) and the application (changes daily) makes every deploy risk the network.
2. **Prefer L2 constructs** — They apply sensible defaults, including encryption and least-privilege IAM. Drop to L1 only for properties L2 does not expose.
3. **Build L3 patterns for repeated shapes** — A `MonitoredLambda` construct that always adds an alarm, a log group with retention, and a dead-letter queue removes an entire category of oversight.
4. **Test the synthesized template** — Snapshot tests catch unintended diffs; fine-grained assertions verify specific properties (encryption on, public access off).
5. **Read `cdk diff` before every deploy** — It shows resource replacements. A replaced RDS instance is a new, empty RDS instance.
6. **Deploy through a pipeline** — Not from a laptop with admin credentials.

## Best Practices

- `cdk deploy` from a developer machine with admin access is how production gets changed by accident. Deploy through CI, with a scoped role.
- Never use `removalPolicy: DESTROY` on a stateful resource in production. The default (`RETAIN` for most data stores) exists for a reason.
- Logical ID changes cause resource replacement. Renaming a construct — an innocuous-looking refactor — will destroy and recreate the resource it names.
- Grant permissions with `.grantRead(fn)`, not by hand-writing a policy. The L2 grant methods produce a correctly scoped policy that a hand-written one usually does not.
- Do not use context lookups (`Vpc.fromLookup`) in a construct that must synthesize in CI without AWS credentials. Pass the values in.
- Pin the CDK version. Construct defaults change between minor versions, and a default change is a template change.

## Examples

**An L3 construct that makes the right thing the default:**

```typescript
export interface MonitoredFunctionProps extends NodejsFunctionProps {
  readonly alarmTopic: ITopic;
}

/** A Lambda that cannot be deployed without an alarm, a DLQ, and log retention. */
export class MonitoredFunction extends Construct {
  public readonly fn: NodejsFunction;

  constructor(scope: Construct, id: string, props: MonitoredFunctionProps) {
    super(scope, id);

    const dlq = new Queue(this, "Dlq", { retentionPeriod: Duration.days(14) });

    this.fn = new NodejsFunction(this, "Fn", {
      runtime: Runtime.NODEJS_22_X,
      architecture: Architecture.ARM_64,        // cheaper and faster
      logRetention: RetentionDays.ONE_MONTH,    // otherwise logs are kept forever, billed forever
      deadLetterQueue: dlq,
      tracing: Tracing.ACTIVE,
      ...props,
    });

    this.fn.metricErrors({ period: Duration.minutes(5) })
      .createAlarm(this, "ErrorAlarm", {
        threshold: 1,
        evaluationPeriods: 2,
        treatMissingData: TreatMissingData.NOT_BREACHING,
      })
      .addAlarmAction(new SnsAction(props.alarmTopic));
  }
}
```

**Assertions that fail the build on a security regression:**

```typescript
test("uploads bucket is encrypted and blocks public access", () => {
  const template = Template.fromStack(new StorageStack(new App(), "Test"));

  template.hasResourceProperties("AWS::S3::Bucket", {
    BucketEncryption: Match.objectLike({
      ServerSideEncryptionConfiguration: Match.anyValue(),
    }),
    PublicAccessBlockConfiguration: {
      BlockPublicAcls: true,
      BlockPublicPolicy: true,
      IgnorePublicAcls: true,
      RestrictPublicBuckets: true,
    },
  });
});
```

## Notes

- Snapshot tests (`expect(Template.fromStack(stack)).toMatchSnapshot()`) are the cheapest protection against an unintended template change. Any diff becomes a deliberate decision to update the snapshot.
- `cdk diff` output containing "requires replacement" on a database, an EIP, or anything with a name is the moment to stop and think. The CDK will happily execute it.
- Renaming a construct ID changes the logical ID and therefore replaces the resource. If a rename is needed on a stateful resource, override the logical ID to keep it stable.
