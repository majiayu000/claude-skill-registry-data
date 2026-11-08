---
name: thread-wall
description: Collapse an iMessage thread with one person into a plain wall of text — speaker turns separated by blank lines, no names, no timestamps, no tapbacks. Use when you say "aggregate today's conversation with <person>", "give me my texts with <person> as one wall of text", "collapse/flatten that thread", "pull what we said today", or want a thread in a form you can paste into your writing. Reads the local macOS Messages database, read-only.
---

# Thread -> wall of text

For when a text conversation turned into something worth keeping. The output is **raw
material for writing**, not a transcript, which is why every piece of chat scaffolding
(names, times, tapbacks, bubble breaks) is noise and gets stripped.

## Do it

```bash
python3 scripts/wall.py <+1number> [today|YYYY-MM-DD|all] [limit]
```

Use the number in E.164 form as Messages stores it (`+15555550123`). `read_messages.py`
does the chat.db read and decodes `attributedBody` (on current macOS the `text` column is
NULL and the body lives in that blob). The terminal needs Full Disk Access to read
`~/Library/Messages/chat.db`.

Print the result in a fenced code block so it can be copied in one grab.

## Rules

1. **Re-pull chat.db right before you output.** It's live. If any time or tool call has
   passed since the read, read again, or the wall will miss messages sent meanwhile.
2. **Default to today only.** "Today's conversation" means today's date, not "the recent
   stuff." Don't bleed in yesterday because it looks continuous.
3. **Collapse consecutive same-sender messages into one paragraph**, joined by single
   spaces. Ten short bubbles are usually one thought; the breaks are typing artifacts.
4. **Blank line between speaker turns, and nothing else.** No names, no timestamps, no
   headers.
5. **Drop tapbacks** (`Loved "…"`, `Liked "…"`, `Laughed at "…"`, `Emphasized "…"`,
   `Reacted ❤️ to an image`). They requote the other person's message verbatim, so leaving
   them in prints half the thread twice.
6. **Drop bare attachments** (no caption); keep any caption text. Links stay as-is.
7. **Say what you dropped**, in one line under the block. Silent filtering of a source the
   user can't see is a trust failure.

## Variants

- A different day, or `all` for the whole history with that person.
- Only your own side (drafting from your own words) — filter `who == "ME"`.
- Speaker labels back on, if the thread is going somewhere with a third reader.

Read-only, on-device. Never send messages from here. Get the other person's OK before
publishing their words.
