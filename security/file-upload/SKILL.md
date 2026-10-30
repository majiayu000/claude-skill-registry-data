---
name: file-upload
description: Detects file upload handlers that accept executable content or write to web-
  accessible paths without validation. Use when writing file upload handlers,
  processing multipart form data, saving uploaded files to disk or cloud
  storage. Also invoke when accepting user-supplied filenames or storing
  uploads in a web-accessible directory.
---

# File Upload Security Check (A04:2025)

## What this checks

Protects against unrestricted file upload attacks where an attacker uploads executable
files (web shells, scripts, HTML with embedded JS) that the server later serves or
executes. Exploitation leads to remote code execution, stored XSS, or full server
compromise.

## Vulnerable patterns

- Upload handler that writes the user-supplied filename directly to disk, enabling path traversal and extension bypass
- Upload destination inside the web-accessible document root, so uploaded content is served directly by the web server
- No extension allowlist, or an extension denylist that misses novel or case-varied extensions
- No upload-size cap enforced at the framework or reverse-proxy level
- MIME type taken from the client-supplied `Content-Type` header rather than the file's magic bytes

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Extension is validated against an allowlist, never a denylist.** Denylists
   miss novel extensions (`.phtml`, `.phar`, `.svg`) and case variations. An
   allowlist of expected types (`.png`, `.jpg`, `.pdf`) fails closed.
2. **The user-supplied filename is never used as the storage path.** Rename the
   file to a CSPRNG identifier, preserving only the validated extension. This
   defeats path traversal (`../../etc/passwd`), overwrites of existing files, and
   filename-based XSS on download.
3. **Uploads are written outside the webroot.** The server must not serve them
   directly — files are handed out through an application route that sets a safe
   `Content-Type` and `Content-Disposition: attachment`, never inferred from the
   filename.
4. **Size is capped at the framework or proxy level**, not just inside the handler.
   A handler-only check lets a multi-gigabyte upload exhaust memory before the
   check runs.
5. **MIME type is validated against the file's magic bytes**, not the
   `Content-Type` header the client sent — the header is attacker-controlled.

Translate these principles to the audited file's language and framework. Use the
framework's documented upload-size limit, storage path configuration, and
content-type sniffing helper — do not hand-roll path joining or extension parsing.

## Verification

Confirm the following properties hold (language-agnostic):

- [ ] Only explicitly-allowed file extensions are accepted — enforced via an allowlist, not a denylist
- [ ] The user-supplied filename is never used as the storage path — files are renamed to a random or hashed identifier
- [ ] Uploaded files are stored outside the web-accessible document root
- [ ] A maximum upload size is enforced at the framework or reverse-proxy level
- [ ] Files are served with `Content-Disposition: attachment` and a safe, explicit `Content-Type` — never inferred from the filename

## References

- CWE-434 ([Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html))
- CWE-22 ([Path Traversal](https://cwe.mitre.org/data/definitions/22.html))
- [OWASP A04:2025 Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/)
