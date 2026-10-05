---
name: cloudflare-tunnel-dns
description: Use when the request is specifically about Cloudflare Tunnel inventory, DNS hostnames, ingress routing, credentials files, or health endpoints for this workspace. Do not use for local WARP behavior, Access OAuth, or zone-edge security review unless the incident clearly spans those layers.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/cloudflare-tunnel-dns/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/cloudflare-tunnel-dns/SKILL.md`
> Source of truth: `registry/skills/cloudflare-tunnel-dns/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Cloudflare Tunnel DNS

## Scope

- Tunnel IDs and credentials files
- DNS hostnames for MCP and health
- Ingress to local ports
- Public endpoint reachability

## Use This Skill When

- You need to confirm the active tunnel target.
- You need to update hostname to ingress mappings.
- You need to verify health and MCP routes from the public edge.

## Do Not Use This Skill When

- The issue is only about WARP, split tunnel vs full tunnel, or local Zero Trust device policy.
- The issue is only about Access OAuth, DCR, or redirect URIs.
- The issue is only about WAF, browser check, or bot policy.

## Checks

- Tunnel ID and name
- Credentials file path
- Hostname -> local port mapping
- `/health` and `/mcp` routing

## Change Guardrails

- Before adding a new tunnel, hostname, or ingress rule, capture the health of existing active tunnels and their public health endpoints.
- After adding or starting a new tunnel, re-run the same health checks for the pre-existing tunnels and compare results before treating the change as successful.
- Do not trade one working tunnel for another without calling out the regression and the exact service, config file, and hostname affected.

## References

- [workspace baseline](../../../registry/skills/cloudflare-governance/references/current-baseline.md)
- [scripts/check-tunnel-runtime-alignment.ps1](scripts/check-tunnel-runtime-alignment.ps1)
- [scripts/plan-staging-public-host-activation.ps1](scripts/plan-staging-public-host-activation.ps1)

## Escalate

- Use [cloudflare-governance](../../../registry/skills/cloudflare-governance/SKILL.md) first for broad Cloudflare review, or when hostname routing changes also require Access policy, edge security, runtime review, or WARP/device investigation.
- Use [cloudflare-zerotrust-device](../../../registry/skills/cloudflare-zerotrust-device/SKILL.md) when the request is primarily about WARP pathing or full-tunnel vs split-tunnel behavior.
