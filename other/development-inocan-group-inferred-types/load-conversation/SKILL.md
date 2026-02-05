---
name: load-conversation
description: Load the full content of a previous Claude Code conversation into current context. Use when user asks to "load conversation <uuid>" or "show me conversation <uuid>" or references loading/viewing a past conversation by its ID.
allowed-tools: Bash, Read
---

# Load Conversation Skill

Load the complete transcript of a previous Claude Code conversation, providing full context of the user-assistant dialogue and files involved.

## How to Load a Conversation

### 1. Parse the Conversation ID

Extract the conversation UUID from the user's request. It should be a UUID format like:
- `e06a3702-af08-41d7-a425-403622c2f266`
- `f792926c-99b9-44ca-8733-e9f9db276da2`

### 2. Execute the Loader Script

The loader script is located in this skill's `scripts/` directory. Execute it:

```bash
cd <skill-base-directory>/scripts && ./load-conversation.sh "<conversation-uuid>"
```

**Note:** The `<skill-base-directory>` is automatically provided by Claude Code as the base directory for this skill.

### 3. Present the Conversation

The script will output:
1. **Header**: Conversation metadata (ID, project, date, message count)
2. **Transcript**: Full conversation flow with User and Assistant messages
3. **Files Reference**: List of unique files that were read or edited during the conversation

### 4. Output Format

Present the entire output from the script to load the conversation context. The transcript format is:

```
=== CONVERSATION ===
ID: <uuid>
Project: <project-path>
Date: <timestamp>
Messages: <count>

=== TRANSCRIPT ===

[User]:
<message content>

[Assistant]:
<message content>

[User]:
<message content>

...

=== FILES ACCESSED ===

Read:
- /path/to/file1.rb
- /path/to/file2.rb

Edited:
- /path/to/file3.rb
```

## Important Notes

- The conversation file must exist at `~/.claude/projects/<encoded-path>/<uuid>.jsonl`
- If the file is not found, inform the user that the conversation doesn't exist
- The transcript includes only user and assistant messages, not tool execution details
- File references help understand which code was involved without cluttering the transcript

## Examples

**User**: "load conversation e06a3702-af08-41d7-a425-403622c2f266"
→ Execute loader script with the UUID, display full transcript

**User**: "show me what we discussed in f792926c-99b9-44ca-8733-e9f9db276da2"
→ Execute loader script with the UUID, display full transcript

**User**: "can you load the conversation from earlier where we worked on retry_before_failing?"
→ User should first use conversation-search to find the UUID, then load it
