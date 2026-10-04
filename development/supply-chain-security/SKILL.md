---
id: supply-chain-security
version: "2.0.0"
title: "Supply Chain Security"
description: "Vet dependencies before they enter the build: typosquats, dependency confusion, malicious packages, known vulnerabilities, unlocked resolution, risky install and build hooks, EOL embedded runtimes, and the authenticity and freshness of your own release channel. Use when adding or upgrading a dependency, reviewing package manifests or lockfiles, configuring package sources or internal namespaces, or publishing a package or application update."
category: supply-chain
severity: critical
applies_to:
  - "when adding or upgrading a dependency"
  - "when reviewing PRs that modify package manifests or lockfiles"
  - "when configuring package sources, registries, or internal namespaces"
  - "when shipping an embedded runtime (Electron, CEF, a bundled JRE)"
  - "before publishing a package or an application update"
languages: ["*"]
token_budget:
  minimal: 1050
  compact: 1600
  full: 2000
rules_path: "rules/"
tests_path: "tests/"
related_skills: ["secret-detection", "container-security", "cicd-security"]
last_updated: "2026-08-12"
sources:
  - "Alex Birsan, Dependency Confusion (2021)"
  - "OpenSSF Best Practices for OSS Developers"
  - "SLSA Supply-chain Levels for Software Artifacts v1.0"
  - "The Update Framework (TUF) specification"
  - "OWASP Top 10 2021 — A06: Vulnerable and Outdated Components"
  - "CWE-1104: Use of Unmaintained Third Party Components"
---

# Supply Chain Security

## Rules (for AI agents)

### ALWAYS
- Verify the identity of a new dependency before adding it: registry metadata,
  repository URL, maintainer set, and provenance checked against the signer you
  *expect*. Name-similarity screening opens the question; it never answers it.
- Query the bundled malicious-package data before adding any dependency —
  `check_dependency`, `check_typosquat` and `lookup_vulnerability` read it, this file
  cannot. Match on ecosystem, normalized name **and affected version range**; an
  active match on the resolved version blocks.
- Treat package age, download volume, maintainer count and activity as risk signals,
  never as proof of trust. Defaults: a verified maintainer signal within 90 days of a
  package identity's first publication, plus a documented reason within 30 days.
- Lock the resolution graph for anything you deploy — commit the lockfile, install
  frozen in CI (`npm ci`, `--frozen-lockfile`, `pip --require-hashes`,
  `cargo --locked`). Lock what you deploy, range what you publish: a library's
  dependency metadata needs compatibility ranges.
- Restrict where packages resolve from, so an internal-only identifier cannot come
  from a public registry. Use the ecosystem's own mechanism — npm scope-to-registry,
  Gradle `exclusiveContent`, a single authoritative index for Python, which has no
  scope isolation at all.
- Treat install and build hooks (`postinstall`, `setup.py` and modern build backends,
  `build.rs`) as arbitrary code execution. Review them, and run dependency builds in
  an isolated least-privileged builder — most ecosystems ship no install sandbox.
- Triage vulnerabilities on severity, exploitability, deployment context, reachability
  where the tooling genuinely supports it, and fix availability **together**. A
  material vulnerability with no published fix needs mitigation or a recorded risk
  acceptance, not a pass.
- Never carry reachability or dev-only reasoning across to a suspected malicious
  package or build-time compromise. A hostile `postinstall` already ran in your build
  environment with your CI credentials, whatever production imports.
- Surface trust-boundary changes on any update regardless of version number: a
  maintainer or ownership change, a new or changed install hook, a source transition,
  a provenance regression. `cicd-security` owns the approval policy that acts on it.
- Track bundled runtimes and engines (Electron, CEF, Chromium, system WebView, a JRE)
  against upstream support windows and advisories directly. Wrapper-package scanners
  match the wrapper version and can report clean while the engine is unpatched.
- Protect your own release channel: restrict publish privileges, verify updates
  against a trusted signing identity or update framework, and reject stale or
  downgraded releases. A checksum served beside the artifact is not authentication.

### NEVER
- Bypass the ecosystem's artifact-integrity verification. Disabling audit
  (`npm config set audit false`) or reproducibility (`--no-package-lock`) is neither.
- Use unfrozen resolution in CI or production when the project has a committed
  lockfile.
- Let an internal-only package identifier resolve from an untrusted public source.
- Treat popularity, package age, name similarity, or the mere presence of a signature
  as sufficient evidence that a dependency is trustworthy.
- Execute unreviewed dependency install or build hooks in a privileged build
  environment.
- Ship an unsupported or known-unpatched embedded runtime.
- Allow broadly authorized release publishing, or execute an update that has not
  passed authenticity and freshness checks.

### KNOWN FALSE POSITIVES
- Maintained forks with distinct names, once repository and maintainer identity are
  verified.
- A new release of an established package is not a newly created package identity.
- Internal packages absent from public registries, where the organization controls
  source routing.
- Audited build hooks executed in an isolated, least-privileged builder.
- A supported and patched embedded runtime, bundled deliberately.
- Verified auto-update: the finding is an unauthenticated, stale, downgradeable or
  otherwise untrusted update path, not the presence of auto-update.

## Context (for humans)

Two distinctions carry most of the weight. A **vulnerable** dependency and a
**compromised** one are triaged differently: reachability, dev-only scoping and fix
availability all inform the first and none of them apply to the second, because a
hostile install hook has already run. And **hashing** an artifact is not
**authenticating** it — a checksum beside the file proves only that it arrived
intact, while a signature checked against a key you already trust proves who produced
it. The same model governs the software you ship: an update channel needs
authenticity, freshness and rollback protection, not just a digest.

AI tools are especially exposed here. They generate plausible package names without
checking which exist, and they cannot see when a package was compromised — a model
recommends what it learned in training, so a maintainer compromised after the cutoff
still gets recommended. That is why the malicious-package lookup is an explicit tool
call, not something the model is expected to know.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it;
  screening heuristics and their limits, provenance and expected-signer verification,
  reachability tooling caveats, checksum versus signature, freshness and rollback
- `references/ecosystem-controls.md` — source routing and resolution locking per
  ecosystem, why Go is not lockfile-shaped, and the three controls people conflate
- `rules/typosquat_patterns.json`
- `rules/dependency_confusion.json`
- `rules/known_malicious.json` — pointer to the relevant
  `vulnerabilities/supply-chain/malicious-packages/*.json` data
- [Alex Birsan's original dependency confusion writeup](https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610).
- [SLSA](https://slsa.dev/).
- [The Update Framework](https://theupdateframework.io/docs/metadata/) — signed metadata, rollback and freshness protection.
- [OWASP Top 10 A06](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/).
