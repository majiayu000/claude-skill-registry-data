---
name: working-with-provenance
description: Use when tracing Konflux builds from image references, finding build logs from artifacts, or verifying source commits for container images - extracts provenance attestations to navigate from images back to builds and source code
allowed-tools: Bash(cosign download:*), Bash(cosign verify:*), Bash(jq:*), Bash(~/.claude/skills/working-with-provenance/scripts/*:*)
---

# Working with Provenance

## Overview

Every Konflux build produces SLSA provenance attestations containing the complete build history: source repository, commit SHA, pipeline run URL, and build parameters. Use `cosign download attestation` with `jq` to extract this information and trace artifacts back to their origins.

## When to Use

Use this skill when you need to:
- Find build logs for an image (missing SBOM, failed tasks, debugging)
- Trace an image back to its source commit (what changed, code review)
- Verify which repository and commit produced an artifact (security, compliance)
- Extract build parameters or pipeline information (reproduce builds, debug configuration)

Do NOT use for non-Konflux images (Docker Hub, upstream images without attestations).

## Quick Reference

| Need | Command Pattern | Helper Script |
|------|----------------|---------------|
| Build log URL | `cosign download attestation $IMAGE \| jq '.payload \| @base64d \| fromjson \| .predicate.buildConfig.tasks[0].invocation.environment.annotations."pipelinesascode.tekton.dev/log-url"'` | `~/.claude/skills/working-with-provenance/scripts/build-log-link.sh $IMAGE` |
| Commit link | `cosign download attestation $IMAGE \| jq '.payload \| @base64d \| fromjson \| .predicate.buildConfig.tasks[0].invocation.environment.annotations \| ."pipelinesascode.tekton.dev/repo-url" + "/commit/" + ."pipelinesascode.tekton.dev/sha"'` | `~/.claude/skills/working-with-provenance/scripts/build-commit-link.sh $IMAGE` |
| Git repository | `cosign download attestation $IMAGE \| jq '.payload \| @base64d \| fromjson \| .predicate.buildConfig.tasks[0].invocation.environment.annotations."pipelinesascode.tekton.dev/repo-url"'` | `~/.claude/skills/working-with-provenance/scripts/build-git-repo.sh $IMAGE` |
| Origin pullspec | `cosign download attestation $IMAGE \| jq '.payload \| @base64d \| fromjson \| .subject[0].name + ":" + .predicate.buildConfig.tasks[0].invocation.environment.annotations."pipelinesascode.tekton.dev/sha"'` | `~/.claude/skills/working-with-provenance/scripts/build-origin-pullspec.sh $IMAGE` |

## Helper Scripts

This skill includes ready-to-use bash scripts that you can invoke directly:

```bash
# Extract build log URL
~/.claude/skills/working-with-provenance/scripts/build-log-link.sh quay.io/org/image:tag

# Extract commit URL (handles GitHub and GitLab)
~/.claude/skills/working-with-provenance/scripts/build-commit-link.sh quay.io/org/image:tag

# Extract git repository URL
~/.claude/skills/working-with-provenance/scripts/build-git-repo.sh quay.io/org/image:tag

# Extract original pullspec with commit SHA
~/.claude/skills/working-with-provenance/scripts/build-origin-pullspec.sh quay.io/org/image:tag
```

## Common Workflow

**Investigating missing SBOM:**

```bash
# 1. Get build log URL from provenance
LOG_URL=$(~/.claude/skills/working-with-provenance/scripts/build-log-link.sh quay.io/org/image:tag)

# 2. Open logs in browser or use debugging-pipeline-failures skill
echo $LOG_URL
```

**Tracing code changes:**

```bash
# 1. Get commit link from provenance
COMMIT=$(~/.claude/skills/working-with-provenance/scripts/build-commit-link.sh quay.io/org/image:tag)

# 2. View the commit
echo $COMMIT  # Opens in browser

# 3. Check recent history
git clone $(~/.claude/skills/working-with-provenance/scripts/build-git-repo.sh quay.io/org/image:tag)
```

## Attestation Structure

Konflux provenance lives at:
```
.payload (base64-encoded)
  └─ .predicate
       ├─ .buildConfig.tasks[0].invocation.environment.annotations
       │    ├─ pipelinesascode.tekton.dev/log-url      (pipeline logs)
       │    ├─ pipelinesascode.tekton.dev/repo-url     (git repository)
       │    └─ pipelinesascode.tekton.dev/sha          (commit SHA)
       └─ .subject[0].name                              (image name)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trying to parse image tags for commit info | Tags can be arbitrary. Use provenance for definitive source. |
| Manual UI navigation to find logs | Use `build-log-link.sh` - faster and scriptable. |
| Assuming images without Konflux builds have provenance | Only Konflux-built images have SLSA attestations via Tekton Chains. |
| Forgetting to base64 decode payload | Always use `.payload \| @base64d \| fromjson` pattern. |

## Real-World Example

```bash
# User reports: "Build quay.io/redhat-user-workloads/konflux-ai-sig-tenant/llm-compressor-demo:7f9a553... missing SBOM"

# 1. Extract build log URL
$ ~/.claude/skills/working-with-provenance/scripts/build-log-link.sh quay.io/redhat-user-workloads/konflux-ai-sig-tenant/llm-compressor-demo:7f9a553dd100ba700fc8f9da942f8dfcecf6a1bd
https://konflux-ui.apps.kflux-prd-rh03.nnv1.p1.openshiftapps.com/ns/konflux-ai-sig-tenant/pipelinerun/llm-compressor-on-push-lvnc5

# 2. Extract source commit
$ ~/.claude/skills/working-with-provenance/scripts/build-commit-link.sh quay.io/redhat-user-workloads/konflux-ai-sig-tenant/llm-compressor-demo:7f9a553dd100ba700fc8f9da942f8dfcecf6a1bd
🐙 https://github.com/ralphbean/llm-compressor-hermetic-demo/commit/7f9a553dd100ba700fc8f9da942f8dfcecf6a1bd

# Now: Open logs to debug SBOM task, review commit for context
```

## Keywords

SLSA provenance, attestation, cosign, Tekton Chains, build logs, commit SHA, source tracing, artifact metadata, supply chain security, SBOM debugging, pipeline logs, container image verification
