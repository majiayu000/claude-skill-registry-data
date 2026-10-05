---
name: context7
description: Use Context7 for current, version-specific library and framework documentation. Trigger when the user asks about package APIs, framework setup, SDK usage, migrations, deprecations, or says "use context7".
source: https://context7.com/
---

# Context7

Use Context7 whenever current library, framework, SDK, CLI, or API documentation could affect the answer or implementation.

## When To Use

- The user says `use context7`, `context7`, or asks for latest/current docs.
- The task involves package APIs, framework configuration, SDK usage, migrations, deprecations, or version-specific behavior.
- You are unsure whether training-data knowledge is current enough.

## How To Use

1. Identify the library, framework, package, SDK, or tool and its version when available.
2. Query Context7 documentation for the relevant library before giving code or making edits.
3. Prefer version-specific examples and cite the library ID or documentation source in your reasoning when useful.
4. If Context7 is not available in the current tool surface, use the official docs directly and mention that Context7 was not callable from this session.

## Prompt Pattern

Use requests like:

```text
use context7 for Next.js 15 middleware examples
use context7 with /vercel/next.js for app router setup
use context7 for Prisma relation query examples
```

