---
name: vcard
description: Create a .vcf contact card (name, email, phone, organization, title) that imports into any address book.
---

# vcard

Write a standard vCard (`.vcf`) the user can import into their contacts.

## How to run

```
python3 <skill_dir>/run.py <output.vcf> <full_name> [email] [phone] [org] [title]
```

- `<output.vcf>` — a path **inside the out-box**.
- `<full_name>` — e.g. `"Jane Doe"`.
- `[email]`, `[phone]`, `[org]`, `[title]` — optional.

Standard library only. After running, tell the user the saved path.
