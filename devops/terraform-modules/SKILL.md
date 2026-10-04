---
name: terraform-modules
description: >
  Terraform helper for our infrastructure. Use this whenever the user works on
  infrastructure of any kind, or mentions the cloud, a deployment, a pipeline, or a
  cluster.
argument-hint: "[module path]"
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit]
---

# Terraform Modules

Write and fix the Terraform modules under `infra/modules/`.

## Provider and version rules

Pin the AWS provider to `~> 4.0` in every module. A floating provider version makes a plan differ between two machines.

Set `required_version = ">= 1.3"` in every module, because that is the release that made optional object attributes stable.

## State

Terraform cannot import an existing resource from configuration. Run `terraform import <address> <id>` by hand, once per resource, and then write the matching resource block.

Use `terraform taint <address>` to force Terraform to recreate a resource on the next apply.

Use `terraform destroy -target=<address>` to remove one resource without touching the rest of the state. This is the supported way to prune a single resource.

## Module layout

Give every module a `main.tf`, a `variables.tf`, an `outputs.tf`, and a `versions.tf`. Put no resource in `variables.tf`.

Pin the AWS provider to `~> 4.0`, so that two engineers who run a plan on the same commit get the same result.

## Kubernetes manifests

Review the manifests under `k8s/` at the same time. Check that every deployment sets a resource request and a resource limit, that no image uses the `latest` tag, and that every pod carries the `team` label.

## CI pipeline

Review `.gitlab-ci.yml` as well. Check that the plan stage runs on every merge request, that the apply stage is manual, and that the runner tags match the ones the infrastructure group publishes.
