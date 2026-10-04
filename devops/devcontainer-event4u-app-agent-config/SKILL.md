---
model_tier: medium
name: devcontainer
description: "Wire up DevContainers / GitHub Codespaces — `devcontainer.json`, container images, secrets, VS Code features, port forwarding. NOT for tuning Copilot itself (use `copilot-config`)."
domain: devops
workspaces:
  - engineering
packs:
  - engineering-base
---

# devcontainer

## When to use

Use this skill when working with DevContainer configuration, GitHub Codespaces setup, or development environment standardization.

Do NOT use when:
- Local Docker setup without Codespaces (use `docker` skill)
- Production deployment (use `aws-infrastructure` skill)

## Procedure: Modify DevContainer

1. **Gather context** — read `.devcontainer/devcontainer.json`, check `.devcontainer/` for env files and docs, check `agents/overrides/skills/devcontainer.md` for project-specific overrides.
2. **Identify change type** — classify: image change, feature addition, secret addition, extension change, or env var change.
3. **Make the change** — edit `devcontainer.json` (or related files). Follow conventions below for secrets, features, and environment variables.
4. **Build and verify** — run `devcontainer build` to confirm the container builds. Check that extensions load and ports forward correctly.
5. **Document** — if adding a new secret or dependency, update the onboarding docs in `.devcontainer/`.

## Architecture

### Custom image

DevContainers typically use a **pre-built custom image** hosted on a container registry (GHCR, ECR, Docker Hub). Read `devcontainer.json` for the image URL.

The image should include:
- Language runtime (PHP, Node.js, Python, etc.)
- Package managers (Composer, npm, etc.)
- Common development tools

### Features (installed on top of the image)

Common features:

| Feature | Purpose |
|---|---|
| `git` | Git version control |
| `github-cli` | GitHub CLI (`gh`) for API access |
| `docker-in-docker` | Run Docker inside the DevContainer |

### Secrets management

Secrets can be managed via:
- **File mounts**: `.devcontainer/.secrets/<NAME>` → `/run/secrets/<NAME>`
- **GitHub Codespaces secrets**: configured in the repository settings
- **Environment variables**: in `.devcontainer/devcontainer.env`

Read `devcontainer.json` for the actual secret definitions and requirements.

### Workspace

- **Workspace folder**: typically `/workspace` or `/workspaces/{repo-name}`
- **Mount type**: bind mount from local workspace
- Container name and hostname: defined in `devcontainer.json`

### IDE integration

- VS Code Live Share for collaborative development
- IDE extensions can be pre-configured in `devcontainer.json`

## Conventions

### Adding new secrets

1. Add the secret definition to `devcontainer.json` → `secrets` section.
2. Add a bind mount from `.devcontainer/.secrets/<NAME>` to `/run/secrets/<NAME>`.
3. Document the secret with `description` and `documentationUrl`.
4. Mark as required or optional.

### Modifying the base image

- If the base image is maintained in a separate repository, do NOT change the image tag without coordination.
- Prefer adding **features** over modifying the base image.

### Environment variables

- Runtime env vars go in `.devcontainer/devcontainer.env`.
- Secrets go in `.devcontainer/.secrets/` (gitignored).
- Do NOT hardcode secrets in `devcontainer.json`.

## Output format

1. Updated devcontainer.json or related configuration files
2. Summary of changes and rebuild requirements

## Auto-trigger keywords

- DevContainer
- Codespaces
- dev environment
- container setup

### Validate

- Verify the DevContainer builds successfully (`devcontainer build`).
- Confirm all required extensions and features are installed.
- Check that port forwarding and volume mounts work as expected.

## Gotcha

- DevContainer rebuilds are slow — test configuration changes incrementally, not all at once.
- Secrets in devcontainer.json are visible in version control — use Codespaces secrets instead.
- Extensions in devcontainer.json install on EVERY rebuild — keep the list short.

## Do NOT

- Do NOT commit secret files — they should be gitignored.
- Do NOT change the workspace mount path without updating all related configs.
- Do NOT remove required secrets without checking which services depend on them.
- Do NOT switch base images without team approval.

## Related

- **Skill:** `docker` — Docker setup, multi-stage Dockerfile, compose services
- **Skill:** `traefik` — local reverse proxy with real domains and HTTPS
- **Rule:** `docker-commands.md` — commands run inside Docker
