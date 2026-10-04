---
id: container-security
version: "1.6.0"
title: "Container Security"
description: "Hardening for Dockerfiles, OCI images, Kubernetes manifests, and Helm charts. Use when generating a Dockerfile or image build, writing Kubernetes, Helm, or Kustomize manifests, or reviewing container changes in a pull request."
category: hardening
severity: high
applies_to:
  - "when generating a Dockerfile or OCI image build"
  - "when generating Kubernetes / Helm / Kustomize manifests"
  - "when reviewing container changes in PR"
languages: ["dockerfile", "yaml", "go", "python"]
token_budget:
  minimal: 2400
  compact: 3100
  full: 4200
rules_path: "checklists/"
related_skills: ["iac-security", "secret-detection", "iam-best-practices", "supply-chain-security"]
last_updated: "2026-08-12"
sources:
  - "CIS Docker Benchmark v1.6"
  - "CIS Kubernetes Benchmark v1.9"
  - "NIST SP 800-190 Application Container Security Guide"
  - "OWASP Docker Top 10"
external_tools:
  - name: hadolint
    purpose: "Dockerfile linting (~60 ShellCheck-backed rules)"
    command: "hadolint <file>"
  - name: trivy
    purpose: "container image + filesystem CVE scan (scans installed packages, not just Dockerfile text)"
    command: "trivy image <image> | trivy fs ."
---

# Container Security

## Rules (for AI agents)

### ALWAYS
- Use **multi-stage builds**: separate builder/test stages from the final runtime
  image so build toolchains and source aren't shipped. The last stage should be a
  minimal base — `gcr.io/distroless/<variant>`, `scratch`, or a versioned `-slim` /
  `-alpine` variant — pinned by SHA256 digest, not just tag. Two bases have nothing
  to pin: `scratch`, and a reference to an earlier stage in the same file
  (`FROM base`), which is pinned on that stage's own `FROM` line.
  <!-- pattern: { id: dkr-multi-stage, severity: high, check: llm } -->
  <!-- pattern: { id: dkr-pinned-base-digest, severity: high, cwe: 1357, check: deterministic } -->
- Run as a non-root user: set `USER` explicitly on the **final stage**, as a **number**
  not a name. Omitting it leaves the container running as root. K8s `runAsNonRoot`
  rejects UID 0 and cannot resolve a username, so `USER appuser` fails at startup with
  "image has non-numeric user"; any non-zero UID passes, and 10000+ by convention also
  avoids colliding with host accounts.
  <!-- pattern: { id: dkr-missing-user-directive, severity: critical, cwe: 250, check: deterministic } -->
  <!-- pattern: { id: dkr-non-root-user, severity: critical, cwe: 250, check: deterministic } -->
- Use **`npm ci`** (and equivalents `pnpm install --frozen-lockfile`,
  `yarn install --frozen-lockfile`) in container builds, not `npm install`.
  `npm install` mutates the lockfile and resolves versions per-build,
  producing non-deterministic images that drift from the lockfile.
  <!-- pattern: { id: dkr-npm-install-not-ci, severity: medium, check: deterministic } -->
- Add a `.dockerignore` excluding `.git`, `node_modules`, `.env`, `*.pem`, `*.key`,
  `target/`, `.terraform/`, `dist/`, `coverage/`.
  <!-- pattern: { id: dkr-dockerignore-exists, severity: high, check: llm } -->
- Build with **BuildKit** (default since Docker Engine 23; `DOCKER_BUILDKIT=1` on
  older engines) so `RUN --mount=type=secret,id=<name>` is available for build-time
  credentials. `# syntax=docker/dockerfile:1` selects the frontend and does **not**
  enable BuildKit by itself.
  <!-- pattern: { id: dkr-build-with-buildkit, severity: low, check: llm } -->
- Emit an **SBOM** (`docker buildx --sbom=true` / `syft`) and attach it to the
  image so downstream scanners can audit the dependency set.
  <!-- pattern: { id: dkr-sbom-emitted, severity: medium, check: llm } -->
- Pin **apt** packages and clean lists in the same layer: `apt-get update &&
  apt-get install -y --no-install-recommends pkg=1.2.3 && rm -rf
  /var/lib/apt/lists/*`. The `update` must be in that same `RUN` — without it there
  are no package lists; in an earlier layer it goes stale behind the build cache.
  <!-- pattern: { id: dkr-apt-version-pin, severity: medium, cwe: 1357, check: deterministic } -->
- Set explicit `HEALTHCHECK` for long-running services, and separately set
  `livenessProbe` / `readinessProbe` / `startupProbe` in K8s. Kubernetes never runs
  the image's `HEALTHCHECK` — probes are the only mechanism there, so neither one
  covers the other.
  <!-- pattern: { id: dkr-healthcheck-defined, severity: medium, check: llm } -->
- Set resource `requests` and `limits` on every container (CPU and memory). Without a
  memory limit, one container can exhaust the node and take down every pod scheduled
  beside it — the limit is what bounds a runaway's blast radius to its own container.
- Harden at the **container-level** `securityContext`
  (`spec.containers[].securityContext`): `capabilities.drop: [ALL]` then add back only
  what's needed, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`.
  These three exist **only** at container level — under the pod's `spec.securityContext`
  they are silently ignored while the manifest still applies, so the control vanishes
  with nothing to show for it. Use `emptyDir` for paths that must stay writable.
- Apply a seccomp profile (`seccompProfile.type: RuntimeDefault` at minimum) and
  AppArmor / SELinux where available. This one — like `runAsNonRoot` and
  `runAsUser` — may be set on the pod and inherited by its containers.
- Scan every image in CI (Trivy, Grype, Snyk, or your registry's scanner) and triage
  findings on severity, reachability and fix availability together. Fail the build on
  fixable CRITICAL / HIGH findings; a **material vulnerability with no published fix
  needs mitigation or a recorded risk acceptance, not an automatic pass** — "unfixable"
  is remediation information, not a reason it stopped mattering.
  <!-- pattern: { id: dkr-image-scan-required, severity: high, check: llm } -->
- Set `automountServiceAccountToken: false` on every workload that does not call the
  Kubernetes API. The default mounts a real ServiceAccount token into the container,
  so an RCE in an app that never needed cluster access still hands the attacker one.
- For **multi-tenant** workloads (per-user/per-customer sessions on shared
  infra), isolate tenants at the **kernel boundary**: a separate VM — or
  gVisor / Kata — per tenant, never just separate containers on one shared
  daemon. Drop `privileged`, enable user namespaces, and give each tenant its
  own network. A privileged container on a shared host escapes to the host
  trivially, so on shared infra that is full compromise of *every* co-tenant.
- Expose container orchestration to clients only through a **scoped,
  authenticated broker API** that performs the few operations a client may
  request (start/stop *my* session). The client must never hold direct daemon
  or cluster access.
- Consult `iam-best-practices` for cluster RBAC and the identity a workload runs as,
  and `supply-chain-security` for base-image provenance. This skill owns the
  container's own configuration, not what it inherits.

### NEVER
- Run containers as root or with `privileged: true` / `allowPrivilegeEscalation:
  true` outside of explicit, audited system pods (e.g., CNI plugins).
- Use a base image that is **past its vendor's end-of-life date**, or any
  non-LTS release of a runtime that ships an LTS line. EOL images stop
  receiving security patches, so a maintained image with open CVEs is
  still safer than an EOL one with none. Resolve the date against
  `endoflife.date/<runtime>` rather than from memory — a version that was
  supported when this rule was written may not be today. A dated snapshot
  of the common runtimes is in `references/eol-base-images.md`.
  <!-- pattern: { id: dkr-eol-base-image, severity: critical, cwe: 1104, check: llm } -->
- Mount the host docker socket (`/var/run/docker.sock`) inside an application
  container. It's effectively root on the host.
- Expose the container **daemon API over the network** (`tcp://…:2375`, or
  `:2376` even with TLS) to clients or apps. The daemon API is root-on-host:
  whoever reaches it runs arbitrary privileged containers and mounts the host
  filesystem. (A desktop/CLI app talking straight to a remote daemon is the
  same anti-pattern as a mounted `docker.sock`, just over TCP.)
- Ship a **single shared client credential** (one mTLS cert/key, token, or
  kubeconfig bundled into every copy of a distributed app) to reach that daemon
  or cluster. Every install holds the same key — trivially extracted from the
  app bundle — so it grants every user identical access and cannot be revoked
  per-user. Issue per-user / per-session, short-lived, scoped credentials.
- Run a tenant's container `privileged` on a host shared with other tenants, or
  attach tenant containers to a **shared external bridge network** — the first
  gives container-escape → co-tenant takeover, the second gives cross-tenant
  L3 reachability.
- Embed secrets in image layers via `ENV`, `ARG`, `COPY`, or by `echo`-ing them
  to a file. Even if `--squash`'d, BuildKit cache and registry layers leak.
  <!-- pattern: { id: dkr-no-secrets-in-env, severity: critical, cwe: 798, check: deterministic } -->
  <!-- pattern: { id: dkr-no-secrets-in-build-args, severity: critical, cwe: 798, check: llm } -->
  <!-- pattern: { id: dkr-no-secret-leak-in-layers, severity: critical, check: llm } -->
- Run `curl … | sh` or `wget -O- … | sh` in a `RUN` — piping an unverified
  remote script to a shell is arbitrary remote code at build time. Download,
  verify a pinned SHA-256, then execute.
  <!-- pattern: { id: dkr-no-curl-pipe-sh, severity: critical, cwe: 829, check: deterministic } -->
- Use an **unversioned** tag as the final image base — `latest`, `stable`, or a bare
  variant like `python:slim` / `node:alpine`. Builds become non-reproducible and
  quietly pick up CVEs. The *versioned* variants (`python:3.12-slim`,
  `node:20-alpine`) are the recommended minimal bases: it is the missing version that
  makes a tag mutable, not the variant name.
  <!-- pattern: { id: dkr-explicit-latest-tag, severity: high, check: deterministic } -->
- Use `ADD <url>` to fetch a remote resource **unverified**. Either
  `ADD --checksum=sha256:<hash> <url>` (Dockerfile frontend 1.6+), or `RUN curl
  --fail` plus an explicit checksum step, or vendor the artifact.
  <!-- pattern: { id: dkr-no-add-remote, severity: medium, check: deterministic } -->
- Use `hostNetwork: true`, `hostPID: true`, or `hostIPC: true` for application
  pods.
- Run pods in the `kube-system` namespace, or any namespace without a
  `NetworkPolicy` and PodSecurity admission policy.

### KNOWN FALSE POSITIVES
- A **builder stage** legitimately runs as root, installs a toolchain, and skips apt
  version pins — it is discarded and never shipped. These rules target the *final*
  stage.
- `FROM scratch` and `FROM <earlier-stage>` are not unpinned bases: neither can carry
  a tag, and the stage reference is pinned on its own `FROM` line.
- A base-image CVE with no published upstream fix should not hold the build red
  indefinitely — but route it to mitigation or a recorded exception rather than
  dropping it, and re-check when the base image next moves.
- `latest` in a `docker-compose.dev.yml` or a throwaway local build is not a
  production reproducibility problem.
- Operators that legitimately need cluster-admin access (kubelet, CSI drivers,
  CNI plugins) require elevated privileges; they belong in `kube-system` or a
  dedicated namespace with auditing, not in application namespaces.
- Bare-metal Kubernetes nodes sometimes legitimately disable `seccomp` for
  drivers that aren't compatible; document the exception.
- One-shot debugging pods (kubectl debug, ephemeral containers) intentionally
  bypass many of these controls; they should not be persisted as YAML in the
  repo.
- A remote Docker / K8s endpoint over mTLS (`:2376`) is acceptable for an
  **operator's own** CI / build farm where each operator holds a personal,
  revocable cert — the anti-pattern is shipping **one shared** cert inside a
  distributed end-user app.
- `privileged` or a shared bridge network within a **single trust domain** (one
  team's own microservices, or a sim stack on the developer's own machine) is
  lower-risk than the multi-tenant case; these rules target the shared-host,
  cross-tenant blast radius specifically.

## Context (for humans)

Containers leak two ways: image-layer leaks (secrets in `ENV`, build artifacts
left in the final image, vulnerable base CVEs) and runtime escapes (privileged
mode, docker.sock, host namespaces). NIST SP 800-190 frames these as **image
risks**, **registry risks**, **orchestrator risks**, and **runtime risks**.

AI assistants almost always generate Dockerfiles that work and ship — fast — but
they default to a single-stage `FROM node` / `FROM python` and `USER root`. This
skill is the counterweight; pair it with `iam-best-practices` for cluster
RBAC and `supply-chain-security` for image provenance beyond the pod.

A distinct, often-missed class is **remote-daemon and multi-tenancy** exposure.
Handing a client app direct daemon access (`tcp://host:2375` + a cert shipped in
the app bundle) makes every user root on the host; running multiple tenants'
privileged containers on one shared daemon with a shared network means one
tenant's escape compromises all of them. The container hardening flags
(`privileged`, host namespaces, capabilities) matter most precisely where the
blast radius is multi-tenant — isolate at the VM/kernel boundary, and never let
a client touch the daemon directly.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/eol-base-images.md` — dated snapshot of EOL runtimes; check endoflife.date for the current answer
- `checklists/k8s_pod_security.yaml`
- The nine deterministic `dkr-*` checks live in the scanner
  (`internal/tools/library_scanners.go`), not in a checklist file — run them with
  `secure-vibe scan` or the `scan_dockerfile` tool.
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker).
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes).
- [NIST SP 800-190](https://csrc.nist.gov/publications/detail/sp/800-190/final).
