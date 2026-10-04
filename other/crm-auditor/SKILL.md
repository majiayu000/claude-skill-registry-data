---
name: crm-auditor
description: Data quality audit on CRM with completeness scoring and specific fix recommendations
tags: [crm, data-quality, audit, hygiene, operations]
---

# CRM Auditor

Performs a comprehensive data quality audit on CRM data. Checks for missing fields, duplicate entries, stale leads, invalid emails, inconsistent formatting, and leads stuck in the same stage too long. Calculates a completeness score per record and overall, then outputs an audit report with specific records to fix. Works with any CRM accessible via `crm-writer`.

## Prerequisites

- `agency.config.json` in the project root
- CRM data accessible via `crm-writer` or provided as CSV/JSON
- Optional: email validation tool (`email-validator` skill or ZeroBounce API)

## Phase 0: Read Config

1. Read `agency.config.json` from the project root.
2. Extract CRM configuration:
   - `crm.tabs[]` -- CRM tab names and their purpose
   - `crm.required_fields` -- fields that must be populated per record
   - `crm.stages[]` -- valid pipeline stages
   - `crm.stale_threshold_days` -- days before a lead is considered stale (default: 30)
3. Extract `tools.crm` for data access method (Google Sheets webhook, API, etc.).
4. Extract `tools.email_validation` for email checking capability.
5. Define required fields if not in config:
   ```
   Default required fields:
   - company_name
   - contact_name
   - email
   - stage
   - last_updated
   - source
   ```

## Phase 1: Pull CRM Data

Read all CRM data via `crm-writer` or from provided export:

**Tabs to audit:**
- Researched Leads
- Outreach CRM
- Inbound Leads
- Any other tabs defined in `crm.tabs[]`

For each tab, load all rows and parse into structured records. Note:
- Total record count per tab
- Column headers present
- Date of earliest and most recent record

## Phase 2: Missing Field Analysis

For each record, check required fields:

```
MISSING FIELD ANALYSIS
===
Tab: Outreach CRM (150 records)

Field            | Present | Missing | % Complete
-----------------|---------|---------|----------
company_name     | 148     | 2       | 98.7%
contact_name     | 145     | 5       | 96.7%
email            | 140     | 10      | 93.3%
phone            | 85      | 65      | 56.7%
stage            | 150     | 0       | 100.0%
last_updated     | 130     | 20      | 86.7%
source           | 120     | 30      | 80.0%
deal_value       | 95      | 55      | 63.3%
next_action      | 75      | 75      | 50.0%

OVERALL COMPLETENESS: 80.6%
```

Flag records with 3+ missing required fields as "critically incomplete."

## Phase 3: Duplicate Detection

Check for duplicates across multiple dimensions:

**Email duplicates:**
- Exact match on email field
- Group duplicate sets together

**Company name duplicates:**
- Exact match
- Fuzzy match (case insensitive, whitespace normalized, common suffixes stripped: Inc, Ltd, LLC, Pvt)
- Flag potential duplicates for manual review

**Phone duplicates:**
- Normalize phone numbers (strip spaces, dashes, country codes)
- Exact match on normalized form

```
DUPLICATE REPORT
===
EXACT DUPLICATES (same email): 8 sets, 18 records
  - john@acme.com appears in rows 12, 45, 89
  - sarah@beta.com appears in rows 23, 67

PROBABLE DUPLICATES (fuzzy company match): 5 sets, 12 records
  - "Acme Corp" / "Acme Corporation" / "ACME" -- rows 12, 34, 56
  - "Beta Inc" / "Beta Inc." -- rows 23, 78

CROSS-TAB DUPLICATES: 3 records appear in both Researched Leads and Outreach CRM
  - john@acme.com -- Researched Leads row 5, Outreach CRM row 12
```

## Phase 4: Stale Lead Detection

Identify leads that have not been updated recently:

```
STALE LEADS (not updated in 30+ days)
===
Company          | Contact      | Stage           | Last Updated | Days Stale
-----------------|-------------|-----------------|--------------|----------
Acme Corp        | John Smith  | Discovery Call  | 2024-01-15   | 60 days
Beta Inc         | Sarah Jones | Proposal Sent   | 2024-01-28   | 47 days
Gamma Ltd        | Mike Chen   | Qualified       | 2024-02-01   | 43 days

TOTAL STALE: 23 leads (15.3% of pipeline)
```

Categorize stale leads:
- **Re-engage**: in active stages (Qualified, Discovery, Proposal) -- needs follow-up
- **Archive**: in early stages (New Lead) for 60+ days -- likely dead
- **Urgent**: in late stages (Negotiation, Verbal Commit) -- deal at risk

## Phase 5: Email Validation

If email validation tools are available:

```
EMAIL QUALITY CHECK
===
Valid emails: 128 (91.4%)
Invalid format: 5 (3.6%)
  - "john@" (row 34) -- missing domain
  - "sarah.jones" (row 67) -- missing @ and domain
  - "mike@.com" (row 89) -- empty domain name
Risky/disposable: 4 (2.9%)
  - "contact@mailinator.com" (row 12)
Bounced (if validation API used): 3 (2.1%)
```

If no validation tool, check format only:
- Valid email regex pattern
- Common typos (gmial.com, gamil.com, outlok.com)
- Generic addresses (info@, contact@, hello@) flagged as low quality

## Phase 6: Consistency Checks

Audit formatting consistency across the CRM:

**Stage names:**
- Check all stage values against `crm.stages[]`
- Flag non-standard stage names
- Example issues: "qualified" vs "Qualified" vs "QUALIFIED", "Prop Sent" vs "Proposal Sent"

**Date formats:**
- Check all date fields for consistent formatting
- Flag mixed formats (MM/DD/YYYY vs DD/MM/YYYY vs YYYY-MM-DD)

**Phone formats:**
- Check for consistent phone number formatting
- Flag entries with letters, special characters, or incomplete numbers

**Company name formatting:**
- Flag all-caps entries
- Flag entries with leading/trailing whitespace
- Flag entries with inconsistent capitalization

```
CONSISTENCY ISSUES
===
Stage name variations: 4 non-standard values found
  - "qual" should be "Qualified" (3 records)
  - "proposed" should be "Proposal Sent" (1 record)

Date format inconsistencies: 12 records
  - 8 records use MM/DD/YYYY, 130 use YYYY-MM-DD

Company name issues: 7 records
  - "ACME CORP" should be "Acme Corp" (2 records)
  - " Beta Inc " has leading/trailing spaces (1 record)
```

## Phase 7: Stage Stuck Analysis

Identify leads stuck in the same stage too long:

```
STAGE DURATION ANALYSIS
===
Stage             | Avg Days | Expected Max | Stuck (over max)
------------------|----------|-------------|------------------
New Lead          | 5 days   | 7 days      | 8 leads
Qualified         | 8 days   | 14 days     | 3 leads
Discovery Call    | 12 days  | 14 days     | 2 leads
Proposal Sent     | 15 days  | 21 days     | 5 leads
Negotiation       | 10 days  | 14 days     | 1 lead
```

For each stuck lead, recommend an action:
- Advance to next stage (if ready)
- Send a follow-up
- Schedule a call
- Disqualify and archive

## Phase 8: Completeness Score

Calculate a per-record completeness score:

```
score = (filled_required_fields / total_required_fields) * 100
```

Categorize:
- **Green (90-100%)**: record is complete, no action needed
- **Yellow (70-89%)**: partially complete, minor fixes needed
- **Red (below 70%)**: critically incomplete, needs immediate attention

```
CRM HEALTH SUMMARY
===
Overall completeness score: 80.6%
Green records (90%+): 95 (63%)
Yellow records (70-89%): 35 (23%)
Red records (<70%): 20 (13%)

Data quality grade: B-
```

## Phase 9: Output

Return structured JSON:

```json
{
  "crm_audit": {
    "audit_date": "2024-03-15",
    "total_records": 150,
    "tabs_audited": ["Researched Leads", "Outreach CRM", "Inbound Leads"],
    "overall_completeness": 80.6,
    "data_quality_grade": "B-",
    "missing_fields": {
      "by_field": {},
      "critically_incomplete_records": []
    },
    "duplicates": {
      "exact_email_duplicates": 8,
      "probable_company_duplicates": 5,
      "cross_tab_duplicates": 3,
      "records_to_merge": []
    },
    "stale_leads": {
      "total": 23,
      "re_engage": [],
      "archive": [],
      "urgent": []
    },
    "email_quality": {
      "valid": 128,
      "invalid_format": 5,
      "risky": 4,
      "records_to_fix": []
    },
    "consistency_issues": {
      "stage_variations": [],
      "date_format_issues": [],
      "name_formatting": []
    },
    "stuck_leads": [],
    "record_scores": {
      "green": 95,
      "yellow": 35,
      "red": 20
    },
    "priority_actions": [
      "Fix 5 invalid email addresses (rows 34, 67, 89, 91, 103)",
      "Merge 8 duplicate email sets",
      "Re-engage 12 stale leads in active stages",
      "Archive 11 stale New Leads (60+ days old)",
      "Standardize 4 non-standard stage names"
    ]
  }
}
```

## Example Usage

**Trigger phrases:**
- "Audit our CRM data quality"
- "How clean is our pipeline data?"
- "Check for duplicate leads in the CRM"
- "Find stale leads that need follow-up"
- "Run a data hygiene check"
- "What's our CRM completeness score?"

```
User: Audit our CRM data quality
Assistant: [reads CRM data via crm-writer, checks all fields for completeness, finds 8 duplicate sets, 23 stale leads, 5 invalid emails, calculates 80.6% completeness, outputs prioritized action list]
```

```
User: Find leads stuck in our pipeline
Assistant: [analyzes stage durations, identifies 19 leads past expected stage time, categorizes by urgency, recommends specific next actions per lead]
```
