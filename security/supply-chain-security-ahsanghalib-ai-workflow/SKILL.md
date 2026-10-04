---
name: supply-chain-security
description: >-
  Use when reviewing dependencies, lockfiles, package manifests, install
  scripts, CI actions, plugins, build inputs, SBOMs, artifact provenance,
  signatures, or release supply-chain risk. Do not use for live host or
  container vulnerability scanning, registry takedown, package publishing,
  deployment, or automatic dependency upgrades.
license: Apache-2.0
metadata:
  source: mukul975/Anthropic-Cybersecurity-Skills
  source_revision: 54a7988
  source_url: https://github.com/mukul975/Anthropic-Cybersecurity-Skills
  compatibility: harness-neutral; opt-in defensive review; no runtime dependencies
---

# Supply-Chain Security

Assess whether software inputs can be identified, reproduced, reviewed, and
trusted through development, CI, packaging, and release. This skill
specializes the dependency and integration boundary in
`security-and-hardening`; it does not replace that skill's general secret,
authorization, URL, file, command, or approval controls.

## Safety boundary

- Review only repositories, artifacts, registries, and CI systems the user is
  authorized to inspect. Default to read-only local evidence.
- Do not install packages, execute lifecycle hooks, run untrusted build steps,
  download arbitrary artifacts, publish packages, alter registry policy,
  deploy, rotate signing keys, or change lockfiles without explicit approval
  for the exact action.
- Never request, print, copy, or embed registry credentials, signing keys,
  OIDC tokens, CI secrets, or private package contents.
- Do not treat a package name, checksum, SBOM, signature, or vulnerability
  scanner result as proof of trust without checking its scope, provenance,
  freshness, and verification chain.
- Stop and report when a check requires network access, a missing tool, a
  private registry, a protected key, or a live environment.

## Review workflow

### 1. Inventory the supply chain

Identify package manifests and lockfiles, registries and mirrors, direct and
transitive dependencies, plugins/actions, install and build hooks, generated
code, base images, SBOMs, artifact stores, release workflows, signing or
attestation metadata, and deployment consumers.

Record the inspected revision, package-manager/runtime versions, configured
sources, and whether each item is observed, inferred, proposed, stale, or
unknown. Keep local source evidence separate from registry or provider claims.

### 2. Trace trust and provenance

Check the controls relevant to the project:

- lockfile integrity, exact or bounded versions, dependency source and
  resolution order, transitive dependency visibility, and review of lifecycle
  scripts;
- repository, maintainer, release, and artifact provenance; package-name
  similarity and dependency-confusion indicators; ownership and namespace
  controls;
- CI action and plugin pinning, workflow permissions, secret exposure, pull
  request boundaries, untrusted fork behavior, and artifact handoff between
  jobs;
- SBOM format, completeness, component identifiers, dependency relationships,
  license/provenance fields, generation revision, and vulnerability data
  freshness;
- digest pinning, signature identity and issuer, transparency or attestation
  evidence, reproducible-build claims, and the policy that consumes them.

Name uncertainty explicitly. A vulnerability match is not automatically
reachable or exploitable, and a signature verifies an identity claim only when
the expected identity, issuer, digest, and policy are all checked.

### 3. Use safe local evidence

Prefer repository-local manifests, lockfiles, workflow definitions, existing
SBOMs, checksums, and documented validation commands. Run only read-only or
already-approved checks. Do not silently substitute a networked package audit,
registry lookup, dependency installation, build, or signing operation when the
required capability is absent.

For an SBOM, validate its format and component/dependency relationships before
correlating findings. For signatures or attestations, verify the artifact
digest and the expected identity/issuer using an already available approved
tool; never broaden identity matching to make verification pass.

### 4. Report and recommend

Rank findings by affected artifact, trust boundary, exploitability evidence,
blast radius, freshness, and remediation confidence. Distinguish:

- confirmed local evidence;
- provider or registry evidence and its retrieval date;
- plausible indicators requiring manual review;
- blocked, stale, or unverified checks.

Recommend the smallest reversible remediation: pin or replace a dependency,
constrain a source, remove an unnecessary hook, reduce CI permissions, require
artifact verification, regenerate an incomplete SBOM, or add a review gate.
Do not apply it automatically.

## Output contract

```markdown
## Scope, Revision, and Evidence Sources

## Supply-Chain Inventory and Trust Boundaries

## Controls Checked

## Findings and Confidence

## Blocked or Unverified Checks

## Approval-Gated Remediation

## Residual Risk and Recommended Next Step
```

Include exact file paths, artifact identifiers, versions/digests, commands
actually run, and retrieval dates where applicable. Redact secrets and avoid
including full sensitive manifests or provider responses in the report.

## Upstream basis

Adapted for this harness-agnostic repository from the defensive concepts in
[mukul975/Anthropic-Cybersecurity-Skills SBOM analysis](https://github.com/mukul975/Anthropic-Cybersecurity-Skills/tree/54a798831d2266a3ca61ce68a7acb80b81160d57/skills/analyzing-sbom-for-supply-chain-vulnerabilities),
[Sigstore signing](https://github.com/mukul975/Anthropic-Cybersecurity-Skills/tree/54a798831d2266a3ca61ce68a7acb80b81160d57/skills/implementing-sigstore-for-software-signing),
and the package-registry review concepts in the same Apache-2.0 collection. The
local entrypoint intentionally omits upstream install, registry, signing,
deployment, and network automation.
