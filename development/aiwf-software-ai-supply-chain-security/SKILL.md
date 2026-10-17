---
name: aiwf-software-ai-supply-chain-security
description: Use for dependency, package, lockfile, SBOM, CI/CD, build provenance, signing, release, container, compiler, CUDA/NVIDIA binary, model, dataset, adapter, extension, and AI artifact supply-chain security.
---

# AIWF Software And AI Supply-Chain Security

## Core Rule

Track an artifact from authoritative source through pinned identity, transport, verification, build or load, distribution, update, and retirement. A familiar filename or repository name is not provenance.

## Workflow

1. Inventory ecosystems, manifests, lockfiles, registries, build images, CI actions, release jobs, binary downloads, models, datasets, adapters, and extensions.
2. Record publisher, canonical URL, version/revision, license, hash/signature/attestation, build context, execution behavior, owner, and update policy.
3. Prefer lockfiles, immutable revisions, official registries, minimal permissions, isolated builds, reproducible steps, and reviewed release identities.
4. Generate or consume ecosystem-standard SBOM/provenance formats with established tools; do not invent a private format as a substitute.
5. Match advisories to the installed artifact and reachable behavior. Distinguish affected, potentially affected, not affected, and unverified.
6. Treat model weights, unsafe serialization, custom model code, notebooks, install scripts, containers, and GPU binaries as executable supply chain where applicable.
7. Validate upgrade/removal in a disposable environment and preserve rollback.

Read `references/source-register.json` before tool, format, advisory, or standard-version claims.

## Hard Gates

- Explicit approval is required before dependency upgrades, registry changes, key/signature changes, CI permission changes, artifact deletion, or running untrusted code.
- Do not download or load unknown models, datasets, extensions, wheels, containers, or installers merely to inspect them.
- Never mark an advisory resolved from a version string alone when backports, forks, or reachability are unclear.
- Add `aiwf-nvidia-cuda-cudnn-sdk` for compatibility and `aiwf-incident-response-recovery` for suspected compromise.

## Output

Return artifact inventory, provenance gaps, advisory evidence, prioritized remediation, compatibility/rollback risks, and release verification steps.
