---
name: pulumi-go
description: Creates Pulumi infrastructure-as-code projects in Go, configures OIDC authentication, integrates with Pulumi ESC for centralized secrets and configuration management, and builds multi-language component resources. Use when setting up Pulumi Go projects, writing infrastructure code with Go, configuring OIDC for Pulumi, using Pulumi ESC with Go, automating cloud infrastructure with Golang, creating reusable Pulumi components in Go, or working with pulumi-go-provider. Also use when the user mentions Pulumi with Go/Golang, AWS/Azure/GCP infrastructure in Go, or Go-based ComponentResource patterns.
---

# Pulumi Go Skill

## Development Workflow

### 1. Project Setup

```bash
# Create new Go project
pulumi new go

# Or with a cloud-specific template
pulumi new aws-go
pulumi new azure-go
pulumi new gcp-go
```

### 2. Pulumi ESC Integration

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

### 3. Go Patterns

**Basic resource creation:**
```go
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Get configuration from ESC
        cfg := config.New(ctx, "")
        instanceType := cfg.Require("instanceType")

        // Create resources with proper tagging
        bucket, err := s3.NewBucket(ctx, "my-bucket", &s3.BucketArgs{
            Versioning: &s3.BucketVersioningArgs{
                Enabled: pulumi.Bool(true),
            },
            ServerSideEncryptionConfiguration: &s3.BucketServerSideEncryptionConfigurationArgs{
                Rule: &s3.BucketServerSideEncryptionConfigurationRuleArgs{
                    ApplyServerSideEncryptionByDefault: &s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs{
                        SseAlgorithm: pulumi.String("AES256"),
                    },
                },
            },
            Tags: pulumi.StringMap{
                "Environment": pulumi.String(ctx.Stack()),
                "ManagedBy":   pulumi.String("Pulumi"),
            },
        })
        if err != nil {
            return err
        }

        // Export outputs
        ctx.Export("bucketName", bucket.ID())
        ctx.Export("bucketArn", bucket.Arn)

        return nil
    })
}
```

**Component resources:**
```go
package main

import (
    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/lb"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

type WebServiceArgs struct {
    Port     pulumi.IntInput
    ImageUri pulumi.StringInput
}

type WebService struct {
    pulumi.ResourceState

    URL pulumi.StringOutput `pulumi:"url"`
}

func NewWebService(ctx *pulumi.Context, name string, args *WebServiceArgs, opts ...pulumi.ResourceOption) (*WebService, error) {
    component := &WebService{}
    err := ctx.RegisterComponentResource("custom:app:WebService", name, component, opts...)
    if err != nil {
        return nil, err
    }

    // Create child resources with pulumi.Parent(component)
    loadBalancer, err := lb.NewLoadBalancer(ctx, name+"-lb", &lb.LoadBalancerArgs{
        LoadBalancerType: pulumi.String("application"),
        // ... configuration
    }, pulumi.Parent(component))
    if err != nil {
        return nil, err
    }

    component.URL = loadBalancer.DnsName

    ctx.RegisterResourceOutputs(component, pulumi.Map{
        "url": component.URL,
    })

    return component, nil
}
```

**Stack references for cross-stack dependencies:**
```go
package main

import (
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Reference outputs from networking stack
        networkingStack, err := pulumi.NewStackReference(ctx, "myorg/networking/prod", nil)
        if err != nil {
            return err
        }

        vpcId := networkingStack.GetStringOutput(pulumi.String("vpcId"))
        subnetIds := networkingStack.GetOutput(pulumi.String("privateSubnetIds"))

        ctx.Export("vpcId", vpcId)

        return nil
    })
}
```

**Working with Outputs:**
```go
package main

import (
    "fmt"
    "strings"

    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        // Apply transformation
        uppercaseName := bucket.ID().ApplyT(func(id string) string {
            return strings.ToUpper(id)
        }).(pulumi.StringOutput)

        // Combine multiple outputs
        combined := pulumi.All(bucket.ID(), bucket.Arn).ApplyT(
            func(args []interface{}) string {
                id := args[0].(string)
                arn := args[1].(string)
                return fmt.Sprintf("Bucket %s has ARN %s", id, arn)
            },
        ).(pulumi.StringOutput)

        // Conditional resources
        if ctx.Stack() == "prod" {
            _, err := cloudwatch.NewMetricAlarm(ctx, "alarm", &cloudwatch.MetricAlarmArgs{
                // ... configuration
            })
            if err != nil {
                return err
            }
        }

        return nil
    })
}
```

### 4. Using ESC with pulumi env run

```bash
# Run pulumi commands with ESC credentials
pulumi env run myorg/aws-dev -- pulumi up

# Run tests with secrets
pulumi env run myorg/test-env -- go test ./...

# Open environment and export to shell
pulumi env open myorg/myproject-dev --format shell
```

### 5. Deployment Workflow with Validation

**Build and preview:**
```bash
# Build Go binary first
go build -o $(basename $(pwd))

# Preview changes
pulumi preview
```

**Validation checkpoint:** Review the preview output. If changes are unexpected:
- Check ESC environment values: `pulumi env open myorg/myproject-dev`
- Verify stack config: `pulumi config`
- Inspect resource diffs carefully before proceeding

**Deploy:**
```bash
# Deploy after validation
pulumi up

# Verify outputs
pulumi stack output
```

**Error recovery:** If deployment fails:
1. Check error logs for resource-specific issues
2. Verify credentials and permissions: `pulumi env open myorg/myproject-dev --format shell`
3. Attempt rollback if needed: `pulumi refresh` (updates state without changes)
4. Fix the issue and retry: `pulumi up`

For destructive changes (deletions), Pulumi will prompt for confirmation during `pulumi up`.

### 6. Error Handling

```go
func main() {
    pulumi.Run(func(ctx *pulumi.Context) error {
        bucket, err := s3.NewBucket(ctx, "bucket", &s3.BucketArgs{})
        if err != nil {
            return fmt.Errorf("failed to create bucket: %w", err)
        }

        policy, err := s3.NewBucketPolicy(ctx, "policy", &s3.BucketPolicyArgs{
            Bucket: bucket.ID(),
            Policy: bucket.Arn.ApplyT(func(arn string) string {
                return fmt.Sprintf(`{"Version":"2012-10-17",...}`, arn)
            }).(pulumi.StringOutput),
        })
        if err != nil {
            return fmt.Errorf("failed to create bucket policy: %w", err)
        }

        return nil
    })
}
```

### 7. Multi-Language Components

Create reusable components in Go for consumption from any Pulumi language.

**Project structure:**
```
my-component/
├── PulumiPlugin.yaml
├── go.mod
├── go.sum
└── main.go
```

**PulumiPlugin.yaml:**
```yaml
runtime: go
```

**Component implementation:**
```go
package main

import (
    "context"
    "log"

    "github.com/pulumi/pulumi-aws/sdk/v6/go/aws/s3"
    "github.com/pulumi/pulumi-go-provider/infer"
    "github.com/pulumi/pulumi/sdk/v3/go/pulumi"
)

// Use Input types for all properties
type SecureBucketArgs struct {
    BucketName       pulumi.StringInput `pulumi:"bucketName"`
    EnableVersioning pulumi.BoolInput   `pulumi:"enableVersioning,optional"`
    Tags             pulumi.StringMapInput `pulumi:"tags,optional"`
}

type SecureBucket struct {
    pulumi.ResourceState

    BucketId  pulumi.StringOutput `pulumi:"bucketId"`
    BucketArn pulumi.StringOutput `pulumi:"bucketArn"`
}

func NewSecureBucket(ctx *pulumi.Context, name string, args *SecureBucketArgs, opts ...pulumi.ResourceOption) (*SecureBucket, error) {
    component := &SecureBucket{}
    err := ctx.RegisterComponentResource("myorg:storage:SecureBucket", name, component, opts...)
    if err != nil {
        return nil, err
    }

    bucket, err := s3.NewBucket(ctx, name+"-bucket", &s3.BucketArgs{
        Bucket: args.BucketName,
        Versioning: &s3.BucketVersioningArgs{
            Enabled: args.EnableVersioning,
        },
        ServerSideEncryptionConfiguration: &s3.BucketServerSideEncryptionConfigurationArgs{
            Rule: &s3.BucketServerSideEncryptionConfigurationRuleArgs{
                ApplyServerSideEncryptionByDefault: &s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs{
                    SseAlgorithm: pulumi.String("AES256"),
                },
            },
        },
        Tags: args.Tags,
    }, pulumi.Parent(component))
    if err != nil {
        return nil, err
    }

    component.BucketId = bucket.ID().ToStringOutput()
    component.BucketArn = bucket.Arn

    ctx.RegisterResourceOutputs(component, pulumi.Map{
        "bucketId":  component.BucketId,
        "bucketArn": component.BucketArn,
    })

    return component, nil
}

func main() {
    prov, err := infer.NewProviderBuilder().
        WithNamespace("myorg").
        WithComponents(
            infer.ComponentF(NewSecureBucket),
        ).
        Build()
    if err != nil {
        log.Fatal(err.Error())
    }
    _ = prov.Run(context.Background(), "go-components", "v0.0.1")
}
```

**Publishing:**
```bash
# Consume from git repository
pulumi package add github.com/myorg/my-component

# With version tag
pulumi package add github.com/myorg/my-component@v1.0.0

# Local development
pulumi package add /path/to/local/my-component
```

## Best Practices

### Security
- Use Pulumi ESC for all secrets — never commit secrets to stack config files
- Enable OIDC authentication instead of static credentials
- Use dynamic secrets with short TTLs when possible
- Apply least-privilege IAM policies

### Code Organization
- Use Component Resources for reusable infrastructure patterns
- Leverage Go's type system for configuration validation
- Keep stack-specific config in ESC environments
- Use stack references for cross-stack dependencies

### Deployment
- Always run `pulumi preview` before `pulumi up` and review changes carefully
- Use ESC environment versioning and tags for releases
- Implement proper tagging strategy for all resources
- Build your Go program before running Pulumi: `go build -o $(basename $(pwd))`

## Common Commands

```bash
# Environment Commands (pulumi env)
pulumi env init <org>/<project>/<env>        # Create environment
pulumi env edit <org>/<env>                  # Edit environment
pulumi env open <org>/<env>                  # View resolved values
pulumi env run <org>/<env> -- <command>      # Run with env vars
pulumi env version tag <org>/<env> <tag>     # Tag version

# Pulumi Commands
pulumi new go                          # New project
pulumi config env add <org>/<env>     # Link ESC environment
go build -o $(basename $(pwd))         # Build Go binary
pulumi preview                         # Preview changes
pulumi up                              # Deploy
pulumi stack output                    # View outputs
pulumi destroy                         # Tear down
```

## References

- [references/pulumi-esc.md](references/pulumi-esc.md) - ESC patterns and commands
- [references/pulumi-patterns.md](references/pulumi-patterns.md) - Common infrastructure patterns
- [references/pulumi-go.md](references/pulumi-go.md) - Go-specific guidance
- [references/pulumi-best-practices-aws.md](references/pulumi-best-practices-aws.md) - AWS best practices
- [references/pulumi-best-practices-azure.md](references/pulumi-best-practices-azure.md) - Azure best practices
- [references/pulumi-best-practices-gcp.md](references/pulumi-best-practices-gcp.md) - GCP best practices
