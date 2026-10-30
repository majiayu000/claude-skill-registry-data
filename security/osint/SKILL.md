---
name: osint
description: >-
  Open-source intelligence: full profiling protocol, breach and leak exposure,
  image authenticity and reverse image search, entity dossiers, investigator
  OPSEC, CTF OSINT, and local Google Maps scraping. One contract; the parts
  under parts/ carry the methods — open the ones the task needs.
---

# osint — open-source intelligence

> Home branch in Memora: `root/skill/osint`.
>
> Public data and authorized targets only. Confirm target scope and output depth
> via `ask_questions` before starting an entity dossier or active collection.

## Choosing a part

| Task | Part |
|---|---|
| Full profiling protocol (Level 0 local → Level 1 free → Level 2 verification → Level 3 API) | `parts/osint-protocol/` |
| Decision-grade entity research dossier (`.docx` with verdict, timeline, red flags, provenance log) | `skills/osint/parts/dossier/` |
| Breach exposure for an email/username/phone (HIBP, Pwned Passwords, DeHashed, IntelX, Snusbase) | `parts/what-leaked-about-you/` |
| Image/video authenticity (ELA, clone detection, C2PA credentials, deepfake tells) | `parts/is-this-photo-real/` |
| Reverse image search across Yandex, Google Lens, Bing, TinEye, Baidu | `parts/find-the-original-image/` |
| Businesses, leads, emails, and reviews from Google Maps via local Docker scraper | `parts/google-maps-scraper/` |
| Investigator OPSEC (attribution surface, browser/TLS fingerprint, proxy/Tor vs. VPN) | `parts/investigate-without-getting-made/` |
| CTF OSINT techniques (DNS, username enumeration, geolocation, Wayback, public filings) | `parts/ctf-osint/` |

## Rules

- Walk `root/skill/osint` in Memora before starting; record entity findings and verified tool behavior as nodes.
- Gather intake parameters (`dossier`, `google-maps-scraper`) in a single batched `ask_questions` call with one-line consequences, never one question at a time in prose.
- Use native MCP servers (`maigret`, `shodan`, `dnstwist`, `osint-tools`) via `call_mcp_tool` when available.

## Related

`research` (`skills/research/parts/searchmcp-research/` for multi-source web verification), `security` (surface assessment), `browser` (anti-detect Camoufox via `browsermcp`).
