---
name: crm
description: Manage your CRM (e.g., Google Sheets) -- contacts, pipelines, interactions, and digest
version: 0.1.0
execution-mode: side_effecting
argument-hint: "<subcommand> [args] (add, update, log, view, stale, digest, search)"
status: tested
category: fleet-ops
providers:
  required: [python]
---
# CRM

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=crm] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

Manage contacts and pipelines in a your CRM (e.g., Google Sheets). All operations use the Sheets API via OAuth (stdlib only).

## Subcommands

```
[crm] add <name> <email> [--pipeline consulting|job|network] [--source linktree|linkedin|conference|referral|cold]
[crm] update <name-or-email> --stage <stage>
[crm] log <name-or-email> <note>
[crm] view [consulting|job|network]
[crm] stale
[crm] digest
[crm] search <query>
```

## Pipeline Stages

| Pipeline | Stages |
|----------|--------|
| Consulting | Lead > Qualified > Discovery > Proposal > Negotiating > Won > Lost |
| Job Search | Identified > Applied > Screen > Technical > Final > Offer > Rejected |
| Network | Met > Connected > Engaged > Collaborating > Advocate |

## Sheet Structure

The CRM lives in a single Google Sheet with these tabs:

| Tab | Columns |
|-----|---------|
| Contacts | Name, Email, Phone, Company, Pipeline, Stage, Source, Created, Updated |
| Interactions | Date, Name, Email, Type, Note |

The skill creates the sheet and tabs on first run if they do not exist. The sheet ID is stored in `$HOME/.opencode/skills/crm/config.json`.

## First-Run Setup

If `config.json` does not exist, the skill will:

1. Create a new Google Sheet named "your organization CRM"
2. Create the Contacts and Interactions tabs with header rows
3. Save the sheet ID to `config.json`

If the OAuth token lacks the Sheets scope, the skill prints instructions:

```
ERROR: Sheets API scope not authorized.

Fix: Re-authorize with the spreadsheets scope added.

1. Edit $HOME/.gmail-mcp/gcp-oauth.keys.json — ensure the
   Google Sheets API is enabled in the same GCP project.
2. Delete $HOME/.gmail-mcp/credentials.json
3. Re-run the OAuth flow:
   cd ~/.npm/_npx/952459504b2da320/node_modules/@gongrzhe/server-gmail-autoauth-mcp
   node dist/index.js auth
   (When prompted for scopes, include:
    https://www.googleapis.com/auth/gmail.send
    https://www.googleapis.com/auth/spreadsheets)
4. Re-run [crm]
```

## Implementation

All subcommands share the same OAuth token refresh and Sheets API helpers. Run the appropriate script via Bash. Replace `$SUBCOMMAND`, `$ARGS` etc. with parsed values from `$ARGUMENTS`.

### Core: Token Refresh and Sheets Helpers

This block is the foundation for every subcommand. Include it at the top of every script invocation.

```python
import json, urllib.request, urllib.parse, datetime, os, sys

KEYS_PATH = "$HOME/.gmail-mcp/gcp-oauth.keys.json"
CREDS_PATH = "$HOME/.gmail-mcp/credentials.json"
CONFIG_PATH = "$HOME/.opencode/skills/crm/config.json"

SHEETS_BASE = "https://sheets.googleapis.com/v4/spreadsheets"

PIPELINES = {
    "consulting": ["Lead", "Qualified", "Discovery", "Proposal", "Negotiating", "Won", "Lost"],
    "job": ["Identified", "Applied", "Screen", "Technical", "Final", "Offer", "Rejected"],
    "network": ["Met", "Connected", "Engaged", "Collaborating", "Advocate"],
}

def get_token():
    """Refresh OAuth token using stored credentials."""
    with open(KEYS_PATH) as f:
        keys = json.load(f)["installed"]
    with open(CREDS_PATH) as f:
        creds = json.load(f)
    data = urllib.parse.urlencode({
        "client_id": keys["client_id"],
        "client_secret": keys["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())["access_token"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "invalid_scope" in body or "insufficient" in body:
            print("ERROR: Sheets API scope not authorized.")
            print("Fix: Delete credentials.json and re-auth with spreadsheets scope.")
            print("See [crm] skill docs for full instructions.")
            sys.exit(1)
        raise

def sheets_get(token, sheet_id, range_):
    """GET values from a sheet range."""
    url = f"{SHEETS_BASE}/{sheet_id}/values/{urllib.parse.quote(range_)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read()).get("values", [])
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("ERROR: 403 Forbidden. Sheets scope likely missing from OAuth grant.")
            sys.exit(1)
        raise

def sheets_append(token, sheet_id, range_, values):
    """Append rows to a sheet range."""
    url = f"{SHEETS_BASE}/{sheet_id}/values/{urllib.parse.quote(range_)}:append"
    url += "?valueInputOption=USER_ENTERED&insertDataOption=INSERT_ROWS"
    payload = json.dumps({"values": values}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def sheets_update(token, sheet_id, range_, values):
    """PUT (overwrite) values in a sheet range."""
    url = f"{SHEETS_BASE}/{sheet_id}/values/{urllib.parse.quote(range_)}"
    url += "?valueInputOption=USER_ENTERED"
    payload = json.dumps({"values": values}).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }, method="PUT")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def sheets_create(token, title):
    """Create a new spreadsheet and return its ID."""
    payload = json.dumps({
        "properties": {"title": title},
        "sheets": [
            {"properties": {"title": "Contacts"}},
            {"properties": {"title": "Interactions"}},
        ]
    }).encode()
    req = urllib.request.Request(SHEETS_BASE, data=payload, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }, method="POST")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        return data["spreadsheetId"]

def get_or_create_sheet(token):
    """Load sheet ID from config, or create the CRM sheet."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)["sheet_id"]
    # First run: create the sheet
    sheet_id = sheets_create(token, "your organization CRM")
    # Add header rows
    sheets_update(token, sheet_id, "Contacts!A1:I1", [
        ["Name", "Email", "Phone", "Company", "Pipeline", "Stage", "Source", "Created", "Updated"]
    ])
    sheets_update(token, sheet_id, "Interactions!A1:E1", [
        ["Date", "Name", "Email", "Type", "Note"]
    ])
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"sheet_id": sheet_id}, f, indent=2)
    print(f"Created CRM sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
    return sheet_id

def find_contact(token, sheet_id, query):
    """Find a contact row by name or email (case-insensitive partial match). Returns (row_index, row_data) or (None, None)."""
    rows = sheets_get(token, sheet_id, "Contacts!A2:I")
    q = query.lower()
    for i, row in enumerate(rows):
        name = row[0].lower() if len(row) > 0 else ""
        email = row[1].lower() if len(row) > 1 else ""
        if q in name or q in email:
            return i + 2, row  # +2 for 1-indexed + header
    return None, None

def now_iso():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
```

### Subcommand: add

Parse `$ARGUMENTS` for: name, email, optional --pipeline (default: network), optional --source (default: cold).

```python
# After core block above:
name = "$NAME"
email = "$EMAIL"
pipeline = "$PIPELINE"  # consulting, job, or network
source = "$SOURCE"       # linktree, linkedin, conference, referral, cold

token = get_token()
sheet_id = get_or_create_sheet(token)

# Check for duplicate
_, existing = find_contact(token, sheet_id, email)
if existing:
    print(f"Contact already exists: {existing[0]} <{existing[1]}> ({existing[4]}/{existing[5]})")
    sys.exit(1)

stage = PIPELINES[pipeline][0]  # First stage
ts = now_iso()
sheets_append(token, sheet_id, "Contacts!A:I", [
    [name, email, "", "", pipeline.capitalize(), stage, source, ts, ts]
])
print(f"Added {name} <{email}> to {pipeline} pipeline at stage: {stage}")
```

Then post a bus message:
```
Type: STATUS
To: all
Message: CRM: added $NAME <$EMAIL> to $PIPELINE pipeline
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### Subcommand: update

Parse `$ARGUMENTS` for: name-or-email, --stage value.

```python
# After core block above:
query = "$QUERY"
new_stage = "$STAGE"

token = get_token()
sheet_id = get_or_create_sheet(token)

row_idx, row = find_contact(token, sheet_id, query)
if not row:
    print(f"No contact found matching: {query}")
    sys.exit(1)

pipeline = row[4].lower() if len(row) > 4 else "network"
valid = PIPELINES.get(pipeline, [])
if new_stage not in valid:
    print(f"Invalid stage '{new_stage}' for {pipeline} pipeline.")
    print(f"Valid stages: {' > '.join(valid)}")
    sys.exit(1)

old_stage = row[5] if len(row) > 5 else "unknown"
# Update stage (col F = index 5) and updated timestamp (col I = index 8)
sheets_update(token, sheet_id, f"Contacts!F{row_idx}", [[new_stage]])
sheets_update(token, sheet_id, f"Contacts!I{row_idx}", [[now_iso()]])
print(f"Updated {row[0]}: {old_stage} -> {new_stage}")
```

Post a bus message:
```
Type: STATUS
To: all
Message: CRM: moved $NAME from $OLD_STAGE to $NEW_STAGE
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### Subcommand: log

Parse `$ARGUMENTS` for: name-or-email, note text.

```python
# After core block above:
query = "$QUERY"
note = "$NOTE"

token = get_token()
sheet_id = get_or_create_sheet(token)

row_idx, row = find_contact(token, sheet_id, query)
if not row:
    print(f"No contact found matching: {query}")
    sys.exit(1)

ts = now_iso()
sheets_append(token, sheet_id, "Interactions!A:E", [
    [ts, row[0], row[1], "note", note]
])
# Update the contact's Updated timestamp
sheets_update(token, sheet_id, f"Contacts!I{row_idx}", [[ts]])
print(f"Logged interaction for {row[0]}: {note[:80]}")
```

Post a bus message:
```
Type: STATUS
To: all
Message: CRM: logged interaction with $NAME
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

### Subcommand: view

Parse `$ARGUMENTS` for optional pipeline filter. If empty, show all.

```python
# After core block above:
pipeline_filter = "$PIPELINE_FILTER"  # "" for all, or consulting/job/network

token = get_token()
sheet_id = get_or_create_sheet(token)
rows = sheets_get(token, sheet_id, "Contacts!A2:I")

if not rows:
    print("CRM is empty. Use [crm] add to add contacts.")
    sys.exit(0)

# Filter
if pipeline_filter:
    rows = [r for r in rows if len(r) > 4 and r[4].lower() == pipeline_filter.lower()]

# Group by pipeline and stage
from collections import defaultdict
by_pipeline = defaultdict(lambda: defaultdict(list))
for r in rows:
    p = r[4] if len(r) > 4 else "unknown"
    s = r[5] if len(r) > 5 else "unknown"
    by_pipeline[p][s].append(r)

for pipeline, stages in sorted(by_pipeline.items()):
    order = PIPELINES.get(pipeline.lower(), [])
    print(f"\n=== {pipeline.upper()} ({sum(len(v) for v in stages.values())} contacts) ===")
    for stage in (order if order else sorted(stages.keys())):
        contacts = stages.get(stage, [])
        if contacts:
            print(f"\n  [{stage}] ({len(contacts)})")
            for c in contacts:
                name = c[0] if len(c) > 0 else "?"
                email = c[1] if len(c) > 1 else ""
                company = c[3] if len(c) > 3 else ""
                label = f"    - {name}"
                if company:
                    label += f" ({company})"
                if email:
                    label += f" <{email}>"
                print(label)
```

### Subcommand: stale

Show contacts with no interaction in 30+ days.

```python
# After core block above:
from datetime import datetime, timedelta

token = get_token()
sheet_id = get_or_create_sheet(token)

contacts = sheets_get(token, sheet_id, "Contacts!A2:I")
if not contacts:
    print("CRM is empty.")
    sys.exit(0)

cutoff = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
stale = []
for r in contacts:
    updated = r[8] if len(r) > 8 else r[7] if len(r) > 7 else ""
    if updated and updated < cutoff:
        stale.append(r)

if not stale:
    print("No stale contacts (all touched within 30 days).")
else:
    print(f"=== STALE CONTACTS ({len(stale)}) -- no interaction in 30+ days ===\n")
    for r in stale:
        name = r[0] if len(r) > 0 else "?"
        pipeline = r[4] if len(r) > 4 else "?"
        stage = r[5] if len(r) > 5 else "?"
        updated = r[8] if len(r) > 8 else "?"
        print(f"  - {name} | {pipeline}/{stage} | last: {updated}")
```

### Subcommand: digest

Weekly pipeline health summary.

```python
# After core block above:
from collections import defaultdict
from datetime import datetime, timedelta

token = get_token()
sheet_id = get_or_create_sheet(token)

contacts = sheets_get(token, sheet_id, "Contacts!A2:I")
interactions = sheets_get(token, sheet_id, "Interactions!A2:E")

week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
cutoff_30 = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

total = len(contacts)
by_pipeline = defaultdict(int)
by_stage = defaultdict(lambda: defaultdict(int))
stale_count = 0

for r in contacts:
    p = r[4] if len(r) > 4 else "unknown"
    s = r[5] if len(r) > 5 else "unknown"
    by_pipeline[p] += 1
    by_stage[p][s] += 1
    updated = r[8] if len(r) > 8 else ""
    if updated and updated < cutoff_30:
        stale_count += 1

recent_interactions = [i for i in interactions if len(i) > 0 and i[0] >= week_ago]

print(f"=== CRM WEEKLY DIGEST ({datetime.utcnow().strftime('%Y-%m-%d')}) ===\n")
print(f"Total contacts: {total}")
print(f"Stale (30+ days): {stale_count}")
print(f"Interactions this week: {len(recent_interactions)}\n")

for pipeline_name in ["Consulting", "Job", "Network"]:
    count = by_pipeline.get(pipeline_name, 0)
    if count == 0:
        continue
    stages = by_stage.get(pipeline_name, {})
    print(f"--- {pipeline_name} ({count}) ---")
    order = PIPELINES.get(pipeline_name.lower(), [])
    for stage in order:
        n = stages.get(stage, 0)
        if n > 0:
            bar = "#" * n
            print(f"  {stage:14s} {bar} ({n})")
    print()

if recent_interactions:
    print("--- Recent Activity ---")
    for i in recent_interactions[-10:]:
        date = i[0][:10] if len(i) > 0 else "?"
        name = i[1] if len(i) > 1 else "?"
        note = i[4][:60] if len(i) > 4 else ""
        print(f"  {date} | {name} | {note}")
```

### Subcommand: search

```python
# After core block above:
query = "$QUERY".lower()

token = get_token()
sheet_id = get_or_create_sheet(token)

contacts = sheets_get(token, sheet_id, "Contacts!A2:I")
interactions = sheets_get(token, sheet_id, "Interactions!A2:E")

matches = []
for r in contacts:
    searchable = " ".join(r).lower()
    if query in searchable:
        matches.append(r)

if not matches:
    print(f"No contacts matching: {query}")
    sys.exit(0)

for r in matches:
    name = r[0] if len(r) > 0 else "?"
    email = r[1] if len(r) > 1 else ""
    company = r[3] if len(r) > 3 else ""
    pipeline = r[4] if len(r) > 4 else "?"
    stage = r[5] if len(r) > 5 else "?"
    source = r[6] if len(r) > 6 else ""
    print(f"\n  {name} <{email}>")
    if company:
        print(f"    Company: {company}")
    print(f"    Pipeline: {pipeline} / {stage}")
    if source:
        print(f"    Source: {source}")

    # Show recent interactions
    contact_interactions = [i for i in interactions if len(i) > 2 and (i[1].lower() == name.lower() or i[2].lower() == email.lower())]
    if contact_interactions:
        print(f"    Interactions ({len(contact_interactions)}):")
        for i in contact_interactions[-3:]:
            date = i[0][:10] if len(i) > 0 else "?"
            note = i[4][:60] if len(i) > 4 else ""
            print(f"      {date}: {note}")
```

## Execution Instructions

1. Parse `$ARGUMENTS` to determine subcommand and args
2. Compose the full Python script by combining the Core block with the appropriate Subcommand block
3. Replace all `$PLACEHOLDER` values with the actual parsed arguments
4. Run via `python3 << 'PYEOF' ... PYEOF`
5. After any write operation (add, update, log), post a bus message:
   ```
   Type: STATUS
   To: all
   Message: CRM: <action summary>
   ```
   (The skill invocation runtime injects the caller's canonical identity as `from_id`.)

## Error Handling

| Error | Meaning | Fix |
|-------|---------|-----|
| `invalid_grant` | Refresh token expired | Re-auth: see first-run setup |
| `403 Forbidden` | Missing Sheets scope | Add `spreadsheets` scope, re-auth |
| `404 Not Found` | Sheet ID invalid | Delete `config.json`, re-run to create |
| `No contact found` | Name/email not in CRM | Check spelling, use `[crm] search` |

## Prerequisites

- OAuth credentials at `~/.gmail-mcp/gcp-oauth.keys.json`
- Refresh token at `~/.gmail-mcp/credentials.json`
- Google Sheets API enabled in the same GCP project as Gmail
- Sheets scope (`https://www.googleapis.com/auth/spreadsheets`) in the OAuth grant

## Skill Chains

### Mandatory

None — CRM data management via external API; all operations are reversible (add/update/log can be undone).

### Advisory

- `[follow-up]` — check stale contacts after CRM updates to trigger follow-up drafts
- `[crm] digest` — weekly pipeline health summary after batch updates

## Authority

- **T1 (TRUSTED)**: May run all subcommands (add, update, log, view, stale, digest, search)
- **T2 (Active/High)**: May run all subcommands (add, update, log, view, stale, digest, search)
- **T3 (Medium)**: May run all subcommands; operator notification required for bulk operations (e.g., batch add/update of 10+ contacts)
- **T4 (Probationary)**: Read-only subcommands only (view, stale, digest, search); modify operations (add, update, log) BLOCKED
- **Operator**: Override any restriction
