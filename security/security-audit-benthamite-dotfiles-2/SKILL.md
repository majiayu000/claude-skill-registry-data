---
name: security-audit
description: "Audit development-environment secrets, supply chains, macOS security controls, and Claude/Codex agent permissions. Use for environment security reviews, secrets checks, dependency audits, or periodic security posture assessments; use specialist skills for app-binary assessments or application-code reviews."
---

# Security audit

Audit the development environment and explain the exposure each finding
establishes. Honor the user's natural-language scope: a dependency-only request
selects that domain without requiring a literal flag. Run all four domains only
for a comprehensive environment audit. Explicit selectors are `--secrets`,
`--deps`, `--machine`, or `--agents`. Keep `--claude` as a compatibility selector for
the Claude-only portion of `--agents`. These are skill-request selectors, not
flags for a bundled all-domain scanner.

When reviewing or testing this skill itself, inspect its artifacts and use only
synthetic fixtures. Do not run the four domains against the real machine,
credentials, histories, account state or live agent configuration. Inspect test
entry points before running them; related repository suites include live checks.

An optional directory scopes secrets and dependency checks to that directory.
Without one, use the current directory plus configuration locations relevant
only to the selected domains. Machine checks concern the current Mac; agent checks
cover installed agents, their active account/profile configurations, and the
current project's overrides. State these roots before scanning; do not silently
expand into unrelated repositories or accounts.

Read the selected domain references completely before running their checks:

| Domain | Required reference |
|---|---|
| Secrets and credential incidents | [secrets](references/secrets.md) |
| Dependencies and other executable supply chains | [supply chain](references/supply-chain.md) |
| macOS controls, isolation, and recovery | [machine](references/machine.md) |
| Claude, Codex, MCP, plugins, and browser automation | [agents](references/agents.md) |

Independent domains may use subagents. Give each the resolved scope, relevant
reference, and all safety boundaries below. Deduplicate findings that cross
domains.

## Safety boundaries

An audit is read-only unless the user authorizes remediation. Do not rotate
credentials, change settings, install audit dependencies, resolve/build project
dependencies, activate project code, or mutate accounts while auditing.
Authorized remediation remains limited to the requested targets and actions.

Preserve the owner's guard policy. Repairing enforcement of an existing rule
does not authorize changing what the rule permits. A different rule requires
an explicit decision on that proposed policy; existing authorization for the
same change suffices. In Pablo's configuration, guards must allow or deny,
never introduce interactive approval prompts.

Before credential-related work, read
`~/My Drive/dotfiles/claude/context/secrets.md`. Use its personal/Epoch
placement and broker rules; this skill does not redefine them. For service
access use `claude/context/service-access.md`; for MCP placement use
`claude/context/mcp-servers.md`, resolved under that dotfiles root.

Never emit matching secret values or raw config/history lines. Use an approved
local scanner or metadata-only helper that reports path, line, type, and a
keyed fingerprint when necessary. Do not open vault contents, private keys,
browser cookies/session databases, or credential files for content inspection.
The bundled shell classifier supplies value-free output for shell-file reads
permitted by the guard; other checks must stay within the existing read policy. A
metadata-only output is not permission to bypass a denied input read.
Do not source a target shell file, load an editor config, run `direnv allow`,
start an MCP server, or execute a project-supplied scanner to inspect it.

Inspect a check's execution, output, and network effects before running it.
Capture and filter potentially sensitive stdout **and stderr** locally before
tool output reaches the transcript. Do not send secrets, config files, or
private dependency metadata to a remote scanner; verify the destination and
data scope for advisory queries. All temporary captures and sanitized artifacts
must be private (0700 directories, 0600 files), outside Drive, and cleaned up.
Do not treat redaction as permission to acquire a prohibited input. Mark
unavailable, unsafe, denied, or unsupported checks as not checked, with the
concrete reason. Do not weaken a guard to complete a check.

## Threat model and evidence

Assume a dependency or agent workflow could execute malicious code. Assess
which files, authenticated services, devices, and credentials that process can
reach, and how the owner would recover. Consider credential theft/phishing,
physical loss, persistence, and prompt injection where relevant.

OS permissions and actual sandbox/VM boundaries constrain processes. A browser
profile separates browser state; it does not protect another profile from
malware running as the same OS user. A VM application's presence does not
establish isolation. Per-process secret injection reduces inheritance but still
exposes the injected values to that process and its descendants; same-user OS
process inspection can expose them to peers too. Test that channel with the
synthetic fixture described in the agents reference when evaluating credential
isolation. Encryption at rest does not establish protection while data is unlocked.

Distinguish a configured control from an observed effective control. Use safe
synthetic fixtures to verify a guard's decisions or isolation behavior when
needed; never probe with actual credentials or destructive actions. Do not
equate installed tools, hook counts, famous publishers, or a scanner's silence
with security. Keep an unverified claim explicitly unverified.

## Report

Give a compact coverage table per selected domain: checked (with or without a
finding), not checked (reason), or not applicable (reason). Identify roots,
tool versions, and reference dates only where they affect the conclusion.
Track skipped subchecks so a partial scan cannot look complete.

For each deduplicated finding include location, observed evidence, confidence,
the concrete exposure and affected workflow, severity rationale, and a scoped
remedy. Separate findings from optional hardening and unresolved questions.

- Critical: evidence of an immediately consequential exposure, such as a
  currently usable credential exposed publicly or active compromise.
- High: an established, substantial access or execution path to sensitive assets.
- Medium: a material control gap with a plausible but constrained exposure.
- Low: an established limited-impact gap. Keep optional hardening separate from
  vulnerability findings rather than assigning it a severity by default.

A scanner match is a candidate until classified; do not test a credential's
live validity without authorization. Advisory severity, local exposure,
confidence, and fix availability are separate facts. Keep relevant unfixed
transitive and dev-tool vulnerabilities visible; no upgrade path does not
remove the risk. Do not label a whole domain safe when consequential checks
were unavailable.

End with the material risk and coverage limits, plus prioritized do/skip/defer
recommendations. If remediation was authorized, perform it within that scope
and verify the reported behavior before claiming it resolved.
