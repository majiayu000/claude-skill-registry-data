---
name: dart-dart-format
description: "To format Dart code consistently, run `dart format .` on the given roots to apply standard formatting."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"dart_format","arguments":{}}
```

## Tool Description
Runs `dart format .` for the given project roots.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
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
          },
          "paths": {
            "type": "array",
            "title": "Paths to run this tool on. Must resolve to a path that is within the \"root\".",
            "items": {
              "type": "string"
            }
          }
        },
        "required": [
          "root"
        ]
      }
    }
  }
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
