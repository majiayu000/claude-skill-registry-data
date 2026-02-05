---
name: incomplete-onboarding-assessor
description: Assess incomplete onboardings using COLD/WARM/HOT temperature model with time decay
---

# incomplete-onboarding-assessor Skill

## Purpose

Assess users who started but haven't completed onboarding, using a temperature-based engagement model with time decay. This skill helps prioritize re-engagement efforts.

**Use this skill when:**
- User asks about incomplete/abandoned/stalled onboardings
- User asks about onboarding status or progress
- User asks "who hasn't finished onboarding?"
- User asks about re-engagement priorities
- User asks to assess onboarding engagement levels

---

## Temperature Model

### Original Temperature (at time of last engagement)

| Temperature | Definition | Signals |
|-------------|------------|---------|
| **WARM** | Showed intent | Sent access code, received onboarding messages |
| **HOT** | High engagement | Engaged in exercise, shared personal info, asked questions, did demo |
| **COLD** | Explicit decline | Said "not interested", asked to stop, negative response |

**Important:** Sending an access code = WARM (not COLD). COLD only occurs after:
1. Time decay drops them to COLD, OR
2. Explicit "not interested" communication

### Time Decay Rules

Temperature decays based on days since last USER message:

| Days Silent | Decay Effect |
|-------------|--------------|
| 0-3 days | No decay (maintain original temperature) |
| 4-7 days | Drop one level (HOT→WARM, WARM stays WARM) |
| 8-14 days | Drop two levels (HOT→COLD, WARM→COLD) |
| 15+ days | All leads are COLD regardless of original |

---

## Step 1: Determine Time Window

If user specifies a time window, use it. If not, ask:

```
What time window should I assess?
- Last 7 days
- Last 14 days
- Last 30 days (recommended for full picture)
- Custom range
```

Default to **30 days** if user says "recent" or doesn't specify.

---

## Step 2: Query Incomplete Onboardings

Run this query using the **sql-reader skill**:

```sql
WITH incomplete_onboardings AS (
  SELECT
    co.id as onboarding_id,
    co.form_data->>'name' as initiator_name,
    co.form_data->>'invitee_name' as partner_name,
    co.form_data->>'relationship_goal' as relationship_goal,
    co.form_data->>'relationship_dynamic' as relationship_dynamic,
    co.created_at as onboarding_date,
    co.state as onboarding_state,
    EXTRACT(DAY FROM NOW() - co.created_at)::int as days_since_onboarding
  FROM conversation_onboarding co
  WHERE co.state IN ('INITIATOR_JOINED', 'AWAITING_PARTICIPANTS')  -- Fixed: was 'PENDING'
    AND co.created_at >= NOW() - INTERVAL '[TIME_WINDOW] days'
    AND co.form_data->>'name' IS NOT NULL
    AND co.form_data->>'name' != ''
    AND LENGTH(co.form_data->>'name') > 1  -- Filter out test users (single-letter names)
)
SELECT
  io.*,
  p.id as person_id,
  p.type as person_type,  -- Fixed: column is 'type' not 'person_type'
  MAX(m.provider_timestamp) as last_user_message,
  EXTRACT(DAY FROM NOW() - MAX(m.provider_timestamp))::int as days_since_last_msg,
  COUNT(DISTINCT m.id) as user_message_count  -- Messages sent BY the user (not Wren's messages)
FROM incomplete_onboardings io
LEFT JOIN persons p ON LOWER(p.name) = LOWER(io.initiator_name)
  AND p.type IN ('USER', 'USER_RESEARCH')  -- Fixed: moved filter to JOIN, use uppercase enum values
LEFT JOIN person_contacts pc ON pc.person_id = p.id
LEFT JOIN message m ON m.sender_person_contact_id = pc.id
  AND m.provider_timestamp >= io.onboarding_date
GROUP BY
  io.onboarding_id, io.initiator_name, io.partner_name,
  io.relationship_goal, io.relationship_dynamic, io.onboarding_date,
  io.onboarding_state, io.days_since_onboarding, p.id, p.type
ORDER BY io.onboarding_date DESC;
```

**Replace `[TIME_WINDOW]` with the number of days (e.g., 30).**

**Schema Notes (learned from execution):**
- `persons.type` column (not `person_type`) - values are uppercase: `'USER'`, `'USER_RESEARCH'`
- `conversation_onboarding.state` uses `'AWAITING_PARTICIPANTS'` (not `'PENDING'`)
- Filter test users by `LENGTH(name) > 1` to exclude single-letter names like "c" or "r"

---

## Step 3: Get Chat History for Each User

For each incomplete onboarding, fetch the 1:1 conversation history:

```sql
SELECT
  m.provider_timestamp,
  CASE WHEN m.sender_person_contact_id IS NOT NULL THEN 'user' ELSE 'wren' END as sender,
  LEFT(m.content, 200) as body  -- Fixed: use 'content' not 'body', truncate for readability
FROM message m
JOIN conversation c ON c.id = m.conversation_id
JOIN conversation_participant cp ON cp.conversation_id = c.id
JOIN person_contacts pc ON pc.id = cp.person_contact_id
JOIN persons p ON p.id = pc.person_id
WHERE pc.person_id = [PERSON_ID]  -- Use person_id from Step 2 query
  AND c.type = 'ONE_ON_ONE'  -- Fixed: was 'INDIVIDUAL'
ORDER BY m.provider_timestamp ASC
LIMIT 30;
```

**Schema Notes:**
- `message.content` is the correct column (not `body`)
- `conversation.type` uses `'ONE_ON_ONE'` for 1:1 coach conversations (not `'INDIVIDUAL'`)
- Query by `person_id` (from Step 2) rather than name match for accuracy

---

## Step 4: Assess Original Temperature

For each user, analyze their chat history to determine **original temperature**:

### WARM Signals (default for any who sent access code)
- Only access code sent
- Basic onboarding responses
- No personal sharing or questions

### HOT Signals (upgrade from WARM)
- Asked questions about how Wren works
- Requested a demo ("show me how it works")
- Shared personal relationship details
- Engaged in a coaching exercise
- Expressed curiosity ("I'm curious", "tell me more")
- Completed any reflection or exercise

### COLD Signals (explicit decline only)
- Said "not interested" or "stop"
- Asked to be removed
- Explicitly declined to continue

**Default to WARM** if unclear. Only mark COLD for explicit decline.

---

## Step 5: Apply Time Decay

Calculate **current temperature** by applying decay to original:

```python
def apply_time_decay(original_temp: str, days_silent: int) -> str:
    """Apply time decay to get current temperature."""

    TEMP_ORDER = ['COLD', 'WARM', 'HOT']

    if days_silent <= 3:
        decay_levels = 0
    elif days_silent <= 7:
        decay_levels = 1
    elif days_silent <= 14:
        decay_levels = 2
    else:  # 15+ days
        return 'COLD'  # All become COLD

    current_index = TEMP_ORDER.index(original_temp)
    new_index = max(0, current_index - decay_levels)
    return TEMP_ORDER[new_index]
```

---

## Step 6: Generate Assessment Report

Create a markdown report with this structure:

```markdown
# Incomplete Onboarding Assessment
**Date:** [Today's date]
**Time Window:** Last [X] days

## Summary

| Metric | Count |
|--------|-------|
| Total incomplete | X |
| Currently HOT | X |
| Currently WARM | X |
| Currently COLD | X |

## Priority List

### Immediate Action (HOT)
[Users still HOT - highest priority]

### High Priority (WARM or recently decayed)
[Users who are WARM or were HOT but decayed]

### Low Priority (COLD)
[Users who are COLD]

## Individual Assessments

### [User Name] — [Original Temp] → **[Current Temp]**

| Metric | Value |
|--------|-------|
| Onboarding started | [Date] ([X] days ago) |
| Last user message | [Date] ([X] days ago) |
| Days silent | [X] |
| Partner | [Partner name] |
| Goals | [relationship_dynamic] |
| User messages sent | [X] |

**Chat history summary:**
- [Key engagement points]
- [Questions asked]
- [Personal info shared]

**Recommended action:** [Light the spark / Stoke the flame / Convert]

---
```

---

## Step 7: Save and Return Results

1. Save the report to `docs/incomplete_onboarding_assessment_[DATE].md`
2. Return a summary to the user with:
   - Total counts by temperature
   - Top 3 priority users to re-engage
   - Any special cases or concerns

---

## Configurable Parameters

These values can be adjusted based on business needs:

```python
# Time decay thresholds (days)
DECAY_THRESHOLD_1 = 3   # No decay within this
DECAY_THRESHOLD_2 = 7   # Drop 1 level by this
DECAY_THRESHOLD_3 = 14  # Drop 2 levels by this
DECAY_ALL_COLD = 15     # All COLD after this

# PersonType filters (use UPPERCASE - matches database enum values)
INCLUDE_PERSON_TYPES = ['USER', 'USER_RESEARCH']  # Fixed: uppercase
EXCLUDE_PERSON_TYPES = ['TEST', 'EMPLOYEE']       # Fixed: uppercase
```

**Database Schema Reference:**
- `persons.type` column (not `person_type`) - uppercase enum values
- `conversation_onboarding.state`: `'INITIATOR_JOINED'`, `'AWAITING_PARTICIPANTS'`, `'COMPLETED'`
- `conversation.type`: `'ONE_ON_ONE'`, `'GROUP'` (not `'INDIVIDUAL'`)

---

## Recommended Actions by Temperature

| Current Temp | Action | Approach |
|--------------|--------|----------|
| **HOT** | Convert | Help craft partner invite, emphasize value |
| **WARM** | Stoke the flame | Build on what they shared, deepen conversation |
| **COLD** | Light the spark | Low-barrier CTA, ask what's holding them back |

---

## Common Violations

- **BANNED:** Marking users as COLD just because they only sent access code
  - Access code = WARM (shows intent)
- **BANNED:** Drafting nudge messages (this skill assesses only; nudges are handled by cronjob)
- **BANNED:** Including TEST or EMPLOYEE person types in assessment
- **CRITICAL:** Always check days since LAST USER MESSAGE, not just days since onboarding

---

## Special Cases

### Duplicate Name Matches
The query may return multiple rows for the same onboarding if multiple people share the same name (e.g., "Samuel", "Ryan", "Amanda"). To identify the correct person:

1. **Check message count** - The person with LOW message count (1-20) matching the onboarding timeframe is likely correct
2. **Check activity date** - Activity starting around onboarding date indicates the right person
3. **High message counts (100+)** usually indicate an ACTIVE existing user, not a stalled onboarding

**Example:** If onboarding shows "Samuel" with 3 messages (person_id 518) and another "Samuel" with 281 messages (person_id 1), the 3-message person is the incomplete onboarding. The 281-message person is an active user who happens to share the name.

**Action:** For rows with 100+ messages and recent activity, mark as "Active user - not stalled" and exclude from priority list.

### Active Users Re-onboarding
If a user appears incomplete but has recent activity in other conversations, they may be:
- Re-onboarding on a new channel (e.g., WhatsApp)
- Already engaged elsewhere

**Action:** Note as "Not actually stalled" and exclude from priority list.

### Technical Issues
If a user has no messages after receiving access code, check:
- Were onboarding messages delivered?
- Any system errors?

**Action:** Note as "Possible technical issue" for investigation.

---

## Success Criteria

You've completed this skill when:
- [ ] Queried incomplete onboardings for the specified time window
- [ ] Retrieved chat history for each user
- [ ] Assessed original temperature based on engagement signals
- [ ] Applied time decay to calculate current temperature
- [ ] Generated markdown report with individual assessments
- [ ] Saved report to docs/
- [ ] Returned summary with priority users

---

## Related Skills

- **sql-reader**: Required for database queries
- **langfuse-prompt-and-trace-debugger**: For debugging nudge delivery issues
