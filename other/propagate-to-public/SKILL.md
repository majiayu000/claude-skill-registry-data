---
name: propagate-to-public
description: 'Promote a tested release of the Senzing Bootcamp from this development repository into the public repository (Senzing/bootcamp): every assistant''s package, each assistant''s catalog, the pages published at hub.senzing.com/bootcamp/ and the public README. Use when the maintainer wants to publish, promote, release, sync or push the bootcamp to the public repository. Builds everything fresh from source, writes only the public clone''s working tree and stops there (no commit, no push). Maintainer tool — not part of the bootcamper experience.'
argument-hint: "[path to the public clone] (omit for ~/github.com/senzing/bootcamp)"
---

# Promote to the public repository

This is a **maintainer** tool. It carries a tested release from this development repository
into a clone of the public repository, `Senzing/bootcamp`, which is where bootcampers install
from and what `hub.senzing.com/bootcamp/` is published from.

The public repository holds only what a bootcamper installs and reads. It gets one large,
tested change per release; the many small changes that make up a release stay here.

The work is done by the build, not by hand:

```console
python3 -m tools.bootcamp_build promote --to <public clone>            # plan: prints the change, writes nothing
python3 -m tools.bootcamp_build promote --to <public clone> --apply    # writes the public clone's working tree
```

It is deterministic on purpose. Every package is built fresh from `source/` for the promotion,
so what is promoted cannot be a stale build.

With no argument, use the default checkout, `~/github.com/senzing/bootcamp`. An argument is the
path to the public repository's working tree: pass it to `promote` as `--to`.

## What is promoted

| In the public repository | Comes from | How |
| --- | --- | --- |
| `plugins/<assistant>/senzing-bootcamp/` | `source/` and `hosts/<assistant>/` | Mirrored: a file the build no longer produces is removed |
| Each assistant's catalog (`.claude-plugin/marketplace.json`, `.github/plugin/marketplace.json`, `.agents/plugins/marketplace.json`) | The host profiles | Written |
| `docs/` | `site/` | Mirrored, except the paths `site/promote.json` lists under `preserve`, which exist only in the public repository (the promo video) |
| Files under `public/`, such as `README.md` and `assets/` | `public/` | Written at the same path from the root |

Nothing else in the public repository is touched: its workflows, its license, its contribution
files and its own `.claude/` stay as they are.

**Never promoted:** `tests/`, `specs/`, `.claude/`, `tools/`, `hosts/`, `feedback/` and anything
else that exists to develop the bootcamp. None of those paths is read by the promotion at all.
`feedback/**` is the processed-feedback archive and its ledger, which hold bootcamper text, so
it is never promoted.

## How to run

1. **Release first.** `/release` bumps the version, writes the changelog entry and tags the
   commit. Promote the tagged commit, with a clean working tree, so the public change is
   exactly one version.
2. **Run every check.** `python3 -m tools.bootcamp_build check` and the test suite must pass.
   The check refuses a build in which any assistant's package names another assistant.
3. **Read the plan.** Run `promote` without `--apply`. It lists what would be added, changed
   and removed, and writes nothing.
4. ⛔ **Look at `removed` and `changed` before applying.** A file listed there that this
   repository never produced was edited in the public repository by someone else: applying
   would discard that edit. Stop and run `/retrofit-from-public` first.
5. **Apply.** Run it again with `--apply`.
6. **Hand the diff to the maintainer.** The promotion ⛔ **never commits, branches or pushes**.
   `main` in the public repository requires a signed commit and a code-owner review, so the
   maintainer reviews `git -C <public clone> diff`, then commits and opens the pull request.
   That diff is the last gate before a bootcamper sees the change.

## Guardrails

- It writes only into a git working tree whose `origin` is `Senzing/bootcamp`, and refuses
  any other directory before reading or writing anything in it.
- **Don't guess the destination.** If the public repository isn't at the default path and none
  was given, or the destination does not exist, is not a git repo, or its `origin` is not
  `Senzing/bootcamp`, ask for it rather than promoting somewhere uncertain. The promotion
  refuses each of these, and guessing a destination is how a release lands in the wrong tree.
- The Gemini package installs in Antigravity from a local clone of the public repository, so
  it needs nothing beyond `plugins/gemini/senzing-bootcamp/`.
- After the pull request merges, check that GitHub Pages built:
  `gh api repos/Senzing/bootcamp/pages/builds/latest`, then the live pages.
