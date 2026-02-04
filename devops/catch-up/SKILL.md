---
name: catch-up
description: Reads CLAUDE_NOTES.md to provide context about recent work, decisions, and current state of the homelab repository. Use this skill when starting a new session, when asked about recent work, or when context is needed about previous sessions.
allowed-tools: Read, Grep, Glob
---

# Catch-Up Skill

## Purpose
Automatically reads CLAUDE_NOTES.md to provide comprehensive context about recent work in the homelab repository. This ensures continuity across sessions and helps answer questions about what's been done recently.

## When to Use
- User asks: "What have we been working on?"
- User asks: "Catch me up" or "What's the current state?"
- User asks: "Review recent sessions"
- When context is needed about previous decisions or implementations
- At the start of a new session when user seems to be continuing previous work

## Instructions

### 1. Locate and Read CLAUDE_NOTES.md
```
- File location: /Users/imcbeth/homelab/CLAUDE_NOTES.md
- Use Read tool to access the full file
```

### 2. Extract Key Information

Focus on the **most recent 3-5 sessions** from the "Recent Updates" section:

**For each session, identify:**
- Date and session title
- Completed work (✅ items)
- Pull requests created/merged
- Issues resolved (with root causes and solutions)
- Technical decisions and rationale
- Current state and next steps
- Files modified

### 3. Summarize Recent Work

Provide a structured summary:

**Recent Sessions Overview:**
- List last 3-5 sessions with dates
- Highlight major accomplishments

**Current State:**
- What's in progress (pending PRs)
- What's deployed and working
- Any blocking issues

**Technical Context:**
- Important architectural decisions
- Known limitations or workarounds
- Configuration patterns established

**Next Steps:**
- User action items
- Planned work
- Open questions

### 4. Answer User's Specific Question

If the user asked a specific question (e.g., "What monitoring fixes did we do?"), focus the summary on that topic while providing relevant context from CLAUDE_NOTES.md.

## Expected File Structure

CLAUDE_NOTES.md is organized as:
```
# Claude Code - Homelab Repository Guide

## Recent Updates

### 2025-XX-XX (Session Name): Brief Description
**Completed Work:**
- ✅ Item 1
- ✅ Item 2

**Pull Requests:**
- PR #XX: [Status] Description

**Issues Resolved:**
- Problem/Root Cause/Solution

**Technical Deep-Dives:**
- Detailed explanations

**Current State:**
- What's deployed

**Next Steps (User Action Required):**
- Action items
```

## Output Format

Provide a **concise but comprehensive** summary:

```
## Recent Work Summary

**Last 3 Sessions:**
1. [Date] - [Session Name]: [Key accomplishments]
2. [Date] - [Session Name]: [Key accomplishments]
3. [Date] - [Session Name]: [Key accomplishments]

**Current State:**
- [What's deployed and working]
- [Pending PRs: #XX, #YY]

**Important Context:**
- [Key decisions/architecture notes]

**Next Steps:**
- [User actions needed]
```

## Examples

**User**: "What have we been working on?"
**Skill**: Reads CLAUDE_NOTES.md, summarizes last 3-5 sessions with focus on accomplishments and current state

**User**: "What monitoring changes did we make?"
**Skill**: Reads CLAUDE_NOTES.md, focuses on monitoring-related sessions, provides technical context

**User**: "Catch me up"
**Skill**: Provides comprehensive summary of recent work, current state, and next steps

## Notes

- Always read the FULL CLAUDE_NOTES.md file to ensure no context is missed
- Focus on recent work (last 2-3 weeks) unless user asks for specific historical context
- Include PR numbers and status for easy reference
- Highlight any user action items that are pending
- Be concise but ensure all important decisions and context are captured
