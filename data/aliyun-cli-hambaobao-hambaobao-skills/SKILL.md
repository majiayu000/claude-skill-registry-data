---
name: aliyun-cli
description: |
  Manage Alibaba Cloud resources using the Aliyun CLI tool.
  Use this skill whenever the user wants to manage any Alibaba Cloud resource via the aliyun CLI,
  including: ECS instances, VPC networking, OSS object storage, RDS databases, SLB/CLB load
  balancers, RAM users/roles/policies, DNS records, or aliyun CLI setup and authentication.
  If the user mentions "阿里云", "Alibaba Cloud", "aliyun", "ECS", "VPC", "OSS", "RDS", "SLB",
  "RAM", "ACR", "Container Registry", or any Alibaba Cloud service, use this skill.
metadata:
  openclaw:
    emoji: "☁️"
    requires:
      bins: ["aliyun"]
    install:
      - id: brew
        kind: brew
        formula: aliyun-cli
        bins: ["aliyun"]
        label: "Install Aliyun CLI (brew)"
---

# Aliyun CLI Skill

This skill teaches you how to use the [Aliyun CLI](https://github.com/aliyun/aliyun-cli) to manage
Alibaba Cloud resources. You will construct and explain `aliyun` commands, interpret their output,
and guide users through cloud resource management tasks.

## Quick Reference

| Resource | Reference File | Common Operations |
|----------|---------------|-------------------|
| Setup & Auth | `references/setup.md` | install, configure, switch profiles |
| ECS (Elastic Compute Service) | `references/ecs.md` | list, start/stop/reboot, resize disk, create snapshot |
| VPC (Virtual Private Cloud) | `references/vpc.md` | manage VPCs, VSwitches, EIPs, NAT gateways, route tables |
| OSS (Object Storage Service) | `references/oss.md` | buckets, upload/download, sync, presigned URLs |
| RDS (Relational Database Service) | `references/rds.md` | instances, databases, accounts, backups, IP whitelist |
| SLB / CLB (Load Balancer) | `references/slb.md` | create LB, manage listeners, add/remove backend servers |
| RAM (Resource Access Management) | `references/ram.md` | users, groups, roles, policies, access keys |
| DNS (AliDNS) | `references/dns.md` | list domains, add/update/delete records |
| ACR (Container Registry) | `references/acr.md` | instances, namespaces, repositories, image tags, docker login |

Read the relevant reference file before responding to a request.

## CLI Syntax Pattern

Every `aliyun` command follows this structure:

```
aliyun <Product> <Operation> [--Parameter Value ...]
```

- **Product**: service name in PascalCase or lowercase (e.g., `ecs`, `oss`, `vpc`, `rds`, `ram`)
- **Operation**: API action name in PascalCase (e.g., `DescribeInstances`, `StartInstance`)
- **Parameters**: prefixed with `--` (e.g., `--RegionId cn-hangzhou`, `--InstanceId i-xxxx`)

OSS is an exception — it uses a subcommand style like `aliyun oss ls`, `aliyun oss cp`.

## Always Check These First

Before constructing any command:

1. **Region** — Most operations require `--RegionId`. Common regions:
   - `cn-hangzhou` (Hangzhou), `cn-beijing` (Beijing), `cn-shanghai` (Shanghai)
   - `cn-shenzhen` (Shenzhen), `ap-southeast-1` (Singapore), `us-west-1` (US West)
   - If the user hasn't specified a region, ask or use `aliyun configure get` to find the default.

2. **Resource IDs** — Most mutating operations (start, stop, delete) need a specific resource ID.
   If the user hasn't provided one, first run a Describe/List command to find it.

3. **Pagination** — Describe* APIs return paginated results. Default page size is typically 10.
   Use `--PageSize 100` and `--PageNumber` to retrieve more. Mention this if results seem incomplete.

4. **Dry run** — Aliyun CLI does not have a universal dry-run flag. For destructive operations,
   always confirm resource IDs with the user before executing.

## Output Formats

The CLI supports multiple output formats via the `--output` flag:
- Default: JSON (structured, good for parsing)
- `--output cols=<col1>,<col2>` — tabular output for quick scanning
- `--output table` — aligned table

For human-readable summaries, use `--output cols=InstanceId,InstanceName,Status` style where available.

**zsh gotcha**: If you use `rows=Instances.Instance[]`, the `[]` will be interpreted as a glob by zsh
and cause a "no matches found" error. Quote the argument to avoid this:
```bash
aliyun ecs DescribeInstances \
  --output 'cols=InstanceId,InstanceName,Status' 'rows=Instances.Instance[]'
```
Or simply omit `rows=` and use the default JSON output when tabular formatting isn't critical.

## Common Workflow Pattern

When the user asks to perform an operation on a named resource (e.g., "restart my server called web-prod"):

1. **Discover** — Run a Describe command to find the resource ID
   ```bash
   aliyun ecs DescribeInstances --RegionId cn-hangzhou
   ```
2. **Confirm** — Show the result and confirm the target with the user if there's any ambiguity
3. **Act** — Run the mutating command with the confirmed resource ID
4. **Verify** — Optionally run another Describe to confirm the new state

## Error Handling

Common errors and what to do:

| Error | Cause | Solution |
|-------|-------|----------|
| `InvalidAccessKeyId` | Wrong or expired credentials | Run `aliyun configure` to reconfigure |
| `Forbidden.RAM` | Insufficient RAM permissions | Check RAM policy for required action |
| `IncorrectInstanceStatus` | Wrong instance state for operation | Describe instance status first |
| `InvalidRegionId` | Unsupported region for this product | Check product availability in that region |
| `Throttling` | API rate limit hit | Add a brief delay and retry |

If the user has not yet installed or configured the CLI, read `references/setup.md` and guide them
through it before attempting any commands.

## Safety Guidelines

- For **destructive operations** (delete instance, release EIP, drop RDS database), always:
  1. Show the user what will be deleted with a Describe command first
  2. Explicitly ask for confirmation before running the delete command
- For **cost-incurring operations** (create ECS, purchase bandwidth), mention the cost implications
- Never expose or log AccessKey secrets — remind users to use RAM roles or environment variables
  instead of hardcoding credentials

## Parallelism

When the user needs to operate on multiple resources (e.g., "list all instances in all regions"),
you can run several commands and combine the results. For shell loops:

```bash
for region in cn-hangzhou cn-beijing cn-shanghai cn-shenzhen ap-southeast-1; do
  echo "=== $region ==="
  aliyun ecs DescribeInstances --RegionId $region
done
```
