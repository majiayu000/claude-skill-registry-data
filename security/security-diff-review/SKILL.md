---
name: security-diff-review
description: "Routes an authorized Git diff security review to the original native security-diff-scan skill."
---

# Security Diff Review

Load and follow the complete original `codex-security:security-diff-scan`
skill exposed by the current host. Its references, capability preflight,
findings and completion contracts remain native author responsibilities.
This adapter selects the provider and does not reproduce its scan stages.

If the original provider or a required capability is missing, the route is
unavailable. Use the host's official Codex Security plugin setup to install
or enable it and refresh session exposure. Do not use abbreviated local
scan steps as a counterfeit fallback or claim completion from registration.

## Owner Policy

- Review authorized code and the user's selected Git range or working-tree
  patch. Preserve unrelated changes and private machine state.
- Review-only by default; do not patch findings without an explicit fix
  request. Route authorized remediation to `fix-security-finding`.
- Keep exploitability, confirmed findings and unknowns tied to source evidence.
- Return the original provider's report and actual coverage, validation
  results and unresolved gaps. A failed or skipped gate is not PASS.
