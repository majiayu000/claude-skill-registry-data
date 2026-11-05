---
name: email-draft
description: Compose a local .eml email draft (recipient, subject, body) that opens as an editable, unsent message in Outlook, Apple Mail, or Thunderbird.
---

# email-draft

Write a ready-to-review `.eml` draft to the out-box. It is marked unsent, so
double-clicking it opens an editable draft in the user's mail client — nothing is
ever sent from this computer.

## How to run

```
python3 <skill_dir>/run.py <output.eml> <to> <subject> <body>
python3 <skill_dir>/run.py <output.eml> <to> <subject> --body-file <body.txt>
```

- `<output.eml>` — a path **inside the out-box**.
- `<to>` — the recipient address.
- `<subject>` — the subject line.
- `<body>` — the message text; use `\n` for line breaks. For more than a few
  lines, save the text with `write_file` and pass it with `--body-file`.

Standard library only. After running, tell the user where the draft was saved and
that they can open it to review and send it themselves.
