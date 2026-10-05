---
name: dockerfile-smells
description: This skill should be used when the user mentions "Dockerfile", "docker image size", "container security", "multi-stage build", "distroless", "run as root", "docker layer caching", or is reviewing/optimizing a container image. It provides a catalog of Dockerfile anti-patterns and the hardening principles that fix them.
---

# Dockerfile Smells and Hardening

## Purpose
A consistent set of Dockerfile anti-patterns and their fixes, so container reviews produce smaller, safer, cache-friendly images the same way every time. This is container-build domain knowledge, the specific smells and the reasons they matter, not generic Docker syntax.

## Smell catalog

| Smell | Why it hurts | Fix |
|-------|--------------|-----|
| Runs as `root` (no `USER`) | container escape = host root; violates PSS/most policies | add `USER <uid>` (numeric, non-root) |
| `latest` / unpinned base tag | non-reproducible; silent base drift; supply-chain risk | pin `FROM img@sha256:<digest>` |
| Single-stage build | ships compilers, headers, build deps in runtime image | multi-stage: build → slim runtime |
| `COPY . .` before dep install | any source edit busts the dependency cache layer | copy manifests, install, *then* copy source |
| Secrets baked in a layer | recoverable from image history forever | `RUN --mount=type=secret`; never `ENV TOKEN=` |
| `apt-get` with no cleanup | apt lists/caches bloat the layer | `--no-install-recommends` + `rm -rf /var/lib/apt/lists/*` in the same `RUN` |
| Missing `.dockerignore` | huge context; `.git`/secrets sent to daemon | add `.dockerignore` |
| No `HEALTHCHECK` | orchestrator can't detect a wedged process | add `HEALTHCHECK` where the app exposes a check |
| `ADD` for local files / remote URLs | silent auto-extract, unverified downloads | use `COPY`; fetch with verified checksums |
| Many chained `RUN` layers | extra layers, larger image | combine related commands, order by volatility |

## Hardening principles (apply in order)
1. **Least privilege at runtime**: non-root numeric `USER`, drop capabilities, read-only root filesystem where possible.
2. **Minimal surface**: distroless or `-slim` runtime base; install only what runs in production.
3. **Reproducibility**: pin base image by digest; pin package versions where feasible.
4. **Cache efficiency**: order layers least-volatile → most-volatile (base, then deps, then source).
5. **No secrets in layers**: build secrets via BuildKit mounts; runtime secrets via the orchestrator, never `ENV`/`ARG` bake-in.

## Layer-ordering rule
Put the things that rarely change (base image, system packages, dependency manifests + install) **above** the things that change every commit (application source). One dependency layer that survives across builds saves the most CI time.

## Additional Resources
### Reference Files
For the full hardening checklist with the security rationale, consult:
- **`references/hardening-checklist.md`**: non-root user, minimal/distroless base, digest pinning, no secrets in layers, HEALTHCHECK, dropping setuid/setgid, read-only root filesystem, and least-capability, each with the concrete threat it addresses.

For copy-pasteable multi-stage templates, consult:
- **`references/multistage-patterns.md`**: build-vs-runtime split templates per ecosystem (Node, Python, Go, Java/JVM, Rust), cache-mount patterns, and exactly what to copy into the final stage.
