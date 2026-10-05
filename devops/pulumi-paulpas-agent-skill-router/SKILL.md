---




name: pulumi
description: Integrates with the Pulumi Python SDK and Automation API to manage stacks,
  resources, programs, ESC (Environments, Secrets, and Configuration), and deployment
  orchestration.
license: MIT
compatibility: opencode
metadata:
  version: "1.0.0"
  domain: coding
  triggers: pulumi python, pulumi automation api, pulumi sdk, pulumi stacks, pulumi
    esc, infrastructure as code python, pulumi program, pulumi deploy
  archetypes:
  - tactical
  - generation
  anti_triggers:
  - brainstorming
  - vague ideation
  - code golf
  - over-engineering
  response_profile:
    verbosity: low
    directive_strength: high
    abstraction_level: operational
  role: implementation
  scope: implementation
  output-format: code
  content-types:
  - code
  - guidance
  - do-dont
  - examples
  related-skills: coding-terraform-sdk, coding-kubernetes-api, coding-docker-api




---




# Pulumi Python SDK & Automation API Integration

Integrates with Pulumi using the official Python SDK (`pulumi`) and Automation API (`pulumi.automation`) to define cloud infrastructure as Python code, manage stacks, orchestrate deployments, handle secrets with ESC, and build self-service infrastructure platforms.

## TL;DR for Code Generation

- [ ] Use `pulumi.export()` for stack outputs and `pulumi.Config()` for stack configuration
- [ ] Always call `.apply()` on `Output[T]` values — never access them synchronously
- [ ] Use the Automation API (`LocalWorkspace` + `InlineProgram`) for programmatic infrastructure management
- [ ] Pass configuration via `StackConfig` objects or `config` dicts, not environment variables
- [ ] Use `pulumi.ResourceOptions` for parent/child relationships, depends_on, and protection
- [ ] Install Pulumi CLI separately — the Python SDK requires it for state management and deployment
- [ ] Use `pulumi.StackReference` to share outputs between stacks

---

## When to Use

Use this skill when:

- Defining cloud infrastructure in pure Python (AWS, Azure, GCP, Kubernetes, etc.) using Pulumi providers
- Building internal platforms that provision infrastructure on demand via Automation API
- Managing secrets, environment configurations, and feature flags with Pulumi ESC
- Implementing multi-stack deployments with shared state references
- Creating custom infrastructure abstractions and reusable Pulumi components
- Running Pulumi programs inline from web services, CLIs, or CI/CD pipelines

---

## When NOT to Use

Avoid this skill for:

- Write-only infrastructure that you never update or destroy (use Terraform or CloudFormation instead)
- Infrastructure where you cannot install the Pulumi CLI (the SDK depends on the `pulumi` binary)
- Simple static infrastructure that is better expressed in YAML or HCL
- Learn Pulumi concepts (refer to the official Pulumi documentation and tutorials)

---

## Core Workflow

1. **Define the Pulumi Program** — Create a Python file that imports `pulumi` and provider packages (e.g., `pulumi_aws`). Declare resources as Python objects with typed properties. **Checkpoint:** Verify program runs with `pulumi preview` before deploying.

2. **Configure the Stack** — Use `pulumi.Config()` to read configuration values (region, instance size, etc.) and `pulumi.export()` to expose stack outputs. **Checkpoint:** Verify config keys are set via `pulumi config set` or the Automation API config parameter.

3. **Deploy with `pulumi up`** — Run `pulumi up` (or `stack.up()` in Automation API) to create or update resources. Pulumi computes a desired state diff and applies it. **Checkpoint:** Verify each resource's `status` shows "created" or "updated" and outputs are populated.

4. **Manage Stack Outputs** — Read outputs with `pulumi stack output` or via `StackReference`. Use `Output.apply()` to chain dependent resource creation. **Checkpoint:** Validate output values match expected schema (ARNs, URLs, IDs).

5. **Destroy Resources** — Run `pulumi destroy` (or `stack.destroy()`) when infrastructure is no longer needed. Protected resources will block destruction. **Checkpoint:** Confirm all resources are removed from the stack state with `pulumi stack export`.

---

## Implementation Patterns

### Pattern 1: Pulumi Program — AWS S3 Website Infrastructure

```python
"""Pulumi program to deploy a static website to AWS S3.

Run with: pulumi up
"""
import pulumi
import pulumi_aws as aws
import pulumi_aws.s3 as s3


def create_static_site() -> dict:
    """Define an S3-backed static website with public access.

    Returns:
        Dict with bucket name, website URL, and ARN.
    """
    config = pulumi.Config()
    bucket_name = config.require("bucket_name")
    index_document = config.get("index_document", "index.html")
    error_document = config.get("error_document", "error.html")

    # Create the S3 bucket with website hosting
    bucket = s3.Bucket(
        bucket_name,
        bucket=bucket_name,
        website=s3.BucketWebsiteArgs(
            index_document=index_document,
            error_document=error_document,
        ),
        force_destroy=True,
    )

    # Apply a bucket policy for public read access
    bucket_policy = bucket.arn.apply(
        lambda arn: aws.iam.get_policy_document(
            statements=[
                aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
                    principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                        type="*",
                        identifiers=["*"],
                    )],
                    actions=["s3:GetObject"],
                    resources=[f"{arn}/*"],
                ),
            ],
        )
    )

    s3.BucketPolicy(
        f"{bucket_name}-policy",
        bucket=bucket.id,
        policy=bucket_policy.json,
    )

    # Export stack outputs
    pulumi.export("bucket_name", bucket.id)
    pulumi.export("website_url", bucket.website_endpoint)
    pulumi.export("bucket_arn", bucket.arn)

    return {
        "bucket_name": bucket.id,
        "website_url": bucket.website_endpoint,
        "bucket_arn": bucket.arn,
    }


# Entry point for pulumi run
stack_outputs = create_static_site()
```

### Pattern 2: Automation API — Inline Program and Deployment

```python
import os
import json
from pulumi import automation as auto


def deploy_inline_program(
    stack_name: str,
    project_name: str,
    config: dict[str, str],
) -> dict:
    """Deploy infrastructure using Pulumi Automation API with an inline program.

    This runs a Pulumi program entirely from code without needing
    Pulumi.yaml or Python files on disk — perfect for embedded use.

    Args:
        stack_name: Name for the Pulumi stack.
        project_name: Project name for the stack.
        config: Stack configuration key-value pairs.

    Returns:
        Dict with stack outputs and deployment summary.
    """

    # Define the inline program (closure — captures config at definition time)
    def pulumi_program():
        import pulumi
        import pulumi_aws as aws

        # Read config inside the program
        cfg = pulumi.Config()
        instance_type = cfg.require("instance_type")
        ami_id = cfg.get("ami_id", "ami-0c55b159cbfafe1f0")

        # Create an EC2 instance
        sg = aws.ec2.SecurityGroup(
            "web-sg",
            description="Allow HTTP traffic",
            ingress=[aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=80,
                to_port=80,
                cidr_blocks=["0.0.0.0/0"],
            )],
            egress=[aws.ec2.SecurityGroupEgressArgs(
                protocol="-1",
                from_port=0,
                to_port=0,
                cidr_blocks=["0.0.0.0/0"],
            )],
        )

        instance = aws.ec2.Instance(
            "web-server",
            instance_type=instance_type,
            ami=ami_id,
            vpc_security_group_ids=[sg.id],
            tags={"Name": "web-server", "ManagedBy": "Pulumi-Automation"},
        )

        pulumi.export("instance_id", instance.id)
        pulumi.export("public_ip", instance.public_ip)
        pulumi.export("public_dns", instance.public_dns)

    # Create or select a stack using Automation API
    stack = auto.create_or_select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=pulumi_program,
    )

    # Set configuration
    for key, value in config.items():
        stack.set_config(key, auto.ConfigValue(value))

    # Deploy
    up_result = stack.up(on_output=print)

    return {
        "stack_name": stack_name,
        "deployment_status": up_result.summary.result,
        "outputs": up_result.outputs,
        "resource_count": up_result.summary.resource_changes,
    }
```

### Pattern 3: Pulumi ESC — Environment Management

```python
"""Secure environment and secret management with Pulumi ESC (Environments,
Secrets, and Configuration).

ESC lets you define environments that compose configuration from
multiple sources (AWS secrets, OIDC, static config) and import them
into Pulumi stacks or any tool.
"""

import json
import pulumi_esc_sdk as esc
from pulumi_esc_sdk.api import environments_api
from pulumi_esc_sdk.models import EnvironmentDefinition


def create_esc_environment(
    org_name: str,
    env_name: str,
    aws_region: str = "us-east-1",
    oidc_provider_arn: str | None = None,
    static_vars: dict[str, str] | None = None,
) -> dict:
    """Create or update a Pulumi ESC environment with OIDC and static config.

    This environment can be opened from any Pulumi stack or external
    tool without hardcoding secrets.

    Args:
        org_name: Pulumi Cloud organization.
        env_name: ESC environment name.
        aws_region: AWS region for provider configuration.
        oidc_provider_arn: IAM OIDC provider ARN for AWS authentication.
        static_vars: Static environment variables to include.

    Returns:
        Dict with environment name and status.
    """
    configuration = esc.Configuration(
        access_token=os.environ["PULUMI_ACCESS_TOKEN"],
    )

    with esc.ApiClient(configuration) as api_client:
        api = environments_api.EnvironmentsApi(api_client)

        # Build the environment definition with OIDC integration
        env_def: dict = {
            "values": {
                "aws": {
                    "login": {
                        "use": "aws-iam",
                        "with": {
                            "region": aws_region,
                        },
                    },
                },
                "environmentVariables": {},
            }
        }

        if oidc_provider_arn:
            env_def["values"]["aws"]["login"]["with"]["oidcProviderArn"] = (
                oidc_provider_arn
            )
            env_def["values"]["aws"]["login"]["with"]["roleArn"] = (
                f"arn:aws:iam::123456789012:role/pulumi-esc-role"
            )

        if static_vars:
            env_def["values"]["environmentVariables"] = static_vars

        try:
            api.create_environment(
                org_name=org_name,
                environment_name=env_name,
                environment_definition=EnvironmentDefinition(
                    json.dumps(env_def)
                ),
            )
        except esc.ApiException as exc:
            if exc.status == 409:
                # Update existing environment
                api.update_environment(
                    org_name=org_name,
                    environment_name=env_name,
                    environment_definition=EnvironmentDefinition(
                        json.dumps(env_def)
                    ),
                )
            else:
                raise RuntimeError(
                    f"Failed to create ESC environment '{env_name}': "
                    f"HTTP {exc.status} — {exc.body}"
                ) from exc

    return {
        "environment_name": env_name,
        "organization": org_name,
        "aws_region": aws_region,
    }
```

### BAD vs GOOD: Output Handling

```python
# ❌ BAD — trying to access Output[T] like a regular value
def bad_output_handling():
    import pulumi_aws as aws
    bucket = aws.s3.Bucket("my-bucket")
    # This is WRONG — Output is a lazy promise, not a string!
    print(f"Bucket name: {bucket.id}")  # Prints <output> not the actual name

# ✅ GOOD — using .apply() to work with Output values
def good_output_handling():
    import pulumi
    import pulumi_aws as aws

    bucket = aws.s3.Bucket("my-bucket")

    # Correct: chain computation with .apply()
    bucket_url = bucket.bucket_domain_name.apply(
        lambda domain: f"https://{domain}"
    )

    pulumi.export("bucket_url", bucket_url)

    # For combining multiple outputs, use Output.all()
    combined = pulumi.Output.all(bucket.id, bucket.arn).apply(
        lambda args: f"Bucket {args[0]} has ARN {args[1]}"
    )
    pulumi.export("summary", combined)
```

## MUST DO

- Use `pulumi.export()` to expose all values that downstream stacks or users will need
- Use `Output[T].apply()` and `Output.all()` for chaining dependent resource values
- Set `protect=True` on critical infrastructure resources to prevent accidental deletion
- Use `pulumi.Config()` for all configurable values — never hardcode region, size, or environment
- Use `StackReference` with `require_output()` to share values between Pulumi stacks
- Use the Automation API's `on_output` callback to stream `pulumi up` logs in real time
- Use Pulumi ESC for managing secrets and multi-environment configuration

## MUST NOT DO

- Never try to access `Output[T]` values synchronously (e.g., `bucket.id + "/suffix"`) — always use `.apply()`
- Do not store plaintext secrets in stack config — use `pulumi config set --secret`
- Never run `pulumi destroy` on protected resources without first removing the protection flag
- Avoid creating very large Pulumi programs that cannot be reasoned about as a unit
- Do not ignore `pulumi preview` — always review the diff before applying changes
- Never embed Pulumi access tokens in code — use the `PULUMI_ACCESS_TOKEN` environment variable

---

## Constraints

### MUST DO
- Validate all inputs at function boundaries before processing — guard clauses should fail early with descriptive errors
- Implement proper error handling that distinguishes between recoverable and unrecoverable failures
- Add comprehensive logging with structured context (correlation IDs, operation names, timing) for debugging and monitoring
- Write unit tests covering normal operations, edge cases, and error conditions before integrating the component

### MUST NOT DO
- Do not silently swallow exceptions — always log or propagate errors with meaningful context
- Avoid unbounded resource allocation without limits (connection pools, memory buffers, thread counts)
- Never use hardcoded credentials, API keys, or secrets in source code
- Do not bypass input validation for perceived performance gains


## Live References

- [Pulumi Python SDK Documentation](https://www.pulumi.com/docs/reference/pkg/python/pulumi/)
- [Pulumi Automation API Documentation](https://www.pulumi.com/docs/iac/automation-api/)
- [Pulumi Automation API Concepts](https://www.pulumi.com/docs/iac/automation-api/concepts-terminology/)
- [Pulumi ESC Python SDK](https://www.pulumi.com/docs/esc/sdk/python/)
- [Pulumi GitHub Repository](https://github.com/pulumi/pulumi)
- [Pulumi Registry — Providers](https://www.pulumi.com/registry/)
- [Pulumi Automation API Examples (Python)](https://github.com/pulumi/automation-api-examples/tree/main/python)

## Related Skills

| Skill | Purpose |
|---|---|
| `coding-terraform-sdk` | Terraform/OpenTofu as an alternative IaC framework |
| `coding-kubernetes-api` | Pulumi Kubernetes provider for managing K8s resources |
| `coding-docker-api` | Docker API for container-level operations alongside Pulumi |
