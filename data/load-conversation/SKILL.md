---
name: load-conversation
description: Load the full content of a previous Claude Code conversation into current context. Use when user asks to "load conversation <uuid>" or "show me conversation <uuid>" or references loading/viewing a past conversation by its ID.
---

# Load Conversation

Load a past conversation by its UUID into the current context. This retrieves the full user/assistant message transcript from the conversation history database.

## Usage

The user will provide a conversation ID (UUID) in one of these formats:
- "load conversation abc123-def456-..."
- "show me conversation abc123"
- "show me that conversation" (when ID was mentioned previously)

## Instructions

1. Extract the conversation UUID from the user's request. It should be a UUID-like string (with or without dashes).

2. Run the load command:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/load-conversation/scripts/load.sh --id "CONVERSATION_UUID"
```

Replace `CONVERSATION_UUID` with the actual conversation ID from the user's request.

3. Present the conversation transcript to the user in a readable format.

4. If the conversation is not found, inform the user and suggest:
   - Verifying the conversation ID
   - Using the conversation search skill to find the correct ID

## Output

The transcript will show:
- Conversation metadata (ID, project, dates)
- Full message history with USER and CLAUDE labels
- Timestamps for each message

This allows the user to review past discussions and use them as context for the current conversation.
