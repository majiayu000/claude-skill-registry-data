---
name: vkc-repo-guardrails
description: Enforce Viet K-Connect non-negotiables (no Server Actions, API Routes only, Drizzle/Supabase patterns, TanStack Query repo layer, i18n ko/en/vi key parity). Use before/after code changes and for PR review checklists.
metadata:
  short-description: Repo guardrails + checks
---

# Viet K-Connect Repo Guardrails

## When to use

- You’re about to implement or review changes in this repo.
- You need a repeatable “PR checklist” to prevent architecture drift.

## Quick start

1) Run local checks:
- `bash .codex/skills/vkc-repo-guardrails/scripts/guardrails.sh`
2) If it fails, fix violations first (especially Server Actions / i18n key drift).
3) For new work, follow the VKC prompt protocol: `docs/CODEX_PROMPT_PROTOCOL.md`

## Non‑negotiables (must keep)

- **No Server Actions**: never add `"use server"`.
- **Server code lives in API Routes**: only `src/app/api/**`.
- **DB access**: Drizzle via `@/lib/db` + `@/lib/db/schema`.
- **Client data layer**: `src/repo/<domain>/{fetch,query,mutation,types}.ts` + query keys in `src/repo/keys.ts`.
- **i18n**: `messages/{ko,vi}.json` keys stay in sync; `en` is allowed to be partial (ko fallback).
- **Imports**: prefer `@/*` alias; avoid deep `../` chains for shared modules/components.
- **Components**: ATOMIC folders + `export default` component pattern.

## Where to look (canonical examples)

- API (user): `src/app/api/reports/route.ts`
- API (admin): `src/app/api/admin/news/route.ts`
- Responses: `src/lib/api/response.ts`
- Rate limit helper: `src/lib/api/rateLimit.ts`
- Repo structure rules: `docs/REPO_STRUCTURE_GUIDE.md`

## Expected PR output (what to report)

- Guardrails result: `PASS` / `FAIL` + concrete violations
- i18n parity: `PASS` / `FAIL`
- Any intentional deviations: explicit rationale + follow-up task

## References

- Repo architecture pointers: `.codex/skills/vkc-repo-guardrails/references/architecture.md`
- Conventions checklist: `.codex/skills/vkc-repo-guardrails/references/conventions.md`
