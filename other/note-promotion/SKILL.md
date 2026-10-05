---
name: note-promotion
description: >
  Decide whether material should become a stable, reusable, linkable Obsidian note.
  Load when user asks to upgrade, promote, or stabilize material into a formal note.
  Do NOT use for inbox triage, link discovery, or weekly synthesis.
license: Apache-2.0
compatibility: opencode; requires obsidian-mcp
metadata:
  version: "4.1.0"
  last-reviewed: "2026-05-14"
  owner: r007b34r
---

# note-promotion

## Constraints

- NEVER promote everything; require stability + reuse + independence
- NEVER polish before deciding; score first, format only if promoting
- NEVER create notes without integration targets (minimum 2 links)
- NEVER write without user confirmation
- NEVER overwrite source voice; preserve strong original phrasing

## Trigger Boundary

**Use when:** upgrade material into formal note, decide if finding is worth preserving, turn synthesis output into stable note, create linkable knowledge unit, user says "promote" or "stabilize."

**Do NOT use for:**
- First-pass inbox routing -> `inbox-triage`
- Note relationship discovery -> `connection-review`
- Week-level meaning extraction -> `weekly-synthesis`
- Vault system health diagnosis -> `vault-health-feedback`

## Boundaries

- **Owns:** promotion decision, note type selection, integration planning, write execution
- **Delegates to:** `connection-review` (new note needs integration links), `inbox-triage` (material too raw)
- **Never absorbs:** inbox routing, relationship analysis, synthesis, health diagnosis

## Continuations

| Condition | Next skill |
|-----------|-----------|
| New promoted note needs integration links | `connection-review` |
| Material fails promotion test, return to inbox | `inbox-triage` |
| Promotion decision is ambiguous after scoring | Escalate to human |

## Companion Skill

All vault operations follow `obsidian-mcp`. Forbidden: `obsidian_patch_note`, `obsidian_append_to_note`. Verify every write through readback.
## Procedure

### Phase 1: Score

When scoring, read `references/examples.md` for promotion calibration.

Apply promotion test (>=3/5 to promote):

| Criterion | Score | Evidence required |
|-----------|-------|-------------------|
| Stable (not transient fragment) | 0/1 | Has persisted or been referenced again |
| Reusable (future value) | 0/1 | Applicable beyond original context |
| Independent (standalone) | 0/1 | Understandable without source capture |
| Connectable (links exist) | 0/1 | Can link to existing theme/project/question |
| Compression benefit | 0/1 | Clearer or more retrievable than source |

Score < 3: recommend wait / keep raw / archive.
Score >= 3: proceed to Phase 2.

### Phase 2: Type Selection

| Type | Use when |
|------|----------|
| reference-note | Stable external knowledge or method |
| idea-note | Personal framing, observation, or judgment |
| project-note | Mainly useful inside active work |
| topic-note | Multiple notes need a conceptual home |
| synthesis-note | Cross-note understanding worth preserving |
| contradiction-note | Important tension deserves explicit framing |
| question-note | The question itself is worth returning to |

### Phase 3: Plan

Define: title, tags, links (integration targets), write strategy (create new or merge into existing).

### Phase 4: Execute (after user confirmation only)

When writing promoted notes, read `references/templates.md` for note structure.

1. `obsidian_write_note overwrite:false` for new notes
2. `obsidian_replace_in_note` for merging into existing
3. Read back and verify frontmatter, content, links
<details>
<summary>Edge Cases (expand when decision is unclear)</summary>

- Material scores 3/5 but all points are weak: default to "wait" -- borderline cases benefit from time
- Material is excellent but has zero link targets: cannot promote yet; suggest creating a topic-note first
- Source is a synthesis output: check if synthesis-note type is appropriate or if the thesis deserves idea-note treatment
- Multiple candidates from same source: promote the strongest one; note others as "watch" items
- Material overlaps with existing note: merge strategy preferred over creating near-duplicates

</details>

## Gotchas

### Gotcha 1: Promoting every good idea
**What happens:** Agent marks most material as worth promoting
**Why it is wrong:** Creates hollow vault growth; promoted notes without stability become noise
**Correct approach:** Apply scoring strictly; default to "wait" when uncertain

### Gotcha 2: Promotion as polishing
**What happens:** Agent rewrites and beautifies content without deciding if promotion is warranted
**Why it is wrong:** Polishing is not promotion; a well-written fragment is still a fragment
**Correct approach:** Score first, decide promote/wait, THEN format if promoting

### Gotcha 3: Island notes without links
**What happens:** Agent creates a promoted note with no links to existing knowledge
**Why it is wrong:** Unlinked notes are undiscoverable; defeats the purpose of promotion
**Correct approach:** Require at least 2 integration targets before writing

## Validators (CI only, not runtime)

- `validators/pre-check.sh`: Confirms source material exists and is readable
- `validators/post-check.sh`: Verifies promoted note has frontmatter, >=2 links, and correct type tag

## Exit Criteria

- Promotion decision is explicit with score and per-criterion evidence
- Weak material has not been polished into fake clarity
- Integration targets are named (>=2 links)
- If written: note exists, frontmatter correct, content reads back correctly
