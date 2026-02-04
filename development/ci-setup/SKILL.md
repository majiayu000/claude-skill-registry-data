---
name: ci-setup
description: Set up pre-commit hooks and GitHub Actions workflows for testing, linting, security scanning, releases, and deployments. Supports Python, Node.js, Go, Rust, and multi-language projects.
---

# CI/CD Setup

Configure pre-commit hooks and GitHub Actions for automated testing, linting, security scanning, and release management across multiple languages and package registries.

## Pre-commit Hooks

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Core Hooks (Language-Agnostic)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
```

### Python Hooks

| Hook | Purpose | Config |
|------|---------|--------|
| `black` | Code formatting | `pyproject.toml` |
| `ruff` | Linting (replaces flake8/isort) | `pyproject.toml` |
| `mypy` | Type checking | `pyproject.toml` |
| `bandit` | Security scanning | Args: `-r src -x tests` |

### JavaScript/TypeScript Hooks

| Hook | Purpose | Config |
|------|---------|--------|
| `eslint` | Linting | `eslint.config.js` |
| `prettier` | Formatting | `.prettierrc` |

```yaml
- repo: https://github.com/pre-commit/mirrors-eslint
  rev: v9.0.0
  hooks:
    - id: eslint
      additional_dependencies:
        - eslint
        - typescript
        - "@typescript-eslint/parser"
        - "@typescript-eslint/eslint-plugin"

- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v4.0.0
  hooks:
    - id: prettier
```

### Go Hooks

```yaml
- repo: https://github.com/dnephin/pre-commit-golang
  rev: v0.5.1
  hooks:
    - id: go-fmt
    - id: go-vet
    - id: golangci-lint
```

### Rust Hooks

```yaml
- repo: https://github.com/doublify/pre-commit-rust
  rev: v1.0
  hooks:
    - id: fmt
    - id: cargo-check
    - id: clippy
```

## Package Registries

| Language | Registry | Workflow Template | Auth Method |
|----------|----------|-------------------|-------------|
| Python | PyPI | `publish-pypi.yml` | OIDC Trusted Publishing |
| Node.js | NPM | `publish-npm.yml` | `NPM_TOKEN` secret or OIDC |
| Go | pkg.go.dev | Auto-indexed | None needed |
| Rust | crates.io | `publish-crates.yml` | `CARGO_REGISTRY_TOKEN` |

## GitHub Workflows

### Workflow Matrix by Language

**Python:**
| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `python-ci.yaml` | push, PR | Tests, lint, security |
| `publish-pypi.yml` | release/latest | Publish to PyPI |

**Node.js:**
| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `node-ci.yaml` | push, PR | Tests, lint, security |
| `publish-npm.yml` | release/latest | Publish to NPM |

**Shared:**
| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `docs.yml` | push to main/release | Deploy docs |
| `create-release.yml` | release/* branch | Draft GitHub release |
| `codeql.yml` | push, PR, weekly | Security analysis |
| `docker-build-push.yml` | push to release/* | Container builds |
| `validate-branch-flow.yml` | PR to release/* | Enforce branch rules |

### Branch Flow

```
main → release/latest → release/x.y.z
         ↓                    ↓
    publishes package    creates draft release
    (PyPI/NPM/crates)
```

### Trusted Publishing (OIDC)

Both PyPI and NPM support OIDC - no secrets required:

**PyPI:**
```yaml
permissions:
  id-token: write
steps:
  - uses: pypa/gh-action-pypi-publish@release/v1
```

**NPM (provenance):**
```yaml
permissions:
  id-token: write
steps:
  - run: npm publish --provenance --access public
    env:
      NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Required Secrets

| Secret | Purpose | Required For |
|--------|---------|--------------|
| `CODECOV_TOKEN` | Coverage uploads | All languages |
| `NPM_TOKEN` | NPM publishing | Node.js |
| `CARGO_REGISTRY_TOKEN` | crates.io publishing | Rust |
| `DIGITALOCEAN_ACCESS_TOKEN` | Container registry | Docker (if using DO) |
| None for PyPI | OIDC Trusted Publishing | Python |

## Templates

### Pre-commit
- `templates/.pre-commit-config.yaml` - Multi-language configuration

### Python
- `templates/workflows/python-ci.yaml` - Tests and linting
- `templates/workflows/publish-pypi.yml` - PyPI publishing

### Node.js
- `templates/workflows/node-ci.yaml` - Tests and linting
- `templates/workflows/publish-npm.yml` - NPM publishing

### Shared
- `templates/workflows/docs.yml` - MkDocs deployment with mike
- `templates/workflows/create-release.yml` - Draft release automation
- `templates/workflows/codeql.yml` - CodeQL security scanning
- `templates/workflows/docker-build-push.yml` - Container builds
- `templates/workflows/validate-branch-flow.yml` - Branch flow enforcement
