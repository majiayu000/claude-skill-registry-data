---
name: tac-karpathy-discipline
description: >-
  Load before ANY non-trivial task in tac-express. Enforces four principles: Think-Before-Coding, Simplicity-First, Surgical-Changes, Goal-Driven-Execution. Includes TAC Express–specific checks, anti-patterns, and the violation response protocol.
---

# Karpathy Coding Protocol — TAC Express Edition

> Adapted from Andrej Karpathy's observations on LLM coding pitfalls.
> Bias: caution over speed. For trivial one-liners, use judgment — not every change needs full rigor.

---

## PRINCIPLE 1 — Think Before Coding

Don't assume. Don't hide confusion. Surface trade-offs.

**Before writing a single line:**
1. State assumptions explicitly. If uncertain about scope, data shape, or intent — ASK.
2. Surface ambiguity. If the request has multiple valid interpretations, present them. Never pick silently.
3. Push back when warranted. If a simpler approach exists, say so. If the ask violates The Fourteen Laws, name the violation and propose the compliant alternative.

**TAC Express checks BEFORE coding:**
- Which package does this belong in? (`packages/ui` / `packages/services` / `packages/database` / `apps/web` / `apps/dashboard`)
- Does this violate any of The Fourteen Laws?
- Is a forbidden package about to be installed?
- Is business logic ending up in a component instead of `packages/services`?
- Am I about to call Supabase directly from a component (LAW 6/8)?
- Does the status update need a TrackingEvent insert (ADR-004)?

```
❌ "Update the shipment status" → sets shipment.status directly
✅ Flags: ADR-004 says status is event-derived. Inserts a TrackingEvent instead.

❌ "Add a filter" → writes filter logic in the component
✅ Moves filter logic to packages/services, passes result as prop
```

---

## PRINCIPLE 2 — Simplicity First

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked
- No abstractions for single-use code
- No error handling for impossible scenarios
- If you write 200 lines and it could be 50 — rewrite it

**TAC Express–specific simplicity rules:**
- Don't pre-build multi-variant CVA components when only one variant is needed yet
- Don't create a service function for something called only once from one place
- Don't add loading/error states to a component that has no async data yet
- Don't add Zod schemas for data that isn't user-facing input yet
- Don't create new CSS tokens when existing ones already express the intent

---

## PRINCIPLE 3 — Surgical Changes

Touch only what you must. Clean up only your own mess.

**When editing existing files:**
- Do NOT "improve" adjacent code, comments, or formatting
- Do NOT refactor things that aren't broken
- Match existing style even if you'd do it differently
- If you notice unrelated dead code — mention it, don't delete it

**When YOUR changes create orphans:**
- Remove imports, variables, and functions that your changes made unused
- Do NOT remove pre-existing unused code unless explicitly asked

**TAC Express–specific surgical rules:**
- Don't reorder exports in `packages/ui/src/components/index.ts` unless the task requires it
- Don't rename CSS custom properties you didn't introduce
- Don't touch `apps/web/app/layout.tsx` fonts unless the task is font-related (ADR-005)
- Don't "clean up" `globals.css` tokens while fixing a layout bug
- Don't switch `var(--token)` to inline hex while "just fixing padding"

---

## PRINCIPLE 4 — Goal-Driven Execution

Define success criteria. Loop until verified.

Transform imperative tasks into verifiable goals:

| Instead of... | Transform to... |
|---------------|-----------------|
| "Add validation" | "Write tests for invalid inputs → make them pass" |
| "Fix the bug" | "Write a test that reproduces it → make it pass" |
| "Make it look better" | "Apply Violet Grid token pattern → verify no raw colors" |
| "Integrate the service" | "Mock at DB boundary → unit test passes → integration test passes" |

**TAC Express verification ladder (run in order):**
```
1. pnpm typecheck             → zero TypeScript errors
2. pnpm lint --max-warnings 0 → zero ESLint warnings
3. pnpm test                  → all tests pass
4. pnpm build                 → succeeds in all packages
5. Browser check              → feature works end-to-end in dev
6. Visual review              → Violet Grid token compliance, no hardcoded values
```

---

## Quick Decision Matrix

| Task Type | Mode | Apply Principles |
|-----------|------|-----------------|
| Obvious 1-liner / typo fix | Speed | 3 only |
| Bug fix | Caution | 1 + 3 + 4 |
| New feature | Full rigor | All 4 |
| Refactor | Caution | 1 + 2 + 3 + 4 |
| Code review | Full rigor | All 4 |
| Design/token change | Full rigor | 1 + 3 + Law compliance |

---

## Violation Response Protocol

When asked to do something that violates The Fourteen Laws:

```
"I can't do that — it violates [LAW X].

What you asked: [restate request]
Why it violates: [brief explanation]
Compliant approach: [concrete alternative]"
```

Never silently comply with a violation. Always name it and propose the fix.

---

## Worktree & artifact hygiene (end-of-session teardown)

> Added 2026-05-18 after the post-#162 follow-up surfaced an inert
> `tac-whatsapp-sends-102/` directory sitting at the repo root — a stale
> clone from a previous worktree-style session that nobody tore down.
> Inert directories at the repo root pollute grep, pollute `git status`,
> and make worktree-list inspection misleading.

### At the start of a session that creates a worktree

1. Use `git worktree add` to a path **outside the repo root**
   (`C:/tac/tw-<short-task-name>` is the established convention —
   see existing `tw-dod`, `tw-launch`, `tw-prodscope`, `tw-sb1` …)
   OR use the harness `Agent({ isolation: "worktree" })`, which
   auto-cleans on no-op.
2. Never `git clone` a sibling copy of the repo *inside* the primary
   clone's directory. The repo root is for the primary working tree only.

### At the end of every session

Whenever the session created a worktree, before declaring the run done:

1. **List worktrees:** `git worktree list`.
2. **Identify the ones this session created.** Branch name + path
   should match.
3. **For each whose PR is merged or abandoned:**
   - `git worktree remove <path>` — drops the worktree.
   - `git branch -D <branch>` — ONLY if the branch is fully merged
     or deliberately abandoned. Otherwise keep it.
4. **If a stale non-worktree directory exists inside the repo root**
   (an old clone, a scratchpad copy, an untracked sibling repo):
   - Verify it is NOT a registered worktree (`git worktree list`
     does not show it AND `<dir>/.git` does not exist).
   - Confirm with the owner before deleting if there's any chance
     it contains uncommitted work.
   - Otherwise `rm -rf <dir>` — repo-root pollution is a real cost.

### Sentinel against recurrence

If the same untracked-stale-directory artifact appears again across
sessions, that's a `tac-skillify` trigger — convert this section into
a hooked cleanup step rather than written discipline. Until then, the
written rule + end-of-session checklist is the floor.
