---
name: lead-gen-email
description: Skill for Lead Generation and Email Marketing automation in n8n. Use for creating leads, scoring, enrichment, email campaigns, and nurturing sequences. Activate when working on lead capture forms, email workflows, MQL/SQL qualification, or marketing automation.
---

# Lead Gen + Email Marketing Skill

## Overview

This skill covers the Lead Generation and Email Marketing module of the AI Marketing Department. It provides patterns, templates, and best practices for building lead capture, scoring, enrichment, and email automation workflows.

## Database Schema Reference

### Core Tables

```sql
-- Leads table (main CRM)
leads (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  first_name TEXT,
  last_name TEXT,
  company TEXT,
  job_title TEXT,
  source TEXT,           -- 'form', 'linkedin', 'meta_ads', 'google_ads', 'organic'
  source_detail TEXT,
  score INTEGER DEFAULT 0,
  score_breakdown JSONB,
  qualification_status TEXT, -- 'new', 'mql', 'sql', 'customer', 'disqualified'
  email_status TEXT,     -- 'subscribed', 'unsubscribed', 'bounced'
  enriched_data JSONB,
  tags TEXT[],
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
)

-- Lead events (for scoring)
lead_events (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  lead_id UUID NOT NULL,
  event_type TEXT,       -- 'form_submit', 'email_open', 'email_click', etc.
  event_data JSONB,
  score_delta INTEGER,
  source TEXT,
  created_at TIMESTAMPTZ
)

-- Email sequences
email_sequences (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  name TEXT,
  trigger_type TEXT,     -- 'lead_created', 'tag_added', 'score_reached', 'manual'
  trigger_config JSONB,
  status TEXT            -- 'draft', 'active', 'paused'
)

-- Sequence steps
sequence_steps (
  id UUID PRIMARY KEY,
  sequence_id UUID NOT NULL,
  step_order INTEGER,
  delay_days INTEGER,
  delay_hours INTEGER,
  action_type TEXT,      -- 'send_email', 'add_tag', 'update_score', 'notify_team'
  action_config JSONB
)

-- Sequence enrollments
sequence_enrollments (
  id UUID PRIMARY KEY,
  sequence_id UUID NOT NULL,
  lead_id UUID NOT NULL,
  current_step INTEGER,
  status TEXT,           -- 'active', 'completed', 'exited'
  next_action_at TIMESTAMPTZ
)
```

## Workflow Patterns

### 1. Lead Capture Entry Point

**Purpose**: Normalize leads from any source (forms, ads, LinkedIn, etc.)

**Pattern**:
```
Webhook Trigger → Source Detection → Data Normalization → 
Dedup Check → Create/Update Lead → Log Event → Trigger Sub-workflows
```

**Source Detection Logic**:
```javascript
function detectSource(headers, body) {
  // LinkedIn Lead Gen
  if (headers['x-linkedin-webhook'] || body.leadgen_id) {
    return { source: 'linkedin', source_detail: body.form_name };
  }
  // Meta Ads
  if (body.leadgen_id && body.field_data) {
    return { source: 'meta_ads', source_detail: body.ad_name };
  }
  // Google Ads
  if (body.google_key) {
    return { source: 'google_ads', source_detail: body.campaign_name };
  }
  // Default: form
  return { source: 'form', source_detail: body.form_name || 'Web Form' };
}
```

### 2. Lead Enrichment Agent

**Purpose**: AI-powered data enrichment using external sources

**Pattern**:
```
Execute Workflow Trigger → Get Lead → Check if needs enrichment →
AI Agent (with Perplexity tool) → Parse structured output →
Calculate score adjustments → Update Lead → Log Event
```

**AI Output Schema**:
```json
{
  "company_name": "string",
  "company_size": "1-10 | 10-50 | 50-200 | 200-1000 | 1000+",
  "industry": "string",
  "is_decision_maker": "boolean",
  "decision_maker_level": "C-Level | Director | Manager | IC",
  "linkedin_company_url": "string | null",
  "company_website": "string | null",
  "technologies_used": ["array"],
  "enrichment_confidence": "high | medium | low",
  "notes": "string"
}
```

### 3. Lead Scoring Engine

**Purpose**: Calculate lead score based on events and attributes

**Pattern**:
```
Execute Workflow Trigger → Get Lead → Get Scoring Rules → 
Get Lead Events → Calculate Score → Update Lead → 
Check Status Change → Trigger MQL Alert if needed
```

**Scoring Rule Types**:
- `event`: Points for specific actions (form_submit: +10, email_open: +2)
- `attribute`: Points for lead characteristics (decision_maker: +15)
- `decay`: Negative points for inactivity (-5 after 30 days)

**Thresholds**:
- MQL: score >= 50
- SQL: score >= 100

### 4. Email Campaign Builder (AI)

**Purpose**: Generate complete email campaigns using AI

**Input Schema**:
```json
{
  "campaign_name": "Welcome Campaign",
  "campaign_type": "broadcast | promotional | educational | re-engagement",
  "tenant_id": "uuid",
  "tone": "professional | friendly | urgent",
  "cta_goal": "book_demo | download | visit_page | reply",
  "product_name": "Your Product",
  "company_name": "Your Company",
  "brand_voice": "optional brand guidelines"
}
```

**Output**: Subject lines (3 variants), preview text, HTML content, plain text

### 5. Nurturing Sequence Processor

**Purpose**: Scheduled automation that processes sequence steps

**Pattern**:
```
Schedule (15 min) → Get Pending Enrollments → 
For Each: Get Next Step → Get Lead → Check Subscribed →
Route by Action Type → Execute Action → 
Calculate Next Action Time → Update Enrollment
```

**Action Types**:
- `send_email`: Send personalized email
- `add_tag`: Add tag to lead
- `update_score`: Adjust score by delta
- `notify_team`: Send Slack notification
- `webhook`: Call external URL

### 6. MQL Alert System

**Purpose**: Notify sales team when leads qualify

**Pattern**:
```
Execute Workflow Trigger → Get Lead → Check Qualification →
Build Rich Notification → Send Slack + Email → Log Event
```

## Personalization Tokens

Use in email content:
- `{{first_name}}` - Lead's first name
- `{{last_name}}` - Lead's last name
- `{{company}}` - Company name
- `{{email}}` - Email address
- `{{unsubscribe_url}}` - Unsubscribe link

## Supabase Query Patterns

### Get leads needing nurturing action:
```javascript
filterString: "status=eq.active&next_action_at=lte.{{ $now.toISO() }}"
```

### Get leads by score range:
```javascript
filterString: "tenant_id=eq.{{ $json.tenant_id }}&score=gte.50&score=lt.100"
```

### Get subscribed leads only:
```javascript
filterString: "email_status=eq.subscribed"
```

## Error Handling Best Practices

1. **Always check email_status** before sending emails
2. **Log all events** to lead_events for audit trail
3. **Use continueOnFail** on Slack/email nodes
4. **Validate email format** on lead capture
5. **Check enriched_at** to avoid duplicate enrichment

## Multi-tenant Considerations

- All tables have `tenant_id` column
- RLS policies enforce tenant isolation
- Store `tenant_id` in workflow config node
- Pass `tenant_id` to all sub-workflows

## Testing Checklist

- [ ] Lead capture from different sources
- [ ] Duplicate detection working
- [ ] Enrichment populates enriched_data
- [ ] Score calculation correct
- [ ] MQL threshold triggers alert
- [ ] Sequence steps execute in order
- [ ] Unsubscribed leads skip emails
- [ ] Personalization tokens replaced
