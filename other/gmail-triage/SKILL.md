---
name: gmail-triage
description: Daily multi-account Gmail inbox triage — scan unread, classify by urgency, cross-reference contacts, generate actionable digest. Supports ace/personal/skestates accounts.
version: 1.0.0
author: vamsee
tags: [email, gmail, triage, digest, automation]
related_skills: [gmail-multi-account, himalaya, gmail-outreach, gmail-extract-and-act]
metadata:
  hermes:
    tags: [email, gmail, triage, digest]
    related_skills: [gmail-multi-account, himalaya]
---

# Gmail Triage

Scan all 3 Gmail accounts, classify emails, cross-reference contacts, and produce an actionable digest.

## Prerequisites

- himalaya configured with 3 accounts (see `gmail-multi-account` skill)
- Contact CSVs available in respective repos

## Core Principle: Email is a QUEUE, Not an ARCHIVE

Do NOT save all emails to repos. The workflow is:

```
INBOUND → TRIAGE → EXTRACT DATA → ACT → DELETE
                                      ↓
                          Topic completed? → DELETE email
                          Awaiting reply?  → KEEP (live)
                          New reply arrives → RE-ACTIVATE
```

Key rules:
1. Extract only structured DATA/information needed (not raw email bodies)
2. Delete the email when the topic is completed
3. Keep email alive when awaiting response from other party
4. When client/other party responds, the topic is live again
5. Learn from patterns — extraction and routing improve over time

See GitHub issue #2017 for the full workflow design.

## Triage Workflow

### Step 1: Scan all inboxes

```bash
for acct in ace personal skestates; do
  echo "=== $acct ==="
  himalaya --account $acct envelope list --page-size 50 --output json
done
```

### Step 2: Classify each email

Categories (priority order):
1. **URGENT** — from VIP/client contacts, contains "urgent", "asap", "deadline", invoice/payment
2. **ACTIONABLE** — requires response, question asked, meeting request, RFP
3. **FYI** — informational, no action needed, CC'd
4. **NEWSLETTER** — marketing, subscription content, bulk sender
5. **SPAM** — unknown sender, no contact match, suspicious

### Step 3: Cross-reference contacts

For each sender:
1. Search contact CSV for the account
2. If found: use contact category (client/vendor/recruiter/personal)
3. If NOT found: flag as "unknown sender" — recommend add-to-contacts or unsubscribe

### Step 4: Generate digest

Format:
```
=== GMAIL DAILY DIGEST — {date} ===

[ACE] owner@example.com
  URGENT (2):
    - From: client@example.com | Subject: RFP Response Deadline
    - From: vendor@example.com | Subject: Invoice #1234 Past Due
  ACTIONABLE (3):
    - ...
  FYI (5): [collapsed]
  NEWSLETTER (12): [collapsed, unsubscribe candidates marked]

[PERSONAL] owner.personal@example.com
  ...

[SKESTATES] info@example.org
  ...

=== RECOMMENDED ACTIONS ===
1. Reply to client@example.com RE: RFP (ACE)
2. Review invoice from vendor@example.com (ACE)
3. Unsubscribe from 8 newsletters (PERSONAL)
4. Add 2 unknown senders to contacts or block
```

## Communication Style Profiles

When drafting suggested responses in the digest, load the per-account style profile:

```
config/email/ace-style.yaml       — professional-technical, concise (2-5 sentences)
config/email/personal-style.yaml  — casual-terse, ultra-short (1-2 sentences)
config/email/skestates-style.yaml — business-formal-warm, medium (3-6 sentences)
```

Each profile defines greeting, closing, signature, tone, and formality rules.
Match the profile to the sending account and check `formality_rules` for context-specific adjustments.

See `config/email/README.md` for full usage guide. Reference: #1986.

## Account-Specific Classification Rules

### ace
- VIP: anyone in GTM prospect list, active clients
- URGENT: anything from @ril.com, @lng-agroup.com, @installation-contractor.com (known clients)
- EXTRACT (not noise): CRE listing senders — sandsig.com, marcusmillichap.com, loopnet.com,
  partnersrealestate.com, ten-x.ccsend.com, c.costarmail.com. These feed structured data
  extraction to assethold/data/cre-listings/ via the cre-listing template (#1991).
  Do NOT classify as NEWSLETTER or recommend unsubscribe.
- NEWSLETTER: LinkedIn notifications, industry digests (keep subscribed but low priority)
- NOISE: confirmed noise domains listed in config/email-filters/ace-noise-domains.yaml —
  safe to delete and unsubscribe (collide.io, skylineseven.ccsend.com, etc.)

### personal
- VIP: family (achanta*, @gmail.com family addresses)
- URGENT: banks, government, medical
- NEWSLETTER: aggressive unsubscribe candidates

### skestates
- VIP: tenant-rents@example.net, tenant-leases@example.net
- URGENT: insurance, tax, legal, tenant maintenance requests
- NEWSLETTER: real estate marketing (unsubscribe)

## Automation

This skill is designed to run as a cron job:

```
# Daily at 7 AM CT
0 7 * * * hermes "Load gmail-triage skill. Scan all 3 accounts and deliver digest."
```

Deliver to: Telegram or CLI local file at `~/.hermes/email-digests/`

## Gmail API Direct Usage Pattern (no dependencies)

For headless server automation, use the Gmail REST API directly with urllib (no pip deps):

```python
import json, os, urllib.request, urllib.parse, base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# OAuth config (shared file, never hardcoded)
cfg_path = os.path.expanduser("~/.gmail-mcp/oauth-env.json")
with open(cfg_path) as f:
    cfg = json.load(f)

def refresh_token(acct):
    """Refresh access token using stored refresh token"""
    cred_path = os.path.expanduser(f"~/.gmail-{acct}/credentials.json")
    with open(cred_path) as f:
        saved = json.load(f)
    data = urllib.parse.urlencode({
        "client_id": cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "refresh_token": saved["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        tokens = json.loads(resp.read().decode())
    saved.update(tokens)
    with open(cred_path, "w") as f:
        json.dump(saved, f, indent=2)
    return tokens["access_token"]

def gmail_get(endpoint, token):
    req = urllib.request.Request(
        f"https://gmail.googleapis.com/gmail/v1/{endpoint}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def gmail_post(endpoint, token, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"https://gmail.googleapis.com/gmail/v1/{endpoint}",
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

# Usage:
token = refresh_token("ace")
profile = gmail_get("users/me/profile", token)
messages = gmail_get(f"users/me/messages?maxResults=25&q=is:unread", token)
```

### Creating a Draft in an Existing Thread

To reply within an existing email chain (not create a new thread):

```python
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 1. Get the original thread's last message Message-ID
detail = gmail_get(f"users/me/threads/{thread_id}", token)
last_msg = detail["messages"][-1]
last_hdrs = {h["name"]: h["value"] for h in last_msg["payload"]["headers"]}
last_message_id = last_hdrs.get("Message-ID", "")

# 2. Build email with threading headers
msg = MIMEMultipart("alternative")
msg["To"] = "recipient@example.com"
msg["Subject"] = last_hdrs["Subject"]  # EXACT same subject
msg["In-Reply-To"] = last_message_id
msg["References"] = " ".join(all_message_ids_in_thread)  # all Message-IDs from thread
msg.attach(MIMEText(text_body, "plain"))
msg.attach(MIMEText(html_body, "html"))

# 3. Create draft WITH threadId
raw_b64 = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
gmail_post("users/me/drafts", token, {"message": {"threadId": thread_id, "raw": raw_b64}})
```

### Extracting Structured Data from Email Subjects

Common CRE/business email patterns:

```python
import re

# Cap rate: "9.75% CAP", "7.00% CAP"
cap_match = re.search(r'(\d+\.?\d*)\s*%?\s*CAP', subject, re.IGNORECASE)

# Price: "$800K", "$3.2M", "$500,000"
price_match = re.search(r'\$(\d+(?:,\d+)*(?:\.\d+)?[KMB]?)', subject)

# Building SF: "62,225 SF", "18,265 SF"
sf_match = re.search(r'([\d,]+)\s*SF', subject, re.IGNORECASE)

# Lease years: "15 Years Remaining", "10 Yr NNN"
years_match = re.search(r'(\d+)\s*(?:Years?|Yr)(?:\s+Remaining)?', subject, re.IGNORECASE)

# Vehicles per day: "72,000+ VPD"
vpd_match = re.search(r'([\d,]+)\s*VPD', subject, re.IGNORECASE)

# State: "| FL |", "- TX"
state_match = re.search(r'\|\s*([A-Z]{2})\s*\|', subject)
```

### Legal Scan Before Committing Email Data

Always scan extracted email content before committing to git repos:

```python
import yaml

# Load deny list
with open("/path/to/workspace-hub/.legal-deny-list.yaml") as f:
    deny = yaml.safe_load(f)

# Scan all extracted text
all_text = " ".join(extracted_data).lower()
for item in deny.get("client_references", []):
    pattern = item["pattern"]
    case_sensitive = item.get("case_sensitive", False)
    searchable = all_text if not case_sensitive else " ".join(extracted_data)
    if (pattern.lower() if not case_sensitive else pattern) in searchable:
        # BLOCK — do not commit, flag for review
        raise ValueError(f"Protected client reference found: {pattern}")

# If no matches, safe to commit
```

## Pitfalls

1. himalaya JSON output can be large — use `--page-size` to limit
2. Contact CSV parsing: watch for malformed entries (angle brackets in email fields)
3. Don't auto-act on emails — digest is READ-ONLY, actions need user approval
4. Rate limit Gmail IMAP — space requests 1-2 seconds apart
5. Some emails have no From header — skip gracefully
6. Do NOT archive entire email bodies to repos — extract structured data only (#2017)
7. Old skills (now in _archived/) used the archive-everything model — use the queue model via gmail-extract-and-act instead (#2019)
