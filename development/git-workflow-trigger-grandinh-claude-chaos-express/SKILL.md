---
name: git-workflow-trigger
description: Natural language wrapper for git commands - automatically triggers /git:commit, /git:status, /git:push when users express git workflow intent
schema_version: 1.0
---

# git-workflow-trigger

**Type:** WRITE-CAPABLE
**DAIC Modes:** IMPLEMENT only
**Priority:** Medium

## Trigger Reference

This skill activates on:
- **Keywords:** "commit changes", "save changes", "create commit", "git status", "show changes", "push changes", "commit this", "save work", "git commit", "push to remote", "push work"
- **Intent Patterns:** `(commit|save).*?(changes|work)`, `create.*?commit`, `(show|display|check).*(changes|status)`, `push.*?(changes|to remote|work)`

From: `skill-rules.json` - git-workflow-trigger configuration

## Purpose

Automatically trigger git commands (`/git:commit`, `/git:status`, `/git:push`) when users express git workflow intent using natural language.

**Important:** This skill is classified as WRITE-CAPABLE and only triggers in IMPLEMENT mode, even for read-only operations like `git status`. This is intentional to keep git operations grouped together. If you need git status outside IMPLEMENT mode, use the `/git:status` command directly.

## Core Behavior

1. **Git Workflow Detection**
   - Detect git operations from natural language
   - Route to appropriate git command based on intent

2. **Command Routing**
   - **Commit:** "commit changes" → `/git:commit`
   - **Status:** "show changes" → `/git:status`
   - **Push:** "push changes" → `/git:push`

3. **Mode Restriction**
   - This skill only triggers in IMPLEMENT mode (WRITE-CAPABLE classification)
   - All git operations (including status) are grouped together
   - For git status outside IMPLEMENT mode, use `/git:status` directly

## Natural Language Examples

**Triggers this skill:**
- ✓ "Commit my changes"
- ✓ "Save work and commit"
- ✓ "Show my changes"
- ✓ "Push to remote"
- ✓ "Git status"

## Safety Guardrails

**WRITE-CAPABLE RULES:**
- ✓ Only write operations in IMPLEMENT mode
- ✓ Verify active task for commits
- ✓ Read operations (status) allowed in any mode
