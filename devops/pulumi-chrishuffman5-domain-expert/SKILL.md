---
name: pulumi
description: "Covers Pulumi IaC platform: infrastructure as code using general-purpose languages (TypeScript, Python, Go, C#, Java), Pulumi Cloud, stack management, state backends, and component resources. WHEN: \"Pulumi\", \"pulumi up\", \"pulumi stack\", \"Pulumi Cloud\", \"Pulumi ESC\", \"infrastructure in TypeScript\", \"infrastructure in Python\", \"ComponentResource\", \"pulumi.Output\"."
license: MIT
---

# Pulumi Technology Expert

This skill covers Pulumi across all supported versions (3.x). Pulumi is an infrastructure as code platform that uses general-purpose programming languages instead of DSLs. Current version is 3.x.

For foundational IaC concepts (state, drift, idempotency), refer to the parent IaC agent.

## How to Approach Tasks

1. **Classify** the request:
   - **Troubleshooting** -- Load `references/diagnostics.md`
   - **Architecture** -- Load `references/architecture.md`
   - **Best practices** -- Load `references/best-practices.md`
   - **Language-specific** -- Identify which SDK language (TypeScript, Python, Go, C#, Java) and tailor examples accordingly

2. **Identify language** -- Ask which language the user is working in if not obvious. Pulumi code looks fundamentally different across languages.

3. **Load context** -- Read the relevant reference file.

4. **Recommend** -- Provide code examples in the user's language with explanations.

## Core Architecture

### How Pulumi Works

```
┌──────────────────┐     ┌──────────────────┐
│  Pulumi Program  │     │  Pulumi Engine    │
│  (TypeScript,    │────▶│                  │
│   Python, Go,    │     │  - Resource graph │
│   C#, Java)      │     │  - Diff engine   │
└──────────────────┘     │  - Step generator │
                          └──────┬───────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
             ┌──────▼──────┐ ┌──▼──────┐ ┌───▼─────┐
             │  Provider   │ │Provider │ │Provider │
             │  AWS        │ │ Azure   │ │ K8s     │
             └──────┬──────┘ └────┬────┘ └────┬────┘
                    │            │           │
               Cloud APIs    Cloud APIs   K8s API
```

1. **Program execution** -- Pulumi runs your code (TypeScript, Python, etc.) to declare desired resources
2. **Resource registration** -- Each `new Resource(...)` call registers a resource with the Pulumi engine
3. **Diff** -- Engine compares declared resources against the current state
4. **Deploy** -- Engine calls provider CRUD operations to reconcile

### Language SDKs

| Language | Package | Minimum Version |
|---|---|---|
| TypeScript/JavaScript | `@pulumi/pulumi` | Node.js 18+ |
| Python | `pulumi` | Python 3.9+ |
| Go | `github.com/pulumi/pulumi/sdk/v3` | Go 1.21+ |
| C# | `Pulumi` | .NET 6+ |
| Java | `com.pulumi:pulumi` | Java 11+ |
| YAML | Native | N/A |

### Stacks

A stack is an instance of a Pulumi program with its own configuration and state:

```bash
# Create stacks per environment
pulumi stack init dev
pulumi stack init staging
pulumi stack init production

# Switch stacks
pulumi stack select production

# Stack-specific configuration
pulumi config set aws:region us-east-1
pulumi config set --secret dbPassword SuperSecret123
```

## Key Concepts

### Resources

```typescript
// TypeScript example
import * as aws from "@pulumi/aws";

// Create a resource
const bucket = new aws.s3.Bucket("my-bucket", {
    acl: "private",
    tags: { Environment: "production" },
});

// Export outputs
export const bucketName = bucket.id;
export const bucketArn = bucket.arn;
```

```python
# Python example
import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket("my-bucket",
    acl="private",
    tags={"Environment": "production"},
)

pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
```

### Outputs and Inputs

Pulumi uses `Output<T>` to represent values that are resolved asynchronously (after resource creation):

```typescript
// Outputs are resolved after the resource is created
const bucket = new aws.s3.Bucket("my-bucket");

// Use .apply() to transform outputs
const bucketUrl = bucket.id.apply(id => `https://${id}.s3.amazonaws.com`);

// Use pulumi.interpolate for string interpolation with outputs
const greeting = pulumi.interpolate`Bucket: ${bucket.id}`;

// Chain outputs
const objectKey = bucket.id.apply(id => {
    return new aws.s3.BucketObject(`${id}-index`, {
        bucket: id,
        key: "index.html",
        content: "<h1>Hello</h1>",
    });
});
```

### Component Resources

Reusable abstractions that group multiple resources:

```typescript
class VpcComponent extends pulumi.ComponentResource {
    public readonly vpcId: pulumi.Output<string>;
    public readonly subnetIds: pulumi.Output<string>[];

    constructor(name: string, args: VpcArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:networking:Vpc", name, {}, opts);

        const vpc = new aws.ec2.Vpc(`${name}-vpc`, {
            cidrBlock: args.cidrBlock,
        }, { parent: this });

        this.vpcId = vpc.id;
        // ... create subnets, route tables, etc.

        this.registerOutputs({
            vpcId: this.vpcId,
        });
    }
}

// Use the component
const network = new VpcComponent("prod", {
    cidrBlock: "10.0.0.0/16",
});
```

### Configuration and Secrets

```typescript
const config = new pulumi.Config();

// Plain config
const region = config.require("aws:region");
const instanceCount = config.requireNumber("instanceCount");

// Secret config (encrypted in state)
const dbPassword = config.requireSecret("dbPassword");
```

```bash
# Set configuration
pulumi config set instanceCount 3
pulumi config set --secret dbPassword MySecret123

# Configuration stored in Pulumi.<stack>.yaml
```

## State Management

### Backends

| Backend | Command | Use Case |
|---|---|---|
| **Pulumi Cloud** | Default | Managed state, secrets, RBAC, CI/CD integration |
| **S3** | `pulumi login s3://bucket` | Self-hosted, AWS |
| **Azure Blob** | `pulumi login azblob://container` | Self-hosted, Azure |
| **GCS** | `pulumi login gs://bucket` | Self-hosted, GCP |
| **Local** | `pulumi login --local` | Development only |

### State Operations

```bash
# Export state
pulumi stack export > state.json

# Import state (after manual editing)
pulumi stack import < state.json

# Refresh (detect drift)
pulumi refresh

# Delete a resource from state without destroying
pulumi state delete <urn>

# Unprotect a resource (remove deletion protection)
pulumi state unprotect <urn>
```

## CLI Reference

```bash
# Core workflow
pulumi new aws-typescript     # Create new project from template
pulumi up                     # Preview and deploy
pulumi preview                # Preview only (no changes)
pulumi destroy                # Destroy all resources
pulumi refresh                # Detect drift

# Stack management
pulumi stack ls                # List stacks
pulumi stack select <name>     # Switch stacks
pulumi stack output            # Show stack outputs
pulumi stack rm <name>         # Delete stack

# Configuration
pulumi config set <key> <value>
pulumi config set --secret <key> <value>
pulumi config get <key>

# Import existing resources
pulumi import aws:s3/bucket:Bucket my-bucket my-existing-bucket-name
```

## Reference Files

- `references/architecture.md` — Engine internals, provider system, resource lifecycle, Output/Input model, deployment engine, Pulumi Cloud architecture
- `references/best-practices.md` — Project organization, component design, testing, CI/CD integration, secret management, multi-stack patterns
- `references/diagnostics.md` — Common errors (Output resolution, provider auth, state conflicts), debugging techniques, migration from Terraform
