---
name: dart-get-active-location
description: "To get the current cursor location from the connected editor, retrieve the active location after connecting to the Dart Tooling Daemon."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"get_active_location","arguments":{}}
```

## Tool Description
Retrieves the current active location (e.g., cursor position) in the connected editor. Requires "connect_dart_tooling_daemon" to be successfully called first.

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
