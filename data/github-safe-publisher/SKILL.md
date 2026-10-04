---
name: github-safe-publisher
description: Prepare private work for safe public GitHub publishing. Use when the user asks to publish safely, turn private project work into a GitHub-safe artifact, sanitize a project, make a public case study, prepare material for GitHub, review a repo before pushing, or check whether files contain secrets, client data, raw prompts, logs, local paths, private source, or other sensitive material.
---

# GitHub Safe Publisher

## Overview

Use this skill to turn private project material into public-safe GitHub artifacts such as case studies, skill releases, README updates, demo notes, and example prompts. The skill produces a safety verdict and concrete next steps; it must not auto-commit, auto-push, publish, upload, send, or share anything without explicit human review.

## Workflow

1. Identify the intended public artifact: skill, case study, README section, demo screenshot note, example prompt, template, or changelog.
2. Read `references/public-safety-boundaries.md` before deciding what can be reused, generalized, or removed.
3. Work from a copy or rewritten summary, not the private original. Prefer a sanitized draft folder before touching a public repo.
4. Remove or replace sensitive details: credentials, account data, client material, raw prompts, logs, databases, exports, local paths, private source, and screenshots with private UI.
5. Run the scanner on the proposed public folder:

```bash
python scripts/scan_public_safety.py path/to/public-candidate
```

6. Read `references/release-workflow.md` before staging changes.
7. Require manual review of `git status --short`, the unstaged diff, and the staged diff before any commit or push.

## Verdicts

Return one of these verdicts in every review:

- `BLOCK`: Real secrets, credentials, raw private data, client-identifying material, local machine paths, databases, exports, logs, or unintended source files are present.
- `REVIEW`: The artifact is probably publishable after specific human checks or rewrites.
- `READY`: The artifact uses public-safe examples, passes the scanner, and has a clean manual diff review.

If blocked, explain the minimum fix. Do not rewrite blocked material into a public repo until the sensitive source is removed or generalized.

## Sanitization Rules

- Replace real people, businesses, accounts, emails, phone numbers, domains, addresses, and project codenames with neutral examples.
- Replace credentials with placeholders such as `YOUR_API_KEY_HERE`.
- Convert raw private notes into public explanations; do not copy memory files, chat logs, prompts, or operational strategy verbatim.
- Publish patterns, workflows, and lessons. Keep implementation source, deployment details, private data, and system-of-record content private unless the user explicitly confirms they are public-safe.
- For screenshots, crop or recreate them with fake data. Do not publish account menus, browser tabs, analytics, emails, invoices, API dashboards, or file paths.

## Scanner

Use `scripts/scan_public_safety.py` for a deterministic first pass. Treat it as a guardrail, not proof of safety.

Recommended commands:

```bash
python scripts/scan_public_safety.py path/to/candidate
python scripts/scan_public_safety.py path/to/candidate --json
python scripts/scan_public_safety.py path/to/candidate --no-baseline
```

The scanner checks risky filenames, file extensions, binary-like artifacts, local path patterns, credential terms, token formats, private-key blocks, and private/client wording. Folder scans use `.public-safety-baseline.json` when present to suppress known review findings; use `--no-baseline` to see the raw scan. A clean scan still requires human diff review.

## Git Safety

- Never run broad staging commands such as `git add .` unless the user has already reviewed the whole repo state.
- Prefer staging named files only after inspecting them.
- Always inspect:

```bash
git status --short
git diff -- path/to/file
git diff --cached
```

- Do not commit or push unless the user explicitly asks for that action after the safety review is clean.

## Output Format

When preparing or reviewing a public candidate, respond with:

1. Verdict: `BLOCK`, `REVIEW`, or `READY`.
2. Public artifact type and target repo/folder.
3. Files inspected or created.
4. Scanner result summary.
5. Remaining manual checks.
6. Exact next commands, if any, without auto-running publish actions.
