---
name: jira-attachments
description: Fetch and view/analyze image and file attachments from a Jira ticket. Use when the user wants to see, describe, or analyze a screenshot/image/attachment on a Jira ticket, or references an image that only exists inside a ticket. Downloads the real bytes via the existing Atlassian MCP for metadata plus a personal API token for the binary, then reads the file so the image is actually viewable.
disable-model-invocation: false
allowed-tools: Bash(bash *) Bash(gh *) Bash(curl *) Read
---

# Jira attachments

The official Atlassian MCP returns attachment *metadata* (id, filename, mimeType, a
`content` URL) but has **no tool that returns the bytes** — and its OAuth token can't be
borrowed. This skill closes that gap: metadata comes from the MCP (existing auth), and the
binary is downloaded with a personal Atlassian API token, then read from disk so the image
is genuinely viewable (not just base64 text).

## Prerequisites (one-time)

The download step needs these in the shell profile (`~/.zshrc` or a sourced file):

```sh
export ATLASSIAN_EMAIL="you@example.com"          # email on your Atlassian account
export ATLASSIAN_API_TOKEN="…"                     # id.atlassian.com/manage-profile/security/api-tokens
export ATLASSIAN_SITE="your-site.atlassian.net"    # your Jira Cloud site host
```

If a download fails with an auth error, the token/email/site are missing or wrong — stop and
tell the user to set them; do not go hunting for credentials elsewhere.

## Steps

1. **Resolve the ticket.** Accept a ticket key (e.g. `ABC-1234`) or an issue URL. Determine
   the `cloudId` for the site by calling `getAccessibleAtlassianResources` (do not hardcode
   it — it differs per site).

2. **Get attachment metadata** via the MCP (no token needed):
   `getJiraIssue(cloudId, issueIdOrKey, fields:["summary","attachment"])`.
   Each attachment gives `id`, `filename`, `mimeType`, `size`, `content`.
   - If `attachment` is empty, tell the user the ticket has no attachments and stop.
   - If the user named a specific file, filter by `filename`; otherwise take all
     image/* attachments (offer to include non-images too).

3. **Download each wanted attachment** into the session scratchpad using the helper —
   pass the attachment `id` (the script builds the correct site-URL form itself):

   ```sh
   bash ~/.claude/skills/jira-attachments/fetch-attachment.sh <attachment_id> "<scratchpad>/<filename>"
   ```

   Use the real session scratchpad directory for `<scratchpad>`. The script prints
   `saved: <path> (<mime>, <bytes>)` on success and exits non-zero with the response body
   on failure.

4. **View it.** `Read` each saved file — image files render visually — then answer the
   user's actual question (describe the UI, extract the error text, compare to code, etc.).

## Notes

- Download uses `https://<site>/rest/api/3/attachment/content/<id>` with Basic auth. Do
  **not** use the `content` URL from metadata verbatim — it points at
  `api.atlassian.com/ex/jira/...`, which only accepts OAuth Bearer, not the API token.
- Only the byte download uses the token; all metadata stays on the MCP.
- Files land in the scratchpad, so no cleanup is required and nothing enters the repo.
