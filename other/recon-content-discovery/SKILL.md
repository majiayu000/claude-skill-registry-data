---
name: recon-content-discovery
description: >
  Discover hidden paths, endpoints, params, and JS-exposed routes on a web target. Load after
  a live host is found, on "dirbust/content discovery/fuzzing", or when mapping an app's real
  surface. Signals: a single web host to deep-map, SPA with API calls, /api, JS bundles.
domain: recon
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: info
mitre: [T1595.003]
tools: [feroxbuster, ffuf, katana, gau, arjun, gospider]
schema_version: 1
---

# Content & endpoint discovery

## When it applies
You have a live host and need its *real* surface: hidden dirs, backups, admin panels, API
routes, and parameters — the inputs every other skill tests.

## Why it works
Apps expose far more than the UI links to. Historical URLs, JS bundles, and predictable paths
reveal endpoints (and params) that were never meant to be public or were left from old versions.

## Method
1. **Passive URL mining first**: `gau target.com` + `waybackurls` pull historical URLs (old
   params, deprecated endpoints) with zero requests to the target.
2. **Crawl, incl. JS**: `katana -u https://target -jc -kf all` or `gospider` to extract links
   and endpoints embedded in JavaScript (SPAs hide the API here).
3. **Directory/file brute**: `feroxbuster -u https://target -w raft-medium-directories.txt -x
   php,txt,bak,zip,json` — recursive; add extensions matching the stack.
4. **Parameter discovery**: `arjun -u https://target/endpoint` finds hidden GET/POST params that
   feed injection tests (XSS/SQLi/IDOR).
5. **Rank findings**: admin/upload/import/debug/graphql/swagger routes and anything with params
   go to the front of the hunting queue.

## Gotchas
- Auto-calibrate against soft-404s (`ffuf -ac`, ferox filters) or you'll drown in false 200s.
- Respect rate limits/program rules — throttle (`-t`, `--rate-limit`) on live targets.
- Pull params from JS *and* wayback; each finds ones the other misses.

## Verify success
A prioritized list of reachable endpoints + parameters, feeding `web-*`/`api-*` hunting.

## References
ProjectDiscovery katana; feroxbuster/ffuf docs; s0md3v Arjun; TomNomNom gau/waybackurls.
