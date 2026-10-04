---
name: read
description: Takes a Figma file URL, lists its pages, and collects every top-level frame on the page you pick. Metadata and screenshots are read in parallel and laid out as a markdown tree. Gives you the whole structure from a URL alone, without selecting frames one by one in the desktop app. Triggers - "/fig:read", "read this Figma file", "list every frame", "피그마 파일 읽어줘", "프레임 전부 뽑아줘", "전체 구조 보여줘".
allowed-tools: AskUserQuestion, Bash, mcp__plugin_figma_figma__get_metadata, mcp__plugin_figma_figma__get_screenshot
---

# fig:read — collecting every frame in a Figma file

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install fig@byjunyoung`), rather than improvising what the scripts do.

Takes a single Figma file URL, walks the page → frame structure automatically, and collects every top-level frame on the pages you pick as metadata plus screenshots. It works without selecting anything in the desktop app.

## When to invoke

- The user hands over a Figma **file** URL (no node specified) and says "read all of it", "show me the structure", "pull every frame"
- Taking a screen inventory before spec or canonical-page work
- An explicit "/fig:read"

## When NOT to invoke

- Frame naming and section tidying → `/fig:prep`
- Auditing rule violations → `/fig:lint`
- Auditing whether working changes landed in the canonical page → `/fig:sync`
- Design context for a code implementation → the `figma:figma-design-to-code` skill · carrying it into the front-end repo → `/fig:code`

## Inputs

- `figma_url` (required): a URL of the form figma.com/design/:fileKey/...
  - A node-id parameter is ignored and the whole file is used (the user picks the page)

## Procedure

### 1. Parse the URL

Extract the fileKey from the Figma URL:
- Pattern: `figma.com/design/([A-Za-z0-9]+)/...`
- If no fileKey comes out, ask the user for the exact URL again

### 1.5 Check the token first

Before going down the REST API path, confirm the token's state with a light ping. The environment variable's name is set by `tools.figma_token_env` (default `FIGMA_TOKEN`).

```bash
source ~/.zshrc 2>/dev/null
VAR=$(python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py \
      | python3 -c 'import json,sys; print(json.load(sys.stdin)["tools"]["figma_token_env"])')
TOKEN="${!VAR}"
if [ -z "$TOKEN" ]; then
  echo "STATE=NO_TOKEN ($VAR not set)"
else
  CODE=$(curl -sS -o /dev/null -w '%{http_code}' \
    -H "X-Figma-Token: $TOKEN" "https://api.figma.com/v1/me")
  echo "STATE=HTTP_$CODE"
fi
```

Branching by state:

| STATE | Meaning | What to do |
|---|---|---|
| `NO_TOKEN` | The environment variable is not set | Say "no token set", link the PAT guide in Notes, fall back to plugin:figma |
| `HTTP_200` | Fine | Proceed with the REST path in step 2 |
| `HTTP_401` | Token expired or invalid | **"FIGMA_TOKEN has expired or is invalid. It needs reissuing."** + the guide + fallback |
| `HTTP_403` | Insufficient permission | "The token lacks permission. Reissue it with the file_content:read scope" + fallback |
| `HTTP_429` | Rate limited | "Try again shortly" + fallback |
| anything else | Unknown error | Surface the HTTP code as it is + fallback |

**Important**: 401 is the one status code that covers "no token", "expired", and "invalid" alike. Because the environment variable's existence is checked above first, a 401 here means the value is present and was rejected — so the guidance is expired or invalid.

### 2. List the pages

**First choice: the Figma REST API (if 1.5 came back HTTP_200)**

```bash
curl -sS -w "\nHTTP_CODE=%{http_code}" \
  -H "X-Figma-Token: $FIGMA_TOKEN" \
  "https://api.figma.com/v1/files/{fileKey}?depth=1"
```

- depth=1 returns page nodes only (avoiding a download of the whole tree)
- From the response body, `.document.children[]` → extract `{nodeId}|{pageName}`
- Take HTTP_CODE alongside it to guard against per-file permission problems:
  - `200` → proceed
  - `403` → "no access to this file (it may belong to another team, or be private)" + fallback
  - `404` → "file not found. Check the URL"
  - anything else → surface the error + fallback
- Never print the token in a response or a log — it belongs in the header only

**Second choice: the plugin:figma MCP fallback (no token, or an error)**

Call `mcp__plugin_figma_figma__get_metadata` with the fileKey alone.
- The limit: it depends on the desktop app's open file and viewport, so it may return only some of the pages
- If the node-id in the user's URL is a page (canvas type), include that page as a direct entry candidate too

**Zero pages**: with no token set and an empty plugin response too, point at the "PAT setup guide" at the end of the output and stop.

With only one page, skip the selection step and go straight to 3-2.

### 3. Pick the pages (when there are ≥ 2)

Present the page list through `AskUserQuestion`:
- `multiSelect: true`
- One page name per option label (at most 4 can be shown — with 5 or more pages, offer the first 3 plus "all" plus "pick manually")
- With far too many (over 8), print a numbered markdown list and have the user type the numbers

### 3-2. Read the frame tree

Call `get_metadata` for each selected page:
- `fileKey` + the page `nodeId`
- depth 2 is enough (the page's direct children are the top-level frames)

Collect the top-level frame ids for each page.

### 4. Frame-count guard

If the total frame count exceeds `tools.frame_count_guard`, warn before proceeding:
- Print, as markdown, "{N} frames found. Pulling screenshots too will cost significant time and context. Continue?"
- Branch through `AskUserQuestion`: "all of it / metadata only (skip screenshots) / pick pages again"

### 5. Collect per frame (in parallel)

For each frame, both calls go out in parallel inside one message:
- `mcp__plugin_figma_figma__get_metadata` (fileKey + nodeId)
- `mcp__plugin_figma_figma__get_screenshot` (fileKey + nodeId)

Too many at once is heavy, so send them **in batches of 5**.

If a screenshot call fails, keep the metadata and state the failure in the output (`screenshot: failed`).

### 6. Emit the markdown tree

Print to the conversation in this form:

```
# {file name}

## {page name 1}

### {frame name} (`{nodeId}`)
- Link: https://figma.com/design/{fileKey}/?node-id={nodeId with : → -}
- Size: {width}×{height}
- Children: {childCount}
- Screenshot: {path, or "failed"}

### {frame name 2} ...

## {page name 2} ...
```

Show the image `get_screenshot` returned as it is (inline in the assistant's response).

### 7. Point at what comes next

One line at the end of the output:
> Candidates for the next step: `/fig:prep` (tidy the structure) · `/fig:lint` (audit) · `/fig:sync` (audit against the canonical page)

## Output contract

- Everything is markdown, in the conversation only (no files, no external pages created)
- Node links are clickable figma.com URLs — the nodeId's `:` becomes `-`
- Failures are marked "failed" explicitly, never silently dropped

## Constraints

- No external writes of any kind — this is a pure read skill
- Beyond page selection, keep the interviewing minimal (as little burden on the user as possible)
- What is collected stays in context, so structure it for the next skill to pick up

## Notes

- The plugin:figma MCP's `get_metadata` and `get_screenshot` need only fileKey + nodeId — the desktop app's selection state is irrelevant
- But plugin MCP `get_metadata(fileKey only)` is bound to the desktop app's context and exposes only some pages → enumerating every page requires the Figma REST API
- Expanding down into components, instances, and vectors is deliberately not done. It stops at top-level frames
- When a design changes often there is no point caching the result — call again each time

### Setting up a Figma Personal Access Token (PAT)

The REST path needs a PAT. A one-time setup:

1. Figma web → profile, top right → Settings → **Security** tab → **Personal access tokens** → **Generate new token**
2. Minimise the scope: check `File content` → **Read-only** and nothing else
3. Copy the token (shown once, starts with `figd_`)
4. Add it to the end of `~/.zshrc` (matching the name in `tools.figma_token_env`):

   ```bash
   export FIGMA_TOKEN="figd_paste_it_here"
   ```

5. Open a new terminal, or run `source ~/.zshrc`

Token safety:
- Never expose it in a response, a log, or a commit
- Even when parsing with jq, pass it in the header only and rely on the response body alone
- If expiry is suspected, revoke the token in Figma's Security tab and reissue

The limits of expiry detection:
- A Figma PAT does not encode its expiry date, so there is no way to check ahead of time
- It can only be detected after the fact, from an API call's HTTP status
- A `401` covers "no token", "expired", and "invalid" all at once, so the skill checks the environment variable's existence first to separate the cases
