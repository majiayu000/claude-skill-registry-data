---
name: cloudflare
description: Use when building or reviewing Cloudflare platform projects and you need the official Cloudflare product decision trees for workers, storage, AI, networking, security, or infrastructure-as-code.
---

# Cloudflare Platform Skill

This skill is for Cloudflare product selection and platform architecture.
For workspace operational work such as WARP, Zero Trust, Access, Tunnel, DNS, or edge-policy review, start from [cloudflare-governance](../cloudflare-governance/SKILL.md).

## Use This Skill

- When you need to choose the right Cloudflare product or service.
- When you are building or reviewing Cloudflare platform work across Workers, Pages, storage, networking, security, AI, or IaC.
- When you need official Cloudflare product decision trees before writing code or config.

## Quick Decision Trees

### I need to run code

- Serverless functions at the edge -> Workers
- Full-stack web app with Git deploys -> Pages
- Stateful coordination or real-time -> Durable Objects
- Long-running multi-step jobs -> Workflows
- Run containers -> Containers
- Multi-tenant customer-deployed code -> Workers for Platforms
- Scheduled tasks -> Cron Triggers
- Lightweight edge logic -> Snippets
- Process execution events -> Tail Workers
- Optimize latency to backend infrastructure -> Smart Placement

### I need to store data

- Key-value -> KV
- Relational SQL -> D1 or Hyperdrive
- Object/file storage -> R2
- Message queue -> Queues
- Vector embeddings -> Vectorize
- Strongly consistent per-entity state -> Durable Objects
- Secrets management -> Secrets Store
- Streaming ETL to R2 -> Pipelines
- Persistent cache -> Cache Reserve

### I need networking or security

- Expose local service to internet -> Tunnel
- TCP/UDP proxy -> Spectrum
- WebRTC TURN server -> TURN
- Private network connectivity -> Network Interconnect
- Optimize routing -> Argo Smart Routing
- Web Application Firewall -> WAF
- DDoS protection -> DDoS Protection
- Bot detection or management -> Bot Management
- API protection -> API Shield
- CAPTCHA alternative -> Turnstile

### I need AI or media

- Run inference -> Workers AI
- AI gateway or AI search -> AI Gateway or AI Search
- Build stateful AI agents -> Agents SDK
- Image optimization -> Images
- Video streaming -> Stream
- Browser automation or screenshots -> Browser Rendering
- Third-party script management -> Zaraz

### I need IaC

- Use Pulumi, Terraform, or the REST API when you are managing Cloudflare infrastructure as code.

## References

- Use the Cloudflare docs for the specific product you selected.
- Prefer product-specific skills when the task is narrow.

## Route To

- Use [wrangler](../wrangler/SKILL.md) when the task is primarily `wrangler` CLI, `wrangler.jsonc`, deploy, or local dev.
- Use [building-mcp-server-on-cloudflare](../building-mcp-server-on-cloudflare/SKILL.md) when the task is specifically about remote MCP servers on Workers.
- Use [cloudflare-governance](../cloudflare-governance/SKILL.md) when the task is operational or administrative and spans Access, Tunnel, DNS, edge security, Zero Trust, WARP, or local runtime state.
