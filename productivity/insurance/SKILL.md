---
name: insurance
description: Local-first insurance record organizer for tracking policies, renewals, claims logs, and related insurance records. Use when the user wants to store policy details, list recorded policies, track renewal dates, log claim events, or summarize insurance records. NEVER provides insurance advice, recommends coverage amounts, or facilitates policy purchases.
---

# Insurance

Local-first insurance record manager. Track what is already on file, keep dates organized, and log claim-related events.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All insurance records stored locally only** under `memory/insurance/`
- **No external APIs** for insurance data
- **No connection** to insurance company systems
- **No policy purchases** through this skill
- User controls all data retention and deletion

### Safety Boundaries (NON-NEGOTIABLE)
- ✅ Track recorded policy details
- ✅ Log claims and incident records
- ✅ Summarize stored premiums, renewals, and policy counts
- ✅ Highlight missing or untracked policy categories in the user's stored records
- ❌ **NEVER provide insurance advice**
- ❌ **NEVER recommend specific coverage amounts**
- ❌ **NEVER tell the user what insurance they should buy**
- ❌ **NEVER replace** a licensed insurance agent, broker, or attorney
- ❌ **NEVER facilitate policy purchases**

### Legal Disclaimer
Insurance decisions depend on individual circumstances, jurisdiction, and exact policy language. This skill is only for organizing and reviewing stored insurance records. Missing categories in stored records do not imply the user needs additional insurance. For coverage decisions or legal interpretation, consult a licensed insurance professional.

## Data Files
This skill stores local JSON files in:

- `memory/insurance/policies.json`
- `memory/insurance/claims.json`

Additional files may be added later as the skill expands.

## Core Workflows

### Add Policy Record
User: "Add my home insurance policy"
→ Use `scripts/add_policy.py`
→ Store the policy details locally

### List Recorded Policies
User: "Show my insurance policies"
→ Use `scripts/list_policies.py`
→ Show all policies already stored in local records

### Check Upcoming Renewals
User: "Any insurance renewals coming up?"
→ Use `scripts/check_renewals.py --days 60`
→ Show policies in local records renewing soon

### Generate Summary
User: "Summarize my insurance records"
→ Use `scripts/generate_summary.py`
→ Show totals by type, total annual premium, and upcoming renewals

### Log Claim Event
User: "Log a claim for my auto policy"
→ Use `scripts/log_claim.py`
→ Store claim-related event details locally

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `add_policy.py` | Add a new policy record |
| `list_policies.py` | List all stored policies |
| `check_renewals.py` | Find policies renewing soon |
| `generate_summary.py` | Summarize stored policy records |
| `log_claim.py` | Log a claim or incident record |

## Disclaimer

This skill is for local insurance record organization only. It does not provide insurance advice, recommend coverage levels, interpret legal policy obligations, or replace licensed professionals.
