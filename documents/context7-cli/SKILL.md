---
name: context7-cli
description: Use the local Context7 CLI in this repo to search libraries and fetch Context7 context for skills or documentation tasks. Trigger when you need to run `c7 search`/`c7 context`, resolve library IDs, or retrieve text/json outputs from Context7 via the CLI.
---

# Context7 CLI

## Overview

Use the local `agent-skills` CLI (subcommand `c7`) to query Context7 for library discovery and context snippets. Prefer this tool when a task needs authoritative library context and you want a deterministic CLI output that can be piped into downstream steps.

## Quick Start

1. Ensure `CONTEXT7_API_KEY` is set or pass `--api-key`.
2. If `agent-skills` is already installed, use it directly:

```bash
command -v agent-skills
agent-skills c7 search --library-name react --query "useEffect cleanup"
```

3. Otherwise, run the CLI from the repo:

```bash
go run ./cmd/agent-skills c7 search --library-name react --query "useEffect cleanup"
```

For repeated calls, build once:

```bash
go build -o bin/agent-skills ./cmd/agent-skills
./bin/agent-skills c7 context --library-id /facebook/react --query "useEffect cleanup"
```

Or install remotely (requires Go) only if the binary is missing:

```bash
if ! command -v agent-skills >/dev/null 2>&1; then
  go install github.com/strantalis/agent-skills/cmd/agent-skills@latest
fi
agent-skills c7 search --library-name react --query "useEffect cleanup"
```

## Tasks

### Search for libraries

Use this to discover candidate library IDs.

```bash
go run ./cmd/agent-skills c7 search --library-name react --query "useEffect cleanup"
```

- Default output is JSON. Use `--format jsonl` for JSON lines or `--format text` for tab-separated lines.
- Use `--limit` to reduce results when you only need the top few.

### Fetch context

Prefer explicit `--library-id` for determinism.

```bash
go run ./cmd/agent-skills c7 context --library-id /facebook/react --query "useEffect cleanup"
```

If you only have a name, you may use `--library-name`. If multiple libraries match, use `--select=interactive` or `--select=first`, or provide `--library-id` for determinism.

```bash
go run ./cmd/agent-skills c7 context --library-name react --query "useEffect cleanup"
```

## Output formats

- Use `--format json` when another tool or step needs structured output.
- Use `--format jsonl` for streaming or piping one JSON object per line.
- Use `--format text` for direct reading or quick copy/paste.

## Flags (global to `c7`)

- `--api-key` (or `CONTEXT7_API_KEY`): Context7 API key.
- `--base-url`: Override the Context7 base URL.
- `--timeout`: HTTP timeout (default 30s).
- `--retries`: Retry count for 202/429/5xx responses.
- `--cache-dir`: Enable disk cache when set.
- `--cache-ttl`: Cache TTL (default 24h, only used when cache-dir is set).

## Troubleshooting

- 401/403: Missing or invalid API key. Set `CONTEXT7_API_KEY` or pass `--api-key`.
- 429: Rate limited. The client retries automatically; reduce request rate if persistent.
- 202: Context is still processing; retries will handle this automatically.

## Reference

See `references/api_reference.md` for the full command reference and examples.
