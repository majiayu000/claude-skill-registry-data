---
name: subsystem-removal
description: "Use when deleting a whole subsystem from a codebase."
version: 1.0.0
author: Charles Ponti, Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [refactor, deletion, monorepo, migration]
    related_skills: [kernel-clean-code, docs-curation, kernel-git-commit]
---

# Removing a subsystem

For deleting an entire surface — an app, a service, a package, a database, a CLI — rather than
cleaning a diff. The work is mostly evidence: what actually imports this, what must survive, and
what proves the survivors still run once it is gone.

## When to Use

- "kill the dashboard / database / app", "remove the whole X package".
- A product pivot leaves a surface with no consumer.
- Consolidating duplicated packages (vendored copies, two config loaders, two write paths).

Not for: pruning unused exports or dead functions inside a live module — that is a code review.

## Procedure

1. **Inventory consumers before touching anything.** For each candidate, find every importer
   outside its own directory, and read the `package.json` dependencies of the survivors:

   ```bash
   grep -rln '@scope/pkg-name' --include='*.ts' --include='*.json' --include='*.mjs' . \
     | grep -v node_modules | grep -v "^./packages/pkg-name/"
   ```

   A package imported by nothing that survives is a candidate; one imported by a library you are
   keeping is not. Write the keep/kill list down first — this step decides whether the change is a
   refactor or an outage. Deleting a package only because it "looks like an app" is how a shared
   schema or config parser disappears under a working library.

2. **Derive the survivors from the real entry points, not from the tests.** If agents or scripts
   load your packages from their builds, grep _those_ files for what they load. A green test suite
   proves the remaining library code compiles; it says nothing about whether the product still runs.

### If the subsystem is the implementation your consumers load

Step 1's rule ("imported by nothing that survives is a candidate") answers the wrong question here:
when the consumers import the candidate, the deletion is a **port**, not a removal. Do this before
you delete anything, and see `references/porting-a-package-into-consumers.md` for the recipe.

1. Build a table of consumer → the exact symbols it uses, by grepping each consumer's loader call
   and the member accesses that follow it. That table is the port's acceptance criteria.
2. Rehome the shared modules into one surviving consumer; keep one module per source file so the
   behaviour stays diffable against the original.
3. Replace the dependency rather than vendoring it: schema libraries become hand-written
   combinators exposing the same `.parse`/`.safeParse` contract, SDKs become plain `fetch` against
   the same endpoints, `dotenv` is deleted in favour of one config file plus the environment.
4. Only then delete the source, and prove the consumers still run with it gone.

5. **Tag the last state that has the subsystem.**

   ```bash
   git tag -a <name>-final -m 'Last state before <subsystem> was removed'
   ```

   "It is in the history somewhere" is not a restore path; a tag is. Name the tag in the removal
   commit so the next reader finds it without archaeology.

6. **Delete, and delete the build output too.** `git rm -r` the packages, then `rm -rf` what the
   tooling left (`.svelte-kit/`, `build/`, `dist/`, stale workspace entries). Tracked-file deletion
   alone leaves directories that keep globs non-empty and hide a broken config.

7. **Sweep the configuration that named it.** A removed package appears in four places and none
   fails loudly: the workspace file (`apps/*`), the task runner's `globalEnv`/inputs, the root
   `package.json` scripts, CI steps — plus dependency catalogs, pinned versions and build
   allow-lists. Remove each, then let one real run prove the config still parses.

8. **Re-run install once before believing a dependency warning.** The first install after a removal
   often reports an ignored build script for the package you just deleted, because the lockfile has
   not been rewritten yet. Confirm with `grep -c <pkg> <lockfile>`: zero means stale output, not a
   leftover dependency.

9. **Delete the dead configuration keys on both sides.** Schema key, allowlist, validator, env mapping,
   test fixture and the user's own config file are six separate places. A key nothing reads still looks
   supported — the next person sets it and wonders why nothing happens. When the config loader validates
   unknown keys at startup, deleting the allowlist entry without deleting the config entries is an
   _outage_, not a half-finished refactor: see the pitfalls below and land both sides in one change.

10. **Verify with the consumers' own commands.** Build, then the full suite, then the preflight or
    dry run of each surviving consumer. An unbuilt package with a green suite is the classic false
    pass in a build-from-`dist` monorepo. **And build each consumer for the platform its code is
    actually compiled on:** conditional sources (`#if os(...)`, build tags, target-specific files) are
    skipped by a host-platform run without a word, so a green suite proves only the branch you were
    already on. Console output claiming success is not the evidence — find the object file of the
    file you changed.

11. **Hand the docs over.** Delete pages whose subject was removed, rewrite the survivors whose
    structure assumed it, mark reversed ADRs superseded, and grep README / AGENTS.md / skill bodies
    for the capability's name. See `docs-curation` for the sweep.

## Pitfalls

- **Type-only imports hide consumers.** A package pulled in through a `tsconfig` path alias rather
  than a `package.json` dependency does not appear in a dependency graph dump. Grep the scope name
  across sources too.
- **Scripted edits that prepend an import block corrupt the file that defines it.** A blanket
  replace across a directory rewrites the defining module too, producing a self-import and
  duplicated node imports: `Identifier 'x' has already been declared` from the syntax check, and
  `does not provide an export named 'x'` at runtime as the self-import signature. Dedupe existing
  imports, skip the defining file, and `node --check` every touched file.
- **A destructured dynamic import is not an export.** `const { setting } = await import(...)` binds
  locally only; add `export { setting }` for modules that import through it.
- **Top-level `await` cannot cross into a `--require` CJS preload.** If something must load the ESM
  package before the process starts, that boundary is a real constraint — pick a synchronous read
  there, or accept a second loader with the reason written down.
- **One green surface is not proof of a working system.** After deleting a store-backed component,
  exercise two paths that read different stores: a page served from a separate index returns 200
  while the one opening the database throws.
- **Removing the code is the easy half.** Config, docs, CI and the user's own config file lag
  behind. Enumerate all four and say which you touched.
- **A validating loader makes config removal a two-sided change, and half of it is an outage.** A
  loader that rejects unknown keys at startup (`unknown config keys (refusing to guess)`) kills every
  pass of the live service the moment the allowlist drops a key that any config file still carries —
  while the code that _used_ the key is already deleted and looks innocent. Read the service's own
  error log for the loader's message **before** starting, because an interrupted earlier refactor may
  have left exactly that half-state already running.
- **When the removed thing was a selector _value_, keep the key and tighten the validator.** Rejecting
  it with an explicit reason ("<survivor> is the only supported runtime; <removed> support was
  removed") fails at load with something a reader can act on. Deleting the key outright defers the
  same mistake to dispatch time, where it shows up as a missing binary or a setting nobody honours.
- **`git add` is atomic across its pathspecs.** One path that no longer exists aborts the whole
  command, so staging a hundred renames plus a few deletions in a single call silently stages nothing
  and the next status looks like your edits vanished. Stage deletions of mid-refactor paths one at a
  time with `git rm --cached --ignore-unmatch <path>`, then re-read `git status --porcelain` for the
  `RD` / `MD` / `D` states before reporting the index clean.
- **A compiler does not prune what it no longer emits.** Deleting a module's source leaves the previous
  build's `dist/<name>.js` and `.map` on disk and still requirable, so the "removed" subsystem can
  linger as a live import path. Delete the per-file artifacts by hand as well as the source.
- **Verify on the service's own next scheduled cycle, not by hand-running its entry point.** Long-lived
  jobs carry environment a manual invocation lacks (data-home variables, exported paths, the job's own
  cwd), so a hand-run can report a healthy system as broken. Read the job's log for one clean pass
  instead, and confirm the supervisor/job list still shows it running.
- **A duplicated implementation hides the drift it was meant to prevent.** Consolidating two copies is
  a _deletion of the copy_, so first read the doomed file for what it does that the survivor does not
  — a buffer cleared at the start of every run, a retry, a lock. Those side effects are invisible in
  the signature, and the glitch appears only after the copy is gone. Port each one into the survivor
  with a test, then delete. Check the doomed copy's tests too: some cover behaviour the survivor never
  had.
- **Expect a stale pin to have been hiding API drift, and treat the first failing build as the
  finding.** A consumer pinned two versions back compiles against an interface that has since been
  removed, so "point it at the new version" is a migration with real work in it, not a version-number
  edit. Budget for it out loud instead of reporting the bump as a one-liner, and check
  `git merge-base --is-ancestor <tag> <branch>` before assuming a removed symbol was ever deleted — an
  older tag that is not on the branch's line never had it.
  - **A symbol missing from the branch may live on a tagged line that was never merged — repair the ancestry
    instead of hunting for a deletion.** If `git log --all --diff-filter=D -- <path>` finds nothing while an older
    tag still has the file, the tag is on an unmerged branch: `git merge-base --is-ancestor <tag> <branch>`
    confirms it, and `git tag --contains <sha>` stops being answerable at all. The repair is one merge that keeps
    your tree (`git merge --no-ff -X ours <sha>`), and before running it, list what only that line holds
    (`git diff --name-status <sha> <branch>`) — a page, sample or test can exist nowhere else, and `-X ours` would
    silently leave it out. Never repoint a published tag to close the gap; the releases that predate the merge will
    keep reporting they do not contain that commit, because they genuinely do not.
- **Port the side effects before the file goes, and delete the copy's tests with it only after the
  survivor covers them.** A test count that drops because the tests moved is fine; a test count that
  drops because a regression lost its guard is the deletion quietly weakening the code.
- **A deletion must not change what the user sees.** When the survivor has lost a capability the doomed copy
  still provides — a styling hook, a pacing constant, a default — restore it in the survivor using the copy's
  own values and pin that with a test (the default reproduces today's output), then delete. Dropping it instead
  ships a visual change nobody chose, and a look change belongs to a design decision, not to a refactor. If the
  hook was removed rather than never written, the old tag still has it: restore from there and keep the
  defaults identical so nothing that never passed the hook changes.
- **Prove independence by deleting the source, not by pointing its variable at a nonexistent path.**
  A default or fallback still resolves, so `SRC=/nonexistent` passes while the dependency is intact.
  Delete or rename the tree and re-run every consumer's own check command plus a dry run.
- **Resolve credentials lazily in every consumer you keep.** A CLI that looks up its API key at
  module scope makes its own `--dry-run` demand a secret, so the verification path fails for a reason
  that has nothing to do with the change — and the failure looks like a regression in the port.
- **After a block replace, diff the module's export list.** A regex bounded by two neighbouring
  functions silently swallows the exports that sat between them; the loss surfaces later as
  `does not provide an export named 'x'`. Compare `grep -oE 'export [a-z ]*[A-Za-z_]+'` before and
  after, and `node --check` the file.
- **A relocated data file is not relocated until its loader opens it.** The source layout
  (`data/thing.json`) and the loader's candidate path (`data/thing/thing.json`) differ, so a copy
  that `diff`s clean still fails to load. Run the consumer that reads it, not just the copy.
- **A removal that changes the interface's granularity needs a name sweep, not just an import sweep.**
  Splitting one module into several leaves the old name in three places that still compile: a sibling
  consumer's `load('old')` call, the user's own config file keys, and prose in other skills that
  says "a <old-name> draft". Grep the retired name across every consumer, its docs and the config
  before calling the removal done — a green build proves only the imports you happened to fix.
- **Prompts and other behaviour-bearing constants are not safely retypeable.** Slice them out of the
  original file by export name and assert byte equality per constant against the source before the
  source is deleted — one changed space is a product change nobody will catch by reading a diff.
