---
name: skill-usage-log-reviewer
description: "Audit installed Claude skills: flag unused, spot duplicates, generate deactivation checklist. Reduces context noise from skill overload. Use when portfolio grows to 10+ skills or sessions feel slow. Triggers: 'audit my skills', 'skill usage review', 'which skills to deactivate', 'аудит скилов', 'какие скилы деактивировать'."
version: 1.0.0
---

# Skill Usage Log Reviewer

This skill audits your installed Claude skill collection — identifying which skills you actively use, which are dormant, and which overlap with each other. It outputs a structured audit report with a one-click deactivation checklist, helping you keep your skill portfolio lean and your sessions fast.

**Input:**
- List of installed skill names (paste, file listing, or description)
- Optional: brief usage notes per skill ("used daily", "tried once", "never used")

**Output:**
- `skill-audit-report.md` — table with Keep / Review / Deactivate verdicts, reasoning, and a deactivation checklist

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Collect the Skill List

1. Check if Claude can see the installed skills from the conversation context (e.g., available_skills list or plugin manifest). If yes — use it directly; do not ask the user.
2. If not available from context: ask the user to provide their skill list.
   - Accepted formats: pasted names, `ls` output from skill folder, plugin manifest text, or free-form description
3. Validate input is non-empty.
   - If empty: stop and respond — "No skills listed. Please paste your installed skill names, or describe which skills you have active in Claude."
4. Check if input looks like a conversation transcript or unrelated text (no skill names detectable):
   - If detected: stop and respond — "This doesn't look like a skill list. Please provide the names of your installed Claude skills."

---

### Step 2: Collect Usage Context

1. Check if the user already provided usage notes alongside the skill list (e.g., "skill-x — used daily", "skill-y — never tried").
   - If usage notes are present for all skills: skip to Step 3.
2. If usage notes are absent or partial: gather usage context with targeted questions.
   - Group skills into batches of 5–8 and ask: "For each skill below, tell me roughly how often you use it: daily / weekly / monthly / never."
   - Do not ask per-skill individually — batch questions to reduce friction.
3. If the user declines to answer usage questions: default all skills to "Unknown" and note this in the report; still run the duplicate detection step.

---

### Step 3: Classify Each Skill

For each skill, assign a usage tier based on answers:

| Usage frequency | Tier |
|----------------|------|
| Daily or several times a week | **Active** |
| Once or twice a month | **Occasional** |
| Never used, tried once, or not sure | **Unused** |
| Frequency unknown (user didn't answer) | **Unknown** |

---

### Step 4: Detect Functional Duplicates

1. Compare skill names and descriptions (use the spec descriptions if visible; otherwise infer from names).
2. Identify pairs or groups of skills with overlapping core intent:
   - Example duplicates: `meeting-prep-briefer` + `one-to-one-prep` (both prepare for meetings)
   - Example non-duplicates: `team-update-aggregator` + `stakeholder-adapter` (aggregation vs. formatting)
3. For each duplicate pair:
   - Flag the lower-value skill (e.g., less specific, less used) as a duplicate candidate.
   - Note the overlap reason in the Reason column of the audit table.

---

### Step 5: Assign Audit Verdict

Apply this decision logic per skill:

| Condition | Verdict |
|-----------|---------|
| Active usage | ✅ Keep |
| Occasional usage + unique functionality | ✅ Keep |
| Occasional usage + overlaps with another skill | ⚠️ Review |
| Unused + unique functionality | ⚠️ Review |
| Unused + functional duplicate | ❌ Deactivate |
| Unused for 30+ days (confirmed) | ❌ Deactivate |
| Unknown usage + strong duplicate detected | ⚠️ Review |

---

### Step 6: Generate Audit Report

1. Compile results into `skill-audit-report.md` using the Output Format below.
2. Summary stats: total skills audited, Keep / Review / Deactivate counts.
3. Audit table: one row per skill, sorted by verdict (Deactivate first, then Review, then Keep).
4. Deactivation checklist: list all ❌ Deactivate skills as unchecked items.
5. Notes section: flag any collection-level observations (e.g., "4 meeting-prep skills detected — consider consolidating to 1–2").
6. If file system access available (Cowork mode): save as `skill-audit-report.md` in the workspace folder and confirm path.
7. If no file system access: display full output inline in chat.

**Edge Cases:**
- Small collection (≤5 skills): complete audit normally; add note "Your collection is small — deactivating is optional. Focus on keeping only what you actually trigger."
- All skills Active: confirm collection is healthy; output table with all Keep verdicts + "No action needed."
- Duplicate pair detected but both marked Active: set both to ✅ Keep, add observation in Notes: "Both are active — consider which covers more of your use case long-term."

---

## Negative Cases

- **Empty input:** Stop — "No skills listed. Please paste your installed skill names, or describe which skills you have active in Claude."
- **Input is a conversation log or unrelated text:** Stop — "This doesn't look like a skill list. Please provide the names of your installed Claude skills."
- **User provides plugin bundle names only (not individual skills):** Respond — "These look like plugin names. For a detailed audit, list the individual skill names within each plugin (e.g., 'skill-spec-writer', not 'skill-builder'). You can list plugin names and I'll do a coarser audit."

---

## Output Format

```markdown
# Skill Audit Report
**Date:** YYYY-MM-DD
**Total skills audited:** N
**Keep:** X | **Review:** Y | **Deactivate:** Z

---

## Summary

[1–2 sentences: overall collection health and main recommended action]

---

## Audit Table

| Skill | Verdict | Reason |
|-------|---------|--------|
| skill-name | ❌ Deactivate | Not used in 30+ days; duplicate of skill-y |
| skill-name | ⚠️ Review | Used once; overlaps with skill-z |
| skill-name | ✅ Keep | Used weekly for meeting prep |

---

## Deactivation Checklist

Skills recommended for deactivation — go to Claude settings and remove each:

- [ ] skill-name — reason: not used in 30+ days; duplicate of skill-y
- [ ] skill-name — reason: never triggered; functionality covered by skill-z

*(If no deactivations: "No skills recommended for deactivation.")*

---

## Notes

[Collection-level observations, e.g., "3 meeting-prep skills detected — consider consolidating"]
```

**Field rules:**
- Verdict uses emoji prefix: ✅ Keep / ⚠️ Review / ❌ Deactivate
- Reason column: ≤15 words, specific (not generic like "not needed")
- Audit table sorted: ❌ first, then ⚠️, then ✅
- Deactivation Checklist: only ❌ Deactivate verdicts appear here
- Notes section: always present; "No additional observations." if nothing to flag
