---
name: notion
description: "Pages, data sources, and files via the official CLI or API."
version: 1.0.0
author: External Agent contributors, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
required_environment_variables:
  - name: NOTION_API_TOKEN
    prompt: "Notion API token for the integration (starts with ntn_ or secret_)"
    help: "Create an integration at https://www.notion.so/my-integrations and share the pages or data sources it should access."
metadata:
  hermes:
    tags: [notion, notes, pages, databases, api, ntn]
    category: note-taking
    related_skills: [obsidian]
---

# Notion Skill

Work with Notion pages, data sources, files, comments, search, Workers, and raw API calls. Prefer the official `ntn` CLI; use `curl` only when `ntn` is unavailable or a raw request is clearer. Ported from External Agent `skills/notion/SKILL.md`.

## When to Use

- Reading, creating, updating, or trashing Notion pages (Markdown-first).
- Querying data sources (databases) and resolving database IDs.
- Uploading or listing files, managing comments, searching the workspace.
- Raw API calls for anything the CLI does not cover.

## Prerequisites

- The `ntn` CLI (`npm install -g ntn`) or `curl`. Run commands through `terminal`.
- `NOTION_API_TOKEN`: a Notion integration token (or personal access token). Create an integration at https://www.notion.so/my-integrations, then share the pages or data sources it should access with that integration — unshared content is invisible to the token. The token is supplied by the user at runtime; never hardcode or embed one.
- API version `2026-03-11` (current latest). `ntn api` sets the `Authorization` and `Notion-Version` headers automatically.

## How to Run

Script/headless auth (run through `terminal`):

```
export NOTION_API_TOKEN=secret_or_ntn_token
export NOTION_API_VERSION=2026-03-11
```

`ntn api` uses CLI login by default, or `NOTION_API_TOKEN` when set. For interactive login, run `ntn login` once.

## Quick Reference

| Need | Command |
|---|---|
| Health / setup check | `ntn doctor` |
| List API surface | `ntn api ls` |
| Read a page as Markdown | `ntn pages get <page-id>` |
| Create a page | `ntn pages create --parent page:<page-id> --content '# Title\n\nBody'` |
| Query a data source | `ntn datasources query <data-source-id>` |
| Raw API call | `ntn api v1/users/me` |
| Curl fallback | `curl` to `https://api.notion.com/v1/...` with `Authorization` + `Notion-Version` headers |

## Procedure

### Inspect

```
ntn doctor
ntn api ls
ntn api ls --json
ntn api v1/comments --help
ntn api v1/comments --spec -X POST
ntn api v1/comments --docs -X POST
```

### Pages

Markdown-first helpers:

```
ntn pages get <page-id>
ntn pages get <page-id> --json
ntn pages create --parent page:<page-id> --content '# Title\n\nBody'
ntn pages create --parent data-source:<data-source-id> --content '# Title\n\nBody'
ntn pages edit <page-id> --content '# Updated'
ntn pages trash <page-id> --yes
```

Notes:

- `pages get` prints Markdown with page properties as frontmatter.
- Content input: `--content`.
- Parent refs: `page:<id>`, `database:<id>`, `data-source:<id>`.
- For properties/templates/full Pages API, use `ntn api v1/pages`.

### Data sources

```
ntn datasources resolve <database-id>
ntn datasources resolve <database-id> --json
ntn datasources query <data-source-id>
ntn datasources query <data-source-id> --limit 50 --json
ntn datasources query <data-source-id> --sort 'Date desc'
ntn datasources query <data-source-id> --filter '{"property":"Done","checkbox":{"equals":true}}'
```

Use `resolve` when you have a database ID. Query needs a data source ID.

### Raw API

```
ntn api v1/users/me
ntn api v1/search query=roadmap page_size:=10
ntn api v1/pages 'parent[data_source_id]='"$DS_ID" 'properties[Name][title][0][text][content]=New item'
ntn api "v1/pages/$PAGE_ID" -X PATCH in_trash:=true
ntn api "v1/blocks/$PAGE_ID/children" -X PATCH \
  'children[0][type]=paragraph' \
  'children[0][paragraph][rich_text][0][text][content]=Hello'
```

Input syntax:

- `path=value`: string body field.
- `path:=json`: typed JSON body field.
- `name==value`: query parameter.
- `Header:Value`: request header.
- `--data '<json>'` or stdin JSON for larger bodies.
- Only one body source per request.

### Files

```
ntn files create < image.png
ntn files create --filename photo.png --content-type image/png < /tmp/photo
ntn files create --external-url https://example.com/photo.png
ntn files get <upload-id>
ntn files list
```

### Workers

```
ntn workers new
ntn workers deploy
ntn workers list --json
ntn workers runs list --json
ntn workers runs logs <run-id>
```

Workers may require Business/Enterprise plan and workspace enablement.

### Curl fallback

```
curl -sS "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2026-03-11" \
  -H "Content-Type: application/json"
```

## Pitfalls

- A token that cannot see a page is almost always a sharing problem: the page or data source must be shared with the integration.
- Use `in_trash`, not `archived`.
- Append block positioning uses `position`, not flat `after`.
- `transcription` block renamed to `meeting_notes`.
- Databases can contain multiple data sources; page parents generally use `data_source_id`.
- The API token grants full access to everything shared with the integration — keep it secret, never paste it into a page or a message, and never commit it.

## Verification

- `ntn doctor` passes and `ntn api v1/users/me` returns the integration's user object.
- Live check on the host: the CLI (or curl) plus a user-supplied `NOTION_API_TOKEN` are present, and a read of a known shared page returns its Markdown. The CLI and token are host-side prerequisites; without them the skill reports the missing setup instead of working around it.
