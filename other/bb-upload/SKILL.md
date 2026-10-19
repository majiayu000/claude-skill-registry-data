---
name: bb-upload
description: Hunt file-upload vulnerabilities on the SERVE side — stored XSS via Content-Type override on public object storage (MinIO/S3 response-content-type), polyglot type confusion against magic-byte sniffers (file-type ISO-BMFF dead bytes), filename command injection, extension and Content-Type-only upload checks, and serve-time policy bypasses. Use whenever the user mentions file upload bugs, avatar/attachment/upload endpoints, public buckets, cdn subdomains serving uploads, polyglot files, or uploaded content executing or rendering as HTML.
---

# Upload Attack Hunter

Upload defenses cluster at upload time (filename checks, extension whitelists, magic-byte sniffing, forced Content-Type) while the serve path gets none. Invert the review: upload a perfectly valid file, then attack how it is SERVED. Techniques below are paid findings from Voorivex Team research unless noted.

## Attack 1 — Content-Type override on public object storage (stored XSS, same-origin)

Any uploaded object served from the TARGET'S OWN origin (`cdn.target.com/...`, `target.com/uploads/...`) behind MinIO/S3:

**MinIO** — append the documented-but-dangerous response overrides to ANY public object URL:
```
https://cdn.target.com/files/avatar.png?response-content-type=text/html
```
`text/html` comes back = game over: upload a polyglot (valid PNG bytes + `<script>` payload appended), browse the overridden URL → same-origin stored XSS on `cdn.target.com`. Other overridable params: `response-expires`, `response-cache-control`, `response-content-encoding`, `response-content-disposition`.

**S3** refuses the override for anonymous GETs (`400 InvalidRequest`) — that error is a GREEN LIGHT, not a wall: any AWS identity may read a public object. Presign the GET with YOUR OWN credentials baking in the header (boto3 `generate_presigned_url`, `ResponseContentType: 'text/html'`, s3v4, virtual-host addressing). Unknown bucket region? Deliberately mis-sign with a wrong host — the `SignatureDoesNotMatch` error body leaks the `CanonicalRequest` with the real host; correct and re-sign.

**Impact rule**: value exists only when the bucket is fronted by the target's domain. `bucket.s3.amazonaws.com` random storage domain = usually nothing.

## Attack 2 — Polyglot type confusion vs magic-byte sniffers

The sniffer and the consumer disagree about the file's type — the gap is the bug. Map EVERY type checkpoint in the pipeline and check whether they can disagree:
1. Client form field claim (`Content-Type` in the multipart part — free to lie)
2. Server byte sniff (`file-type` / libmagic / `finfo`)
3. The extension the file is STORED under (`${hash}.${ext}` — who chooses ext?)
4. The `Content-Type` used at SERVE time (derived from stored extension? from upload header?)

**file-type (Node) ISO-BMFF bypass** — the HEIC/MP4 detector reads the brand at bytes 8–11 and never validates bytes 0–3 (the ISO box-size field). Dead header bytes = free polyglot space. Open a JavaScript block comment over the magic bytes:
```python
head = b"/*--" + b"ftyp" + b"heic" + b"\x00\x00\x00\x00" + b"heic" + b"mif1"
file  = head + b"*/\n" + b"globalThis.mark()"   # passes file-type AND node --check
```
First 32 bytes: `/*--ftypheic\x00\x00\x00\x00heicmif1*/` + payload. Wrapper grammar per consumer: `/* */` for JS/CSS, `<!-- -->` for HTML, `"` + filler for JSON (keep the brand bytes printable). Brand swaps change the sniffed verdict: `avif`→image/avif, `mif1`→image/heif, `qt  `→video/quicktime, `M4A `→audio/x-m4a.

Escalation in a chat/attachment app: registered as `.js` + client-side path traversal → service worker executes in the ADMIN's session; `.html`/`.svg` → stored XSS; `.json` → poisoned API responses.

**Remediation principle to cite in reports**: decide the type ONCE from verified bytes at upload, persist it, and serve exactly it.

## Attack 3 — Filename injection (when content checks win)

- **Blind command injection in the filename** ($2,400): `filename="test || sleep 30 ||.gif"` — extension check passes (`.gif` appended after the operator chain), the filename still hits a shell-out. Confirm with one timed request; try `;`, `|`, `&&`, backticks, `$()` separators — SQLi/SSTI payloads in the same field may bounce while shell injection lands.
- **Content-Type-only check = RCE on PHP stacks** ($1,500): upload a PHP webshell with `Content-Type: image/png` when the server validates only that header.
- Stored XSS via filename rendered in listings (moderation queues, admin file tables) — the cPanel Mailman case paid via a moderation-queue `From:` header; same class.

## Targeting heuristics

- Re-audit every "well-secured" public bucket focusing on the retrieval GET — upload-time validation never protects serve-time behavior.
- Legacy/previous-gen upload endpoints (found via fuzzing + wayback) lack modern validation entirely.
- When the browser silently redirects after upload, read the RAW response in Burp — hidden functionality lives behind 30x's.
- Detection templates for bug classes like these should use a harmless sentinel value, not a payload (survives WAF/CDN rules).
- Chain upward: same-origin stored XSS → cookie theft / SDK re-init (bb-domxss) → ATO (bb-chains).

## Verdict + evidence

- PoC = screenshot of the payload executing/rendering from the target's own domain, plus the exact upload request and the exact overridden URL.
- "Arbitrary file upload" that never executes or renders = Low. Execution or same-origin HTML rendering is the finding.
- State the storage backend evidence (MinIO error strings, S3 XML errors) — it proves the class, not just the instance.
