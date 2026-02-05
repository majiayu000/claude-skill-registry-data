---
name: therapist-data-scientist
description: Calculate Gottman SPAFF affect ratios and other therapeutic insights for relationship coaching data. Employee-facing tool for HIPAA-certified team members.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Therapist Data Scientist Skill

Calculate accurate Gottman SPAFF (Specific Affect) affect ratios and extract therapeutic insights from relationship coaching data using SQL queries.

## 🚨 MANDATORY: Read Data Quirks First

**BEFORE running any analysis or queries, you MUST read the data quirks documentation:**

```bash
cat docs/sql/DATA_QUIRKS.md
```

**Why:** The database has critical semantic quirks for relationship data:
- NULL repair rates = stonewalling behavior (not missing data)
- Affect ratio 100:1 can mean perfect OR avoidance
- Conflict state capitalization inconsistencies

**DO NOT skip this step. Read the file before every analysis.**

---

## When to Use

Use this skill when you need to:
- Calculate affect ratios for individual partners or couples
- Analyze positive/negative communication patterns over time
- Measure relationship health using Gottman metrics
- Generate data-driven insights for coaching interventions
- Track affect trends and changes over weeks/months
- Investigate conflict patterns (what couples fight about)
- Examine specific message content during conflicts
- Answer ad-hoc questions about relationship communication data

**This skill supports flexible SQL exploration - write custom queries as needed, not just the example queries provided.**

## Prerequisites

**You MUST run sql-reader skill bootstrap first** to understand the schema.

This skill assumes you already know:
- Table structures (`message`, `message_enrichment`, `persons`, `conversation_participant`, `conversation`)
- How to find couples (see sql-reader "Relationship Coaching Schema Patterns")
- How to join messages to people (through `person_contacts` table)
- Schema gotchas (`message.content` not `message.body`, duplicate person names, etc.)

**If you haven't run sql-reader bootstrap, stop and do that first.**

This skill focuses on **Gottman framework calculations**, not schema navigation.

## Gottman SPAFF Affects

### Positive Affects
- Partner-Affection
- Partner-Validation
- Partner-Enthusiasm
- Humor
- Partner-Interest

### Negative Affects
- Partner-Criticism
- Partner-Contempt
- Partner-Defensiveness
- Partner-Complaint
- Partner-Sadness
- Partner-Anger
- Partner-Belligerence
- Partner-Domineering
- Partner-Fear / Tension
- Partner-Threats
- Partner-Disgust
- Partner-Whining
- Stonewalling

### Affect Ratio Thresholds
- **≥20:1** - Upper target (exceptional)
- **≥5:1** - Lower target (healthy, "magic ratio")
- **1:1-5:1** - At-risk
- **<1:1** - Distress

**⚠️ Sample Size Warnings:**
- **<20 classified messages**: Results may not be reliable, consider longer time period
- **Low classification rate**: If total messages >> classified messages, check if messages are being classified
- **No recent activity**: Check last message date - couple may have stopped using the app

**🚨 Four Horsemen (Most Toxic - Flag These):**
1. **Partner-Criticism** - Attacking partner's character
2. **Partner-Contempt** - Mockery, disrespect (strongest predictor of divorce)
3. **Partner-Defensiveness** - Making excuses, counter-attacking
4. **Stonewalling** - Withdrawal, silent treatment

## Example SQL: 8-Week Affect Ratio for a Person

```sql
-- Calculate affect ratio for a specific person over last 8 weeks (56 days)
-- Replace {{person_id}} with actual person_id

WITH target_person AS (
  SELECT
    p.id AS person_id,
    p.name AS person_name,
    cp.person_contact_id,
    cp.conversation_id
  FROM persons p
  JOIN conversation_participant cp ON cp.person_id = p.id
  WHERE p.id = {{person_id}}
    AND cp.role = 'MEMBER'
  LIMIT 1
),
affect_counts AS (
  SELECT
    tp.person_id,
    tp.person_name,
    tp.conversation_id,
    -- Count positive affects
    COUNT(*) FILTER (
      WHERE me.affect IN (
        'Partner-Affection',
        'Partner-Validation',
        'Partner-Enthusiasm',
        'Humor',
        'Partner-Interest'
      )
    ) AS positive_count,
    -- Count negative affects
    COUNT(*) FILTER (
      WHERE me.affect IN (
        'Partner-Criticism',
        'Partner-Contempt',
        'Partner-Defensiveness',
        'Partner-Complaint',
        'Partner-Sadness',
        'Partner-Anger',
        'Partner-Belligerence',
        'Partner-Domineering',
        'Partner-Fear / Tension',
        'Partner-Threats',
        'Partner-Disgust',
        'Partner-Whining',
        'Stonewalling'
      )
    ) AS negative_count,
    -- Total messages with affect classification
    COUNT(*) AS total_classified,
    -- Date range
    MIN(m.provider_timestamp)::date AS first_message_date,
    MAX(m.provider_timestamp)::date AS last_message_date
  FROM target_person tp
  JOIN message m ON m.conversation_id = tp.conversation_id
    AND m.sender_person_contact_id = tp.person_contact_id
  JOIN message_enrichment me ON me.message_id = m.id
  WHERE m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days'
    AND m.provider_timestamp < CURRENT_DATE
  GROUP BY tp.person_id, tp.person_name, tp.conversation_id
)
SELECT
  person_id,
  person_name,
  conversation_id,
  positive_count,
  negative_count,
  total_classified,
  first_message_date,
  last_message_date,
  -- Calculate affect ratio
  CASE
    WHEN negative_count = 0 AND positive_count > 0 THEN 100.0
    WHEN negative_count = 0 THEN 0.0
    ELSE ROUND(positive_count::numeric / negative_count::numeric, 2)
  END AS affect_ratio,
  -- Health assessment
  CASE
    WHEN negative_count = 0 AND positive_count > 0 THEN '🌟 Exceptional (no negatives)'
    WHEN negative_count = 0 THEN '⚠️ No data'
    WHEN positive_count::numeric / negative_count::numeric >= 20.0 THEN '🌟 Exceptional (≥20:1)'
    WHEN positive_count::numeric / negative_count::numeric >= 5.0 THEN '✅ Healthy (≥5:1)'
    WHEN positive_count::numeric / negative_count::numeric >= 1.0 THEN '⚠️ At-Risk (1:1-5:1)'
    ELSE '🚨 Distress (<1:1)'
  END AS relationship_health,
  -- Targets
  5 AS lower_target,
  20 AS upper_target
FROM affect_counts;
```

### Usage Example

```bash
# Calculate affect ratio for person_id 123
arsenal/dot-claude/skills/sql-reader/connect.sh "
-- [Paste the SQL above, replacing {{person_id}} with 123]
"
```

## Example SQL: Couple Affect Ratio (Both Partners Combined)

```sql
-- Calculate affect ratio for a couple (both partners) over last 8 weeks
-- Replace {{person_id}} with either partner's person_id

WITH target_conversation AS (
  SELECT c.id AS conversation_id
  FROM conversation c
  JOIN conversation_participant cp ON cp.conversation_id = c.id
  WHERE cp.person_id = {{person_id}}
    AND c.type = 'GROUP'
  LIMIT 1
),
couple_participants AS (
  SELECT
    tc.conversation_id,
    cp.person_contact_id,
    p.id AS person_id,
    p.name AS person_name
  FROM target_conversation tc
  JOIN conversation_participant cp ON cp.conversation_id = tc.conversation_id
  JOIN persons p ON cp.person_id = p.id
  WHERE cp.role = 'MEMBER'
),
affect_counts AS (
  SELECT
    cp.conversation_id,
    -- Count positive affects across both partners
    COUNT(*) FILTER (
      WHERE me.affect IN (
        'Partner-Affection',
        'Partner-Validation',
        'Partner-Enthusiasm',
        'Humor',
        'Partner-Interest'
      )
    ) AS positive_count,
    -- Count negative affects across both partners
    COUNT(*) FILTER (
      WHERE me.affect IN (
        'Partner-Criticism',
        'Partner-Contempt',
        'Partner-Defensiveness',
        'Partner-Complaint',
        'Partner-Sadness',
        'Partner-Anger',
        'Partner-Belligerence',
        'Partner-Domineering',
        'Partner-Fear / Tension',
        'Partner-Threats',
        'Partner-Disgust',
        'Partner-Whining',
        'Stonewalling'
      )
    ) AS negative_count,
    COUNT(*) AS total_classified,
    STRING_AGG(DISTINCT cp.person_name, ' & ' ORDER BY cp.person_name) AS couple_names
  FROM couple_participants cp
  JOIN message m ON m.conversation_id = cp.conversation_id
    AND m.sender_person_contact_id = cp.person_contact_id
  JOIN message_enrichment me ON me.message_id = m.id
  WHERE m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days'
    AND m.provider_timestamp < CURRENT_DATE
  GROUP BY cp.conversation_id
)
SELECT
  conversation_id,
  couple_names,
  positive_count,
  negative_count,
  total_classified,
  -- Calculate affect ratio
  CASE
    WHEN negative_count = 0 AND positive_count > 0 THEN 100.0
    WHEN negative_count = 0 THEN 0.0
    ELSE ROUND(positive_count::numeric / negative_count::numeric, 2)
  END AS affect_ratio,
  -- Health assessment
  CASE
    WHEN negative_count = 0 AND positive_count > 0 THEN '🌟 Exceptional (no negatives)'
    WHEN negative_count = 0 THEN '⚠️ No data'
    WHEN positive_count::numeric / negative_count::numeric >= 20.0 THEN '🌟 Exceptional (≥20:1)'
    WHEN positive_count::numeric / negative_count::numeric >= 5.0 THEN '✅ Healthy (≥5:1)'
    WHEN positive_count::numeric / negative_count::numeric >= 1.0 THEN '⚠️ At-Risk (1:1-5:1)'
    ELSE '🚨 Distress (<1:1)'
  END AS relationship_health,
  5 AS lower_target,
  20 AS upper_target
FROM affect_counts;
```

## Example SQL: Per-Person Breakdown for a Couple

```sql
-- Show each partner's affect ratio separately, plus couple total
-- Replace {{person_id}} with either partner's person_id

WITH target_conversation AS (
  SELECT c.id AS conversation_id
  FROM conversation c
  JOIN conversation_participant cp ON cp.conversation_id = c.id
  WHERE cp.person_id = {{person_id}}
    AND c.type = 'GROUP'
  LIMIT 1
),
couple_participants AS (
  SELECT
    tc.conversation_id,
    cp.person_contact_id,
    p.id AS person_id,
    p.name AS person_name
  FROM target_conversation tc
  JOIN conversation_participant cp ON cp.conversation_id = tc.conversation_id
  JOIN persons p ON cp.person_id = p.id
  WHERE cp.role = 'MEMBER'
),
per_person_affects AS (
  SELECT
    cp.person_id,
    cp.person_name,
    cp.conversation_id,
    COUNT(*) FILTER (
      WHERE me.affect IN (
        'Partner-Affection',
        'Partner-Validation',
        'Partner-Enthusiasm',
        'Humor',
        'Partner-Interest'
      )
    ) AS positive_count,
    COUNT(*) FILTER (
      WHERE me.affect IN (
        'Partner-Criticism',
        'Partner-Contempt',
        'Partner-Defensiveness',
        'Partner-Complaint',
        'Partner-Sadness',
        'Partner-Anger',
        'Partner-Belligerence',
        'Partner-Domineering',
        'Partner-Fear / Tension',
        'Partner-Threats',
        'Partner-Disgust',
        'Partner-Whining',
        'Stonewalling'
      )
    ) AS negative_count
  FROM couple_participants cp
  JOIN message m ON m.conversation_id = cp.conversation_id
    AND m.sender_person_contact_id = cp.person_contact_id
  JOIN message_enrichment me ON me.message_id = m.id
  WHERE m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days'
    AND m.provider_timestamp < CURRENT_DATE
  GROUP BY cp.person_id, cp.person_name, cp.conversation_id
)
SELECT
  person_name,
  positive_count,
  negative_count,
  CASE
    WHEN negative_count = 0 AND positive_count > 0 THEN 100.0
    WHEN negative_count = 0 THEN 0.0
    ELSE ROUND(positive_count::numeric / negative_count::numeric, 2)
  END AS affect_ratio,
  CASE
    WHEN negative_count = 0 AND positive_count > 0 THEN '🌟 Exceptional'
    WHEN negative_count = 0 THEN '⚠️ No data'
    WHEN positive_count::numeric / negative_count::numeric >= 5.0 THEN '✅ Healthy'
    WHEN positive_count::numeric / negative_count::numeric >= 1.0 THEN '⚠️ At-Risk'
    ELSE '🚨 Distress'
  END AS health
FROM per_person_affects
ORDER BY person_name;
```

## Example SQL: 8-Week Repair Rate for a Couple

**Repair Rate** measures how often partners successfully de-escalate conflicts. When one partner starts a conflict, does the other partner respond in a way that prevents escalation?

**Repair Rate Thresholds:**
- **≥75%** - Healthy repair ability
- **<75%** - Highly defensive, poor conflict management

```sql
-- Calculate repair rate for a couple over last 8 weeks (56 days)
-- Replace {{person_id}} with either partner's person_id
--
-- Repair Success = When partner responds to conflict WITHOUT escalating
-- (i.e., next 5 messages don't contain escalation states)

WITH couple_info AS (
  SELECT
    c.id AS conversation_id,
    MIN(cp.person_id) AS person1_id,
    MAX(cp.person_id) AS person2_id,
    MAX(CASE WHEN cp.person_id = (SELECT MIN(person_id) FROM conversation_participant WHERE conversation_id = c.id AND role = 'MEMBER')
      THEN p.name END) AS person1_name,
    MAX(CASE WHEN cp.person_id = (SELECT MAX(person_id) FROM conversation_participant WHERE conversation_id = c.id AND role = 'MEMBER')
      THEN p.name END) AS person2_name
  FROM conversation c
  JOIN conversation_participant cp ON cp.conversation_id = c.id
  JOIN persons p ON cp.person_id = p.id
  WHERE c.type = 'GROUP'
    AND cp.role = 'MEMBER'
    AND {{person_id}} IN (
      SELECT person_id
      FROM conversation_participant
      WHERE conversation_id = c.id
    )
  GROUP BY c.id
  HAVING COUNT(DISTINCT cp.person_id) = 2
  LIMIT 1
),
-- Find all conflicts started by each person
conflicts AS (
  SELECT
    m.id as conflict_message_id,
    pc.person_id as conflict_starter_id,
    m.provider_timestamp as conflict_time,
    m.conversation_id
  FROM couple_info ci
  JOIN message m ON m.conversation_id = ci.conversation_id
  JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
  JOIN message_enrichment me ON me.message_id = m.id
  WHERE me.conflict_state IN ('New Conflict', 'New conflict', 'Escalation')
    AND m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days'
    AND m.provider_timestamp < CURRENT_DATE
),
-- Check next 5 responses from partner for escalation
conflict_responses AS (
  SELECT
    c.conflict_message_id,
    c.conflict_starter_id,
    c.conflict_time,
    ci.person1_id,
    ci.person2_id,
    -- Did partner respond?
    MAX(CASE WHEN m2.id IS NOT NULL AND pc2.person_id != c.conflict_starter_id THEN 1 ELSE 0 END) as has_response,
    -- Did partner escalate in next 5 messages?
    MAX(CASE
      WHEN pc2.person_id != c.conflict_starter_id
        AND me2.conflict_state IN ('Escalation', 'New Conflict', 'New conflict', 'De-escalation Failed')
      THEN 1
      ELSE 0
    END) as has_escalation
  FROM conflicts c
  JOIN couple_info ci ON ci.conversation_id = c.conversation_id
  LEFT JOIN LATERAL (
    SELECT m.id, m.sender_person_contact_id, m.provider_timestamp
    FROM message m
    WHERE m.conversation_id = c.conversation_id
      AND m.provider_timestamp > c.conflict_time
    ORDER BY m.provider_timestamp
    LIMIT 5
  ) m2 ON true
  LEFT JOIN person_contacts pc2 ON m2.sender_person_contact_id = pc2.id
  LEFT JOIN message_enrichment me2 ON me2.message_id = m2.id
  GROUP BY c.conflict_message_id, c.conflict_starter_id, c.conflict_time, ci.person1_id, ci.person2_id
)
SELECT
  ci.person1_name,
  ci.person2_name,

  -- Person 1 starts conflict, Person 2's repair rate
  COUNT(*) FILTER (WHERE cr.conflict_starter_id = ci.person1_id) as person1_conflicts_introduced,
  CASE
    WHEN COUNT(*) FILTER (WHERE cr.conflict_starter_id = ci.person1_id AND cr.has_response = 1) = 0 THEN NULL
    ELSE ROUND(
      100.0 * COUNT(*) FILTER (
        WHERE cr.conflict_starter_id = ci.person1_id
          AND cr.has_response = 1
          AND cr.has_escalation = 0
      )::numeric /
      NULLIF(COUNT(*) FILTER (WHERE cr.conflict_starter_id = ci.person1_id AND cr.has_response = 1), 0)::numeric,
      1
    )
  END AS person2_repair_rate,

  -- Person 2 starts conflict, Person 1's repair rate
  COUNT(*) FILTER (WHERE cr.conflict_starter_id = ci.person2_id) as person2_conflicts_introduced,
  CASE
    WHEN COUNT(*) FILTER (WHERE cr.conflict_starter_id = ci.person2_id AND cr.has_response = 1) = 0 THEN NULL
    ELSE ROUND(
      100.0 * COUNT(*) FILTER (
        WHERE cr.conflict_starter_id = ci.person2_id
          AND cr.has_response = 1
          AND cr.has_escalation = 0
      )::numeric /
      NULLIF(COUNT(*) FILTER (WHERE cr.conflict_starter_id = ci.person2_id AND cr.has_response = 1), 0)::numeric,
      1
    )
  END AS person1_repair_rate,

  75 AS healthy_repair_threshold

FROM couple_info ci
LEFT JOIN conflict_responses cr ON cr.person1_id = ci.person1_id AND cr.person2_id = ci.person2_id
GROUP BY ci.person1_name, ci.person2_name;
```

### Interpretation

**Repair rate shows how well partners handle conflict:**
- **High repair rate (≥75%)**: Partner can receive conflict without escalating, good emotional regulation
- **Low repair rate (<75%)**: Partner tends to escalate conflicts, highly defensive behavior
- **NULL repair rate**: No conflicts with responses in time window

**What the numbers mean:**
- `person1_conflicts_introduced`: How many conflicts Person 1 started
- `person2_repair_rate`: When Person 1 starts conflict, % of time Person 2 doesn't escalate
- `person2_conflicts_introduced`: How many conflicts Person 2 started
- `person1_repair_rate`: When Person 2 starts conflict, % of time Person 1 doesn't escalate

## Example SQL: Affect Distribution for a Couple

**Affect Distribution** shows which specific affects appear most frequently for each partner. This helps identify patterns beyond just positive/negative ratios.

```sql
-- Affect distribution for both people in a partnership for the last 56 days
-- Replace {{person_id}} with either partner's person_id
-- Shows counts of each affect type per person

WITH couple AS (
  SELECT
    c.id AS conversation_id,
    MIN(cp.person_id) AS person1_id,
    MAX(CASE WHEN cp.person_id = (SELECT MIN(person_id) FROM conversation_participant WHERE conversation_id = c.id AND role = 'MEMBER')
      THEN p.name END) AS person1_name,
    MAX(cp.person_id) AS person2_id,
    MAX(CASE WHEN cp.person_id = (SELECT MAX(person_id) FROM conversation_participant WHERE conversation_id = c.id AND role = 'MEMBER')
      THEN p.name END) AS person2_name
  FROM conversation c
  JOIN conversation_participant cp ON cp.conversation_id = c.id
  JOIN persons p ON cp.person_id = p.id
  WHERE c.type = 'GROUP'
    AND cp.role = 'MEMBER'
    AND {{person_id}} IN (
      SELECT person_id
      FROM conversation_participant
      WHERE conversation_id = c.id
    )
  GROUP BY c.id
  HAVING COUNT(DISTINCT cp.person_id) = 2
  LIMIT 1
),
filtered_messages AS (
  SELECT
    m.id,
    pc.person_id
  FROM message m
  JOIN couple cp ON m.conversation_id = cp.conversation_id
  JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
  WHERE m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days'
    AND m.provider_timestamp < CURRENT_DATE
),
affect_counts AS (
  SELECT
    me.affect,
    COUNT(CASE WHEN fm.person_id = cp.person1_id THEN 1 END) AS person1_count,
    COUNT(CASE WHEN fm.person_id = cp.person2_id THEN 1 END) AS person2_count
  FROM filtered_messages fm
  JOIN message_enrichment me ON me.message_id = fm.id
  CROSS JOIN couple cp
  WHERE me.affect IS NOT NULL
    AND me.affect <> 'Neutral'
  GROUP BY me.affect
)
SELECT affect, person_1, person_2, partnership FROM (
  SELECT
    'name' AS affect,
    (SELECT person1_name FROM couple) AS person_1,
    (SELECT person2_name FROM couple) AS person_2,
    'Both' AS partnership,
    0 AS sort_order
  UNION ALL
  SELECT
    'Period: Last 56 days' AS affect,
    '' AS person_1,
    '' AS person_2,
    '' AS partnership,
    0 AS sort_order
  UNION ALL
  SELECT
    affect,
    person1_count::text AS person_1,
    person2_count::text AS person_2,
    (person1_count + person2_count)::text AS partnership,
    1 AS sort_order
  FROM affect_counts
) AS combined
ORDER BY
  sort_order,
  CASE
    WHEN affect IN ('name', 'Period: Last 56 days') THEN 0
    ELSE -1 * (CAST(partnership AS int))
  END;
```

### Interpretation

This query shows:
- **Each affect type** and how often each partner displays it
- **Sorted by frequency** (most common affects first)
- **Partnership total** showing combined couple patterns

**How Our Affects Map to Gottman SPAFF:**

Our system uses **Partner-prefixed affects** that directly map to Gottman's SPAFF coding:

**Positive Affects:**
- `Partner-Affection` → SPAFF: Affection
- `Partner-Validation` → SPAFF: Validation
- `Partner-Enthusiasm` → SPAFF: Joy/Interest
- `Humor` → SPAFF: Humor
- `Partner-Interest` → SPAFF: Interest

**Negative Affects:**
- `Partner-Criticism` → SPAFF: Criticism (Four Horsemen #1)
- `Partner-Contempt` → SPAFF: Contempt (Four Horsemen #2)
- `Partner-Defensiveness` → SPAFF: Defensiveness (Four Horsemen #3)
- `Stonewalling` → SPAFF: Stonewalling (Four Horsemen #4)
- `Partner-Complaint` → SPAFF: Complaint (negative but not as toxic as criticism)
- `Partner-Anger` → SPAFF: Anger
- `Partner-Sadness` → SPAFF: Sadness
- `Partner-Belligerence` → SPAFF: Belligerence/Domineering
- `Partner-Domineering` → SPAFF: Domineering
- `Partner-Fear / Tension` → SPAFF: Fear/Tension
- `Partner-Threats` → SPAFF: Threats
- `Partner-Disgust` → SPAFF: Disgust
- `Partner-Whining` → SPAFF: Whining

**Example Output:**
```
affect                    | person_1 | person_2 | partnership
--------------------------+----------+----------+-------------
name                      | Craig    | Amy      | Both
Period: Last 56 days      |          |          |
Partner-Affection         | 45       | 52       | 97
Partner-Validation        | 38       | 41       | 79
Humor                     | 31       | 28       | 59
Partner-Interest          | 22       | 25       | 47
Partner-Enthusiasm        | 18       | 20       | 38
Partner-Complaint         | 12       | 8        | 20
Partner-Criticism         | 5        | 3        | 8
Partner-Defensiveness     | 4        | 6        | 10
Partner-Sadness          | 3        | 2        | 5
Stonewalling             | 1        | 0        | 1
```

**What to look for:**
- **High positive affects** (Affection, Validation, Humor) = Healthy relationship
- **Presence of Four Horsemen** (Criticism, Contempt, Defensiveness, Stonewalling) = Warning signs
- **Contempt** appearing at all = Strongest predictor of relationship failure
- **Balance between partners** = Both should show similar positive affect patterns

## Common Ad-Hoc Queries

Beyond the standard metrics, you'll often need to write custom SQL for exploratory questions.

**Note:** For schema-related queries (finding couples by name, understanding table relationships), see the sql-reader skill's "Relationship Coaching Schema Patterns" section.

### What Did They Fight About?
```sql
-- View conflict messages with content, affect, and topic
SELECT
  m.id, m.provider_timestamp,
  p.name AS sender,
  m.content AS message_text,
  me.affect, me.conflict_state,
  me.subject, me.topic
FROM message m
JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
JOIN persons p ON pc.person_id = p.id
JOIN message_enrichment me ON me.message_id = m.id
WHERE m.conversation_id = {{conversation_id}}
  AND m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days'
  AND (
    me.conflict_state IN ('New Conflict', 'Escalation')
    OR me.affect IN ('Partner-Criticism', 'Partner-Contempt',
                     'Partner-Defensiveness', 'Stonewalling')
  )
ORDER BY m.provider_timestamp;
```

### Check Message Volume and Classification Rate
```sql
-- Diagnose low affect ratio sample sizes
SELECT
  COUNT(*) as total_messages,
  COUNT(me.id) as classified_messages,
  ROUND(100.0 * COUNT(me.id) / COUNT(*), 1) as classification_rate,
  MIN(m.provider_timestamp)::date as first_message,
  MAX(m.provider_timestamp)::date as last_message,
  MAX(m.provider_timestamp)::date - MIN(m.provider_timestamp)::date as days_span
FROM message m
LEFT JOIN message_enrichment me ON me.message_id = m.id
WHERE m.conversation_id = {{conversation_id}}
  AND m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days';
```

## Primary Workflow

1. **Identify the person or couple**: Get the `person_id` or `conversation_id`
2. **Use helper scripts for standard metrics**:
   - `affect_ratio.sh <person_id>` - Calculate affect ratio
   - `repair_rate.sh <person_id>` - Calculate repair rate
   - `affect_distribution.sh <person_id>` - View detailed breakdown
3. **Write custom SQL for exploratory questions** (what did they fight about, message volume, etc.)
4. **Interpret results**: Apply Gottman framework thresholds and check sample size warnings

## Helper Script

Create a quick helper script for common queries:

```bash
#!/bin/bash
# File: arsenal/dot-claude/skills/therapist-data-scientist/affect_ratio.sh

PERSON_ID="$1"
DAYS="${2:-56}"

if [ -z "$PERSON_ID" ]; then
  echo "Usage: $0 <person_id> [days]"
  echo "Example: $0 123 56"
  exit 1
fi

arsenal/dot-claude/skills/sql-reader/connect.sh "
-- [Paste the single person query here with \$PERSON_ID and \$DAYS variables]
"
```

## Best Practices

1. **Always use 56 days (8 weeks)** for consistency with research
2. **Check for sufficient data** - At least 20+ classified messages for reliable ratios
3. **Look at both individual and couple ratios** - Partners may have different patterns
4. **Consider temporal trends** - Run queries for different time windows to see changes
5. **Validate affect classification** - Spot-check message_enrichment.affect values

## Integration with Claude Code

When using this skill:

1. **Announce usage**: "I'm using the therapist-data-scientist skill to calculate affect ratios..."
2. **Get person_id**: Query the persons table or conversation_participant table first
3. **Run appropriate SQL**: Choose single person, couple, or breakdown query
4. **Report findings**: Share ratio, health assessment, and recommendations

## Troubleshooting

### "No rows returned"
- Verify person_id exists: `SELECT * FROM persons WHERE id = X;`
- Check if person has messages in last 56 days
- Verify message_enrichment table has affect classifications

### "affect_ratio is NULL"
- No messages with affect classifications in the time window
- Check message_enrichment.affect column for that conversation

### "Division by zero error"
- Should be handled by CASE statements, but if it occurs, check for negative_count = 0

## Example SQL: A/B Test - Intervention Impact on Affect Ratio

Compare Gottman affect ratios (positive/negative) on days with interventions vs withheld days.

**Method:** Per-user ratios → calculate delta → average across users

```sql
-- A/B Test: Affect ratio delta (SENT days vs WITHHELD days)
WITH withholding_users AS (
    SELECT p.id as person_id, p.name FROM persons p
    JOIN messages_preferences mp ON mp.person_id = p.id
    WHERE mp.withhold_interventions_enabled = true
),
user_conversations AS (
    SELECT DISTINCT wu.person_id, wu.name, cp.conversation_id
    FROM withholding_users wu
    JOIN conversation_participant cp ON cp.person_id = wu.person_id
    JOIN conversation c ON cp.conversation_id = c.id
    WHERE c.type = 'GROUP' AND cp.role = 'MEMBER'
),
day_classification AS (
    SELECT DATE(i.created_at AT TIME ZONE 'America/Los_Angeles') as the_date, m.conversation_id,
        CASE WHEN COUNT(*) FILTER (WHERE i.status = 'WITHHELD') > 0 AND COUNT(*) FILTER (WHERE i.status = 'SENT') = 0 THEN 'WITHHELD'
             WHEN COUNT(*) FILTER (WHERE i.status = 'SENT') > 0 AND COUNT(*) FILTER (WHERE i.status = 'WITHHELD') = 0 THEN 'SENT'
             ELSE 'MIXED' END as day_type
    FROM intervention i JOIN message m ON i.source_message_id = m.id
    WHERE i.created_at >= NOW() - INTERVAL '112 days'
    GROUP BY 1, 2
),
user_daily_affects AS (
    SELECT uc.name, DATE(m.provider_timestamp AT TIME ZONE 'America/Los_Angeles') as msg_date, uc.conversation_id,
        SUM(CASE WHEN me.affect IN ('Partner-Affection','Partner-Validation','Partner-Enthusiasm','Partner-Interest','Humor') THEN 1 ELSE 0 END) as pos,
        SUM(CASE WHEN me.affect IN ('Partner-Contempt','Partner-Criticism','Partner-Defensiveness','Stonewalling','Partner-Belligerence') THEN 1 ELSE 0 END) as neg
    FROM message m
    JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
    JOIN user_conversations uc ON pc.person_id = uc.person_id AND m.conversation_id = uc.conversation_id
    LEFT JOIN message_enrichment me ON me.message_id = m.id
    WHERE m.provider_timestamp >= NOW() - INTERVAL '112 days'
    GROUP BY 1, 2, 3
),
user_totals AS (
    SELECT uda.name, dc.day_type, SUM(uda.pos) as pos, SUM(uda.neg) as neg
    FROM user_daily_affects uda
    JOIN day_classification dc ON uda.msg_date = dc.the_date AND uda.conversation_id = dc.conversation_id
    WHERE dc.day_type IN ('SENT', 'WITHHELD')
    GROUP BY 1, 2
),
user_ratios AS (
    SELECT name,
        MAX(CASE WHEN day_type = 'SENT' THEN pos END) as sent_pos,
        MAX(CASE WHEN day_type = 'SENT' THEN neg END) as sent_neg,
        MAX(CASE WHEN day_type = 'WITHHELD' THEN pos END) as wh_pos,
        MAX(CASE WHEN day_type = 'WITHHELD' THEN neg END) as wh_neg
    FROM user_totals GROUP BY name
)
SELECT name,
    sent_pos || '/' || sent_neg as "sent +/-",
    wh_pos || '/' || wh_neg as "withheld +/-",
    CASE WHEN sent_neg > 0 THEN ROUND(sent_pos::numeric / sent_neg, 2) END as sent_ratio,
    CASE WHEN wh_neg > 0 THEN ROUND(wh_pos::numeric / wh_neg, 2) END as wh_ratio,
    CASE WHEN sent_neg > 0 AND wh_neg > 0 THEN ROUND((sent_pos::numeric/sent_neg) - (wh_pos::numeric/wh_neg), 2) END as delta
FROM user_ratios ORDER BY name;
```

**For average delta** (add to end of query above):
```sql
-- Replace final SELECT with:
SELECT COUNT(*) as n_users, ROUND(AVG(sent_pos::numeric/sent_neg), 2) as avg_sent_ratio,
    ROUND(AVG(wh_pos::numeric/wh_neg), 2) as avg_wh_ratio,
    ROUND(AVG((sent_pos::numeric/sent_neg) - (wh_pos::numeric/wh_neg)), 2) as avg_delta
FROM user_ratios WHERE sent_neg > 0 AND wh_neg > 0;
```

**Interpretation:** `delta > 0` means better affect ratio on intervention days. Users with 0 negatives in either condition are excluded. MIXED days (pre-Dec 2025) excluded for clean comparison.

## Further Reading

- **Gottman Institute**: https://www.gottman.com/
- **SPAFF Coding System**: Specific Affect Coding System (research manual)
- **Magic Ratio Research**: https://www.gottman.com/blog/the-magic-relationship-ratio-according-science/
