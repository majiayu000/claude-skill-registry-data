---
name: devcontainers
description: Use when building, modifying, using, or distributing Dev Containers — creating or editing devcontainer.json from scratch, adding devcontainer features, writing Dockerfiles for dev containers, authoring custom features or templates, publishing to GHCR, using the devcontainer CLI (devcontainer up, build, exec, features test), or debugging container startup failures. Also use when the user mentions ghcr.io/joeblackwaslike/devcontainer, the claude-code or claude-code-extend templates, or asks about setting up a reproducible development environment in a container. Invoke this skill whenever the word "devcontainer", "dev container", ".devcontainer", or "devcontainer.json" appears, or whenever someone wants to containerize their development environment.
metadata:
  last_updated: "2026-06-01"
---

# Dev Containers

Core principle: A devcontainer is a version-controlled, reproducible development environment. Prefer features over Dockerfile layers for common tools; write Dockerfiles only for custom tooling not available as a feature.

## Route First

| Task | Reference |
|---|---|
| Create or edit devcontainer.json | `references/devcontainer-json.md` |
| Add or find features | `references/features.md` + `references/generated/features-index.md` |
| Author a custom feature | `references/features.md` (authoring section) |
| Create or publish a template | `references/templates.md` |
| devcontainer CLI commands | `references/cli.md` |
| Publish features/templates to OCI/GHCR | `references/distribution.md` |
| Debug startup, mounts, GPU, PATH, permissions | `references/gotchas.md` |
| Joe's personal devcontainer (ghcr.io/joeblackwaslike/devcontainer) | `references/joe-devcontainer.md` |
| Browse all available features / templates | `references/generated/features-index.md` or `references/generated/templates-index.md` |

Read the most specific reference first; read others only if the first doesn't cover the need.

## Quick Patterns

### Minimal devcontainer.json

```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": { "version": "lts" }
  }
}
```

### Config file discovery order

1. `.devcontainer/devcontainer.json`
2. `.devcontainer.json` (project root)
3. `.devcontainer/<subfolder>/devcontainer.json` (multi-config; user selects at open time)

### `image` vs `build`

Use `image` when the base needs no customization.
Use `build.dockerfile` when you need custom layers (apt installs, baked files, config not available as a feature).

```json
{ "build": { "dockerfile": "Dockerfile", "context": "..", "args": { "NODE_VER": "18" } } }
```

### Lifecycle execution order

```
initializeCommand   (host machine, before anything)
→ image pull / build
→ features install  (as root)
→ onCreateCommand   (container, once on creation)
→ postCreateCommand (container, once; runs as remoteUser)
→ postStartCommand  (container, every start/rebuild)
→ postAttachCommand (container, every editor attach)
```

Any non-zero exit skips all subsequent scripts. Scripts can be a string, array, or parallel object:

```json
"postCreateCommand": {
  "deps": "npm install",
  "types": "npm run typecheck"
}
```

### Environment variables: `containerEnv` vs `remoteEnv`

| Property | Set at | Visible to |
|---|---|---|
| `containerEnv` | Image build time | All processes in container |
| `remoteEnv` | Runtime (by tooling) | VS Code terminals, tasks, debug only |

Always append to PATH — never overwrite:

```json
"remoteEnv": { "PATH": "${containerEnv:PATH}:/my/custom/bin" }
```

### VS Code customizations

```json
"customizations": {
  "vscode": {
    "extensions": ["ms-python.python", "esbenp.prettier-vscode"],
    "settings": { "editor.formatOnSave": true }
  }
}
```

## Red Flags — Stop

- Installing a common tool in `postCreateCommand` when a Feature exists for it
- Setting `PATH` in `remoteEnv` without `${containerEnv:PATH}:` prefix
- Adding `"--gpus all"` to `runArgs` without guarding for non-GPU hosts
- Publishing to GHCR without setting package visibility to **public**
- Editing devcontainer.json and expecting auto-rebuild — VS Code requires explicit `Dev Containers: Rebuild Container`
- Running `postCreateCommand` as root when the intent is user-level setup (use `remoteUser`)

## Completion Criteria

- Config validates: `devcontainer read-configuration --workspace-folder .` exits 0
- Container starts: `devcontainer up --workspace-folder .` exits 0
- All lifecycle scripts exit 0
- For features: `devcontainer features test -f ./src/<feature>` passes
- For distribution: GHCR package is set to **public** and version is confirmed in registry
