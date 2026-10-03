---
name: sandbox-source-intake
description: >
  Safely clone, inspect, and triage fresh GitHub repos without overusing disk or
  running risky code. Use when the user asks to clone many repos, evaluate
  bleeding-edge tools, install MCP servers, run unknown scripts, or harvest
  patterns from public repos.
---

# Sandbox Source Intake

Use this before trusting a fresh repo.

## Clone Policy

- Use shallow clones: `git clone --depth 1 <url> sources/<name>`.
- Prefer a small curated set over bulk cloning.
- Check `du -sh sources` after each batch.
- Skip or sparse-clone very large repos unless needed.

## Inspection Order

1. README and license.
2. Manifests: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`.
3. Install scripts, Dockerfiles, GitHub Actions.
4. Tool/MCP configs and permissions.
5. Source entry points.

## Red Flags

- raw executable zip/binary download as primary install
- curl-piped shell
- postinstall scripts that fetch remote code
- account/session control without a narrow use case
- broad filesystem or shell tools exposed through MCP
- unclear license

## Output

```md
# Source Intake Report
Repo:
Local path:
Disk size:
License:
Runtime:
Install risk:
Useful patterns:
Do not run:
Next action:
```

Then use `$repo-intelligence-brief` for safe repos.

## Validation

- Clone depth, disk size, license, runtime, and install risk are recorded.
- No untrusted install scripts, binaries, package installs, or servers were run.
- Risky repos are marked inspiration-only until reviewed.
