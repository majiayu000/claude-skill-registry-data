---
name: tmp
description: "Dump a one-off convo artifact under .tmp/grunt/."
---
# tmp

One turn. Author from this session (email/script/note). Write once. Recap path. Stop.

## Invocation

`/tmp [what]`

Empty `$ARGUMENTS` + no already-visible dumpable blob → `need task`. Empty + visible blob (code fence / draft) → dump that.

## When

Dump a one-off convo artifact. Not `/handoff` (no pickup no Goal/State/Next). Not `.tmp/grunt/plans/`. Not `.tmp/grunt/implementations/`. Not product source. Not OS `/tmp`.

## Path

`.tmp/grunt/{serial}-{slug}-{YYYYMMDDTHHMMSSZ}.{ext}`

- serial: unpadded int ≥ 1, next after existing tmp dumps (own counter; not plan/handoff/implementation serials)
- slug: lower, non `[a-z0-9]` → `-`, collapse, trim 50
- stamp: UTC `YYYYMMDDTHHMMSSZ`
- ext: `TMP_EXT` or explicit `.{ext}` in args; else `md`

## Write

```
TMP_NAME: <3-6 word name>
TMP_EXT: md
<artifact only>
```

`TMP_EXT` optional. Write any root filename under `.tmp/grunt/` (not `plans|handoffs|implementations|browser|orchestrator-logs`). Grok `orchestrate-parent.js` runs `.rulesync/scripts/persist-tmp.mjs`: serial/slug/ext from `TMP_*`, strips those lines, no YAML frontmatter, rewrites path + content. Write outside that root or missing `TMP_NAME:` is denied.

Host without that hook: name the file per **Path** yourself, or pipe the body to `node .rulesync/scripts/persist-tmp.mjs --workspace {repo}` and use its `path`.

Never rewrite an existing dump; new serial. Artifact file content after hook = artifact only (no TMP_* lines no YAML frontmatter).

## Report

```
[tmp]: serial={int} path=.tmp/grunt/{serial}-{slug}-{stamp}.{ext}
```

Do not dump the body.

## Rules

- One write. `/tmp` is not a mode.
- Secrets/tokens: refuse dump. Text artifacts only; no binary.
- Protocol: `.rulesync/reference/cascade.md`. Do not paste it here.
