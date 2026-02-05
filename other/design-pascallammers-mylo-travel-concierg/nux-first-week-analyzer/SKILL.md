---
name: nux-first-week-analyzer
description: Analyze new user experience (NUX) in their first week after onboarding completion
triggers:
  - nux analysis
  - nux report
  - new user experience
  - first week analysis
  - new user cohort
  - onboarding cohort analysis
  - how are new users doing
  - user retention analysis
  - first week engagement
  - nux metrics
  - new user metrics
---

# nux-first-week-analyzer Skill

## Purpose

Analyze the new user experience (NUX) for users who have completed onboarding. This skill helps identify engagement patterns, intervention effectiveness, user confusion, and product issues during the critical first 7 days.

**Use this skill when:**
- User asks for "NUX analysis" or "NUX report"
- User asks about "new user experience" or "first week"
- User asks about onboarding cohorts or cohort analysis
- User asks about user engagement after onboarding
- User asks about intervention effectiveness for new users
- User asks about user retention or dropout patterns
- User asks "how are new users doing?"
- User asks for "NUX metrics" or "new user metrics"

---

## Data Filters

### User Types

| Type | Include | Flag | Notes |
|------|---------|------|-------|
| USER | Yes | No | Regular users |
| EMPLOYEE | Yes | **Yes** | Flag as `[EMPLOYEE]` in reports |
| TEST | No | N/A | Exclude completely |

**Always filter out TEST users. Always flag EMPLOYEE users.**

---

## Step 1: Determine Analysis Parameters

Ask the user (or use defaults):

| Parameter | Default | Description |
|-----------|---------|-------------|
| Time window | 28 days | How far back to look for completed onboardings |
| Include incomplete | No | Only COMPLETED onboardings by default |
| Cohort granularity | Weekly | Group by week (Mon-Sun) |

---

## Step 2: Identify Cohorts

Run this query using the **sql-reader skill**:

```sql
-- Get all completed onboardings with user details
WITH onboarded_users AS (
  SELECT
    co.id as onboarding_id,
    co.created_at as onboarding_completed_at,
    co.conversation_id as group_conversation_id,
    DATE_TRUNC('week', co.created_at AT TIME ZONE 'America/Los_Angeles')::date as cohort_week,
    pc.person_id,
    p.name,
    p.type as person_type,
    EXTRACT(DAY FROM NOW() - co.created_at) as days_since_onboarding
  FROM conversation_onboarding co
  JOIN conversation_participant_onboarding cpo ON cpo.conversation_onboarding_id = co.id
  JOIN person_contacts pc ON cpo.person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  WHERE co.state = 'COMPLETED'
    AND co.created_at >= NOW() - INTERVAL '[TIME_WINDOW] days'
    AND p.type != 'TEST'  -- Exclude TEST users
),
user_1on1_convs AS (
  SELECT
    cp.person_id,
    c.id as one_on_one_conv_id
  FROM conversation_participant cp
  JOIN conversation c ON cp.conversation_id = c.id
  WHERE c.type = 'ONE_ON_ONE'
    AND cp.role = 'MEMBER'
)
SELECT
  ou.cohort_week,
  ou.person_id,
  ou.name,
  ou.person_type,
  ou.onboarding_completed_at,
  ou.group_conversation_id,
  u1.one_on_one_conv_id,
  ou.days_since_onboarding::int
FROM onboarded_users ou
LEFT JOIN user_1on1_convs u1 ON ou.person_id = u1.person_id
ORDER BY ou.cohort_week, ou.onboarding_completed_at, ou.name;
```

**Replace `[TIME_WINDOW]` with number of days (default: 28).**

---

## Step 3: Calculate Time to First Intervention

```sql
WITH onboarded_users AS (
  SELECT
    co.id as onboarding_id,
    co.created_at as onboarding_completed_at,
    DATE_TRUNC('week', co.created_at AT TIME ZONE 'America/Los_Angeles')::date as cohort_week,
    pc.person_id,
    p.name,
    p.type as person_type
  FROM conversation_onboarding co
  JOIN conversation_participant_onboarding cpo ON cpo.conversation_onboarding_id = co.id
  JOIN person_contacts pc ON cpo.person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  WHERE co.state = 'COMPLETED'
    AND co.created_at >= NOW() - INTERVAL '[TIME_WINDOW] days'
    AND p.type != 'TEST'
),
user_1on1_convs AS (
  SELECT cp.person_id, c.id as one_on_one_conv_id
  FROM conversation_participant cp
  JOIN conversation c ON cp.conversation_id = c.id
  WHERE c.type = 'ONE_ON_ONE' AND cp.role = 'MEMBER'
),
first_interventions AS (
  SELECT
    ou.person_id,
    ou.onboarding_completed_at,
    MIN(im.created_at) as first_intervention_at
  FROM onboarded_users ou
  JOIN user_1on1_convs u1 ON ou.person_id = u1.person_id
  JOIN intervention_message im ON im.conversation_id = u1.one_on_one_conv_id
  WHERE im.status = 'SENT'
    AND im.created_at >= ou.onboarding_completed_at
    AND im.created_at < ou.onboarding_completed_at + INTERVAL '7 days'
  GROUP BY ou.person_id, ou.onboarding_completed_at
)
SELECT
  ou.cohort_week,
  ou.person_id,
  ou.name,
  CASE WHEN ou.person_type = 'EMPLOYEE' THEN '[EMPLOYEE]' ELSE '' END as flag,
  ou.onboarding_completed_at,
  fi.first_intervention_at,
  ROUND(EXTRACT(EPOCH FROM (fi.first_intervention_at - ou.onboarding_completed_at)) / 3600, 1) as hours_to_first,
  ROUND(EXTRACT(EPOCH FROM (fi.first_intervention_at - ou.onboarding_completed_at)) / 86400, 1) as days_to_first
FROM onboarded_users ou
LEFT JOIN first_interventions fi ON ou.person_id = fi.person_id
ORDER BY ou.cohort_week, ou.name;
```

---

## Step 4: Analyze Message Activity

### Messages by Day Since Onboarding

```sql
WITH onboarded_users AS (
  SELECT
    co.created_at as onboarding_completed_at,
    DATE_TRUNC('week', co.created_at AT TIME ZONE 'America/Los_Angeles')::date as cohort_week,
    pc.person_id,
    p.name,
    p.type as person_type
  FROM conversation_onboarding co
  JOIN conversation_participant_onboarding cpo ON cpo.conversation_onboarding_id = co.id
  JOIN person_contacts pc ON cpo.person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  WHERE co.state = 'COMPLETED'
    AND co.created_at >= NOW() - INTERVAL '[TIME_WINDOW] days'
    AND p.type != 'TEST'
),
user_messages AS (
  SELECT
    ou.cohort_week,
    ou.person_id,
    c.type as conv_type,
    FLOOR(EXTRACT(EPOCH FROM (m.provider_timestamp - ou.onboarding_completed_at)) / 86400) as day_number
  FROM onboarded_users ou
  JOIN person_contacts pc ON pc.person_id = ou.person_id
  JOIN message m ON m.sender_person_contact_id = pc.id
  JOIN conversation c ON m.conversation_id = c.id
  WHERE m.provider_timestamp >= ou.onboarding_completed_at
    AND m.provider_timestamp < ou.onboarding_completed_at + INTERVAL '7 days'
    AND m.provider_data->>'reaction_id' IS NULL
)
SELECT
  day_number,
  COUNT(*) as total_messages,
  COUNT(*) FILTER (WHERE conv_type = 'GROUP') as group_msgs,
  COUNT(*) FILTER (WHERE conv_type = 'ONE_ON_ONE') as one_on_one_msgs,
  COUNT(DISTINCT person_id) as active_users
FROM user_messages
GROUP BY day_number
ORDER BY day_number;
```

### Engagement Status per User

```sql
WITH onboarded_users AS (
  SELECT
    co.created_at as onboarding_completed_at,
    DATE_TRUNC('week', co.created_at AT TIME ZONE 'America/Los_Angeles')::date as cohort_week,
    pc.person_id,
    p.name,
    p.type as person_type,
    EXTRACT(DAY FROM NOW() - co.created_at) as days_since_onboarding
  FROM conversation_onboarding co
  JOIN conversation_participant_onboarding cpo ON cpo.conversation_onboarding_id = co.id
  JOIN person_contacts pc ON cpo.person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  WHERE co.state = 'COMPLETED'
    AND co.created_at >= NOW() - INTERVAL '[TIME_WINDOW] days'
    AND p.type != 'TEST'
),
user_messages_by_day AS (
  SELECT
    ou.person_id,
    COUNT(*) FILTER (WHERE FLOOR(EXTRACT(EPOCH FROM (m.provider_timestamp - ou.onboarding_completed_at)) / 86400) = 0) as day_0,
    COUNT(*) FILTER (WHERE FLOOR(EXTRACT(EPOCH FROM (m.provider_timestamp - ou.onboarding_completed_at)) / 86400) BETWEEN 1 AND 3) as days_1_3,
    COUNT(*) FILTER (WHERE FLOOR(EXTRACT(EPOCH FROM (m.provider_timestamp - ou.onboarding_completed_at)) / 86400) BETWEEN 4 AND 6) as days_4_6,
    COUNT(*) FILTER (WHERE FLOOR(EXTRACT(EPOCH FROM (m.provider_timestamp - ou.onboarding_completed_at)) / 86400) >= 7) as days_7_plus
  FROM onboarded_users ou
  JOIN person_contacts pc ON pc.person_id = ou.person_id
  JOIN message m ON m.sender_person_contact_id = pc.id
  WHERE m.provider_timestamp >= ou.onboarding_completed_at
    AND m.provider_data->>'reaction_id' IS NULL
  GROUP BY ou.person_id
)
SELECT
  ou.cohort_week,
  ou.person_id,
  ou.name,
  CASE WHEN ou.person_type = 'EMPLOYEE' THEN '[EMPLOYEE]' ELSE '' END as flag,
  ou.days_since_onboarding::int as tenure_days,
  COALESCE(um.day_0, 0) as day_0,
  COALESCE(um.days_1_3, 0) as days_1_3,
  COALESCE(um.days_4_6, 0) as days_4_6,
  COALESCE(um.days_7_plus, 0) as days_7_plus,
  CASE
    WHEN COALESCE(um.days_1_3, 0) = 0 AND COALESCE(um.days_4_6, 0) = 0 AND COALESCE(um.days_7_plus, 0) = 0
      AND ou.days_since_onboarding > 1 THEN 'Day 0 only'
    WHEN COALESCE(um.days_4_6, 0) = 0 AND COALESCE(um.days_7_plus, 0) = 0
      AND ou.days_since_onboarding > 6 THEN 'Day 0-3 only'
    WHEN ou.days_since_onboarding <= 6 THEN 'Too early'
    ELSE 'Active week 1+'
  END as engagement_status
FROM onboarded_users ou
LEFT JOIN user_messages_by_day um ON ou.person_id = um.person_id
ORDER BY ou.cohort_week, ou.name;
```

---

## Step 5: Analyze Intervention Types

### Intervention Type Breakdown (First 7 Days)

```sql
WITH onboarded_users AS (
  SELECT
    co.created_at as onboarding_completed_at,
    DATE_TRUNC('week', co.created_at AT TIME ZONE 'America/Los_Angeles')::date as cohort_week,
    pc.person_id,
    p.type as person_type
  FROM conversation_onboarding co
  JOIN conversation_participant_onboarding cpo ON cpo.conversation_onboarding_id = co.id
  JOIN person_contacts pc ON cpo.person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  WHERE co.state = 'COMPLETED'
    AND co.created_at >= NOW() - INTERVAL '[TIME_WINDOW] days'
    AND p.type != 'TEST'
),
user_1on1_convs AS (
  SELECT cp.person_id, c.id as one_on_one_conv_id
  FROM conversation_participant cp
  JOIN conversation c ON cp.conversation_id = c.id
  WHERE c.type = 'ONE_ON_ONE' AND cp.role = 'MEMBER'
),
interventions_7d AS (
  SELECT
    ou.cohort_week,
    ou.person_id,
    im.prompt_key,
    i.type as intervention_type
  FROM onboarded_users ou
  JOIN user_1on1_convs u1 ON ou.person_id = u1.person_id
  JOIN intervention_message im ON im.conversation_id = u1.one_on_one_conv_id
  JOIN intervention i ON im.intervention_id = i.id
  WHERE im.status = 'SENT'
    AND im.created_at >= ou.onboarding_completed_at
    AND im.created_at < ou.onboarding_completed_at + INTERVAL '7 days'
)
SELECT
  prompt_key,
  intervention_type,
  COUNT(*) as count,
  COUNT(DISTINCT person_id) as unique_users
FROM interventions_7d
GROUP BY prompt_key, intervention_type
ORDER BY count DESC;
```

---

## Step 6: Identify User Confusion Signals

### Confusion Message Patterns

```sql
WITH onboarded_users AS (
  SELECT
    co.created_at as onboarding_completed_at,
    DATE_TRUNC('week', co.created_at AT TIME ZONE 'America/Los_Angeles')::date as cohort_week,
    pc.person_id,
    p.name,
    p.type as person_type
  FROM conversation_onboarding co
  JOIN conversation_participant_onboarding cpo ON cpo.conversation_onboarding_id = co.id
  JOIN person_contacts pc ON cpo.person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  WHERE co.state = 'COMPLETED'
    AND co.created_at >= NOW() - INTERVAL '[TIME_WINDOW] days'
    AND p.type != 'TEST'
),
user_1on1_convs AS (
  SELECT cp.person_id, c.id as one_on_one_conv_id
  FROM conversation_participant cp
  JOIN conversation c ON cp.conversation_id = c.id
  WHERE c.type = 'ONE_ON_ONE' AND cp.role = 'MEMBER'
),
user_msgs_to_coach AS (
  SELECT
    ou.cohort_week,
    ou.person_id,
    ou.name,
    ou.person_type,
    m.id as message_id,
    m.content,
    m.provider_timestamp,
    FLOOR(EXTRACT(EPOCH FROM (m.provider_timestamp - ou.onboarding_completed_at)) / 86400) as day_number
  FROM onboarded_users ou
  JOIN user_1on1_convs u1 ON ou.person_id = u1.person_id
  JOIN person_contacts pc ON pc.person_id = ou.person_id
  JOIN message m ON m.conversation_id = u1.one_on_one_conv_id
    AND m.sender_person_contact_id = pc.id
  WHERE m.provider_timestamp >= ou.onboarding_completed_at
    AND m.provider_timestamp < ou.onboarding_completed_at + INTERVAL '7 days'
    AND m.provider_data->>'reaction_id' IS NULL
)
SELECT
  cohort_week,
  person_id,
  name,
  CASE WHEN person_type = 'EMPLOYEE' THEN '[EMPLOYEE]' ELSE '' END as flag,
  day_number,
  message_id,
  provider_timestamp,
  content
FROM user_msgs_to_coach
WHERE
  -- Confusion patterns
  LOWER(content) LIKE '%how does%'
  OR LOWER(content) LIKE '%what is%'
  OR LOWER(content) LIKE '%why did%'
  OR LOWER(content) LIKE '%i don''t understand%'
  OR LOWER(content) LIKE '%don''t get it%'
  OR LOWER(content) LIKE '%not sure how%'
  OR LOWER(content) LIKE '%wrong person%'
  OR LOWER(content) LIKE '%confused%'
  OR LOWER(content) LIKE '%??%'
  OR LOWER(content) LIKE '%how do i%'
  OR LOWER(content) LIKE '%how do you%'
  OR LOWER(content) LIKE '%what are you%'
  OR LOWER(content) LIKE '%who are you%'
  OR LOWER(content) LIKE '%what do you do%'
  OR LOWER(content) LIKE '%how do you work%'
ORDER BY cohort_week, name, day_number;
```

### Confusion Pattern Summary

```sql
-- Summarize confusion patterns
SELECT
  'Asks what now after access code' as pattern,
  COUNT(*) as occurrences,
  COUNT(DISTINCT person_id) as unique_users
FROM user_msgs_to_coach
WHERE LOWER(content) LIKE '%what now%'

UNION ALL

SELECT
  'How do you work / functionality questions' as pattern,
  COUNT(*) as occurrences,
  COUNT(DISTINCT person_id) as unique_users
FROM user_msgs_to_coach
WHERE LOWER(content) LIKE '%how do you work%' OR LOWER(content) LIKE '%how does%'

UNION ALL

SELECT
  'Stop / End session requests' as pattern,
  COUNT(*) as occurrences,
  COUNT(DISTINCT person_id) as unique_users
FROM user_msgs_to_coach
WHERE LOWER(content) = 'stop' OR LOWER(content) LIKE '%log off%' OR LOWER(content) LIKE '%stop these texts%'

ORDER BY occurrences DESC;
```

---

## Step 7: Identify Product Experience Issues

Look for these patterns in user messages:

| Pattern | SQL Filter | Issue Category |
|---------|-----------|----------------|
| Bedtime / timing | `LIKE '%bedtime%' OR LIKE '%log off%'` | Quiet hours |
| Technical issues | `LIKE '%not going thru%' OR LIKE '%not letting me%'` | Messaging |
| Stop requests | `= 'stop'` | Pause feature |
| Busy interruptions | `LIKE '%busy%' OR LIKE '%can''t right now%'` | Context |

```sql
-- Product experience issues
SELECT
  person_id,
  name,
  CASE WHEN person_type = 'EMPLOYEE' THEN '[EMPLOYEE]' ELSE '' END as flag,
  day_number,
  message_id,
  LEFT(content, 200) as content_preview,
  CASE
    WHEN LOWER(content) LIKE '%bedtime%' OR LOWER(content) LIKE '%log off%' THEN 'Quiet hours'
    WHEN LOWER(content) LIKE '%not going%' OR LOWER(content) LIKE '%not letting%' THEN 'Technical'
    WHEN LOWER(content) = 'stop' THEN 'Stop request'
    WHEN LOWER(content) LIKE '%busy%' THEN 'Context interruption'
    ELSE 'Other'
  END as issue_category
FROM user_msgs_to_coach
WHERE
  LOWER(content) LIKE '%trying%'
  OR LOWER(content) LIKE '%not going%'
  OR LOWER(content) LIKE '%not letting%'
  OR LOWER(content) LIKE '%can''t%'
  OR LOWER(content) LIKE '%won''t%'
  OR LOWER(content) LIKE '%bedtime%'
  OR LOWER(content) LIKE '%busy%'
  OR LOWER(content) = 'stop'
  OR LOWER(content) LIKE '%log off%'
ORDER BY day_number, name;
```

---

## Step 8: Generate Report

Create a comprehensive markdown report:

```markdown
# New User First Week Analysis

**Analysis Period:** Last [X] days
**Report Generated:** [Date]
**Scope:** COMPLETED onboardings only

---

## Executive Summary

- **X couples (Y users)** completed onboarding
- **Z%** received interventions within first 7 days
- **Average time to first intervention:** X hours
- **Primary issue:** [Key finding]

---

## Cohort Overview

| Cohort Week | Couples | Users | Users With Interventions (7d) | Avg Hours to 1st |
|-------------|---------|-------|-------------------------------|------------------|
| [date] | X | Y | Z (%) | N |

---

## Time to First Intervention

### By User
[Table with each user, flagging EMPLOYEE users]

---

## Engagement Status

| Status | Count | % |
|--------|-------|---|
| Active week 1+ | X | Y% |
| Day 0-3 only | X | Y% |
| Day 0 only | X | Y% |
| Too early | X | Y% |

### By User
[Table with day-by-day message counts]

---

## Intervention Types (First 7 Days)

[Table with intervention types and counts]

---

## User Confusion Signals

[Table with confusion messages]

---

## Product Experience Issues

[Table categorized by issue type]

---

## Key Findings & Recommendations

1. **[Finding]**
   - Impact: [description]
   - Recommendation: [action]

---

## Data Notes

- Analysis excludes TEST users
- EMPLOYEE users flagged with [EMPLOYEE]
- Admin links: `https://admin.prod.cncorp.io/persons/{id}`
```

---

## Step 9: Save Report

Save the report to `docs/new_user_first_week_analysis_[DATE].md`

---

## Common Violations

- **BANNED:** Including TEST users in analysis
- **BANNED:** Not flagging EMPLOYEE users
- **BANNED:** Using `intervention_message.status = 'sent'` (should be `'SENT'` - uppercase)
- **CRITICAL:** Always filter reactions with `m.provider_data->>'reaction_id' IS NULL` when counting user messages
- **CRITICAL:** Use `conversation.type = 'ONE_ON_ONE'` (not 'INDIVIDUAL')
- **CRITICAL:** Join through `person_contacts` to get message sender, not directly to `persons`

---

## Schema Reference

### Key Tables

| Table | Purpose |
|-------|---------|
| `conversation_onboarding` | Tracks onboarding state (COMPLETED, INITIATOR_JOINED, etc.) |
| `conversation_participant_onboarding` | Links participants to onboarding |
| `intervention` | Intervention decisions/triggers |
| `intervention_message` | Actual intervention messages sent |
| `message` | All messages (use `content` column, not `body`) |
| `persons` | User data (filter by `type` column) |

### Person Types

| Type | Action |
|------|--------|
| USER | Include |
| EMPLOYEE | Include but flag |
| TEST | Exclude |

### Intervention Message Status

Use uppercase: `'SENT'`, `'WITHHELD_PREFERENCE'`, `'WITHHELD_RANDOM'`, `'MESSAGING_FAILURE'`

---

## Success Criteria

You've completed this skill when:
- [ ] Identified all completed onboardings in time window
- [ ] Excluded TEST users, flagged EMPLOYEE users
- [ ] Calculated time to first intervention by user
- [ ] Analyzed message activity by day since onboarding
- [ ] Categorized engagement status (Day 0 only, Active week 1+, etc.)
- [ ] Identified intervention types and frequencies
- [ ] Found user confusion signals
- [ ] Identified product experience issues
- [ ] Generated comprehensive markdown report
- [ ] Saved report to docs/

---

## Related Skills

- **sql-reader**: Required for database queries
- **incomplete-onboarding-assessor**: For users who haven't completed onboarding
- **langfuse-prompt-and-trace-debugger**: For debugging intervention delivery
