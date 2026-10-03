---
name: svelte-docs-lookup
description: "How to look up Svelte 5 / SvelteKit docs via MCP. Triggers on: uncertainty about Svelte 5 APIs (runes, $bindable, $derived.by, $state, snippets, lifecycle), wanting to check Svelte runtime behavior, or correcting technical terms before answering. Also check the exact Svelte version first in frontend/package.json. Rule: list sections first, match the use cases, then request documentation in batches. Do not use the heart-of-the-system prompt if the autofixer is sufficient."
---

# Skill: Svelte docs lookup via MCP

## When to consult docs

Pattern: don't know the API. Examples:
- "Is `$derived.by` different from `$derived(() => ...)`?"
- "How do I mark a prop as bindable in Svelte 5?"
- "Can I use `await` at the top of a Svelte component?"
- "Does `<svelte:head>` still work in Svelte 5?"
- "What are the mount lifecycle changes in runes mode?"

If you already know the answer or the autofixer can fix it, **don't** consult docs — it costs tokens.

## Two-step rule (mandatory order)

### Step 1: `svelte_list-sections`

Always call this first. It returns:

```
* title: $state, use_cases: component state, reactive..., path: docs/state.md
* title: $bindable, use_cases: forms, controlled inputs..., path: docs/bind.md
...
```

Analyze the `use_cases` field. Match the user's task against these. E.g., if building forms, look for `forms`, `controlled inputs`, `event handlers`. If you guess wrong, you waste a follow-up call.

Batch the candidates — choose ALL sections that might be relevant before doing Step 2.

### Step 2: `svelte_get-documentation`

Pass an array of section names/paths, e.g.:

```
svelte_get-documentation(section: ["$state", "$derived", "$bindable"])
```

This fetches the full text in one round-trip. Combine related sections to avoid follow-up clarification.

## Version note

This repo runs Svelte 5 — check `frontend/package.json` for the exact pinned version. Sections relevant to:
- **Svelte 5**: `$state`, `$derived`, `$derived.by`, `$props`, `$bindable`, `$effect`, snippets, event handlers (`onclick=`), lifecycle (`onMount` still works in runes mode)
- **SvelteKit**: not used here (this is a SPA, not SvelteKit — see AGENTS.md decision #1). Skip any SvelteKit routing / load function docs.

## Cost-saving heuristics

| Symptom | Cheapest tool |
|---|---|
| Verifying my own Svelte code | `svelte-autofixer` (cheaper, more specific) |
| Quick type sanity check | `svelte-check` |
| Confirming a Svelte 5 API behavior | `svelte_get-documentation` (this skill) |
| "What does X do?" open question | `svelte_list-sections` then `svelte_get-documentation` |
| Visual confirmation | Playwright (separate skill) |

When in doubt between autofixer and docs: try the autofixer first. If it can't fix the issue, escalate to docs.

## Pitfalls

- `$derived(() => expr)` vs `$derived.by(() => expr)`:
  The former is shorthand that returns the arrow function itself (anti-pattern). The latter is the explicit function form. Most of the time you want `$derived(expr)` (no arrow) or `$derived.by(() => { ... return value; })`.
- `bind:value` with `$bindable()`:
  Default `$bindable('')` does NOT make the prop optional in TS, and does NOT catch parent `undefined` values. See bug #4 in AGENTS.md.
- Svelte 4 vs Svelte 5 syntax:
  `on:click={...}` (Svelte 4) is replaced by `onclick={...}`. Same for `on:input`, `on:change`, etc. The autofixer flags these.
- SvelteKit features are not available (SPA): `+page.ts`, `+layout.ts`, `load`, `form actions`, etc. — all absent. Don't pull SvelteKit sections unless the question is genuinely about SvelteKit migration.