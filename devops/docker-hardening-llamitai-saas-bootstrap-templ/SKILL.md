---
name: docker-hardening
description: >
  Audit or fix Docker security controls for images, Compose and explicitly scoped
  runtime infrastructure: CIS Docker Benchmark, non-root users, secrets in layers,
  digest pinning, capabilities, read-only filesystems, seccomp/AppArmor, SBOM,
  signing, image scanning, network segmentation and runtime detection. Use when
  the user asks to harden, audit or review containers for security, or when a
  concrete container security finding needs a fix. Ordinary Docker edits, style
  refactors, deployments and dependency updates do not start a security audit.
---

# Docker Hardening

Audit and harden Docker artifacts against a layered security model. Backbone: the 12 **CIS Docker Benchmark — Level 1** controls. Extended with: minimal/distroless images, supply-chain integrity (SBOM + signing + BuildKit frontend pinning), runtime profiles (capabilities, seccomp, AppArmor/SELinux, user namespaces, rootless Docker), network segmentation, secrets management, and runtime monitoring.

The skill uses a structured audit matrix and **stack-agnostic** references
(choose the matching remediation for the installed language and runtime).

Use only the control categories needed for the requested audit or finding.
review-change owns a read-only diff review; this skill supplies Docker expertise
when relevant. deploy-mvp owns production provisioning and
resolve-dependabot-prs owns dependency PR resolution. Consulting this checklist
does not start those workflows or authorize external changes.

---

## 1. Working principles

- **Stack agnostic.** Detect language by reading `FROM` + lockfiles. Adapt snippets from `references/remediations.md`.
- **Evidence-based.** Every PASS/FAIL must cite `file:line` or a command's output. Without evidence → `MANUAL`.
- **Minimum-diff fixes.** Smallest change that closes each FAIL. Never bundle unrelated refactors.
- **Preserve task scope.** A review stays read-only. When the user requests fixes,
  implement and verify the authorized local changes without another approval
  loop. External runtime/host mutations require authorization for that target.
- **Defense in depth.** Don't treat a single control as "the fix" — every defense-in-depth layer (Section 3) reduces blast radius if another fails.

---

## 2. Audit workflow

### Phase 0 — Scope & discovery

1. Read the requested scope and existing findings. For a specific image, service
   or control, inspect that target and its dependencies. Use all repository
   Docker artifacts only for a repository-wide audit; do not reconfirm a scope
   the user already supplied.
2. Discover artifacts:
   ```bash
   find . -maxdepth 5 -type f \( \
        -iname "Dockerfile*" \
     -o -iname "Containerfile*" \
     -o -iname "docker-compose*.yml" \
     -o -iname "docker-compose*.yaml" \
     -o -iname "compose*.yml" \
     -o -iname "compose*.yaml" \
     -o -iname ".dockerignore" \
     -o -iname "*.dockerignore" \
   \) \
     | grep -Ev '/(node_modules|\.next|\.venv|venv|dist|build|target|vendor|\.git)/'
   ```
3. If `docker` is available **and** the user wants a runtime audit, list running containers + images:
   ```bash
   docker ps --quiet
   docker images
   ```
4. Read each Dockerfile / compose file before scoring — no scoring from memory.
5. Detect language/package manager from `FROM` and copied lockfiles → use it to pick remediation variants.

### Phase 1 — Score the audit

Score each artifact against the audit matrix below. Use this rubric:

| Result | Meaning |
|---|---|
| `PASS` | Control is satisfied. Cite file:line. |
| `FAIL` | Control is violated. Cite the offending line. |
| `N/A` | Control doesn't apply (one-line reason). |
| `MANUAL` | Needs human verification (e.g., base-image trust, CI scan presence, registry policy). |

#### A — CIS Level-1 controls (mandatory, 12 items)

| # | CIS § | Control | Quick check |
|---|---|---|---|
| A1 | 4.1 | Non-root user | `USER <name-or-uid>` before final `CMD`/`ENTRYPOINT`. |
| A2 | 4.3 | Minimal packages | Minimal base (alpine / slim / distroless / scratch); only required packages installed. |
| A3 | 4.6 | HEALTHCHECK present | Dockerfile `HEALTHCHECK …` **or** compose `healthcheck:`. |
| A4 | 4.7 | Update+install in one layer | `update && install` chained with `&&`; packages pinned; no orphan update. |
| A5 | 4.9 | COPY over ADD | No `ADD` (except local tar extraction with justifying comment). |
| A6 | 4.11 | Verified packages | Signed repos / checksums / lockfile integrity. |
| A7 | 5.28 | Pinned image versions | Never `:latest`; project extension: `FROM image:tag@sha256:…` digest. |
| A8 | 5.7 | No sshd in container | No `openssh-server` installed, no `sshd` running. |
| A9 | 5.9 | Only necessary ports | `EXPOSE` and compose `ports:` minimal; never `-P` / `--publish-all`. |
| A10 | 4.2 | Trusted base image | Official / Verified / mirror / distroless / Docker Hardened Images / Wolfi (Chainguard). MANUAL unless mirror enforced. |
| A11 | 4.4 | Scanned + rebuilt | CI gate fails on findings (`docker scout cves --exit-code`, `trivy image --exit-code 1`, `grype --fail-on high`); third-party actions pinned by full commit SHA (tags are mutable), scanner images by digest. MANUAL — check CI. |
| A12 | 4.10 | No secrets in Dockerfile | No `ENV`/`ARG` with credentials; secrets via BuildKit `--mount=type=secret` or runtime env. |

Section numbers follow docker-bench-security (CIS Docker Benchmark v1.6.0);
newer CIS revisions may renumber. Full text + auditor commands:
[`references/cis-controls.md`](references/cis-controls.md).

#### B — Compose runtime hardening (when compose files exist)

| # | Control |
|---|---|
| B1 | `read_only: true` + explicit `tmpfs:` for writable paths |
| B2 | `cap_drop: ["ALL"]`, `cap_add` only what's needed (commonly `NET_BIND_SERVICE`) |
| B3 | `security_opt: ["no-new-privileges:true"]` on every service |
| B4 | `user: "1001:1001"` non-root UID:GID matching the Dockerfile `USER` |
| B5 | Bind mounts use `:ro` unless writes required |
| B6 | Resource limits: `deploy.resources.limits` (cpu + memory) or `mem_limit` / `cpus` / `pids_limit` |
| B7 | No `privileged: true` (outside dedicated DinD runner) |
| B8 | Internal networks (`internal: true`) for service-to-service; only edge services map ports |
| B9 | `secrets:` block (not `environment:`) for sensitive values |
| B10 | Bounded `logging.options.max-size/max-file` |
| B11 | `restart:` policy set (`unless-stopped` / `on-failure`) — prevents silent crashes |
| B12 | `init: true` (PID 1 reaper) for proper signal handling |

Snippets: [`references/remediations.md`](references/remediations.md).

#### C — Supply chain (build + registry)

| # | Control |
|---|---|
| C1 | BuildKit frontend pinned: `# syntax=docker/dockerfile:1` (or with `@sha256:`); never untrusted frontends |
| C2 | SBOM generated: `docker buildx build --sbom=true …` or `syft <image>` in CI |
| C3 | Provenance `--provenance=mode=max` on hosted CI + signed attestation verified at deploy (needed for SLSA Build L2; unsigned provenance alone is not L2) |
| C4 | Image signed: cosign keyless, Notation or GitHub artifact attestations. Docker Content Trust (Notary v1) is retired — flag `DOCKER_CONTENT_TRUST` / `docker trust` usage |
| C5 | Registry pulls verified: `cosign verify` in deploy step / admission controller |
| C6 | Base images from low-CVE source (Docker Hardened Images / Wolfi / Chainguard / distroless) when feasible, pinned by digest |
| C7 | Renovate/Dependabot auto-bumping digests via PR |
| C8 | `.dockerignore` excludes `.env`, `*.pem`, `.git`, `node_modules`, secrets directories |

Snippets: [`references/advanced-hardening.md`](references/advanced-hardening.md) §A — Supply chain.

#### D — Daemon / host (only score if user grants host access)

| # | Control |
|---|---|
| D1 | Docker daemon running on the latest stable release |
| D2 | `/etc/docker/daemon.json`: `"icc": false`, `"userns-remap": "default"`, `"no-new-privileges": true`, `"live-restore": true` |
| D3 | Audit rules for `/var/lib/docker`, `/etc/docker`, `dockerd` binary (auditd) |
| D4 | Rootless Docker considered for multi-tenant or untrusted workloads |
| D5 | SELinux / AppArmor enabled at host level; default Docker profile loaded |
| D6 | `docker-bench-security` clean run (or documented exceptions) |

Snippets: [`references/advanced-hardening.md`](references/advanced-hardening.md) §D — Host & daemon configuration.

#### E — Runtime profiles (advanced)

| # | Control |
|---|---|
| E1 | Seccomp profile applied (default or tighter custom) |
| E2 | AppArmor profile applied (Linux) or SELinux labels (`:Z`/`:z` on volumes) |
| E3 | User namespaces enabled (`userns-remap`) or rootless mode |
| E4 | `--pid=host` / `--network=host` / `--ipc=host` not used |
| E5 | Docker socket (`/var/run/docker.sock`) not mounted into containers |
| E6 | `--device` exposures minimal and justified |

#### F — Monitoring & detection

| # | Control |
|---|---|
| F1 | Centralized log driver (`syslog`, `journald`, `fluentd`, `awslogs`, etc.) — not just json-file |
| F2 | Container start/stop/exec events shipped to SIEM (`docker events` → collector) |
| F3 | Runtime threat detection: Falco (or equivalent) deployed |
| F4 | Image vulnerability scans fire alerts on new CVEs in deployed images |

### Phase 2 — Report

For a read-only review, return findings without writing a report file. For an
audit that requests a durable report, reuse its specified path or the existing
internal engineering documentation tree:

- `docs/content/docs/equipo/docker-hardening-report.md` in this boilerplate (with `title`/`description` frontmatter, since that tree renders in the docs site)
- `security/docker-hardening-report.md` if `security/` exists
- `docker-hardening-report.md` at repo root otherwise

Create parent folders only when a report file is in scope. A single-control fix
needs its finding, diff and verification evidence, not a full audit document.

Use [the report template](references/report-template.md) for a durable report.


### Phase 3 — Apply requested fixes

If the task is audit/review only, return the findings. If the user has authorized
remediation, continue with each in-scope finding:

1. Make the smallest local change that addresses the finding.
2. Validate the affected artifact with the applicable build/config/runtime check.
3. Report the diff and observed result; leave untested runtime controls unverified.

Never bundle unrelated refactors. Don't switch base-image families (e.g., debian → alpine → distroless) as part of a fix unless the user explicitly asked — surface that as a recommendation. Production rollout remains a separate authorized action.

---

## 3. Defense in depth — 7 layers

This is the mental model. Every audit category in Phase 1 belongs to one of these layers. When recommending fixes, name the layer so the user sees what's being reinforced.

| Layer | What it protects against | Audit categories |
|---|---|---|
| **1. Image** | Vulnerable / malicious base, oversized attack surface | A2, A3, A6, A7, A10, A11, C6 |
| **2. Build** | Secret leakage, supply-chain tampering, cache poisoning | A4, A5, A12, C1–C5, C7, C8 |
| **3. Runtime** | Container breakout, privilege escalation | A1, A8, B1–B7, B11, B12, E1–E6 |
| **4. Network** | Lateral movement, exposed services | A9, B5, B8 |
| **5. Host** | Daemon compromise, host privilege abuse | D1–D6 |
| **6. Orchestration** | RBAC misuse, weak secrets handling | B9, C5 |
| **7. Monitoring** | Late detection of breach / abuse | A3 (HEALTHCHECK), A11, B10, F1–F4 |

### Least privilege checklist

Apply at every layer:
- Non-root user
- Dropped capabilities (`cap_drop: ALL` + selective `cap_add`)
- Read-only root filesystem
- Minimal network exposure (localhost binds, internal networks)
- Restricted syscalls (seccomp profile)
- Bounded resources (cpu/memory/pids)
- No host namespaces, no host devices, no docker socket
- Time-bound, scoped credentials (no long-lived tokens)

---

## 4. Anti-patterns the audit must flag

- `FROM <anything>:latest` — pin the tag, ideally the digest. **FAIL**.
- `ENV API_KEY=…` / `ARG GITHUB_TOKEN=…` / `COPY .env …` / `COPY id_rsa …` — secrets in layers. **FAIL**.
- `RUN apt-get update` on its own line. **FAIL**.
- `ADD http://…` — remote fetch without checksum. **FAIL**.
- `USER root` after the last functional step. **FAIL**.
- `privileged: true` in compose (outside docker-in-docker runners). **FAIL**.
- `-v /var/run/docker.sock:/var/run/docker.sock` inside a non-build container — equivalent to root on host. **FAIL**.
- `--network=host` / `--pid=host` / `--ipc=host` — namespaces broken. **FAIL**.
- `chmod 777` anywhere in the Dockerfile. **FAIL**.
- `docker scan` (deprecated) in CI — replace with `docker scout` or `trivy`.
- Third-party CI actions referenced by tag/branch (`@master`, `@v1`) or scanner images by `:latest` — pin by full commit SHA / digest. **FAIL**.
- `DOCKER_CONTENT_TRUST=1` / `docker trust` / `notary` — retired DCT; migrate to cosign, Notation or attestations.
- Untrusted BuildKit frontend (`# syntax=` pointing at a non-Docker, non-pinned image). **FAIL**.

---

## 5. Things this skill must NOT do

- Don't turn an audit-only request into implementation or production rollout.
- Don't "wholesale rewrite" a Dockerfile — minimum diff per FAIL.
- Don't declare PASS without file:line evidence.
- Don't invent CIS section numbers — stick to the 12 listed in Phase 1 A.
- Don't run or recommend deprecated/retired tooling (`docker scan`, `notary`, Docker Content Trust).
- Don't change the user's base-image family without consent — recommend, don't impose.
- Don't mix languages in a report: match the user's language; reports under `docs/content/` are Spanish.
- Don't audit host (D) without confirmed host access.

---

## 6. References

| File | What's in it |
|---|---|
| [`references/cis-controls.md`](references/cis-controls.md) | Full text of the 12 CIS Level-1 controls — description, risk, auditor procedure, remediation |
| [`references/remediations.md`](references/remediations.md) | Paste-ready Dockerfile + compose snippets for every control, with variants per package manager (apt / apk / dnf) and per language (Node / Python / Go / Java / .NET / Ruby / PHP / Rust) |
| [`references/advanced-hardening.md`](references/advanced-hardening.md) | Supply chain (SBOM, signing, BuildKit frontend), runtime profiles (seccomp, AppArmor, SELinux), user namespaces, rootless Docker, host daemon config, monitoring (Falco, docker events, audit) |
| [`references/report-template.md`](references/report-template.md) | Structure of a durable audit report: scope, per-category summary, findings with evidence, remediations |
| [`references/checklist.md`](references/checklist.md) | Flat pre-deploy checklist — print-friendly, ~60 items grouped by layer |

External docs:

- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- docker-bench-security: https://github.com/docker/docker-bench-security
- Docker Engine security: https://docs.docker.com/engine/security/
- Dockerfile best practices: https://docs.docker.com/build/building/best-practices/
- BuildKit secrets: https://docs.docker.com/build/building/secrets/
- Docker Scout: https://docs.docker.com/scout/
- Trivy: https://aquasecurity.github.io/trivy/
- Grype: https://github.com/anchore/grype
- Syft (SBOM): https://github.com/anchore/syft
- Cosign (signing): https://docs.sigstore.dev/cosign/overview/
- Falco (runtime detection): https://falco.org/
- Wolfi (low-CVE base): https://wolfi.dev/
- Chainguard Images: https://images.chainguard.dev/
- Docker Hardened Images: https://docs.docker.com/dhi/
- DCT retirement: https://docs.docker.com/retired/#docker-content-trust-dct
- SLSA Build track: https://slsa.dev/spec/v1.2/build-track-basics
- Rootless Docker: https://docs.docker.com/engine/security/rootless/
