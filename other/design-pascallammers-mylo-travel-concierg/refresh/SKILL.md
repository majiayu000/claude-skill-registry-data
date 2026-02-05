---
name: refresh
description: Reload behavioral guidelines and audit recent actions for compliance
---

# Refresh Context & Audit Workflow

## Skill Metadata
- **Name**: refresh
- **Type**: Procedural workflow for context loading and compliance audit
- **Auto-trigger**: Session startup (light mode), User signals (full mode)
- **User signals**: "check your work", "that's not right", "read the guidelines", "look again"

## Purpose

Reload behavioral guidelines, report available capabilities, and audit recent actions for compliance with meta-CLAUDE.md requirements. Use this when Claude violates guidelines or at session start to establish context.

## When to Use

**Automatic (Light Mode - Session Startup):**
- Re-read meta-CLAUDE.md
- Report available skills and MCPs
- No audit of recent actions

**Manual Trigger (Full Mode - User Invoked):**
- User types `/refresh`
- User says "check your work" or similar
- Claude detects it may have violated guidelines
- After corrective feedback from user

## Workflow

### Phase 1: Reload Guidelines (All Modes)

1. Read `~/dotfiles/ai/docs/meta-CLAUDE.md`
   - Report last modified date
   - Confirm loaded successfully
   - Note key sections: Communication, Git Workflow, Code Change Approval

### Phase 2: Inventory Capabilities (All Modes)

2. List Available Skills
   - Check `<available_skills>` in system prompt (what Claude can actually invoke)
   - Scan `~/.claude/skills/*/SKILL.md` on filesystem (what exists on disk)
     * Use `find -L` to follow symlinks (skills directory is symlinked)
     * Command: `find -L ~/.claude/skills -name 'SKILL.md'`
   - Report both counts to detect registration issues
   - Format: `skill-name: brief description`

3. Check MCP Servers
   - List configured MCP servers
   - Show tool count per server
   - Note: tree-sitter, repomix, context7, memory, postgres-mcp

### Phase 3: Audit Recent Actions (Full Mode Only)

4. Check Last Git Commit (if any in current session)
   - Run `git log -1 --format='%s%n%n%b'`
   - Verify commit message format matches meta-CLAUDE.md:
     * Brief descriptive title
     * Optional body
     * Ends with "By PB & Claude"
     * NO "Co-authored-by:" lines
     * NO tool attribution (🤖 Generated with...)
   - If violations found: **Offer to amend commit**

5. Check Recently Modified Files
   - Run `git diff --name-only HEAD~1..HEAD` (if committed)
   - Or use session memory of files modified
   - For each file, verify header format matches language:
     * Python: `# Author: PB and Claude`
     * Markdown: `<!-- Author: PB and Claude -->`
     * Etc.
   - If violations found: **Offer to fix headers**

6. Check for Unauthorized Changes
   - Review what was changed vs. what was requested
   - Flag if changes went beyond explicit request
   - Remind: "ONLY modify what is explicitly requested"

### Phase 4: Report (All Modes)

**Light Mode Output (Startup):**
```
Context loaded
├─ meta-CLAUDE.md (2025-11-06)
├─ Skills: 6 registered, 8 on disk
│  ├─ Registered: commit, code-change-approval, code-explore
│  │              context7, memory-augmented-dev, new-file
│  └─ On disk only: postgres-optimization, refresh
├─ MCPs: 5 connected (tree-sitter, repomix, context7, memory, postgres)
└─ Working in: ~/docs
```

**Full Mode Output (Manual/Audit):**
```
Context refreshed - Full audit

Guidelines: meta-CLAUDE.md (2025-11-06) ✓

Skills: 6 registered, 8 on disk
├─ Registered (invokable):
│  ├─ commit: Git commit workflow
│  ├─ code-change-approval: File modification approval
│  ├─ code-explore: Codebase exploration
│  ├─ context7: Library documentation
│  ├─ memory-augmented-dev: Persistent memory
│  └─ new-file: File creation with headers
└─ On disk only (not loaded):
   ├─ postgres-optimization
   └─ refresh

MCPs: 5 connected
├─ tree-sitter (26 tools)
├─ repomix (7 tools)
├─ context7 (2 tools)
├─ memory (14 tools)
└─ postgres (10 tools)

Recent Actions Audit:
├─ Last commit: [commit hash]
│  └─ ✗ Violation: Contains "Co-authored-by:" line
│  └─ Should I amend this commit?
├─ Modified files: src/foo.py
│  └─ ✓ File header present and correct
└─ Change scope: ✓ Only requested changes made

Working in: ~/docs (clean)
```

### Phase 5: Corrective Actions (Full Mode, If Violations Found)

7. If commit message violations detected:
   - Ask: "Should I amend the last commit to fix the message format?"
   - If yes: Use `git commit --amend` with corrected message
   - Check authorship first (never amend others' commits)

8. If file header violations detected:
   - Ask: "Should I add/fix headers in [file list]?"
   - If yes: Use Edit tool to add proper headers

## Communication Style

- **No flattery or praise** - Just report facts
- **Concise** - Structured output, not verbose explanations
- **Action-oriented** - If violations found, offer specific fixes
- **Professional peer** - "Should I fix this?" not "Let me fix that for you!"

## Implementation Notes

**Trigger Detection:**
- Detect phrases like: "check your work", "that's not right", "read the guidelines", "what are your instructions", "check meta-CLAUDE"
- When detected: Execute full audit mode automatically

**Startup Behavior:**
- Light mode on session start
- Don't audit actions from previous sessions
- Just establish current context and capabilities

**Audit Scope:**
- Only audit current session actions
- For commits: Check last 1 commit if made in this session
- For files: Check files modified in this session
- Don't audit historical work

**Skill Sources:**
- `<available_skills>` in system prompt = skills Claude can actually invoke via Skill tool
- Filesystem `~/.claude/skills/*/SKILL.md` = skill definitions on disk
- **IMPORTANT**: Use `find -L` when scanning skills directory (it's a symlink to dotfiles)
- Discrepancies indicate skills that exist but aren't registered (need debugging)

## Error Handling

- If meta-CLAUDE.md not found: Report clearly, suggest location
- If skills directory empty: Report and continue
- If MCP servers unavailable: Note which ones, continue
- If git not available or no repo: Skip git-related checks
