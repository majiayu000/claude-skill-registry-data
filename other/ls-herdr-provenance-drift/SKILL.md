---
name: ls-herdr-provenance-drift
description: "Check Herdr source, skill, schema, and release drift; maintain the master provenance manifest and reviewed compatibility without automatically upgrading hosts. Start with ls-herdr-task-routing."
metadata:
  version: "1.1"
---

# Herdr provenance maintenance

Read the master first if needed:
[ls-herdr-task-routing](localsetup://package/ls-herdr-task-routing/SKILL.md)

Use `localsetup herdr provenance --help`. The master owns the single
[canonical manifest](localsetup://package/ls-herdr-task-routing/references/upstream/provenance.json).

## Check before updating

Check preserved source hashes offline first. Compare upstream stable release
metadata and the manifest's bounded source-watch paths when network evidence
is needed. `source_watch.commit` pins the reviewed watched-source baseline
independently of `source.commit`, which remains the tagged release pin; older
manifests without `source_watch.commit` use the release commit as their legacy
baseline. Unchanged version numbers do not prove unchanged skill or API source.
The scheduled daily watcher is read-only for repository contents and host state.
It compares only the canonical manifest's official release and watched-file
evidence. A confirmed newer stable release needs an immutable commit SHA;
changed watched bytes are reported independently, even if another path is
unknown. The workflow opens or updates a deduplicated `provenance-refresh` issue
handoff for findings and emits a concise run summary. Unknown evidence means
unknown freshness, not "current." A handoff gives no authority to upgrade a
host. QC Patrol remains a separate workflow.

Keep the reviewed source baseline and tagged release separate from imported
skill/schema hashes, installed client version, bundled client schema, and live
server version/protocol/endpoint. Never turn a client schema into a claim about
every remote server. Compare operations actually used; a newer compatible
release need not block them.

## Accept one coherent update

1. Resolve the official release to its full immutable commit and inspect release
   notes, upstream skill changes, license, and consumed API changes.
2. Update the preserved upstream evidence and source manifest together. Preserve
   original notices; LocalSetup's adaptation does not relicense upstream work.
3. Map changed guidance to the relevant specialist and shared core. Extend the
   existing owner rather than duplicating commands or transport logic.
4. Validate affected contracts and realistic tasks, update compatibility evidence
   and owning generated catalogs, and review the material diff.
5. Create the normal scoped local checkpoint. Publishing and actual host upgrades
   remain separate operations with their existing authority.

Do not replace source pins merely because a network check found a newer tag.
Do not rewrite historical release evidence or claim an untested version is
supported. Apply dependency verification once for a newly selected artifact
and reuse applicable evidence; do not turn it into repetitive user prompts.

Live host upgrades route to [remote](localsetup://package/ls-herdr-remote-connect/SKILL.md).

## Reviewed layout appearance change

The watched-source baseline at
[`5608de0`](https://github.com/herdrdev/herdr/commit/5608de0608918aba2f9d501e7793b984a0ca9cfa)
changes two layout pane-creation call sites to use the shared appearance helper
during a pending host-theme transition. The watched skill, generated API schema,
schema definitions and operation definitions are byte-identical to the prior
baseline. This bounded review requires no LocalSetup API change. The tagged
release, imported evidence and binary pins remain unchanged; source review does
not qualify a running client or server.
