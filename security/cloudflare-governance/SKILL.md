---
name: cloudflare-governance
description: Use as the default entrypoint for broad Cloudflare requests when the user has not already named a narrower specialist. Covers Cloudflare governance, family-wide audit, WARP and Zero Trust device policy triage, tunnel and DNS review, Access and MCP auth review, edge security review, API credential discovery, and local runtime correlation. Do not use for deep specialist procedures when the request is already clearly about one narrow area.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/cloudflare-governance/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-governance/SKILL.md`
> Source of truth: `registry/skills/cloudflare-governance/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Cloudflare Governance

## Purpose

This is the default routing skill for Cloudflare-related work in this workspace.

## First 60 Seconds

1. Decide whether the request is broad or already narrow.
2. Identify whether the active evidence is local, account-level, zone-level, or mixed.
3. Confirm what credentials are available.
4. Route to one primary specialist and only add a secondary specialist when the issue is clearly mixed-scope.

## Use This Skill When

- You need to decide which Cloudflare sub-skill should handle the task.
- You want a broad baseline check before a narrower action.
- You need a dry-run summary that spans more than one Cloudflare layer.
- You need to discover which Cloudflare script should run first.

## Do Not Use This Skill When

- The user already named a specialist skill and the request is clearly within that scope.
- The task is purely `wrangler` CLI or Cloudflare platform product selection rather than governance.

## Route To

- WARP client, Zero Trust device policy, split tunnel vs full tunnel, or API auth: [cloudflare-zerotrust-device](../../../registry/skills/cloudflare-zerotrust-device/SKILL.md)
- Access and OAuth or DCR: [cloudflare-access-mcp](../../../registry/skills/cloudflare-access-mcp/SKILL.md)
- Tunnel and DNS: [cloudflare-tunnel-dns](../../../registry/skills/cloudflare-tunnel-dns/SKILL.md)
- Edge security and WAF: [cloudflare-edge-security](../../../registry/skills/cloudflare-edge-security/SKILL.md)
- Local runtime sync and release state: [cloudflare-runtime-sync](../../../registry/skills/cloudflare-runtime-sync/SKILL.md)

## Baseline

- [current-baseline.md](references/current-baseline.md)
- [dry-run-report.md](references/dry-run-report.md)
- [workflow-guide.md](references/workflow-guide.md)
- [routing-matrix.md](references/routing-matrix.md)
- [script-catalog.md](references/script-catalog.md)
- [cloudflare-family-review-checklist.md](references/cloudflare-family-review-checklist.md)
- [family-review-2026-04-17.md](references/family-review-2026-04-17.md)
- [scripts/inventory-cloudflare-scope.ps1](scripts/inventory-cloudflare-scope.ps1)

## Handoff Rule

- Start here when the task touches more than one Cloudflare layer.
- Route to `cloudflare-zerotrust-device` when the task is primarily about local WARP state, Zero Trust device policy, split tunnel vs full tunnel, or Cloudflare API credential checks.
- Route down to a focused sub-skill once the active change surface is clear.
- Route back here if the task expands across Access, Tunnel, DNS, edge security, and runtime state.
- Keep governance thin: classify, route, and summarize. Do not duplicate the deep operational procedures that live in the specialist skills or scripts.
