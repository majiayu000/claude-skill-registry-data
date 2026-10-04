---
name: A2A JSON-RPC Call
skill_key: a2a_call
description: Call a peer agent's A2A JSON-RPC endpoint. Supports tasks/send (send a task message) and tasks/get (query task status).
runner:
  kind: python_file
  target: a2a_call.py
requires:
  always: true
---

This skill invokes A2A JSON-RPC methods on a remote agent endpoint.

**Input parameters** (via stdin JSON):
- `url` (string, required): The peer's A2A JSON-RPC endpoint URL.
- `method` (string, required): `"tasks/send"` or `"tasks/get"`.
- `task_id` (string, optional): Required for `tasks/get`. The task ID to query.
- `message_text` (string, optional): For `tasks/send` — a text message to include.
- `message_data` (object, optional): For `tasks/send` — a data payload to include.
- `skill_id` (string, optional): For `tasks/send` — the target skill ID on the peer agent.
- `metadata` (object, optional): Extra metadata to attach to the request.

**Output** (stdout JSON):
- `ok` (bool): Whether the call succeeded.
- `result` (object): The JSON-RPC result on success.
- `error` (string): Error message on failure.
