---
name: cloudflare
description: Run every Cloudflare job through the official `cf` CLI - domains, DNS, Workers deploys, secrets and custom domains, KV, D1, R2, WAF, SSL and cache. Use when the user mentions Cloudflare, cf, DNS, a domain, deploy, Workers, KV, D1, R2, CDN, SSL or cache.
---

Use the official `cf` CLI (`npm i -g cf`) for every Cloudflare action. Never Wrangler, an S3 SDK script or raw calls to api.cloudflare.com; if `cf` cannot do something, say so and stop. The Cloudflare connector in Claude can help for reads, but changes go through `cf`.

```bash
cf --version                 # missing: run the setup-cloudflare skill
cf auth whoami               # must say "authenticated": true
cf auth login                # OAuth in the browser, the user grants every scope, sensitive ones included
```

When `cf` stops with "More than one account available", run `cf accounts list` and `export CLOUDFLARE_ACCOUNT_ID=<id>` for the session. Zone commands take `-z <domain or zone id>`. Never print tokens or read the `cf` config file.

Find any command instead of guessing it, with generic queries (action + resource type, no names or ids):

```bash
cf cli search "<what you want to do>"     # JSON matches
cf <discovered command> --help              # flags of that command
cf schema <command without the leading cf>  # exact API request body
```

The commands used most:

```bash
cf zones list
cf dns records list -z <domain>
cf dns records create -z <domain> --body '{"type":"CNAME","name":"www","content":"target","proxied":true}'
cf init <dir> && cf dev        # then cf build, cf deploy
cf r2 buckets list
cf r2 objects put <key> --bucket-name <bucket> --file <path> --content-type <mime>
```

Everything else (DNS update or delete, Worker custom domain, secrets, routes, crons, KV, D1, cache purge, SSL, WAF, Access, email routing, DNSSEC, analytics) goes through `cf cli search "<job>"`. Add `--local` to simulate KV, D1 and R2 objects. Subcommand names follow the CLI release: if one errors, search it.

Every mutating command accepts `--dry-run`. Confirm with the user before anything destructive (DNS deletes, zone changes, purges), and pass `--force` only after their yes.

When another service (Lumail, Stripe, Google, a mail provider) shows DNS records to add, create each one exactly as given (type, name, content, priority, TTL), keep mail and verification records unproxied (`"proxied": false`), then list the zone to confirm they exist.
