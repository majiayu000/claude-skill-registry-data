---
name: pulumi-typescript
description: Scaffolds Pulumi TypeScript infrastructure-as-code projects, writes IaC code with proper resource configuration, manages Pulumi ESC environments for centralized secrets and configuration, configures OIDC authentication for cloud providers, and builds multi-language component resources. Use when the user asks to create Pulumi TypeScript projects, write Pulumi infrastructure code, set up ESC environments, configure OIDC for Pulumi, implement infrastructure automation with Node.js/TypeScript, create reusable Pulumi components, or work with stack references. Also use when the user mentions Pulumi with TypeScript, AWS/Azure/GCP infrastructure in TypeScript, or PulumiPlugin.yaml for multi-language components.
---

# Pulumi TypeScript Skill

## Development Workflow

### 1. Project Setup

```bash
# Create new TypeScript project
pulumi new typescript

# Or with a cloud-specific template
pulumi new aws-typescript
pulumi new azure-typescript
pulumi new gcp-typescript
```

**Project structure:**
```
my-project/
├── Pulumi.yaml
├── Pulumi.dev.yaml      # Stack config (use ESC instead)
├── package.json
├── tsconfig.json
└── index.ts
```

### 2. Pulumi ESC Integration

Instead of using `pulumi config set` or stack config files, use Pulumi ESC for centralized secrets and configuration.

**Link ESC environment to stack:**
```bash
# Create ESC environment
pulumi env init myorg/myproject-dev

# Edit environment
pulumi env edit myorg/myproject-dev

# Link to Pulumi stack
pulumi config env add myorg/myproject-dev
```

**ESC environment definition (YAML):**
```yaml
values:
  # Static configuration
  pulumiConfig:
    aws:region: us-west-2
    myapp:instanceType: t3.medium

  # Dynamic OIDC credentials for AWS
  aws:
    login:
      fn::open::aws-login:
        oidc:
          roleArn: arn:aws:iam::123456789:role/pulumi-oidc
          sessionName: pulumi-deploy

  # Pull secrets from AWS Secrets Manager
  secrets:
    fn::open::aws-secrets:
      region: us-west-2
      login: ${aws.login}
      get:
        dbPassword:
          secretId: prod/database/password

  # Expose to environment variables
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
```

### 3. TypeScript Patterns

**Basic resource creation:**
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Get configuration from ESC
const config = new pulumi.Config();
const instanceType = config.require("instanceType");

// Create resources with proper tagging
const bucket = new aws.s3.Bucket("my-bucket", {
    versioning: { enabled: true },
    serverSideEncryptionConfiguration: {
        rule: {
            applyServerSideEncryptionByDefault: {
                sseAlgorithm: "AES256",
            },
        },
    },
    tags: {
        Environment: pulumi.getStack(),
        ManagedBy: "Pulumi",
    },
});

// Export outputs
export const bucketName = bucket.id;
export const bucketArn = bucket.arn;
```

**Component resources for reusability:**
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

interface WebServiceArgs {
    port: pulumi.Input<number>;
    imageUri: pulumi.Input<string>;
}

class WebService extends pulumi.ComponentResource {
    public readonly url: pulumi.Output<string>;

    constructor(name: string, args: WebServiceArgs, opts?: pulumi.ComponentResourceOptions) {
        super("custom:app:WebService", name, {}, opts);

        // Create child resources with { parent: this }
        const lb = new aws.lb.LoadBalancer(`${name}-lb`, {
            loadBalancerType: "application",
            // ... configuration
        }, { parent: this });

        this.url = lb.dnsName;
        this.registerOutputs({ url: this.url });
    }
}
```

**Stack references for cross-stack dependencies:**
```typescript
import * as pulumi from "@pulumi/pulumi";

// Reference outputs from networking stack
const networkingStack = new pulumi.StackReference("myorg/networking/prod");
const vpcId = networkingStack.getOutput("vpcId");
const subnetIds = networkingStack.getOutput("privateSubnetIds");
```

**Working with Outputs:**
```typescript
import * as pulumi from "@pulumi/pulumi";

// Use apply for transformations
const uppercaseName = bucket.id.apply(id => id.toUpperCase());

// Use pulumi.all for multiple outputs
const combined = pulumi.all([bucket.id, bucket.arn]).apply(
    ([id, arn]) => `Bucket ${id} has ARN ${arn}`
);

// Conditional resources
const isProd = pulumi.getStack() === "prod";
const monitoring = isProd ? new aws.cloudwatch.MetricAlarm("alarm", {
    // ... configuration
}) : undefined;
```

### 4. Using ESC with pulumi env run

Run any command with ESC environment variables injected:

```bash
# Run pulumi commands with ESC credentials
pulumi env run myorg/aws-dev -- pulumi up

# Run tests with secrets
pulumi env run myorg/test-env -- npm test

# Open environment and export to shell
pulumi env open myorg/myproject-dev --format shell
```

### 5. Async Patterns

```typescript
// Export async function for top-level await
export = async () => {
    const data = await fetchExternalData();

    const resource = new aws.s3.Bucket("bucket", {
        tags: { data: data.value },
    });

    return {
        bucketName: resource.id,
    };
};
```

### 6. Multi-Language Components

Create components in TypeScript that can be consumed from any Pulumi language (Python, Go, C#, Java, YAML).

**Project structure for multi-language component:**
```
my-component/
├── PulumiPlugin.yaml      # Required for multi-language
├── package.json
├── tsconfig.json
└── index.ts               # Component definition
```

**PulumiPlugin.yaml:**
```yaml
runtime: nodejs
```

**Component with proper Args interface:**
```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Args interface - use Input types for all properties
export interface SecureBucketArgs {
    // Wrap all scalar members in Input types
    bucketName: pulumi.Input<string>;
    enableVersioning?: pulumi.Input<boolean>;
    tags?: pulumi.Input<Record<string, pulumi.Input<string>>>;
}

export class SecureBucket extends pulumi.ComponentResource {
    public readonly bucketId: pulumi.Output<string>;
    public readonly bucketArn: pulumi.Output<string>;

    // Constructor must have 'args' parameter with type annotation
    constructor(name: string, args: SecureBucketArgs, opts?: pulumi.ComponentResourceOptions) {
        super("myorg:storage:SecureBucket", name, {}, opts);

        const bucket = new aws.s3.Bucket(`${name}-bucket`, {
            bucket: args.bucketName,
            versioning: { enabled: args.enableVersioning ?? true },
            serverSideEncryptionConfiguration: {
                rule: {
                    applyServerSideEncryptionByDefault: {
                        sseAlgorithm: "AES256",
                    },
                },
            },
            tags: args.tags,
        }, { parent: this });

        this.bucketId = bucket.id;
        this.bucketArn = bucket.arn;

        this.registerOutputs({
            bucketId: this.bucketId,
            bucketArn: this.bucketArn,
        });
    }
}
```

**Publishing for multi-language consumption:**
```bash
# Consume from git repository
pulumi package add github.com/myorg/my-component

# With version tag
pulumi package add github.com/myorg/my-component@v1.0.0

# Local development
pulumi package add /path/to/local/my-component
```

**Multi-language Args requirements:**
- Use `pulumi.Input<T>` for all scalar properties
- Avoid union types (`string | number`) - not supported
- Avoid functions/callbacks - not serializable
- Constructor must have `args` parameter with type declaration

## Deployment Workflow with Validation

Follow this validated workflow for safe deployments:

### 1. Preview Changes
```bash
pulumi preview
```
Review the output to understand what resources will be created, modified, or deleted.

### 2. Validate Changes
Check the preview output for:
- Unexpected resource deletions or modifications
- Correct number and type of resources
- Proper configuration values (region, instance type, tags, etc.)

If changes look incorrect, investigate the root cause before proceeding:
```bash
# Check current stack state
pulumi stack output

# Review ESC environment values
pulumi env open myorg/myproject-dev

# Verify configuration
pulumi config
```

### 3. Deploy
Once validated, deploy the changes:
```bash
pulumi up
```

### 4. Verify Outputs
After successful deployment, confirm the outputs:
```bash
pulumi stack output
```

Compare outputs against expected values (e.g., bucket names, endpoint URLs, resource IDs).

### Error Recovery

If `pulumi up` fails mid-deployment:
1. Check the error message for the specific resource that failed
2. Review resource configuration and ESC environment values
3. Fix the underlying issue (e.g., IAM permissions, invalid configuration)
4. Run `pulumi up` again — Pulumi will resume from where it left off
5. If the stack is in an inconsistent state, use `pulumi refresh` to sync state with actual cloud resources

## Best Practices

### Security
- Use Pulumi ESC for all secrets - never commit secrets to stack config files
- Enable OIDC authentication instead of static credentials
- Use dynamic secrets with short TTLs when possible
- Apply least-privilege IAM policies
- Always enable server-side encryption on S3 buckets (AES256 or KMS) — this is a non-negotiable default
- Block public access on S3 buckets unless explicitly required
- Enable versioning on storage resources for data protection

### Code Organization
- Use ComponentResources for reusable infrastructure patterns
- Leverage TypeScript's type system for configuration validation
- Keep stack-specific config in ESC environments
- Use stack references for cross-stack dependencies

### Deployment
- Always run `pulumi preview` before `pulumi up`
- Use ESC environment versioning and tags for releases
- Implement proper tagging strategy for all resources

## Common Commands

```bash
# Environment Commands (pulumi env)
pulumi env init <org>/<project>/<env>        # Create environment
pulumi env edit <org>/<env>                  # Edit environment
pulumi env open <org>/<env>                  # View resolved values
pulumi env run <org>/<env> -- <command>      # Run with env vars
pulumi env version tag <org>/<env> <tag>     # Tag version

# Pulumi Commands
pulumi new typescript                  # New project
pulumi config env add <org>/<env>     # Link ESC environment
pulumi preview                         # Preview changes
pulumi up                              # Deploy
pulumi stack output                    # View outputs
pulumi destroy                         # Tear down
pulumi refresh                         # Sync state with cloud
```

## References

- [references/pulumi-esc.md](references/pulumi-esc.md) - ESC patterns and commands
- [references/pulumi-patterns.md](references/pulumi-patterns.md) - Common infrastructure patterns
- [references/pulumi-typescript.md](references/pulumi-typescript.md) - TypeScript-specific guidance
- [references/pulumi-best-practices-aws.md](references/pulumi-best-practices-aws.md) - AWS best practices
- [references/pulumi-best-practices-azure.md](references/pulumi-best-practices-azure.md) - Azure best practices
- [references/pulumi-best-practices-gcp.md](references/pulumi-best-practices-gcp.md) - GCP best practices
