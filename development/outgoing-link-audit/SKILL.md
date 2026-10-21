---
name: outgoing-link-audit
description: >
  Liveness audit of every OUTGOING (external) link on an Astro site built with the
  new-website kit. Builds the site, extracts each external href from dist/, fetches
  it, and classifies it OK / REDIRECT / REBRAND / DEAD — flagging links that 404,
  time out, or now redirect to a different domain (a rebrand), with the source page
  and a suggested fix. This is the network-dependent complement to the offline
  `tests/links.spec.ts` guard (which only blocks already-known-dead domains from
  regressing). Run it about once a month, or before a release/launch. Trigger
  phrases: "audit outgoing links", "check external links", "are our links still
  live", "monthly link check", "any dead links", "did any linked site rebrand",
  "link rot check", "review outgoing links".
---

# Outgoing Link Audit

Links to other people's sites rot: companies rebrand, move domains, or shut down.
The offline test gate (`tests/links.spec.ts`) can only catch domains you *already
know* are dead. This skill is the active sweep that *discovers* the rot.

Read-only with respect to the site: it diagnoses and reports. You apply fixes (and
add any newly-dead domain to the test) only after the user confirms.

## When to run

Monthly, or before a notable release / before launch. It hits third-party servers,
so it is deliberately **not** part of CI (`npm test` must stay hermetic and offline).

## Prerequisite: does the site even have external links?

If the build has no outgoing anchors there is nothing to audit — say so and stop:

```bash
cd "$(git rev-parse --show-toplevel)"
[ -d dist ] || npm run build >/dev/null
SITE_HOST=$(grep -oE "site:[[:space:]]*['\"]https?://[^'\"]+" astro.config.mjs \
  | sed -E "s#.*://(www\.)?##; s#/.*##" | head -1)
grep -rhoE '<a [^>]*href="https?://[^"]+"' dist --include='*.html' \
  | grep -oE 'href="https?://[^"]+"' | sed -E 's/^href="//; s/"$//' \
  | grep -vE "://(www\.)?${SITE_HOST}(/|$|:)" | sort -u | wc -l
```

## Shortcut: the shared script does steps 1–3

`scripts/check_external_links.sh` already builds, extracts, fetches and prints the
grouped report (DEAD / REDIRECT / UNVERIFIED / OK). Run it first:

```bash
bash scripts/check_external_links.sh
```

Then apply **judgment** to its output (the bit a script can't do — see the box in
step 2) and do step 4 (fixes). The procedure below explains what the script does and
is the manual fallback.

## Procedure

### 1. Build, then extract every external link

Audit the built output so it matches exactly what Cloudflare serves. The script
derives your own host from `site:` in `astro.config.mjs` and excludes it; everything
else absolute and `http(s)` from an `<a href>` is an outgoing link. To keep "which
page is this on?" for the report, run `grep -rl "<url>" dist` per finding.

### 2. Fetch each unique URL and classify

Use a real browser User-Agent — several hosts return 403 to a bare curl. Follow
redirects but record the **final** URL and status. Classify each result:

- **OK** — final code `200` and the final host is the same registrable domain.
- **REDIRECT** — `200` but final host differs only by `www`/scheme/trailing path.
  Usually harmless; note it, low priority.
- **REBRAND / MOVED** — `200` but the final host is a **different domain**. This is
  the high-value finding: update the link to the new canonical URL.
- **DEAD** — `4xx`, `5xx`, connection error, or timeout. Re-check once (could be
  transient); if it stays dead, flag for removal/replacement.

> Judgment, not just codes: a `403`/`429` can mean "bot-blocked", not "dead" — try a
> second UA or note it as *unverified* rather than calling a live page dead. A `200`
> that lands on a parked / "for sale" page is effectively dead even though the code is
> green. Use the model for these calls; let the script do the fetching.

### 3. Report

Group findings by severity. For each: the URL, the classification, the final URL (if
changed), and the source page(s). Lead with REBRAND + DEAD (the actionable ones);
list OK as a count.

### 4. Hand off the fixes

For each REBRAND/DEAD link, after the user confirms:

1. Update the link in the source page (`src/pages/*.astro` or a content collection
   entry). Use the new canonical URL.
2. **If a domain is now permanently dead/rebranded, add it to
   `tests/links.spec.ts` → `STALE_DOMAINS`** with the reason, so it can never be
   re-introduced. This is how the offline guard stays current — the audit feeds it.
3. Re-run `npm run build && npm test` to confirm green, then commit.

## Scope notes

- Audits the **active branch** you're on; `dist/` is the build of `src/`, which is
  what Cloudflare serves and what we fetch from.
- Internal-link health (clean, resolving, no `.html` hops) is already covered by the
  `navigation` + `seo` specs in `website-qa` — this skill is **external** links only.
