---
name: vault-health-feedback
description: >
  Diagnose whether an Obsidian knowledge workflow produces cognitive return
  or is becoming a passive archive. Load when vault feels archival or dead.
  Do NOT use for inbox triage, link review, synthesis, or direct restructuring.
license: Apache-2.0
compatibility: opencode; requires obsidian-mcp
metadata:
  version: "4.1.0"
  last-reviewed: "2026-05-14"
  owner: r007b34r
---

# vault-health-feedback

## Constraints

- NEVER scan whole vault; sample strategically
- NEVER give more than 3 recommendations
- Check layers in order: workflow -> cognitive -> structural
- NEVER equate structural mess with system failure (check workflow first)
- NEVER repair, move, or restructure without explicit confirmation

## Trigger Boundary

**Use when:** vault feels archival, knowledge not returning, system health diagnosis needed, highest-leverage repair unclear, user says "vault is dead" or "nothing comes back."

**Do NOT use for:**
- Inbox routing -> `inbox-triage`
- Recent-note relationships -> `connection-review`
- Week-level synthesis -> `weekly-synthesis`
- Direct restructuring before diagnosis
- Promoting material -> `note-promotion`

## Boundaries

- **Owns:** workflow health diagnosis, cognitive return assessment, structural friction detection
- **Delegates to:** `inbox-triage` (root cause is inbox backlog), `opencode-context-maintenance` (root cause is context drift)
- **Never absorbs:** inbox routing, relationship analysis, synthesis, promotion, direct restructuring

## Continuations

| Condition | Next skill |
|-----------|-----------|
| Root cause is inbox backlog | `inbox-triage` |
| Root cause is context drift | `opencode-context-maintenance` |
| Vault paths inaccessible, possible config issue | `opencode-context-maintenance` |
| Vault is deeply archival, needs structural redesign | Escalate to human |

## Companion Skill

All vault operations follow `obsidian-mcp`. Forbidden: `obsidian_patch_note`, `obsidian_append_to_note`. Verify every write through readback.
## Procedure

### Phase 1: Workflow Layer (always check first)

When assessing health metrics, read `references/examples.md`.

1. `obsidian_list_notes path:"Inbox/"` -> inbox freshness (items, age)
2. `obsidian_search_notes query:"type: synthesis"` -> synthesis frequency
3. Check for recent triage/review/promotion activity
4. Score: active / stale / dead

### Phase 2: Cognitive Layer (only if workflow is active or stale)
1. Sample 5-10 recent notes for reuse signals (links back, references)
2. Check if themes recur across time windows
3. Look for notes that were never revisited after creation
4. Score: returning value / flat / declining

### Phase 3: Structural Layer (only if cognitive layer shows issues)
1. Check for orphan zones, hollow clusters, tag noise
2. Identify fragmentation patterns
3. Score: clean / messy but functional / blocking workflow

### Phase 4: Recommend

When formatting diagnosis, read `references/templates.md`.

1-3 highest-leverage interventions, ranked. Report what NOT to do now.

<details>
<summary>Health Metrics Thresholds (expand for quantitative reference)</summary>

Workflow layer:
- Inbox items >30 days old = stale signal
- Synthesis frequency <1 per month = workflow gap
- No triage activity in 2+ weeks = dead workflow

Cognitive layer:
- Reuse rate <10% of notes ever linked-to = cognitive concern
- No note revisited within 30 days of creation = flat return
- Themes never recur across windows = no compounding

Structural layer:
- Orphan rate >40% unlinked notes = structural concern
- Tag entropy >50 tags with <3 uses each = noise
- Folder depth >4 with <2 notes per leaf = over-organization

Severity ranking:
- Dead workflow > declining cognitive > structural blocking
- Stale workflow > flat cognitive > messy structural
- Active workflow with messy structure = healthy (do not intervene)

</details>
## Gotchas

### Gotcha 1: Starting from structure
**What happens:** Agent counts orphans and messy folders first
**Why it is wrong:** Structural mess may be irrelevant if workflow is healthy
**Correct approach:** Always check workflow -> cognitive -> structural in order

### Gotcha 2: Too many recommendations
**What happens:** Agent gives 5-7 improvement suggestions
**Why it is wrong:** No execution focus; user is overwhelmed
**Correct approach:** Maximum 3 interventions, ranked by leverage

### Gotcha 3: Diagnosis becomes cleanup
**What happens:** Agent starts moving/renaming/restructuring during diagnosis
**Why it is wrong:** Unauthorized modification; diagnosis should inform, not act
**Correct approach:** Report findings, recommend interventions, wait for confirmation

## Validators (CI only, not runtime)

- `validators/pre-check.sh`: Confirms vault is accessible for sampling
- `validators/post-check.sh`: Verifies <=3 recommendations and layer order respected

## Exit Criteria

- No more than 3 recommendations
- Every risk signal has evidence
- Layers checked in order (workflow -> cognitive -> structural)
- No repair executed without confirmation
