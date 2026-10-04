---
model_tier: medium
name: terraform
description: "Use when writing Terraform — AWS modules, resources, variables, outputs, remote state — even when the user just says 'provision this infra' or 'add an S3 bucket' without naming Terraform."
domain: devops
workspaces:
  - engineering
packs:
  - engineering-base
triggers:
  - phrase: "terraform module"
  - phrase: "terraform state"
---

# terraform

## When to use

Use this skill when writing or modifying Terraform configurations (`.tf` files), creating new infrastructure modules, or understanding AWS resource definitions.

## Procedure: Write Terraform config

1. Read the infrastructure repo structure (check `agents/overrides/skills/terraform.md` for the repo location).
2. Check existing modules in `modules/` for patterns and conventions.
3. Read `variables.tf` of the target module to understand required inputs.
4. Check `versions.tf` for provider version constraints.

## Project structure (typical)

```
{infrastructure-repo}/
├── environments/
│   ├── pro/                    # Production environment
│   │   ├── root.hcl            # Terragrunt root config
│   │   ├── core/               # Core infrastructure (VPC, DNS zones)
│   │   └── {service}/          # Per-service resources
│   └── sta/                    # Stage environment
│       └── ...
├── modules/
│   ├── core/                   # VPC, DNS, shared resources
│   └── {service}/              # Per-service module (ECS, ALB, ECR, etc.)
└── Taskfile.yml                # Task runner commands (or Makefile)
```

Read `agents/overrides/skills/terraform.md` for the actual repository layout and service names.

## Conventions

### Provider versions

- Always pin provider versions in `versions.tf`.
- Check `versions.tf` in the existing modules for the project's version constraints.

### Module sources

Prefer community or organization-specific Terraform modules from the Terraform Registry:

```hcl
module "alb" {
  source  = "{org}/application-load-balancer/aws"
  version = ">= 1.0.0, < 2.0.0"
}
```

Check existing modules in the project for which registry modules are used.

### Naming

- Resource prefix: `var.global_prefix` (e.g., `{project}-{env}`)
- All resources must include `tags = var.tags`
- Security groups: `${var.global_prefix}-<purpose>` (e.g., `-ecs`, `-mysql`, `-redis`)
- Log groups: `/aws/ecs/${cluster}/${service}`

### State management

- Remote state in **S3** with **DynamoDB** locking.
- State is encrypted.
- Key pattern: `${path_relative_to_include()}/terraform.tfstate`

### Variables

- Use typed `variable` blocks with `description`.
- Use `object()` types for complex inputs (not `any` unless unavoidable).
- Use `optional()` with defaults where appropriate.
- Group variables by domain (naming, network, ECS, Redis, database, etc.).

### Lifecycle rules

- Use `ignore_changes = [task_definition]` on ECS services — task definitions are managed by CI/CD, not Terraform.
- Use `deletion_protection = true` on databases.

### Security

- OIDC authentication for GitHub Actions (no long-lived credentials).
- Secrets stored in **AWS Secrets Manager**.
- Security groups follow least-privilege: only allow traffic between known services.
- IAM policies use specific resource ARNs, not wildcards (except where unavoidable).

### Permissive defaults and missing security blocks

The failure that reaches production is almost never a pinned-version mistake;
it is a resource that works either way and was left on its permissive default.
Four constructs carry it. Each backstop grep is over the `.tf` tree you are
changing, not over this repository.

| Backstop grep | What a hit means | Override condition |
|---|---|---|
| `grep -rn '0\.0\.0\.0/0' --include='*.tf' .` | An ingress or egress rule whose CIDR is 0.0.0.0/0, i.e. open to the whole internet. On a management or database port stop and treat it as CRITICAL - the corpus row enumerates which ports those are. | A deliberately public listener - an ALB or CloudFront origin on 80/443. Nothing else. Record the reason next to the rule. |
| `grep -rn 'publicly_accessible\|block_public_acls\|ignore_public_acls' --include='*.tf' .` | Either `publicly_accessible = true` on a database, or a bucket with no public-access block present at all. Absence is the more common hit and the grep returning nothing is the failing case. | A bucket that genuinely serves public web assets, with the policy written explicitly rather than inherited from a default. |
| `grep -rnE '"(Action\|Resource)" *: *"\*"\|= *\["\*"\]' --include='*.tf' .` | A wildcard IAM action or resource. One compromised workload credential then reaches everything in the account. | A named, reviewed exception - `iam:PassRole` scoped by condition, or a bootstrap role. Never the default. |
| `grep -rL 'encrypt' --include='*.tf' .` (lists files with NO encryption mention; `-L` prints names only, so no `-n`) | A storage, volume, snapshot, or database resource with no encryption block. | None for data at rest. A resource holding no data at all. |

Read the surface class before the fix, not after: the mitigation text, the
abuse case, and the negative test live in the `infrastructure` rows of
[`threat-modeling`](../threat-modeling/SKILL.md)'s corpus, which is the single
authority for them. Ask that skill's grounded-corpus step for the
`infrastructure` surface class - it carries the invocation - and describe the
change you are making, e.g. *terraform security group ingress open to
0.0.0.0/0*. Do not copy the command here: one skill owns that interface, for
the same reason one file owns the control text.

Those rows also carry a `Decided by:` clause stating which check actually
decides each one. For all four constructs above that clause reads NO CHECK IN
THIS REPOSITORY - no HCL or IAM-policy parser ships here, so these greps and
your own IaC policy scanner are the whole enforcement story. Do not write or
imply otherwise.

## Common patterns

### ECS service with CodeDeploy (Blue/Green)

Used for web services with zero-downtime deployments:
- ALB → Target Group → ECS Service
- CodeDeploy handles traffic shifting
- Auto-rollback on CloudWatch alarms (5xx error rate)

### ECS service without CodeDeploy

Used for workers and schedulers:
- Direct ECS service update
- `deployment_controller { type = "ECS" }`
- `lifecycle { ignore_changes = [task_definition] }`

### GitHub OIDC IAM role

Each environment has a GitHub IAM role with:
- OIDC trust policy (scoped to repo + environment)
- Policies for ECR push/pull, ECS deployment, Secrets Manager read, CloudWatch logs

## Output format

1. Terraform configuration files (.tf) with proper module structure
2. Variables, outputs, and state management config

## Auto-trigger keywords

- Terraform
- AWS infrastructure
- modules
- resources
- state management

## Known pitfalls

| Symptom | Root cause | Fix |
|---|---|---|
| `Error acquiring the state lock` blocks every command | A prior `apply` crashed / was killed and left the lock held (DynamoDB / backend lock) | Confirm no apply is actually running, then `terraform force-unlock <lock-id>` — never delete the lock table |
| `plan` wants to destroy+recreate a resource after a rename | Renaming a resource block changes its address; Terraform sees the old address gone and a new one added | `terraform state mv <old.addr> <new.addr>` (or a `moved {}` block) so it tracks the same object |
| `count`/`for_each` errors with "value depends on resource attributes that cannot be determined until apply" | The count/for_each expression reads an unknown (not-yet-created) value | Key `for_each` off a static/known map, or split into a two-stage apply with `-target` |
| A change applies but the next `plan` shows the same diff again (perpetual diff) | The provider normalizes/computes the attribute differently than written (ordering, defaults, case) | Match the provider's canonical form, or `ignore_changes` on that attribute in `lifecycle` |
| `plan` shows a resource as tainted/replaced after a manual console change | Out-of-band drift — someone edited the resource outside Terraform | `terraform apply -refresh-only` to reconcile state, then decide code-vs-cloud; stop the manual edits |

## Gotcha

- `terraform apply` without `-auto-approve` requires interactive confirmation — don't use in CI without the flag.
- The model forgets to run `terraform plan` before `apply` — always plan first, review changes.
- State files contain sensitive data — never commit them to Git. Use remote state (S3 + DynamoDB).

## Do NOT

- Do NOT use `*` in IAM resource ARNs unless absolutely necessary.
- Do NOT remove `deletion_protection` from databases.
- Do NOT change provider versions without testing in Stage first.
- Do NOT hardcode AWS account IDs — use `data.aws_caller_identity.current`.
