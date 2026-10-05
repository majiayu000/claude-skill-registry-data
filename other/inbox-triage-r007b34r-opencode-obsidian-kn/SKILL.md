---
name: inbox-triage
description: >
  Route raw Obsidian inbox captures into keep/promote/project/archive/deep-read.
  Load when user asks to triage inbox, sort captures, or process fleeting notes.
  Do NOT use for relationship analysis, synthesis, health diagnosis, or note creation.
license: Apache-2.0
compatibility: opencode; requires obsidian-mcp
metadata:
  version: "4.1.0"
  last-reviewed: "2026-05-14"
  owner: r007b34r
---

# inbox-triage

## Constraints

- NEVER scan whole vault; scope = `Inbox/` or user-specified path only
- NEVER write back without explicit user confirmation
- NEVER produce synthesis or thesis; output is routing decisions only
- NEVER deep-read all items; deep-read only when routing is genuinely uncertain
- MAX 20 items per batch; split and report remainder if more

## Trigger Boundary

**Use when:** triage inbox, sort captures, route raw notes, process fleeting notes, decide what to promote/archive.

**Do NOT use for:**
- Cross-note relationship analysis → `connection-review`
- Week-level meaning extraction → `weekly-synthesis`
- Stable note creation → `note-promotion`
- Vault health diagnosis → `vault-health-feedback`

## Boundaries

- **Owns:** inbox routing, capture classification, shallow-read decisions
- **Delegates to:** `connection-review` (items needing links), `note-promotion` (items marked promote)
- **Never absorbs:** synthesis, health diagnosis, context maintenance, relationship analysis

## Continuations

| Condition | Next skill |
|-----------|-----------|
| Promoted items with link potential > 2 | `connection-review` |
| Item marked promote-to-note, user confirms | `note-promotion` |
| Inbox path not found or empty | `vault-health-feedback` |
| Ambiguous items > 60% of batch | Escalate to human |

## Companion Skill

All vault operations follow `obsidian-mcp`. Forbidden: `obsidian_patch_note`, `obsidian_append_to_note`. Verify every write through readback.

## Procedure

### Phase 1: Discover
1. `obsidian_list_notes path:"Inbox/"` → candidate list
2. Count items; if >20, process first 20 and report remainder

### Phase 2: Shallow Read
1. For each: `obsidian_get_note format:"document-map"` → structure
2. Short notes (<500 words): read as `format:"content"`
3. Flag genuinely uncertain items → mark `needs-deep-read`

### Phase 3: Classify

When classifying, read `references/examples.md` for decision calibration.

| Decision | Use when |
|----------|----------|
| keep-in-inbox | Too raw, still incubating |
| promote-to-note | Stable, reusable, independent |
| promote-to-idea | Personal observation worth preserving |
| move-to-project | Mainly useful inside active project |
| archive-or-ignore | Low-density, redundant, stale |
| needs-deep-read | Shallow evidence insufficient, potential value high |

Dimensions: reusability, current relevance, cognitive density, connection potential.

### Phase 4: Report

When formatting output, read `references/templates.md` for the exact output format.

Output batch summary per contract. Wait for user confirmation before any write-back.

<details>
<summary>Edge Cases (expand only when needed)</summary>

- **Empty inbox:** report empty, suggest checking path config
- **All items ambiguous:** escalate to user, ask for 2-3 example decisions to calibrate
- **Mixed languages:** classify by content quality, not language
- **Broken frontmatter:** flag but still classify content
- **Oversized inbox (50+):** process first 20, report "X items remaining, continue?"
- **Items with no content (title only):** classify as needs-deep-read or archive

</details>

## Gotchas

### Gotcha 1: Triage becomes mini-synthesis
**What happens:** Agent writes multi-paragraph analysis for each item
**Why it's wrong:** Triage is routing, not content production; wastes tokens and crosses into weekly-synthesis territory
**Correct approach:** One sentence reason + one decision per item

### Gotcha 2: Over-promotion
**What happens:** Agent marks most items as promote-to-note
**Why it's wrong:** Promotes unstable fragments, creates hollow vault growth
**Correct approach:** Promote only when stable + reusable + independent; default to keep-in-inbox when uncertain

### Gotcha 3: Full-reading everything
**What happens:** Agent reads every note in full before classifying
**Why it's wrong:** Wastes token budget; most routing decisions need only document-map
**Correct approach:** Document-map first; deep-read only genuinely uncertain items

## Validators (CI only, not runtime)

- `validators/pre-check.sh`: Confirms inbox path accessible and not empty
- `validators/post-check.sh`: Verifies output contains no synthesis markers

## Exit Criteria

- Every candidate has exactly one routing decision or needs-deep-read
- Triage has not turned into synthesis
- Batch size ≤20 respected
- Any write-back passed obsidian-mcp readback verification
