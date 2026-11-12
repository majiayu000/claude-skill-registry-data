---
name: nextjs-conventions
description: Apply Next.js conventions for schema-validated input, Server Components by default, Server Actions with typed results, forward-only migrations, and consented analytics. Use when writing or reviewing Next.js app code or next.config files.
license: MIT
compatibility: "Claude Code"
---

# Shared Next.js and web conventions

- Validate every input from forms and APIs with a schema validator (for example Zod with `.safeParse()`).
- Default to Server Components. Use `'use client'` only for state or event handling.
- Prefer Server Actions over API routes when possible. Return `{ ok: true, data? } | { ok: false, error }`, where `error` is the `{ code, message, details? }` object from `developer-os:error-handling-conventions`.
- Follow the project's migration policy; if it declares none, write forward-only migrations.
- When the project has a `DESIGN.md`, record in `docs/decisions/` which side is the source of truth for tokens (`DESIGN.md` generating the Tailwind theme, or the reverse), and keep the other in sync.
- Route analytics calls through the project's tracking wrapper when one exists, behind a consent gate where the platform requires consent.
