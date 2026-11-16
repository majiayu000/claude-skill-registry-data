---
name: file-upload-security
description: Accept user file uploads without introducing remote code execution, stored XSS, or polyglot attacks. Covers magic-byte validation, strict type allowlists, image re-encoding to defang embedded payloads, EXIF stripping, virus scanning, path-safe storage keys, and serving via a separate origin with Content-Disposition. Invoke when adding upload to a new endpoint or migrating from local-disk storage to object storage.
---

# File Upload Security

User-uploaded files are one of the highest-leverage attack surfaces. A single endpoint that accepts `*` MIME types and writes to a server-served path is a path to RCE, XSS, SSRF, stored-XSS in PDFs, and a half-dozen other failure modes. The defaults of every web framework do **less** than they should — this skill is what to add on top.

Generic, not CMS-specific. For Payload-specific tuning see [`payload-cms-security`](../payload-cms-security/SKILL.md). For WordPress see [`wordpress-hardening`](../wordpress-hardening/SKILL.md). For storage choice / backend architecture see [`backend-architecture`](../backend-architecture/SKILL.md).

## When to invoke

- Adding file upload to an endpoint for the first time
- A user-uploaded file caused or contributed to an incident
- Migrating from local-disk uploads to object storage (R2 / S3 / Spaces)
- Reviewing an existing upload feature you inherited
- Adding new file types (e.g. previously images only, now PDFs too)

## The threat model

A user can upload anything labeled as anything. From your perspective:

- The **filename** is attacker-controlled — `../../etc/passwd`, `🔥.jpg.exe`, `index.html`
- The **`Content-Type` header** is attacker-controlled — JPG bytes claiming to be `application/json`, executable bytes claiming to be `image/png`
- The **file extension** is attacker-controlled
- The **file contents** may be a polyglot — bytes that are valid as image *and* valid as HTML / JavaScript / PHP

Defense: trust nothing the client says about the file. Inspect the bytes, re-derive the type, generate your own key for storage, serve from an origin that cannot execute anything.

## Step 1 — Validate at the boundary

### Size limits, server-side

```ts
import multer from 'multer';

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024,    // 10 MB hard cap
    files: 5,
    fields: 20,
    fieldSize: 1024,
    fieldNameSize: 100,
  },
});

app.post('/api/upload', requireAuth, upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'no file' });
  // ... continue with content validation
});
```

Defaults from middleware libraries are too generous (50MB+). Set what you actually need. Different endpoints get different caps — avatar upload doesn't need 10MB.

### Magic-byte detection (not MIME)

`Content-Type` is a hint. Read the first bytes to determine the *actual* type.

```ts
import { fileTypeFromBuffer } from 'file-type';

const detected = await fileTypeFromBuffer(req.file.buffer);
if (!detected) {
  return res.status(400).json({ error: 'unrecognized file type' });
}

const ALLOWED_MIMES = new Set([
  'image/jpeg',
  'image/png',
  'image/webp',
  'application/pdf',
]);

if (!ALLOWED_MIMES.has(detected.mime)) {
  return res.status(400).json({ error: `type ${detected.mime} not allowed` });
}
```

For Python: `python-magic` (`libmagic` bindings). For Go: `mimetype`. For Ruby: `marcel`.

Allowlist, not denylist. "Anything except `.exe` and `.php`" misses `.phtml`, `.phar`, `.shtml`, `.cgi`, `.pl`, `.jsp`, `.aspx`, and tomorrow's bypass.

### Filename — never trust the client's

Never store with the client-supplied name. Generate one server-side.

```ts
import { randomUUID } from 'node:crypto';

const ext = detected.ext;                     // from file-type, not from filename
const storageKey = `uploads/${userId}/${randomUUID()}.${ext}`;
```

Patterns to enforce in the storage key:

- **Generated, not user-supplied** — UUID, ULID, or content-hash (SHA-256 of bytes — also gives you free dedup)
- **No path traversal possible** — no `..`, no leading `/`, no special characters. With a UUID this is automatic.
- **Scoped by owner** — `uploads/<userId>/<random>` makes per-user access policies trivial
- **No executable extensions** — extension comes from server-detected type, not client filename

If you must keep the original filename for display, store it as a separate database field, never as part of the storage key.

## Step 2 — Defang content

The bytes are the problem. After validation, transform the file so any embedded payload becomes inert.

### Images: re-encode

Run every image through `sharp` (or equivalent) to a known format. This:

- Strips polyglot bytes — the re-encoded image is just the visual content
- Removes EXIF metadata — including geotags (PII leak)
- Normalizes the format — your storage layer holds known-good images

```ts
import sharp from 'sharp';

const processed = await sharp(req.file.buffer)
  .rotate()                              // honor EXIF orientation, then drop EXIF
  .resize({ width: 4096, height: 4096, fit: 'inside', withoutEnlargement: true })
  .jpeg({ quality: 85, progressive: true })  // or .webp() for modern
  .withMetadata({ exif: {} })            // strip EXIF
  .toBuffer();

// Upload `processed`, not `req.file.buffer`
```

A PHP webshell embedded in a JPEG file does not survive re-encoding. So does most ImageTragick-style abuse. The cost is a few hundred ms of CPU per upload.

### PDFs and documents

Re-encoding a PDF is harder than re-encoding an image, but you can:

- **Strip JavaScript** with `qpdf` / `pdfcpu` — removes embedded JS that some PDFs use for "interactive" forms (or for malware)
- **Convert to PDF/A** — a more restricted PDF subtype, no JS allowed
- **Render to image + new PDF** — destroys text but eliminates everything else; only when you really need it (legal redaction, etc.)

```bash
# Strip JavaScript and re-write the PDF
qpdf --decrypt --remove-restrictions input.pdf cleaned.pdf

# Or convert to PDF/A
qpdf --object-streams=disable --linearize input.pdf cleaned.pdf
```

### Office documents

Active content is the issue (VBA macros, OOXML scripting). Three options, increasingly strict:

1. **Scan for macros** — reject if present (LibreOffice headless can introspect)
2. **Convert to PDF** server-side and store the PDF — destroys macros and most other active content
3. **Don't accept Office docs** — accept PDF only, instruct users to convert client-side

### Generic / unknown types

If you really must accept "any file", treat the upload like a quarantine zone:

- Never serve from a domain that can execute
- Always with `Content-Disposition: attachment` (forces download, not inline render)
- Pass through a virus scanner (ClamAV is free, decent for known malware) — see Step 4

## Step 3 — Storage and serving

### Storage: object storage, not local disk

See [`backend-architecture`](../backend-architecture/SKILL.md) for the "images disappear on redeploy" trap. For uploads specifically:

- **S3-compatible storage** (S3, R2, B2, Spaces, MinIO if self-hosted)
- **Private bucket** with signed URLs for access — never make the bucket public unless the content really is public
- **Path scoped by owner** — `uploads/<userId>/<key>` so IAM policies can restrict access by prefix

### Serving: separate origin, no script execution

The cardinal sin: serving user uploads from the same origin as your app, with `Content-Type` derived from extension and no `Content-Disposition`. An attacker uploads `xss.html`, your server serves it as `text/html` from your app's origin, the attacker links to it, and now they have stored XSS with same-origin access to your auth cookies.

Patterns:

- **Serve from a separate domain** — `cdn.example.com` or `uploads.example.com`. Even if XSS lands here, your auth cookies are not in scope.
- **`Content-Disposition: attachment`** for non-image uploads — forces download instead of inline rendering for browsers that would otherwise sniff into something dangerous
- **Strict `Content-Type`** — match the server-detected type from Step 1, not the original
- **`X-Content-Type-Options: nosniff`** — disables browser MIME-sniffing
- **`Content-Security-Policy: default-src 'none'`** for the uploads origin — even if HTML lands there, the CSP refuses to render scripts/images/anything
- **No directory listing** on the bucket

```nginx
# Example serving config for the upload origin (nginx fronting R2/S3)
server {
    listen 443 ssl;
    server_name uploads.example.com;

    add_header X-Content-Type-Options nosniff always;
    add_header Content-Security-Policy "default-src 'none'; img-src 'self'; style-src 'unsafe-inline';" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Force download for anything not in the image allowlist
    location ~* \.(jpg|jpeg|png|webp|gif|svg)$ {
        # served inline as images
    }
    location / {
        add_header Content-Disposition "attachment" always;
    }
}
```

### SVG is special

SVG is XML with `<script>` support. If a user uploads `evil.svg` and you serve it as `image/svg+xml`, browsers render the SVG **and execute its scripts**. SVG is effectively HTML in disguise.

Options:

- **Don't accept SVG** if you can avoid it (most "image upload" features don't need vector)
- **Sanitize SVG** with `DOMPurify`'s SVG mode or `svg-sanitizer` (PHP) before storing
- **Force download** with `Content-Disposition: attachment` even if served as `image/svg+xml`

### Signed URLs for private content

For per-user / per-tenant uploads (not public), generate short-lived signed URLs at access time:

```ts
import { GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

app.get('/api/files/:id', requireAuth, async (req, res) => {
  const file = await db.files.findFirst({
    where: { id: req.params.id, userId: req.user.id }      // BOLA check — see api-security
  });
  if (!file) return res.status(404).end();

  const url = await getSignedUrl(
    s3,
    new GetObjectCommand({ Bucket: 'uploads', Key: file.storageKey }),
    { expiresIn: 300 }  // 5 minutes
  );
  res.json({ url });
});
```

5-minute TTL is plenty for direct downloads; longer only if needed.

## Step 4 — Virus scanning (for non-image uploads)

For PDFs, Office docs, archives, and "any file" features, run a virus scan. Not perfect, but catches known-malicious files.

- **ClamAV** is free, self-hostable, decent for known malware. Run as a daemon, scan via socket.
- **VirusTotal API** for higher fidelity (paid) — also gives you reputation signals
- **Hosted scanners** — Cloudflare (with paid tier features), bundled with some CDN providers

```ts
// Sketch — clamav-client style
import { Clam } from 'clamav.js';
const clam = new Clam({ host: '127.0.0.1', port: 3310 });

const scanResult = await clam.scan(req.file.buffer);
if (scanResult.isInfected) {
  await db.uploadAttempts.create({
    data: { userId: req.user.id, reason: 'av-positive', signature: scanResult.viruses.join(',') }
  });
  return res.status(400).json({ error: 'file rejected' });
}
```

False positives happen — log them, allow operator review, don't punish the user with a confusing error.

## Step 5 — Pre-signed PUT for large uploads

For files > a few MB, having the user upload through your app server is wasteful. Pre-signed PUT URLs let the browser upload directly to S3/R2 while your app stays in control:

```ts
import { PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

app.post('/api/uploads/request', requireAuth, async (req, res) => {
  const { filename, size, mime } = req.body;

  // Server-side validation BEFORE issuing the URL
  if (size > 100 * 1024 * 1024) return res.status(400).json({ error: 'too large' });
  if (!ALLOWED_MIMES.has(mime)) return res.status(400).json({ error: 'type not allowed' });

  const storageKey = `uploads/${req.user.id}/${randomUUID()}`;
  const url = await getSignedUrl(s3, new PutObjectCommand({
    Bucket: 'uploads',
    Key: storageKey,
    ContentType: mime,
    ContentLength: size,
  }), { expiresIn: 300 });

  // Record the pending upload so we know what to validate after
  await db.pendingUploads.create({ data: { storageKey, userId: req.user.id, expectedSize: size, expectedMime: mime }});

  res.json({ url, storageKey });
});

// Browser PUTs the file directly to `url`. After upload completes,
// the client calls /api/uploads/confirm with the storageKey.

app.post('/api/uploads/confirm', requireAuth, async (req, res) => {
  const { storageKey } = req.body;
  const pending = await db.pendingUploads.findFirst({
    where: { storageKey, userId: req.user.id }
  });
  if (!pending) return res.status(404).json({ error: 'no pending upload' });

  // Fetch the uploaded object, validate magic bytes server-side, then re-encode/scan
  const obj = await s3.send(new GetObjectCommand({ Bucket: 'uploads', Key: storageKey }));
  // ... validation, re-encoding, scanning as usual
  // If validation fails, delete the object
});
```

The browser uploads big files efficiently; your app stays the gatekeeper for validation, scanning, and re-encoding (via a worker that picks up confirmed uploads).

## Step 6 — Operational hygiene

- **Orphan cleanup** — pending uploads that never confirmed, abandoned files when records are deleted. Daily cron.
- **Per-user quota** — soft cap with notification, hard cap with rejection. Prevents one user filling your bucket.
- **Per-IP / per-account rate limit** on upload endpoints — stops bulk abuse
- **Backup the bucket** — see [`backup-disaster-recovery`](../backup-disaster-recovery/SKILL.md). Object storage is durable but not deletion-proof.
- **Audit log of uploads** — who uploaded what, when, what was the validation result. See [`log-strategy`](../log-strategy/SKILL.md).
- **Periodic re-scan** — virus signatures update; what passed yesterday may be flagged today. Re-scan high-value buckets monthly.

## Checklist

For a file-upload feature going to production:

- [ ] Server-side size cap matches actual need (not framework default)
- [ ] Magic-byte detection used; MIME header from client ignored
- [ ] Strict type allowlist (not denylist)
- [ ] Storage key generated server-side (UUID / hash); no client filename in the path
- [ ] Images re-encoded through `sharp` / equivalent; EXIF stripped
- [ ] PDFs run through `qpdf` to strip JS, or converted to PDF/A
- [ ] SVG not accepted, or sanitized before storage
- [ ] Office docs converted to PDF server-side, or rejected
- [ ] Stored in object storage with a private bucket; signed URLs for access
- [ ] Served from a separate origin (`cdn.example.com`, not `app.example.com`)
- [ ] `X-Content-Type-Options: nosniff` set on the upload origin
- [ ] Strict CSP on the upload origin (`default-src 'none'` baseline)
- [ ] `Content-Disposition: attachment` for non-image types
- [ ] Virus scan in place for non-image uploads
- [ ] Per-user quota and per-IP rate limit
- [ ] BOLA-safe download: owner check on every fetch (see [`api-security`](../api-security/SKILL.md))
- [ ] Orphan / abandoned upload cleanup runs daily
- [ ] Bucket itself is backed up

## What this skill will not do

- Help build upload features for systems you do not own
- Endorse serving user uploads from the application's own origin without `Content-Disposition` and a strict CSP
- Recommend "trust the client's MIME header" for any production system
