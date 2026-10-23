---
name: dependency-review
description: Review dependency necessity, identity, provenance, and reproducibility without modifying them. Use when manifests, lockfiles, vendor state, generated dependency state, registries, fetched tools, or version pins change.
---

# Dependency Review

Show that each changed dependency is needed, is the intended project, and resolves the same way on every build.

## Workflow

1. Identify the changed dependency surface, the comparison target, the repository's pinning policy, and its usual update path.
2. For each added, removed, or changed dependency or tool, name its consumer and the current need. A dependency that a few lines of code or an existing dependency could replace is a finding.
3. Confirm the identity of each new package: the exact name matches the intended project, its source repository and publisher are the expected ones, and it is not a near-miss of a popular name. Code models invent plausible package names, so a name that appears in no registry, or that a different publisher owns, is a blocking finding.
4. Check maintenance and license: the project is not archived or deprecated, and its license is compatible with the repository's license and policy.
5. Check that manifests, lockfiles, vendored code, checksums, and generated state agree, without normalizing unrelated content. Flag floating versions, Git or URL sources, fetched installers, lifecycle scripts, and pins that differ from how the repository pins other dependencies.
6. Run the repository's configured audit command, such as `npm audit`, `pip-audit`, `govulncheck`, or `cargo audit`, when one exists. Read-only registry and advisory queries are fine when the host allows network access. Never install packages, run lifecycle scripts, regenerate lockfiles, or change caches without explicit authority.
7. Delegate exploitability and credentials to `security-review`, CI machinery to `ci-review`, infrastructure impact to `infra-review`, and runtime compatibility to `rollout-readiness-review`.

Do not upgrade unrelated dependencies, churn an entire lockfile, recommend new scanners, or trust committed generated code without checking its source.

## Result

Report each finding with its location, the affected contract, the evidence, the consequence, the smallest correction, how to verify it, and the uncertainty. State directly when no actionable finding exists. When tooling or provenance data is unavailable, report the result as inconclusive with the missing evidence. Finish when every changed dependency is accounted for.
