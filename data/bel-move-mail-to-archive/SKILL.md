---
name: bel-move-mail-to-archive
description: This skill should be used when moving a single email message to the Archive folder in Microsoft 365 Mail. It provides a clean interface to move one specific email using its messageId without polluting the context window. Use this skill when processing bulk archive operations, moving spam emails, or any workflow requiring reliable one-email-at-a-time moves to Archive.
---

# Move Email to Archive Skill

## ⚠️ IMPORTANT: Claude Context Required

**This skill ONLY works when executed within Claude Agent context** (bassi, Claude Code, or other Claude Agent environments).

- ✅ **Works:** Inside a Claude agent that has MS365 authentication
- ❌ **Does NOT work:** As a standalone Python script outside Claude context
- ❌ **Does NOT work:** Without MS365 authentication already provided by Claude

The Python script (`scripts/move_to_archive.py`) is a **parameter preparation tool**, not a standalone email mover. It prepares parameters that Claude's tool system then executes.

---

## Purpose

Move one specific email message to the Archive folder in Microsoft 365 Mail with a clean, context-efficient interface.

## When to Use

- Moving individual emails to Archive (spam, no-TODO items, notifications)
- Bulk archive operations (chain multiple calls efficiently)
- Any workflow requiring reliable, one-at-a-time email archival
- When the main context should not be polluted by full email move operation details

## How to Use This Skill

### Quick Start: Direct API Call (Within Claude Context)

For a single email move, use the MS365 mail API directly with these parameters:

**Function:** `mcp__ms365__move-mail-message`

**Required Parameters:**
- `messageId`: The unique message ID of the email to move (string)
- `body`: JSON object with destination folder ID

**Optional Parameter:**
- Archive Folder ID: Use default from `references/archive_config.md` unless overriding

### Example Call Structure

```python
# Minimum parameters needed (within Claude agent context)
messageId = "AAMkADA4YjhhZDYwLWZiMWYtNDVkMy1hNjE3LWI3YzRlMzAwNGE0MgBGAAA..."
archive_folder_id = "AQMkADA4YjhhZDYwLWZiMWYtNDVkMy1hNjE3LWI3YzRlMzAwADRhNDIALgAAA-cCSmDe9C5Ai1IxFty3vKgBACIai-AjXXpFuMeLL-NexTAAAAIBVAAAAA=="

response = mcp__ms365__move-mail-message(
    messageId=messageId,
    body={"DestinationId": archive_folder_id}
)
```

### Key Success Pattern: One Email at a Time

**Critical Finding:** Moving emails individually (one per call) works reliably. Batch operations cause `ErrorInvalidIdMalformed` errors. Always move ONE email per operation call.

### Python Script Approach (Prepares Parameters for Claude)

Use `scripts/move_to_archive.py` to prepare parameters. This script:
- Handles default Archive folder ID lookup
- Validates messageId parameter format
- Returns JSON with parameters ready for Claude's API execution
- Can be chained in loops without context pollution

**What it does:** Returns the parameters Claude needs to execute the move
**What it does NOT do:** Move emails directly (requires Claude context)

**Usage:**
```bash
python scripts/move_to_archive.py --message-id "AAMkADA4YjhhZDYwLWZiMWYtNDVkMy1h..." [--archive-id "custom-id"]
```

**Output:**
```json
{
  "status": "ready",
  "operation": {
    "api_function": "mcp__ms365__move-mail-message",
    "parameters": {
      "messageId": "AAMkADA4YjhhZDYwLWZiMWYtNDVkMy1h...",
      "body": {
        "DestinationId": "AQMkADA4YjhhZDYwLWZi..."
      }
    }
  }
}
```

## Reference Materials

- **API Documentation:** See `references/api_docs.md` for full MS365 Mail API parameter details
- **Archive Configuration:** See `references/archive_config.md` for Archive folder ID and defaults
- **Archive Folder ID Default:** `AQMkADA4YjhhZDYwLWZiMWYtNDVkMy1hNjE3LWI3YzRlMzAwADRhNDIALgAAA-cCSmDe9C5Ai1IxFty3vKgBACIai-AjXXpFuMeLL-NexTAAAAIBVAAAAA==`

## Expected Response

Success response includes:
- `id`: Email ID (confirming which email was moved)
- `parentFolderId`: Archive folder ID (confirming destination)
- `subject`: Email subject (for reference)
- `receivedDateTime`: When email was received

**Indicates Success:** `parentFolderId` equals the Archive folder ID

## Important Notes

1. **One at a time:** Always move ONE email per operation call
2. **Message ID format:** Use the full message ID from the email list response
3. **No batch operations:** Do not attempt to move multiple emails in a single call
4. **Claude context required:** All operations must happen within Claude agent context
5. **Context efficiency:** This skill is designed to keep operations lean and not blow up context window

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `ErrorInvalidIdMalformed` | Invalid or malformed message ID | Verify message ID from current email list response |
| `ErrorItemNotFound` | Email no longer exists | Refresh email list; may have been deleted |
| `ErrorAccessDenied` | Permission issue | Verify authenticated user has Archive folder access |
| Wrong parentFolderId | Incorrect Archive folder ID | Verify folder ID from `references/archive_config.md` |
| Script doesn't move emails | Running outside Claude context | Ensure script runs within Claude agent environment |

## Bulk Operations: Using Sub-Agents

For archiving multiple emails without polluting context:

1. **Prepare list of message IDs** to archive
2. **Launch a sub-agent** using the bulk archive agent template
3. **Sub-agent iterates** through each ID and calls the move operation
4. **Sub-agent returns summary** to main context (one-line result, not 50+ lines)

### Sub-Agent Usage

See `.claude/agents/bulk-archive-agent.md` and `.claude/agents/BULK_ARCHIVE_TASK_TEMPLATE.md` for:
- Complete sub-agent architecture
- Task prompt template ready to copy/paste
- Examples of bulk archive workflows
- Error handling patterns

**Quick Example:**
```
Main Context: "Archive 50 emails"
   → Launch bulk-archive sub-agent with message IDs
   → Sub-agent moves silently (one at a time)
   → Returns: "✅ Archived 48 emails. ❌ 2 failed."
Result: Clean context, 1 summary line instead of 50 confirmations
```

---

## Architecture Overview

```
Single Email Move (use skill directly):
  User request → Direct API call → Archive → Done (inline, context stays clean)

Bulk Email Move (use sub-agent):
  User request → Identify emails → Launch sub-agent → Sub-agent archives silently → Summary to context
                                                  ↓
                                          (50+ operations happen here,
                                           context stays clean)
```
