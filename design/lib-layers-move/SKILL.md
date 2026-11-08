---
name: lib-layers-move
kind: pattern
rule: lib-layers
description: Pattern of rule lib-layers. Load when moving code or a symbol between libs — where to start, in which order to move domains, what to do with boundaries, imports and the README of both libs, and what to check with. Creating and removing a lib itself — pattern lib-layers-new.
---
<!-- rt-kit v0.34.0 · patterns/lib-layers-move.md · 314217994602 · правится надстройкой, не здесь -->

# Moving code between libs

Pattern of the rule `lib-layers`. What must be true — the law
`docs/constitution/lib-imports.md`.

## When to use

- A symbol moves from one lib to another.
- A domain is moved into a new layout.
- Shared code is collected from copies into one place.

## Start with `docs/plans/`

```bash
grep -rn "<lib name>" docs/
```

The decision about where the code moves is often already made and written down, and one made
anew drifts from it. That is why the move of the list utilities was done twice: the first edition
put them into `libs/common/util`, which the very first item of that same plan forbids, and it had
to be rolled back whole.

## The order is set by the dependency graph, not by the list in the plan

A domain is moved after everyone it depends on. Domain lists in plans are sorted by importance,
and following them head-on forces the boundaries to be widened for a while.

```bash
grep -rn "@<scope>/<family>/<domain>" libs/ apps/ | sed 's/:.*//' | sort -u
```

The edges are written out by grepping the domain aliases and sorted topologically. Every
temporary line in the boundaries is a weakened mechanical check — the one the cutting was started
for.

## Where exactly the shared goes

A lib of its own is created when no existing lib sees the code.

| Who needs it                                    | Where                                                       |
| ----------------------------------------------- | ----------------------------------------------------------- |
| the backend or both frontends, without Angular  | `libs/common/util`                                          |
| the frontends only, pulls Angular               | `common/platform` — a service and a token, `common/ui` — a component |
| a subject that already has a lib                | into it: `site-routing`, `i18n`, `photo`, `captcha`         |
| every domain of one family                      | the family base `<family>/core`                             |
| the whole backend                               | the `util` layer already listed with every domain           |

No new lines appear in the boundaries with such a move — except the right to see the contract,
if the code reads it.

## After the move

1. **The README of both libs.** The one the file left and the one it came to: the README lists
   what lies in the lib and who calls it. No check reads these texts.
2. **Import order.** Moving an alias breaks it, and it arrives as a `prettier/prettier` error
   from the lint, not from the build:

    ```bash
    npx nx lint <project> --fix
    ```

    `test` and `build` have no `--fix` flag, so it cannot be passed to `run-many -t lint test` —
    the whole call fails.

3. **Lint over all touched projects, not over one application.** The script errs silently and
   not the way a person does: the import line is not rewritten, it disappears whole. When the
   list utilities were moved, imports vanished this way in six files out of eight, and the run
   over the project list found them — the build of one application never reached these files.

    ```bash
    npx nx run-many -t lint --projects=<list by changed files>
    ```

    This run is quick, hot on the heels of the move, and it never serves as the set before the
    push: a set assembled by changed files skips what the edit reached through dependencies.
    Before the push goes the same set the pipeline runs, by the same commands.

## Check

```bash
npm run check:layers
npm run check:dupes
```

The second is mandatory: a move is the very moment when a copy stays in the old place.

**Moved routes are checked by the screen, by the whole scenario: open the panel, close it, go
back with the browser.** The outlet address is assembled at runtime, and neither the linter, nor
the build, nor the layout check looks into it: a panel that stayed closed throws no error and
leaves the browser output clean. The three actions check three different places — opening takes
the command from the current route, closing goes from its parent, going back reads the address
from the browser history. After a move each of them breaks apart from the other two.

## Common misses

- A new address chosen without reading `docs/plans/` — drifts from the decision already made.
- The move order taken from the list in the plan — the boundaries have to be widened for a while.
- The README fixed in only one lib.
- Lint run over the application, not over the list of touched projects — vanished imports are
  not seen.
- A copy left in the old place, and `check:dupes` not run.
