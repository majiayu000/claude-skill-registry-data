---
name: path-traversal
description: Detects file operations with user-controlled paths vulnerable to ../
  traversal, absolute paths, or symlink escapes. Use when writing code that
  opens, reads, writes, or deletes files using paths constructed from user
  input. Also invoke when serving static files, handling file downloads by
  name, or resolving paths from URL parameters or request bodies.
---

# Path Traversal Security Check (A01:2025)

## What this checks

Protects against directory traversal attacks where an attacker uses `../` sequences,
absolute paths, or symlinks to access files outside the intended directory. Exploitation
leads to reading sensitive files (`/etc/passwd`, `.env`, private keys), overwriting
configuration, or achieving remote code execution via file write.

## Vulnerable patterns

- A caller-supplied filename interpolated or concatenated into a path before opening, with no canonicalization.
- Path-join helper used as the only defense — these collapse some `..` segments but do not verify the final path stays under the intended root, and many treat an absolute caller-supplied path as overriding the base.
- Existence or stat check on the user path that does not follow symlinks, but the subsequent read/write does — symlink escape.
- Canonicalization performed once at handler entry, but a later file operation uses the un-canonicalized value.

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties. Translate each property into the audited file's language and
filesystem API — use that platform's documented canonicalization and symlink-
resolution call.

1. **The intended root is resolved to a canonical absolute path once**, up
   front. Everything that follows compares against the resolved root, not
   against a relative string that can match itself after traversal.
2. **The caller-supplied path is joined with the root, then resolved to a
   canonical absolute path that also follows symlinks** — using the platform's
   real-path / canonicalize / resolve-symlinks call. Only after this does the
   containment check make sense.
3. **The resolved target must start with the resolved root.** A mismatch means
   traversal or symlink escape; reject rather than fall through. Standard
   path-join APIs alone do not satisfy this — they collapse some `..` segments
   but do not verify containment.
4. **The check runs before every file operation** — read, write, delete, stat.
   A canonicalization that happens once at handler entry but is not re-applied
   to a later file operation is a bug.

## Verification

- [ ] Every file operation using a caller-supplied path or filename resolves to a canonical absolute path and verifies it starts with the intended root directory
- [ ] Symlinks are resolved before the containment check, blocking symlink escapes
- [ ] User-supplied filenames are never concatenated or interpolated into paths without canonicalization — path-join alone is NOT sufficient
- [ ] The root directory itself is resolved to a canonical path before comparison

## References

- CWE-22 ([Improper Limitation of a Pathname to a Restricted Directory](https://cwe.mitre.org/data/definitions/22.html))
- CWE-59 ([Improper Link Resolution Before File Access](https://cwe.mitre.org/data/definitions/59.html))
- [OWASP A01:2025 Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
