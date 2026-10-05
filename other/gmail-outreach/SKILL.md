---
name: gmail-outreach
description: Outbound email actions — periodic relationship touchbase messages and batch unsubscribe from newsletters/marketing. Combines gmail-touchbase + gmail-unsubscribe into one skill.
version: 1.0.0
author: vamsee
tags: [email, gmail, outreach, touchbase, unsubscribe, automation]
related_skills: [gmail-multi-account, contact-manager, gmail-triage]
metadata:
  hermes:
    tags: [email, gmail, outreach]
    related_skills: [gmail-multi-account, contact-manager]
---

# Gmail Outreach — Touchbase + Unsubscribe

Outbound email management: maintain relationships and remove noise. Combines two functions into one skill.

## Prerequisites

- OAuth tokens in `~/.gmail-{account}/credentials.json`
- Client credentials in `~/.gmail-mcp/oauth-env.json`
- Contact CSVs normalized (see `contact-manager` skill)
- `gmail-multi-account` skill configured

## Part 1: Touchbase — Relationship Maintenance

Identify contacts due for periodic outreach and draft check-in messages.

### Contact Cadence Rules

| Contact Category | Cadence | Trigger |
|---|---|---|
| Active clients | 30 days | Last email exchange > 30 days ago |
| GTM prospects | 21 days | No engagement in 21 days |
| Important vendors | 90 days | No interaction in 90 days |
| Alumni network | 180 days | No contact in 6 months |
| Recruiters | 90 days | No response in 90 days |
| Family/personal | 30 days | No contact in 30 days |

### Touchbase Workflow

1. Load contact CSV for the account
2. Check last interaction date (search Gmail for sent-to + received-from)
3. Filter contacts past their cadence threshold
4. Sort by priority: clients > prospects > vendors > network
5. Draft personalized check-in messages using communication style profiles (#1986)

### Draft Templates

**Client check-in:**
```
{FirstName},

Hope all is well on your end. It's been a few weeks since we last connected — just wanted to check in and see if there's anything I can help with on the [project] front.

Let me know if you'd like to catch up briefly.

Thank you,
Vamsee
```

**Touchbase with GTM prospect:**
```
{FirstName},

I wanted to follow up on our earlier conversation about [topic]. I've been working on [recent project/capability] and thought it might be relevant to what you're doing at [Company].

Would love to catch up when you have a moment.

Thank you,
Vamsee Achanta, P.E.
```

**Network check-in:**
```
Hey {FirstName},

Long time no talk. Hope [work/family/life] has been treating you well.

Let's catch up when you get a chance.

Vamsee
```

### Per-Account Style Profiles

Load the full style profile for the sending account before drafting any message:

```
config/email/ace-style.yaml       — professional-technical, concise (2-5 sentences)
config/email/personal-style.yaml  — casual-terse, ultra-short (1-2 sentences)
config/email/skestates-style.yaml — business-formal-warm, medium (3-6 sentences)
```

Each profile defines greeting, closing, signature, tone, formality rules, and
calibration examples. Check `formality_rules` to adjust for context (new client
vs ongoing thread, vendor follow-up vs family matters). See `config/email/README.md`
for the full usage guide. Reference: #1986.

Quick reference (see YAML files for complete rules):

| Account | Tone | Greeting | Closing | Signature |
|---|---|---|---|---|
| ace | Professional-technical | "{FirstName}," | "Thank you," | "Vamsee Achanta, P.E." (formal) / "Vamsee" (casual) |
| personal | Casual/abbreviated | "{FirstName}," or none | "Vamsee" or none | "Vamsee" |
| skestates | Business-formal-warm | "{FirstName}," | "Thank you very much," | "Vamsee" (on behalf of "the owners" / "SKEstates Inc") |

### Execution

```python
import json, urllib.request, urllib.parse, os
from datetime import datetime, timedelta

def search_gmail_for_contact(email, account, token):
    """Check for last interaction with an email address"""
    query = urllib.parse.quote(f"from:{email} OR to:{email}")
    result = gmail_get(f"users/me/messages?q={query}&maxResults=1", token)
    if result.get("messages"):
        msg = gmail_get(f"users/me/messages/{result['messages'][0]['id']}?format=metadata", token)
        hdrs = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        return hdrs.get("Date", "")
    return None

def get_touchbase_candidates(account, contacts_csv, cadence_days=30):
    """Get contacts due for touchbase"""
    import csv
    cutoff = datetime.now() - timedelta(days=cadence_days)
    token = refresh_token(account)
    candidates = []

    with open(contacts_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("email", "")
            category = row.get("category", "")
            last_contact = search_gmail_for_contact(email, account, token)
            if last_contact:
                contact_date = datetime.strptime(last_contact[:24], "%a, %d %b %Y %H:%M:%S")
                if contact_date < cutoff:
                    candidates.append({
                        "email": email,
                        "name": row.get("name", ""),
                        "category": category,
                        "last_contact": last_contact,
                    })
    return candidates
```

## Part 2: Unsubscribe — Batch Noise Removal

Identify emails with List-Unsubscribe headers and batch process unsubscribes.

### Unsubscribe Detection

```python
def find_unsubscribe_candidates(account, max_results=200):
    """Scan inbox for emails with List-Unsubscribe headers"""
    token = refresh_token(account)
    search = gmail_get(f"users/me/messages?maxResults={max_results}", token)

    candidates = []
    for msg_stab in search.get("messages", []):
        detail = gmail_get(
            f"users/me/messages/{msg_stab['id']}?format=metadata&metadataHeaders=List-Unsubscribe&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date&metadataHeaders=List-Unsubscribe-Post",
            token
        )
        hdrs = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
        
        if hdrs.get("List-Unsubscribe"):
            method = "http" if hdrs["List-Unsubscribe"].startswith("http") else "mailto"
            one_click = bool(hdrs.get("List-Unsubscribe-Post", ""))
            candidates.append({
                "msg_id": msg_stab["id"],
                "from": hdrs.get("From", ""),
                "subject": hdrs.get("Subject", ""),
                "date": hdrs.get("Date", ""),
                "unsubscribe_url": hdrs.get("List-Unsubscribe", ""),
                "method": method,
                "one_click": one_click,
            })
    return candidates
```

### Unsubscribe Execution

HTTP/one-click unsubscribe (POST to the URL):
```python
def execute_unsubscribe(url, method="http"):
    """Execute unsubscribe via HTTP POST or mailto"""
    if method == "http" and url.startswith("http"):
        req = urllib.request.Request(url, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"status": resp.status, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}
    elif method == "mailto":
        # Send empty email to unsubscribe address
        mailto_addr = url.replace("<mailto:", "").replace(">", "").split(",")[0]
        return {"method": "mailto", "address": mailto_addr}
    return {"error": "unsupported method", "success": False}
```

### Unsubscribe + Delete Pipeline

```python
def unsubscribe_and_delete(account, domains_to_remove, max_per_domain=500, dry_run=False):
    """Unsubscribe from domains and delete matching emails"""
    token = refresh_token(account)
    stats = {"unsubscribed": 0, "deleted": 0, "skipped": 0}

    for domain in domains_to_remove:
        query = f"from:{domain} has:List-Unsubscribe"
        search = gmail_get(f"users/me/messages?q={urllib.parse.quote(query)}&maxResults={max_per_domain}", token)
        
        for msg_stab in search.get("messages", []):
            detail = gmail_get(f"users/me/messages/{msg_stab['id']}?format=metadata", token)
            hdrs = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
            unsub_url = hdrs.get("List-Unsubscribe", "")
            
            if unsub_url:
                method = "http" if unsub_url.startswith("http") else "mailto"
                if not dry_run:
                    execute_unsubscribe(unsub_url, method)
                    gmail_post(f"users/me/messages/{msg_stab['id']}/trash", token, {})
                stats["unsubscribed"] += 1
                stats["deleted"] += 1
            else:
                stats["skipped"] += 1

    return stats
```

## Safety Rules

1. ALWAYS show unsubscribe candidates to user before executing
2. First run: execute in dry_run mode and show what would happen
3. Never unsubscribe domains marked as REVIEW in email-routing.yaml
4. Touchbase drafts: ALWAYS require user approval before sending
5. Batch unsubscribe: max 20 domains per batch to avoid Gmail rate limits
6. Log all unsubscribe actions — track what was unsubscribed and when
7. Unsubscribe list is maintained in `~/.hermes/unsubscribe-log.yaml`

## Usage Examples

### Find touchbase candidates for ace account
```bash
cd /mnt/local-analysis/workspace-hub
# Load contact CSV, check last interaction dates, produce candidate list
```

### Find unsubscribe candidates
```python
candidates = find_unsubscribe_candidates("personal", max_results=200)
# Display: sender, subject, unsubscribe method (HTTP/mailto), one-click support
```

### Execute batch unsubscribe (after user approval)
```python
domains = ["promote.weebly.com", "e.swimoutlet.com", "lists.wikimedia.org"]
stats = unsubscribe_and_delete("personal", domains, dry_run=False)
# Returns: {"unsubscribed": N, "deleted": N, "skipped": N}
```

## Unsubscribe Watchlist (from email-routing.yaml)

```
CONFIRMED DELETE (safe to unsubscribe + delete):
  collide.io, skylineseven.ccsend.com, promote.weebly.com
  e.swimoutlet.com, email.myflighthub.com, mail.urbanairparks.com
  e.stantonoptical.com, lists.wikimedia.org, jongordon.com
  atticbuddies.com, email.theparkingspot.com, marketing.goindigo.in
  deeplearning.ai, gamemail.com, suzeorman.com

REVIEW FIRST (do not auto-unsubscribe):
  substack.com, info.marineinsight.com, indianstarllc.ccsend.com
  rigzonemail.com, m.learn.coursera.org, irctc.co.in
  info.dpam.com, blueskysfund.com, cincsystems.net
```

## Deprecation Notice

This skill replaces:
- `gmail-touchbase` — functionality merged into this skill
- `gmail-unsubscribe` — functionality merged into this skill

## Pitfalls

1. one-click unsubscribe (List-Unsubscribe-Post header) requires POST to the URL with `List-Unsubscribe` header set to "1"
2. Some unsubscribe URLs are POST-only and require specific headers — test before batch
3. Touchbase cadence: use Gmail search for last interaction, not local timestamps (more reliable)
4. Don't touchbase with contacts who explicitly opted out — check "do_not_contact" column in contact CSV
5. Gmail API rate limits — batch requests with 0.15s delays between calls
6. Touchbase emails should feel personal — avoid obvious template language
7. Always cross-reference against email-routing.yaml REVIEW list before auto-unsubscribing
