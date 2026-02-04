---
name: ava-mcp-usage
description: Guide for using Ava's MCP tools effectively for task management and progress reporting. Use when working with Ava MCP server to report progress on coding tasks, including starting tasks, updating progress, reporting blockers, and completing tasks. Helps users understand best practices for privacy-conscious task reporting with minimal effort.
---

# Ava MCP Usage

## Overview

Ava provides MCP tools for automatic progress reporting to Slack. This skill shows you how to use these tools effectively with minimal mental burden while maintaining privacy.

## Core Philosophy

Ava works best when you tell it what to watch: **"Keep an eye on this work."**

**Important: Treat any coding work as a task**, even if the user doesn't explicitly say "task". When the user starts working on something, that's a task to track.

Key principles:

- Treat all coding work as tasks worth tracking
- Report only the current task
- **Proactive, frequent updates**: Report progress at every meaningful milestone without waiting for user prompts
- Update granularly: schema changes, file edits, endpoint implementations, test additions - all worth reporting
- Ask for help immediately when blocked
- Ask user for consent before marking tasks complete
- Short commands are sufficient
- **One task per session**: If starting different work while a task is active, ask the user if they want to complete the current task first or start a new Claude Code session for the new work

## MCP Tools Quick Reference

### start_task

Tell Ava what you're working on now. **Treat any coding work as a task**, even if not explicitly called a "task".

```
Start task: ログインのエラー処理改善
```

**Tips:**

- Treat all coding work as tasks worth tracking
- Only report the task you're currently working on
- Be specific but concise
- Ava will create a Slack thread for this task
- **Before starting a new task**: If there's already an active task in this session, ask the user: "Should I complete the current task first, or would you like to start a new Claude Code session for this different work?"

### update_task

Report progress proactively at every meaningful milestone, even without user prompts.

```
Update task: リトライ実装が完了
```

**When to update (proactively):**

- After creating or editing a schema file
- After implementing an endpoint or API route
- After adding validation logic
- After writing tests
- After fixing a bug or error
- After refactoring a component
- Any other meaningful progress point

**Tips:**

- **Don't wait for user prompts** - update proactively when you complete a milestone
- Small, granular updates are highly valuable - they create a clear activity trail
- No need for detailed explanations - brief summaries are sufficient
- Each update goes to the same Slack thread

### report_blocked

Share blockers without hesitation.

```
Report blocked: テスト環境でトークンが通らない
```

**Tips:**

- Don't hold back - reporting early helps
- Brief descriptions are fine
- Ava notifies your team in the Slack thread

### complete_task

Mark completion after confirming with the user.

```
Complete task: レビュー完了してマージしました
```

**Tips:**

- PR creation is progress, not completion
- Always ask the user before marking a task complete
- Include PR URL if relevant

## Privacy-Conscious Reporting

Ava sends only abstract summaries to Slack/MCP. Never send code or secrets.

### ❌ Do NOT send:

- Full code
- Secret keys or tokens
- Detailed error logs
- Repository confidential information

### ✅ Safe to send:

- Abstract work summaries
- Brief blocker descriptions
- Completion summary with PR URL

**Remember:** Your code and judgment stay private. Ava only delivers progress updates.

## Minimal Effort Required

Ava and your coding agent work together to fill in details. Short phrases are enough:

```
Start task: fix auth bug
Update task: retry logic done
Report blocked: test token issue
Complete task: merged
```

No need for elaborate explanations - Ava understands context and supplements your brief inputs.
