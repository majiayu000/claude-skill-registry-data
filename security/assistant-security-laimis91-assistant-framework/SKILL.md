---
name: assistant-security
description: "Analyzes threats, vulnerabilities, dependencies, and attack surfaces. Use for security work, and before changing auth, external input, secrets, sensitive data, persistence, network or shell calls, dependencies or config, or external integrations."
requires:
  - assistant-review
---

# Analyze Security Risks

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Inspect the requested surface and report concrete attack paths, their impact, and the smallest useful remediation. Infer scope and method from context; ask only when missing source, access, or deployment facts prevent a trustworthy conclusion. Keep analysis read-only unless remediation is authorized. When the request is to decide what to do with an incoming security advisory or vulnerability report rather than to analyze code, use `assistant-advisory-triage`.

Load the relevant reference, using only checklist categories that apply:

| Analysis | Reference | Focus |
|---|---|---|
| Threat model | `threat-model.md` | Trust boundaries and threats; STRIDE where useful |
| Code review | `code-review.md` | Reachable vulnerabilities in changed code |
| Dependency audit | `dependency-audit.md` | Actual dependency versions and exposure |
| Attack surface | `attack-surface.md` | Entry points, privileges, and integrations |
| Agent and tool authority | `agent-authority.md` | Untrusted content steering agents and tools, delegated authority, approval binding, durable context |
| Installer and filesystem ownership | `install-boundaries.md` | Writes to user-owned or shared locations: markers, links, shared roots, path overlap, sentinels |
| Dependency and release provenance | `release-provenance.md` | Who influences resolution, artifact identity, CI as authorization, which release contains a fix |

Load a boundary companion (the last three rows) only when the assessed target has that surface: agent, tool, prompt, memory or task-state flows; installer or other writes to user-owned files; dependency resolution, CI or release artifacts. An ordinary web or API request loads none of them.

For a detailed requested threat model, `prompts/threat-model.md` provides additional prompts. Check relevant paths such as authentication/authorization, tenant isolation, untrusted input, data access, shell/process execution, file paths, network integrations, serialization, dependency/configuration risk, and privacy/logging. Do not turn an irrelevant category into a finding.

Each finding needs specific redacted evidence (file/line, configuration, dependency, or threat path), a reachable attack or misuse path, impact, severity, remediation, and a verification step. Separate demonstrated behavior from assumptions. Do not invent vulnerabilities or report generic advice as findings.

Every reported security item is in one of two states:

- **Confirmed**: the source trace and observed or bounded local evidence establish the lower-trust actor, the input or action, the crossed boundary, the affected principal or resource, and the result. Only confirmed items are findings and receive severity.
- **Needs validation**: a specific source-grounded boundary hypothesis is blocked on a named runtime, deployment, provider or host fact. State the hypothesis, that blocking fact, and a safe check an owner can run. It carries no severity.

Generic advice that is neither is not reported. In prose output, list needs-validation items under a **Needs validation** heading, separate from the findings. Respect the requested severity threshold and order findings by material risk.

Use a consistent severity scale:

- **critical**: immediate exploitation or breach risk;
- **high**: significant vulnerability needing attention before release;
- **medium**: material weakness with limited or conditional exploitability;
- **low**: minor exposure or defense improvement.

State the assessed scope, result, and confidence; report residual risks, inaccessible areas, and evidence gaps that limit a clean conclusion. Omit empty reporting sections. If structured output is requested, preserve `findings` with `severity`, `category`, `description`, `impact`, and `remediation`; include evidence and attack path, `summary`, highest material `risk_level` (or `none`), and prioritized `action_items` when findings require fixes. Put needs-validation items in a separate `needs_validation` list (each with `hypothesis`, `blocking_fact` and `safe_check`), never in `findings`. When this perspective runs inside a Review specialist pass that returns the canonical Reviewer schema, map each needs-validation item to an `observations` entry with the blocking fact in `evidence_gap` and the owner check in `follow_up`, never to `findings`.

For an explicit full or comprehensive audit, list the assessed surfaces, the blocked surfaces with their blocker, and the excluded or out-of-scope surfaces with the reason. Call the audit complete, or report no findings for it, only when no in-scope surface is blocked or unassessed; otherwise label it partial.

Never paste, log, or repeat secret values; redact and cite location only. Use local/repo-native checks where available. Do not claim OS-level isolation the host does not enforce. Running target scripts or installers stays within existing authorization, and fixture execution follows assistant-review's `script-execution.md` rules; when a check needs isolation that is unavailable, report the item as needs validation with a safe validation plan. Do not upload proprietary code, install scanners, or call external scanning services without authorization. If a credential exposure or active exploit path is found, promptly report the redacted evidence and required containment within the authorized scope; do not claim broad safety from inaccessible evidence or perform unapproved remediation.
