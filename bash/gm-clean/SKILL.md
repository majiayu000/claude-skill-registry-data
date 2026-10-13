---
name: gm-clean
description: "Archive GitHub notification emails from Takazudo's personal dev orgs (Takazudo, zudolab) out of the takazudo@gmail.com inbox. Use when: (1) User invokes /gm-clean, (2) User says 'clean gmail', 'archive github mails', or 'clear github notifications from inbox'. Covers issue, PR, review and CI-run notifications for every repo under those two orgs. Never touches work orgs (pxgrid, SAISONCARD, etc.). Archive only — removes the INBOX label, never deletes."
---

# gm-clean

Archive personal-dev GitHub notification emails so they stop competing for attention in the inbox. The emails stay in All Mail and remain searchable.

## Filter

```
in:inbox from:notifications@github.com (list:Takazudo.github.com OR list:zudolab.github.com)
```

- GitHub stamps every notification with `List-ID: <repo>.<owner>.github.com`. Matching the owner suffix scopes this to the two personal orgs exactly, so issues, PRs, reviews and CI runs of any repo — current or future — are caught without listing repos.
- Work orgs (`pxgrid/*`) have a different owner suffix and never match. `SAISONCARD/*` mails carry no List-ID and never match either.
- The org list lives in `ORGS` at the top of the script. Add an org there, not in ad-hoc queries.

## Run

Default: archive immediately, no confirmation (archiving is reversible).

```bash
python3 $HOME/.claude/skills/gm-clean/scripts/gm-clean.py
```

Flags (pass through when the user asks):

- `--dry-run` — count matches, archive nothing
- `--by-repo` — also print per-repo counts; costs one metadata read per message, so it is slow on large inboxes

The script talks to the Gmail API directly with the `gmail-ws` MCP's saved OAuth credential, and uses `batchModify` (1000 ids per call). Do **not** use the MCP tools for this — paging and per-message label edits are far slower and hit the per-minute quota.

## Report

Relay `matched`, `archived`, and `remaining in inbox` (should be 0; a non-zero value means new mail arrived mid-run — just rerun).

## Failures

- `saved credential lacks gmail.modify` → call `mcp__gmail-ws__start_google_auth` (service `gmail`, email `takazudo@gmail.com`), have the user approve in the browser, rerun.
- `ERROR 400 invalid_grant` on token refresh → the refresh token was revoked; same re-auth.
- Repeated 403 quota errors are retried with a 20s wait; if it still exits, wait a minute and rerun.
