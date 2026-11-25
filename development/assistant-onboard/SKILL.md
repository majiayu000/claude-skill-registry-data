---
name: assistant-onboard
description: "Map an unfamiliar codebase and its patterns. Use for onboarding, project orientation, or explicit codebase-learning requests."
---

# Map the Codebase

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Build a useful, scoped orientation from inspected source. Infer the project and focus from context; ask only when a missing choice materially changes the inspection. Keep onboarding read-only for production code.

- Read project instructions, README/docs, build manifests, and relevant CI configuration. Identify purpose, stack, structure, and source-backed build, test, and run commands. Batch independent reads when supported.
- Load [inventory.md](inventory.md) only when the user asks for size or language counts, or the repository is unfamiliar and large.
- Trace the entry points and representative paths relevant to the requested depth. Map module responsibilities, data flow, configuration, and external dependencies. Follow important ownership, lifecycle, cancellation, and failure boundaries where they affect understanding.
- Sample enough representative source and tests to identify conventions with concrete file examples. Inspect existing helpers and patterns before suggesting future change points.
- Report relevant risks and gaps: for example permissions, persistence, integrations, resource ownership, or weak verification. Include semantic type or design-pressure observations only where inspected evidence makes them useful; project size does not require candidate arrays or a redesign.

Return a concise map with key paths and their roles, entry points, commands, conventions, relevant risks, likely change points, and coverage limits. Distinguish observed facts from assumptions and uninspected areas; do not claim full coverage from a sample. Ask specific questions about material domain gaps instead of generic follow-ups.

Use local, read-only discovery. Do not install analyzers, upload source, or use external services without authorization. Do not create orientation or memory files unless the user or applicable project policy authorizes persistence. Use the authorized path, preserve existing user notes, and keep credentials, customer data, private endpoints, and transient task state out of durable notes. Otherwise return the map in the conversation.

For a refresh, read any policy-allowed existing orientation and inspect relevant changes since its recorded source/date. Update only stable facts within the authorized scope. Report inaccessible areas and stop before code changes.
