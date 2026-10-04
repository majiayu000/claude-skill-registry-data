---
name: pulumi-python
description: Creates Pulumi infrastructure-as-code projects in Python, defines cloud resources (AWS, Azure, GCP), configures ESC environments for secrets management, sets up OIDC authentication for secure deployments, and builds multi-language component resources. Use when creating Pulumi Python projects, writing infrastructure code, configuring cloud providers, managing secrets with Pulumi ESC, setting up OIDC for Pulumi, automating infrastructure deployments with Python, creating reusable Pulumi components in Python, or configuring Python toolchains (pip, poetry, uv) for Pulumi. Also use when the user mentions pyproject.toml with Pulumi, component_provider_host, or Python virtual environments for infrastructure code.
---

# Pulumi Python Skill

## Development Workflow

### 1. Project Setup

```bash
# Create new Python project
pulumi new python

# Or with a cloud-specific template
pulumi new aws-python
pulumi new azure-python
pulumi new gcp-python
```

**Project structure:**
```
my-project/
├── Pulumi.yaml
├── __main__.py
├── requirements.txt     # or pyproject.toml
└── venv/                # Virtual environment
```

### 2. Pulumi ESC Integration

Use Pulumi ESC for centralized secrets and configuration instead of stack config files.

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

**Validate ESC environment:**
```bash
# View resolved values (verify no errors)
pulumi env open myorg/myproject-dev

# Check for missing required values
pulumi env open myorg/myproject-dev --format json | jq .
```

### 3. Python Patterns

**Basic resource creation:**
```python
import pulumi
import pulumi_aws as aws

# Get configuration from ESC
config = pulumi.Config()
instance_type = config.require("instanceType")

# Create resources with proper tagging
bucket = aws.s3.Bucket(
    "my-bucket",
    versioning=aws.s3.BucketVersioningArgs(
        enabled=True,
    ),
    server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
        rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
            apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                sse_algorithm="AES256",
            ),
        ),
    ),
    tags={
        "Environment": pulumi.get_stack(),
        "ManagedBy": "Pulumi",
    },
)

# Export outputs
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
```

**Using dictionary literals (concise alternative):**
```python
import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket(
    "my-bucket",
    versioning={"enabled": True},
    server_side_encryption_configuration={
        "rule": {
            "apply_server_side_encryption_by_default": {
                "sse_algorithm": "AES256",
            },
        },
    },
    tags={
        "Environment": pulumi.get_stack(),
        "ManagedBy": "Pulumi",
    },
)
```

**Component resources for reusability:**
```python
import pulumi
from pulumi_aws import lb


class WebServiceArgs:
    def __init__(self, port: pulumi.Input[int], image_uri: pulumi.Input[str]):
        self.port = port
        self.image_uri = image_uri


class WebService(pulumi.ComponentResource):
    url: pulumi.Output[str]

    def __init__(self, name: str, args: WebServiceArgs, opts: pulumi.ResourceOptions = None):
        super().__init__("custom:app:WebService", name, {}, opts)

        # Create child resources with parent=self
        load_balancer = lb.LoadBalancer(
            f"{name}-lb",
            load_balancer_type="application",
            # ... configuration
            opts=pulumi.ResourceOptions(parent=self),
        )

        self.url = load_balancer.dns_name

        self.register_outputs({
            "url": self.url,
        })
```

**Stack references for cross-stack dependencies:**
```python
import pulumi

# Reference outputs from networking stack
networking_stack = pulumi.StackReference("myorg/networking/prod")
vpc_id = networking_stack.get_output("vpc_id")
subnet_ids = networking_stack.get_output("private_subnet_ids")
```

**Working with Outputs:**
```python
import pulumi

# Apply transformation
uppercase_name = bucket.id.apply(lambda id: id.upper())

# Combine multiple outputs
combined = pulumi.Output.all(bucket.id, bucket.arn).apply(
    lambda args: f"Bucket {args[0]} has ARN {args[1]}"
)

# Using Output.concat for string interpolation
message = pulumi.Output.concat("Bucket ARN: ", bucket.arn)

# Conditional resources
is_prod = pulumi.get_stack() == "prod"
if is_prod:
    alarm = aws.cloudwatch.MetricAlarm(
        "alarm",
        # ... configuration
    )
```

### 4. Using ESC with pulumi env run

Run any command with ESC environment variables injected:

```bash
# Run pulumi commands with ESC credentials
pulumi env run myorg/aws-dev -- pulumi up

# Run tests with secrets
pulumi env run myorg/test-env -- pytest

# Open environment and export to shell
pulumi env open myorg/myproject-dev --format shell
```

### 5. Multi-Language Components

Create components in Python that can be consumed from any Pulumi language (TypeScript, Go, C#, Java, YAML).

**Project structure for multi-language component:**
```
my-component/
├── PulumiPlugin.yaml      # Required for multi-language
├── pyproject.toml         # or requirements.txt
└── __main__.py            # Component + entry point
```

**PulumiPlugin.yaml:**
```yaml
runtime: python
```

**Component with proper Args class (__main__.py):**
```python
from typing import Optional
import pulumi
from pulumi import Input, Output, ResourceOptions
from pulumi.provider.experimental import component_provider_host
import pulumi_aws as aws


class SecureBucketArgs:
    """Args class - use Input types for all properties."""

    def __init__(
        self,
        bucket_name: Input[str],
        enable_versioning: Optional[Input[bool]] = None,
        tags: Optional[Input[dict]] = None,
    ):
        self.bucket_name = bucket_name
        self.enable_versioning = enable_versioning or True
        self.tags = tags


class SecureBucket(pulumi.ComponentResource):
    """A secure S3 bucket with encryption and versioning."""

    bucket_id: Output[str]
    bucket_arn: Output[str]

    # Constructor must have 'args' parameter with type annotation
    def __init__(
        self,
        name: str,
        args: SecureBucketArgs,
        opts: Optional[ResourceOptions] = None,
    ):
        super().__init__("myorg:storage:SecureBucket", name, {}, opts)

        bucket = aws.s3.Bucket(
            f"{name}-bucket",
            bucket=args.bucket_name,
            versioning={"enabled": args.enable_versioning},
            server_side_encryption_configuration={
                "rule": {
                    "apply_server_side_encryption_by_default": {
                        "sse_algorithm": "AES256",
                    },
                },
            },
            tags=args.tags,
            opts=ResourceOptions(parent=self),
        )

        self.bucket_id = bucket.id
        self.bucket_arn = bucket.arn

        self.register_outputs({
            "bucket_id": self.bucket_id,
            "bucket_arn": self.bucket_arn,
        })


# Entry point for multi-language support
if __name__ == "__main__":
    component_provider_host(
        name="python-components",
        components=[SecureBucket],
    )
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
- Use `pulumi.Input[T]` type hints for all properties
- Args class must have `__init__` with typed parameters
- Constructor must have `args` parameter with type annotation
- Use `Optional[Input[T]]` for optional properties

**Important:** Use `component_provider_host()` (from `pulumi.provider.experimental`) as the entry point for multi-language components. This is the modern API — the older `pulumi.provider.main()` with a custom Provider subclass is deprecated for component authoring.

### 6. Deployment Workflow

**Validate and deploy with error recovery:**

```bash
# Step 1: Preview changes
pulumi preview

# Step 2: Review output for errors or unexpected changes
# If errors appear, fix code and re-run preview

# Step 3: Deploy only after preview succeeds
pulumi up

# Step 4: Verify outputs
pulumi stack output
```

**For ESC-based deployments:**
```bash
# Step 1: Validate ESC environment resolves correctly
pulumi env open myorg/myproject-dev

# Step 2: Preview with ESC environment
pulumi env run myorg/myproject-dev -- pulumi preview

# Step 3: Deploy with ESC environment
pulumi env run myorg/myproject-dev -- pulumi up

# Step 4: Check stack outputs
pulumi stack output
```

## Configuration & Security

- Use Pulumi ESC for all secrets — never commit secrets to stack config files or Pulumi.yaml
- Enable OIDC authentication instead of static credentials
- Use dynamic secrets with short TTLs when possible
- Apply least-privilege IAM policies to OIDC roles
- Use ComponentResources for reusable infrastructure patterns
- Leverage Python type hints for better IDE support and error detection

## Common Commands

```bash
# Environment Commands (pulumi env)
pulumi env init <org>/<project>/<env>        # Create environment
pulumi env edit <org>/<env>                  # Edit environment
pulumi env open <org>/<env>                  # View resolved values
pulumi env run <org>/<env> -- <command>      # Run with env vars
pulumi env version tag <org>/<env> <tag>     # Tag version

# Pulumi Commands
pulumi new python                      # New project
pulumi config env add <org>/<env>     # Link ESC environment
pulumi preview                         # Preview changes
pulumi up                              # Deploy
pulumi stack output                    # View outputs
pulumi destroy                         # Tear down

# Dependency Management
pip install -r requirements.txt        # Install deps (pip)
poetry add pulumi-aws                  # Add dep (poetry)
uv add pulumi-aws                      # Add dep (uv)
```

## Python-Specific Configuration

**Using pip (default):**
```yaml
# Pulumi.yaml
runtime:
  name: python
  options:
    toolchain: pip
    virtualenv: venv
```

**Using poetry:**
```yaml
# Pulumi.yaml
runtime:
  name: python
  options:
    toolchain: poetry
```

**Using uv:**
```yaml
# Pulumi.yaml
runtime:
  name: python
  options:
    toolchain: uv
    virtualenv: .venv
```

**Enable type checking:**
```yaml
# Pulumi.yaml
runtime:
  name: python
  options:
    typechecker: mypy  # or pyright
```

## References

- [references/pulumi-esc.md](references/pulumi-esc.md) - ESC patterns and commands
- [references/pulumi-patterns.md](references/pulumi-patterns.md) - Common infrastructure patterns
- [references/pulumi-python.md](references/pulumi-python.md) - Python-specific guidance
- [references/pulumi-best-practices-aws.md](references/pulumi-best-practices-aws.md) - AWS best practices
- [references/pulumi-best-practices-azure.md](references/pulumi-best-practices-azure.md) - Azure best practices
- [references/pulumi-best-practices-gcp.md](references/pulumi-best-practices-gcp.md) - GCP best practices
