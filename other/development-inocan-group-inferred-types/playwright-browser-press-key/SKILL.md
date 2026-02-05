---
name: playwright-browser-press-key
description: "To press a keyboard key in the page, send a key press for shortcuts or input behavior."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_press_key","arguments":{}}
```

## Tool Description
Press a key on the keyboard

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "key": {
      "type": "string",
      "description": "Name of the key to press or a character to generate, such as `ArrowLeft` or `a`"
    }
  },
  "required": [
    "key"
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
