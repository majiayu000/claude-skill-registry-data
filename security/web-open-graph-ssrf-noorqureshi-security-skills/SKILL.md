---
name: web-open-graph-ssrf
description: >
  SSRF through link-preview / URL-unfurl / oEmbed features. Load when the app generates a
  preview card for a user-supplied URL: chat/forum/comment link unfurling, "add a link" in
  posts or profiles, oEmbed endpoints, rich-text editors that auto-embed, bookmark/save-for-later
  tools, or any UI that shows an Open Graph title/image/description for a pasted link. Signals:
  params like url=, link=, embed=, preview=; a "fetching preview" spinner; response JSON with
  og:title / og:image fields; User-Agents like *bot, *crawler, Slackbot, Discordbot, or a
  fetch from a different egress IP than the app.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A10:2021-SSRF]
cwe: [CWE-918]
tools: [burp, collaborator, interactsh]
schema_version: 1
---

# Open Graph / link-preview SSRF

## When it applies
The app unfurls user-supplied URLs — chat messages, comments, profile links, oEmbed consumers,
"import bookmark", RSS/save-for-later. The dedicated fetch this triggers is an SSRF primitive,
often with **weaker filtering than the main app** because previews must work for arbitrary
third-party sites. Also applies when the preview is rendered by a headless browser (adds
XSS-in-preview and local-file angles).

## Why it works
Unfurlers are built to fetch *anything*, so allowlists are rare or trivially bypassed. The fetch
frequently runs in a **separate worker/microservice** with its own network position — internal
dashboards, metadata IPs, and queues may be reachable from there even when the web tier is
locked down. The fetcher also *parses* the response (HTML, images, sometimes JS), which adds
parser-differential bypasses the main app's URL validator doesn't share.

## Method
1. **Find the unfurl path.** Paste a URL to your `interactsh`/Collaborator host into every
   link-accepting field. Watch for the OOB hit and fingerprint the fetcher: User-Agent, source
   IP (different ASN than the app = separate worker = different trust zone), and whether DNS
   and HTTP come from different IPs (DNS-rebinding candidate).
2. **Probe internal reach** with the standard SSRF matrix from `web-ssrf` — `127.0.0.1`,
   `169.254.169.254`, RFC1918 ranges, common internal ports — but expect *different* results
   than app-tier SSRF: test the worker's neighbours, not the web server's.
3. **Exploit the fetch-and-parse contract:**
   - **Redirect chains** — your URL 302s to `http://169.254.169.254/latest/meta-data/`.
     Validators that check only the submitted URL pass; the worker follows.
   - **OG-tag pivot** — serve a page whose `og:image`/`og:url` points internal. Some fetchers
     re-fetch OG sub-resources with a second, unvalidated request.
   - **Parser differentials** — `http://allowed.com@internal/`, `http://internal#@allowed.com`,
     scheme-relative and backslash variants (`http:\\internal`), IDN homographs. The validator
     and the worker's HTTP client often tokenize URLs differently.
   - **DNS rebinding** — validator resolves to a public IP, worker resolves again to
     `127.0.0.1`. Reliable when the OOB hit showed separate DNS/HTTP sources.
4. **If the preview renders (headless browser):** try `file:///etc/passwd`, `file:///` paths to
   app config, and a page that fires JS to exfiltrate rendered internal content via OOB —
   renderer workers frequently run with broad network access.
5. **Cache angle:** previews are cached by URL. Check whether a poisoned preview (internal
   content, attacker HTML) is then served to *other* users who paste the same URL — stored
   impact without any victim-side script.

## Gotchas
- **Async unfurling** — the fetch may happen seconds/minutes after submission, from a queue.
  Correlate by unique canary tokens per URL, not by timing.
- **Image-proxy only** — some apps only proxy `og:image`, not the page fetch. A proxy that
  returns the fetched body is still full read-SSRF; one that re-encodes images is limited to
  port/host oracle via error vs. success vs. timing.
- **Allowlists exist where previews must look right** — `oembed` consumers may restrict to
  known providers. Provider-side open-redirects and user-content subdomains
  (`allowed.com.evil.com` won't fly; `evil.com`'s redirect *from* an allowed provider URL will)
  are the way through.
- **Timeouts lie** — internal closed ports often fail faster than filtered ones; a fast "no
  preview" vs slow "no preview" distinction maps internal services without any body.
- Rate limits on unfurl endpoints are usually tuned for UX, not scanning — slow down rather
  than trip the WAF and lose the worker's egress IP to a blocklist.

## Verify success
OOB hit from an infrastructure IP you don't otherwise reach; a preview card whose title/image
came from an internal-only address (`http://127.0.0.1:8080/` rendering an internal admin
title); metadata JSON in a preview; or a cached poisoned preview served to a second account.

## References
PortSwigger SSRF research; bug-bounty writeups on chat-unfurler SSRF (Slack/Discord-style
previews); Orange Tsai, "A New Era of SSRF" (parser differentials).
