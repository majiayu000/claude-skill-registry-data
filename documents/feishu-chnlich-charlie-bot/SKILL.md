---
name: feishu
description: This skill should be used when the user asks to read, create, or edit Feishu/Lark documents, search docs in their Feishu workspace, or fetch content from a Feishu wiki or docx URL.
version: 2.1.0
---

# Feishu Docs

Read, create, and edit documents in the Feishu workspace using the Feishu Open API with a user access token.

**IMPORTANT: User approval required for all writes.** Feishu does not support online review/diff. Before creating or editing any document, you MUST show the user the planned content and get explicit approval first.

## Configuration

- Credentials location: `$CHARLIEBOT_HOME/credentials.yaml`
- Keys (section `feishu`): `app_id`, `app_secret`, `user_access_token`, `refresh_token`
- Auth method: OAuth2 user access token (acts as the user's own account)
- Requests: send every Feishu Open API request through `charliebot feishu request`. The command reads the token from `credentials.yaml` inside its own process, so no token appears in a command, an output or a run record.

## API Reference

Send every request through `charliebot feishu request <METHOD> <URL>`:

```bash
charliebot feishu request GET 'https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/raw_content'
charliebot feishu request POST 'https://open.feishu.cn/open-apis/suite/docs-api/search/object' \
  --json '{"search_key":"query","count":10,"docs_types":["docx","wiki"]}'
```

The command adds the bearer header itself and prints the 2xx response body. Pass a request body from a file with `--data-file <path>`, and add any other header with `--header 'NAME:VALUE'`.

| Exit code | Meaning |
|---|---|
| 0 | A 2xx response whose `code` is absent or `0`. |
| 1 | Another status, a nonzero `code`, or a network failure. |
| 2 | Invalid arguments. |
| 3 | `credentials.yaml` is unreadable or a required `feishu` key is missing. |

Pipe the response body to `jq` when you need one field.

### Read a Wiki Page

Wiki URLs look like: `https://xxx.feishu.cn/wiki/{node_token}`

**Step 1** — Resolve the wiki node to get the actual document token:
```
GET https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={node_token}
```
The response contains `data.node.obj_token` (the document ID) and `data.node.obj_type` (usually `docx`).

**Step 2** — Fetch document content:
```
GET https://open.feishu.cn/open-apis/docx/v1/documents/{obj_token}/raw_content
```
Returns plain text in `data.content`.

### Read a Docx Page

Docx URLs look like: `https://xxx.feishu.cn/docx/{doc_token}`

```
GET https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/raw_content
```

### Get Document Blocks (Structured)

For richer content with block types (headings, code, tables, etc.):
```
GET https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks?page_size=500
```
Returns block tree in `data.items`. Use `page_token` from response for pagination.

### Search Documents

```
POST https://open.feishu.cn/open-apis/suite/docs-api/search/object
Content-Type: application/json

{
  "search_key": "your query",
  "count": 10,
  "docs_types": ["docx", "wiki"]
}
```

Requires the `search:docs:read` user scope. Results are returned in `data.docs_entities[]`, each with `docs_token`, `docs_type`, and `title`.

When `docs_types` contains `"doc"`, search returns an empty result. Search has poor recall for every document type.

- Treat an empty result as inconclusive.
- Verify an absence claim with another search surface or a known document link.

After a recorded meeting, Feishu stores AI notes and the transcript in the meeting owner's space. Search can match these title prefixes: notes titled `智能纪要：<title>` or `AI notes: <title>`, and transcripts titled `文字记录：<title>` or `Meeting transcript: <title>`.

- Search returns only notes the user owns or the owner shared with the user.
- When the notes of a meeting that another person owns are not visible, ask the user for the notes link.

### Public Permission

Use this to inspect or update the public-sharing policy for a docx document:

```
GET https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/public?type=docx
PATCH https://open.feishu.cn/open-apis/drive/v1/permissions/{token}/public?type=docx
Content-Type: application/json

{
  "link_share_entity": "tenant_readable"
}
```

Use the doc token / `document_id` as `{token}`.

Required user scopes:
- `docs:permission.setting:read`
- `docs:permission.setting:write_only`

`PATCH` is a write and still requires explicit user approval before execution.

Default policy for Linear-linked docs:
- `link_share_entity: tenant_readable` so the document is readable within the configured tenant
- Do **not** widen to `tenant_editable` unless the user explicitly asks
- Do **not** enable external public access by default

### List Wiki Space Nodes

To browse a wiki space:
```
GET https://open.feishu.cn/open-apis/wiki/v2/spaces/{space_id}/nodes?page_size=50
```

### Create a Document

```
POST https://open.feishu.cn/open-apis/docx/v1/documents
Content-Type: application/json

{
  "title": "Document Title",
  "folder_token": "optional_folder_token"
}
```
Returns `data.document.document_id`.

To create in a specific folder, provide `folder_token`. Omit it to create in the user's root folder.

### Add Content Blocks to a Document

```
POST https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
Content-Type: application/json

{
  "children": [
    {
      "block_type": 2,
      "text": {
        "elements": [
          {
            "text_run": {
              "content": "Your text here",
              "text_element_style": {}
            }
          }
        ]
      }
    }
  ]
}
```

Common block types:
- `2` — Text paragraph
- `3` — Heading 1
- `4` — Heading 2
- `5` — Heading 3
- `12` — Bullet (unordered list)
- `13` — Ordered list
- `14` — Code block
- `31` — Table (use two-step process below)
- `32` — Table cell (auto-created, do not insert manually)

For the top-level document block, `block_id` equals `document_id`.

### Insert a Table

Tables require a two-step process: create the table block, then fill each cell.

**Step 1** — Create the table (block_type 31):
```
POST https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children

{
  "children": [
    {
      "block_type": 31,
      "table": {
        "property": {
          "row_size": 3,
          "column_size": 2
        }
      }
    }
  ]
}
```

The response contains `data.children[0].table.cells` — a flat array of cell block IDs in **row-major order** (row0col0, row0col1, row1col0, row1col1, ...).

**Step 2** — Fill each cell by adding a text block as its child:
```
POST https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{cell_block_id}/children

{
  "children": [
    {
      "block_type": 2,
      "text": {
        "elements": [
          {
            "text_run": {
              "content": "Cell content",
              "text_element_style": {}
            }
          }
        ]
      }
    }
  ]
}
```

**Important notes:**
- Max 5 table blocks per request
- Rate limit: 3 edits/sec per document — add ~0.4s delay between cell writes
- Header row styling is cosmetic in Feishu — first row has no special API treatment

### Update a Block

```
PATCH https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}
Content-Type: application/json

{
  "update_text_elements": {
    "elements": [
      {
        "text_run": {
          "content": "Updated text"
        }
      }
    ]
  }
}
```

### Delete Blocks

```
DELETE https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children/batch_delete
Content-Type: application/json

{
  "start_index": 0,
  "end_index": 1
}
```

## Token Refresh

The user access token expires every **2 hours**. `charliebot feishu request` handles this itself: when Feishu answers `401` or an expired-token code (`99991663` or `20005`), the command gets an app access token from `app_id` and `app_secret`, exchanges the stored `refresh_token`, writes the new `user_access_token` and `refresh_token` to `credentials.yaml`, and retries the request once. Never mint, print or store a token by hand.

If the refresh itself fails, the command exits 1 and leaves `credentials.yaml` unchanged.

The refresh token lasts **30 days**. If it expires, ask the user to re-authorize via OAuth.

## OAuth2 Re-authorization

When the refresh token expires or new scopes are needed, the user must re-authorize:

1. Print the authorize URL and open it in a browser: `charliebot feishu consent-url --scope <scope>…` (repeat `--scope` or list several scopes after one flag). The URL carries the app id and redirects to `http://localhost:9999/callback`.
2. User authorizes and gets redirected to `http://localhost:9999/callback?code=XXX`.
3. Exchange the code: `charliebot feishu exchange-code XXX`. The command gets an app access token from `app_id` and `app_secret` and stores the new `user_access_token` and `refresh_token` in the `feishu` section of `credentials.yaml`. It prints no token.
4. Confirm with a request, for example `charliebot feishu request GET https://open.feishu.cn/open-apis/authen/v1/user_info`.

Current scopes depend on what your app has been granted; check your token's actual granted scopes.

## URL Parsing

Extract tokens from Feishu URLs:
- `https://<tenant>.feishu.cn/wiki/WIKINODETOKENEXAMPLE0123` → node_token = `WIKINODETOKENEXAMPLE0123` (wiki, needs 2-step)
- `https://<tenant>.feishu.cn/docx/DOCTOKENEXAMPLE0123` → doc_token = `DOCTOKENEXAMPLE0123` (direct read)

## Linking with Linear

- **Title format:** `{identifier} {title}` — e.g. `ABC-123 Example Linear issue title`
- **Organize by date:** Feishu docs linked from Linear issues are living documents with ongoing updates. Structure content with **H1 date headers** (e.g. `# 2026-03-26`) as top-level sections. Each day's work goes under its date. New updates append a new date section — never overwrite previous dates.
- **Use Pacific Time (PT) for dates** — all date headers use `America/Los_Angeles` timezone, not UTC. Run `TZ=America/Los_Angeles date +%Y-%m-%d` to get the correct date.

## Content conventions

For docs linked to a Linear issue, the division of content between the issue and
the doc is defined in the `linear` skill (Content conventions).
