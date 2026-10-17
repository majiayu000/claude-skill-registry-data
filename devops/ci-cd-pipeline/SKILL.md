---
name: ci-cd-pipeline
description: Build CI/CD that earns its keep — fail-fast stages, caching, gated releases, artifact provenance, minutes budget aware.
version: 1
triggers: ci, cd, pipeline, github actions, continuous integration, deployment pipeline
category: Engineering & code
blurb: Build CI/CD that earns its keep — fail-fast stages, caching, gated releases and artifact provenance.
archetype: knowledge
example: Design a CI pipeline that fails fast and stays cheap.
---

# CI/CD Pipeline — the DevOps seat

Automate the path from commit to artifact, with gates that catch real problems. Pipelines are the primary green gate; humans approve deploys.

## When to use
- New repo setup; changing build/test/deploy workflows.
- Builds are slow, flaky, or missing gates.
- Adding release automation or artifact provenance.

## Method
1. **Stages**: lint → typecheck → test → build → package/sign → publish. Cheapest first; fail fast.
2. **Determinism**: lockfile-enforced installs (`frozen-lockfile`), pinned tool versions, byte-exact checkouts where hashes matter.
3. **Caching**: dependency and build caches keyed on lockfiles; never cache secrets or test fixtures.
4. **Secrets in CI**: from the secret store only; masked in logs; never in artifacts; scrub error output.
5. **Budget awareness**: keep workflows minimal where minutes are constrained; heavy builds run on owned hardware; don't add pipelines that duplicate the primary gate.
6. **Provenance**: publish artifacts with checksums; sign releases (`secure-build-pattern`); keep build outputs plus manifest hashes.
7. **Deploys**: HITL approval; always a rollback path; never direct-to-prod from a laptop.

## Artifacts
- Pipeline configs, gate reports, artifact checksums/manifests, release records.

## Quality gates
- [ ] Pipeline fails fast and reports the first real cause.
- [ ] Same commit ⇒ same artifact (deterministic).
- [ ] Release artifacts carry hash + signature.
- [ ] No secret ever appears in logs or artifacts.

## Red lines
- No disabling gates to unblock a merge (fix it, or consciously override and log why).
- No unpinned third-party actions; pin versions.

## Related
`testing-strategy` (what runs) · `release-management` (what ships) · `dependency-governance` (what enters).
