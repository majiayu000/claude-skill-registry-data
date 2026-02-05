---
name: playwright-browser-tabs
description: "To manage browser tabs, list, create, select, or close Playwright tabs."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_tabs","arguments":{}}
```

## Tool Description
List, create, close, or select a browser tab.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "list",
        "new",
        "close",
        "select"
      ],
      "description": "Operation to perform"
    },
    "index": {
      "type": "number",
      "description": "Tab index, used for close/select. If omitted for close, current tab is closed."
    }
  },
  "required": [
    "action"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"playwright","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
