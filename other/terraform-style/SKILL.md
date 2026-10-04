---
name: terraform-style
description: Terraform/HCL style conventions for writing readable, reusable modules — collection types, resource naming, name_prefix, for_each toggles, variable and output grouping, null defaults, and canonical file layout. Use when writing, reviewing, or refactoring Terraform code (.tf files, modules, root configurations), or when deciding how to name resources, structure variables, or shape module outputs.
license: MIT
---

# Terraform style conventions

Apply these conventions to every module and root configuration; match them when editing existing
code. They are load-bearing for readability and call-site ergonomics, not cosmetic preferences.
For the rationale behind each rule and extended examples, see [reference.md](reference.md).

## 1. Collections: `set(string)` for unordered, unique items

Use `set(string)` (not `list(string)`) whenever elements must be unique and order is irrelevant —
subnet IDs, instance types, CIDRs, ARNs, repository names, regions, namespaces. Uniqueness becomes
intrinsic, `for_each` gets stable keys without `toset()`, and the type documents intent.

```hcl
variable "private_subnet_ids" {
  description = "Private subnet IDs the cluster spans."
  type        = set(string)
}
```

Reserve `list(...)` for genuinely ordered data or where duplicates are meaningful. Terraform
auto-converts a `set` to a `list` when an argument requires one.

## 2. Never name a resource `this`

- A module's single primary resource → `main` (`aws_eks_cluster.main`).
- A `for_each`/`count` resource → a singular noun for one element (`aws_ecr_repository.repo`).
- A secondary singleton → a purpose word (`aws_iam_openid_connect_provider.irsa`,
  `aws_ecr_lifecycle_policy.retention`).

The name should read well at the reference site, not echo the resource type
(`aws_eks_node_group.node_group` is redundant; `.main` is not).

## 3. Prefer `name_prefix` over `name`

For resources whose name is unique within an account/region (IAM roles and policies, instance
profiles, security groups, launch templates, target groups), use `name_prefix` with a trailing `-`.
The provider appends a random suffix, so two stacks — or a create-before-destroy replacement —
never collide on a hard-coded name.

```hcl
resource "aws_iam_role" "node" {
  name_prefix = "${var.cluster_name}-node-" # good: stands up twice without a clash
}
# avoid: name = "${var.cluster_name}-node"
```

Keep the prefix ≤ 38 chars: the AWS random suffix is 26 and IAM role names cap at 64.

## 4. Toggle resources with `for_each`, not `count`

Gate a resource on a boolean with `for_each` over a one-or-zero-element set, keeping a stable
address instead of a positional index:

```hcl
resource "aws_iam_role" "node_windows" {
  for_each = toset(var.enable_windows_nodes ? ["true"] : [])
  # referenced as aws_iam_role.node_windows["true"].arn — not [0]
}
```

Reserve `count` for genuine cardinality (N identical resources).

## 5. Don't prefix outputs with the module name

Outputs read as `module.<name>.<output>`, so a concept prefix duplicates the module name at every
call site. Name the output for the attribute it exposes:

```hcl
output "endpoint" { value = aws_eks_cluster.main.endpoint } # module.cluster.endpoint
# avoid: output "cluster_endpoint"  → module.cluster.cluster_endpoint
```

## 6. Group cohesive variables into one object

Prefer one object variable over a cluster of flat scalars that are always configured together.
Give every attribute `optional(type, default)` and the variable `default = {}` so `module "x" {}`
still works and callers set only what they need:

```hcl
variable "endpoint_access" {
  description = "Cluster API endpoint exposure."
  type = object({
    private      = optional(bool, true)
    public       = optional(bool, false)
    public_cidrs = optional(set(string), [])
  })
  default = {}
}
```

Group only what is genuinely cohesive — unrelated knobs stay flat.

## 7. Group cohesive outputs into one object

When several outputs are facets of one concept and would share a prefix (`oidc_arn`, `oidc_url`),
fold them into a single object output named for the concept:

```hcl
output "node_role" {
  description = "IAM role shared by worker nodes."
  value = {
    arn  = aws_iam_role.node.arn
    name = aws_iam_role.node.name
  }
}
```

A primary resource's own top-level attributes (`name`, `arn`, `endpoint`) stay flat.

## 8. `null` over empty-string defaults

Never default an optional string to `""`. Use `default = null` for a flat variable, or
`optional(string)` with no second argument for an object attribute — `null` is the unambiguous
"unset" signal. Consumers absorb the null with `coalesce(var.proxy.http, "")` or `compact([...])`.

## 9. Canonical file layout

Provider and `required_version` constraints live in `terraform.tf` — never `versions.tf`. A module
consists of `terraform.tf`, `main.tf`, `variables.tf`, `outputs.tf`, `README.md`, plus optional
domain-specific files (`iam-*.tf`). Every variable and output carries a `description`.

To scaffold a new module with this layout, use the `terraform-module` skill; before committing,
run the `terraform-validate` workflow.
