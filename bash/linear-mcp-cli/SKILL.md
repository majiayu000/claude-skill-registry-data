---
name: linear-mcp-cli
description: Use when reading Linear data from the CLI via MCP.
trigger: Linear issues, mcp.linear.app, linear MCP server, workspace issues
category: mcp
version: 1.0.0
---

# Linear via the `linear` MCP server (direct JSON-RPC)

## When to use

The agent needs Linear data (issues, teams, projects, comments) but the `linear::*`
MCP tools are **not in the CLI agent's toolset** (MCP tools only load where the MCP
client config is active). This skill calls the very same MCP server directly with the
OAuth token OpenAmer already stored, so no browser and no API key is needed.

## Files

- `scripts/linear_mcp.py` — stdlib-only (urllib) streamable-HTTP MCP client + CLI.

## Credentials

`C:\Users\damir\AppData\Local\openamer-laptop\mcp-tokens\linear.json`
(keys: `access_token`, `refresh_token`, `expires_at`, `scope` = `read write`).
Token lives ~24h. Expired? `openamer mcp reauth linear` — do NOT hand-roll the OAuth dance
(`openamer mcp login linear` also works).

Endpoint: `https://mcp.linear.app/mcp` · server name: `Linear MCP` · protocol `2025-03-26`.

## Commands

```bash
cd C:/Users/damir/AppData/Local/openamer-laptop/skills/mcp/linear-mcp-cli/scripts
python linear_mcp.py workspace                 # connected workspace (name + url)
python linear_mcp.py list-issues               # ALL issues, one page at a time
python linear_mcp.py list-issues --limit 250   # single big page
python linear_mcp.py list-issues --status Todo --team Openamer
python linear_mcp.py tools list_issues         # JSON schema of a tool
python linear_mcp.py call get_issue '{"id":"OPE-1"}'
python linear_mcp.py call save_issue '{"id":"OPE-3","title":"New title"}'
```

### Comment tools (create / read / delete)

```bash
# create a top-level comment on an issue -> returns the new comment {id, body, author, ...}
python linear_mcp.py call save_comment '{"issueId":"OPE-2","body":"text"}'
# read all comments of an issue -> {"comments":[{id, body, author, quotedText, ...}]}
python linear_mcp.py call list_comments '{"issueId":"OPE-2"}'
# delete by comment id -> {"success": true}
python linear_mcp.py call delete_comment '{"id":"<comment-uuid>"}'
```

Full comment round-trip test (create -> list -> delete -> list again, asserts absence):

```python
import sys; sys.path.insert(0, r"...\skills\mcp\linear-mcp-cli\scripts")
import linear_mcp as L
tok = L.load_token(); sid = L.handshake(tok)
c = L.call(tok, sid, "save_comment", {"issueId": "OPE-2", "body": "text"}, rid=3)
cid = c["id"]
L.call(tok, sid, "delete_comment", {"id": cid}, rid=5)
assert cid not in [x["id"] for x in L.call(tok, sid, "list_comments", {"issueId": "OPE-2"}, rid=6)["comments"]]
```

`list-issues` prints `IDENTIFIER<TAB>TITLE`, one line per issue; progress goes to stderr,
so `... list-issues 2>/dev/null` is safe to pipe.

## Pitfalls

- **SSE framing.** Every response is `text/event-stream`; take the *last* `data:` line and
  `json.loads` it. A plain JSON parse of the raw body fails.
- **Session id.** The server works stateless (no `mcp-session-id` returned here), but send
  the header anyway if present, plus `MCP-Protocol-Version: 2025-03-26`.
- **`Accept`** must list both `application/json` and `text/event-stream`, else HTTP 406.
- **Tool result shape.** `result.content[0].text` is a *JSON string*, not an object —
  `json.loads` it a second time. Descriptions are truncated with a
  `(truncated, use get_issue for full description)` marker.
- **Pagination.** `{"issues":[…],"hasNextPage":bool,"cursor":…}`. Walk until
  `hasNextPage` is false; `limit` caps at 250.
- **Write scope is real.** `save_issue`/`delete_*` mutate the live workspace — only call
  them on explicit user instruction.
- String args: pass real newlines in markdown, not literal `\n` (server instruction).

## Verification

```bash
python linear_mcp.py workspace && python linear_mcp.py list-issues
```
Expected on this machine: workspace `openamer`, 4 issues (OPE-1..OPE-4).
An empty list or HTTP 401 means expired token -> `openamer mcp reauth linear`.
