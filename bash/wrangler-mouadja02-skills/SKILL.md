---
name: wrangler
description: >-
  Runs Cloudflare Wrangler CLI work: deploying and tailing Workers, managing KV, R2, D1, and Queues,
  secrets, bindings, and account routing. Use when deploying to Cloudflare Workers or debugging a
  Wrangler deploy or account mix-up.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
license: MIT
---

# Wrangler

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

## When to Use

- Deploying or tailing Cloudflare Workers
- Managing KV namespaces, R2 buckets, D1 databases, or Queues via CLI
- Debugging Wrangler account routing or deploy failures

Use for Cloudflare Wrangler CLI work: deploys, tails, KV/R2/D1/Queues/Workers, secrets, bindings, and account routing.

## Defaults

- Retrieval first for flags/config: `wrangler --help`, subcommand `--help`, local `node_modules/wrangler/config-schema.json`, then Cloudflare docs.
- Prefer repo wrapper: `npm exec --yes --package wrangler -- wrangler ...` unless repo has its own script.
- `wrangler whoami` before account-sensitive work.

## Quick Commands

```bash
# Check auth
npm exec --yes --package wrangler -- wrangler whoami

# Deploy
npm exec --yes --package wrangler -- wrangler deploy

# Tail logs
npm exec --yes --package wrangler -- wrangler tail <worker> --format json --sampling-rate 0.999 --search '<term>'

# KV operations
npm exec --yes --package wrangler -- wrangler kv key list --namespace-id <id> --prefix '<prefix>'
npm exec --yes --package wrangler -- wrangler kv key get '<key>' --namespace-id <id>
```

## Pitfalls

- Do not invent flags from memory. Wrangler 4 removed/changed some old flags; confirm with `--help`.
- `wrangler kv key list` has no `--limit`; use `--prefix` and filter locally.
- Run Wrangler KV/list/get/admin reads serially when workerd/local storage starts up; parallel runs can hit SQLite `SQLITE_BUSY`.
- `wrangler tail --sampling-rate` must be `>0` and `<1`; use `0.999` for near-full sampling, not `1`.
- Stop tails you start. Kill the exact `wrangler tail <worker>` process when done.
- Never print secrets. Query exact secret names only; do not dump env.

## Account Check

For repo config, read `wrangler.toml` / `wrangler.json` before commands. If config account and intended product disagree, stop and ask.

```bash
cat wrangler.toml | grep -E "account_id|name ="
npm exec --yes --package wrangler -- wrangler whoami
```
