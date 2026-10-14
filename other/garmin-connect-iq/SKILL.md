---
name: garmin-connect-iq
description: Use when developing, debugging, or answering API questions about Garmin Connect IQ apps, Monkey C, or the Toybox API.
---

# Garmin Connect IQ

Use Garmin's current Connect IQ API reference before relying on memory. This public skill does not redistribute Garmin's API documentation; create a local mirror only for personal development use under Garmin's terms.

## API reference

- Start with [Garmin's Connect IQ API documentation](https://developer.garmin.com/connect-iq/api-docs/) for module discovery.
- If a local mirror has been created, use its class and method indexes and search `references/api-docs/Toybox/` when the owning module is unknown.
- Treat availability annotations, supported devices, API levels, permissions, and deprecation notices in the local pages as authoritative for implementation choices.

To create or refresh a private local mirror, run `powershell -File scripts/sync-api-docs.ps1` from this skill directory, review Garmin's current developer agreement, and then validate the skill and local links. Do not commit or redistribute the generated `references/api-docs/` directory.
