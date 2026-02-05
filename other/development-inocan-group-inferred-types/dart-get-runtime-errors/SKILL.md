---
name: dart-get-runtime-errors
description: "To read recent runtime errors from a running Dart or Flutter app, fetch runtime errors after connecting to the Dart Tooling Daemon."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"get_runtime_errors","arguments":{}}
```

## Tool Description
Retrieves the most recent runtime errors that have occurred in the active Dart or Flutter application. Requires "connect_dart_tooling_daemon" to be successfully called first.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "clearRuntimeErrors": {
      "type": "boolean",
      "title": "Whether to clear the runtime errors after retrieving them.",
      "description": "This is useful to clear out old errors that may no longer be relevant before reading them again."
    }
  }
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
