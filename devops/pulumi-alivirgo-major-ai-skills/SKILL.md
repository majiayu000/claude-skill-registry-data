---
name: pulumi
description: "Manage Pulumi stacks, providers, secrets, and infrastructure previews before applying reviewed changes."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["pulumi", "iac", "stacks", "typescript", "python", "cloud", "devops"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Pulumi Infrastructure as Code AI Skill Guide

## Overview

Pulumi expresses cloud infrastructure as real programs (TypeScript, Python, Go, C#, YAML). State lives in a **backend** (Pulumi Cloud or self-managed); each **stack** is an isolated deployment of the same program (e.g. `dev`, `prod`). Agents should treat `pulumi preview` as mandatory before `up`, and treat stack secrets as first-class - plaintext config for credentials is a defect.

```
Program (index.ts / __main__.py)
        |
        v
+----------------+     preview/up      +------------------+
| Stack config   | ------------------> | Cloud providers  |
| + secrets      | <------------------ | AWS/GCP/Azure/k8s|
+----------------+     state refresh   +------------------+
```

## When to use

- Creating or reviewing Pulumi projects and stack configs
- Previewing diffs before applying infrastructure changes
- Managing stack secrets, provider credentials, and resource imports
- Migrating imperative cloud CLI scripts into durable IaC

## Operational directives

1. Always `pulumi stack select` (or pass `-s`) before mutating; confirm with `pulumi whoami -v`.
2. Run `pulumi preview` and summarize create/update/replace/delete counts before `pulumi up`.
3. Store secrets with `pulumi config set --secret`; never commit decrypted values.
4. Prefer immutable replaces carefully - call out replacements that destroy data (DBs, disks).
5. Use resource options (`protect`, `retainOnDelete`, aliases) for production stateful resources.

## Concrete examples

### Project bootstrap (TypeScript)

```bash
pulumi new aws-typescript -y -n api-infra -s dev
pulumi config set aws:region us-east-1
pulumi config set --secret dbPassword '***'
pulumi preview
pulumi up --yes
```

### Minimal program sketch

```typescript
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.BucketV2("assets", {
  tags: { service: "api", env: pulumi.getStack() },
});

export const bucketName = bucket.id;
```

### Stack operations

```bash
pulumi stack ls
pulumi stack output --json
pulumi refresh --yes
pulumi destroy --yes   # only with explicit user approval
```

### Import existing resource

```bash
pulumi import aws:s3/bucketV2:BucketV2 assets my-existing-bucket-name
```

## Change-risk table

| Diff type | Risk | Agent action |
| :--- | :--- | :--- |
| Create | Low-Medium | Confirm naming/tags/region |
| Update in-place | Medium | Check security group / IAM blast radius |
| Replace | High | Call out downtime and data loss |
| Delete | High | Require explicit user confirmation |

## Best practices

1. One stack per environment; share code via Component Resources, not copy-paste.
2. Enable policy packs / CI previews on PRs; block merge on unexpected deletes.
3. Pin provider plugin versions in CI for reproducible plans.
4. Use `protect: true` on production databases and critical DNS zones.

## Limitations

- Preview is not a guarantee against provider eventual-consistency races.
- Large monorepos may need automation API or ESC for secrets at scale.
- Cross-cloud programs still need correct provider credentials per stack.

## Related skills

- `gcloud-cli` / `azure-cli` - imperative ops and auth debugging beside Pulumi
- `packer` - image baking referenced by compute resources
- `kubernetes` - Pulumi k8s provider workloads
- `vault` - external secret backends integrated with stacks
