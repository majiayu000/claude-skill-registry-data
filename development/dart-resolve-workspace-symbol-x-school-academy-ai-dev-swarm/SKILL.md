---
name: dart-resolve-workspace-symbol
description: "To search for symbols across Dart workspaces, resolve a symbol name to find definitions or catch spelling errors."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"resolve_workspace_symbol","arguments":{}}
```

## Tool Description
Look up a symbol or symbols in all workspaces by name. Can be used to validate that a symbol exists or discover small spelling mistakes, since the search is fuzzy.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "description": "Returns all close matches to the query, with their names and locations. Be sure to check the name of the responses to ensure it looks like the thing you were searching for.",
  "properties": {
    "query": {
      "type": "string",
      "description": "Queries are matched based on a case-insensitive partial name match, and do not support complex pattern matching, regexes, or scoped lookups."
    }
  },
  "required": [
    "query"
  ]
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
