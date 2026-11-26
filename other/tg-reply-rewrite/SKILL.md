---
name: tg-reply-rewrite
description: "Use when a bot or agent reply, alert, log summary, or status report is about to go to Telegram and the reader is not an engineer — rewrite the text so a person on a phone understands what happened, how urgent it is, and what to do next, without changing any fact. Use tg-rich-messages for delivery."
license: MIT
---

# tg-reply-rewrite

Input: the raw reply. Output: the same facts as a short Telegram message for a non-engineer on a phone. This skill edits text only and sends nothing; delivery belongs to [`tg-rich-messages`](../tg-rich-messages/).

Do not rewrite when the reader asked for an exact string, JSON, code, or another machine format. Pass those through unchanged. Write in the reader's language.

## Rules

1. **First line: what happened and whether it is urgent.** It must make sense alone, in a notification preview. Take urgency from the source; if the source gives none, judge it from the consequence; if you cannot tell, say so.
2. **One thought per block.** Separate blocks with a blank line. Most urgent first.
3. **Every finding answers three questions:** what happened, what it means for the reader, what to do. End it with a ready sentence the reader can copy and send to the agent. It names the target and the expected result. Destructive steps ask for a proposal first.
4. **Explain or remove jargon.** Keep a technical term only when the reader needs it, and add its meaning in a few plain words on first use.
5. **Keep every fact, number, and identifier unchanged.** Names, versions, dates, IDs, and links stay character for character. Never invent a cause, a number, or a consequence the source does not support. A guess in the source stays a guess, and an unproven result is not reported as done.
6. **Group long identifier lists without losing them.** Show "thing: N items" and the worst two, then put the full list in a collapsed block.
7. **Commands are a last resort.** Use one only when the reader has no agent to ask, and put it in code formatting with one line saying what it does.
8. **What is fine goes in one line at the end.** List the checks that passed and nothing more. If everything is fine, that line is the whole message.
9. **Secrets never pass through.** Rule 5 does not cover tokens, passwords, or private keys: replace them with `[removed]` and tell the reader one was removed.

## Length

| Part | Limit | Source |
|---|---|---|
| First line | about 80 characters, 120 at most | editorial, notification preview |
| Findings | up to 5 in the open text; the rest in a collapsed block | editorial |
| Whole message | aim for under 1 200 characters | editorial, about two phone screens |
| `sendMessage` text | 4 096 characters after entity parsing | Bot API |
| Rich message | 32 768 characters, 500 blocks | Bot API, see tg-rich-messages |

Over the target: collapse details first. Split only as a last resort, at a block boundary.

## Output format

- **Short reply, no tables:** `sendMessage` with `parse_mode: HTML`. Allowed here: `<b>`, `<i>`, `<code>`, `<pre>`, `<a href>`, `<blockquote>`, `<blockquote expandable>`. Escape `&`, `<`, `>` in all dynamic text.
- **Tables or collapsed sections with headings:** `sendRichMessage`. Use `<details>` for long lists. Move the body into `html`, `markdown`, or `blocks` as described in tg-rich-messages.
- Bold the first line and the finding titles only.

## Example (invented data)

Before:

```text
[scan 03:00] host=web-1 ERR backup job nightly-db exit=1 last_ok=3d ; WARN disk /var 92% (threshold 85%) ; pending_sec_updates=1 libfoo 1.2.3->1.2.4 ; ports OK ; tls cert OK 61d ; hint: journalctl -u nightly-db -n 50
```

After (`parse_mode: HTML`):

```html
<b>Database backups on web-1 are failing. Urgent: fix today.</b>

<b>Backups are failing</b>
The job nightly-db stopped with an error (exit code 1). The last good copy is 3 days old. If the database is lost now, those 3 days are gone.
<blockquote>Find out why nightly-db fails on web-1, fix it, run it once, and show me the result.</blockquote>

<b>Disk is filling up</b>
The /var folder on web-1 is 92% full, over the 85% threshold. A full disk can stop services from saving data.
<blockquote>Show what takes the most space in /var on web-1 and propose what to delete. Delete nothing yet.</blockquote>

<b>A security update is waiting</b>
libfoo can go from 1.2.3 to 1.2.4. The fix is available but not installed.
<blockquote>Install libfoo 1.2.4 on web-1 and confirm the new version is running.</blockquote>

Fine at the 03:00 scan: open ports, TLS certificate (61 days left).
```

The `journalctl` hint is gone because the agent can run it; every fact from the scan stayed.
