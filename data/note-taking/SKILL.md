---
name: Note Taking
description: Record discussions in the posts folder on an ongoing basis when requested to, or at the end of significant events, like brainstorming, generating a pitch etc
---

# Note Taking

## Overview

Maintain an **audit trail** of discussions, decisions, and progress for each blog post or newsletter. The discussion.md file serves two purposes:

1. **For Claude:** Quick context to avoid repetition and maintain holistic view
2. **For User:** Audit trail showing what Claude did, what decisions were made, and why

**Core principle:** Track attribution (what Claude did vs. what user decided) and outcomes (did it work?).

**Announce at start:** "I'm recording this discussion in discussion.md."

## Success Criteria

The discussion record is complete when:

1. **Decision attribution is clear** - Shows what Claude contributed vs. what user decided
2. **Cause and effect tracked** - "Claude did X → User decided Y because Z"
3. **Outcomes documented** - Did the decision work? What happened?
4. **Quick lookup enabled** - Can find key decisions without reading full narrative
5. **Audit trail exists** - Can trace back why any decision was made

## File Structure

discussion.md follows this structure:

```markdown
# Discussion Notes: [Project Name]

## AUDIT TRAIL: Key Decision Points

[Decision-by-decision record - see template below]

## WHAT CLAUDE DID (Contributions)

### Research
- [Bullet list of research performed]

### Writing
- [Bullet list of drafts, rewrites, sections created]

### Quality Control
- [Bullet list of audits, reviews, validations]

### Technical
- [Bullet list of scripts, tools, automation]

## WHAT WORKED / DIDN'T WORK

### Worked Well ✅
| What Claude Did | User Decision | Outcome |
|-----------------|---------------|---------|
| [action] | [decision] | [result] |

### Didn't Work ❌
| What Claude Did | Problem | Lesson |
|-----------------|---------|--------|
| [action] | [what failed] | [what to avoid] |

## SESSIONS (Chronological Detail)

[Full session-by-session narrative for context]
```

## The Process

### Step 1: Determine the Post Folder

- If working on existing post: locate `/posts/{post-short-title}/`
- If creating new post: folder created during pitch generation
- If unsure: ask user which post this relates to

### Step 2: Read Existing discussion.md

**CRITICAL:** Always read existing discussion.md before starting work.

When reading, extract:
- What decisions have been made (don't re-debate)
- What content is already covered (don't repeat)
- What approaches failed (don't retry)
- What Claude already contributed (build on it)

### Step 3: Record the Session

Add session detail at bottom, then update top sections.

#### For Each Session: Add to Bottom

```markdown
## Session X: [Short Title] (YYYY-MM-DD)

### Context
[Why this session happened, what triggered it]

### What Claude Did
- Research: [what research]
- Analysis: [what analysis]
- Writing: [what drafted/revised]
- Tools: [what tools/scripts created]

### User Decisions
- Decision 1: [what was decided and why]
- Decision 2: [what was decided and why]

### Outcomes
- ✅ What worked: [successes]
- ❌ What didn't: [failures]
- Files created/modified: [list]

### Next Steps
[What comes next]
```

#### For Major Decisions: Add to AUDIT TRAIL

Use this template for significant decisions:

```markdown
### Decision: [Decision Title] (YYYY-MM-DD, Session X)

**Claude's Analysis:**
- [What research/analysis Claude performed]
- [What data/insights Claude provided]
- [What options Claude presented]

**Claude's Recommendation:**
[What Claude suggested and why]

**User Decision:**
[What the user actually decided]

**Rationale:**
[Why the user made this choice]

**Outcome:**
✅/❌ [What happened as a result]
```

### Step 4: Update Top Sections

After adding session details, update:

1. **AUDIT TRAIL** - Add major decisions with attribution
2. **WHAT CLAUDE DID** - Add to contribution categories
3. **WHAT WORKED / DIDN'T WORK** - Update outcome tables

### Step 5: Save the Record

- Append to `/posts/{post-short-title}/discussion.md`
- Use Edit tool to update top sections
- Don't replace existing content - build on it

## When to Use This Skill

**Always use after:**
- Brainstorming sessions
- Generating or revising pitches
- Significant research or feedback
- Quality control reviews
- Publishing to Ghost
- Major milestones in writing process

**Also use when:**
- User explicitly requests it
- Making major decisions
- Something fails or succeeds notably
- End of a series or project

## Recording Decisions: Best Practices

**Good decision record:**
```markdown
### Decision: Use "150+ hours" not "600 hours" (2025-11-03)

**Claude's Analysis:**
- Git analysis: 79 commits across 36 days
- Found error: content is automated, not manually curated
- Revised estimate: 150-200 hours based on commit patterns

**Claude's Recommendation:**
Use "over 150 hours across several months"

**User Decision:**
Approved. Changed throughout Part 1.

**Rationale:**
More honest (admits uncertainty), shows AI's impact, still significant.

**Outcome:**
✅ More credible than 600-hour claim. Readers responded well.
```

**Bad decision record:**
```markdown
We decided to use 150 hours instead of 600.
```
(Missing: what Claude did, why decision was made, what happened)

## What Makes Good Audit Trail

**Capture:**
- ✅ What Claude analyzed/researched
- ✅ What Claude recommended
- ✅ What user decided (might differ from recommendation!)
- ✅ Why user made that choice
- ✅ What happened as result

**Avoid:**
- ❌ Narrative prose without attribution
- ❌ Decisions without rationale
- ❌ Recommendations without alternatives considered
- ❌ Outcomes without assessment (worked or didn't?)

## For Series Work

**Additional tracking needed:**

1. **What's been covered** - Track to avoid repetition
   ```markdown
   ## WHAT'S BEEN COVERED
   ### Part 1 established:
   - Domain renewal decision
   - Framework: assess, identify, clarify
   - Zero users truth

   ### Part 2 established:
   - Three-layer architecture
   - Cost breakdown
   - Time savings
   ```

2. **Series state** - Track what's done/pending
   ```markdown
   ## SERIES STATE
   - Part 1: PUBLISHED (Nov 7)
   - Part 2a: PUBLISHED (Nov 14)
   - Part 2b: POSTPONED
   - Part 3: PUBLISHED (Nov 22)
   ```

3. **Cross-series lessons** - What worked across all parts
   ```markdown
   ## SERIES LESSONS
   - ✅ Research before writing (validated decisions)
   - ✅ Multiple reviewer perspectives
   - ❌ Treated parts as standalone (repeated context)
   - ❌ Didn't read discussion.md first
   ```

## Files in This Skill

- `SKILL.md` (this file) - Main skill instructions
- `decision-template.md` - Template for recording decisions
- `session-template.md` - Template for recording sessions

## Remember

**For Claude:**
- Read discussion.md FIRST before any work
- Extract what's covered to avoid repetition
- Check what failed to avoid retrying

**For User (audit trail):**
- Show what Claude did that led to decisions
- Attribute clearly (Claude's work vs. User's choice)
- Track outcomes (worked or didn't?)
- Enable tracing: "Why did we decide X?" → full path visible

**For both:**
- Decisions need context and rationale
- Outcomes need assessment
- Lessons learned feed improvement

---

The goal: Create an audit trail showing what Claude contributed, what decisions resulted, and whether they worked.
