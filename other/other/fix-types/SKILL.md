---
name: fix-types
description: "[Fix & Debug] ⚡ Fix type errors"
infer: true
---

Run `bun run typecheck` or `tsc` or `npx tsc` and fix all type errors.

## ⚠️ Anti-Hallucination Reminder

**Before modifying ANY code:** Verify assumptions with actual code evidence. Search for usages, read implementations, trace dependencies. If confidence < 90% on any change, investigate first or ask user. See `.claude/skills/shared/anti-hallucination-protocol.md` for full protocol.

## Rules
- Fix all of type errors and repeat the process until there are no more type errors.
- Do not use `any` just to pass the type check.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
