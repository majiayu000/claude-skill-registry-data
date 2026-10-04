---
name: url-validation
description: Preflight and safety gate for every audit. Use first to normalize a target URL, block SSRF and unsafe schemes, revalidate redirects, inspect robots.txt, establish scope and budgets, and report HTTPS, redirect, or AI-crawler access defects. Writes the required preflight record for every downstream skill.
license: MIT
---

# URL Validation (preflight gate)

This skill answers two separate questions and must not conflate them:

1. **Is it safe and in scope to audit this target?** A hard gate. If it fails,
   nothing else runs.
2. **Does what we learned while checking constitute a finding?** Several
   preflight observations are real discoverability defects and are reported.

## When to use

Run this first for every audit, before any other skill in this marketplace.
The orchestrator invokes it automatically; run it directly when you want to
check whether a target is auditable at all, or to inspect a site's robots
posture on its own.

## Inputs

| Input | Required | Notes |
|---|---|---|
| `url` | yes | A bare domain (`example.com`), a full URL, or a pasted link. Whitespace, wrapping punctuation and fragments are tolerated. |
| `--max-pages` | no | Page budget for the whole audit. Default 20. |
| `--max-seconds` | no | Detection budget. Default 150. |
| `--strictness` | no | `lenient`, `balanced` (default), or `strict`. Shifts derived thresholds, never the safety gate. |
| `--workspace` | no | Where to create the run directory. Default `./.audit/`. |

## Procedure

1. **Normalise.** Trim, strip wrapping punctuation, add a scheme when missing,
   punycode internationalised hosts, drop the fragment, canonicalise the path.
2. **Gate on safety.** Scheme allowlist, credential rejection, obfuscated-IP
   rejection, reserved-suffix rejection, port allowlist.
3. **Resolve DNS** and require *every* returned address to be public unicast.
4. **Resolve the redirect chain**, re-validating each hop against the same
   rules. A public host that redirects into private space is refused at the hop
   that does so, not after.
5. **Establish scope** as the registrable domain of the final URL.
6. **Fetch and parse `robots.txt`**; record how each known AI crawler is
   treated.
7. **Probe HTTPS and canonical host** behaviour (`http` → `https`, apex → `www`
   or the reverse).
8. **Write the preflight record** and emit findings.

Run it:

```
python3 scripts/validate_url.py <url> [--max-pages N] [--strictness LEVEL] [--json]
```

Exit codes: `0` cleared, `1` refused (unsafe or unreachable), `2` internal error.

## Checks performed

| Check id | Detects | Severity | Claim level |
|---|---|---|---|
| `no_https` | Site served over plaintext HTTP | high | 1 |
| `https_not_enforced` | HTTP does not redirect to HTTPS | high | 1 |
| `redirect_chain_long` | 3+ hops before the final document | medium | 1 |
| `host_canonicalisation` | Apex and `www` both serve 200 without redirecting | medium | 1 |
| `robots_missing` | No `robots.txt` at all | low | 1 |
| `robots_unparseable` | `robots.txt` present but malformed | medium | 1 |
| `robots_blocks_ai_retrieval` | Blocks a live-retrieval AI crawler | critical | 1 |
| `robots_blocks_ai_training` | Blocks a training crawler only | medium | 1 |
| `robots_blocks_all` | `Disallow: /` for `*` | critical | 1 |
| `crawl_delay_excessive` | Crawl-delay high enough to starve a crawler | medium | 2 |

## Output

Writes `01-url-validation.json` into the run workspace:

```json
{
  "cleared": true,
  "target": { "url": "...", "origin": "...", "registrable_domain": "...", "resolved_ips": ["..."] },
  "redirect_chain": [ { "from": "...", "status": 301, "to": "..." } ],
  "robots": { "exists": true, "sitemaps": ["..."], "ai_crawlers": { "GPTBot": { "allowed": false, ... } } },
  "config": { "thresholds": { ... } },
  "findings": [ ... ]
}
```

## Guardrails

Read-only and recommend-only. `GET` and `HEAD` only; never authenticates,
never submits a form, never follows a redirect out of scope, never fetches a
private address. `robots.txt` is honoured for every subsequent request, not
merely reported on.

## Grounding

The AI-crawler distinction is the load-bearing idea. Blocking a *training*
crawler (`GPTBot`, `Google-Extended`, `ClaudeBot`) affects what a model
absorbs over time. Blocking a *live-retrieval* crawler (`OAI-SearchBot`,
`PerplexityBot`, `Claude-User`, `ChatGPT-User`) means the brand cannot be
fetched while an answer is being generated — and arXiv:2604.25707 §6 reports
search-trigger rates of 98.64% (ChatGPT), 99.67% (Google AIO) and 100%
(Perplexity). Retrieval is attempted on essentially every prompt, so a block
at that layer is decisive, which is why the two cases carry different
severities.
