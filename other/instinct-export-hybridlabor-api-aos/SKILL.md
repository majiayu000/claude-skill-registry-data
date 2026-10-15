---
name: instinct-export
description: >-
  Use when the user wants to share or back up learned instincts — validates
  the local instincts file, allowlists the six known fields, strips secrets
  and home-directory paths, and writes a sanitized JSON artifact the user
  names. Never modifies the instincts file itself.
category: bdb-core
---

# instinct-export — sanitize and share learned instincts

Concept inspired by the instinct/skill-create ideas in affaan-m/ECC;
no code copied.

Instincts are small learned behaviours stored locally under
`~/.aos/instincts/instincts.json` (format defined in `/instinct-status`).
Exporting one means making it portable — into version control, a teammate's
machine, a dotfile repo. That is exactly where leaks happen, so sanitization
is the job, not a nicety.

## 1. Read and validate the source

Read `~/.aos/instincts/instincts.json`. If it is missing, the file is not
silently treated as empty: report that there is nothing to export and stop.
If the JSON does not parse, fail loudly with the parse error — never export
garbage "with best effort".

**Shared bounds, same as on the import side:** `trigger` and `action` must be
JSON strings ≤ 200 / ≤ 400 characters, no newlines or control characters;
at most 200 instinct entries. A store that fails these bounds is corrupt, not
exportable — fail loudly with the reason the same way as the parse-error path
above, never ship an artifact `/instinct-import` would reject wholesale.

**Field allowlist:** every exported entry keeps exactly the six shared fields
— `id`, `trigger`, `action`, `confidence` (0–1), `source`, `updated` — and
**every other field is dropped.** No auxiliary metadata travels with the
entry. Nothing on the allowlist is negotiable; extra fields are removed, not
published.

## 2. Redact — drop anything that looks like a credential or a leak

For every entry, scrub `trigger` and `action` against these redaction rules
(a hit means remove the content, or the whole entry if the lesson dies with
it):

- `sk-…` prefixed keys.
- `ghp_…` tokens.
- `github_pat_…` tokens.
- `xox`-prefixed Slack tokens (`xoxp-`, `xoxb-`, …).
- AWS `AKIA…` access-key ids.
- JWTs: three dot-separated base64 parts (`header.payload.signature`).
- Any base64 or hex run of 32+ characters.
- URL userinfo: `user:pass@…` in any URL.
- E-mail addresses.
- Absolute home paths: `/Users/<name>/…`, `/home/<name>/…`,
  `C:\Users\<name>\…`. Rewrite to `~/…`
  or describe the location in words. Relative paths (`src/lib/`) are safe.

An instinct that only exists to memorialize a secret is dropped, not
partially redacted. **A missing entry is recoverable; a leaked credential is
not.**

## 3. Re-scan the output before writing

After redaction and field-filtering, serialize the JSON and scan the whole
serialized output once more against the section-2 list before any write.
Redaction that happens only on the entry objects can miss paths, e-mails or
tokens introduced by formatting or by fields added late; the final scan is
what closes that gap. If the re-scan still finds a hit, fix it and re-scan
again — never write with a known hit remaining.

## 4. Write the artifact

Default if the user names no path: a scratch/output folder the user names —
for example `~/instinct-export/instincts-YYYY-MM-DD.json`. Never the home
root (`~/instincts-export-….json` is out), never a dotfiles repo path, never
inside `~/.aos/`. If the user names a path inside the AOS state dir, refuse
it — resolve `..` segments and symlinks first and check the resolved path,
not the spelled-out one. Never overwrite an existing export file without the
user's explicit yes. The export keeps `version: 1` and an `exported:
<ISO date>` key at the top level; the instincts file itself is never
modified.

## 5. Report

Summarize: N instincts exported, K sanitized (list the `ids`), M omitted and
why (one line each). Show the output path and state that the original file
was untouched.
