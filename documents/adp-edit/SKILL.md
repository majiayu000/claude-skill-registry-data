---
name: adp-edit
description: "Edit, publish or answer comments on an ADP artifact (adp/2: it has a manifest and a db). Load it before ANY edit, publish or comment reply on such an artifact, when a comment was sent to Claude, or when the user asks what changed. Gives the loop: export to a local copy, edit, then propose (the page's inbox applies it) or publish and record, each write pinned to the version read."
metadata:
  version: "2.3.0"
---

# Edit an ADP artifact (read, hold, publish, record)

**Sites host:** read the base ADP skill's `refs/sites.md` first. Keep this protocol;
use its native Sites calls and separate source/record revisions instead of the
Claude Artifact/ArtifactData calls below.

Changes are records: the page's record lives in its db, and every write to it is pinned to the version read (`if_version`); a refused write means someone wrote first. Full text: `~/.adp/catalog/kit/guides/artifact-dataplane.md` (setup puts it there), read only if this road leaves a question open.

`ADP` means `python3 -I <adp skill folder>/scripts/adp.py`. DIR is the artifact laid out at its published paths and must hold EVERY published file. Batches are written to files (`--out`, default `DIR.adp/`) and printed as `writes` lists whose entries carry `file_path`. P.json maps `"collection/doc"` to the version you read, e.g. `{"manifest/current": 4, "parts/home": 2}`.

## Docs (ArtifactData)

`manifest/current`, `parts/<id>`, `content/<id>`, `changes/<NNNNNN>` (append-only), `agents/<name>`, `config/current`, `incoming/<pid>`, `requests/`, `presence/`. Every doc read returns `version`; every write to an existing doc needs `if_version`.

## Protocol

1. **Export (read).** `ADP export DIR --url URL` without its inputs prints the Artifact and ArtifactData reads and exits 2. Run them, save each result as the tool returned it (the `Artifact list` text as it is, ArtifactData as JSON), run it again with `--files-listing F.json --docs D.json [--version V]`. It builds `DIR.adp/` (`incoming/`, `state.json`, base/live/work, `report.json`) and merges live into work when nothing is held. A DIR that is missing or empty (a session editing a page it did not build) is filled with the live files by the first export, so nothing reads as held: do not read the page's files into DIR yourself (the Artifact `read` returns `index.html` inside the publish wrapper, and export stores it bare); read into `DIR.adp/incoming/files` as printed, or into any other folder. An empty ArtifactData collection is `[]` (`docs.json` may be `{}` for a page with no docs). A page with no `manifest/current` doc was never seeded (a page built by an older session, or never opened by an editor): after this export merged, DIR equals live, so run `ADP seed DIR --by <you> --batches`, write the printed batches (it is the record the editor open would have written; nothing else in the db changes), then export again and go on with step 2. A seed batch refused with `version_mismatch` means another session seeded in the meantime: read the docs again, export again, and go on without seeding. `ADP classify BASE.json LIVE.json INCOMING.json` sorts parts and files into new, ours, theirs, applied, held, retired.
2. **Hold.** `ADP hold DIR ID ... --by <you> [--hours H] (at most 2) [--pins P.json]` prints one pinned batch and the `hold_until` it set for the parts you will touch. A refused batch: export again. Someone else's live hold means hands off. `P.json` is `{"parts/ID": version, "manifest/current": version}` as read; a part you held is one version higher once the hold's batch has committed, so pin that one in `record`; its `needs_pin` lists what is missing or stale.
3. **Edit** in DIR. Keep every marker and `data-part`; add both for a new part; never reuse a retired id.
4. **Check.** `ADP check DIR`, `ADP manifest DIR`, then `ADP diff OLD.json NEW.json` or `ADP diff-pages OLD NEW` for the changed lines.
5. **Publish** to the same URL with `ADP files DIR [--since MANIFEST.json]` (only changed files; null removes one; MANIFEST.json is `ADP manifest DIR` saved right after the export, before your edit: `manifest/current` lists parts and too few files) and a `label` of at most 60 characters. On a conflict, merge onto the newer version; never force. Over 250 files use the printed batches.
6. **Record.** `ADP record OLD.json DIR --seq N --by <you> --summary "<what>" [--version V] [--threads T,..] [--pins P.json]` prints the batch (OLD.json is `manifest/current` as read; at most 50 writes, `manifest/current` last). Then `ADP ack DIR --result FILE`, where FILE is the JSON the ArtifactData batch returned (it stores the new doc versions); a plain-text publish result is not accepted, so do not ack it.
7. **By proposal** (a DIR with `.adp/state.json` from export): `ADP propose DIR --by <you> --summary S [--retire ID --reason R]` writes `incoming/<pid>` and its batch; exit 2 lists what is held, unretired or missing an export. Resolve it, do not bypass it. `ADP ack DIR --proposal PID` moves base once applied. Copy (`content/<id>`) is proposed only when its fragment changed after the export (`src_copy` in the state keeps the first copy the work tree had, and `ack` adopts the copy as proposed), so a stale fallback `content.js` never reverts a live copy doc; an edit made after a propose or before a re-export stays unsent until the next propose.

`ADP config` shows the switches (a DIR is accepted and not read). If `edit.locked` is true, stop and tell the user who locked it; `ADP config set KEY VALUE` changes one.

## Wording fixes need no publish

Copy lives in `content/<part id>`. Change it with an ArtifactData update with `if_version`, then record a change.

## Comments and requests

1. When a thread is sent to you, note the part its anchor sits in (anchors are part ids). Do not promise work in the thread.
2. The holder of that part makes the change and publishes.
3. Reply after the publish naming the version and the part ids.
4. A page with the Work with Claude / Codex pane (the name is the host's agent label) keeps `requests/`: `ADP requests DUMP.json` lists the open ones, with `resolved` and, for a claimed one, `lease`. A host with a queue instead of a watching session (Sites) may need a guarded claim: `ADP work DOCS.json --host claude|sites --artifact ID --path requests/RID --action claim|progress|checkpoint|block|complete --by <you>` prints one pinned write (a lease with a token; `complete` needs `--token` and `--receipt` with passing checks); run it, read the doc back, and never blindly retry an unknown outcome. A reply from the page clears the claim. Answer one with a single ArtifactData `update` of `requests/RID`, `{status: "done", response}` (Markdown). A new request is version 1 and each write returns the next version, so the pin needs no read. On long work, first write `{state: "working", progress: [{text}]}`; after a page change, add `changed` (part ids) and `version`. Write no timestamps. A request a reply reopened is answered in the next `requests/RID/turns/NNNN`, `{by: "claude", text}`, with `{status: "done"}` on the request, pinned with its version as read; `response` stays as it was.

## Other

- Moving a page's records between hosts (Claude and Sites): `ADP bundle`, `ADP import-plan`, `ADP import-ack`, described in `docs/adp-export-import.md`. They print the native calls; you run them; nothing syncs by itself.
- Agents cannot join a room; they learn of changes from comment watches, the newer-version notice on an Artifact result, and `agents/`. `ADP log -n 20` shows what the tool did.
