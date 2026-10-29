---
name: clip
description: "macOS only. Use whenever the user asks to copy, clip, or put ANY text on their clipboard for pasting into Slack, Jira, Notes, or Docs, however short or simple the text. pbcopy is never sufficient here: it pastes literal *asterisks*, backticks, and dashes into Slack, which is the failure this skill exists to prevent. Also use when the user says a paste lost its bold or bullets, or asks for 'the shell script for this'. Usage: /clip [slack|jira] for the last finalized draft in chat, or /clip <markdown file> [slack|jira]"
---

# Rich-Text Clipboard Copy

Put a markdown draft on the macOS clipboard as rich text so the paste target renders bold, bullets, code, and links natively. macOS only: needs `osascript`, `textutil`, and NSPasteboard. `pbcopy` is the wrong tool here: it ships plain text, and Slack shows literal `*asterisks*` and backticks.

## Typical call

The user usually runs `/clip slack` or `/clip jira` with no file. That means: take the last finalized draft in the chat (the status update, the comment, the answer the user just approved), write it to a scratchpad `.md`, and clip it for that target. When it is ambiguous which chat text the user means, pick the most recent finalized draft and name it in the confirmation. If the user passes a file, use that file.

## Steps

1. Write the draft to a `.md` file in the scratchpad. GFM subset only: `**bold**`, `` `code` ``, fenced ```` ``` ```` code blocks (multi-line commands only; a one-liner stays inline in backticks), `- ` bullets (nesting by two spaces), `[text](url)`, blank line between paragraphs. No headings in Slack drafts; use a bold label line instead.
2. Pick the target and run the matching script (paths are relative to this skill's directory). They are not interchangeable.

   | Target | Command | Why |
   |---|---|---|
   | Slack | `scripts/clip-slack.sh <file>` | Slack is Electron and ignores AppleScript clipboard classes. This writes an NSAttributedString plus `public.html` and `public.rtf`. |
   | Jira, Notes, Docs | `scripts/clip.sh <file>` | AppleScript `«class HTML»` + `«class RTF »` + `«class utf8»` plain text for terminals. Jira pastes `[text](url)` as an inline link instead of a smart-link card. |

3. Confirm the script printed `clipboard: ... rich text from <file>`. Tell the user it is on the clipboard and which target it was built for. The clipboard is the deliverable; chat text is only a preview.
4. Re-run after every edit the user asks for. The clipboard does not update itself.

## Rules

- Never fall back to `pbcopy`, `echo | pbcopy`, or hand-written Slack mrkdwn (`*bold*`, `•`). That was the failure that created this skill.
- Bare Jira URLs in a Slack draft unfurl into title cards mid-sentence. Use `[PROJ-123](url)` link text inside sentences.
- The user's voice rules still apply to the content. This skill only handles delivery.

## Scripts

`scripts/md2html.py` is the shared converter (GFM subset to HTML). `clip-slack.sh` and `clip.sh` both call it, then `textutil` for RTF. No pandoc dependency.
