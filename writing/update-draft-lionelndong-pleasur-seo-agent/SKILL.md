---
name: update-draft
description: Consolidate all update audits (claims, product-mentions, topic-gaps) into a single revised article. Preserves the original voice; applies only the audited changes.
allowed-tools: Read, Write, Glob
---

# Update Draft Skill

Take the original article + all the audit recommendations and produce one consolidated updated draft. The goal is **surgical update**, not rewrite.

## Input

`/update-draft <slug>`

Reads:
- `content-pipeline/updates/1-extracted/{slug}.md` (original article)
- `content-pipeline/updates/0-guidance/{slug}.md` (priorities)
- `content-pipeline/updates/2-update-claims/{slug}.md` (if exists)
- `content-pipeline/updates/3-update-product-mentions/{slug}.md` (if exists)
- `content-pipeline/updates/4-update-topic-gaps/{slug}.md` (if exists)
- `content-pipeline/0-context/{slug}.md` (if user provided context)
- `brand-config.md`
- `examples/` (2 articles for voice — same as `/draft`)
- `.claude/skills/draft/references/voice-guide.md`

## Process

1. **Read the original article body** from the extract.
2. **Read all available audits.** Each audit gives you a queue of specific changes.
3. **Read 2 articles from `examples/`** to anchor voice — voice should match the original article AND the brand examples.
4. **Apply changes in this order, preserving original prose where untouched:**

   **Step A — Apply claim updates.** For each replacement in `2-update-claims`:
   - Find the original sentence in the body
   - Replace with the proposed rewrite (which already has the new value + new source link)
   - Don't touch surrounding prose

   **Step B — Apply product mention additions.** For each addition in `3-update-product-mentions`:
   - Find the proposed insertion section
   - Insert the suggested text using the appropriate annotation (walkthrough / inline / tip box)
   - Match the surrounding paragraph's rhythm

   **Step C — Apply topic gap additions.** For each gap in `4-update-topic-gaps`:
   - Insert the proposed H2 at the specified location
   - Draft the section using the audit's key points + evidence
   - Apply BLUF + voice rules from `voice-guide.md`
   - Match existing section length conventions (don't insert a 1500-word monster between two 300-word sections)

   **Step D — Apply removals.** If `4-update-topic-gaps` flagged sections for removal AND the user's context confirms removal is desired, cut them. Otherwise leave alone — removal is destructive and benefits from explicit user confirmation.

   **Step E — Refresh stale "last updated" date.** If the article had a date marker, update it.

5. **Self-edit pass.** Read the consolidated article end-to-end. Check:
   - Voice is consistent (no jarring tone shifts where audits inserted new content)
   - Transitions still flow (newly inserted sections need transitions in/out)
   - No duplicate content (an updated claim might collide with a new section that also discusses that data)
   - Forbidden phrases (from `brand-config.md`) absent from inserted content

6. **Save** to `content-pipeline/updates/7-updated-draft/{slug}.md`. Include a `## Editor's notes` section at the bottom listing:
   - Each change applied (one line each)
   - Each audit recommendation that was NOT applied and why
   - Anything flagged for human review

   In autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`), additionally write a copy of the editor's notes to `content-pipeline/audit/auto-edit-notes/{slug}.md` so they're available for async post-publish spot-checks even after format-for-publish strips them from the published body.

## Output

`content-pipeline/updates/7-updated-draft/{slug}.md`

The full updated article with editor's notes at the bottom.

## Quality checklist

- [ ] Every queued claim replacement was applied
- [ ] Every "high priority" product mention addition was applied
- [ ] Every "high priority" topic gap section was added
- [ ] Voice in inserted content matches original article voice
- [ ] Newly inserted sections have BLUF openers and transitions
- [ ] Editor's notes at the bottom list every change made
- [ ] No "wholesale rewrites" of sections that weren't flagged

## What NOT to do

- **Don't refactor the article.** The user asked for an update, not a rewrite. Existing prose stays unless an audit says to change it.
- **Don't add new claims.** If audits didn't surface a new stat, don't sneak one in.
- **Don't change section ordering** unless an audit recommends it.
- **Don't change the H1 / title** unless explicitly requested in user context.

## When the audits conflict

Rare, but happens — e.g., topic-gaps recommends removing a section that product-mentions just added a product to. Resolve by:
- Checking which audit had higher priority in the guidance file
- Defaulting to keeping content rather than removing
- Noting the conflict in editor's notes for the human to decide
