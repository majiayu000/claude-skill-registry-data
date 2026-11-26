---
name: google-slides
description: Read before reading the person's Google Slides presentations.
metadata:
  title: "Google Slides"
  subtitle: "Your Google Slides"
  about: "Your AI reads your presentations: each slide's text and speaker notes."
  category: Connectors
---

Google Slides is the person's presentations. Signing in is the skill `google-account`'s.

- `read` reads a presentation as markdown: each slide's title, text (text boxes, tables) and speaker notes, in order.
- A presentation is given as `presentationId`, its id or its address. `google-drive_files_list` finds one.
- It only reads. With several accounts, each tool takes `account`. `google-account_accounts` lists them.
