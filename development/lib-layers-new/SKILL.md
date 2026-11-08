---
name: lib-layers-new
kind: pattern
rule: lib-layers
description: Pattern of rule lib-layers. Load when creating, renaming or removing a lib — the generator instead of bare nx g, the tag, the alias, the barrel, the README, and how to finish a removal. Moving code between existing libs — pattern lib-layers-move.
---
<!-- rt-kit v0.34.0 · patterns/lib-layers-new.md · a97044dda529 · правится надстройкой, не здесь -->

# Creating or removing a lib

Pattern of the rule `lib-layers`. What must be true — the law
`docs/constitution/lib-imports.md`.

## When to use

- A new domain or a new layer of an existing domain is created.
- A lib is renamed.
- A lib is removed.

## First — is a lib needed at all

A domain has screens, state and requests. Mechanics shared by several domains is not started as
a domain: the layers under it would stay empty forever.

The sign: if there is nothing to fill `feature`, `data-access` or `api` with — these are
utilities, and their place is the lib that already sees them. The frontend always has such a
lib — the family base; the backend — the `util` layer already listed with every domain.

That is how the `list` domain lived as nine libs for three files of code: seven libs empty, and
each with its own `project.json`, `vitest.config.mts`, barrel, tag and alias.

## Created by the generator, not by bare `nx g`

```bash
node tools/generate-domain-lib.mjs
```

The generator lays out `project.json`, `tsconfig.json`, `vitest.config.mts` and the barrel. Bare
`nx g` gives a vitest config without `passWithNoTests`, and a lib that has no tests yet fails
`nx run-many -t test` with the line "No test files found". The layout check looks at the
presence of the file, not at its content, so it lets such a lib through.

## What is added by hand

1. The tag in `eslint/boundaries/domains/<family>-<domain>.config.mjs` — one per lib, equal to
   the name and the path.
2. The alias in `tsconfig.base.json`.
3. The lib's README: what lies in it and who calls it.

Rights to foreign libs are written out as lines with a comment saying why. An import that "just
worked" means the tag is not narrowed yet.

## Removing and moving a lib

```bash
git rm -r libs/<family>/<domain>/<layer>
rm -rf libs/<family>/<domain>/<layer>
```

`git rm -r` leaves `node_modules/.vite` inside the removed directory, and the layout check keeps
seeing it as a domain without layers. Finish with `rm -rf`.

Then the tag, the alias and the rights lines of everyone who saw the lib are removed.

**A move is the same action plus a graph reset.** A directory moved by `mv` is not recounted by
the builder's graph: the project stays in the cache under the old path, and under the new one it
does not exist at all.

```bash
mv <old lib path> <new lib path>
npx nx reset
```

Without the reset the run over all projects stays green and goes over one project fewer: it
takes the set from the graph cache, and the dropped project is no longer there. Such a run can
be told from a full one only by the number of projects in its output — it does not name the
missing one, and the miss lives until the first edit in the dropped lib.

## Check

```bash
npm run check:layers
```

The check looks at the layers, the single tag = name = path, the alias, the presence of
`project.json`, `vitest.config.mts` and `src/index.ts`, the empty dependency list of
`common/util`, the family base boundaries and re-exports. Seconds — run after any creation,
rename or removal.

## Common misses

- A lib created for mechanics: the layers are empty and there is nothing to fill them with.
- Bare `nx g` — a vitest config without `passWithNoTests`, and the shared test run goes red.
- Removal without `rm -rf` — the check sees the ghost of a domain without layers.
- **A lib nobody imports is checked by nothing.** `nx lint` and `nx test` check the lib itself,
  not its contract with the consumer. The first importer is the first check: the models layer is
  accepted after `nx build` and a live run of the scenario, not by a green `lint test`.
- **A lib's own `sourceTag` is written as a string literal.** The layout check finds the
  description of a lib by the text `sourceTag: '<tag>'`, not by evaluating the module. A tag taken
  from a constant passes the lint and is reported as "described in no file". Constants are for the
  tags in `onlyDependOnLibsWithTags` only.
