---
name: pmctl
description: Browse and inspect Postman collections, requests, and environments from the terminal using pmctl. Use when you need to discover API endpoints, look up request details (method, URL, headers, body, query params), resolve environment variables to real base URLs, or construct curl commands from Postman data. Works with any Postman workspace. Requires pmctl to be installed (`pip install pmctl`).
---

# pmctl — Postman CLI for API Discovery

`pmctl` wraps the Postman API to let you browse collections, inspect requests, and resolve environment variables from the terminal. Use it to discover endpoints, construct curl commands, and understand APIs without opening the Postman GUI.

**Install:** `pip install pmctl`
**Source:** [github.com/wbingli/pmctl](https://github.com/wbingli/pmctl)

## Setup

```bash
# Add a profile with your Postman API key
pmctl profile add <name> --api-key "PMAK-..." --default

# Set a default workspace (scopes list commands)
pmctl profile set-workspace <workspace-id>

# Verify
pmctl profile whoami
```

Get an API key at https://go.postman.co/settings/me/api-keys

## Commands

### Profiles

```bash
pmctl profile list                          # List profiles
pmctl profile add <name> -k "PMAK-..." -d  # Add (--default)
pmctl profile switch <name>                 # Switch default
pmctl profile set-workspace <id>            # Set default workspace
pmctl profile remove <name>                 # Remove
pmctl profile whoami                        # Current user info
```

### Collections

```bash
pmctl collections list                      # List (scoped to default workspace)
pmctl collections list --all                # All workspaces
pmctl collections show <UID>                # Tree view of all requests
```

### Requests

```bash
# List all requests in a collection (flat table: method, name, path, URL)
pmctl requests list -c "Collection Name"
pmctl requests list -c <collection-uid>

# Fuzzy search (characters matched in order, e.g. "getCmp" matches "get Campaign")
pmctl requests list -c "My API" --search "getUser"

# Show request details (headers, body, query params, path variables)
pmctl requests show "request name" -c "Collection Name"
```

`-c` / `--collection` accepts a collection name (case-insensitive) or UID.
`requests show` uses case-insensitive substring match — use short terms.
`requests list --search` uses fuzzy matching (characters in order).

### Environments

```bash
pmctl environments list                     # List environments
pmctl environments show <name-or-id>       # Show variables
pmctl environments show <name> --full       # Full values (no truncation)
```

### Workspaces

```bash
pmctl workspaces list                       # List accessible workspaces
pmctl workspaces list --search "keyword"    # Filter by name
```

## Global Options

- `--json` — Machine-readable JSON output (works as global flag or per-subcommand)
- `--profile <name>` / `-p` — Use a specific profile instead of default

## Workflow: Resolve a Full API URL

Postman requests use `{{variable}}` placeholders. Resolve them via environments:

```bash
# 1. Get the request (shows URL like {{base-url}}/v1/users/:userId)
pmctl requests show "get User" -c "My API" --json

# 2. Resolve the variable for a specific environment
pmctl environments show "Production" --json | jq -r '.values[] | select(.key == "base-url") | .value'

# 3. Combine: replace {{base-url}} with resolved value, :userId with actual ID
```

## Workflow: Construct a curl Command

```bash
# Get full request details as JSON
REQ=$(pmctl requests show "create User" -c "My API" --json)

# Extract method, URL, headers, body
echo "$REQ" | jq '.[0].request | {method, url: .url.raw, headers: .header, body: .body.raw}'

# Get environment base URL
BASE=$(pmctl environments show "QA" --json | jq -r '.values[] | select(.key == "base-url") | .value')
```

## Workflow: Discover All Endpoints for a Topic

```bash
# Fuzzy search across a collection
pmctl requests list -c "My API" --search "user"

# Or browse the full tree
pmctl collections show <uid>
```

## Tips

- `--json` output is pipeable to `jq` for scripting
- `environments show --json` returns **unmasked** secrets — useful for scripting
- Collection names are matched case-insensitively; prefer names over UIDs for readability
- Multiple profiles let you manage separate Postman accounts (personal, work, etc.)
