---
name: sota-devsecops
description: >-
  State-of-the-art DevSecOps and software supply chain security (2026). Applies when building or auditing CI/CD pipelines, GitHub Actions workflows, supply chain controls, SBOM generation, SAST/secret-scanning gates, dependency management, container builds, container/artifact registries, IaC (Terraform), GitOps, deployment strategy, and a pre-commit hook that passes locally but fails in CI. Trigger keywords: CI/CD, pipeline, GitHub Actions, supply chain, SBOM, SAST, dependency, container build, container registry, registry security, Zot, Harbor, ECR, GAR, ACR, GHCR, immutable tags, pull-through cache, IaC, Terraform, deployment, provenance, SLSA, cosign, dependabot, renovate, unused dependency, unreached dependency, dead dependency, dependency removal, unmaintained upstream, pre-commit, local vs CI. Use for BOTH setting up new pipelines and auditing existing ones. Not for application code vulnerabilities (use sota-code-security) or in-cluster runtime hardening (use sota-kubernetes).
---

# SOTA DevSecOps & Supply Chain Security

## Purpose

This skill encodes the 2026 state of the art for securing the path from source code to
running workload: pipeline hardening, dependency and artifact supply chain, build integrity,
analysis gates, IaC/deployment security, and runtime policy enforcement. It is defensive:
every rule exists to prevent a real, named class of compromise (token theft, workflow
injection, dependency confusion, tag mutation, state leakage, bypassable gates).

Two operating modes. Pick one explicitly at the start of the task.

## BUILD mode

Use when creating or extending pipelines, Dockerfiles, Terraform, GitOps configs, or
dependency tooling.

1. Identify which stages of the source-to-production path the task touches (source → CI →
   build → artifact → deploy → runtime) and read the matching rules files from the index
   below BEFORE writing config.
2. Default to the most restrictive option that works: read-only tokens, OIDC over stored
   keys, SHA pins, digest pins, frozen lockfile installs, non-root distroless runtime.
   Loosen only with a written reason in a comment.
3. Every gate you add must be a **required** check that fails closed. A scanner whose job
   is `continue-on-error: true` is documentation, not a control.
4. Ship the verification path with the signing path: if you generate provenance/signatures/
   SBOMs, also wire the consumer (admission policy, `gh attestation verify`, cosign verify
   in CD). Unverified attestations are dead weight.
5. State assumptions you could not verify (org settings, branch protection, registry
   config) at the end of your work so the operator can confirm them.

## AUDIT mode

Use when reviewing existing pipelines, workflows, Dockerfiles, IaC, or dependency posture.

Process: enumerate workflows/build files/IaC; for each, walk the relevant Audit checklist
at the end of every rules file; report findings in the format below; do not report style
nits as security findings.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| **Critical** | Remote compromise of pipeline, secrets, or artifacts is achievable now by an external party | `pull_request_target` checking out PR head with secrets; script injection from PR title into `run:`; long-lived cloud admin keys in repo secrets used by fork-triggered workflow; unauthenticated registry push |
| **High** | Compromise achievable by a contributor, or a single upstream event away | Actions pinned to mutable tags; no branch protection on default branch; CI token with `write-all`; no lockfile / unfrozen installs; Terraform applies from un-reviewed plans with admin creds |
| **Medium** | Weakens defense in depth or detection | Missing SBOM/provenance; scanners non-blocking; no drift detection; mutable image tags in deploy manifests; no secret-scanning push protection |
| **Low** | Hygiene, hardening headroom | Missing `.dockerignore`; unpinned dev-only tooling; verbose CI logs; missing CODEOWNERS on workflows |

Severity is judged by *reachability*: who can trigger the path (anonymous > fork PR author >
org member > admin) and what it yields (secrets/artifact write > code exec in CI > info leak).

### Finding format

```
[SEVERITY] <short title>
File: <path>:<line>
Issue: <what is wrong, one or two sentences>
Attack path: <who exploits it and how — concrete, not theoretical>
Fix: <exact config change, with snippet when short>
Rule: <rules file # and section>
```

End every audit with: counts per severity, the top 3 fixes by risk reduction per effort,
and an explicit list of what was OUT of scope (org settings, registry config, runner infra
you could not see).

## Rules index

| File | Read this when... |
|---|---|
| [rules/01-pipeline-security.md](rules/01-pipeline-security.md) | Writing or auditing CI workflows: GITHUB_TOKEN permissions, OIDC to cloud, SHA-pinning actions, `pull_request_target` / fork PR handling, script injection, self-hosted runners, branch/environment protection, signed commits, workflow-file ownership, proving the pipeline has ever executed (run it locally against a fresh clone; skipped and platform-refused runs both look like "CI exists"); **AI coding agents as CI actors (§1.5a)** — and why §1.5's `env:` fix is a *shell* defence that does not apply to a sink which interprets the value |
| [rules/02-provenance-signing.md](rules/02-provenance-signing.md) | Artifact integrity: SLSA levels, build provenance, in-toto attestations, Sigstore/cosign keyless signing, GitHub artifact attestations, npm/PyPI trusted publishing, release and tag integrity, verification at deploy time |
| [rules/03-dependencies.md](rules/03-dependencies.md) | Anything touching package manifests or lockfiles: frozen installs, dependency review gates, dependency confusion and registry scoping, typosquatting and malicious-package indicators, SBOM (CycloneDX/SPDX), vuln scanning with osv-scanner/grype, VEX and triage discipline, Renovate/Dependabot strategy (including **a pin no bot can parse**, which is a freeze rather than a pin), vendoring |
| [rules/10-inert-dependencies.md](rules/10-inert-dependencies.md) | The **declared-but-not-reached sweep**: a dependency, module or plugin that is installed, pinned, scanned and never *runs*. Reachability from a real entrypoint rather than import presence; the per-ecosystem tools and the blind spot each one has; **deletion-as-proof** (no tool's silence is evidence); the leverage ratio; upstream health fetched from a live primary source and reported as dates, not adjectives; the four-bucket classification and the do-not-reimplement list; and why "unused" is an absence claim that needs two independent methods | ...auditing what a repo carries that it does not use — the cheapest finding available, since the fix is a deletion; **and why "unreached" proves nothing about a fallback (§3a)** — a cache, mirror or standby is supposed to be unreached, so deleting one needs the successor measured healthy |
| [rules/04-build-containers.md](rules/04-build-containers.md) | Dockerfiles and build systems: hermetic/reproducible builds, multi-stage builds, build secrets, base image strategy (distroless/Chainguard, digest pinning), image scanning, registry security, immutable tags |
| [rules/05-analysis-gates.md](rules/05-analysis-gates.md) | The scanners themselves: SAST (Opengrep/CodeQL), secret scanning and push protection, IaC scanning (checkov/trivy/tfsec), DAST, license compliance, and flaky-test discipline; the PR gate stack | ...choosing and configuring what runs in CI |
| [rules/09-gates-that-hold.md](rules/09-gates-that-hold.md) | **A warning on a PASSING run may have no path to a human — pre-commit discards a passing hook's output entirely (`rules/11` §4)** · Whether any of it actually **gates** — a property of the pipeline, not the scanner. **What SSDF/CRA/Scorecard/SLSA do and don't require** (all want a record the scan ran, none want evidence it *could have failed*, so a negative control is a house rule); required checks and bypass patterns; a gate whose **scope shrank** under an innocent refactor; **a gate only gates if failing it makes the artifact unconsumable** — build to a candidate identifier the deploy watcher provably cannot match, promote by same-digest retag after the last gate; **a verdict that dies with the executor** (`/dev/termination-log`, budgeted from the container count) so the operator gets a cause instead of `exit code 1`; and **reproducing the gate's exact invocation** rather than a convenient equivalent | ...whenever a gate is green and you need to know what that green is worth, or a deploy failed in a subsystem that is not where the cause is; **count the unit the predicate reads, not its container; a PR proves only its own diff-shape arm (§2c)** |
| [rules/11-after-the-gate-fails.md](rules/11-after-the-gate-fails.md) | **Re-running a failed check destroys the evidence of why it failed (§4a)** · The sibling of rules/09: that file asks whether a gate *can* fail and whether failing *matters*; this one starts after it went red. A verdict that lives only in a garbage-collected log does not exist (§4, `/dev/termination-log` and its per-container byte budget), reproducing the gate's own **invocation** rather than an equivalent (§5), a bespoke watcher inheriting the publishing conventions of what it watches (§6), and **archiving a red run's log before anything re-runs** — a fixed log path is a single-slot buffer, and a list of "unexplained intermittent failures" is often a list of runs whose evidence was overwritten |
| [rules/06-iac-deployment.md](rules/06-iac-deployment.md) | Terraform and delivery: state security, plan/apply separation with review, saved-plan apply, drift detection, GitOps (Flux/Argo) security model, progressive delivery (canary/blue-green/flags), rollback readiness, build-once-promote-many environment parity |
| [rules/07-runtime-ops.md](rules/07-runtime-ops.md) | Runtime enforcement and operations: admission control for signed images (Kyverno/policy-controller), policy as code (OPA/Kyverno) with tests, Pod Security, incident-ready CI/CD audit logging, deployment traceability, backup/restore testing, break-glass |
| [rules/08-registry-security.md](rules/08-registry-security.md) | Securing the container/artifact registry as infrastructure: the registry as a tier-0 supply-chain trust anchor; no anonymous push/pull and least-privilege robot/CI accounts (Zot accessControl, Harbor robots, cloud IAM); immutable tags and digest pinning to defeat tag mutation; OCI referrers for signature/SBOM/scan storage; scan-on-push and continuous re-scan; pull-through cache and image-layer dependency confusion; retention/GC that won't break running deploys; registry HA/backup; network hardening (no anonymous internet exposure, no hostNetwork, TLS) |
| [rules/12-scm-ci-platform-governance.md](rules/12-scm-ci-platform-governance.md) | Org-level SCM/CI settings no workflow file contains: forking of private repos and who may change visibility, org-wide (secure-method) 2FA, the fork-PR approval policy for outside contributors, and the fallback when a self-hosted runner serves a public repo — read with an **owner** token, since `null` means not visible; **runner groups** as the privilege boundary (labels only route), review policy as an enforced setting (last-push approval, risk-tiered reviewers), least-privilege CI administration, settings as code scanned for drift, and keeping CI plugins and workflow scanners current |
| [rules/13-vulnerability-remediation.md](rules/13-vulnerability-remediation.md) | After a scanner reports: priority inputs the advisory lacks (workload privilege, environment, data classification), reachability beyond Go, choosing a scanner by its advisory sources; fixing a vulnerable **transitive** (find the parent, bump it, override last and documented); **suppression discipline**; interim mitigation when a fix exists but cannot be taken; **backporting** a fix; reporting what you find upstream **privately**; software no SCA tool can see |
| [rules/14-sbom-component-inventory.md](rules/14-sbom-component-inventory.md) | What an SBOM must contain (PURL, supplier, licence, dependency edges, serial, run ID, subject metadata), the CI gate that fails an incomplete one, **SBOMs as sensitive data** (access control, scrubbing internal URLs and build paths before sharing), supplier SBOMs for procured software, and patched or forked components (distinct version, recorded pedigree) |
| [rules/15-dependency-adoption.md](rules/15-dependency-adoption.md) | Taking in a **new** dependency, action or CI plugin: the language-neutral selection checklist, confirming origin and chain of custody (provenance attestations, trusted publishing), reading a high-risk dependency's source on adoption and its published diff on upgrade, and hardening the security-relevant defaults of what you consume |

When a task spans stages (most do), read every matching file. For a full pipeline audit,
read all of them.

## Top 10 non-negotiables

Violations of these are at minimum **High** in AUDIT mode and must never be introduced in
BUILD mode:

1. **Top-level `permissions:` block in every workflow**, starting from `contents: read`
   (or `{}`), elevating per job only. Never rely on org/repo default token permissions.
2. **No long-lived cloud credentials in CI secrets.** Use OIDC federation with
   `sub`-claim conditions scoped to repo + ref/environment.
3. **Pin third-party actions (and base images) by full commit SHA / digest**, with a
   version comment, updated by Renovate/Dependabot. Tags are mutable attack surface.
4. **Never combine untrusted PR code with secrets or write tokens.** `pull_request_target`
   (or `workflow_run`) must not check out or execute PR head content; treat fork artifacts
   as hostile input.
5. **No untrusted expression interpolation in `run:` scripts.** PR titles, branch names,
   issue bodies, commit messages go through `env:` indirection, quoted.
6. **Lockfiles committed; CI installs are frozen** (`npm ci`, `--frozen-lockfile`,
   `--require-hashes`, `--locked`). A build that resolves versions at build time is not
   reproducible and not reviewable.
7. **Security gates are required status checks that fail closed.** No
   `continue-on-error`, no `|| true`, no unprotected default branch, no "admins bypass".
8. **Build once, promote the same digest through environments.** Deploy manifests
   reference image digests (or signed, verified tags), never `:latest`.
9. **Terraform state is secret material**: remote encrypted backend, least-privilege
   access, plan on PR with read-only creds, apply only a reviewed saved plan via a
   protected environment.
10. **Production admission requires verified provenance**: signed images (cosign/Kyverno
    ImageValidatingPolicy or equivalent), non-root, pinned digests — enforce, don't just audit.

If the user asks for something that violates a non-negotiable, implement the secure
alternative and explain the delta; only comply after they acknowledge the risk explicitly.
