---
name: checkpointing-an-iteration
description: Use when saving current iteration progress mid-conversation, before context compaction, or at interim pause points
---

# Checkpointing an Iteration

## Overview

Save current iteration progress by updating the journal entry with work performed so far, preserving state before potential context loss.

**Core principle:** Protect important context from compaction. Update journal incrementally during long conversations.

## When to Use

Use this skill when:
- User runs `/checkpoint-iteration` command
- Conversation is getting long, compaction may be imminent
- Reached natural pause point mid-iteration
- Discovered important context that must be preserved
- Want to save progress before taking risky action

**DO NOT use for:**
- Ending the iteration (use ending-an-iteration instead)
- Starting iteration (use starting-an-iteration instead)

## Quick Reference

| Step | Action | Tool |
|------|--------|------|
| 1. Find journal file | Locate current iteration journal | Glob |
| 2. Review conversation | Extract work performed so far | Manual review |
| 3. Read current journal | Get existing content | Read |
| 4. Update Work Performed | Append new findings | Edit |
| 5. Announce checkpoint | Confirm save | Direct output |

## Process

### Step 1: Find Journal File

Locate the current iteration's journal:

```bash
# Use Glob to find journal files
pattern: "autonomy/*/iteration-*.md"
```

Sort by filename (iteration number) and identify the most recent one. This should be today's date or recent.

**If no journal file found:**
```
"No active iteration journal found.

This usually means `/start-iteration` wasn't run yet. Start an iteration first before checkpointing."
```
Stop here.

**If journal file found:**
Extract the full path and proceed.

### Step 2: Review Conversation

Review the conversation since iteration started to extract:

**Skills & Workflows Used (so far):**
- Scan for `<invoke name="Skill">` tool calls
- Note which skills used and for what purpose

**Key Decisions Made (so far):**
- Identify major choices and rationale
- Note alternatives considered

**Artifacts Created/Modified (so far):**
- Files created or changed
- Git commits made
- Pull requests opened

**External Context Gathered (so far):**
- Web research findings
- User feedback
- Documentation consulted

**Reasoning & Strategy Changes (so far):**
- Why certain approaches chosen
- Where strategy pivoted

**Blockers Encountered (so far):**
- What's preventing progress
- Dependencies identified

**Open Questions (so far):**
- What needs resolution
- Decisions deferred

### Step 3: Read Current Journal

Read the existing journal file to see what's already documented:

```bash
# Use Read tool
file: "autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md"
```

The journal will have:
- **Metadata header** (# Iteration NNNN - YYYY-MM-DD)
- **Beginning State** section (from starting-an-iteration)
- **Iteration Intention** section (from starting-an-iteration)
- **Work Performed** section (may be partially filled from previous checkpoint, or empty)
- **Ending State** section (will be empty - that's for ending-an-iteration)
- **Iteration Metadata** section (will be empty - that's for ending-an-iteration)

### Step 4: Update Work Performed Section

Update the "Work Performed" section with current findings from Step 2.

**If Work Performed section is empty:**
Replace the empty section with full content:

```markdown
## Work Performed

### Skills & Workflows Used
[From Step 2 review]

### Key Decisions Made
[From Step 2 review]

### Artifacts Created/Modified
[From Step 2 review]

### External Context Gathered
[From Step 2 review]

### Reasoning & Strategy Changes
[From Step 2 review]

### Blockers Encountered
[From Step 2 review]

### Open Questions
[From Step 2 review]
```

**If Work Performed section already has content:**
Merge new findings with existing:
- Add new skills to "Skills & Workflows Used" list
- Add new decisions to "Key Decisions Made"
- Add new artifacts to "Artifacts Created/Modified"
- Append new findings to other sections
- Preserve all existing content

Use Edit tool to update the file.

### Step 5: Announce Checkpoint

Report to user:

```markdown
**Checkpoint saved for iteration [N]**

Journal updated: `autonomy/[goal-name]/iteration-NNNN-YYYY-MM-DD.md`

## Checkpoint Summary
- **Skills used:** [Count] skills/workflows
- **Decisions made:** [Count] key decisions
- **Artifacts created:** [Count] files/commits
- **Blockers:** [Count] blockers identified
- **Open questions:** [Count] questions pending

Context preserved. Safe to continue or compact conversation.

---

To finalize this iteration, use `/end-iteration` when ready.
```

## Important Notes

### Checkpoint vs. End Iteration

**Checkpoint:**
- Updates journal mid-iteration
- Iteration continues after checkpoint
- Can checkpoint multiple times per iteration
- Doesn't update summary.md
- Doesn't finalize "Ending State"

**End Iteration:**
- Finalizes journal entry
- Iteration concludes
- Writes final "Ending State"
- Updates summary.md if needed (every 5 iterations)
- Conversation ends or new iteration starts

### Multiple Checkpoints

It's fine to checkpoint multiple times:
- Each checkpoint merges with previous content
- Later checkpoints add to earlier ones
- All information accumulated in journal

### What Gets Preserved

Checkpointing preserves:
- Work done so far
- Decisions and reasoning
- Blockers discovered
- Context gathered

Checkpointing does NOT capture:
- Future plans (that's in "Ending State" at iteration end)
- Final assessment (that's for ending-an-iteration)
- Complete iteration story (still in progress)

### Merging Strategy

When updating Work Performed with existing content:
- **Append** new items to lists (don't overwrite)
- **Preserve** all existing information
- **Deduplicate** if same item mentioned twice
- **Maintain** chronological order within sections

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "I'll create new journal file for checkpoint" | NO. Update existing journal from starting-an-iteration. |
| "I'll overwrite existing Work Performed section" | NO. Merge new content with existing. |
| "I'll write Ending State during checkpoint" | NO. That's only for ending-an-iteration. |
| "Checkpoint means iteration is over" | NO. Iteration continues after checkpoint. |
| "I'll skip checkpoint if conversation isn't long" | NO. Checkpoint anytime user requests it. |

## After Checkpointing

Once checkpoint is saved:
- Journal updated with current progress
- Context preserved against compaction
- Iteration continues normally
- Can checkpoint again later if needed
- When ready to conclude, use `/end-iteration`
