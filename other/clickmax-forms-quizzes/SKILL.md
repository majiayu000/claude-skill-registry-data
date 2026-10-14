---
name: clickmax-forms-quizzes
description: Use when the user wants to safely create, edit, publish, inspect, or analyze Clickmax forms and quizzes.
---

## When this applies

Use this skill when the user wants form/quiz operations where schema safety matters: editing one step, rebuilding a quiz, branching, scoring, qualification, publish state, submissions, or analytics.

Not this skill:

- lead cohort search from submissions -> use the relevant CRM lead/list/segment skill after identifying the submitted form
- page/funnel placement for a form -> resolve page/funnel work separately

- Read [quiz build](references/quiz-build.md) when creating a quiz from scratch or wiring branching/scoring/checkout — it has the exact step/block/condition shapes so you never guess the schema.

## Key assumptions

- Form/quiz content is persisted as one schema document; full replacement overwrites the current schema.
- Step-level tools exist to avoid re-emitting the whole schema for small edits.
- `expectedUpdatedAt` protects against silently overwriting concurrent edits; use it when replacing schema or editing a stale form.
- `theme` and `settings` are part of the working schema; preserve them unless the user asks to change them.
- Quiz branching, score accumulation, and qualification outcomes must remain coherent after every edit.
- Publish state is controlled by `active`; deleting is not the same as pausing collection.

## Thought process

1. Inspect the current form/quiz first.
2. Choose granular step upsert/delete for one-question or one-step changes.
3. Choose full schema replacement only for broad rebuilds where the whole schema is intentionally regenerated.
4. Before publishing, verify branching targets, scoring rules, required fields, and qualification outcomes are still reachable.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__forms_list` to find candidate forms/quizzes by kind/status/search.
- Use `mcp__plugin_clickmax_clickmax__forms_get` before edits; keep the returned step ids, schema shape, theme/settings, and update timestamp in mind.
- Use `mcp__plugin_clickmax_clickmax__forms_step_upsert` for a single new/changed step; this is the default safe path for incremental quiz editing.
- Use `mcp__plugin_clickmax_clickmax__forms_step_delete` only when removing that step is explicit, then check whether any branching target pointed to it.
- Use `mcp__plugin_clickmax_clickmax__forms_replace_schema` only when the desired result is a complete replacement; send the full schema and protect stale writes with the known update timestamp when available.
- Use `mcp__plugin_clickmax_clickmax__forms_update` for metadata/status changes, including publishing or pausing through active state.
- Use `mcp__plugin_clickmax_clickmax__forms_submissions_list` for response rows and `mcp__plugin_clickmax_clickmax__forms_analytics` for performance summaries.

## Choose the kind first: form vs quiz

`forms_create` takes `kind`: `form` (default) or `quiz`. Decide by the user's NOUN first, then by the features they ask for:

- "formulário", "form", "cadastro", "aplicação/inscrição" that just COLLECTS answers → `kind: 'form'` (linear field capture; no scoring, no branching, no result screens).
- "quiz", or any request for per-answer branching, **scoring / lead score**, result tiers, or qualification-by-points → `kind: 'quiz'`.

Scoring (`$score`), per-answer branching and result/qualification tiers are QUIZ-ONLY — a plain `form` cannot score. So when the user asks for a "formulário" that ALSO produces a score/qualification (e.g. "formulário de aplicação que gera um score do lead"), do NOT silently build a quiz and call it a form. Either build it as a quiz AND say plainly you used the quiz mode _because the score requires it_, or ask whether they want a simple form (no score) or a scored quiz. Never present a quiz as if it had fulfilled a plain-form request, and never build a full quiz when the user only asked for a form.

## Build a form from scratch

Same terminating, incremental flow as the quiz, minus the scoring/branching blocks:

1. `mcp__plugin_clickmax_clickmax__forms_create` with `{ name, kind: 'form' }` and NO `schema` → seeded starter (valid `theme`/`settings` + one step).
2. `mcp__plugin_clickmax_clickmax__forms_get` by that `id` → read the step ids, `theme`, `settings`, `updatedAt`.
3. Add/edit steps one at a time with `mcp__plugin_clickmax_clickmax__forms_step_upsert`, using only field blocks (`capture`, `text`, `number`, `currency`, `scale`, `measure`, `description`, …) — NO `options.score`/`goto`, `loading`, or `results`. See [quiz build](references/quiz-build.md) for the exact block shapes (a form is those same blocks without the scoring/branching ones).
4. Publish with `mcp__plugin_clickmax_clickmax__forms_update` `{ status: 'active' }`.

## Build a quiz from scratch

Terminating flow — build INCREMENTALLY on the server seed; never hand-author the whole schema in a retry loop. See [quiz build](references/quiz-build.md) for exact step/block shapes.

1. `mcp__plugin_clickmax_clickmax__forms_create` with `{ name, kind: 'quiz' }` and NO `schema` → returns a complete valid seed (valid `theme`/`settings` + one step). Do not author `theme`/`settings` by hand.
2. `mcp__plugin_clickmax_clickmax__forms_get` by that `id` → read the seed's step ids, `theme`, `settings`, and `updatedAt` (real ids needed for `goto`/`next`/`displayRule` targets).
3. Add/edit steps one at a time with `mcp__plugin_clickmax_clickmax__forms_step_upsert` (omit `stepId` to create, pass it to edit; `blocks` = the full list for that ONE step). Wire branching with `options.score`/`options.goto`, `button` `goto`, and `loading.displayRule` over `$score`.
4. For per-answer checkout: give each result step an `offer` block with a REAL `checkoutUrl`/`offerId` (see the anti-loop rule below), reached by score/goto.
5. Global `theme`/`settings`/`qualification` edits → `mcp__plugin_clickmax_clickmax__forms_replace_schema` (whole document). Publish with `mcp__plugin_clickmax_clickmax__forms_update` `{ status: 'active' }`.

If a `mcp__plugin_clickmax_clickmax__forms_step_upsert` is rejected, fix that one payload against the reference shapes — do NOT recreate the quiz.

## Report

- For edits: report the changed step(s), publish state, and whether branching/scoring still needs review.
- For full rebuilds: state that the schema was replaced, not patched.
- For submissions/analytics: summarize counts, conversion/response pattern, and only the most relevant examples.
- When summarizing one specific created/read form in a visual card, use the form name as the large headline/value. Put step count, field count, capture mode, and status in pills/secondary metrics instead of replacing the headline with counts.
- When you just created or inspected one specific form and offer a next-step CTA, point it to that concrete form route: `action="open-page"` with `path="/creator/forms/<formId>"`. Do not send the user to generic list routes such as `/forms-quizzes` or `/creator/forms` when the intent is "ver/abrir o formulário" that was just created/read.
- When you just created or inspected one specific quiz and offer a next-step CTA, point it to that concrete quiz route: `action="open-page"` with `path="/creator/quiz/<formId>"`. Do not send the user to generic list routes such as `/forms-quizzes` or `/creator/quiz` when the intent is "ver/abrir o quiz" that was just created/read.

## Warnings

- Do not reconstruct the whole quiz schema blind and retry on rejection. Build on the seed: `forms_create` (no schema) → `forms_get` → incremental `forms_step_upsert`. Guessing the step/block shape is what makes the call reject and loop — read [quiz build](references/quiz-build.md) for the exact shapes and fix the single failing payload instead.
- Do not reference a checkout/offer that does not exist. The `offer` block's `checkoutUrl`/`offerId` must be real: create the product+offer+checkout page first (`clickmax-products`/`clickmax-offers`/`clickmax-funnels` → `pages_create` → use the page URL) OR ask the user which checkout to use OR build the quiz with a results+capture step and leave the CTA pending. Always TERMINATE with a wired offer, a question, or a documented pending CTA — never loop trying to point at a nonexistent checkout.
- Branching + per-answer checkout uses `option.score`/`option.goto` + `button goto` + `loading.displayRule` over `$score`, plus an `offer` block in the result step — there is no magic "checkout node".
- Do not use full schema replacement for a small question edit unless the user explicitly wants a rebuild.
- Do not drop existing theme/settings during schema replacement.
- Do not publish a quiz if branching targets, scoring, or qualification outcomes are incomplete.
- Prefer pausing over deleting when the user only wants to stop accepting responses.
- A `scale` block's `max` must be ≤ 10 (mobile layout breaks above that, FLOWS-1034) — cap it and tell
  the user, don't author higher even if asked. See [quiz build](references/quiz-build.md) for the shape.

## Anti-patterns

- Guessing schema field names instead of inspecting the current form (or reading [quiz build](references/quiz-build.md)).
- Re-emitting the entire schema in a loop, or calling `forms_create` again after an error — it leaves a duplicate half-built quiz. Keep the same quiz id and fix the one rejected `forms_step_upsert`.
- Looping to wire an `offer` to a checkout/offer that does not exist yet, instead of creating it first, asking the user, or leaving the CTA pending and terminating.
- Expecting a dedicated "checkout" step type; checkout is an `offer` block with a real `checkoutUrl`, reached by score/goto branching.
- Recreating an entire quiz when a step-level edit is enough.
- Treating form analytics as lead membership source of truth.

---

Clickmax skill revision: `b8294822a4d6`
