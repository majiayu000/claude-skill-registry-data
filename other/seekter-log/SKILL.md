---
name: seekter-log
description: Update the application tracker. Record replies (rejection, screening, interview, offer), log an application the user made by hand, or sweep the inbox for replies. Use when the user runs /seekter-log, says a company replied or rejected them, or asks to check emails for responses.
---

# /seekter-log — keep the tracker true

All changes go through `scripts/seekter.py`; never edit front matter or `skipped.md` by hand. `move` changes the status inside the file (files never change folder) and appends a log line; moving a skip to any other status turns its table row into a file, and moving a file to `skipped` turns it into a row.

## A. The user tells you something

| User says | Command |
|---|---|
| "X rejected me" | `python3 scripts/seekter.py move <url-or-file> rejected --note "<date>, <one line from the mail>"` |
| "X invited me to a call / screening / interview" | `move … interviewing --note "<stage, date, who>"` |
| "Got an offer from X" | `move … offer --note "<amount, deadline>"` |
| "I applied to X myself" | `check <url>` first, then `add --status applied --source manual --notes "applied by hand"` |
| "Forget X" / "Don't apply to X again" | `move … skipped --note "<reason>"` and add X to the blacklist in `profile/profile.md` §7 |

Find the file first when the user only gives a company name: `python3 scripts/seekter.py list | grep -i <company>`. If several rows match, ask which role.

## B. Inbox sweep (when the user asks, or weekly)

Follow "Reply analysis" in `reference/sources/inbox.md`: open the user's webmail in Claude in Chrome, collect messages since the last sweep, **read bodies, not subjects**, and match with the rejection regex there (then read the matched sentence; boilerplate like "if you are not selected" is a false positive).

**Read every folder the profile's §11 table lists**, and re-read that table each sweep rather than trusting a remembered count: the list grows. It went from three folders to four on 25 Sept when **Action Required** was added for mail that asks the candidate to act.

For each reply:
1. Match it to a tracker row by company (and role if several). No match → it's an application missing from the tracker: `add` it with `--source inbox`.
2. `move` it to `rejected` / `interviewing` / `offer` with a one-line note and the mail date.
3. Anything asking the user to act (take-home, scheduling link, questions) → tell the user; never reply on their behalf. **Move that mail into the `Action Required` folder** so it is not buried in the hundreds of confirmations in Job Application. Move it back to Job Application once the thing is done. Rejections and "we received your application" mails never go there.

Postings with no reply after 30 days: `move … closed --note "no response after 30 days"` only when the user asks for a clean-up.

## C. Finish

`python3 scripts/seekter.py index`, then report in two lines: what moved where, and anything that needs the user.
