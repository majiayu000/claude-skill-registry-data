---
name: supply-chain-review
description: Review agent skill supply-chain risk. Use when Codex is asked to inspect third-party skill sources, dependencies, install commands, package managers, remote downloads, version pins, provenance, or update risks before installation or publication.
license: MIT
---

# Supply Chain Review

## Core Workflow

1. Identify the source, publisher, version, commit, license, install path, and
   update mechanism.
2. Review dependencies, package managers, install commands, remote downloads,
   generated code, and executable artifacts.
3. Check whether versions and sources are pinned, inspectable, and reproducible.
4. Look for typosquatting, untrusted domains, opaque binaries, install hooks,
   telemetry surprises, or broad permissions.
5. Recommend pinning, vendoring, removal, manual review, or blocked install.
6. Record approval conditions and re-review triggers.

## Safety Rules

- Do not install or execute third-party packages just to inspect them.
- Do not trust stars, downloads, or marketplace position as safety proof.
- Do not approve remote script execution without source review and a clear
  rollback path.

## Deliverable Shape

For supply-chain reviews, provide:

- Source and provenance
- Dependencies and install path
- Pinning and reproducibility notes
- Suspicious or opaque components
- License and update concerns
- Approval conditions
- Safe install recommendation

## References

- Read `references/supply-chain-review-checklist.md` when reviewing third-party
  skill sources, dependencies, or install steps.
