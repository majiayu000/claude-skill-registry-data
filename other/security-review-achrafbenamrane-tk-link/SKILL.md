---
name: security-review
description: Review the current branch's diff against the project security checklist (SEC-* rules) and report findings with rule IDs + a verdict. Use before merging anything touching auth, storage, secrets, deep links, network, payments, or database migrations.
argument-hint: [base branch, default main]
allowed-tools: Read, Grep, Glob, Bash(git diff*), Bash(git log*), Bash(npm run secrets:check*)
---

## Context

- Changed vs base: !`git diff --stat ${ARGUMENTS:-main}...HEAD 2>/dev/null | tail -40 || git diff --stat HEAD`

## Task

Audit the diff against [`docs/security/checklist.md`](../../../docs/security/checklist.md) (the
`SEC-*` catalog) and [`docs/security/threat-model.md`](../../../docs/security/threat-model.md).
**Treat AI-written code like a junior dev's PR — be skeptical and check explicitly.**

1. Read `docs/security/checklist.md`. Run `npm run secrets:check`.
2. Diff the branch (`git diff ${ARGUMENTS:-main}...HEAD`). Prioritize files touching: secrets/env,
   `src/shared/lib/storage`, `src/shared/lib/supabase.ts`, `src/features/auth`, deep links
   (`+native-intent`, `deep-link.ts`), network calls, `supabase/migrations`, Edge Functions.
3. For each relevant rule, evaluate the change. **Explicitly verify** the high-leverage ones:
   - No secret in source/bundle or a secret-looking `EXPO_PUBLIC_*` (SEC-SECRET-\*).
   - All persistence via `@/shared/lib/storage`; secrets not in `appStorage` (SEC-STORE-\*).
   - New tables have RLS + owner-scoped policies + `WITH CHECK`; never trust the client (SEC-RLS-001).
   - Inputs Zod-validated; deep-link params not trusted for authz (SEC-INPUT-001, SEC-LINK-\*).
4. Report each finding on one line: `[P1|P2|P3] SEC-ID — file:line — issue — concrete fix`.
5. End with `## Verdict: APPROVE | REQUEST-CHANGES` (any P1 ⇒ REQUEST-CHANGES). Under `## Harness:`
   propose a lint rule / test / hook for any finding likely to recur.

Return the findings + verdict + harness proposals only — keep exploration out of the summary.
