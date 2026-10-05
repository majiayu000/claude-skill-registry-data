---
name: dep-audit
description: Audit dependencies for vulnerabilities and version conflicts in ettametta. Use when checking for security issues in Python/Node.js packages, resolving version conflicts, or hardening the dependency tree. Covers pip-audit, npm audit, bandit, safety, and Docker image scanning.
---
# Dependency Audit

Skill for scanning ettametta's dependencies for vulnerabilities, version conflicts, and outdated packages across Python, Node.js, and Docker.

## Quick Scans

### Python vulnerability scan
```bash
# pip-audit (preferred — uses OSV database)
pip-audit -r requirements.txt

# safety (already in CI but non-blocking)
safety check --full-report

# bandit (static analysis for Python code)
bandit -r src/api/ -f json
```

### Node.js vulnerability scan
```bash
npm audit
npm audit --production  # skip devDependencies
```

### Check for outdated packages
```bash
# Python
pip list --outdated

# Node.js
npm outdated
```

### Docker image scan
```bash
# If trivy is installed
trivy image ettametta-api:latest
```

## Architecture Reference

### Dependency Files (fragmented across 7+ locations)

| File | Purpose | Pinning |
|------|---------|---------|
| `requirements.txt` | Root-level (generated from .venv) | Exact pins |
| `src/api/requirements.txt` | Primary API deps (76 deps) | Mixed (`>=` and `==`) |
| `src/api/requirements.in` | pip-compile input | Loose constraints |
| `src/api/requirements-locked.txt` | pip-compile output with hashes | Generated |
| `src/api/requirements-agents.txt` | Agent framework extras | Mixed |
| `src/services/openclaw/requirements.txt` | OpenClaw service | Mixed |
| `src/engines/remote_ai_setup/requirements.txt` | Remote AI setup (heavy ML stack) | Mixed |

### Node.js
| File | Purpose |
|------|---------|
| `package.json` | Root workspace config (workspaces: `apps/*`, `src/tests/e2e`) |
| `apps/dashboard/package.json` | Next.js dashboard |
| `apps/remotion-studio/package.json` | Remotion 4.0.454, React 19, Zod 4.3.6 |
| `src/tests/e2e/package.json` | Playwright E2E tests |

### CI Security Scans (both non-blocking)

In `.github/workflows/ci-cd.yml` (lines 71-86):
```yaml
- name: Security scan
  run: |
    bandit -r src/api/ -f json -o bandit-report.json || true
    safety check --full-report || true
```

The `|| true` means **scan failures do not block deploys**.

## Known Issues

### Version conflicts

| Package | Root `requirements.txt` | `src/api/requirements.txt` | Issue |
|---------|------------------------|---------------------------|-------|
| `bcrypt` | `5.0.0` | `4.0.1` | Conflict |
| `langchain` | `0.1.20` | `0.1.20` | Pinned old version (likely due to breaking API changes) |

### Fragmented requirements

Requirements are spread across 7+ files with inconsistent pinning. The root `requirements.txt` was generated from `.venv` and may not reflect what's actually deployed. The `requirements-locked.txt` with hashes is the most trustworthy but may be stale.

### No Dependabot/Renovate

No automated dependency update tool is configured. Only manual `pip-compile` and `npm audit`.

## Fixing Vulnerabilities

### Python

```bash
# Generate updated locked requirements
cd src/api
pip-compile requirements.in --generate-hashes -o requirements-locked.txt

# Install from locked file
pip install --require-hashes -r requirements-locked.txt
```

### Node.js

```bash
# Fix non-breaking
npm audit fix

# Fix including breaking changes (review first)
npm audit fix --force
```

### Docker base images

Update base image tags in Dockerfiles:
- `api.Dockerfile` — Python 3.10-slim
- Dashboard — Node.js 18-alpine
- `discovery-go/Dockerfile` — Go

## Hardening Checklist

1. Run `pip-audit` and fix critical/high vulnerabilities
2. Run `npm audit` and fix critical/high vulnerabilities
3. Resolve the bcrypt version conflict (pick one version)
4. Make CI security scans blocking (remove `|| true`)
5. Add Dependabot or Renovate for automated updates
6. Add `pip-audit` to CI pipeline alongside `safety`
7. Pin Docker base images to digest (not just tag)

## References

- [Requirements File Map](references/requirements-map.md)
- [CI Security Config](references/ci-security.md)
