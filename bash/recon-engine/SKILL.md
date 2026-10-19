---
name: recon-engine
description: Two-engine recon for authorized bug bounty / attack-surface mapping. PASSIVE brain (scripts/recon.py, stdlib, no keys, sandbox-safe) collects subdomains/URLs/IPs/providers from crt.sh, Shodan CTL, HackerTarget, CertSpotter, urlscan, Wayback, VirusTotal (with VT_API_KEY) and RDAP into BadRecon-style artifacts (subdomains.csv, urls.csv, ips.csv, providers.json, recon_notes.md, FINDINGS.md), scope-matched. ACTIVE muscle (scripts/recon.sh) chains the Go bug-bounty suite (subfinder, dnsx, waybackurls/gau, katana, gospider, httpx, + opt-in nuclei/gowitness/gitleaks/arjun/naabu/subzy) for DNS brute-force, live crawling, HTTP probing, ~30-bucket URL classification and opt-in active checks — runs on the USER's own machine with those tools, never in the sandbox. Use whenever the user asks for recon, subdomain enumeration, attack-surface mapping, "find subdomains/URLs/assets for X", or "run recon on" any target.
---

# Recon Engine — passive brain + active muscle

Two engines, one skill. The skill is the **brain** (scope, decisioning, triage,
handoff); the scripts are the **muscle** (enumeration).

- **`scripts/recon.py` — passive engine.** Stdlib Python, no keys required, safe to run
  anywhere including this sandbox. Multi-source intelligence collection; the only traffic
  touching the target is optional DNS resolution.
- **`scripts/recon.sh` — active engine.** Bash pipeline chaining the standard Go
  bug-bounty toolchain. Breadth and depth on a scoped, authorized target. Runs **on the
  user's own machine where those tools are installed — not in this sandbox**; this skill
  never executes it for the user. Full guide: `references/active-enumeration.md`.

**Install the toolchain first (for `recon.sh`).** `recon.sh` needs the Go bug-bounty
suite installed. On a fresh Ubuntu (20.04/22.04/24.04) machine, have the user run
`scripts/setup.sh` **before** the first `recon.sh` run — it installs Go + the toolchain
(subfinder, dnsx, httpx, katana, gospider, nuclei, gowitness, gitleaks, naabu, gf, …),
Python recon tools, nuclei templates, ~1 GB of SecLists wordlists, and shell/tmux env.
It needs sudo and runs on the user's own machine, never the sandbox. After it finishes,
`recon.sh`'s own `check_tools` reports anything still missing. `recon.py` (passive) needs
none of this.

```bash
# passive — always available
python <skill_dir>/scripts/recon.py run --target example.com [--scope scope.txt] [--resolve] [--out DIR]
# VT_API_KEY=<key> python recon.py run --target example.com   # adds VirusTotal provider

# active — install the toolchain first (Ubuntu, sudo), then run on the user's own machine
bash <skill_dir>/scripts/setup.sh                              # one-time toolchain install
bash <skill_dir>/scripts/recon.sh -d example.com -o recon_example
bash <skill_dir>/scripts/recon.sh -d example.com --nuclei --active-checks --params --ports
# notify: --slack/--discord <webhook> (summary); --telegram <bot_token>:<chat_id> OR
#   TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID env — Telegram also sends per-finding alerts
```

**Notifications.** `recon.sh` pushes the end-of-run summary to Slack/Discord/Telegram,
and when Telegram is configured it also fires a concise alert on each confirmed
high-signal finding (zone transfer, takeover, nuclei critical/high, open redirect, CORS,
exposed `.git`, public bucket, secrets). Opt-in; the bot token is passed at runtime (flag
or env), never committed; secret values are never sent. Full setup:
`references/active-enumeration.md`.

## Which engine

- **Default / sandbox / no tools installed / first passive map → `recon.py`.**
- **User has the Go toolchain + an authorized, scoped target → `recon.sh`** for active
  subdomain brute-force, live crawling, HTTP probing, classification and opt-in checks.
- **Best practice:** run `recon.py` for passive breadth, then `recon.sh` for depth on the
  resolved in-scope set. `recon.py` is **not** superseded — it is the passive/API-source
  layer and the only one that runs with no tools. See the comparison and full flag/output
  reference in `references/active-enumeration.md`.

**Passive-first always.** Prefer passive collection; active modules that send traffic to
the target (`recon.sh` crawlers and especially its opt-in `--nuclei`, `--screenshots`,
`--gitleaks`, `--params`, `--ports`, `--test-redirects`, `--active-checks`) run only
within a confirmed program scope on a target the user is authorized to test.

## Passive output contract (recon.py — BadRecon-compatible)

| Artifact | Contents | Agent use |
|---|---|---|
| `subdomains.csv` | subdomain, sources, resolved_ip, in_scope | scope-filtered attack surface |
| `urls.csv` | url, sources, in_scope | endpoint dictionary; feed js-audit/js-recon |
| `ips.csv` | ip, hostnames | infra clustering, cross-target correlation |
| `providers.json` | per-engine state + counts + timestamps | read BEFORE interpreting anything |
| `recon_notes.md` | provider status table + totals | the "what actually ran" record |
| `FINDINGS.md` | interesting-URL flags + redacted secret-shapes | triage leads (leads, NOT findings) |
| `raw/<engine>.json` | unnormalized provider output | re-parse without re-fetching |

## Active output (recon.sh — summary)

Writes a structured output dir: `subdomains/`, `urls/` (in-scope `allurls.txt` +
~30 classified buckets), `httpx/` (`httpx_all.json`, status-split, `tech_summary.txt`),
`dns/`, `vuln/`, `ports/`, `params/`, `screenshots/`, `leaks/`, `logs/`, `reports/summary.md`.
Scope is enforced by snapshotting the original roots (`root_domains.txt`) before
enumeration and filtering every crawled URL against them. Full layout, tool list
(required vs optional) and run modes: `references/active-enumeration.md`.

## Interpretation rules (inherited from BadRecon discipline — enforce all)

1. **Read the "what ran" record first.** Passive: `providers.json` — an engine in
   `rate_limited`/`http_403`/`skipped_no_key`/`exception:*` state proves nothing about the
   target. Active: `logs/*.log` + `run_config.txt` — a tool that errored or was missing
   proves nothing either. Empty from a healthy source is data; empty from a failing or
   not-run source is "missing evidence" — record, never conclude absence.
2. **Asset / source / scan separation.** Passive keeps it in the `sources` column on every
   row; correlation claims ("this IP ties two targets") must cite the observing sources.
3. **Scope-match before anything else.** `in_scope=no` rows / out-of-scope hosts are context
   only — never tested, never reported as target findings. Active scope is only as good as
   the roots you give `recon.sh`; confirm the program scope and pass exactly those roots.
4. **Interesting URLs, secret-shapes and every `vuln/` hit are LEADS.** Passive stores
   secret values redacted (`AKIA00***REDACTED`); active nuclei/CORS/`.git`/open-redirect
   hits must be reproduced by hand before they are findings. Validity checks and CVE
   claims need explicit authorization plus version/reproduction evidence.
5. **CT/DNS/intel sources give names, not liveness.** Historical subdomains may be dead —
   resolve (passive `--resolve` or active httpx) before treating as live; dead-but-in-CT
   names still matter (takeover checks, historical content).

## Triage handoff

Summarize totals (`recon_notes.md` / `reports/summary.md`) → list in-scope subdomains by
source count → group flagged URLs by pattern (admin/config/backup/api/env/params) → hand
the endpoint set and `httpx_all.json` to `js-recon`/`js-audit`, class buckets to the
matching hunters (`sqli_params`→`bb-sqli`, `redirect_ssrf`→`bb-ssrf`,
`idor_params`→`idor-runner`/`bb-authz`, `oauth_endpoints`→`bb-oauth`, …), takeover
candidates to takeover review, and any **hand-confirmed** issue to `vuln-report` (strict
5-section template). Recon observations go to the report's intel section, never its
findings section. Handoff map in detail: `references/active-enumeration.md`.

## Passive engine notes (recon.py)

- `crtsh` — Certificate Transparency; slowest, richest for historical names. `*.domain` wildcard query.
- `shodan_ctl` — free hostname enumeration via Shodan's CT feed, no key.
- `hackertarget` — hostsearch with IPs; unauthenticated quota can exhaust → handled as rate-limited.
- `certspotter` — unauthenticated tier rate-limits; `rate_limited` state is normal without a key.
- `urlscan` — public scan index: URLs + page IPs + domains.
- `wayback` — archived URLs (capped 30k, collapsed); best source for forgotten endpoints and old JS.
- `virustotal` — only with `VT_API_KEY` env; reputation/resolutions, never vulnerability proof.
- `rdap` — registrar/ASN context; never a testing authorization.

Custom subsets: `--engines crtsh,wayback,urlscan`. Re-run single engines alone and merge
CSVs by the `sources` column. Provider keys load from env / git-ignored `keys.env`
(`keys.env.example` is the placeholder template — never commit real keys).
