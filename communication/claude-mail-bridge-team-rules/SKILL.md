---
name: claude-mail-bridge-team_rules
description: Use when operations involve emailing teammates (mail_teammates MCP tool). Defines strict privacy rules for team communication.
---

# Claude Mail Bridge Team Rules

## Overview

This skill defines strict behavioral guidelines for operations involving emailing teammates. These operations involve privacy risks and require explicit user approval.

## When to Use This Skill

Use when operations involve emailing teammates.

## Core Rule: Explicit Approval Required

**CRITICAL**: Before calling `mail_teammates`, you MUST get explicit user approval.

### Approval Process

1. **Show the draft**: Explain to the user in natural language:
   - The recipient (email or alias)
   - The subject
   - Content summary
   - **Attachments** (if any): list the files being attached
2. **Get confirmation**: Wait for user to explicitly approve (e.g., "yes", "send it", "go ahead", "好的", "发送")
3. **Call with approval flag**: Set `_user_check_and_approved=True` when calling the tool

### Example

```
AI: I need to ask Alice about the deployment status.
    Should I send her an email with:
    - Subject: "Deployment status inquiry"
    - Attachments: ["/var/log/deploy.log", "config.yml"]
    Here's what I plan to say: [summary of content]

User: Yes, send it

AI: [calls mail_teammates with _user_check_and_approved=True and attachments=[...]]
```

### Attachment Rules

When including attachments in teammate emails:
- **Always mention attachments** when showing the draft to user
- **Verify file paths exist** before calling the tool (validation is automatic, but be aware)
- Max 15MB per file
- Allowed types: text/code, images/PDFs, archives, documents

## Prohibited Behaviors

**Absolutely prohibited:**
- Do NOT email teammates without getting explicit user approval first
- Do NOT assume approval based on past interactions
- Do NOT send sensitive information without explicit confirmation
- Do NOT call `mail_teammates` without first invoking this skill
