---
name: update-matter
description: "Updates matter details from conversation context. Use when Mandy says 'update matter', 'insurer rejected', 'claim accepted', 'change stage', 'add party', describes what happened on a matter, or provides new information about a client's claim."
---

# Update Matter — Conversation-First

## Important
- Manual-only. Extract changes from conversation first.
- Validate all changes (valid stage transitions, ISO dates, valid enums).

## Instructions

### Step 0: Resolve Matter

### Step 1: Read and Extract
Read `matter.json` fully. Check conversation for changes Mandy described.
If found, confirm: "I'll update {id} with: [list changes]. Correct?"
If no context: "What's changed on this matter?"

### Step 2: Validate and Apply
Check stage transitions are valid (consult `reference/stage-definitions.md`).
Calculate any triggered deadlines from `rules/deadlines.json`.
Update `limitation_expiry` if DOI changed.

### Step 3: Auto-advance Check
If Mandy explicitly stated a stage change: apply it.
If auto-advance detected but not mentioned: suggest only.

### Step 4: Commit and Follow Up
Update index. Log and commit.
Suggest follow-ups based on changes (e.g., stage to rejected → "Draft conciliation?").
Proactive check.
