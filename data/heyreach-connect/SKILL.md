---
name: heyreach-connect
description: "Connect to HeyReach for LinkedIn automation. Load when user mentions 'heyreach', 'linkedin outreach', 'linkedin campaigns', 'heyreach campaigns', 'add leads', 'campaign stats'. Meta-skill that validates config and routes to operations."
---

# HeyReach Connect

Meta-skill for HeyReach LinkedIn automation integration.

## Trigger Phrases

- "heyreach" / "heyreach campaigns"
- "linkedin outreach" / "linkedin automation"
- "list campaigns" / "show campaigns"
- "campaign stats" / "campaign metrics"
- "add leads to campaign"
- "campaign leads"
- "linkedin accounts"

---

## Pre-Flight Check (ALWAYS RUN FIRST)

```bash
python 00-system/skills/heyreach/heyreach-master/scripts/check_heyreach_config.py --json
```

| `ai_action` | What to Do |
|-------------|------------|
| `proceed_with_operation` | Config OK → Continue |
| `prompt_for_api_key` | Ask user for API key, save to .env |

### Setup Guide

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HEYREACH API SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Log into HeyReach at https://app.heyreach.io
2. Go to Settings → API
3. Copy your API key

Paste your HeyReach API key:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Routing Table

All scripts located in: `00-system/skills/heyreach/heyreach-master/scripts/`

| User Says | Script | Args |
|-----------|--------|------|
| "list campaigns" | list_campaigns.py | `[--limit N] [--json]` |
| "campaign details [X]" | get_campaign.py | `--campaign-id ID [--json]` |
| "pause/resume [campaign]" | toggle_campaign.py | `--campaign-id ID --status ACTIVE\|PAUSED` |
| "add leads to [campaign]" | add_leads.py | `--campaign-id ID --linkedin-urls URLs` |
| "leads in [campaign]" | get_leads.py | `--campaign-id ID [--limit N]` |
| "conversations" | get_conversations.py | `[--campaign-id ID] [--limit N]` |
| "linkedin accounts" | list_accounts.py | `[--json]` |
| "lead lists" | list_lists.py | `[--limit N]` |
| "create list [name]" | create_list.py | `--name NAME` |
| "analytics/stats" | get_stats.py | `[--json]` |
| "metrics for [campaign]" | get_metrics.py | `--campaign-id ID` |

---

## Example Workflows

### List Campaigns
```bash
python 00-system/skills/heyreach/heyreach-master/scripts/list_campaigns.py --json
```

### Add Leads
```bash
python 00-system/skills/heyreach/heyreach-master/scripts/add_leads.py \
  --campaign-id camp-123 \
  --linkedin-urls "linkedin.com/in/user1,linkedin.com/in/user2"
```

### Get Stats
```bash
python 00-system/skills/heyreach/heyreach-master/scripts/get_stats.py --json
```

---

## Error Handling

| Error | Solution |
|-------|----------|
| 401 | Invalid API key - re-run setup |
| 403 | API not available for subscription |
| 404 | Campaign/lead not found |
| 429 | Rate limited (auto-retry) |

---

**Version**: 1.0
