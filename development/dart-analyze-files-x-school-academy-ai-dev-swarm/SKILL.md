---
name: dart-analyze-files
description: "To run static analysis across a Dart or Flutter project, analyze files to find compile and lint errors."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"analyze_files","arguments":{}}
```

## Tool Description
Analyzes the entire project for errors.

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
