---
name: m8m-mcp-connection-builder
description: Author reusable MCP connection context and usage guides locally, then deliver an authorized installation to the configured M8M tenant's persistent server installer. Use for new connections or explicit version changes.
metadata:
  version: "2.2.0"
---

# M8M MCP connection builder

Understand the requested service/endpoint or source, intended consumers, tools
and use cases. Author a semantic brief and a complete Markdown usage guide that
explains when to read which tools, how to interpret their results and how to
answer when data is missing. Preserve source, dependencies and requested scope.
Ordinary authoring returns local material; an installation request authorizes
handoff to the exact configured tenant's server installer.

Read [server delivery](references/server-delivery.md) for export or installation.
The bundled shared client uses Python's standard library and needs no platform
checkout. Use its generic `bundle` export for selected context. Do not require
a universal connection manifest, invent another client protocol or directly edit
server workers. Keep credentials and local live session state out of delivery.
Authentication requirements are references to approved private server resources.

The server `$m8m-server-installer` discovers actual services and installed versions,
inspects exact contracts and grants, prepares the destination definition, registers
its immutable version and binds a supported consumer only when requested. Initial
support is approved remote Streamable HTTP with read-only JSON tools for staff
Tasks. Other consumers, OAuth setup and deploying a new daemon from source remain
requirements until actual server capability exists. An endpoint or tool list alone
does not establish usability. Do not silently change the intended consumer.

Inspect/reuse the exact selected installed identity before proposing an upgrade.
Preserve complete usage instructions and tool/resource requirements. The server
resolves semantic references against its actual scoped catalog; unknown source
permissions and incompatible contracts remain visible blockers.

Follow the same saved operation through submit/status/continue and lost-response
retries. Report installation from its actual receipt, exact connection/version,
tool scope, consumer binding, verification and unresolved requirements. Installing
a connection does not select a playbook, enable customer replies, start a Task,
publish content or activate a schedule.
