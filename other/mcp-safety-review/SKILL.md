---
name: mcp-safety-review
description: >
  Review MCP servers, agent tools, install scripts, or fresh GitHub repos for
  security and trust risk. Use when tools request shell/filesystem/network
  access, credentials, browser/session control, messaging accounts, package
  installs, or destructive write permissions. Skip pure CI/conformance harness
  design after trust is established; use
  `$auto-skill-build-mcp-conformance-harness`.
---

# MCP Safety Review

Goal: decide whether a server/tool should be installed, sandboxed, modified, or rejected.

## Review Phases

1. **Source**: repo age, maintainer, license, release artifacts, install path.
2. **Runtime**: language, dependencies, postinstall hooks, Docker privileges, shell execution.
3. **Data**: files read, secrets touched, remote endpoints, telemetry.
4. **Tools**: classify every MCP tool by read/write/destructive/account-control capability.
5. **Auth**: API keys, OAuth, token storage, tenant boundaries, local-only claims.
6. **Blast radius**: what the tool can change without human confirmation.

## Severity

- `high`: credential exposure, destructive actions without confirmation, account takeover path, arbitrary command execution from untrusted input.
- `medium`: broad permissions, unclear auth boundary, unpinned remote code, weak logging of sensitive data.
- `low`: missing docs, weak error handling, optional hardening.
- `info`: posture notes without a concrete abuse path.

## Output

```md
# Safety Review
Verdict:
Severity:
Confidence:
Why it matters:
Evidence:
Required mitigations:
Install decision:
```

Hard rule: do not run raw binaries, zips, curl-piped scripts, or package
installers from a fresh repo until this review is complete.

## Pair With

- `$auto-skill-safety-mcp-secret-guard` when configs, logs, or examples may
  contain credentials.
- `$auto-skill-build-mcp-conformance-harness` after the server is trusted and
  the user needs repeatable CI/release gates.

## Validation

- Every exposed tool is classified by read/write/destructive/account-control capability.
- Install/run decision states what was not executed.
- Required mitigations are concrete enough to apply before trust is expanded.
