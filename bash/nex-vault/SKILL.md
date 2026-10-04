---
name: nex-vault
description: "Secure local contract and document vault for managing business agreements with automatic expiration tracking, renewal deadline alerts, and compliance monitoring. Use when the user says \"track my contracts\", \"when does this lease expire\", \"add a new contract\", \"show me upcoming renewals\", \"what's my total subscription cost\", or when managing business agreements, leases, insurance policies, and SLAs with deadline awareness."
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🔐"
    requires:
      bins:
        - python3
      env:
        - VAULT_TELEGRAM_TOKEN
        - VAULT_TELEGRAM_CHAT_ID
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-vault.py"
      - "lib/*"
      - "setup.sh"
scope: instance
invocation: workflow
---

<!-- provenance: ABSORBED FROM: /Users/marcelspatz/YURI-OS-MUSUBI/RESEARCH/ORACLE-CORPUS/openclaw-skills/skills/nexaiguy/nex-vault | scanned: 2026-05-17 | score: 20 -->

# Nex Vault

Local Contract and Document Vault with Expiry Alerts. Track all your important documents—contracts, leases, insurance policies, SLAs, warranties, licenses, subscriptions, certificates, and permits. Never miss an expiration date, renewal deadline, or termination notice period again.

## When to Use

Use this skill when the user asks about:

- Uploading, adding, or tracking contracts, leases, or business documents
- Tracking insurance policies, warranties, or maintenance agreements
- Monitoring expiration dates, renewal deadlines, or termination notice periods
- Getting alerts when documents are about to expire
- Finding clauses related to termination, renewal, auto-renewal, or payment terms
- Searching for specific contracts, parties, or document types
- Viewing upcoming document deadlines or expiring agreements
- Extracting key dates and clauses from documents
- Exporting a list of documents for compliance or budgeting
- Setting up automatic notifications via Telegram
- Checking monthly or yearly costs for all subscriptions and contracts
- Documenting termination notice requirements
- Understanding auto-renewal clauses and renewal periods

Trigger phrases in Dutch and English: "contract", "huurovereenkomst", "lease", "verzekering", "insurance", "SLA", "warranty", "garantie", "licentie", "license", "abonnement", "subscription", "vervaldag", "expiry", "opzeg", "termination", "verlenging", "renewal", "clausules", "clauses", "deadlines", "vervaldagen", "documentvault", "document vault", "expires", "verloopt", "notification alerts"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs dependencies, initializes the database, and optionally configures Telegram notifications.

## Available Commands

The CLI tool is `nex-vault`. All commands output plain text.

### Adding Documents

Add a contract or document to the vault:

```bash
# Add a contract with full metadata
nex-vault add /path/to/contract.pdf --type contract --party "Verhuurder NV" --end-date 2027-01-01 --notice-days 90 --auto-renewal --monthly-cost 850

# Add with minimal info, auto-parse dates from PDF
nex-vault add /path/to/sla.pdf --type sla --party "CloudProvider"

# Add without a file (just metadata)
nex-vault add "Ethias Brandverzekering" --type insurance --end-date 2026-12-31 --yearly-cost 450

# Add with all optional fields
nex-vault add /path/to/lease.docx --type lease --party "Makelaars Antwerpen" --start-date 2024-01-01 --end-date 2027-01-01 --notice-days 120 --auto-renewal --renewal-period "1 year" --monthly-cost 1200 --tags "property,residential" --notes "Ground floor, fully renovated"
```

### Viewing Documents

Show full details of a document including key clauses and upcoming alerts:

```bash
nex-vault show <id>
nex-vault show 5
```

### Listing Documents

List documents with filters:

```bash
# List all documents
nex-vault list

# List by type
nex-vault list --type contract
nex-vault list --type insurance
nex-vault list --type lease

# List by status
nex-vault list --status active
nex-vault list --status expired
nex-vault list --status pending

# List by party name
nex-vault list --party "Verhuurder"

# List expiring soon (default 90 days)
nex-vault list --expiring

# List expiring within custom timeframe
nex-vault list --expiring 30
```

### Searching

Full-text search across document names, parties, notes, and extracted content:

```bash
nex-vault search "liability insurance"
nex-vault search "payment terms"
nex-vault search "CloudProvider"
```

### Viewing Expiring Documents

Show documents expiring within N days:

```bash
nex-vault expiring
nex-vault expiring 30
nex-vault expiring 7
```

### Managing Alerts

View and manage expiry alerts:

```bash
# Show upcoming alerts (next 90 days by default)
nex-vault alerts list
nex-vault alerts list --days 30

# Run daily alert check manually
nex-vault alerts check

# Send Telegram notifications
nex-vault alerts notify

# Mark an alert as sent
nex-vault alerts mark-sent <alert_id>
```

### Parsing Documents

Extract and re-parse dates and clauses from a document:

```bash
# Auto-extract dates, clauses, and renewal info from file
nex-vault scan /path/to/document.pdf

# Scan and update an existing document entry
nex-vault scan <id> /path/to/new_version.pdf
```

### Editing Documents

Update document metadata:

```bash
nex-vault edit <id> --end-date 2027-06-01
nex-vault edit <id> --party "New Party Name"
nex-vault edit <id> --monthly-cost 900
nex-vault edit <id> --notice-days 60
nex-vault edit <id> --auto-renewal true
nex-vault edit <id> --notes "Updated contract terms"
```

### Removing Documents

Remove a document from tracking (keeps the file):

```bash
nex-vault remove <id>
```

### Statistics

View vault statistics:

```bash
nex-vault stats
```

Shows:
- Total documents and count by type
- Documents by status (active, expired, pending)
- Total monthly costs and yearly costs
- Most common parties

### Exporting

Export document list for external use:

```bash
# Export as CSV
nex-vault export csv --output contracts.csv

# Export as JSON
nex-vault export json --output vault_backup.json
```

### Configuration

Manage Telegram notification settings:

```bash
# Show current configuration
nex-vault config show

# Set Telegram bot token
nex-vault config set-telegram-token YOUR_BOT_TOKEN

# Set Telegram chat ID
nex-vault config set-telegram-chat YOUR_CHAT_ID

# Test Telegram connection
nex-vault config test-telegram
```

## Example Interactions

**User (Dutch):** "Ik heb een nieuwe huurovereenkomst. Upload het en zeg me wanneer ik moet opzeggen."
**Agent runs:** `nex-vault add /path/to/lease.pdf --type lease --party "Makelaar"`
**Agent:** Extracts dates from the PDF, determines termination notice deadline, and confirms the document is tracked.

**User (English):** "Show me all my contracts expiring in the next 30 days."
**Agent runs:** `nex-vault expiring 30`
**Agent:** Lists contracts with their expiration dates and termination notice deadlines.

**User (Dutch):** "Welke verzekeringen moet ik verlengen?"
**Agent runs:** `nex-vault list --type insurance --expiring 90`
**Agent:** Shows insurance policies expiring within 90 days and their renewal deadlines.

**User (English):** "Find all documents with auto-renewal clauses."
**Agent runs:** `nex-vault search "auto-renewal"` then `nex-vault list` filtered manually
**Agent:** Shows documents with auto-renewal and explains the renewal periods.

**User (Dutch):** "Wat zijn mijn totale maandelijkse kosten?"
**Agent runs:** `nex-vault stats`
**Agent:** Shows the sum of all monthly costs.

**User (English):** "Set up Telegram alerts for contracts expiring soon."
**Agent runs:** `nex-vault config set-telegram-token` and `nex-vault config set-telegram-chat`
**Agent:** Configures notifications and confirms the connection.

**User (Dutch):** "Toon me alle details van contract #3"
**Agent runs:** `nex-vault show 3`
**Agent:** Displays full contract details including key clauses and upcoming alerts.

**User (English):** "Export all my documents to CSV for my accountant."
**Agent runs:** `nex-vault export csv --output vault.csv`
**Agent:** Exports and confirms the file location.

**User (Dutch):** "Update het einddatum van contract #2 naar volgende maand"
**Agent runs:** `nex-vault edit 2 --end-date 2026-05-05`
**Agent:** Confirms the update and recalculates alert deadlines.

**User (English):** "Run the daily alert check and send me any expiring documents."
**Agent runs:** `nex-vault alerts check` then `nex-vault alerts notify`
**Agent:** Checks for upcoming expirations and sends Telegram notifications if configured.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Section headers followed by `---` separators
- List items prefixed with `- `
- Dates in ISO-8601 format (YYYY-MM-DD)
- Document statuses: `active`, `expired`, `pending`, `terminated`
- Monetary values in euros with 2 decimal places (€ symbol)
- Every command output ends with `[Nex Vault by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally. Do not show raw database paths or internal details.

## Important Notes

- All documents and metadata are stored locally at `~/.nex-vault/`. No data is sent to external servers.
- Telegram notifications are optional. If no Telegram credentials are configured, the `alerts notify` command will skip sending.
- The skill supports multiple file formats: PDF, DOCX, TXT, and scanned documents (JPG/PNG with OCR).
- Date extraction is optimized for Belgian and EU contract formats (DD/MM/YYYY, DD-MM-YYYY, etc.).
- Key clauses are automatically extracted during parsing, including termination, renewal, payment, liability, and confidentiality clauses.
- File hashes are stored to detect when a document has been replaced or updated.
- For recurring alerts, set up a cron job or systemd timer to run `nex-vault alerts check` daily.
- Auto-renewal detection uses both Dutch and English keywords ("automatische verlenging", "auto-renewal", etc.).

## Recommended Cron Setup

To enable daily automatic alert checks, add to your crontab:

```bash
# Run alert check every morning at 08:00
0 8 * * * /home/user/.local/bin/nex-vault alerts check
```

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
License: MIT-0

## Session Notes

### 2026-06-16
- session: 178m | peak ctx: 0% | compacts: 0
- tools: Bash×205, Read×121, WebFetch×114, Edit×87, WebSearch×72, Write×33, TodoWrite×13, Agent×10, ToolSearch×9, Skill×4, AskUserQuestion×1, mcp×1, TaskStop×1
- corrections: go over it again, full red team and grounding in more fresh online research together with local, then check the compatibility across other organs, run phase 1. all agentic nano swarm | 'The legal one is the wall: an Austria-resident running automated Polymarket ' rick we are not doing full automated trading on polymarket, also polymarket is allowed in austria, you mustve fact checke | go over it again, full red team and grounding in more fresh online research together with local, then check the compatibility across other organs, run phase 1. all agentic nano swarm
- errors: none
