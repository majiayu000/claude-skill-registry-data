---
name: supply-chain-review
description: "Reviews lockfiles, installers, provenance, CI permissions, dependency confusion, artifacts, registries, and publishing."
---

# Supply Chain Review

Review how code and dependencies enter the build.

## Workflow

1. Inspect package manifests, lockfiles, CI workflows, release scripts, and
   build/publish configuration.
2. Identify install-time execution, unpinned sources, registry drift, generated
   artifacts, and privileged tokens.
3. Check whether changes widen permissions or provenance risk.
4. Recommend minimal hardening and validation.

## Output

- supply-chain surfaces
- risky changes or defaults
- affected workflow
- evidence
- remediation
- validation gaps

## Rule

Do not upgrade or rewrite the build unless the user asks for implementation.
Review first, then patch only when scoped.
