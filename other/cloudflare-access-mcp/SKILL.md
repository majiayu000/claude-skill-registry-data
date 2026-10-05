---
name: cloudflare-access-mcp
description: Use when the request is specifically about Cloudflare Access app OAuth, DCR, redirect URIs, Access policies, or MCP connector authentication for this workspace. Do not use for tunnel ingress, DNS, WARP, Zero Trust device policy, or zone-edge security review.
runtime_projection: true
source_of_truth: registry/skills/cloudflare-access-mcp/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-access-mcp/SKILL.md`
> Source of truth: `registry/skills/cloudflare-access-mcp/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Cloudflare Access MCP

## Scope

- Access applications
- OAuth metadata and DCR
- Redirect URI allowlists
- Policies for ChatGPT or other MCP clients

## Use This Skill When

- A connector login fails with invalid redirect, invalid target, or OAuth errors.
- You need to add or verify callback URLs for ChatGPT or another MCP client.
- You need to inspect Access app policy coverage or OAuth metadata.

## Do Not Use This Skill When

- The issue is about local WARP or Zero Trust device behavior.
- The issue is about tunnel routing, hostname mapping, or DNS records.
- The issue is about WAF, browser checks, or bot rules.

## Checks

- Access app ID and name
- OAuth enabled state
- DCR enabled state
- Redirect URIs
- User and service-token policies

## References

- [workspace baseline](../../../registry/skills/cloudflare-governance/references/current-baseline.md)

## Escalate

- Use [cloudflare-governance](../../../registry/skills/cloudflare-governance/SKILL.md) first for broad Cloudflare review or when the issue also involves Tunnel, DNS, edge security, runtime drift, or WARP device policy.
