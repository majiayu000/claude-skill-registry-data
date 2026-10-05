---
name: container-security-hardening
description: "A container image is an attack surface you chose."
---

# Container Security Hardening (Verbose)

## Core Patterns

### Minimize What Is In the Image

A container image is an attack surface you chose. Every binary in it is a tool
available to whoever gets code execution — `curl` to stage a payload, `apt` to
install one, a shell to run it interactively.

```dockerfile
# ❌ Before
FROM python:3.12                       # ~1 GB, full Debian, root, shell, apt
WORKDIR /app
COPY . .                               # ships .git, .env, tests, CI config
RUN pip install -r requirements.txt    # compilers and caches stay in the layer
EXPOSE 80
CMD ["python", "main.py"]              # runs as root, PID 1, no signal handling
```

```dockerfile
# ✅ After — multi-stage, non-root, pinned, minimal
FROM python:3.12-slim@sha256:<digest> AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim@sha256:<digest>
RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app
COPY --from=build /install /usr/local
COPY --chown=10001:10001 src/ /app/
USER 10001
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["python", "-u", "main.py"]
```

What each change buys:

| Change | Effect |
|---|---|
| Multi-stage build | Compilers, headers, and package caches never reach the runtime image |
| `.dockerignore` for `.git`, `.env`, `tests/` | Source history and local secrets stay out |
| Numeric `USER 10001` | Process is unprivileged, and `runAsNonRoot` can validate it |
| Digest-pinned base | The build is reproducible and the artifact is identifiable |
| `EXPOSE 8080` | No `NET_BIND_SERVICE` capability needed |
| `-u` on Python | Logs are unbuffered, so a crash does not lose the last output |

Use a numeric UID, not a name. With `runAsNonRoot: true` and no `runAsUser`, the
kubelet must decide whether the image's user is root — and it cannot resolve a
username against `/etc/passwd` inside the image, so the container fails to start
with an error about a non-numeric user. A numeric UID is unambiguous.

### Choose the Smallest Base You Can Operate

| Base | Shell / pkg mgr | Notes |
|---|---|---|
| `ubuntu`, `python:3.12` | Yes | Largest CVE surface; convenient to debug |
| `-slim` variants | Yes | Good default; real reduction, still debuggable |
| Alpine | Yes (busybox, apk) | musl libc — glibc-linked wheels and DNS edge cases |
| Distroless (`gcr.io/distroless/*`) | No | Runtime only; `:debug` tag adds a busybox shell |
| Chainguard / `scratch` | No | Smallest; needs static binaries or full dependency control |

```dockerfile
# A static binary into a base holding only CA certs and tzdata
FROM golang:1.23@sha256:<digest> AS build
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/api ./cmd/api

FROM gcr.io/distroless/static-debian12:nonroot@sha256:<digest>
COPY --from=build /out/api /api
USER 65532:65532                     # the distroless `nonroot` user
ENTRYPOINT ["/api"]
```

Distroless removes the shell, so `kubectl exec` stops working. That is the intended
trade — an attacker with RCE has no shell either. Plan for it:
`kubectl debug -it pod/api --image=busybox --target=api` attaches an ephemeral
container sharing the process namespace, giving you a shell for troubleshooting
without shipping one to production.

### Keep Secrets Out of Layers

Image layers are immutable and additive. A file written in one layer and deleted
in the next is still fully recoverable from the image; `ENV` values are visible in
the image config to anyone who can pull it.

```dockerfile
# ❌ Every one of these persists in the shipped artifact
ARG NPM_TOKEN
ENV DATABASE_PASSWORD=hunter2
RUN echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" > .npmrc \
 && npm ci \
 && rm .npmrc                  # the layer that created .npmrc still contains it
COPY id_rsa /root/.ssh/id_rsa
```

```dockerfile
# ✅ BuildKit mounts — present only during that RUN, never in a layer
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
RUN --mount=type=ssh go mod download          # private modules over agent forwarding
```
```bash
docker build --secret id=npmrc,src=$HOME/.npmrc --ssh default .
docker history --no-trunc myapp:1.4.2      # audit what each layer baked in
```

Runtime secrets belong in a mounted volume from a secret store, not in `ENV`.
Environment variables are readable via `/proc/<pid>/environ`, are captured by most
crash reporters, and appear in `docker inspect` output.

### Why `latest` Breaks Provenance

`FROM node:latest` — or any mutable tag — means the image you built yesterday and
the one you build today are different artifacts with the same name. Four concrete
consequences:

1. **You cannot say what is running.** "We run node:20" identifies a moving target.
2. **Builds are not reproducible.** The same commit produces different images.
3. **Rollback may not roll back.** Re-deploying `myapp:latest` with
   `imagePullPolicy: Always` can pull a *newer* image than the one you are rolling
   back from.
4. **Scan results go stale silently.** A clean report is attached to a tag that now
   points somewhere else, so it describes an image nobody runs.

```dockerfile
FROM node:20.11.1-slim@sha256:<digest>
```

Pin by digest in the `FROM` line and in every Kubernetes manifest. Digests are
immutable, so an automated bump becomes a reviewable commit. Then sign and verify:

```bash
cosign sign   --yes registry.example.com/api@sha256:<digest>
cosign verify --certificate-oidc-issuer https://token.actions.githubusercontent.com \
              --certificate-identity-regexp '^https://github.com/acme/api/' \
              registry.example.com/api@sha256:<digest>
```

An admission controller that verifies these signatures turns "only images we built
get to run" from a policy into an enforced control.

### Constrain the Runtime

The image controls what is available; the runtime controls what is permitted.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: api}
spec:
  template:
    spec:
      automountServiceAccountToken: false   # unless the pod calls the API server
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
        seccompProfile:
          type: RuntimeDefault              # the runtime's default seccomp filter
      containers:
        - name: api
          image: registry.example.com/api@sha256:<digest>
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          resources:
            limits: {memory: 512Mi}         # bound the blast radius of a leak
          volumeMounts:
            - {name: tmp, mountPath: /tmp}  # required by readOnlyRootFilesystem
      volumes:
        - {name: tmp, emptyDir: {}}
```

| Setting | Blocks |
|---|---|
| `runAsNonRoot: true` | An image whose user is root fails to start, rather than silently running as root |
| `allowPrivilegeEscalation: false` | Sets `no_new_privs`; setuid binaries cannot gain privilege |
| `readOnlyRootFilesystem: true` | Writing a payload, tampering with binaries or config on disk |
| `capabilities.drop: ["ALL"]` | Removes even the default set — raw sockets, `chown`, `mknod`, module loading |
| `seccompProfile: RuntimeDefault` | Syscalls no normal application makes, several historically used for escape |
| `automountServiceAccountToken: false` | A stolen token being used to enumerate or modify cluster state |

`readOnlyRootFilesystem: true` is the one that breaks applications, because most
write somewhere — temp files, caches, PID files. Mount `emptyDir` volumes at
exactly those paths rather than abandoning the control.

Enforce it cluster-wide with Pod Security Admission so a manifest cannot opt out:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: prod
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
```

The `restricted` profile requires non-root, dropped capabilities, `no_new_privs`,
and a seccomp profile. Roll it out as `warn` first, read the warnings, then flip to
`enforce`.

### Default-Deny Network Egress

A compromised container's next move is outbound — to fetch a payload, exfiltrate,
or reach cloud metadata. Kubernetes has no egress restriction by default.

```yaml
# 1. Deny everything in the namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny, namespace: prod}
spec: {podSelector: {}, policyTypes: [Ingress, Egress]}
```
```yaml
# 2. Allow back exactly what this workload needs
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: api-egress, namespace: prod}
spec:
  podSelector: {matchLabels: {app: api}}
  policyTypes: [Egress]
  egress:
    - to: [{podSelector: {matchLabels: {app: postgres}}}]
      ports: [{protocol: TCP, port: 5432}]
    - to: [{namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: kube-system}}}]
      ports: [{protocol: UDP, port: 53}]     # DNS
```

Pair this with IMDSv2 required on cloud nodes. An SSRF or RCE that can reach the
instance metadata endpoint frequently converts straight into node-role credentials.

### Scan at the Right Points

```yaml
# Build gate: block on fixable Critical/High before anything is pushed
- run: docker build -t api:${{ github.sha }} .
- run: |
    trivy image --severity HIGH,CRITICAL --ignore-unfixed \
          --exit-code 1 api:${{ github.sha }}
- run: trivy image --format cyclonedx --output sbom.json api:${{ github.sha }}
- run: trivy config ./deploy         # catches a missing securityContext in YAML
```

| When | Scan | Gate on |
|---|---|---|
| Pre-merge | Dockerfile + manifests (`trivy config`, `checkov`) | Missing hardening controls |
| Post-build | Built image, before push | Fixable Critical/High |
| Nightly, on running images | Registry and live workloads | Nothing — report and triage |

The nightly scan is the one teams omit and the one that catches the most: a CVE
published after your last deploy is invisible to a build-time-only scan, because
the image was clean when it was built and is not clean now. Retain the SBOM so
"are we affected by this advisory?" is a query rather than a rebuild, and triage
the output with the vulnerability-assessment skill.

## Common Anti-Patterns

❌ **Running as root because the app "needs" it** — usually it needs a writable
directory or a low port, not UID 0.
✅ Create a numeric user, `chown` the one path it writes, listen above 1024.

❌ **`FROM ...:latest` or a floating tag** — no provenance, no reproducibility,
rollbacks that roll forward.
✅ Pin by digest everywhere and automate the bumps as reviewable commits.

❌ **Secrets in `ARG`/`ENV`, then deleted in a later `RUN`** — layers are additive;
the secret ships.
✅ BuildKit `--mount=type=secret`; audit with `docker history --no-trunc`.

❌ **Single-stage builds** — compilers, package managers, and caches ship to prod
as ready-made attacker tooling.
✅ Multi-stage; copy only the artifact into a minimal runtime.

❌ **`privileged: true` to make something work** — it disables essentially every
container boundary at once. Likewise mounting the Docker socket, which is root on
the host directly.
✅ Identify the one capability actually needed; use a rootless builder (kaniko,
buildah, BuildKit) for in-cluster builds.

❌ **Keeping the default capability set** — `CHOWN`, `SETUID`, `NET_RAW` and more
are granted for free and almost never used.
✅ `drop: ["ALL"]`, then add back only what demonstrably fails.

❌ **Skipping `readOnlyRootFilesystem` because the app writes to `/tmp`.**
✅ Mount an `emptyDir` at `/tmp` and keep the control.

❌ **No egress NetworkPolicy** — a compromised pod can reach the internet and the
metadata endpoint.
✅ Default-deny egress, allowlist per workload, require IMDSv2.

❌ **Scanning only at build time** — yesterday's clean image is not today's.
✅ Re-scan running images on a schedule and retain SBOMs.

## Container Hardening Checklist

- [ ] Multi-stage build; no compilers or package managers in the runtime image
- [ ] Minimal base (slim, distroless, or Chainguard) chosen deliberately
- [ ] Base image and all manifests pinned by digest, never a floating tag
- [ ] `USER` set to a numeric non-root UID
- [ ] `.dockerignore` excludes `.git`, `.env`, tests, and CI config
- [ ] No secrets in `ARG`, `ENV`, or any layer; BuildKit secret mounts used
- [ ] `docker history --no-trunc` reviewed on the shipped image
- [ ] Images signed, and signatures verified at admission
- [ ] `runAsNonRoot`, `runAsUser`, `fsGroup`, and `allowPrivilegeEscalation: false` set
- [ ] `readOnlyRootFilesystem: true` with `emptyDir` at every written path
- [ ] `capabilities.drop: ["ALL"]`, additions justified individually
- [ ] `seccompProfile: RuntimeDefault` (or a tighter custom profile)
- [ ] Memory limits set to bound blast radius
- [ ] `automountServiceAccountToken: false` unless the pod calls the API server
- [ ] Pod Security Admission `restricted` enforced on production namespaces
- [ ] Default-deny NetworkPolicy with per-workload egress allowlists; IMDSv2 required
- [ ] Image scan gates the build on fixable Critical/High findings
- [ ] IaC/manifest scanning catches a missing `securityContext` pre-merge
- [ ] Running images re-scanned nightly; SBOM retained per build
