---
name: connect-an-ai-client
description: Connect an AI client (Claude Code, Claude Desktop, or any MCP client) to the Wandering OS MCP server to ask about trips — anonymous, friend-token, or owner tier.
---
# Connect an AI client

The MCP (Model Context Protocol) server at `https://travel.michaelwheeler.ai/mcp` is a read-only,
stateless streamable-HTTP endpoint over the trip graph: 8 tools, 2 resources
(`graph://schema`, `graph://stats`), 8 slash-command prompts. Trip data is
public on purpose; every answer is privacy-scrubbed for every tier.

## Read first
- services/mcp/README.md — Connect section, the eight-tools table, access tiers, and ground rules.
- docs/GETTING_STARTED.md — the live-surfaces table (fallback URL until the DNS delegation lands).

## Commands
```bash
# anonymous (public tier — full read toolset)
claude mcp add --transport http wandering-os https://travel.michaelwheeler.ai/mcp

# friend or owner tier
claude mcp add --transport http wandering-os https://travel.michaelwheeler.ai/mcp \
  --header "Authorization: Bearer <token>"
```
Client can't send headers? Append `?token=<token>` to the URL. Mint tokens with `just mint-token --role friend --label alice --ttl 30d` (see mint-and-revoke-tokens).

## Gotchas
- The DNS delegation is live for the production deploy, so the primary URL works. On a fresh account before the delegation lands, the working fallback is the CloudFront domain plus `/mcp` (for production, `https://d2na1bvnmer5k1.cloudfront.net/mcp` — see the live-surfaces table). The raw Lambda Function URL is origin-locked — it 403s any caller that is not CloudFront — so it is never usable directly.
- Friend and anonymous see identical data today; friend is the trusted tier future features hang off. Owner unlocks exactly one thing: presigned links for non-image attachments (raw video/audio keep embedded GPS).
- A presented-but-invalid token gets 401 even though anonymous access is open — it never silently downgrades to public.
- Rate limit: 300 requests / 5 min / IP (WAF). Attachment links expire after 15 minutes — ask again.
- Tell clients to read `graph://schema` before using `query_graph`; writes are rejected twice (guard regex + read-only transaction) and `LIMIT 200` is injected when absent.
