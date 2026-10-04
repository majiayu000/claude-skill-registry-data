---
name: knowledge-bases
description: Manage Frontline knowledge bases from the CLI — create/list/update/delete KBs, add and resync sources (URLs and website crawls), inspect crawl sync history, run semantic search, and assign KBs to agents. Use when the user wants to feed documents/URLs into a knowledge base, search indexed content, or control which agent uses which KB. Does not handle file uploads.
allowed-tools: Bash(frontline:*)
---

# Knowledge Bases

A knowledge base (KB) is a searchable collection of indexed content. Content comes from
**sources**: URLs and website crawls (file uploads are not available via the CLI). KBs can be
**shared** (assignable to agents) or **private**. Requires a USER API key (same key as
conversations and playbooks).

Output is JSON by default; add `--table` (or `--pretty`) for a human-readable view. List
commands (`kb list`, `kb source list`, `kb sync-history`) are paginated — pass `--page` /
`--page-size` and read the `{ results, total, pageNum, pageSize, totalPages }` envelope.

## Knowledge base CRUD

```bash
frontline kb list --table                 # all KBs (add --shared / --private to filter)
frontline kb list --search-text "docs"
frontline kb create --name "Help Center" --description "Public docs"
frontline kb create --name "Scratch" --private
frontline kb get 12
frontline kb update 12 --name "Help Center v2"
frontline kb delete 12                     # deletes the KB and all its sources
```

Default knowledge bases cannot be deleted.

## Sources

Sources live under `frontline kb source`. List, inspect, add, resync, and remove them.

```bash
frontline kb source list 12 --table
frontline kb source get 12 340

# Add URL sources (fetched + indexed asynchronously)
frontline kb source add-url 12 --urls '["https://docs.example.com/faq"]' \
  --description "FAQ pages"

# Start a website crawl (discovers + indexes pages under the root URL)
# --max-links is required (1-1000); --max-depth is optional (1-5)
frontline kb source add-crawl 12 --url "https://docs.example.com" \
  --max-links 50 --max-depth 3 \
  --include-paths '["/docs"]' --exclude-paths '["/blog"]'

# Resync URL/web-page sources by id
frontline kb source resync 12 --source-ids '[340,341]'

# Recrawl a website source (use the website source id, not a source id)
frontline kb source resync 12 --website-id 88

# Remove sources
frontline kb source remove 12 --source-ids '[340]'
```

`resync` requires exactly one of `--source-ids` or `--website-id` (passing neither errors):
use `--source-ids` to re-index individual URL/web-page sources, or `--website-id` to recrawl a
website source.

## Filter values

The filter flags expect these exact enum values:

- `kb source list --source-type`: `FILE`, `URL`, `WEBPAGE`, `FOLDER` (also `ARTICLE`, `QNA`, `UNKNOWN`)
- `kb source list --status`: `NONE`, `PROCESSING`, `COMPLETED`, `FAILED`, `DELETING`, `DELETED`, `SYNCING`, `REJECTED`
- `kb sync-history --status`: `PROCESSING`, `SYNCING`, `COMPLETED`, `FAILED`, `DELETING`, `DELETED`
- `kb sync-history --sync-type`: `INITIAL_SYNC`, `MANUAL_RESYNC`, `AUTO_RESYNC`

## Website crawl sync history

Each website crawl produces sync summaries (one per crawl run). Look them up by KB id and
website source id:

```bash
frontline kb sync-history 12 88 --table
frontline kb sync-history 12 88 --status FAILED
```

## Search

Semantic search over a KB's indexed content. Returns chunks with similarity scores. A KB with
no indexed sources yet returns an empty `results` array.

```bash
frontline kb search 12 --query "what is the refund policy" --limit 5
```

## Assigning KBs to agents

Only shared KBs can be assigned. `assign` replaces the agent's full set of assigned KBs.

```bash
frontline kb assigned --agent-id <agentId>
frontline kb assign --agent-id <agentId> --kb-ids '[12,13]'
frontline kb assign --agent-id <agentId> --kb-ids '[]'   # unassign all
```

## See also

- Resolving an agent's `<agentId>` for `assign`/`assigned`: the `frontline-agents` skill.
- Authentication and profiles: the `auth-and-profiles` skill.
- Full reference: <https://docs.getfrontline.ai/cli>.
