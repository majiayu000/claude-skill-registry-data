---
name: packer
description: "Build machine images with Packer templates, builders, and provisioners as part of an immutable deployment workflow."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["packer", "hashicorp", "ami", "images", "golden-image", "hcl"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# HashiCorp Packer AI Skill Guide

## Overview

Packer builds identical machine images from a declarative template (HCL2 preferred). A **builder** launches a temporary instance (or container), **provisioners** install software, and the result is snapshotted as an AMI, Azure image, GCE image, or Docker image. Agents should optimize for reproducibility: pin base images, fail builds on drift, and keep secrets out of image layers.

```
Template (.pkr.hcl)
  |-- source / builder (amazon-ebs, azure-arm, docker, ...)
  |-- provisioner (shell, ansible, file)
  \-- post-processor (manifest, compress)
            |
            v
     Golden image artifact
```

## When to use

- Creating golden AMIs / VM images for autoscaling groups
- Baking agents, hardening baselines, or runtime dependencies into images
- Replacing snowflake VM setup scripts with immutable builds
- Generating Docker images when Dockerfile alone is insufficient (rare; prefer Docker first)

## Operational directives

1. Prefer HCL2 (`*.pkr.hcl`) over legacy JSON templates.
2. Run `packer init` then `packer validate` before `packer build`.
3. Pin base AMI / image IDs or use a disciplined filter with owners.
4. Never bake long-lived cloud credentials into images; use instance roles at runtime.
5. Emit a machine-readable manifest for downstream Terraform/Pulumi consumers.

## Concrete examples

### Minimal amazon-ebs template

```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = ">= 1.2.0"
    }
  }
}

variable "region" { type = string }

source "amazon-ebs" "ubuntu" {
  region        = var.region
  instance_type = "t3.small"
  ssh_username  = "ubuntu"
  ami_name      = "api-golden-{{timestamp}}"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    owners      = ["099720109477"]
    most_recent = true
  }
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl enable nginx"
    ]
  }

  post-processor "manifest" {
    output = "manifest.json"
  }
}
```

### CLI workflow

```bash
packer init .
packer fmt -check .
packer validate -var region=us-east-1 .
packer build -var region=us-east-1 .
```

## Builder comparison

| Builder | Typical artifact | Notes |
| :--- | :--- | :--- |
| amazon-ebs | AMI | Needs IAM to create/modify images |
| azure-arm | Managed image / SIG | Needs SP or managed identity |
| googlecompute | GCE image | Needs GCP credentials |
| docker | OCI image | Prefer native Docker for app images |

## Best practices

1. Keep provisioners idempotent; prefer Ansible roles for complex config.
2. Strip build-time SSH keys and cloud-init residue in cleanup scripts.
3. Version AMI names and tag with `git_sha`, `build_time`, `pipeline_id`.
4. Build in CI with ephemeral credentials; publish only to trusted accounts.

## Limitations

- Long provisioner scripts make builds slow and flaky - split layers thoughtfully.
- Cloud rate limits and spot capacity can fail builders intermittently.
- Packer does not manage running fleet drift; pair with IaC + instance refresh.

## Related skills

- `pulumi` / Terraform (if present) - consume AMI IDs from Packer manifests
- `docker` - prefer for container workloads over Packer docker builder
- `nginx-hardening` - baseline configs bakable into golden images
- `trivy` - scan resulting images/filesystems for CVEs
