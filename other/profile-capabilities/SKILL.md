---
name: profile-capabilities
description: "Use when discovering this profile's skills or optional integrations."
version: 1.0.0
author: Hermes Profile Packs contributors
license: AGPL-3.0-only
---

# Capabilities for hermes-wear

Wrist-first assistant: concise, voice-friendly, safe capture and device-awareness without inventing device capabilities.

## Role-specific selection

Retain all wrist and device-awareness skills and restricted toolsets. No shell-dependent bundle or remote account integration; capability guide explains safe discovery and offline degradation.

- No additional execution skill: existing specialist workflows already cover this scope.

## Procedure

1. Prefer the existing role-owned workflow and native Hermes tools. Load one matching supplemental skill on demand with `skill_view`; never preload the whole catalog or duplicate a capability via a connector and MCP.
2. Read `references/catalog.json` with `skill_view(name="profile-capabilities", file_path="references/catalog.json")` for exact optional integration pins, prerequisites, privacy/egress disclosures, setup and fallback decisions. A listed integration is not an installed or authenticated integration.
3. All external plugins/MCPs are explicit opt-ins. Do not connect, download, launch, authenticate, schedule, upload records/code, or change live configuration merely because a profile was installed. Even anonymous hosted services disclose queries. Native read/search/file/browser tools remain the fallback when available and authorized.
4. If the user chooses an integration, inspect current `hermes` CLI help, exact profile identity, existing connectors and enabled state. Obtain consent for the named service, transmitted data, costs and permissions. Use supported Hermes UI/CLI; never edit live YAML, bypass TLS, ask for secrets in chat, or copy credentials between profiles.
5. Plugin commands in the catalog stage reviewed code disabled without dependency installation. Review current capability and dependency consent before a separate enable action. Warning: native `plugins pack install` enables plugins; `references/hermes-pack.yaml`, if present, is an explicit activation recipe, NOT disabled staging. Use the individual `--no-enable --no-deps` catalog commands for staging, and never invoke pack install during profile provisioning.
6. Fresh installs may contain disabled MCP config seeds. Existing-profile updates preserve user config: compare `references/mcp-servers.json` when present and use supported MCP setup only after approval. Do not reset the whole config or overwrite existing accounts. MCP sampling is disabled; pruning/allowlisting tools and provider authentication are separate decisions.
7. Read back exact enabled state and tools after any approved change. Test a non-sensitive read. Report credential/setup/network failures honestly; do not pretend a failed lookup returned no data. Account for reload/new-session effects; never restart a gateway implicitly.
8. Preserve user customizations. Native distribution updates replace shipped skill roots, but unrelated skill roots survive. Review same-name local collisions before updating; do not claim user-edited shipped skills are protected. Rollback is a reviewed source revision plus a separate approved installed-state restore, never deleting all skills or secrets.

## Boundaries

Installing this pack does not widen role authority or tool permissions. Council retains minimum-necessary personal context and professional-advice boundaries. Academy retains teaching, assessment and CE routing contracts. Coordination profiles remain coordination-only. Wear must keep wrist-first output, device capability verification, backend approvals, and its disabled execution toolsets; unavailable device tools mean no action, not invented success.
