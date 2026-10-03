---
name: svelte-autofixer-flow
description: "Call the `svelte_svelte-autofixer` MCP tool before sending any Svelte code to the user. Triggers on: writing a new component, editing an existing component, refactoring bind/event syntax, $state/$derived/$props/$bindable, extracting inline handlers, snippets that will be sent to the user, or questions like 'why this doesn't work' when the likely answer is Svelte code. Mandatory before replying to the user with a Svelte code block. Cheaper than sending the code to the browser."
---

# Skill: Svelte autofixer flow

The `svelte_svelte-autofixer` MCP tool verifies and fixes Svelte 5 syntax BEFORE code is sent to the user. Running it is mandatory for any code change touching a `.svelte` file.

## When to call

ALWAYS before producing Svelte code as the answer (either to write file, or inline in chat):
- Writing a new component
- Editing an existing component
- Refactoring runes (`$state`, `$derived`, `$props`, `$bindable`)
- Refactoring event handlers / bind
- Extracting inline code into helper
- Producing a Svelte snippet as the answer to a question
- After svelte-check reports errors that hint at Svelte syntax issues

This is the cheapest "verify" pass. It catches: invalid runes, mismatched event syntax, proper Svelte 5 idioms, optional/required prop defaults, lifecycle hook misuse, reactive declarations, etc.

## Tool signature

```
svelte_svelte-autofixer(
  code: "<svelte code string>" | "<absolute path to .svelte file>",
  desired_svelte_version: 5,
  filename: "MyComp.svelte",     # only basename, not full path
  async: false                    # set true only if top-level await is in markup
)
```

`code` may be a string OR an absolute path to a `.svelte` file. Prefer passing a path when a file already exists on disk — saves tokens and avoids string-escaping issues.

`desired_svelte_version`: 5 unless the user explicitly wants Svelte 4 (check `frontend/package.json` for the exact pinned version — this repo is on Svelte 5).

## Flow

```
1. Have draft Svelte code in mind (or in file)
2. Run svelte_svelte-autofixer with the code
3. Read the suggestions list
4. Apply suggestions to your code
5. Re-run autofixer if major changes resulted
6. THEN write the file (or send the snippet to user)
7. THEN run svelte-check (see verify-svelte-check skill)
```

## Don'ts

- Don't ship Svelte code without running the autofixer. The autofixer is allowed by the harness exactly to make this gate cheap.
- Don't run autofixer AFTER writing the file as a "post-check". It's a pre-write gate.
- Don't ignore suggestions just because they're "style". Most are correctness / Svelte 5 idiom fixes.
- Don't pass `filename` with full path — only basename (e.g., `FormField.svelte`).
- Don't fetch Svelte docs to fix things the autofixer can already fix. Use it as the first line.

## Cost vs. docs lookup

| Situation | Tool to use |
|---|---|
| Verify a snippet I'm writing | `svelte_svelte-autofixer` |
| Verify a file on disk | `svelte_svelte-autofixer` with path |
| I don't know the API at all (e.g., what runes exist) | `svelte_list-sections` + `svelte_get-documentation` (see svelte-docs-lookup skill) |
| Visual check (rendering correctly?) | Playwright (see playwright-visual-verify skill) |
| Type errors / unused imports | `svelte-check` (see verify-svelte-check skill) |

Prefer the autofixer first; only escalate to docs when unsure about the API itself.

## Common findings the autofixer catches

- Old `export let foo` (Svelte 4) should be in `$props()` destructure
- `on:click={...}` → `onclick={...}` (Svelte 5 event syntax)
- `${}` interpolation in template where `{...}` is correct
- Missing `$state()` for mutable variables
- `$derived(() => expr)` (function form) used as if it returns `expr` — should be `$derived(expr)` or `$derived.by(() => expr)`
- `bind:` on a non-`$bindable` prop
- Top-level `await` without `async` mode
- `class:` shorthand confusion

The autofixer emits suggestions with line numbers and reasoning. Treat each one as a fix-or-reject decision; do not silently skip suggestions; either apply or note why not.