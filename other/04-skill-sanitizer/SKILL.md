---
# sanitizer: ignore-file  (self-doc: lists detection patterns as examples; not real leaks)
name: skill-sanitizer
description: >-
  Pre-share leak scanner for Claude Code skills (or any folder). Scans BEFORE
  you publish for secrets (API keys, tokens, private keys, .env values,
  high-entropy strings), PII (emails/phones), local machine paths
  (C:\Users\<name>, /home/<name>, /Users/<name>, UNC, internal hostnames),
  and client/proper-noun names from a LOCAL private dictionary; also flags
  service-specific code (jira/github/gitlab/slack/salesforce/notion/linear/
  stripe/aws/google) that should be split into a dedicated service plugin.
  Use when the user says "sanitize this skill", "before sharing a skill",
  "check for leaks", "is this skill clean", "is this safe to commit/publish/
  open-source", "scrub secrets", "redact before commit", or "pre-push leak
  check". Cross-platform, stdlib-only Python, fail-closed.
---


# skill-sanitizer

Scan a skill directory for things that must not leak publicly, BEFORE you share
or `git push` it. Reports BLOCK (hard-stop: real secrets, private keys, client
names, your own identity) and WARN (review: PII, local paths, internal hosts,
high-entropy strings, embedded service code).

## When to use

- Before publishing / open-sourcing / zipping a skill to share.
- As a pre-push or CI gate over a skill folder.
- Auditing a folder someone handed you.

## When NOT to use

- Not a runtime secret-rotation guard.
- Not a full-repo replacement for git-secrets/trufflehog (this is skill-folder scoped).
- It is report-only: it never modifies your files.

## How to run

```
python scanner.py <skill_dir>
```

Common variants:

```
python scanner.py <skill_dir> --format json       # pretty JSON to stdout
python scanner.py <skill_dir> --config .sanitizer.local.json
python scanner.py <skill_dir> --warn-ok           # WARN-only => exit 0
python scanner.py <skill_dir> --no-entropy        # disable the entropy backstop
```

The scanner prints a human report to stderr and, on the last stdout line,
exactly:

```
RESULT_JSON={"version":"1.0","scanned_root":"...","findings":[{"file","line","category","severity","snippet","suggestion"}],"counts":{"block","warn","files_scanned"},"service_plugins_suggested":[...],"suppression":{"suppressed_files","ignore_patterns","dangerous_ignore_globs","ignore_file_suppressed_files","ignore_line_suppressed_lines","ignore_line_suppressed_findings"},"scan_errors":[...],"blocked":true|false,"exit_code":0|1|2|3}
```

`snippet` is always REDACTED (first 4 + last 2 chars) — the full secret is never
emitted to the report.

## Exit codes

- `0` clean (no BLOCK, no WARN) — safe to share. Also `0` for WARN-only with `--warn-ok`.
- `1` at least one BLOCK finding (secret / private key / client name / your own identity) — HARD FAIL pre-push.
- `2` no BLOCK but >=1 WARN (PII / path / host / entropy / plugin-split) — review consciously.
- `3` scan-integrity / usage error: bad path, malformed config, a path that
  could not be scanned (unreadable, permission, Windows MAX_PATH), **OR** a
  dangerous wholesale `.sanitizerignore` glob (`*`, `*.*`, `*.py`, `**`, …) that
  could hide everything. Fail-closed — a wholesale ignore glob FAILS the gate by
  default so a naive `if exit==0: pass` CI check cannot be silently bypassed.
  Explicit named-file excludes (e.g. a skill ignoring its own `SKILL.md`) stay
  `0`. An incomplete or integrity-compromised scan is never reported as clean.

Precedence when several apply: `1` (BLOCK) > `3` (scan-integrity) > `2` (WARN) > `0`.
Fail-closed: any unreadable/binary file is byte-scanned for known-prefix BLOCK
patterns; UTF-16 (BOM or NUL-interleaved) files are decoded properly and
NUL-stripped before regex so they cannot bypass detection. The tool never
crashes and never silently passes.

## How to read findings

The agent should:
1. Locate the target skill dir.
2. Load the local config if present (`.sanitizer.local.json`).
3. Run the scanner.
4. Present BLOCK findings FIRST (with redacted previews), then WARN.
5. Propose the concrete fix printed with each finding.

Severities:
- **BLOCK** — known-prefix provider keys (`sk-`, `ghp_`, `AKIA…`, etc.), private
  keys, secret-named env assignments with real values, connection strings with
  passwords, client/proper-noun dictionary terms, and your OWN auto-seeded
  identity (username/email/hostname/git name). Must be removed before sharing.
- **WARN** — emails, phones, local machine paths, internal hosts/IPs,
  high-entropy unknown strings, and `plugin-split:<service>` advice.

## Remediation guidance

- **Secrets** → remove and rotate the credential; reference it via an env var
  (`os.environ[...]`) or a `.env.example` placeholder. Never commit the real value.
- **Local paths** → replace `C:\Users\<you>` / `/home/<you>` with `~`, `$HOME`,
  `%USERPROFILE%`, or a `<USER>` / `<project-root>` token.
- **PII** → replace personal emails with a reserved `example.com` address; drop
  phone numbers, or allowlist your own contact in the local config.
- **Client / proper-noun names** → genericize the name, or (if intentional and
  public) add it to your local allowlist.
- **Service-specific code (`plugin-split`)** → the skill embeds code for a
  specific service (e.g. Jira). Extract that code into a dedicated `<service>`
  service plugin and depend on it, so this generic skill stays portable. Example:
  move `jira/*` logic into an `atlassian-jira` plugin.

## External local config (private dictionary — never committed)

The shipped skill ships ONLY generic patterns. Anything private (client names,
project codenames, your own contact details) lives in an EXTERNAL,
**gitignored** file that you keep locally:

```
.sanitizer.local.json        # in the scanned dir, or any parent, or $HOME
```

The scanner walks up from the target dir to the filesystem root, then `$HOME`,
and loads the first `.sanitizer.local.json` it finds (cwd wins). The repo ships
ONLY `.sanitizer.example.json` as a template — the real local file must NEVER be
committed. Add this line to your `.gitignore`:

```
.sanitizer.local.json
```

Config shape (all keys optional, plain stdlib JSON):

```json
{
  "block_terms":  ["Globex", "ProjectZephyr"],
  "warn_terms":   ["northwind"],
  "client_names": ["AcmeCorp"],
  "project_codenames": ["Bluebird"],
  "own_username": "youruser",
  "own_emails":   ["you@example.com"],
  "allowlist":    { "emails": ["you@example.com"] },
  "entropy":      { "enabled": true, "min_len": 20, "base64_bits": 4.0, "hex_bits": 3.0 }
}
```

`block_terms` / `client_names` / `project_codenames` / `own_username` →
word-boundary, case-insensitive BLOCK. `warn_terms` → WARN.

## Suppression channels (READ THIS BEFORE TRUSTING A CLEAN VERDICT)

The scanner has THREE ways findings can be hidden. A "clean" result is only
trustworthy once you have reviewed what, if anything, was suppressed. The
scanner ALWAYS reports suppression in both the human report (a `SUPPRESSION`
section) and `RESULT_JSON` (a `"suppression"` object), so the consuming agent
MUST read and relay it.

1. **`.sanitizerignore`** (gitignore-style globs at the scan root) — drops whole
   files before scanning. Counted as `suppressed_files`; the active
   `ignore_patterns` are echoed back. A *dangerous wholesale* glob (`*`, `*.*`,
   `*.py`, `**`, …) that could mask code prints a loud `WARNING` AND forces a
   non-zero exit `3` (scan-integrity failure) — a `.sanitizerignore` of `*` will
   never yield a silent green "Safe to share", and a `if exit==0: pass` CI gate
   cannot be bypassed by it.
2. **`# sanitizer: ignore-file`** — an ANCHORED standalone comment in the first
   ~10 lines of a file (the comment's content must START with the token; a bare
   substring buried in code/data does NOT count). Skips that whole file.
   Counted as `ignore_file_suppressed_files`.
3. **`# sanitizer: ignore-line`** — appended to a single line; drops all findings
   on that line. Counted as `ignore_line_suppressed_lines` plus
   `ignore_line_suppressed_findings` (how many findings were actually hidden) so
   a CI/agent can tell "genuinely clean" from "a directive hid something".

The consuming agent should:
- Read `RESULT_JSON.suppression` (and `scan_errors`) BEFORE reporting "clean".
- Treat any `dangerous_ignore_globs`, nonzero `ignore_line_suppressed_findings`,
  or nonempty `scan_errors` as a reason to NOT report "safe to share" until the
  hidden content / unscanned paths have been reviewed.
- Echo the suppression counts to the user alongside the verdict.

### Unscanned paths / scan errors

If a path cannot be descended or read (Windows MAX_PATH, permissions), the
scanner does NOT report clean: it records the path under `scan_errors`, prints a
`SCAN ERRORS` section, and exits `3` (scan error) so the incompleteness is
surfaced. On Windows it retries with the `\\?\` extended-length prefix first.

## Self-clean guarantee (auto-seed + dogfood)

Even with NO config, the scanner derives your identity at runtime (in-memory
only, never written to disk) from `$USERNAME`/`$USER`, `git config user.name/
user.email`, and the hostname, and flags any of those as BLOCK — so your own
name/email/machine path is ALWAYS caught out of the box. The shipped skill
contains only generic regexes and reserved-example fixtures; running the
scanner on its own skill folder produces **zero BLOCK findings** (its own first
test / dogfood gate).
