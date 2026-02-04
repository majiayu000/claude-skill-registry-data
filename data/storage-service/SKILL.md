---
name: storage-service
description: Patterns for persisting and retrieving application data. Use when implementing data persistence, caching, or session management.
license: MIT
metadata:
  author: AI Agents
  version: "1.0"
---

## When to use this skill

Use this skill when you need to persist application state, cache data, or manage sessions in the browser. Covers data persistence strategies and best practices.

For detailed patterns, examples and implementation guidance, see [references/REFERENCE.md](references/REFERENCE.md).

For project-specific storage implementation details, refer to `.context/CLAUDE.md` or `.context/COPILOT.md`.

  this._singers = await storage.getAllSingers();
} catch (err) {
  console.error('Failed to load singers', err);
}
```
