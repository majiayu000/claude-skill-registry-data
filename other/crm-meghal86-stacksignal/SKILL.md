---
name: crm
description: Personal CRM for managing contacts, relationships, and follow-ups using markdown files. Use when the user wants to add contacts, track relationships, set follow-up reminders, query contacts by tag/company/location, import/export contacts, or manage networking leads. Supports natural language input for adding contacts.
---

# Personal CRM Skill

Manage contacts, relationships, and follow-ups with markdown files. No database needed.

## Setup

Initialize contacts inside memory/ for semantic search integration:
```bash
mkdir -p memory/contacts/{people,companies,events,_templates,scripts}
cp skills/crm/assets/templates/*.md memory/contacts/_templates/
cp skills/crm/scripts/*.py memory/contacts/scripts/
clawdbot memory index
```

## Natural Language Input

When user describes a contact naturally, extract and create:

**User says:** "Met Sarah Lee at Web3 summit. She's head of partnerships at Polygon, based in Dubai. Telegram @sarahlee"

**Extract:**
```yaml
name: Sarah Lee
company: Polygon
role: Head of Partnerships
location: Dubai
telegram: "@sarahlee"
met_at: web3-summit
tags: [web3, partnership]
```

**Then run:** `memory/contacts/memory/contacts/scripts/crm-add.py person "Sarah Lee" --company "Polygon" --role "Head of Partnerships" --location "Dubai" --telegram "@sarahlee" --tags "web3,partnership"`

## Scripts

All scripts use `/usr/bin/python3` and require PyYAML.

### Query Contacts
```bash
memory/contacts/scripts/crm-query.py --list people          # List all people
memory/contacts/scripts/crm-query.py --tag investor         # Filter by tag
memory/contacts/scripts/crm-query.py --company "Acme"       # Filter by company
memory/contacts/scripts/crm-query.py --introduced-by bob    # Find introductions
memory/contacts/scripts/crm-query.py --location singapore   # Filter by location
memory/contacts/scripts/crm-query.py --search "supply chain" # Full-text search
memory/contacts/scripts/crm-query.py -v                     # Verbose output
```

### Add Contact
```bash
memory/contacts/scripts/crm-add.py person "Name" --company "Co" --role "Title" --tags "a,b"
memory/contacts/scripts/crm-add.py company "Company Name" --industry "Tech"
memory/contacts/scripts/crm-add.py event "Event Name" --date 2026-03-15 --location "City"
```

### Update Contact
```bash
memory/contacts/scripts/crm-update.py alice-chen --interaction "Called about demo"
memory/contacts/scripts/crm-update.py alice-chen --set-follow-up 2026-02-15
memory/contacts/scripts/crm-update.py alice-chen --add-tag vip
memory/contacts/scripts/crm-update.py alice-chen --touch  # Update last_contact to today
```

### Follow-ups & Reminders
```bash
memory/contacts/scripts/crm-followups.py --summary         # Quick summary
memory/contacts/scripts/crm-followups.py --days 7          # Due in 7 days
memory/contacts/scripts/crm-followups.py --dormant 90      # Not contacted in 90 days
memory/contacts/scripts/crm-remind.py contact --in 3d      # Remind in 3 days
memory/contacts/scripts/crm-remind.py --list               # List reminders
memory/contacts/scripts/crm-remind.py --check              # Check due reminders
```

### Import/Export
```bash
memory/contacts/scripts/crm-import.py contacts.csv                    # Import CSV
memory/contacts/scripts/crm-import.py contacts.vcf                    # Import vCard
memory/contacts/scripts/crm-import.py linkedin.csv --format linkedin  # LinkedIn export
memory/contacts/scripts/crm-export.py --csv out.csv                   # Export CSV
memory/contacts/scripts/crm-export.py --vcard out.vcf --type people   # Export vCard
```

### Regenerate Index
```bash
memory/contacts/scripts/crm-index.py  # Rebuilds contacts/_index.md
```

## Contact Schema

```yaml
---
name: Alice Chen
type: person  # person | company | event
tags: [investor, crypto]
company: Acme Corp
role: Partner
email: alice@acme.com
phone: +1-555-0123
telegram: "@alice"
twitter: "@alice"
linkedin: https://linkedin.com/in/alice
location: Singapore
introduced_by: bob-smith  # slug of introducer
met_at: token2049-2025    # slug of event
first_contact: 2025-09-20
last_contact: 2026-01-27
follow_up: 2026-02-15
status: active  # active | dormant | archived
---

# Alice Chen

## Context
Partner at Acme Corp. Met through Bob at Token2049.

## Interactions
- **2026-01-27**: Called about pilot program.
- **2025-09-20**: First met at conference.

## Notes
- Prefers Signal over email
```

## Folder Structure

```
memory/
└── contacts/             # Inside memory/ for semantic search
    ├── people/           # One file per person
    ├── companies/        # One file per company
    ├── events/           # One file per event
    ├── _templates/       # Templates for new contacts
    ├── _index.md         # Auto-generated lookup table
    ├── .reminders.json   # Reminder data
    └── scripts/          # CLI tools
```

## Cross-References

- **YAML fields:** `introduced_by: bob-smith`, `met_at: event-slug`
- **Wiki-links in notes:** `[[bob-smith]]`, `[[acme-corp]]`
- **Semantic search:** Memory search finds connections in prose

## Heartbeat Integration

Add to HEARTBEAT.md:
```markdown
### CRM Follow-ups (check 1-2x daily)
1. Run: `/usr/bin/python3 contacts/memory/contacts/scripts/crm-followups.py --summary`
2. Run: `/usr/bin/python3 contacts/memory/contacts/scripts/crm-remind.py --check`
If there are due items, notify the user.
```

## Tips

- Use `--dry-run` on import to preview before creating files
- Run `crm-index.py` after bulk changes to update the index
- Tags are lowercase, comma-separated
- Slugs are auto-generated from names (lowercase, hyphenated)
- For natural language input, extract fields and use crm-add.py
