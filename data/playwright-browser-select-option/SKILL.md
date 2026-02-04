---
name: playwright-browser-select-option
description: "To choose an option in a dropdown, select one or more values in a select element."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_select_option","arguments":{}}
```

## Tool Description
Select an option in a dropdown

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "element": {
      "type": "string",
      "description": "Human-readable element description used to obtain permission to interact with the element"
    },
    "ref": {
      "type": "string",
      "description": "Exact target element reference from the page snapshot"
    },
    "values": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Array of values to select in the dropdown. This can be a single value or multiple values."
    }
  },
  "required": [
    "element",
    "ref",
    "values"
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
