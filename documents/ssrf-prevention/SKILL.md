---
id: ssrf-prevention
version: "2.0.0"
title: "SSRF Prevention"
description: "Server-Side Request Forgery: allowlisting the destination of a server-side fetch, when re-resolution between check and connect matters, redirect and scheme bypasses, parsers that fetch on their own (XXE, SVG, HTML-to-PDF), cloud metadata, and keeping the response from becoming an oracle. Use when fetching a client-supplied URL, wiring webhooks, image proxies, PDF or preview renderers, or reviewing any HTTP-client wrapper."
category: prevention
severity: critical
applies_to:
  - "when generating code that fetches a URL supplied or influenced by a client"
  - "when wiring webhooks, image proxies, PDF renderers, link previews, oEmbed fetchers"
  - "when parsing user-supplied XML, SVG, HTML, or Markdown that a renderer may resolve"
  - "when running in a cloud environment with an instance metadata service"
  - "when reviewing a URL-parsing or HTTP-client wrapper"
languages: ["*"]
token_budget:
  minimal: 1400
  compact: 1800
  full: 2400
rules_path: "rules/"
related_skills: ["api-security", "deserialization-security", "file-upload-security", "iac-security"]
last_updated: "2026-08-14"
sources:
  - "OWASP SSRF Prevention Cheat Sheet"
  - "CWE-918: Server-Side Request Forgery"
  - "AWS IMDSv2 documentation"
  - "PortSwigger Web Security Academy — SSRF labs"
---

# SSRF Prevention

## Rules (for AI agents)

### ALWAYS
- Constrain the destination with an **allowlist of hosts you intend to reach**, not a
  denylist of addresses you intend to avoid. A denylist has to enumerate every spelling
  of every internal address — decimal and octal IPv4, IPv6 and IPv4-mapped IPv6, a
  hostname whose A record is private, a public wildcard resolver like `nip.io` that
  encodes any address into a name — and it only has to be wrong once.
- Know which of the two controls you built, because it decides whether re-resolution
  matters. An **allowlist of hostnames** survives DNS rebinding: the attacker controls
  DNS only for names they own, and those names are not on the list. An **IP-range
  check** does not: the name resolves to a public address when you validate and a
  private one when you connect, and the two resolutions are independent. If your
  control is address-based, resolve once and **connect to that pinned address** —
  a custom dialer or transport, carrying the original hostname for SNI and `Host` —
  so no second lookup can occur.
- Re-validate **at every redirect hop**, or disable redirect-following entirely on
  fetchers that take user-supplied URLs. An allowed host answering `302` to
  `http://169.254.169.254/` is the single most common bypass, and it defeats a check
  performed only on the URL the user submitted.
- Restrict the scheme to `http` and `https` before anything else. `file://`,
  `gopher://`, `dict://`, `ldap://`, `jar://` and friends turn a fetcher into a file
  reader or a protocol-smuggling primitive.
- Keep the **user-URL fetcher and the internal fetcher as separate clients**, and make
  mixing them fail to compile rather than fail at runtime — distinct types in Go, Rust
  or TypeScript. A single client used for both eventually gets called with the wrong
  argument.
- Treat a **parser as a fetcher**. XML entity resolution, SVG with external references,
  HTML-to-PDF renderers, Markdown image embedding, oEmbed and link-preview
  unfurlers, and office-document converters all issue outbound requests from URLs
  inside the document, using no code you wrote. `deserialization-security` owns
  disabling external entities; what belongs here is that the request those parsers
  make is a server-side fetch and needs the same allowlist and the same egress policy.
- Decide what the **response** may reveal. Returning the body, the status code, the
  redirect chain, the content type, or the elapsed time to the caller turns a blind
  SSRF into a readable one. Return a fixed error on failure and never echo the URL or
  the fetch error back — `error-handling-security` owns the shape of that response.
- Enforce **IMDSv2** on EC2 (session token required, hop limit 1) so a plain `GET`
  from a compromised process cannot read instance credentials, and give the workload
  its own identity so the metadata service is not a credential worth reaching.
  Endpoints for each cloud, and the egress rules that go with them, are in
  `references/metadata-and-egress.md`.

### NEVER
- Treat "this service is internal / behind a VPN / on an allowlisted network" as
  mitigation. SSRF originates *inside* that network, so it reaches exactly the services
  the network control was protecting. Reachability is not authentication.
- Ship a forwarder that switches on the shape of its input —
  `path.startsWith('http') ? path : base + path`. It is a latent SSRF that activates
  the day any caller passes user-influenced input.
- Rely on an egress proxy or metadata-blocking sidecar as the **only** control. It
  constrains where traffic goes, not what the application asks for, and it is bypassed
  by any request path that does not traverse it.
- Compare a URL as a **string** — prefix match, `contains`, a regex over the raw text.
  Parse it, then compare the parsed host. `https://allowed.example.com@evil.com/`,
  `https://evil.com/?x=allowed.example.com` and `https://allowed.example.com.evil.com/`
  all defeat string matching and none defeat host comparison.
- Accept a hostname without normalizing IDN / Punycode first. Homograph forms compare
  unequal to the ASCII name they imitate, so a naive allowlist check passes them
  straight through.
- Parse the URL with one library and fetch it with another. Differential parsing
  between WHATWG and RFC 3986 implementations is a documented bypass class: the
  validator and the client disagree about which part is the host.

### KNOWN FALSE POSITIVES
- A URL that is a **configuration constant** — an operator-set integration endpoint,
  a hard-coded base — is not user input. The static config is the allowlist.
- A forwarder that appends only a path segment or query string to a **literal** base
  cannot change host, so it is not SSRF. The finding is an absolute URL that user
  input can influence.
- An outbound webhook **to a customer-supplied URL** is the intended feature of a
  webhook system; the destination is meant to be arbitrary. It still needs the private
  and link-local ranges blocked, redirects disabled, and the response withheld from
  the caller — the delivery result may be reported, never the body.
- A fetch that resolves to a private address is expected when the service's job is to
  reach an internal host — a monitoring prober, a health checker. The control there is
  that the *destination set* is operator-defined, not that the address is public.

## Context (for humans)

SSRF is worth more to an attacker than its description suggests, because the server
making the request is authenticated to things the attacker is not. Cloud instance
metadata is the famous case — a plain `GET` returning role credentials — but internal
admin panels, unauthenticated RPC endpoints, service registries and Redis all sit on
the same side of the same boundary. The vulnerability is not that the server fetched a
URL; it is that the server's network position was standing in for authentication.

The distinction the rules spend the most words on is allowlist-of-hosts versus
address-checking, because it decides whether DNS rebinding is a real threat or a
theoretical one, and most generated validators mix the two: they check the address is
public *and* the host is expected, then hand the original URL to a client that resolves
it again. Which of the two checks was load-bearing determines whether that second
resolution matters.

The class most often missing entirely is the parser that fetches on its own behalf. No
code in the application calls an HTTP client, so nothing about the code looks like a
fetcher — the URL is inside the document, and the library resolves it.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/metadata-and-egress.md` — metadata endpoints per cloud and how each is
  hardened, the reserved and private ranges in both address families, pinned-dialer
  implementations per language, and the parsers that fetch
- `rules/ssrf_sinks.json`
- `rules/cloud_metadata_endpoints.json`
- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html).
- [CWE-918](https://cwe.mitre.org/data/definitions/918.html).
- [AWS IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html).
- [PortSwigger SSRF](https://portswigger.net/web-security/ssrf).
