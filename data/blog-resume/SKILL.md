---
name: blog-resume
description: |
  Resume work on blog posts - both in-progress drafts and published posts needing updates. Restores context when returning to continue work.
  Trigger phrases: "resume", "continue", "work on", "update post", "continue working", "resume post", "continue post"
allowed-tools: Read, Grep
---

# Resume Blog Post Work

## When to Use
- "Continue working on X post"
- "Let's update the Y post"
- "Resume the draft about Z"
- References any specific post file

## Workflow

### 1. Load and Classify
- Read the current state of the post
- Determine type: 
  - **Draft** (has `TODO(@` markers or `draft: true`)
  - **Published** (complete, no TODOs)

### 2. For DRAFT Posts

**Assess completion:**
- Count remaining `TODO(@fabio):` markers
- Identify sections with content vs placeholders
- Note what's written vs what's outlined

**Check for accumulated notes:**
- If draft has lots of detailed notes/changelogs from previous sessions
- Consider reorganizing with `<details><summary>` blocks
- Collapse reference material, detailed logs, iteration notes
- Keep main structure clean with TODOs for narrative writing
- Example: "Detailed iteration changelog" → collapsed, leaving just outcome visible

**Search conversation history** (if helpful):
- Use `conversation_search` to find prior discussions
- Look for: decisions made, angles explored, context
- Keep it light - don't overweight old conversations

**Summarize status:**
```
## Status Check: [Post Title]

**Completed:**
- Section X with personal experience
- Section Y technical explanation

**Still TODO:**
- Section Z (needs main content)
- Frontmatter: SEO description
- Conclusion

**From previous chat (if relevant):**
- Decided to focus on X angle
- Wanted to be honest about Y limitation

**Suggested next:** Write the Z section based on actual usage
```

### 3. For PUBLISHED Posts (Updates)

**Understand the update:**
- Ask what's changing: new section? correction? update?
- Identify where in post it fits
- Suggest structure for the update

**Update patterns - two approaches:**

**Inline updates (preferred for corrections/evolution):**
```markdown
<s>Old information that's no longer accurate</s>
_**UPDATE**: As of version X, this now works differently because...
```

**Updates section (for substantial additions):**
```markdown
## Updates

### October 30, 2025
Brief summary of what changed and why. Keep it conversational
and honest about what you learned or what broke.
```

Use inline updates when showing evolution of thinking in context. Use Updates section for substantial new content that doesn't fit inline.

**Update plan:**
```
## Update Plan: [Post Title]

**What's changing:**
[Brief description]

**Where it fits:**
- New section after § "Current Section"
- OR update to existing § "Section Name"
- OR new "Updates" section at end

**Next:** [Specific action - write update, review change, etc.]
```

### 4. Propose Next Action

For drafts:
- Which section needs writing next?
- Should we review what's written?
- Any decisions needed before continuing?

For updates:
- Where should this content go?
- Write it now or discuss approach first?
- Need to fact-check anything?

## Anti-patterns
- Don't write content without discussion
- Don't assume what updates should say
- Do reference past chats lightly, not rigidly
- Don't force updates into "Updates" section if it makes more sense inline

## Example: Resuming a Draft

```
I've loaded your draft "Refactoring My Blog Workflow with Claude Skills"

**Status:**
✅ Structure is solid with all major sections outlined
✅ Frontmatter complete except description
⏳ All sections are TODO placeholders waiting for your content

**From our earlier chat:**
You're exploring Skills because you're curious, hoping for better 
collaboration flow, but worried about AI slop problem.

**Suggested next:** 
Start with "Why bother?" section - write about what wasn't working 
with the monolithic CLAUDE.md approach. What made you think 
"there's a better way"?

Ready to work on that section?
```

## Example: Updating Published Post

```
You want to update the VirtualBox post with new findings.

**Current post structure:**
- Main content about desktop VM setup
- Has an "Updates" section already (October 30, 2025)

**Options for your new update:**
1. Add new entry to Updates section with date
2. Update inline if it's a correction to existing content
3. New section if it's substantial new information

What kind of update is this - new finding, correction, or additional technique?
```
