---
name: init-project
description: >-
  v1.0.0 — Use when initializing a new project or adding Python support to existing projects.
  Implements anti supply-chain attack protection for Python dependencies and configures
  UV by Astral as the required package manager with rolling 24-hour publication delay.
---

# Init Project — Supply Chain Protection & UV Setup

You are a security-conscious project initialization specialist. Your job is to set up new projects or add Python support to existing projects with mandatory supply-chain protection and UV tool configuration.

This skill MUST be invoked for every project initialization task.

## absolute rules

- Always apply supply-chain protection when Python is involved
- Never allow direct pip dependency resolution without hash verification and a rolling publication-age cutoff
- Never skip UV installation or configuration
- Always generate and commit `uv.lock` before considering the project protected
- Always configure `exclude-newer = "24 hours"` in `[tool.uv]`
- Always configure `[tool.uv.pip] require-hashes = true` and `verify-hashes = true`
- Do not resolve UV releases from network-discovered latest tags inside bootstrap scripts; pin a reviewed release that has been public for at least 24 hours
- Always verify the protection settings work before completing setup

## step 1 — understand the scope

Determine what type of initialization is needed:
1. **New project** — Create project structure with supply-chain protection
2. **Python addition** — Add Python+UV to an existing project
3. **UV-only** — Configure UV in an existing Python project

**Does this project actually resolve Python dependencies with uv/pip?** Apply the
per-project config below only when it does. Projects that are stdlib-only, or that
get their Python packages from the OS (`apt install python3-pil`, `python3-gi`,
etc.), have no uv/pip resolution surface — `exclude-newer` would have nothing to act
on, so do not add a ceremonial `pyproject.toml`. System/apt package provenance is a
distro concern, outside uv's scope. The machine-wide backstop (next note) still
covers any ad-hoc `uv` invocation in those repos.

## step 2 — configure pyproject.toml

Set up proper Python project configuration with UV and native supply chain protection:

```toml
[project]
name = "your-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
# Ignore packages published within the last 24 hours (rolling supply-chain protection).
# This relies on PEP 700 upload-time metadata — PyPI supports it; private indexes may not.
exclude-newer = "24 hours"

[tool.uv.pip]
# Enforce hash verification for all `uv pip` subcommands.
require-hashes = true
verify-hashes = true
```

**Note on `exclude-newer` format:** Accepts friendly durations (`"24 hours"`, `"7 days"`), ISO 8601 durations (`"PT24H"`, `"P7D"`), or absolute RFC 3339 timestamps (`"2026-01-01T00:00:00Z"`). The `"24 hours"` rolling window is recalculated at each `uv` invocation.

**Note on `require-hashes`:** This applies to `uv pip install`/`uv pip sync` commands. For project-mode commands (`uv sync`, `uv add`), hash verification is done via `uv.lock` automatically.

**Note on the machine-wide backstop and precedence:** A global
`~/.config/uv/uv.toml` with `exclude-newer = "24 hours"` applies the cutoff to
*every* project on this machine, including ones not yet initialized. It is only a
backstop — it does not exist on other machines, CI, or clean installs. uv merges
config with **project `pyproject.toml [tool.uv]` overriding the user-level file**,
so always write the per-project `exclude-newer` anyway: it is the portable,
reproducible source of truth and the only thing that protects the project when
cloned elsewhere. (On this setup the global file is provisioned by
`linux_programming_setup` so a clean install reproduces it.)

## step 3 — per-package exclusions (when needed)

If specific packages must be exempt from the global cutoff (e.g. internal packages on a private registry that lacks PEP 700 upload-time metadata):

```toml
[tool.uv]
exclude-newer = "24 hours"
# false = exempt from cutoff; a duration = stricter or looser window for that package
exclude-newer-package = { my-internal-pkg = false, some-trusted-pkg = "1 hour" }
```

## step 4 — index restriction (stricter posture)

To restrict to a single trusted index and disable PyPI entirely:

```toml
[[tool.uv.index]]
name = "internal"
url = "https://your-private-index.example.com/simple"
default = true   # replaces PyPI; PyPI is no longer consulted
```

To use PyPI plus one explicit extra index only for specific packages:

```toml
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cpu"
explicit = true   # ONLY used when a package explicitly pins to this index

[tool.uv.sources]
torch = { index = "pytorch" }
```

**index-strategy** controls multi-index behaviour (default `first-index` is safest):

```toml
[tool.uv]
index-strategy = "first-index"   # stop at first index that has the package (default, safest)
# "unsafe-best-match" picks best version across ALL indexes — avoid this
```

## step 5 — bootstrap UV securely

If UV is not installed, bootstrap it securely after review; do not fetch the latest tag from GitHub API endpoints inside bootstrap scripts:

```bash
# Check if UV is already installed. If not, set UV_VERSION manually after review;
# do not discover it from the GitHub latest-release endpoint inside bootstrap code.
if ! command -v uv &>/dev/null; then
    UV_VERSION="<reviewed-version-public-for-24-plus-hours>" # example only; replace with reviewed release tag
    checksum_url="https://github.com/astral-sh/uv/releases/download/v${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz.sha256"

    curl -fsSL "https://github.com/astral-sh/uv/releases/download/v${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz" \
        -o /tmp/uv.tar.gz
    curl -fsSL "$checksum_url" -o /tmp/uv.sha256

    cd /tmp && shasum -a 256 -c uv.sha256
    tar -xzf uv.tar.gz
    sudo install -m 755 uv-x86_64-unknown-linux-gnu /usr/local/bin/uv
fi
```

## step 6 — initialize dependencies

For new projects with dependencies:

```bash
# Initialize project (respects exclude-newer from pyproject.toml automatically)
uv init

# Add each dependency (24-hour cutoff is enforced via pyproject.toml config)
uv add <package>

# Generate lock file (hashes included automatically)
uv lock

# Export to requirements with hashes for pip compatibility
uv export -o requirements.txt --output-format requirements --generate-hashes

# Commit the lock file
git add uv.lock requirements.txt pyproject.toml
```

## step 7 — plain pip users (no UV)

If the project must support plain `pip` without UV, enforce the same protections:

```bash
# Generate a hash-locked requirements file from UV
uv export --generate-hashes -o requirements.txt

# Install with hashes enforced — never use pip without --require-hashes on this file
pip install --require-hashes -r requirements.txt
```

Add a `pip` configuration file to prevent accidental unprotected installs:

```ini
# pip.conf (Linux: ~/.config/pip/pip.conf, or project: .pip/pip.conf)
[install]
require-hashes = true
```

Or set the environment variable: `export PIP_REQUIRE_HASHES=1`

## step 8 — install script / CI integration

Create `scripts/setup.sh` or update CI:

```bash
#!/usr/bin/env bash
set -euo pipefail

# uv reads exclude-newer and require-hashes from pyproject.toml automatically
uv sync

# If pip must be used, always consume the hash-bearing export — never resolve bare pip
# pip install --require-hashes -r requirements.txt
```

## step 9 — emergency override (documented, not default)

For emergency situations where bypassing protection is necessary:

1. Record the package, version, cutoff exception reason, reviewer approval, and rollback command in a dated security log or README section.
2. Use `exclude-newer-package = { pkg = false }` as a scoped override rather than removing the global setting.
3. Never clear `exclude-newer`, `require-hashes`, or `verify-hashes` from the default install path.
4. Remove the exception after the affected release window closes and regenerate `uv.lock`.

## Verification checklist

Before considering initialization complete:
- [ ] `[tool.uv] exclude-newer = "24 hours"` is set in `pyproject.toml`
- [ ] `[tool.uv.pip] require-hashes = true` and `verify-hashes = true` are set
- [ ] `uv.lock` is committed to the repository
- [ ] `requirements.txt` exported from `uv export --generate-hashes` contains hashes for every dep
- [ ] CI uses `uv sync` (or `pip install --require-hashes -r requirements.txt`)
- [ ] `pyproject.toml` configured for UV with correct `[build-system]`
- [ ] README.md documents the protection policy and that plain `pip install <pkg>` is forbidden

## When to use this skill

- Creating a new Python project from scratch
- Adding Python support to any existing project
- Setting up UV in a project that currently uses pip directly
- Any task involving `pyproject.toml` or Python dependency management
