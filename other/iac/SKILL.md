---
name: iac
description: "Routes Infrastructure as Code requests to the correct technology skill and compares Terraform, OpenTofu, Pulumi, CloudFormation, Bicep, and Ansible for provisioning strategy. WHEN: \"infrastructure as code\", \"IaC comparison\", \"Terraform vs Ansible\", \"Terraform vs Pulumi\", \"which IaC tool\", \"IaC strategy\", \"configuration management vs provisioning\". Do NOT use for tool-specific syntax or debugging — use the `terraform`, `opentofu`, `pulumi`, `cloudformation`, `bicep`, or `ansible` skill directly."
license: MIT
---

# Infrastructure as Code Router

This skill routes Infrastructure as Code requests to the right technology skill and covers cross-tool comparison. Determine which technology best matches the request, then read that skill's SKILL.md for implementation depth.

## Decision Matrix

| Signal | Skill |
|--------|----------|
| Terraform, HCL, providers, modules, state, workspaces, plan/apply | `terraform` |
| OpenTofu, tofu plan, tofu apply, Terraform fork, MPL license | `opentofu` |
| Pulumi, pulumi up, TypeScript/Python/Go IaC, ComponentResource | `pulumi` |
| CloudFormation, CFN, AWS stacks, StackSets, SAM, CDK | `cloudformation` |
| Bicep, ARM template, Azure Resource Manager, az deployment | `bicep` |
| Ansible, playbooks, roles, inventory, modules, AWX, Tower, Jinja2 | `ansible` |
| IaC comparison, "which tool", provisioning vs config management | Handle directly (below) |

## How to Route

1. **Extract technology signals** from the user's question — tool names, file extensions (.tf, .yml), CLI commands (terraform, ansible-playbook), provider names.
2. **Check for version specifics** — if a version is mentioned (Terraform 1.15, Ansible 2.20), read the matched technology skill; version-specific nuance lives in its `references/versions/` directory.
3. **Comparison requests** — if the user is comparing IaC tools, handle directly using the framework below.
4. **Ambiguous requests** — if the user says "automate my infrastructure" without specifying a tool, gather context (cloud provider, existing tooling, team skills) before routing.

## IaC Fundamentals

Load `references/concepts.md` when the user needs foundational understanding of IaC patterns that apply across all tools.

## Tool Selection Framework

### Provisioning vs Configuration Management

This is the most important distinction in IaC:

| Category | Purpose | Tools | Analogy |
|---|---|---|---|
| **Provisioning** | Create/destroy infrastructure resources (VMs, networks, databases, DNS) | Terraform, Pulumi, CloudFormation, Bicep | Building the house |
| **Configuration Management** | Configure existing servers (install packages, manage files, start services) | Ansible, Chef, Puppet, SaltStack | Furnishing the house |

**Terraform and Ansible are complementary, not competing.** Terraform creates the VM; Ansible configures it. The overlap is in simple provisioning (Ansible can create cloud resources) and simple configuration (Terraform provisioners can run scripts).

### When to Use Each Tool

| Scenario | Best Tool | Why |
|---|---|---|
| Multi-cloud infrastructure provisioning | Terraform | Provider ecosystem, state management, plan/apply workflow |
| AWS-only infrastructure | Terraform or CloudFormation | CloudFormation has deeper AWS integration; Terraform is more portable |
| Azure-only infrastructure | Terraform or Bicep | Bicep has native Azure support; Terraform for multi-cloud |
| Server configuration at scale | Ansible | Agentless, SSH-based, idempotent modules, wide OS support |
| Immutable image builds (AMIs, VM images) | Packer + Ansible | Packer orchestrates; Ansible provisions the image |
| Developers who want real programming languages | Pulumi | TypeScript, Python, Go, C# instead of DSLs |
| Kubernetes resource management | Helm, Kustomize, or ArgoCD/Flux | Purpose-built for K8s; Terraform K8s provider is awkward |
| Network device configuration | Ansible | Network modules for Cisco, Juniper, Arista, Palo Alto |

### Comparison Matrix

| Dimension | Terraform | Ansible | Pulumi |
|---|---|---|---|
| **Model** | Declarative | Procedural (idempotent tasks) | Declarative (imperative syntax) |
| **Language** | HCL | YAML + Jinja2 | Python, TypeScript, Go, C# |
| **State** | Remote state file (required) | Stateless (agentless) | Managed or self-hosted state |
| **Agent** | None | None (SSH/WinRM) | None |
| **Strengths** | Plan preview, provider ecosystem, modules | Agentless, simple, config management | Real languages, IDE support, testing |
| **Weaknesses** | State complexity, HCL limits | Slow at scale, ordering matters | Vendor risk, debugging complexity |
| **Community** | Massive (largest IaC ecosystem) | Massive (most popular config mgmt) | Growing (smaller than Terraform) |
| **Licensing** | BSL 1.1 (HashiCorp) | GPL v3 (Red Hat) | Apache 2.0 (core) |

## Anti-Patterns

1. **"Terraform for configuration management"** — Using Terraform provisioners (remote-exec, local-exec) for server config. Use Ansible or cloud-init instead.
2. **"Ansible for infrastructure provisioning at scale"** — Ansible can create cloud resources, but without state tracking it can't detect drift or plan changes. Use Terraform for provisioning.
3. **"One giant Terraform root module"** — Monolithic state files are slow, risky, and hard to maintain. Decompose into smaller, independent state units.
4. **"No remote state"** — Local Terraform state in a team = guaranteed conflicts and data loss.
5. **"Click-ops then import"** — Creating resources manually then importing into Terraform. Start with IaC from day one.

## Reference Files

- `references/concepts.md` — IaC principles (state management, idempotency, immutable infrastructure, drift detection). Read for foundational or comparison questions.
