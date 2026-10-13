---
name: substack-drafter
description: "Drafts articles on Substack from markdown or text files. Converts content to Tiptap JSON, authenticates via Chrome browser tools, and creates drafts via Substack API. Use when publishing, drafting, or posting content to Substack."
disable-model-invocation: true
---

# Substack Drafter

## Purpose

Takes a markdown (.md) or text (.txt) file and creates a draft article on Substack. Uses Chrome MCP browser tools for authentication since Substack relies on httpOnly cookies that cannot be extracted programmatically.

## Critical Constraint

**NEVER publish. Only create drafts.** The user will review and hit publish manually.

## Prerequisites

- User must be signed into their Substack publication in Chrome
- Chrome MCP browser tools must be available (`mcp__claude-in-chrome__*`)
- Python 3 installed (for markdown-to-Tiptap conversion)

## Workflow

### Step 1: Gather Input

Ask the user for:
- **File path**: The .md or .txt file to draft
- **Publication URL**: Their Substack subdomain (e.g., `yourname.substack.com`). Check if previously stored.
- **Title**: Article title (or extract from first H1 in the file)
- **Subtitle**: Optional subtitle

### Step 2: Convert Content to Tiptap JSON

Run the conversion script:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/md_to_tiptap.py" "<input_file>" "/tmp/substack-tiptap-body.json"
```

This produces a Tiptap JSON file compatible with Substack's editor. See [tiptap-reference.md](tiptap-reference.md) for format details.

**Verify** the output file exists and is valid JSON before proceeding.

### Step 3: Authenticate via Browser

Substack uses httpOnly cookies -- you CANNOT use curl or direct HTTP requests. All API calls MUST execute from the browser page context via `mcp__claude-in-chrome__javascript_tool`.

1. Load Chrome MCP tools via ToolSearch:
   ```
   ToolSearch: "select:mcp__claude-in-chrome__tabs_context_mcp"
   ToolSearch: "select:mcp__claude-in-chrome__javascript_tool"
   ```

2. Get current tabs:
   ```
   mcp__claude-in-chrome__tabs_context_mcp
   ```

3. Navigate to the publication URL. Either find an existing tab on the publication or create a new one:
   ```
   ToolSearch: "select:mcp__claude-in-chrome__tabs_create_mcp"
   # Create tab with URL: https://<subdomain>.substack.com/
   ```

4. Verify authentication by fetching the user profile:
   ```javascript
   (async () => {
     const resp = await fetch('/api/v1/user/profile');
     const data = await resp.json();
     return JSON.stringify({ id: data.id, name: data.name });
   })()
   ```
   If this fails or returns no id, the user needs to sign in first.

### Step 4: Create the Draft

Execute from the browser page context:

```javascript
(async () => {
  const resp = await fetch('/api/v1/drafts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      draft_title: "<TITLE>",
      draft_subtitle: "<SUBTITLE>",  // optional, omit if not provided
      draft_bylines: [{ id: <USER_ID>, is_guest: false }],
      type: "newsletter"
    })
  });
  const result = await resp.json();
  return JSON.stringify({ id: result.id, title: result.draft_title });
})()
```

**Save the draft ID** from the response -- you need it for Step 5.

### Step 5: Populate the Draft Body

Read the Tiptap JSON file and embed it directly as a JavaScript object in the browser call. The body must be **double-stringified**: the Tiptap JSON object is stringified into the `draft_body` field, which itself is part of a stringified request body.

```javascript
(async () => {
  const body = <TIPTAP_JSON_OBJECT>;  // embed the full JSON object here
  const resp = await fetch('/api/v1/drafts/<DRAFT_ID>', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      draft_body: JSON.stringify(body),
      draft_bylines: [{ id: <USER_ID>, is_guest: false }]
    })
  });
  const result = await resp.json();
  return JSON.stringify({ status: resp.status, id: result.id, bodyLen: (result.draft_body || '').length });
})()
```

**Important**: Read the Tiptap JSON file contents and embed the parsed object directly in the JavaScript code. Do NOT try to fetch from localhost (HTTPS pages block mixed content) or use base64 encoding schemes.

### Step 6: Confirm

Report to the user:
- Draft title and ID
- Body length (as a sanity check)
- Remind them the draft is ready to review and publish in their Substack dashboard

## Key API Details

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/user/profile` | GET | Get authenticated user info (id, name) |
| `/api/v1/drafts` | POST | Create a new draft |
| `/api/v1/drafts/{id}` | PUT | Update draft (title, body, subtitle) |
| `/api/v1/drafts/{id}` | GET | Retrieve a draft |

All endpoints are relative to the publication URL (e.g., `https://yourname.substack.com/api/v1/drafts`).

## Required Fields for Draft Creation

- `draft_title` (string): Article title
- `draft_bylines` (array): `[{ id: <user_id_number>, is_guest: false }]`
- `type` (string): Usually `"newsletter"`

## Common Pitfalls

1. **Missing draft_bylines**: The API returns `{"errors":[{"param":"draft_bylines","msg":"Invalid value"}]}` if omitted
2. **CORS / mixed content**: Never try to fetch from localhost or external URLs from the Substack page context
3. **Cookies not sent**: Make sure the browser tab is on the correct publication URL before making API calls
4. **Body not appearing**: The `draft_body` value must be a **stringified** Tiptap JSON string, not a raw object
5. **Large bodies**: For articles over ~25KB of Tiptap JSON, embed the full object directly in the JavaScript call rather than chunking

## When NOT to Use This Skill

- User wants to publish directly (we only draft)
- User wants to edit an existing published post (use PUT with the existing draft ID instead)
- Content is not in markdown or plain text format
