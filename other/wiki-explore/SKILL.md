---
skill_id: wiki-explore
name: Wiki Explore
description: "Review and verify unverified wiki pages — \"review unverified pages\", \"verify wiki content\", verification pass, after a major ingest cycle, before content release. The gate that turns AI-generated knowledge into trusted knowledge."
version: 1.0.0
category: knowledge-management
type: human-in-loop
frameworks:
  - llm-wikid-pattern
  - human-in-the-loop-verification
triggers:
  - "review unverified pages"
  - "verify wiki content"
  - regular verification pass
  - after major ingest cycle
  - before content release
collaborates_with:
  - wiki-ingest
  - wiki-query
  - wiki-lint
  - memory-palace
ethics_required: false
priority: medium
tags: [knowledge, verification, mempalace, human-in-loop]
created: 2026-04-16
updated: 2026-04-16
---

# Wiki Explore

## Purpose

Present unverified wiki pages (`explored: false`) for human review and confirmation. The verification gate that turns AI-generated knowledge into trusted wiki content.

The wiki self-expands via `wiki-ingest`, but Maxim never publishes content that depends on `explored: false` pages alone. `wiki-explore` is the loop that closes that gap.

## When To Invoke

- User wants to review AI-generated pages
- After a major `wiki-ingest` cycle (especially nightly batches)
- Before any major content release
- Periodic verification pass (suggested: every 1-2 weeks)

## Inputs

- `filter` (optional):
  - `topic`: only review pages matching this topic
  - `since`: only review pages created/updated since this date
  - `startup`: only review pages tagged with this startup
  - `room`: scope to a wing/room (sources/concepts/entities/syntheses)

## Workflow

1. **Find all `explored: false` pages** via MemPalace search.
2. **Sort**: most recently updated first (newest unverified content has highest review value).
3. **Apply filters** if provided.
4. **For each page**:
   a. Display the page's TLDR
   b. Display the Counter-Arguments section
   c. Display the cited Sources
   d. Ask the user: **Confirm | Edit | Skip | Delete**
   e. **On Confirm**: set `explored: true`, update `updated` date, leave confidence as-is
   f. **On Edit**: apply user's corrections inline, then set `explored: true` + bump `updated`
   g. **On Skip**: leave `explored: false`, move to next page (will appear next session)
   h. **On Delete**: remove page from MemPalace; record deletion in `log-md`
5. **Update related**: if confirmed page becomes the canonical version of a concept that had duplicates, suggest merge to other pages.
6. **Report progress** at the end.

## Interactive Display Format (per page)

```
[Page 3 of 47] Last updated: 2026-04-15

Title: Multi-Agent Handoff Patterns
Tags: [agents, architecture, governance]
Confidence: medium
Sources: raw/sources/handoff-paper.pdf, raw/clippings/multi-agent-essay.md

TLDR:
Inter-agent handoff requires explicit state transfer with status flags
(BLOCKED/PARTIAL/READY) to prevent silent failures. Maxim implements this
via .mxm-skills/agents-handoff.md.

Counter-Arguments:
- Single-agent systems avoid handoff complexity entirely (Hermes-agent thesis)
- Static handoff via files vs runtime message bus — tradeoff unresolved

Action: [C]onfirm | [E]dit | [S]kip | [D]elete | [Q]uit?
```

## Final Report Format

```
Wiki Explore Session — [YYYY-MM-DD HH:MM]
Pages reviewed: [N]
Confirmed: [N]
Edited & confirmed: [N]
Skipped: [N] (will appear next session)
Deleted: [N]
Remaining unverified: [N]

Confidence: 🟢 HIGH (full pass complete) | 🟡 MEDIUM (filtered subset) | 🔴 LOW (early exit)

Suggested next:
- Run /mxm-wiki query <topic> to test the now-verified pages
- Run /mxm-wiki lint to recheck the wiki for any new contradictions
```

## MemPalace Integration

```
# Find unverified pages
mempalace_search({
  query: "explored: false",
  wing: "wing_knowledge",
  limit: 50
})

# Update on Confirm
# (since MemPalace drawers are append-only, "update" = add a new drawer with same path,
# or use a maintenance script to rewrite frontmatter — depends on MemPalace version)

# Delete on Delete
mempalace_delete_drawer({ drawer_id: "<id>" })
```

## Maxim Behavioral Layer

- **Confidence tagging**: 🟢 HIGH on full pass | 🟡 MEDIUM on filtered subset | 🔴 LOW on early exit
- **Anti-rubber-stamp**: every page must be SHOWN to the user (TLDR + Counter-Arguments + Sources). No bulk-confirm.
- **Trust ladder**: confirmed pages move from `explored: false` to `explored: true`, unlocking citation by `wiki-query`

## Why This Skill Exists

Without `wiki-explore`, AI-generated content silently propagates as "knowledge." That's how hallucination compounds. The explored-false default + this skill is the structural fix.

## Handoff

- Confirmed pages → unlock for `wiki-query` citation
- Edited pages → notify `wiki-lint` to re-check the wiki for new contradictions
- Deleted pages → notify `wiki-ingest` to re-trigger if the source remains in `raw/`
- Patterns of consistent edits → suggest improvements to `wiki-ingest` prompts (skill-synthesizer can absorb)

## Source References

- `FINAL_RELEASE_CHANGES/Brandvoice-wiki-example.md` — wiki-explore pattern
- `documents/reference/AGENTS.md` — wiki trust levels
- `.claude/skills/wiki-ingest/SKILL.md` — produces the `explored: false` pages this skill verifies

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
