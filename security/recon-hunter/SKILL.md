---
name: recon-hunter
description: >
  Full-stack recon-to-bug pipeline. Runs passive enumeration, attack surface mapping and
  bug discovery in one continuous flow, then ranks findings with copyable PoCs. Triggers on:
  "recon", "enumerate", "subdomain", "find bugs", "attack surface", "map the target",
  "what's exposed", "scan this", or any domain handed over without further instruction.
  Use for unauthenticated coverage before authenticated testing begins.
tags: [recon, enumeration, osint, subdomain, takeover, secrets, bug-bounty]
version: "2.0"
---

# RECON-HUNTER — Full Recon + Bug Discovery Pipeline

**One rule: impact first. Only report what an attacker can abuse right now.**

This skill drives the `bb_recon` MCP server, which implements the pipeline as
tools. Prefer the tools over raw shell: they enforce scope, keep an audit trail,
apply the triage kill rules, and work without a Go toolchain installed.

---

## PHASE 0 — Scope (mandatory, do this first)

Every active tool refuses to run until scope exists. This is deliberate: it is
the difference between a pentest and an unauthorised scan.

```
scope_set(include=["*.target.com", "203.0.113.0/24"], exclude=["blog.target.com"])
```

- Wildcards cover the apex and all subdomains; a bare host is exact-match only.
- Loopback, RFC1918 and `169.254.169.254` are blocked unless `allow_private=True`
  — set that only for an internal engagement.
- `scope_check(targets=[...])` tests hosts without touching them. Use it on
  anything enumeration turns up before pivoting to it.

Every active call is appended to `audit.jsonl` in the output directory, before
the packets go out.

## HowToHunt Advanced Supplement — Sensitive Info & Origin Discovery

> **Source:** [KathanP19/HowToHunt — Sensitive_Info_Leaks, FindOriginIP, Recon](https://github.com/KathanP19/HowToHunt) (1878+ lines of dorks). Licensed GPL-3.0.

**After standard pipeline, run these HowToHunt dorks for extra coverage:**

```bash
# GitHub dorks (via GitHub search or gitleaks)
# From Sensitive_Info_Leaks/Github_dorks_all.md
org:target "api_key" OR "secret" OR "password"
org:target filename:.env OR filename:config.json
# Shodan (from Shodan_cve_dorks.md)
http.favicon.hash:123456 target.com
ssl:"target.com" http.html:"dashboard"
# Google dorks (from Google_Dorks.md)
site:target.com ext:env OR ext:sql OR ext:log
site:target.com inurl:admin | inurl:dashboard
# Origin IP (from FindOriginIP)
dig +short target.com; curl -s https://ipinfo.io/<IP> | jq .org
# Historical DNS: https://securitytrails.com/domain/target.com/dns
subfinder -d target.com | dnsx -silent | grep -v "104.21."
```

These find secrets, exposed configs, and WAF bypass origins that `bb_recon` tools may miss. Log results as `intel` with tags `sensitive-data` and `origin-ip`.

---

## FAST PATH

For a domain with nothing else specified:

```
scope_set(include=["*.target.com"])
recon_pipeline(domain="target.com")
```

That runs every phase below and returns a ranked report. The phases exist
separately for when you need to go deeper on one of them.

---

## PHASE 1–2 — Enumeration and resolution (passive)

```
subdomain_passive(domain="target.com")     # crt.sh + agniops + crt.name + subfinder
subdomain_resolve(domain="target.com")     # dnsx, falling back to socket resolution
```

Prioritise `dev-`, `staging-`, `internal-`, `admin-`, `api-` prefixes — the
pipeline surfaces these as `interesting_envs`.

## PHASE 3 — Live surface (active)

```
http_probe(domain="target.com")
```

`401`/`403` on admin or internal hosts → queue for auth-bypass testing.
`500` → server errors, injection surface.

## PHASE 4 — Subdomain takeover (active)

```
takeover_scan(hosts=["a.target.com", "b.target.com"])
```

Reports `high` only when the CNAME delegation **and** the unclaimed-service
fingerprint agree. Report `high` findings; treat `medium`/`low` as leads needing
manual proof. A bare "404 Not Found" body is not a takeover.

## PHASE 5 + 13 — Historical URLs, juicy files, injection candidates (passive)

```
url_harvest(domain="target.com")
probe_juicy_files(urls=[...])              # active: which archived files still serve
```

Parameterised URLs are deduplicated by (host, path, parameter set), so a corpus
of 4000 `?id=N` URLs collapses to the one endpoint it represents.
`ssrf_candidates` flags both known parameter names and URL-shaped values.

## PHASE 8 — JavaScript secrets and endpoints (active)

```
js_intel(targets=["https://app.target.com"])
```

Only JS served from in-scope hosts is analysed — third-party CDN bundles are not
the program's asset.

**Secrets are detected, never validated.** Each finding carries a `validate`
command. Run it yourself, after confirming the key belongs to the program: that
request authenticates as the victim against a third party and is logged on an
account nobody in the engagement controls.

## PHASE 10 — Cloud storage (active)

```
cloud_buckets(domain="target.com")
```

Only `exposed` entries are findings. `private` means the bucket exists but denies
listing — the triage rules discard those. `missing` names are unclaimed.

## PHASE 11 + 12 + 14 — Exposed config, CORS, GraphQL (active)

```
exposure_scan(targets=["https://app.target.com"])
```

Each host gets a random-path baseline first, and every hit must both differ from
that baseline and match a content signature. A 200 alone proves nothing — SPA
catch-all routes answer 200 for any path you invent.

---

## PHASES NOT IN THIS SERVER

Port scanning, directory fuzzing, nuclei and screenshots need external binaries.
Use the `scanning` MCP (nuclei, nmap, sqlmap, ffuf) rather than duplicating them
here. `ensure_tools` installs the CLIs if they are missing.

---

## SEVERITY KILL RULES

The pipeline applies these when assembling the report, so they should not reach
you. Apply them manually if you ran the phases separately:

- **KILL** — takeover candidate below `high` confidence
- **KILL** — CORS reflection without `Access-Control-Allow-Credentials: true`
- **KILL** — S3/GCS/Azure bucket that exists but denies listing
- **KILL** — GraphQL endpoint with introspection disabled
- **KILL** — exposed path whose body matches the host's random-path baseline
- **DOWNGRADE** — secret confirmed live but read-only scope
- **KEEP** — any secret that authenticates successfully

## PROOF-OF-CONCEPT STANDARD

Every finding the pipeline emits ships a `poc` a triager can run in 60 seconds.
Keep it that way when writing up.

Data exfiltration cap: **50 records**. Prefer `?shallow=true`, `?limit=1`,
`COUNT(*)` over bulk pull. Proving access is the goal; taking the data is not.

## COVERAGE LEDGER

```
recon_status(domain="target.com")
```

Returns which phases have run and which remain. Recon is not done until
`complete` is true or you have a reason for each skip.
