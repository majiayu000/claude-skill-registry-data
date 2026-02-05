---
name: dart-pub
description: "To run Dart or Flutter pub commands like `pub get` or `pub add`, execute a pub command for the given roots."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"pub","arguments":{}}
```

## Tool Description
Runs a pub command for the given project roots, like `dart pub get` or `flutter pub add`.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "title": "The pub command to run.",
      "description": "Currently only `add`, `get`, `remove`, and `upgrade` are supported."
    },
    "packageName": {
      "type": "string",
      "title": "The package name to run the command for.",
      "description": "This is required for the `add`, and `remove` commands."
    },
    "roots": {
      "type": "array",
      "title": "All projects roots to run this tool in.",
      "items": {
        "type": "object",
        "properties": {
          "root": {
            "type": "string",
            "title": "The file URI of the project root to run this tool in.",
            "description": "This must be equal to or a subdirectory of one of the roots allowed by the client. Must be a URI with a `file:` scheme (e.g. file:///absolute/path/to/root)."
          }
        },
        "required": [
          "root"
        ]
      }
    }
  },
  "required": [
    "command"
  ]
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
