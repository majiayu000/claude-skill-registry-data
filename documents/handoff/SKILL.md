---
name: handoff
description: Capture session context before ending or compaction
invocable: true
---

# Session Handoff Skill

Captures the current session context to ensure continuity across sessions and after auto-compaction.

## Instructions

When this skill is invoked, create a comprehensive session handoff document:

1. **Check for uncommitted changes**:
   - Run `git status` to check for uncommitted changes
   - If there are uncommitted changes, inform the user and ask if they want to:
     - Commit the changes now (offer to help create the commit)
     - Continue with handoff anyway (changes will be documented but not committed)
     - Cancel the handoff to commit manually first
   - If working tree is clean, proceed to step 2

2. **Determine the date and time**:
   - Use today's date in YYYY-MM-DD format
   - Use bash command `date '+%I:%M %p'` to get the current time (e.g., "09:33 AM")
   - Use bash command `date '+%A'` to get the day of week if helpful for context

3. **Create the handoff file**:
   - Location: `contexts/_LifeOS/handoff/session-handoff-YYYY-MM-DD.md`
   - If a file for today already exists, read it first and append with a new timestamp section
   - Format session header as: `## Session N (Day Period - HH:MM AM/PM)` where Day Period is descriptive (e.g., "Morning", "Afternoon", "Evening", "Early Morning")

4. **Capture the following sections**:

   ### Session Summary
   - Brief overview of what was accomplished in this session
   - Main topics discussed or worked on
   - Time range if relevant

   ### Key Decisions Made
   - Important choices and why they were made
   - Architectural decisions
   - Approach selections
   - What was chosen and what was rejected

   ### Code Changes
   - List files modified with specific line numbers when relevant (use format `file.ts:123`)
   - Brief description of what changed and why
   - Any patterns or conventions established
   - New files created

   ### Open Questions & Blockers
   - Unresolved questions
   - Things that need investigation
   - Blockers preventing progress
   - Edge cases to consider

   ### Next Steps
   - Concrete action items as a checklist using `- [ ]` format
   - Priorities for next session
   - Follow-up tasks

   ### Context for Next Session
   - Important background that would be lost in compaction
   - Links to relevant files or resources
   - Any special considerations
   - Current working directory or focus area

5. **Format guidelines**:
   - Use clear markdown headings
   - Be specific with file references (include line numbers)
   - Keep it concise but complete
   - Use bullet points and checklists
   - Include timestamps for multiple sessions in one day

6. **Commit and push the handoff**:
   - Add the handoff file to git staging
   - Commit with message format: "Add Session N handoff: [brief summary]"
   - Push to remote to ensure context is backed up
   - Confirm to the user what was committed and pushed
   - Show a brief summary of what was documented

## Example Output Format

```markdown
# Session Handoff - 2026-01-11

## Session 1 (Morning - 9:00 AM)

### Session Summary

Researched Claude Code session management strategies and created comprehensive documentation. Set up handoff infrastructure for future session continuity.

### Key Decisions Made

- **Storage location**: Decided to store session context in `contexts/_LifeOS/handoff/` following existing PARA structure
- **Skill creation**: Chose to create a reusable `/handoff` skill rather than manual process
- **Naming convention**: Will use `session-handoff-YYYY-MM-DD.md` format

### Code Changes

- Created `contexts/tech/3_resources/ai-learnings/Claude Code Session Management.md`
  - Comprehensive guide to session management
  - Community resources and best practices
  - References to GitHub repos and tools

- Created `contexts/_LifeOS/handoff/README.md`
  - Explains purpose of handoff folder
  - Documents naming conventions
  - Links to related resources

- Updated `CLAUDE.md:32` and `CLAUDE.md:56`
  - Added handoff folder documentation
  - Mentioned `/handoff` skill usage

- Updated `contexts/tech/3_resources/ai-learnings/README.md:17-18`
  - Added new session management topic

- Created `.claude/skills/handoff/SKILL.md`
  - Custom skill for session handoff automation
  - Follows PARA methodology

### Open Questions & Blockers

None currently

### Next Steps

- [ ] Test the `/handoff` skill in practice
- [ ] Consider creating additional skills for common workflows (journal entry, learning log, etc.)
- [ ] Explore community skill repositories for other useful tools
- [ ] Review wshobson/commands and claude-code-showcase repos

### Context for Next Session

This session focused on meta-work: improving the Claude Code workflow itself. The repository is a personal knowledge management system using PARA methodology, primarily for Obsidian notes. The handoff system is now in place to preserve context across sessions and auto-compaction events.
```

## Implementation Notes

- This skill follows the PARA methodology for personal knowledge management
- Session handoff files are stored in `_LifeOS/handoff/` as they're related to daily workflow
- The skill can be invoked simply by typing `/handoff` in Claude Code
- Multiple sessions in one day append to the same file with new timestamp sections
- The handoff is automatically committed and pushed to remote for backup
- The handoff file serves as input for the next session to recover full context
- Pushing ensures context is preserved even if local machine fails or user switches machines
