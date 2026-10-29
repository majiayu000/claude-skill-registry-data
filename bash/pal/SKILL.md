---
name: pal
description: Use the `pal` MCP server via MCPorter (with optional keep-alive daemon for multi-turn tools).
---

# Pal MCP

Use this skill to list or call tools exposed by the `pal` MCP server through
the bundled MCPorter wrapper.

## Call tools

List the server's tools:

```bash
bash "scripts/mcp" list
```

Call a tool by its short name. Pass arguments as JSON:

```bash
bash "scripts/mcp" call <tool> --output json --args '{"key":"value"}'
```

The wrapper prefixes short names with `pal.`. It also accepts a fully qualified
`server.tool` name or an HTTP URL when a specific target is needed. Run
`bash "scripts/mcp" --help` for wrapper usage.

## Continue multi-turn calls

When a PAL tool returns a `continuation_id`, make the next call through this
wrapper. Its MCPorter configuration uses the daemon-managed `keep-alive`
lifecycle, which reuses the server process and its in-memory continuation state
between calls. This lifecycle is required for those multi-turn flows.

## Configure the server

The wrapper uses `npx` to run the pinned MCPorter version by default. The
server configuration is in [`mcporter.json`](mcporter.json).

| Variable | Effect |
| --- | --- |
| `MCPORTER_BIN` | Use this local MCPorter executable from `PATH` instead of `npx` (for example, `mcporter`). |
| `PAL_UVX_BIN` | Use this `uvx` executable path to launch PAL. When unset, the config searches `PATH` and common install paths. |
| `PAL_MCP_FROM` | Override the source from which `uvx` fetches the PAL server. |
| `PAL_DEFAULT_MODEL` | Set PAL's `DEFAULT_MODEL`; defaults to `auto`. |

The default launch requires `npx`, Node, `uvx`, and network access to the
configured server source. PAL also needs the provider credentials required by
the selected model in its environment, such as `OPENAI_API_KEY`,
`GEMINI_API_KEY`, or `OPENROUTER_API_KEY`.

## Check the connection

Run the self-test to list PAL tools and call its `version` tool:

```bash
bash "scripts/selftest"
```
