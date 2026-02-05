---
name: protoc
description: Re-generates the project's code from protobuf source. Use when .proto files are changed.
---

- Run `scripts/server` to re-generate Protobuf files. No custom commands.
- The process uses `protoc` and the relevant plugins to generate code for both server and client sides.
- The process does not automatically exit, so ensure to terminate it manually after generation is complete. Wait for the output "Server started" and then stop the process.
- Always commit all the generated files, even when there are just comment changes.