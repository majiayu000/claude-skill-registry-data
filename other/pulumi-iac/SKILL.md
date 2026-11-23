---
name: pulumi-iac
description: "Build infrastructure with Pulumi in general-purpose languages: stacks, component resources, secrets, preview policy and CI automation."
type: procedural
category: cloud
domain: cloud
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: high
level: advanced
triggers:
  - pulumi stack configuration
  - pulumi component resource
  - pulumi secrets encryption
  - pulumi preview ci
  - pulumi vs terraform
keywords:
  - pulumi
  - iac
  - stack
  - component-resource
  - secrets
  - preview
source: custom
enabled: true
---

# Pulumi Infrastructure as Code

## Purpose

Build infrastructure with Pulumi in general-purpose languages: stacks, component resources, secrets, preview policy and CI automation.

## When to Use

- Infrastructure should be expressed in TypeScript, Python, Go or C# alongside application code.
- Existing Terraform is being migrated or bridged rather than rewritten.
- Stacks must be previewed and promoted consistently.

## When NOT to Use

- The team has no capacity to own a programming-language IaC stack.
- A simple static Terraform module already covers the need.
- You need a provider Pulumi does not support and cannot bridge.

## Capabilities

- Define component resources with typed inputs and outputs.
- Manage per-stack configuration and encrypted secrets.
- Gate previews in CI and promote one stack per environment.
- Interoperate with existing Terraform providers where needed.

## Inputs

- The language runtime and Pulumi CLI version.
- Stack layout (dev/stage/prod) and state backend.
- The provider credentials and the resources to create.

## Workflow

1. Model reusable pieces as component resources instead of long flat programs.
2. Keep configuration in stack files; never hardcode account ids.
3. Store secrets via `pulumi config set --secret` so they are encrypted at rest.
4. Run `pulumi preview --diff` in CI and require review for destructive steps.
5. Promote with `pulumi up` per stack and record outputs in the deployment log.

## Tools

- pulumi CLI
- pulumi config / pulumi stack
- CI runner with OIDC credentials

## Examples

- `pulumi stack select prod && pulumi preview --diff`
- `pulumi config set --secret dbPassword`
- `pulumi up --yes --skip-preview`

## Safety

- `pulumi destroy` on a stateful stack can delete production data; require explicit approval.
- Secrets in plain config leak into state and logs.
- Outputs are visible to anyone with stack access; treat them as public.

## Source

All-Skills canonical library (`skills/cloud/pulumi-iac`). First-party skill, maintained in this repository.

## Notes

- Component resources make the resource graph readable in previews.
- Pulumi can consume Terraform providers and remote state during a migration.
- Pairs with: `cloud/terraform-iac`, `cloud/aws-compute`.
