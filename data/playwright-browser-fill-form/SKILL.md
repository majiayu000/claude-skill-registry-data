---
name: playwright-browser-fill-form
description: "To fill multiple form fields at once, set values for inputs, checkboxes, and selects in a single call."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_fill_form","arguments":{}}
```

## Tool Description
Fill multiple form fields

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Human-readable field name"
          },
          "type": {
            "type": "string",
            "enum": [
              "textbox",
              "checkbox",
              "radio",
              "combobox",
              "slider"
            ],
            "description": "Type of the field"
          },
          "ref": {
            "type": "string",
            "description": "Exact target field reference from the page snapshot"
          },
          "value": {
            "type": "string",
            "description": "Value to fill in the field. If the field is a checkbox, the value should be `true` or `false`. If the field is a combobox, the value should be the text of the option."
          }
        },
        "required": [
          "name",
          "type",
          "ref",
          "value"
        ],
        "additionalProperties": false
      },
      "description": "Fields to fill in"
    }
  },
  "required": [
    "fields"
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
