---
name: dart-set-widget-selection-mode
description: "To enable or disable widget selection mode in a running Flutter app, set selection mode after connecting to the Dart Tooling Daemon."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"set_widget_selection_mode","arguments":{}}
```

## Tool Description
Enables or disables widget selection mode in the active Flutter application. Requires "connect_dart_tooling_daemon" to be successfully called first.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "enabled": {
      "type": "boolean",
      "title": "Enable widget selection mode"
    }
  },
  "required": [
    "enabled"
  ]
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
