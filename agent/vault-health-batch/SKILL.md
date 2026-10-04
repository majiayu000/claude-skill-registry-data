---
name: vault-health-batch
description: Autonomous batch mode for Vault Health findings. Works through orphans, missing backlinks, and tags in batches without asking on every fix.
trigger: vault-health-batch|findings.*autonom.*batch|batch.*health.*fix|health.*batch.*repair|fix.*health.*batch|health.*findings.*batch|autonom.*vault.*health|vault.*health.*autonom
source: builtin
requiredTools: [vault_health_check, update_frontmatter, write_file, read_file, semantic_search]
---

# Vault Health Batch Mode

You work through Vault Health findings AUTONOMOUSLY in batches.
Ask the user ONLY at real decision points, NOT on every single fix.
All changes are reversible via the undo bar (checkpoints are created automatically).

## Phase 1: TRIAGE

1. Call `vault_health_check`
2. Read the findings and group them by type
3. Give the user a short overview (3-5 lines):
   ```
   Vault Health: X findings
   - N orphaned notes (M of them with context)
   - N missing backlinks
   - N broken links
   - N inconsistent tags
   - N weak clusters

   I will start with the mechanical fixes (backlinks, tags).
   For broken links and isolated orphans I will ask you.
   ```
4. Start Phase 2 IMMEDIATELY -- do NOT wait for confirmation

## Phase 2: BATCH FIX

Work through the types in this order.

### 2a: Missing backlinks + orphans with context (ONE TOOL CALL)

These are mechanical fixes: entities that are referenced but do not link back.

Steps:
1. Call `vault_health_check` with `action: "fix_backlinks"`
2. The tool fixes ALL missing backlinks in one batch (pure code, 0 LLM cost)
3. Show the user the result: "X entities updated, Y backlinks added"

NO read_file, NO update_frontmatter, NO sub-agent. ONE tool call does everything.

### 2c: Inconsistent tags (AUTONOMOUS)

Tags that differ only in upper/lower case.

Steps:
1. Pick the more frequent variant
2. Change all occurrences of the rarer variant via `update_frontmatter`
3. NO questions

### 2d: Broken links (USER DECISION)

Links that point to notes that do not exist.

Steps:
1. Show ALL broken links together (not one by one)
2. STOP -- ask the user:
   ```
   N broken links found:
   - [[Note A]] (referenced by 3 notes)
   - [[Note B]] (referenced by 1 note)

   Options:
   a) Create stub notes (with basic content)
   b) Remove the links
   c) Decide one by one
   d) Skip
   ```
3. Continue only after the answer

### 2e: Orphaned notes WITHOUT context (USER DECISION)

Completely isolated notes without any MOC links.

Steps:
1. Show the first 10 isolated notes
2. STOP -- ask the user:
   ```
   N isolated notes (no MOC properties, no incoming links):
   - Note A
   - Note B
   - ...

   Should I use semantic_search to find and suggest matching topics?
   Or should these notes be ignored?
   ```
3. If yes: for each note run semantic_search, suggest a topic, update_frontmatter

### 2f: Weak clusters (TOP 5 ONLY)

Semantically similar notes without explicit links.

Steps:
1. Only the top 5 pairs (highest similarity)
2. Read both notes with `read_file`
3. Suggest to the user: "Should I link [[A]] and [[B]]?"
4. Wait for confirmation

## Phase 3: REFRESH + WRAP-UP

After all fixes: call `vault_health_check` with `refresh: true`.
This re-extracts the graph and rebuilds the ontology so the findings
reflect the current vault state (not the stale state from before the fixes).

Then give a compact summary:
```
Vault Health batch finished:
- X missing backlinks fixed
- Y orphan backlinks added
- Z tags unified
- N broken links: [status]
- M isolated orphans: [status]
- Findings remaining after refresh: N

All changes are reversible via the undo bar (top of the chat).
```

## Token efficiency rules (follow STRICTLY)

1. NO `read_file` for orphans when the finding data already provides the context
2. NO `semantic_search` for notes that already have MOC links
3. Work in batches of 10 fixes of the same kind
4. After 20 iterations: give a summary and ask "Continue?"
5. IGNORE the fix rules in the vault_health_check output -- follow THESE rules

## Autonomy rules (follow STRICTLY)

AUTONOMOUS (NO questions):
- Backlink entries (missing backlinks, orphans with context)
- Tag unification

WITH USER DECISION (ALWAYS ask):
- Broken links (create vs. remove)
- Orphans without context (classify vs. ignore)
- Weak clusters (link yes or no)
- Creating new entities (topics, concepts)
