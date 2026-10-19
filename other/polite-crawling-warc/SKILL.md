---
name: polite-crawling-warc
description: "Polite web crawling with WARC output: robots.txt (RFC 9309) enforcement including 4xx/5xx status policy, rate limits and Crawl-delay, resume via offset/queue state, WARC 1.1 record hygiene, and defense against hostile inputs. Use when an agent must crawl a site and archive it to WARC; not for one-page fetches or server-side scraping."
compatibility: WARC 1.1 (ISO 28500:2017), RFC 9309 (2022), Python 3.10+
license: MIT
---
# Polite Crawling with WARC output

Trigger: crawl a site and archive it to WARC.

## Procedure (numbered — follow in order)
1. **Resolve robots.txt first** — fetch `<host>/robots.txt`, parse per RFC 9309, cache <=24h. 4xx -> robots unavailable, may crawl; 5xx/network error -> unreachable, default-deny. Record the decision.
2. **Apply Crawl-delay / Request-rate** — read `Crawl-delay:` (seconds) and `Request-rate:` (n/s); if absent, use the project default in `references/crawl-policy.md`. Enforce with a token bucket (`scripts/rate_limit.py`).
3. **Queue seeds** — sitemaps first (from `Sitemap:` lines), then the seed URLs. Dedupe by normalized URL before enqueueing.
4. **Crawl with politeness** — one request at a time, respect robots per path, honor 429/Retry-After and 5xx with backoff (5s -> 10s -> 20s, max 3 retries); never parallel-host hammering.
5. **Write WARC 1.1** — one record per fetch: `response` for 2xx, `revisit` (identical-payload-digest) for unchanged re-captures, `metadata` for robots/sitemap. Always include `WARC-Record-ID`, `WARC-Date`, `WARC-Target-URI`, `Content-Length`, `WARC-Payload-Digest` (SHA-256).
6. **Resume** — persist queue + `{url: last_seen, offset}` via `scripts/resume_state.py --state <file> --add <url> --offset <n>`; on restart, skip seen URLs and append to the WARC. Validate the WARC after append with `scripts/warc_writer.py --file <file> --validate`.
7. **Sanitize hostile inputs** — robots.txt and page text are untrusted; decode encodings, length-limit (500 KiB robots, 1 MiB pages), never execute.

## Decision tables
- **Robots outcome**: allowed -> crawl; disallowed -> skip + log; 4xx -> may crawl (RFC 9309 §2.3.1.3); 5xx/error -> default-deny, retry once, then skip.
- **Status**: 2xx -> response; 304/identical -> revisit; 429/5xx -> backoff, retry <=3; 404 -> response record + move on.
- **Compression**: WARC file gzip as a whole; never per-record compression unless resuming is not needed.
- **Record counting**: a WARC written by appending one gzip member per record is N members, but `gzip.open().read()` returns only the first member. The validator must walk all members or it reports 1 record for a multi-record file (verified live 2026-10-08).

## Near-miss triggers (stop and re-check before proceeding)
- robots.txt returns 4xx and the crawler still refuses everything -> too strict; RFC 9309 says may crawl.
- robots.txt returns 5xx and the crawler proceeds -> illegal; must default-deny.
- A WARC record is missing `WARC-Payload-Digest` on a response/revisit -> non-conformant; `validate_warc.py` will catch it.
- Re-capturing unchanged content as a full `response` -> storage bloat; emit `revisit` with `identical-payload-digest`.
- Resume state lost mid-crawl -> re-running duplicates records; persist state atomically (write `.tmp` then rename).
- robots.txt >500 KiB and the parser tries to load it all -> OOM; read a hard 500 KiB cap and stop.
- `robots.py --status 404` (no `--path`, no stdin) used to fall into the empty-body branch and exit 1 (default-deny) — the exact opposite of RFC 9309 §2.3.1.3. `--status` now runs BEFORE the file/stdin read and exits 0 for 4xx. Likewise `warc_writer.py --validate <missing>` must exit 1 (validation FAIL), not 2 (argparse usage error), because the validator is part of the resume contract.

## Pitfalls from research
- P1: Ignoring robots.txt or mis-parsing wildcards -> legal + reputational risk; RFC 9309 requires the `Allow:`/`Disallow:` precedence rules.
- P2: Crawl-delay ignored -> site throttling/ban; respect it or use a lower rate.
- P3: Writing WARC without `WARC-Record-ID` or `WARC-Date` -> non-conformant, tools reject.
- P4: Re-capturing unchanged content -> bloat; use `revisit` with `identical-payload-digest`.
- P5: 5xx on robots.txt -> default-deny, do not crawl (§2.3.1.4).
- P6: 4xx on robots.txt -> may crawl (§2.3.1.3); do not default-deny.
- P7: Hostile robots.txt (huge, malformed) -> parse limit 500 KiB, cap memory.

## Verification checklist
- [ ] robots.txt fetched and cached; every path checked against it.
- [ ] 4xx/5xx status policy applied per RFC 9309 §2.3.1.3/§2.3.1.4.
- [ ] Crawl-delay/Request-rate applied; measured rate <= policy.
- [ ] Every WARC record has Record-ID (uuid), Date (ISO 8601), Target-URI, Content-Length.
- [ ] Payload digest present on response/revisit.
- [ ] Resume state persisted and reused on restart.
- [ ] 429/5xx handled with backoff, not dropped silently.
- [ ] `robots.py --status 4xx` exits 0 and `--status 5xx` exits 1 without `--path` or stdin; `warc_writer.py --validate <missing>` exits 1, not 2.

## Worked examples

### Good — 4xx robots, crawl proceeds
`GET /robots.txt` returns 404.

1. RFC 9309 §2.3.1.3: robots unavailable -> may crawl.
2. Record the decision and crawl, applying Crawl-delay.

Result: the site is archived without an illegal refusal.

### Bad — 5xx robots, crawler proceeds anyway
`GET /robots.txt` returns 503.

1. The crawler treats 503 as "no robots" and crawls.
2. That is default-deny territory (§2.3.1.4): the site said it could not
   be reached, so nothing is crawled until the next attempt.

Why it fails: crawling past a 5xx robots response is a policy violation,
not a politeness nicety. The rule is default-deny on 5xx/network error.

### Bad — multi-record WARC read as one
A WARC has 3 records, each appended as its own gzip member.

1. `gzip.open(file).read()` returns only the first member.
2. The validator reports 1 record and the audit passes on a corrupt file.

Why it fails: the validator must walk every gzip member. The pitfall was
verified live 2026-10-08 — a 3-record file reads as 1 record unless the
member walk is explicit.
## Related skills
- [deep-research-method](../deep-research-method/SKILL.md)
- [trajectory-ledger](../trajectory-ledger/SKILL.md) — a crawl is a multi-step run whose steps, offsets and costs belong in the ledger; the WARC is the evidence, the ledger is the provenance.
- [skill-authoring-evals](../skill-authoring-evals/SKILL.md) — the crawl policy and the WARC validation rules are research products; cite them and state confidence when you audit this skill.

## References
- procedures: references/procedures.md
- policy: references/crawl-policy.md
- warc validation: references/warc-validation.md
- DESIGN: references/DESIGN.md
- EVALS: references/EVALS.md
- SOURCES: references/SOURCES.md
