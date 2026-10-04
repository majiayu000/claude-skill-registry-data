---
name: constellation-troubleshooting
description: This skill should be used when the user asks about "Constellation errors", "fix Constellation", "debug Constellation", "Constellation not working", "API connection issues", "indexing problems", "MCP server", "Failed to reconnect", mentions any Constellation error codes (AUTH_ERROR, PROJECT_NOT_INDEXED, etc.), or when Constellation commands fail.
---

# Constellation Troubleshooting

Quick diagnostic procedures for Constellation plugin issues.

## Quick Diagnosis Flowchart

```
Issue Reported
     |
     v
Can mcp__constellation__code_intel be called?
     |                    |
    YES                   NO
     |                    |
     v                    v
  API Error          MCP Server Issue
 (has code)         (see MCP Diagnosis)
     |
     v
Check error.code:
- AUTH_ERROR --> Authentication section
- PROJECT_NOT_INDEXED --> Indexing section
- SYMBOL_NOT_FOUND --> Query Issues section
- API_UNREACHABLE --> Connectivity section
```

## MCP Server Issues

**Symptom:** "Failed to reconnect to plugin:constellation:constellation" or tool calls fail entirely.

**Cause:** The MCP server isn't starting or is crashing.

**Quick Fixes:**

1. **Restart Claude Code** - MCP connections initialize at startup

2. **Verify MCP configuration:**

   Note, the tool is built into the constellation plugin, but should accurately reflect the following:

   ```json
   {
     "mcpServers": {
       "constellation": {
         "type": "stdio",
         "command": "npx",
         "args": ["-y", "@constellationdev/mcp@1.2.11"],
         "env": {
           "CONSTELLATION_ACCESS_KEY": "${CONSTELLATION_ACCESS_KEY}"
         }
       }
     }
   }
   ```

## Authentication Issues (AUTH_ERROR)

**Symptom:** "Authentication failed" or "Invalid API key"

**Quick Fixes:**

1. **Configure credentials:**

   ```bash
   npx @constellationdev/cli auth
   ```

2. **Check if access key is properly set:**

   In the event of `AUTH_ERROR` failures the MCP server provides details in the `error.guidance[0]` value of the response object, indicating the current state of the `CONSTELLATION_ACCESS_KEY` environment variable.

3. **If key is expired:** Regenerate in Constellation web UI under Settings > API Keys

## Indexing Issues (PROJECT_NOT_INDEXED)

**Symptom:** "Project not indexed" or empty results

**Quick Fixes:**

1. **Index the project:**

   ```bash
   cd /path/to/your/project
   constellation index --full
   ```

2. **Force reindex if stale:**

   ```bash
   constellation index --full --force
   ```

## Connectivity Issues (API_UNREACHABLE)

**Symptom:** Timeout or connection refused

**Quick Fixes:**

1. **Check network connectivity**

2. **Check Constellation status at https://status.constellationdev.io/**

## Query Issues (SYMBOL_NOT_FOUND, FILE_NOT_FOUND)

These are typically **not errors** - the item simply wasn't found in the index.

**Troubleshooting:**

1. Try partial/broader search terms
2. Check spelling and case sensitivity
3. Verify the file extension is in configured languages
4. Re-index if the file was recently added

## Diagnostic Command

Run `/constellation:diagnose` for a quick health check that tests:

- MCP server connectivity
- API authentication
- Project indexing status

See `references/error-codes.md` for complete error code documentation.
