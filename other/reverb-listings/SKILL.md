---
name: reverb-listings
description: "Reverb: Create, read, update, and delete your instrument listings."
metadata:
  version: 0.1.0-alpha.2
  openclaw:
    category: "productivity"
    requires:
      bins:
        - revcli
    cliHelp: "revcli listings --help"
---

# listings

> **AUTH:** Set `REVERB_API_KEY` to your personal API key (from reverb.com/my/api_access) or store it with
`revcli auth set-key`.

```bash
revcli listings <method> [flags]
```

## Helper Commands

| Command                                       | Description                     |
|-----------------------------------------------|---------------------------------|
| [`+draft`](../reverb-listings-draft/SKILL.md) | Create a listing in draft state |

## Methods

| Method   | HTTP   | Path             | Description                     |
|----------|--------|------------------|---------------------------------|
| `list`   | GET    | `/listings`      | Search and browse your listings |
| `get`    | GET    | `/listings/{id}` | Fetch a single listing by ID    |
| `create` | POST   | `/listings`      | Create a new listing            |
| `update` | PUT    | `/listings/{id}` | Update an existing listing      |
| `delete` | DELETE | `/listings/{id}` | Delete a listing                |

## Global Flags

| Flag                | Default | Description                                          |
|---------------------|---------|------------------------------------------------------|
| `--params <JSON>`   | —       | URL path / query parameters as a JSON object         |
| `--json <JSON>`     | —       | Request body as a JSON object                        |
| `--format <FORMAT>` | `json`  | Output format: `json`, `table`, `yaml`, `csv`        |
| `--output <PATH>`   | —       | Write output to a file (relative path, no traversal) |
| `--page-all`        | —       | Paginate through all results (NDJSON output)         |
| `--page-limit <N>`  | `10`    | Max pages when using `--page-all`                    |
| `--page-delay <MS>` | `100`   | Milliseconds between pages                           |
| `--per-page <N>`    | —       | Results per page                                     |
| `--dry-run`         | —       | Validate and print the request without sending       |

## Discovering Commands

```bash
# Inspect available methods
revcli schema listings

# Inspect a specific method's parameters
revcli schema listings.list

# List all available resources
revcli --list-resources
```
