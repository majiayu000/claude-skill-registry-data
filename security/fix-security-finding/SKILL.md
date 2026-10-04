---
name: fix-security-finding
description: "Routes an explicitly requested security fix to the original native fix-finding skill with owner authorization and scope rules."
---

# Fix Security Finding

Use only when the user explicitly asks to fix and verify a security
vulnerability. Load and follow the complete original
`codex-security:fix-finding` skill exposed by the current host, including its
references and remediation-stage constraints. Preserve native ownership;
this adapter does not reproduce the patch or verification workflow.

If the original provider or a required capability is missing, the route is
unavailable. Use the host's official Codex Security plugin setup to install
or enable it and refresh session exposure. Do not silently substitute a
condensed local fix procedure or report a pending provider as completed.

## Owner Policy

- The user's finding, target and authorized remediation stage bound the work.
  Preserve unrelated findings, local changes and legitimate behavior.
- Review authorization does not authorize fixes, and preparation does not
  authorize deployment or publication. Reuse authorization already granted.
- Protect credentials, private runtime configuration and raw sensitive data.
- Report the original provider's actual outcome, changed files, exact
  validation results and remaining proof gaps without weakening its evidence.
