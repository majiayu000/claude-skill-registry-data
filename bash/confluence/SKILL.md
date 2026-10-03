---
name: confluence
description: >-
  Confluence via confluence-cli (read, search, create, update, move, delete,
  attachments, comments). Shared npm CLI; per-workspace .env via SkillCred.
  Use when the user mentions Confluence, wiki pages, CQL search, or
  /confluence_*.
disable-model-invocation: true
---

### TO COPY

# confluence

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/confluence/scripts/skill_env.py)"
confluence <subcommand> …
```

##### END TO COPY

# confluence

## When to use

Use for Atlassian Confluence page/space work. Triggers: "Confluence page", "wiki",
"search Confluence", "create page", `/confluence_*`.

Confirm with the user before **write** ops (create, update, move, delete, upload).
Prefer `CONFLUENCE_READ_ONLY=true` for research-only agents.

## Prerequisites

This skill documents **`confluence-cli`** ([npm](https://www.npmjs.com/package/confluence-cli)). Install once per machine:

```bash
npm install -g confluence-cli
confluence --version
```

Load credentials into the shell, then call `confluence` directly:

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
eval "$(~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/confluence/scripts/skill_env.py)"
confluence read 123456789 --format markdown
```

PowerShell:

```powershell
$env:CURRENT_SKILL_DIRECTORY = "{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/confluence/scripts/skill_env.py --shell powershell | Invoke-Expression
confluence read 123456789 --format markdown
```

`skill_env.py` reads `.env` via SkillCred and prints export commands for the detected OS/shell.

## Credentials — SkillCred `.env`

| Variable | Example |
|----------|---------|
| `CONFLUENCE_DOMAIN` | `company.atlassian.net` |
| `CONFLUENCE_API_PATH` | `/wiki/rest/api` (Cloud) or `/rest/api` (Server/DC) |
| `CONFLUENCE_AUTH_TYPE` | `basic` or `bearer` |
| `CONFLUENCE_EMAIL` | `user@company.com` (required when `basic`) |
| `CONFLUENCE_API_TOKEN` | API token / PAT |

Optional: `CONFLUENCE_PROFILE`, `CONFLUENCE_READ_ONLY=true`, `CONFLUENCE_FORCE_CLOUD`, `CONFLUENCE_LINK_STYLE`.

```bash
cp ~/.meta-skills/skills/productivity/confluence/.env.example "{SKILL_PATH}/.env"
```

## Slash commands

Map `/confluence_<action>` → `confluence <action> …` (**after** `skill_env.py` exports are eval'd).

### Read / search (`confluence`)

| Slash | CLI | Description |
|-------|-----|-------------|
| `/confluence_read` | `confluence read <pageId\|URL> [--format markdown\|text\|storage\|html]` | Read page |
| `/confluence_info` | `confluence info <pageId> [--format json]` | Metadata |
| `/confluence_find` | `confluence find "Title" [--space KEY]` | Find by title |
| `/confluence_search` | `confluence search "query" [--limit N] [--cql]` | Search / CQL |
| `/confluence_spaces` | `confluence spaces` | List spaces |
| `/confluence_children` | `confluence children <pageId> [--recursive] [--format json\|tree]` | Children |
| `/confluence_comments` | `confluence comments <pageId> [--format json] [--all]` | List comments |
| `/confluence_attachments` | `confluence attachments <pageId> [--download] [--dest DIR]` | List / download |
| `/confluence_export` | `confluence export <pageId> [--format markdown] [--dest DIR]` | Export |

### Write (`confluence` — confirm first; `--yes` on deletes)

| Slash | CLI | Description |
|-------|-----|-------------|
| `/confluence_create` | `confluence create "Title" SPACE [--file path\|--content …] [--format markdown]` | Create page |
| `/confluence_create-child` | `confluence create-child "Title" <parentId> [--file …] [--format markdown]` | Child page |
| `/confluence_update` | `confluence update <pageId> [--title …] [--file …] [--format markdown]` | Update |
| `/confluence_move` | `confluence move <pageId> <newParentId> [--title …]` | Move (same space) |
| `/confluence_delete` | `confluence delete <pageId> --yes` | Trash page |
| `/confluence_edit` | `confluence edit <pageId> [--output page.xml]` | Fetch storage XML |
| `/confluence_comment` | `confluence comment <pageId> --content "…" [--location footer]` | Add comment |
| `/confluence_comment-delete` | `confluence comment-delete <id> --yes` | Delete comment |
| `/confluence_attachment-upload` | `confluence attachment-upload <pageId> --file path [--replace]` | Upload |
| `/confluence_attachment-delete` | `confluence attachment-delete <pageId> <attId> --yes` | Delete attachment |
| `/confluence_copy-tree` | `confluence copy-tree <src> <parent> [title] [--dry-run]` | Copy page tree |

### Profiles / misc

| Slash | CLI | Description |
|-------|-----|-------------|
| `/confluence_profile_list` | `confluence profile list` | List profiles |
| `/confluence_profile_use` | `confluence profile use <name>` | Switch profile |
| `/confluence_convert` | `confluence convert -i in.md -o out.xml --input-format markdown --output-format storage` | Offline convert |
| `/confluence_api` | `confluence api <endpoint> …` | Raw REST helper |

Global: `confluence --profile staging <command>`.

## Page IDs

Accept numeric IDs or Confluence URLs (`?pageId=`, `/pages/<id>/…`). Prefer ID or
`/pages/<id>` over `/display/<space>/<title>`.

## List all pages in a space

**Do not** paginate with `confluence search … --start N` (or `content/search?…&start=N`)
on Confluence Cloud — the offset is often ignored → same page of results forever →
infinite loops / huge delays.

Use the content list API and bump `start` while `len(results) == limit`:

```bash
confluence api "content?spaceKey=KEY&type=page&limit=50&start=0"
confluence api "content?spaceKey=KEY&type=page&limit=50&start=50"
# … until fewer than 50 results
```

If you must use `content/search`, follow `_links.next` (cursor), never a bare `start`.

## Agent tips

- Run `eval "$(python scripts/skill_env.py)"` once per shell before `confluence …`.
- Destructive commands: always pass `--yes`.
- Prefer `--format markdown` for agent text; `--format json` for parsing.
- Read-only agents: `CONFLUENCE_READ_ONLY=true` in the workspace `.env`.
- Folders have no body — use `info`, not `read`/`edit`.
- **Never** use `confluence search --start` to crawl a whole space — see
  [List all pages in a space](#list-all-pages-in-a-space).
- Full reference: `confluence --help` / [confluence-cli](https://www.npmjs.com/package/confluence-cli).

## Notes

- Never commit `.env` or API tokens.
