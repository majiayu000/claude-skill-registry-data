---
name: llm-supply-chain
description: Detects compromised or backdoored models loaded from unverified sources,
  floating tags, or unreviewed registries. Use when writing code that
  downloads pre-trained models, loads models from registries or file paths,
  integrates third-party LLM providers, or manages model version selection.
  Also invoke when setting up automated model updates.
---

# LLM Supply Chain Security Check (OWASP LLM05:2025)

## What this checks

Protects against compromised or backdoored models introduced through unverified
downloads, floating version tags, or unreviewed third-party providers. A tampered
model weight file or a silently swapped `latest` tag can introduce persistent
backdoors that survive retraining.

## Vulnerable patterns

- Model artifact downloaded from an arbitrary host or URL with no checksum or signature verification
- Model identifier that uses a floating tag (`latest`, `main`, a mutable branch) instead of an exact pinned revision
- Third-party model integrated with no review of model card, license, or provenance
- Automated model-update job in CI that bumps revisions without a human approval gate

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Model revisions are pinned to an exact commit SHA or content digest**, never a
   mutable name like `main` or `latest`. A floating tag lets the registry (or a
   registry compromise) silently swap what you load on the next pull — including
   backdoored weights that look identical by name.
2. **Weight files are checksum-verified after download.** A cryptographic digest
   (SHA-256 or stronger) of the expected bytes is pinned in version control; the
   loader computes the digest on the downloaded file and refuses to use it on
   mismatch. Pinning the revision alone does not help if the artifact is served
   from a compromised CDN.
3. **Model source is validated against an allowlist of approved organizations or
   registries** before download begins. A wildcard organization field is the
   supply-chain equivalent of accepting any author.
4. **Automated model updates have a human approval gate.** A CI job that bumps a
   pinned revision without review is a backdoor delivery channel; rotate revisions
   through PRs with signed artifacts reviewed by a human.

Translate these principles to the loader API, registry client, and CI system of the
audited file. Use the SDK's documented pinning and verification mechanisms — do not
implement ad-hoc checks.

## Verification

Confirm the response:

- [ ] Model IDs specify an exact commit SHA revision, not `"main"` or `"latest"`
- [ ] SHA-256 checksums for model weight files are pinned in version control and verified post-download
- [ ] Model source organization is validated against an approved allowlist

## References

- CWE-1395 ([Dependency on Vulnerable Third-Party Component](https://cwe.mitre.org/data/definitions/1395.html))
- CWE-494 ([Download of Code Without Integrity Check](https://cwe.mitre.org/data/definitions/494.html))
- [OWASP LLM05:2025 Supply Chain Vulnerabilities](https://genai.owasp.org/llmrisk/llm05-supply-chain-vulnerabilities/)
