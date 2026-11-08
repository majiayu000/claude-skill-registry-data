---
name: dependencies-upgrade
kind: pattern
rule: dependencies
description: Pattern of rule dependencies. Load when raising package versions — choosing the upper bound by peer ranges, the order of checks, the reformatting boundary after a formatter upgrade, handling new linter rules. Not for the branch and commit — pattern git-workflow-commit; for the PR — git-workflow-pr.
---
<!-- rt-kit v0.34.0 · patterns/dependencies-upgrade.md · 896cfd43beb4 · правится надстройкой, не здесь -->

# Raising versions

Pattern of the rule `dependencies`. What must be true — the law
`docs/constitution/delivery.md`.

## When to use

- The version of any package is being raised.
- A vulnerability warning came for a transitive dependency.
- After an install, linter findings poured in or the tree got reformatted.

## The upper bound is set by peer ranges

```bash
npm view @angular/compiler-cli@22.1.0 peerDependencies
npm view typescript versions --json | tail -5
```

A package is raised to the last version that still falls within the peer range of everyone that
depends on it, not to the last one in the registry. It has to be checked package by package:
`autoInstallPeers: true` silently delivers what is missing, and a conflict of peer ranges does not
stop the install.

## Order

1. `package.json` — exact numbers, not a single `^` or `~`.
2. `pnpm install`; the snapshot goes in the same commit. Then `pnpm install --frozen-lockfile`, in
   every repository the edit goes to. Tests, the build and the linter run on modules already
   installed and do not read the snapshot: a range in the declaration against an exact number in
   the snapshot is found only by the strict install, and in a release pipeline that is after the
   merge.
3. The styling properties the tree reads from the package are checked against the new version by
   a command, not by a look: a removed property makes the declaration invalid, not wrong, and
   every check stays green. Every name from `var(--<prefix>-…)` in the tree is searched for in
   the installed sources of the package. One not found is replaced by the package's own rule,
   written in its scale, not by one's own value with the old number. One's own looks like the
   scale and is not picked up by the next version.

    ```bash
    grep -rhoE 'var\(--<prefix>-[a-z0-9-]+' <source roots> | sort -u |
        while read -r name; do
            grep -rq -- "${name#var(}" node_modules/<package>/ || echo "removed: ${name#var(}"
        done
    ```

4. `npx nx run-many -t build -p site admin api` — the build **before** the linters. It reports a
   type incompatibility in one line, while the linter on the same tree gives a hundred findings,
   and the real cause is lost among them.
5. `npm run lint` and `npm run stylelint`.
6. Tests — rule `testing`. After a Playwright version change, first
   `npx playwright install chromium`.
7. A walk over the screens in the browser — rule `browser-verification`: if the package draws
   the layout, the tests do not cover its version change.

## Reformatting

An updated formatter changes every file of the tree. What of that to keep is decided not by the
size of the diff but by whose formatting the linter checks: `.ts` and `.html` —
`eslint.config.mjs`, `.scss` — `stylelint.config.js`. The rest is reformatted later, together
with the edit that touches those files anyway: a full run changed 883 files, of which 85 are
checked, and meaningful edits cannot be made out in such a pile.

## New linter rules

A rule that forbids a technique accepted in this tree is switched off once in the config, with the
reason written next to it. A rule that is right in substance is bypassed by a targeted
`eslint-disable-next-line` — also with a reason. Mixing is not allowed: what is switched off in
the config without a reason looks forgotten a month later, and sixty-five targeted bypasses of
one rule — like a list of what should have been switched off once.

## Common misses

- `pnpm install` does not move a package that is named in `overrides`: the line from the list
  holds the old version, and the install goes through without errors.
- Linters before the build are an extra round: you sort out findings that will be gone after the
  build.
- An update that landed in a branch with another task is reverted only together with it: a
  dependency update has a task of its own and a branch of its own.
