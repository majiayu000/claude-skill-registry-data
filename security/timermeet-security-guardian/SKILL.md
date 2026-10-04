---
name: timermeet-security-guardian
description: Run TimerMeet's security checks (bandit static analysis, pip-audit dependency scan) and review the hardening checklist before a release. Use before tagging/publishing, and after any change touching file I/O, URL handling, subprocess, or dependencies.
---

# TimerMeet Security Guardian

## Overview

TimerMeet is a local, single-user Windows desktop app with **no server and no listening port** -- that entire network attack surface was removed by the v2.0.0 rewrite from a PHP/JS web app. Scope hardening to what actually applies to that threat model: safe file handling, a strict URL scheme allow-list, and clean dependencies. Don't invent controls for threats that don't exist here (there's no auth, no multi-tenant data, no network input to defend against).

## Workflow

1. Run the static/dependency scans:
   ```powershell
   python -m bandit -r timermeet_app timermeet.py build_exe.py -f txt
   python -m pip_audit -r requirements.txt -r requirements-dev.txt
   ```
2. Every bandit finding must end up either fixed or annotated `# nosec B<code> - <one-line reason>` directly in the diff -- never suppressed via a blanket config with no visible reason.
3. Any `pip_audit` finding (a known CVE in a pinned/installed version) must be resolved by upgrading, or explicitly written up as an accepted risk in `SECURITY.md` -- never silently ignored.
4. Re-run `python -m unittest discover -s tests` after any security-motivated change.
5. Walk the checklist in `references/checklist.md` against the actual diff.
6. Keep `SECURITY.md` accurate and modest in scope (see below).

## SECURITY.md guidance

- Supported version: latest tagged release only. This is a single-maintainer project, not one with a long-term support matrix -- don't write a policy that won't be honored.
- Reporting: a GitHub issue on the public repo (`erickson558/timermeet`) is the reporting channel; there's no dedicated security contact/PGP key to promise.

## References

- `references/checklist.md` -- the concrete hardening checklist to walk through before every release.

## Deeper audits

This skill is the fast, cheap gate for every release. When the user explicitly asks for a real vulnerability hunt (worried about "being hacked", wants a security audit/pentest-style review, or before a major version), use the `timermeet-security-audit` skill instead/in addition -- it runs a slower, adversarially-verified multi-angle hunt this routine checklist isn't designed to catch on its own.
