---
name: dart-get-selected-widget
description: "To find the currently selected Flutter widget in the running app, get the selected widget after connecting to the Dart Tooling Daemon."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"get_selected_widget","arguments":{}}
```

## Tool Description
Retrieves the selected widget from the active Flutter application. Requires "connect_dart_tooling_daemon" to be successfully called first.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
