---
name: search-hexdocs
description: Search Hex package documentation for Elixir/Erlang.
compatibility: Requires Node.js 18+. Run `npm install` in {baseDir}/scripts first.
---

# Search hexdocs

Search [hexdocs.pm](https://hexdocs.pm) documentation.

## Usage

```bash
{baseDir}/scripts/hexdocs.js <QUERY> [OPTIONS]
```

## Examples

```bash
# Search all packages
{baseDir}/scripts/hexdocs.js "GenServer callbacks"

# Filter by package
{baseDir}/scripts/hexdocs.js "Ecto.Query" --packages ecto

# Multiple packages
{baseDir}/scripts/hexdocs.js "LiveView hooks" --packages phoenix_live_view,phoenix

# Limit results
{baseDir}/scripts/hexdocs.js "plug conn" --limit 5

# JSON output
{baseDir}/scripts/hexdocs.js "json encode" --packages jason --json
```

## Output Format

```
Results: 42 (showing 10)

<result index="0" package="phoenix" ref="Phoenix.Controller.html#json/2" title="json/2">
Sends JSON response...
</result>
```
