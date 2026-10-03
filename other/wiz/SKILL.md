---
name: wiz
disable-model-invocation: true
allowed-tools: mcp__wiz__discover, mcp__wiz__execute
description: Investigate the project's cloud security posture through the Wiz MCP (read-only), routing each query to the right domain and scoping to the project's own resources.
---

# Wiz (cloud security)

The Wiz MCP exposes ~250 tools across 24 security domains behind two gateway tools. You never call a Wiz tool directly: `discover` finds it, `execute` runs it. This skill is read-only: investigate, never mutate.

> **Setup:** this skill needs the Wiz MCP server enabled in `.claude/settings.local.json` and
> your own Wiz resource IDs in `.env` (see `.env.example`): `WIZ_REPO_BRANCH_ID` (the
> default-branch REPOSITORY_BRANCH resource for SAST) and `WIZ_CONTAINER_REPO_IDS` (the
> container-repository UUIDs for your images). Resolve them once per the "Resolve to IDs"
> section below, then fill them in — never hardcode real UUIDs in the repo.

## The loop

Every query takes the same four steps:

1. **Route.** Call `discover()` with no argument to list the domains. Pick the one domain that owns the answer by the *type of finding* you want, not by nouns in the question (see Routing traps).
2. **Spec.** Call `discover(domain)` for the exact tool `name` and its parameter schema. Read it: params that sound singular are usually **arrays** (`group_by`, `severity`, `status`, `asset_name`, `container_repository`), some are **required** (e.g. `list_issues_grouped` needs `group_by` + `type`), and the `first` / `limit` cap differs per tool (often 20). Never guess.
3. **Query.** Call `execute(tool_name, parameters)` with the exact `name` from step 2, scoped per the project section below. If `execute` rejects the name, re-run `discover(domain)` to confirm spelling (some names repeat across domains).
4. **Summarize.** A result too large for one response is auto-saved to a `tool-results/*.txt` file instead of returned. Parse it with jq or python (or hand the file to a subagent), never re-read it whole. Report a ranked summary (severity, then affected resource) with the Wiz finding IDs so the user can open each in the portal. Never paste raw JSON back.

Prefer a `*_grouped` tool with a small `first` over a raw list: fewer tokens, and it answers "where is the load" directly.

## Routing traps

Route by finding type. `discover()`'s own text carries "Do NOT use for X → Y" notes; these are the most-often mis-routed:

- **"AI" in the question does not mean the `ai_security` domain.** Route by what you want *about* AI: issues to `issues`, threats to `soc`, SAST to `codesec`, CVEs to `vulnerabilities`, sensitive data to `dspm`, compliance to `compliance`. Use `ai_security` only for the AI resource inventory itself.
- **Third-party CVE on a cloud resource or image goes to `vulnerabilities`; a first-party source-code weakness (SAST) goes to `codesec`.** "Issues in our images / repo" spans both: image CVEs are `vulnerabilities`, code flaws are `codesec`. Check both when the ask is broad.
- **A compliance framework score or cross-framework gap goes to `compliance`; a single misconfiguration or security rule goes to `cspm`.**
- **Cloud IAM (principals, entitlements, access keys, MFA) goes to `identity`; Wiz portal users and RBAC go to `settings`.**
- **EOL, outdated, or unsupported technology goes to `inventory`, not `container_security`.**

## Resolve to IDs (names lie)

A free-text name filter that returns zero does **not** mean the resource is absent: `asset_name: ["<project name>"]` can return nothing even though the project's images exist. Filter by the resource's Wiz UUID instead.

The fastest UUID source is a **Wiz portal URL**: its hash fragment encodes the exact filter IDs the view uses (`resource`, `containerRepository`, ...). Ask the user to paste the portal link for the view they mean, or read the IDs out of one they already sent. Otherwise resolve the UUID with a listing / inventory tool, then filter by it.

## The project in Wiz

Typically the project's code and images live under the source host and container registry (e.g. **GitHub / ghcr.io**), not the cloud account; only the running workloads are on the cloud provider (`cloud_platform: ["AWS"]` or equivalent, plus your prod account, cluster, and namespace). So a cloud-platform filter **hides** the image and SAST findings: scope those by the IDs below, not by cloud platform.

- **Source repo (SAST → `codesec` / `list_sast_findings`)**: `resource_id: ["${WIZ_REPO_BRANCH_ID}"]` (the default-branch REPOSITORY_BRANCH resource). Add `is_default_branch: true`.
- **Container images (CVEs → `vulnerabilities`)**: filter `container_repository` by the UUIDs in `${WIZ_CONTAINER_REPO_IDS}` — one per image the project ships.

Default `severity` to `["CRITICAL", "HIGH"]`, `status` to `["OPEN"]`, and add `has_fix: true` when the goal is to fix (only fixable findings are actionable). Per finding, `layerMetadata.isBaseLayer` and `artifactType.group` (`OS_PACKAGE` vs `CODE_LIBRARY`) say whether the fix is a base-image bump or a dependency bump.

```
execute("list_vulnerability_findings_grouped", {
  group_by: ["VULNERABLE_ASSET"], asset_type: ["CONTAINER_IMAGE"],
  container_repository: ["<UUID from $WIZ_CONTAINER_REPO_IDS>"],
  severity: ["CRITICAL", "HIGH"], status: ["OPEN"], has_fix: true, first: 20 })
```

## Before treating a finding as real

Wiz findings, SAST especially, carry false positives; verify against the code before proposing a fix. Read the flagged line. Example false-positive shapes: a weak hash (SHA-1, MD5) mandated by a protocol or used as a non-security checksum, a timer or callback API flagged as "eval", internal config dirs flagged as path traversal, and template rendering with escaping off that produces plain text rather than HTML.

## Read-only guardrail

This skill only investigates. Execute only read tools: names beginning `list_`, `get_`, or `search_`, plus `discover`.

Refuse any mutating tool: anything that creates, changes, resolves, assigns, deletes, reports, or configures (creating a pentest finding, an automation or remediation rule, a Jira or ServiceNow ticket, changing an issue's status). If the user wants one, say it is out of scope for this skill and point them to the Wiz portal.
