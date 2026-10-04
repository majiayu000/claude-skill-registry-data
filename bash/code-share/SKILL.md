---
name: code-share
description: Share code via GitHub Gist instead of inline chat blocks. Use when code output exceeds 10 lines, when the user asks for copy-friendly code sharing in Discord/chat, or when preserving formatting is important.
---

# Gist Code Share

When returning code:

1. If code is 10 lines or fewer, inline code block is allowed.
2. If code is over 10 lines, prefer GitHub Gist.
3. Default to **secret gist** unless user asks for public.
4. Return a short summary + gist URL; avoid pasting long duplicate code in chat.
5. Never publish secrets in shared code. If sensitive values are needed, use placeholders and tell user to fill them locally.

## Required checks

- Verify GitHub CLI auth: `gh auth status`
- If not authenticated (or missing gist scope), ask user to run: `gh auth login`
- Keep behavior simple: do not auto-fallback to alternate sharing backends by default; prefer guiding user to configure GitHub properly.

## Sensitive data policy (mandatory)

Before sharing code, scan for sensitive data and remove it.

- Never include API keys, tokens, passwords, private keys, cookies, session IDs, webhook secrets, phone/email PII, or absolute local secret paths.
- If code requires secrets, replace with placeholders, for example:
  - `API_KEY="<FILL_ME>"`
  - `TOKEN="<YOUR_TOKEN_HERE>"`
  - `.env` entry with empty value
- Add a short note telling the user to fill placeholders locally after copying.

## Update mode (same URL)

When user asks to modify previously shared code, prefer updating the same gist link (new revision) instead of creating a new gist.

Use:

```bash
./scripts/update_gist.sh <gist_url_or_id> <file> "<short description>" [public|secret] [lang]
```

Behavior:
- Keep the same gist URL.
- Save changes as a new revision.
- Return the same fixed 3-line response format.

Create a new gist only when:
- user explicitly asks for a new link, or
- existing gist is not editable by current GitHub account.

## Create gist

Use:

```bash
gh gist create <file> --desc "<short description>"
```

If code is generated in-session, write it to a temp file in workspace first. Use language-appropriate extension (`.py`, `.js`, `.ts`, etc.) so Gist syntax highlighting works well.

With bundled script:

```bash
./scripts/create_gist.sh <file> "<short description>" [public|secret] [lang]
```

If `<file>` has no extension, pass `[lang]` (for example `python`, `typescript`) so the script can upload with a proper extension.

Default behavior: do **not** use `--web` (automation-friendly).
Optional: use `--web` only when the user explicitly asks to open the gist in browser immediately.

## Response format (fixed)

Always use exactly this 3-line format:

1. One sentence on what was shared.
2. Gist URL (separate line).
3. `File: <filename> · Lines: <line_count>`

Example:

Shared the full script as a secret Gist for clean copy/paste.
https://gist.github.com/...
File: lc761_solution.py · Lines: 42
