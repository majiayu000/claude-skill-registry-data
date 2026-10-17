---
name: platform-engineering
description: >-
  Expertise on the CI/CD pipeline, remote builds using Argo Workflows, Kaniko, and GitHub Actions in the ARM64 K3s cluster.
---

# Platform Engineering & CI/CD Pipeline

## Overview
This skill documents the CI/CD and Remote Build pipelines used in this K3s cluster. Building heavy images (like AI agents and Python ecosystems) on ARM64 nodes (CM4 and RK1) can cause high resource contention (OOMKill) and take a long time. 
To solve this, the cluster implements a hybrid approach: **Local Builds (Kaniko + Argo)** by default, and **Remote Builds (GitHub Actions + Skopeo Sync)** for heavy lifting.

## Remote Build Pipeline (Argo + GitHub Actions)

We use a generic Ansible role called `run-remote-build` that orchestrates the following:
1. **GitHub CLI Auth:** The `Makefile` extracts your `gh auth token` and injects it into Ansible as `GITHUB_PAT`.
2. **Argo Workflow:** Ansible creates an Argo Workflow (`build-{{ remote_app_name }}-remote`) in the `kaniko` namespace.
3. **Trigger:** A container inside the workflow runs `gh workflow run` to trigger the remote compilation on GitHub Actions' powerful servers.
4. **Monitor:** It watches the run using `gh run watch`.
5. **Skopeo Sync:** Once the GitHub Action completes and pushes to `ghcr.io`, the next Argo step uses Skopeo to download the image directly into the local registry (`registry.registry:5000`).
6. **Tagging:** To ensure the local cluster doesn't accidentally use the untested remote image, Skopeo appends the `-remote` suffix to the image tag (e.g. `v2026.5.16-telegram-remote`).

## Available Makefile Commands

You can build all configured remote images by running:
```bash
make build-remote-all
```

Or trigger individual builds:
```bash
make build-remote-hermes
make build-remote-leloir
make build-remote-nas
```

## How to add a new Remote Build

To add a new application to the remote build pipeline:
1. **Create the GitHub Action:** Add `.github/workflows/build-<app>.yml` using `workflow_dispatch` with inputs `git_ref` and `image_tag`.
2. **Update bootstrap.yml:** Add a task calling `run-remote-build` specifying `remote_app_name`, `remote_github_workflow`, `remote_ghcr_image`, etc.
3. **Update Makefile:** Add a `build-remote-<app>` target and include it in `build-remote-all`.
