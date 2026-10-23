---
name: svelte-conventions
description: "Use when writing or reviewing Svelte 5 or SvelteKit: runes and when not to use effects, props and snippets, keyed each blocks, raw HTML, shared state and server-side leaks, load functions and form actions, errors and hooks, environment variables, CSRF and auth, prerendering, and tests."
paths: "**/*.svelte, **/*.svelte.ts, **/*.svelte.js, **/+page*.ts, **/+page*.js, **/+layout*.ts, **/+layout*.js, **/+server.ts, **/+server.js, **/hooks.server.*, **/hooks.client.*, **/svelte.config.js"
---

# svelte-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Svelte 5 components and SvelteKit
applications. **Status: a base to confront with real work.** No in-house Svelte project stands behind it yet
(same status as `go-conventions`): every rule was read in the framework's own documentation and is pinned to
**Svelte 5.57 and SvelteKit 3.0** (read 2026-10-02, `references/origin.md`). SvelteKit 3 moved configuration
into the Vite plugin, renamed the `$lib` alias and the environment modules, and replaced the CSRF origin option;
a rule marked `Kit 3` does not describe a 2.x project, and a 2.x idiom is not a defect there. Read the versions
in `package.json` before judging anything.

## When
As soon as a `.svelte` file, a `.svelte.ts` module, a route file (`+page`, `+layout`, `+server`), a hooks file
or a Svelte test is written or modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task touches.** One file per section under `references/`.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Runes: state, derived, effects, props | any reactive value is declared, derived or synchronised, or a prop is read | [`01-runes-reactivity.md`](./references/01-runes-reactivity.md) |
| 2 | Components, templates, shared state and styling | markup, snippets, each blocks, raw HTML, context, a shared module or CSS is written | [`02-components-templates-state.md`](./references/02-components-templates-state.md) |
| 3 | SvelteKit: data, forms, errors, security, rendering | a route, a `load`, an action, a hook, an environment variable or a rendering option is touched | [`03-sveltekit.md`](./references/03-sveltekit.md) |
| 4 | Tests | a Svelte unit, component or end-to-end test is written | [`04-testing.md`](./references/04-testing.md) |

## Output / checkpoint
Code compliant with the sections the change touched, and the project's own check, lint and test scripts
(typically `svelte-check`, the linter, the unit runner) with no new finding. No dedicated checkpoint: compliance
is checked by `gate` (7) and `review` (8).

## Guardrails
No comments in the code produced. Never an install: name the dependency, the person runs `pnpm add -D <package>`
(`CONVENTIONS.md`). Never `{@html}` on a value you do not control. Never keep per-user data in a module-level
variable on the server. Do not rewrite working legacy-mode code (`export let`, `$:`, stores) unless the task is
that migration: new code uses runes, old code keeps its idiom until someone owns the move. When the project
pins an older major than this block, say which rule does not apply.

## Origin
Rewritten from the framework's documentation, including its own best-practices page, read 2026-10-02 and re-verified
on 2026-10-20 (one version fact corrected, see the origin file). Provenance,
licence and refresh protocol are in [`references/origin.md`](./references/origin.md). Read it when checking
freshness, not when applying a rule.
