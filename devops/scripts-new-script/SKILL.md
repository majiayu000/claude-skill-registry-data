---
name: scripts-new-script
description: Add a script to @joinery/scripts — the index.ts/main.ts/adapters/domain folder, the package.json line, the README row and the docs:map re-render. Use when adding a new repo-local CLI under infrastructure/scripts, or when splitting an existing one.
---

# Adding a script

The layout rule and the import direction are in the
[package README](../../../infrastructure/scripts/README.md#structure). Follow it; this file is what
the prose can't enforce. Read [`drift/`](../../../infrastructure/scripts/src/drift) first —
it is the smallest complete example of all four layers.

## The folder

Five things, and the last two are the ones that get forgotten:

```
src/<name>/index.ts      five lines, copied verbatim from any other script
src/<name>/main.ts       the command
src/<name>/adapters/     one file per boundary out
src/<name>/domain/       the pure part
src/<name>/README.md     what it's for, its commands, a 🗂 Structure block
```

plus a line in [`package.json`](../../../infrastructure/scripts/package.json)'s `scripts` shaped
`pnpm --silent cli src/<name>/index.ts`, never a bare `node` call, a row in
the package README's
command table, and — if a human types it rather than a hook or another script calling it — a
forwarding line in the **root** `package.json`, shaped
`pnpm --silent --dir infrastructure/scripts cli src/<name>/index.ts`. `coverage` deliberately has
no forward, because it rides on the root `test:coverage`.

**Create `adapters/` and `domain/` even when one holds a single file.** The point of the layout is
that `ls` answers "what runs, what talks to the outside, what's pure" before anyone opens anything;
a folder that skips a layer because it only needed one file breaks exactly that.

## The five things that go wrong

1. **`pnpm docs:map` is not optional.** A script is a capability, so
   [`ci.yml`](../../../.github/workflows/ci.yml) fails on `docs:map --check` until
   `docs/FEATURES.md` is re-rendered. Never hand-edit that file. If the new row shows `—` in the
   *Explained in* column, the fix is the missing `README.md`, not the cell.

2. **Never name a directory `coverage` or `types`.** Both are in
   [`baseIgnores`](../../../packages/configs/src/eslint/lib/ignores.ts), so ESLint silently
   skips them. `src/coverage/` went unlinted long enough to drift to `interface` and semicolon
   delimiters while the rest of the package used `type`; it is `coverage-report/` now for that
   reason alone, and the pure layer is `domain/` and not `types/` for the same one.

3. **No side effects at module scope, and `process.exit` never.** Read `process.env` inside `main`,
   read flags through `flag()` from
   [`shared/cli.ts`](../../../infrastructure/scripts/src/shared/cli.ts), and let `run`
   decide the exit code — throw `ExpectedError` when the message *is* the whole answer, or
   `CancelledError` from a cancelled prompt. `run` sets `process.exitCode` rather than exiting,
   because a write to a pipe is asynchronous and exiting on the next line truncates it. Two
   modules here used to resolve the repo root at import time and could not be imported outside a
   git checkout, which is why neither had a spec.

4. **cwd is this package's directory, not the repo root.** `pnpm --filter` changes into it first, so
   a relative path like `packages/content` resolves against `infrastructure/scripts/packages/content` and
   matches nothing. Build every path with `at()` from
   [`shared/adapters/git.ts`](../../../infrastructure/scripts/src/shared/adapters/git.ts).

5. **Any value you didn't author goes through `assertNotFlagLike`** before it reaches a `git` or
   `gh` argument — an issue title, a picked label, a ref out of the environment. A leading `-` is
   read as a flag rather than as the value of the one before it. `run` in
   [`shared/adapters/exec.ts`](../../../infrastructure/scripts/src/shared/adapters/exec.ts) can't do
   this for you: it also
   carries the flags themselves.

## Output goes through `out`

Never `console.log`, and never `@clack/prompts`' `log`/`intro`/`outro`/`spinner` directly —
[`shared/adapters/io.ts`](../../../infrastructure/scripts/src/shared/adapters/io.ts) picks clack or
plain lines from
`isTTY && !CI`, and sends `warn`/`error` to stderr in both. Import `confirm`, `select`,
`autocomplete` and `text` from clack directly, since a prompt needs a terminal by definition; wrap
every one in `orExit`. A prompt can't run without a terminal at all, and an agent's shell never has
one, so every command with a prompt also takes the answers as arguments and calls
`requireTerminal(hint)` before the first prompt, the hint naming those arguments. `pnpm issue:pick`
is the example: `pick <number> --type=…` asks nothing, and a bare `pick` with no terminal fails at
once. Read a `--name=value` flag with `optionValue` from
[`shared/domain/cli.ts`](../../../infrastructure/scripts/src/shared/domain/cli.ts); a bare
`--name value` parses as a flag plus a positional.

**`select` or `autocomplete` is decided by the list, not by taste.** A list that grows with the repo
— open issues, labels, projects with a dev server — is `autocomplete`, so it can be typed at instead
of scrolled. A fixed taxonomy of a handful of values — the four branch types, the four boards — stays
`select`, where a search box costs a keystroke and saves none. `autocomplete` takes the same
`options` array, so the swap is the word plus a `filter`. Put the filter's predicate in `domain/`
with a spec rather than inline: `#63` matching `63`, or a label matching its description, is real
logic, and the prompt is the one place you can't see it go wrong in review.

That split is not cosmetic: `map/` runs in CI and `drift/` runs from a pre-push hook a GUI git
client can invoke with no terminal attached.

## Reuse, and when to promote

A helper stays in the script that needs it until a **second** script needs it, then it moves to
[`shared/`](../../../infrastructure/scripts/src/shared/README.md) — which is laid out the same way,
so it lands in
`shared/adapters/` or `shared/domain/`, not at the root. The root of `shared/` is only `cli.ts` and
`errors.ts`. Don't pre-emptively share, and don't reach for a validation or utility dependency: the
package has four, all of them load-bearing.

Two script folders never import each other.

## Verify

```sh
pnpm docs:map            # then commit docs/FEATURES.md
pnpm check               # affected lint, typecheck and test, then both --checks
node src/<name>/index.ts # and once more with CI=1 and </dev/null: an agent's shell has no terminal
```

A spec is only owed by real logic — a parser, a diff, a mapping — and that logic lives in `domain/`,
which is what lets the spec call it with no mock. Don't write one that asserts a mock of `gh`
against itself.
