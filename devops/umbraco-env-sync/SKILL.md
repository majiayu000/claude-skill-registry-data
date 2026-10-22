---
name: umbraco-env-sync
description: >-
  Moving an Umbraco package's own entities between environments with Umbraco Deploy or
  uSync: what moves as files and what moves over the wire, export shape and dependencies,
  restores, keeping secrets out, linking users by alias, translating stored ids, and
  keeping sync code current. Use when adding Deploy or uSync support, or changing an entity
  the package syncs. Not for deploying the site itself.

---

# Moving package data between environments

A site runs in more than one place: a developer's machine, a staging site, live. Umbraco
moves its own schema and content between them. A package's own data (its settings, its
records in its own tables) only moves if the package teaches a sync tool how.

Two tools do this, and a package can support either, both, or neither:

- **Umbraco Deploy**, Umbraco HQ's licensed tool, used on Umbraco Cloud and on its own.
- **uSync**, a community tool (Jumoo). Files on disk are free; push and pull between
  servers needs the licensed uSync.Complete.

This file holds the rules that apply to both. The tool-specific API is in
[references/deploy.md](references/deploy.md) and [references/usync.md](references/usync.md).
Verify any API against the docs and the package versions for the major the project targets
(`umbraco-docs`).

## Does this project sync?

Supporting a sync tool is the package's choice. Look before assuming:

- **Deploy:** a project references `Umbraco.Deploy.Infrastructure`.
- **uSync:** a project references `uSync.BackOffice` or `uSync.Core`.

If neither is there, this skill applies only when the work is to add support. If one is
there, every new entity needs a decision on how it moves, and every change to a synced
entity carries a sync change (see "Keep sync in step" below).

## Ship it as its own package

Put the sync code in a separate project and NuGet package (`MyPackage.Deploy`,
`MyPackage.uSync`) that depends on the main package. Sites that don't use the tool don't
take its dependency.

- Reference only the tool's packages the code needs, with a version range pinned to the
  CMS major (`[18.0.0, 18.999.999)`). Both tools release a major per CMS major.
- Register after the main package (`[ComposeAfter(typeof(MyPackageComposer))]`), so the
  services the sync code calls exist.
- Keep the main package free of any reference to the tool. If the main package must raise
  something the sync code listens to (a saved or deleted notification), that's a plain
  notification the main package publishes anyway.

## Choose how each entity moves

Decide per entity, and write the choice down in the project's `CLAUDE.md` so later changes
follow it.

| The entity is | Move it | Why |
|---|---|---|
| Configuration a developer sets once and every environment shares (providers, connections, store settings, templates, a settings singleton) | **As files on disk**, committed to source control and applied on deploy | It's part of the site's setup, like a Document Type. It should travel with the code. |
| Data editors create and change, and that differs between environments (catalogue records, editor-made presets) | **Over the wire**, an editor picks it in the backoffice and sends or restores it | Editors decide when it moves. Committing it to source control would fight their edits. |
| Data users or the site create at run time (orders, submissions, logs, generated codes) | **Not at all** | It belongs to the environment it was made in. Moving it overwrites real records. |

Something an entity in the first group links to must also be in the first group, or be
something the target always has. A file can't depend on a record an editor may never
send.

## The export shape

Each entity becomes one exported item (Deploy: an artifact; uSync: an XML file).

- **Keep the entity's id the same in every environment.** Create entities with a GUID key,
  and when the sync tool creates one on the target, give it the source's key. Integer ids
  never travel.
- **Link to other entities by key, typed.** Store a reference as the tool's typed id
  (Deploy: a `GuidUdi`; uSync: the key), not a raw GUID with no type and never an integer.
- **Declare every link as a dependency.** A link the export doesn't declare is a link that
  can arrive dangling. This includes lists of ids and links buried in settings JSON.
- **Look up by alias when the key doesn't match.** An entity created by hand on both sites
  has two different keys. Find the existing one by key first, then by alias or code, and
  update it rather than creating a duplicate.
- **Make the output stable.** Sort lists, fix decimal places, serialize polymorphic values
  against their runtime type. The same entity must export to the same bytes, or every save
  shows a change and every diff is noise.
- **Read old exports.** A file written by an earlier version of the package can arrive at a
  newer one. A missing field keeps the target's value or a default. A new field is optional
  on read.

## Restoring

A sync tool restores many entities in one run, in passes: every entity's code runs in the
passes it asks for, and all of one pass finishes before the next starts.

- **Be lenient where a lost value is better than a failed run.** A link to something the
  target doesn't have: drop it and log a warning, unless the entity can't work without it,
  then fail with a message that names it. A value outside the target's limits: clamp it.
  One bad item shouldn't stop the whole restore.
- **Save each pass's work before the next pass reads it.** Keep the entity the pass created
  so the fill-in pass updates it rather than finding or creating it again.

## Keep secrets out

Exports end up in source control, in transfer packages, and on other servers. A secret in
one has leaked.

- **Leave secrets out by default.** API keys, passwords, tokens, connection strings, and
  encrypted values don't go into the export unless the site owner turns them on.
- **Let config references through.** A setting that points at configuration instead of
  holding the secret (`umbraco-security`'s "Secrets and sensitive configuration") is safe to
  move. Each environment resolves it to its own value.
- **Give site owners an ignore list.** A setting naming fields to always leave out, for
  provider settings the package doesn't know about.
- **Merge on restore, don't replace.** A field left out of the export must keep the
  target's own value, not be wiped.
- **Mark fields sensitive where they're defined.** The sync code reads the marker; it
  shouldn't keep its own list of field names to skip.
- **Don't rely on spotting encrypted values.** A value encrypted at rest can reach the sync
  code already decrypted, because the package's service decrypts on read. Filter on the
  field's sensitive marker, and test with a real transfer that the secret isn't in the
  export.

## Users, groups, and members

Deploy doesn't move users, user groups, or members, and free uSync doesn't either. Their
keys differ between environments.

- **Link to a user group by alias, a user by username or email, a member group by name.**
  Look them up on the target by that value, and convert back to the target's key.
- **Skip a link the target can't resolve, and log a warning.** Don't fail the restore.
- **Watch what a lost link means.** If dropping it widens access (a lost "deny this group"
  rule lets the group in), resolve the rule's meaning before skipping: fail, or keep the
  target's existing rule. A permission that quietly loosens on deploy is a security bug.
- The same applies to anything else the tool doesn't move: media referenced from settings
  (move it as a typed media key so the tool can bring it along), languages (by ISO code),
  and entities from another package without sync support.

## Property values that store ids

A property editor whose stored value holds an entity id (a picker for the package's own
entities, a price keyed by currency) needs a translator, so the id is swapped for a typed
key on export and back on import, and the entity is declared as a dependency. Deploy calls
it a value connector, uSync a mapper. Without one, the content arrives pointing at nothing.

## Keep sync in step

Once a project syncs an entity, the sync code is part of that entity. A change that skips
it ships an entity that quietly stops round-tripping.

| Change | Sync change that goes with it |
|---|---|
| New field on a synced entity | Add it to the export and the restore. Optional on read. Leave it out if it's a secret. |
| New link to another entity | Store it as a typed key and declare the dependency. |
| New entity type | Decide how it moves (table above), then the full set: export shape, restore passes, registration, tests. |
| Renamed or removed field | Keep reading the old name from existing exports. |
| New property editor that stores ids | A value translator. |

`feature-design` and `feature-plan` carry these into the plan as tasks; `builder` builds
them alongside the entity change; `reviewer` checks they're there.

## Test it

- Unit test each connector or serializer: export an entity, check the output, restore it
  onto an empty target, check the result. Cover a missing dependency and a secret field.
- One scenario test across entities, restoring a full set, catches links restored before
  the thing they point at.
- Run a real transfer between two local sites when sync support is added, and when the
  restore passes or the secret handling change. Both tools can do it on one machine without a
  license: [references/real-transfer.md](references/real-transfer.md). Check the export
  for a fake secret, and the target's database for the result.

## *Reviewing a diff for environment sync*

Apply when the project syncs (see "Does this project sync?").

- A new entity with no decision on how it moves (files, over the wire, or not at all), or
  one that should move with no sync code.
- A synced entity's model gained, lost, or renamed a field, and the export and restore
  didn't change with it.
- A new link stored as a raw GUID or integer, or not declared as a dependency.
- A secret field exported with no default exclusion; a restore that wipes a field the
  export left out.
- A user, user group, or member stored by key instead of alias; an unresolved one that
  fails the restore, or widens access when skipped.
- An entity users create at run time added to the sync.
- Unsorted lists or culture-dependent formatting in the export.
- An entity created on the target with a new key instead of the source's.
- A new property editor storing ids with no value translator.
