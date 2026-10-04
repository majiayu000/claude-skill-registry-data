---
name: web-research-safe
description: Perform read-only web research with governed browser proposals for manual review.
risk: low
required_tools:
  - web.search
  - web.fetch
  - browser.open
approval_required_for:
  - browser.click_proposed
  - browser.type_proposed
---

# Web Research Safe

Use this skill when the user wants current public information from the web.

Rules:
- Prefer `web.search` and `web.fetch` for read-only research.
- Use `browser.open` only as a dry-run proposal for manual page review.
- Never click, type, submit, download, purchase, log in, or fill forms.
- Never request password, token, seed phrase, payment card, or private account input.
- Treat browser/app bridge actions as one-action proposals that require validation, approval, and audit.

