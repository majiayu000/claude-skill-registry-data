---
name: mac-contacts
description: Search and export your Mac's Contacts straight from the local AddressBook databases, read-only. Use when asked "what's Dana's number", "who is +1 555 0100", "find everyone at Acme", "export my contacts to CSV / vCard", or when another task needs a name for a phone number or email. Merges every account (iCloud, Google, On My Mac) and normalises phones to E.164.
compatibility: macOS; reads local files only; needs Full Disk Access
---

# Mac Contacts (local, read-only)

`scripts/contacts.py`, Python 3 stdlib only.

```bash
python3 scripts/contacts.py search dana            # name, nickname, org, email, or 4+ phone digits
python3 scripts/contacts.py lookup "(555) 010-0123" # reverse: who owns this number / email
python3 scripts/contacts.py list --json             # everyone, merged across accounts
python3 scripts/contacts.py export --csv contacts.csv --vcf contacts.vcf
python3 scripts/contacts.py export --vcf acme.vcf --query acme
python3 scripts/contacts.py search lee --country 44 # numbers without +code are taken as UK
```

Output for one person:

```
Dana Whitfield  (Acme Plumbing)
   mobile   +15550100123
   work     dana@example.com
```

## Where the data is

One SQLite file per account, plus a local one:

- `~/Library/Application Support/AddressBook/Sources/<uuid>/AddressBook-v22.abcddb`
- `~/Library/Application Support/AddressBook/AddressBook-v22.abcddb` (On My Mac; often empty)

Tables: `ZABCDRECORD` (people and groups), `ZABCDPHONENUMBER.ZOWNER`, `ZABCDEMAILADDRESS.ZOWNER`,
`ZABCDPOSTALADDRESS.ZOWNER`, `ZABCDNOTE.ZCONTACT`, all pointing at `ZABCDRECORD.Z_PK`.

## Schema traps

- **Reading only the root file finds almost nobody.** Real contacts live under `Sources/`.
- **The same person appears once per account.** The script merges by name and unions phones/emails.
- **`ZABCDRECORD` mixes people, groups and account info.** Filter by the entity number whose
  `Z_PRIMARYKEY.Z_NAME = 'ABCDContact'`; the number differs between macOS versions, so look it up.
- **Labels** are stored as `_$!<Mobile>!$_`; strip the wrapper.
- **Phones are stored as typed.** `(555) 010-0123`, `555.010.0123` and `+1 555 010 0123` are one number.
  E.164 rules: a leading `+` keeps its code; `00` becomes `+`; 10 digits get `+<country>` (default 1);
  11 digits starting with 1 become `+1...`.
- vCard export is 3.0 with escaped `, ; \`.

## Permission (TCC)

The AddressBook folder needs Full Disk Access for a plain file read (System Settings > Privacy &
Security > Full Disk Access > add the app running the agent, then restart it). Without it you get
`Operation not permitted`. The Contacts permission is for apps using the Contacts framework, not
for this.

## Limits

Read-only; to add or edit a contact use Contacts.app or AppleScript. Contact photos are skipped.
