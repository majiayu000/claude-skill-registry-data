---
name: doc-drift-check
description: Compare a README (or the root README/CLAUDE.md) against the code it describes — commands, exports, CLI flags, env vars, config shape, the boundaries table, the workspace layout — and report claims that no longer hold. Use after a change that alters a package's public surface (exports map, CLI flags, config shape, routes/composables, documented commands), or when asked to check for doc drift, before opening a PR. Skip for pure refactors, style-only diffs, or a project with no README nearby — there's nothing to compare against.
---

# Checking docs against code

This is not [`house-docs`](../house-docs/SKILL.md) — that's voice and structure for docs being
*written*. This checks whether docs already written are still *true*. It runs on whatever's in
scope, doesn't persist a file, and finds nothing to say most of the time. That's expected, not a
failed run.

## 1. Scope it

Default to affected, same as everything else here:

```sh
pnpm exec nx show projects --affected
```

Empty output means nothing to check — say so and stop, don't widen the scope on your own. If asked
to check a specific project or path instead, use that in place of the affected list.

For each project in scope, find its docs — don't assume one README per project, some carry nested
ones (`src/nuxt/README.md`, a subcommand's own `README.md`):

```sh
find packages/<name> apps/<name> infrastructure/<name> -iname "readme*"
```

## 2. What to check, and against what

Every claim in a README traces to one ground truth. Read the doc, then read the source it's making
a claim about — never the other way around, a claim that sounds plausible is exactly what drift
looks like.

| The README claims | Check it against |
| --- | --- |
| A command (`pnpm x`, `nx run …`) | `scripts` in that project's `package.json` |
| An import path / exported symbol | The `exports` map in `package.json` — packages export raw source, so the path in a README example must resolve to a real file today |
| An env var | `.env.example` — name must exist there, and nowhere does the README show a real value |
| A CLI flag or option | The arg-parsing source, not another doc |
| A config key / shape | The type or schema that defines it |
| The Nx tag table and the workspace-layout block | Nothing — `pnpm docs:map --check` renders both from source and fails on a mismatch; check the prose around them instead |

Anything outside this table — decision reports under `docs/decisions/`, dated audits under
`docs/audits/` — is a point-in-time snapshot, not a living doc. Drift doesn't apply to them; leave
them alone.

## 3. Report, don't invent

A README claim with nothing behind it anymore is drift. Code with no README claim at all is a
*gap*, not drift — different problem, don't fix it here by adding new documentation; that's a call
for whoever owns the doc's voice ([`house-docs`](../house-docs/SKILL.md) territory if it happens).

Report each finding as `file:line` — what it says, what's actually true. If asked to fix, apply
only the mechanical ones (a renamed flag, a moved import path, a stale command); leave anything
that needs a judgment call about what the doc *should* say to the human.
