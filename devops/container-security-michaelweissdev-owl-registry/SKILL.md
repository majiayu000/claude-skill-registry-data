---
name: container-security
description: >
  Harden, scan, and secure container images and runtimes against privilege escalation
  and supply-chain exploits. Use when configuring rootless containers, dropping
  Linux capabilities (--cap-drop=ALL), enforcing read-only root filesystems,
  scanning container images with Trivy, implementing Distroless base images, or
  securing the Docker daemon socket.
compatibility: >
  Agent Skills-compatible coding agents configuring Dockerfiles, Kubernetes PodSecurity,
  or container security scanning pipelines.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "container-security, docker, trivy, rootless, distroless, capabilities, hardening"
  topics: "security, devops"
---

# Container Security and Runtime Hardening

Containers share the host operating system kernel. A security flaw inside a privileged container running as root can lead directly to host node takeover. Hardening containers requires minimizing the attack surface (Distroless base images), dropping all Linux capabilities, running as an unprivileged user, mounting the root filesystem read-only, and scanning for known CVEs.

## Core Rules

1. **Never run containers as root**: Use unprivileged user IDs (UID > 1000). Root in a container is root on the host kernel.
2. **Drop all Linux capabilities by default**: Start with `cap-drop=ALL` and selectively add back only strictly necessary capabilities (e.g. `CAP_NET_BIND_SERVICE`).
3. **Mount the root filesystem read-only (`--read-only`)**: Prevent attackers from installing malware, overwriting binaries, or modifying configuration files at runtime.
4. **Never mount the Docker daemon socket (`/var/run/docker.sock`)**: Mounting the Docker socket inside a container gives that container root control over the entire host.
5. **Scan images in CI with Trivy or Grype**: Block deployments containing High or Critical vulnerabilities with available fixes.
6. **Use Distroless or minimal base images**: Eliminate shells (`/bin/sh`, `/bin/bash`), package managers (`apt`, `apk`), and compilers from production images to deny attackers interactive post-exploitation tools.

---

## 1. Hardened Dockerfile: The Distroless Pattern

Google Container Tools' **Distroless** images contain only your application and its direct runtime dependencies (no package managers, no shell, no utilities):

```dockerfile
# Builder stage with full compiler toolchain
FROM golang:1.22-bookworm AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
# Compile statically linked binary
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /bin/server ./cmd/server

# Hardened Distroless production image
# nonroot user UID is 65532:65532
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /app
COPY --from=builder /bin/server /app/server

USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app/server"]
```

---

## 2. Hardened Runtime Configuration (Docker & Compose)

Enforce strict runtime isolation flags:

```bash
# Running with maximum isolation:
docker run -d \
  --name secure-app \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --tmpfs /run:rw,noexec,nosuid,size=16m \
  --user 10001:10001 \
  -p 8080:8080 \
  my-secure-image:v1.0.0
```

Explanation of flags:
- `--read-only`: Mounts root filesystem as read-only.
- `--cap-drop=ALL`: Strips all 40+ Linux kernel capabilities.
- `--security-opt=no-new-privileges:true`: Prevents processes inside from gaining new privileges via SUID binaries.
- `--tmpfs /tmp`: Provides an isolated in-memory scratch space for transient temp files without permitting disk execution (`noexec`).

---

## 3. Vulnerability Scanning with Trivy

Run automated vulnerability assessments against container images:

```bash
# Scan image for OS packages and language library vulnerabilities
trivy image --severity HIGH,CRITICAL --ignore-unfixed my-image:v1.0.0

# Fail CI pipeline if CRITICAL vulnerabilities are found
trivy image --exit-code 1 --severity CRITICAL my-image:v1.0.0
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Vulnerability / Threat | Correct Practice |
| :--- | :--- | :--- |
| Mounting `/var/run/docker.sock` | Instant root host compromise | Use Kubernetes API or rootless Docker-in-Docker |
| Leaving `USER root` active | Container breakout leads to root access on node | Switch to non-root user (`USER 10001`) |
| Running with `--privileged` | Disables all kernel security namespaces and isolation | Drop all caps (`--cap-drop=ALL`) and grant only minimal caps |
| Storing credentials in image layers | Anyone who pulls the image can extract secrets with `docker history` | Use runtime secret injection (Vault / K8s secrets) |
| Using outdated `:latest` images | Inherits known vulnerabilities without notice | Pin exact digest or stable release tags; scan in CI |

---

## 5. Verification Checklist

- [ ] Container process runs with UID != 0 (verified via `docker exec id`).
- [ ] Image vulnerability scan (`trivy image`) reports zero unfixed Critical CVEs.
- [ ] Root filesystem is mounted `--read-only`.
- [ ] Container has zero unnecessary capabilities (`--cap-drop=ALL`).
- [ ] Docker daemon socket is not mounted into any application container.
