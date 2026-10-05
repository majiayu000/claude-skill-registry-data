---
name: iac-best-practices
description: "State is the map between your code and real resources."
---

# IaC Best Practices (Verbose)

## Core Patterns

### Remote State and Locking

State is the map between your code and real resources. Everything else in
Terraform is downstream of it being correct, shared, and singular.

```hcl
terraform {
  required_version = "~> 1.9"

  backend "s3" {
    bucket         = "acme-tfstate-prod"
    key            = "network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-locks"
    encrypt        = true
  }
}
```

Three failure modes make this the first thing you configure:

**Concurrent applies.** Two engineers apply at once against an unlocked backend.
Both read the same state, both create resources, the second write clobbers the
first. You now own resources Terraform does not know about, and state entries for
resources that were replaced. The lock table turns the second apply into a wait.

**Loss.** State on a laptop is one disk failure from a full estate re-import.
Bucket versioning is the cheap insurance — `aws s3api list-object-versions` plus a
copy of the prior version is a two-minute recovery from a bad apply.

**Secrets.** State stores attribute values verbatim, including
`aws_db_instance.password` and any generated private key. Treat the bucket as
production credential storage: SSE-KMS, a bucket policy denying non-TLS access,
and read access limited to the CI role and break-glass.

For Terraform Cloud/Enterprise the mechanism differs but the rules do not.

### Plan Review as the Control Point

Code review catches intent. The plan catches consequence — and they differ far
more often than people expect, because provider behaviour, existing state, and
data sources all participate in the outcome.

```yaml
# .github/workflows/terraform.yml (excerpt)
- run: terraform init
- run: terraform validate
- run: terraform plan -lock-timeout=5m -out=tfplan
- run: terraform show -no-color tfplan > plan.txt
- uses: actions/github-script@v7        # post plan.txt as a PR comment
```

Then, on merge, apply the *saved plan* — not a fresh one:

```bash
terraform apply -input=false tfplan
```

Applying `tfplan` guarantees the approved diff is the executed diff. A fresh plan
at apply time can differ from the reviewed one because the world moved underneath
it.

Read plans for the verbs, in order of danger:

| Plan symbol | Meaning | Review posture |
|---|---|---|
| `+` | create | Normal |
| `~` | update in place | Check the attribute |
| `-/+` | **replace** — destroy then create | Stop. Is it stateful? |
| `-` | destroy | Stop. Was this intended? |

`-/+` on an RDS instance, EBS volume, or anything holding data is the single most
expensive thing a plan can say, and it is easy to trigger accidentally — changing
an availability zone, a subnet group, or an engine argument that forces
replacement. Add `prevent_destroy` where the answer is always no:

```hcl
resource "aws_db_instance" "primary" {
  # ...
  lifecycle {
    prevent_destroy = true
  }
}
```

### Module Composition, and When Not To

A module is an interface, and interfaces are expensive to change once they have
callers. The cost of a premature module exceeds the cost of duplication: every
future caller either fits the abstraction or bolts another variable onto it, and
after a year the module has forty optional inputs and nobody can predict its
output.

Extract when the shape has stabilised across three real call sites — not two, and
certainly not one you are anticipating.

```hcl
module "service" {
  source = "git::ssh://git@github.com/acme/tf-modules.git//service?ref=v2.4.0"

  name          = "checkout"
  environment   = var.environment
  instance_type = "t3.medium"
  desired_count = 4
}
```

Signs a module is doing real work versus passing arguments through:

| Healthy module | Passthrough wrapper |
|---|---|
| Few inputs, opinionated defaults | One variable per resource argument |
| Encodes a decision (naming, tagging, HA topology) | Encodes nothing |
| Callers get shorter | Callers get longer |
| Version bumps mean something | Version bumps are cosmetic |

Always pin `ref=` or `version =` to an immutable tag. A module tracking `main`
means today's plan and tomorrow's plan differ for reasons absent from your diff —
the exact property IaC exists to eliminate.

### State Separation by Blast Radius

Split state along lifecycle boundaries, then along environments:

```
infra/
  network/prod/          # VPC, subnets, transit gateway — changes quarterly
  data/prod/             # RDS, ElastiCache — changes rarely, destroys hurt
  platform/prod/         # EKS, IAM roles — changes monthly
  apps/checkout/prod/    # services — changes daily
```

The daily-churn state should not be *able* to plan a change against the database.
Cross-boundary reads go through data sources, which are read-only by construction:

```hcl
data "aws_vpc" "main" {
  tags = {
    Name = "prod-main"
  }
}
```

`terraform_remote_state` also works but couples you to another state's internal
outputs; prefer tags or SSM parameters as the contract where you can.

The second benefit is plan time. A 4,000-resource state takes minutes to refresh,
so engineers stop running plans, so plans stop being the control point. Splitting
state is a correctness measure disguised as a performance one.

### Provider and Dependency Pinning

```hcl
required_providers {
  aws = {
    source  = "hashicorp/aws"
    version = "~> 5.60"     # allows 5.60.x upward within 5.x, blocks 6.0
  }
}
```

Commit `.terraform.lock.hcl`. It records exact provider versions and hashes, so CI
and every laptop resolve identically. Upgrade deliberately with
`terraform init -upgrade`, in its own pull request, with the plan attached — a
provider major version can change defaults and produce diffs on code you never
touched.

### Policy and Static Checks

Automated checks in CI catch the mistakes review misses once a diff runs long:

```bash
terraform fmt -check -recursive     # formatting, non-negotiable
terraform validate                  # syntax and type errors
tflint --recursive                  # provider-specific lint
checkov -d . --framework terraform  # security posture
```

For rules that must not be bypassed — no public S3 buckets, mandatory cost-centre
tags, approved instance families — enforce with OPA/Conftest or Sentinel against
the plan JSON (`terraform show -json tfplan`), not against the HCL source. The plan
is the truth; HCL can compute the offending value at runtime and slip past a
source-level check.

Container image and runtime hardening rules belong in
`container-security-hardening`; keep the IaC policy set focused on infrastructure
shape.

### Secrets

Never literal, and never more of them in state than necessary:

```hcl
data "aws_secretsmanager_secret_version" "db" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "primary" {
  password = data.aws_secretsmanager_secret_version.db.secret_string
}
```

This still lands the value in state — which is why the encrypted, access-controlled
backend is not optional. The strictly better pattern, where the resource supports
it, is to let the running service fetch its own secret and have Terraform manage
only the reference and the IAM grant.

## Common Anti-Patterns

❌ **Local state, or a remote backend without a lock table** — concurrent applies
silently corrupt state and CI can never run.
✅ Remote backend with locking, versioning, and encryption, configured before the
first resource.

❌ **Applying from a laptop** — no plan record, no approval, no audit trail, and
whatever happened to be in that engineer's shell environment.
✅ Plan on PR, apply from CI using the saved plan file.

❌ **Fixing production in the console "just this once"** — the change is invisible
to everyone else and the next apply reverts it.
✅ Read-only humans in production; every change through the pipeline.

❌ **Modularising the first time you write something** — you are designing an
interface from a sample size of one.
✅ Duplicate until the shape stabilises across three call sites, then extract.

❌ **Module sources on `main`, providers unpinned, lock file gitignored** — plans
stop being reproducible and diffs appear from nowhere.
✅ Pin versions; commit `.terraform.lock.hcl`; upgrade in dedicated PRs.

❌ **One state file for the entire estate** — an application tag change plans
against the database, and refresh takes five minutes.
✅ Split by lifecycle and environment; cross boundaries with data sources.

❌ **Approving a plan containing `-/+` on a stateful resource without reading it**
— that is a destroy with extra steps.
✅ `prevent_destroy` on data stores; treat replace lines as a hard stop.

❌ **`terraform apply -auto-approve` in an interactive workflow** — appropriate in
CI against a reviewed plan file, an accident generator at a terminal.
✅ Reserve auto-approve for pipelines applying a pre-approved `tfplan`.

## IaC Checklist

- [ ] Remote backend with state locking, versioning, and encryption at rest
- [ ] State bucket access restricted to the CI role and break-glass only
- [ ] `terraform plan` runs on every PR and is posted for review
- [ ] Apply consumes the saved plan artifact, not a fresh plan
- [ ] Humans have read-only access to production infrastructure
- [ ] `prevent_destroy` on databases, volumes, and other stateful resources
- [ ] State split by lifecycle and environment, not one monolith
- [ ] Provider and module versions pinned to immutable refs
- [ ] `.terraform.lock.hcl` committed
- [ ] `fmt`, `validate`, `tflint`, and a security scanner run in CI
- [ ] Policy rules evaluated against plan JSON, not HCL source
- [ ] No secret literals in code; state treated as sensitive
- [ ] Scheduled drift detection in place (see `infrastructure-drift-detection`)
