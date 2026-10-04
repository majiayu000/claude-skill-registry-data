---
name: safe-install-checklist
description: Produce safe install recommendations for agent skills and skillsets. Use when Codex is asked whether a skill is safe to install, how to install with least privilege, what to inspect before install, or what approval conditions are required.
license: MIT
---

# Safe Install Checklist

## Core Workflow

1. Identify source, version, publisher, install method, host, and intended use.
2. Confirm the skill was reviewed for instructions, scripts, dependencies,
   secrets, data movement, and required permissions.
3. Recommend least-privilege install options: pin version, copy manually,
   inspect before enabling, disable scripts, or run read-only first.
4. Define approval gates for write access, network access, MCP scopes,
   customer data, production systems, and outbound messages.
5. List post-install checks and re-review triggers.
6. Conclude with approve, approve with changes, block, or defer.

## Safety Rules

- Do not recommend installing unreviewed third-party skills into a privileged
  agent environment.
- Do not make GitHub CLI, Codex, or any one host the only safe path.
- Do not approve auto-updating skill sources for high-risk workflows without a
  re-review process.

## Deliverable Shape

For safe install recommendations, provide:

- Source and version
- Intended host and install method
- Pre-install checks
- Required mitigations
- Least-privilege install path
- Approval gates
- Post-install checks
- Recommendation

## References

- Read `references/safe-install-checklist.md` when producing install guidance or
  reviewing whether a skill is safe to enable.
