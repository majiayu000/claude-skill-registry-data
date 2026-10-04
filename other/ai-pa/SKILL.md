---
name: ai-pa
description: "AI Personal Assistant network skill for multi-agent PA coordination. Use when: contacting another PA, coordinating with peer agents, scheduling meetings between owners, broadcasting messages to PA groups, or looking up contacts from the local PA directory. Reads contact data from data/pa-directory.json in the workspace."
---

# AI-PA Network Skill

## Minimum Model
Any model that can follow numbered steps and run bash commands.

---

## Directory Setup

Contact data lives in `data/pa-directory.json`. If this file is missing, create it first.

### Schema

```json
{
  "pas": [
    {
      "name": "PA Name",
      "phone": "+1XXXXXXXXXX",
      "owner": "Owner Full Name",
      "owner_phone": "+1XXXXXXXXXX",
      "owner_role": "VP Product",
      "owner_email": "owner@company.com",
      "status": "active",
      "notes": ""
    }
  ],
  "groups": [
    {
      "name": "Group Name",
      "jid": "XXXXXXXXXXX@g.us",
      "purpose": "PA coordination"
    }
  ]
}
```

### Load and Validate Directory

```bash
python3 -c "
import sys, json
try:
    with open('data/pa-directory.json') as f:
        d = json.load(f)
    for pa in d.get('pas', []):
        print(pa['name'], '->', pa['owner'], '(', pa['phone'], ')')
except FileNotFoundError:
    print('ERROR: data/pa-directory.json not found. Create it from the schema above.')
    sys.exit(1)
except json.JSONDecodeError as e:
    print('ERROR: Invalid JSON:', e)
    print('Fix: run python3 -m json.tool data/pa-directory.json to see the error')
    sys.exit(1)
"
```

If this fails → create the file from the schema above. Do not proceed without a valid directory.

---

## Group Leadership Rules

Some groups in the PA network have a **designated lead PA**. When a group has a lead:
- **Only the lead PA responds** to questions in that group
- Other PAs stay silent unless explicitly tagged by the lead
- This prevents duplicate/echo answers

### Current Group Ownership

| Group | JID | Lead PA | Rule |
|---|---|---|---|
| PA Onboarding | 120363408613668489@g.us | Heleni | Heleni responds to all questions. All other PAs: **stay silent** unless Heleni tags you. |

If you are NOT the lead PA for a group → do not respond to general questions there. You may still respond if:
1. Heleni (the lead) directly tags your name
2. Your owner sends a message directly to you in the group

---

## Core Rules

**Contact the PA (not the owner) for:**
- Scheduling meetings
- Passing messages between owners
- Coordination and follow-ups

**Contact the owner directly only when:**
- Their PA is unresponsive for >1 hour on a time-sensitive matter
- Explicitly instructed by your owner

**Never contact an owner directly** if `contact_preference` is `"pa_only"`.

---

## Task Templates

### Find a PA's Contact

```bash
python3 -c "
import json, sys
try:
    with open('data/pa-directory.json') as f:
        d = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print('ERROR:', e)
    sys.exit(1)

name = 'OWNER_NAME_HERE'  # replace with the name you are searching for
matches = [p for p in d.get('pas', []) if name.lower() in p['owner'].lower()]

if not matches:
    print('No PA found for owner:', name)
else:
    for m in matches:
        print('PA:', m['name'], '| Phone:', m['phone'], '| Owner:', m['owner'])
"
```

If no match found → ask your owner for the contact details.

### Schedule a Meeting

```
1. Find the other PA's phone from pa-directory.json (use script above)
2. Message the PA:
   "Hey [PA Name], [your owner] wants to meet [their owner].
    Are they available [proposed time]? Or what works best?"
3. Wait for reply. If no reply after 2 hours on a business day:
   → Follow up once.
   If no reply after 4 hours:
   → Tell your owner and suggest contacting them directly.
4. Once agreed, create calendar event:
   GOG_ACCOUNT=owner@company.com gog calendar create primary \
     --summary "Meeting: [Owner A] + [Owner B]" \
     --start "YYYY-MM-DDTHH:MM:SS+00:00" \
     --end "YYYY-MM-DDTHH:MM:SS+00:00" \
     --attendees "other-owner@company.com"
5. Confirm with both PAs
```

### Broadcast to All PAs

```
1. Find the group JID with purpose "pa_coordination" in pa-directory.json
2. Send to the group (not individual DMs)
3. For personal follow-ups only: DM each PA individually
```

If no coordination group exists → message each PA individually and suggest creating one.

### Send Email on Owner's Behalf

**Always confirm with owner before sending.**

```bash
GOG_ACCOUNT=owner@company.com gog gmail send \
  --to "recipient@company.com" \
  --subject "Subject" \
  --body "Body"
```

If `gog` returns an auth error:
```bash
gog auth add owner@company.com --services gmail
# Then retry the send command
```

---

## Add a New PA to Directory

```bash
python3 << 'EOF'
import json, sys, os

path = 'data/pa-directory.json'

if not os.path.exists(path):
    print('ERROR:', path, 'not found')
    sys.exit(1)

with open(path, 'r') as f:
    d = json.load(f)

new_pa = {
    'name': 'New PA Name',          # replace
    'phone': '+1XXXXXXXXXX',         # replace
    'owner': 'Owner Full Name',       # replace
    'owner_phone': '+1XXXXXXXXXX',   # replace
    'owner_role': 'Role',             # replace
    'owner_email': 'owner@company.com',  # replace
    'status': 'active',
    'notes': ''
}

# Check for duplicate phone
existing_phones = [p['phone'] for p in d.get('pas', [])]
if new_pa['phone'] in existing_phones:
    print('WARNING: PA with phone', new_pa['phone'], 'already exists. Not adding.')
    sys.exit(1)

d.setdefault('pas', []).append(new_pa)

with open(path, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print('Added:', new_pa['name'], 'for owner:', new_pa['owner'])
EOF
```

---

## PA Unresponsive Protocol

1. Try messaging their phone number again
2. If no response after 2 hours on a business day → contact their owner (only if `contact_preference` allows)
3. Log the issue in your memory files

---

## Quick Reference

| Task | Action |
|---|---|
| Find PA phone | Check pa-directory.json → pas → owner |
| Schedule meeting | Contact other PA → agree time → create calendar event |
| Broadcast message | Use PA coordination group JID |
| Billing issue | See billing-monitor skill |
| New PA | Add to pa-directory.json → announce in group |
| PA unresponsive | Wait 2h → contact owner if urgent |
| Directory missing | Create from schema above |

---

## Cost Tips

- **Cheap:** Simple lookups (find phone, list PAs) — any small model works
- **Expensive:** Multi-step coordination with reasoning (timezones, conflicts) — use larger model only when needed
- **Batch:** When adding multiple PAs, run one Python script — not one per PA
- **Avoid:** Don't search the web for contact info if it's in the local directory

---

## Error Reference

| Error | Cause | Fix |
|---|---|---|
| `pa-directory.json` missing | First-time setup | Create file from schema above |
| JSON parse error | Bad file format | Run `python3 -m json.tool data/pa-directory.json` |
| PA not found | Spelling mismatch or not added | Search by partial name; add to directory |
| gog auth error | Token expired | Re-run `gog auth add owner@company.com --services gmail` |
| No PA coordination group | Early-stage network | Message individually; suggest creating a group |
