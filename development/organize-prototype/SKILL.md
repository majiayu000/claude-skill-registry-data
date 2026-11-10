---
name: organize-prototype
description: Rename, move, duplicate, archive, restore or delete a prototype, preserving its permanent links and the original work.
---

# Organize a prototype

The [prototypes README](../../README.md) is the contract; read "Organizing prototypes", "meta.json" and "References follow renames and moves". Run `yarn studio context src/prototypes/<key>/<folder> --json` first: it reports the owner, the system, a pending rebuild and whether you may change it (`canEdit`). Only a prototype's owner or an Admin changes it; apply the platform's [contributor scope](../../../../platform/context/contributor-scope.md) and [resource identity](../../../../platform/context/resource-identity.md) rules (moves keep IDs, copies get fresh ones).

When the studio is running, the person can do each of these from the prototype's **…** menu; prefer pointing them there for a single prototype. The menu goes through the dev server's file service, which checks permissions and repairs references.

## Rename or move

- A prototype's address is its permanent ID (`meta.json` `studioId`), so renames and moves never break links. Never change `studioId`.
- Renaming in the studio changes `meta.json` `title` and renames the folder to match (`slugify`d title). By hand: change `title`, then rename the folder; refuse if a prototype of that folder name already exists.
- Moving files inside a prototype: the running dev server repairs relative imports, navigation paths, Markdown links and canvas links after a move it can identify (`References follow renames and moves`). Check the result before replacing anything yourself, and don't apply the same rewrite twice. With the dev server stopped, update references yourself. `meta.json` `order` lists paths inside the prototype; keep it in step.
- Prototypes stay in their contributor's folder (`src/prototypes/<key>/`).

## Duplicate

- Prefer the studio's **Duplicate**: it copies the folder (skipping `.git`, `node_modules` and modules' hidden folders such as `.comments`, refusing symbolic links), gives the copy, each artifact and each named state fresh permanent IDs, points the copy's own permanent links at the copy, resets `created`, and makes an archived source's copy active. The original stays untouched. An Admin's copy of someone else's prototype goes to the Admin's own folder.
- A different system makes a **rebuild copy**: the copy keeps its current `systemId` and gets `meta.json` `rebuild: { targetSystemId, sourcePrototypeId }`. Rebuild it with [build-prototype](../build-prototype/SKILL.md), in the copy only: read the target system's `AGENTS.md`, move the system-dependent views and `systemId` together, and remove `rebuild` only when the migration is complete and checked. The copy's sidebar offers ready-made instructions.
- By hand, leave modules' hidden folders (such as `.comments`) behind and never reuse an ID: copy, then give every file its own new ID with `yarn studio identify` (remove the copied identity comments first).

## Archive or restore

- `meta.json` `"status": "archived"` sets the whole prototype aside; active is the default and is never written. There is no per-artifact status.
- An archived prototype stays in the local studio, read-only, and is left out of the deployed site entirely (not listed, built or bundled). Links to it there show a placeholder, and the build warns about active files that link to it: resolve those warnings, or accept the placeholder.
- Restoring removes `status` (and `archivedBySystemId`). It is refused while the prototype's system is deleted (rebuild it with an available system first) or archived (restore the system first).
- Prefer archiving when the person wants to set work aside. Delete only when asked.

## Delete

Delete only when the person asks.

1. Run `yarn studio delete-prototype src/prototypes/<key>/<folder>` and show the person its preview: links from other prototypes and canvas and document references that would break, what modules keep in it (such as comments), untracked files and uncommitted changes that would be lost. `--json` gives it as data.
2. Apply with `--yes` only after they confirm. The command deletes the folder for good (it is not moved to the trash) and a running studio updates by itself. If it reports that another program is using the folder, close that program and run it again; nothing was deleted.
3. Report the links it listed, for their owners to update.

The studio's own **Delete** moves the folder to the computer's trash (the Recycle Bin on Windows) instead.

## Verify

Open the prototype by its permanent address, check its navigation and the links you kept, and run `yarn studio identity-audit` after copying or moving files by hand. Report preserved originals and any links left for others.
