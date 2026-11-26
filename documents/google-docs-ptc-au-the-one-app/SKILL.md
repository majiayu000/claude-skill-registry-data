---
name: google-docs
description: Read before reading, making or writing in the person's Google Docs.
metadata:
  title: "Google Docs"
  subtitle: "Your Google Docs"
  about: "Your AI reads your Google Docs, writes in them and makes new ones."
  category: Connectors
---

Google Docs is the person's documents. Signing in is the skill `google-account`'s.

- `read` reads a document as markdown, or text: every tab of one with tabs (Gemini's notes keep the Transcript in its own tab), each under its title, or only the `tab` asked for. `create` makes one, `append` adds text at its end, and
  `replace` replaces every match of some text: change only what the person asked.
- `write` replaces a document's whole body (or its `tab`'s) with `markdown` as real Docs formatting, keeping its id and link, and `create` takes `markdown` too: headings, lists, bold, italic, links, code, quotes. Only `read` has kept what `write` deletes.
- A document is given as `documentId`, its id or its address. `google-drive_files_list` finds one.
- With several accounts, each tool takes `account`. `google-account_accounts` lists them.
