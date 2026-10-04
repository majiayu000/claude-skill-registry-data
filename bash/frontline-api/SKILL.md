---
name: frontline-api
allowed-tools: Bash(frontline:*)
description: Make raw HTTP requests to the Frontline Public API using the Frontline CLI. Use as an escape hatch when a specific endpoint does not have a dedicated CLI command, or when exploring the API.
---

## Prerequisites

- The `frontline` CLI must be installed (`npm i -g @getfrontline/cli`).
- The user must be authenticated (`frontline auth login`).

## Commands

### Make a raw API GET request

```bash
frontline api raw get <path> [--query <key=value>...] [--debug]
```

| Flag                 | Description                                                                     |
| -------------------- | ------------------------------------------------------------------------------- |
| `<path>`             | **(required)** API path relative to the base URL (e.g. `/agents`, `/workflows`) |
| `--query <pairs...>` | Query parameters as `key=value` pairs (repeatable)                              |
| `--api-key <key>`    | Override the stored API key for this request                                    |
| `--profile <name>`   | Use a specific CLI profile                                                      |
| `--debug`            | Show HTTP request/response diagnostics                                          |

Output is always the raw JSON response — there is no `--json`/`--pretty` flag here.

**Important:** Only `GET` requests are supported currently. Passing any other method will result in an error.

**Example:**

```bash
# Raw GET request to the agents endpoint
frontline api raw get /agents

# Raw GET with query parameters
frontline api raw get /agents --query status=active --query limit=10

# With debug output to see full request details
frontline api raw get /billing --debug
```

**Output:** JSON on stdout (`{ ok: true, data: … }` when the endpoint uses the SOR envelope).

## When to use this skill

- When you need to access an API endpoint that does not have a dedicated CLI command.
- When you want to explore the API response structure.
- When building automation scripts that need raw API data.

## Discovering available endpoints

Run `frontline --help` to see all available commands. If a resource is not listed, you can try calling it directly via `frontline api raw get /resource-name`.

## Troubleshooting

- **"No API key found"**: run `frontline auth login` to authenticate.
- **"Only GET requests are supported"**: the raw API command currently only supports GET. POST/PUT/DELETE are not yet available.
- Use `--debug` to see the full HTTP request URL, headers, and response status for diagnosing issues.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
