---
id: file-upload-security
version: "2.0.0"
title: "File Upload Security"
description: "Accept, store, process, and serve user uploads safely: type-appropriate content validation, decompression limits, generated storage keys, quarantine before publication, isolated media processing, and scoped direct-to-storage credentials. Use when generating a file-upload endpoint, wiring presigned or SAS uploads to S3, GCS, or Azure Blob, processing user-supplied images or documents, or serving user-generated content."
category: prevention
severity: high
applies_to:
  - "when generating an HTTP file-upload endpoint"
  - "when wiring direct-to-storage upload (S3 presigned, GCS signed URL, Azure SAS)"
  - "when parsing, re-encoding, or extracting user-supplied files"
  - "when serving or linking user-generated content"
languages: ["*"]
token_budget:
  minimal: 1300
  compact: 1800
  full: 2300
rules_path: "rules/"
related_skills: ["ssrf-prevention", "api-security", "container-security", "deserialization-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP File Upload Cheat Sheet"
  - "CWE-434: Unrestricted Upload of File with Dangerous Type"
  - "CWE-409: Improper Handling of Highly Compressed Data"
  - "CWE-22: Path Traversal"
  - "CVE-2016-3714 (ImageTragick), CVE-2021-22205 (GitLab ExifTool RCE)"
---

# File Upload Security

## Rules (for AI agents)

### ALWAYS
- Put every new upload in a **non-public quarantine** location, and do not expose it,
  link it, index it, or hand it to a downstream workflow until validation has
  succeeded. Quarantine → validate → process → publish, in that order. This is the
  invariant the rest of these rules hang from, and the one direct-to-storage uploads
  most often skip.
- Validate content **server-side with checks appropriate to the format**. Where a
  format has a reliable signature, verify it; for container and document formats —
  DOCX, XLSX and ZIP are all ZIP at the container level — also validate structure
  against the format you expect. Text-based formats such as SVG and CSV have no
  signature to check at all, so a signature check alone is not a content policy. The
  client's `Content-Type` and the filename are attacker-controlled and are never the
  check.
- Keep a **per-endpoint allowlist** of accepted types and deny everything else. Deny
  `image/svg+xml` by default: an SVG is a document that can carry script. Where an
  endpoint genuinely requires SVG, treat it as active content — rasterize it, or run
  a maintained **SVG-aware** sanitizer with an explicit element, attribute, URL and
  CSS allowlist. A generic HTML sanitizer is the wrong tool for it.
- Bound the **expansion**, not only the upload. For archives and compressed or
  container formats, cap expanded bytes, entry count, nesting depth, compression
  ratio, per-entry size and processing time, and reject before extracting when the
  projected expansion exceeds policy. A limit on the compressed bytes says nothing
  about what they become (CWE-409).
- Store under an **application-generated identifier** — a UUID or content hash —
  outside the executable or web document root, and never build the storage path from
  the user-supplied name. Keep the original filename as bounded metadata only, and
  encode it for the specific output context where it is displayed. There is no
  "escaped at rest" that is safe in every context.
- Run every parse, re-encode or extraction of untrusted bytes in an **isolated
  worker**: least privilege, no unnecessary network, and CPU, memory and wall-clock
  limits. The decoder is the attack surface, so invoking one is not itself the
  defense — ImageTragick (CVE-2016-3714) and the GitLab ExifTool RCE (CVE-2021-22205)
  were both a server handing user bytes to a media library. `container-security` owns
  what that isolation looks like.
- Scan for malware where the threat model calls for it, out of band, with the object
  still quarantined. Do **not** send uploads to a third-party or public scanning
  service — VirusTotal among them — unless the data classification explicitly permits
  disclosing that content to that provider. Submitting a customer contract for
  scanning is disclosing the contract.
- Serve according to what the content is. Untrusted content a browser may render
  inline belongs on an **isolated, cookie-less origin**, with a server-determined
  `Content-Type`, `X-Content-Type-Options: nosniff`,
  `Content-Disposition: attachment` wherever inline rendering is not required, and
  `Content-Security-Policy: default-src 'none'; sandbox`. A private document behind an
  authorizing application handler is a different and equally acceptable architecture.
  `nosniff` narrows type sniffing; it does not make a shared origin safe for active
  content.
- For **direct-to-storage** uploads, scope the credential with the provider's own
  mechanism to the intended object, operation and a short lifetime, and apply
  provider-side size constraints where they exist. A signed `Content-Type` binds the
  header the client sends, not the bytes — the stored object still has to be
  validated server-side before it leaves quarantine, and your gateway and application
  size limits do not sit on this path at all.
- Where the "upload" accepts a **URL** and the server fetches it, apply
  `ssrf-prevention` before the fetch, with size and time limits on the response.
  Validation starts on what comes back. `api-security` owns who may upload and who
  may read the result.

### NEVER
- Treat the client's `Content-Type` or the filename extension as the type check.
- Treat successful parsing as proof of safety. A structurally valid PDF is still a
  PDF that can carry active content; `pdfinfo` answers "is this parseable", not "is
  this safe to render or redistribute".
- Extract an archive without a path-traversal-safe extractor. Zip Slip
  (CVE-2018-1002201) wrote outside the target directory through `../` entries — a
  separate problem from how much the archive expands, and both need handling.
- Publish, link, index, or pass downstream an object that has not left quarantine.

### KNOWN FALSE POSITIVES
- An integration that must round-trip the user's filename: preserve it as metadata
  and encode it at the point of display. The stored object key is still generated.
- Signed build artifacts (tarballs, DEBs, RPMs) may rely on supply-chain signature
  verification instead of commodity AV where policy defines that trust model. Verify
  the signature **before** parsing or extracting, and note that it waives nothing
  else — safe extraction, decompression limits and sandboxed processing all still
  apply. A signature proves origin, not that the bytes are harmless.

## Context (for humans)

Upload endpoints are a persistent rich target because the path from upload to
execution is short: an HTML file with a credential stealer, a shell dropped into a
misconfigured document root, an SVG carrying script, an image that reaches a
vulnerable decoder.

The defenses are individually well understood and cheap. What makes them fail is
applying them one at a time. A signature check is bypassed by a polyglot — a file
that is simultaneously a valid PNG and a valid HTML page. An isolated serving origin
neutralises that polyglot's HTML. A decompression limit stops the archive that
validates fine and expands to fill the disk. Each is a layer, and a missing layer is
what turns stored data into stored execution.

Two boundaries are worth stating plainly because they are where this skill's rules
most often get misread. **Parseable is not safe** — every structural validator
answers a question about format, never about intent. And **scanning is disclosure**:
sending a file to an external service to ask whether it is malicious hands that
service the file, which is a decision about data classification and not only about
security.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/direct-upload.md` — what a presigned URL, a GCS signed URL and an Azure
  SAS actually bind, and what each leaves for the server to validate
- `references/format-handling.md` — content validation per format, SVG sanitizer
  choice, archive limits, and hardening the media processors
- `rules/upload_validation.json`
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).
- [CWE-434](https://cwe.mitre.org/data/definitions/434.html) · [CWE-409](https://cwe.mitre.org/data/definitions/409.html) · [CWE-22](https://cwe.mitre.org/data/definitions/22.html).
- [Snyk Zip Slip](https://snyk.io/research/zip-slip-vulnerability) · [ImageTragick](https://imagetragick.com/).
