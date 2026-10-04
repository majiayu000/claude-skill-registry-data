---
name: upgrade-mendix-version
description: "Move a project to a newer Mendix version headlessly, with no Studio Pro. Use when raising a project's Mendix version, when a build complains the project version does not match MxBuild, or before adopting a newer runtime. Covers the one check that decides whether a converter must run, and the two green false successes that upgrade nothing."
---

# Upgrading a Mendix version without Studio Pro

## Why this needs a skill

Both ways of getting it wrong **look like success**:

| what you do | what you see | what is true |
|---|---|---|
| `mxbuild --loose-version-check` | `BUILD SUCCEEDED` | the project is still on the old version |
| `UPDATE _MetaData SET _ProductVersion` | the project reports the new version, and mxcli agrees | every unit is read against the wrong schema |

Neither prints a warning. The first is not hypothetical — it is what happened to
the project that reported this, and it took going back to look at the version
column to notice that a successful build had upgraded nothing.

## The check that decides everything

A `.mpr` is SQLite. The version lives in one table, `_MetaData`, with columns
`_FormatVersion`, `_ProductVersion`, `_BuildVersion` and `_SchemaHash`.

Use Python rather than the `sqlite3` CLI: `python3` ships with a `sqlite3`
module, while the CLI is frequently absent (it is not in the mxcli devcontainer).

```bash
mprhash() { python3 -c "import sqlite3,sys
print(*sqlite3.connect(sys.argv[1]).execute(
  'SELECT _ProductVersion,_SchemaHash FROM _MetaData').fetchone(), sep='  ')" "$1"; }

mprhash app.mpr
```

```
11.13.0  {SHA256}5Fk35jOyzj+cWnJe9ZkGWQjMEzsge3nIzS2zxH9jp6M=
```

For the version alone, mxcli says it on connect — no SQL needed:

```
Connected to: /path/App.mpr (Mendix 11.14.0)
```

One `UPDATE` would make the project *claim* the new version. Whether that is an
upgrade or a corruption is decided by the **fourth column**:

1. Create a blank project at the target version (or use a project you already
   have there) and read its `_SchemaHash`.
2. Compare it with the project's.
   - **Same** → the model schema did not change. The version is a label.
   - **Different** → the schema changed, so units stored against the old one
     would be read against the new. A converter must run.

`_SchemaHash` is a property of the **Mendix version, not of the project** —
which is what makes this usable. Measured across two unrelated projects and two
machines: a 517-unit application and a blank app, both at 11.13.0, carry
byte-identical hashes, and the same holds at 11.14.0. So a reference value can be
recorded and reused rather than rebuilt each time.

```
11.13.0   {SHA256}5Fk35jOyzj+cWnJe9ZkGWQjMEzsge3nIzS2zxH9jp6M=
11.14.0   {SHA256}o9B9S8lorV9RD5gY9B6j1bJp4ALW87u4newnreIbRAg=
```

Two values are not a rule. Treat the table as a cache to check against, and
**re-derive the target version's hash from a blank project the first time you go
to a version that is not listed** — one command, and it is the only thing that
actually answers the question.

## Doing it

`mx convert` is the converter. It sits beside `mxbuild` in the toolset, and
mxcli does not wrap it.

```bash
# 1. Cache the target toolchain.
mxcli setup mxbuild --version 11.14.0        # ~/.mxcli/mxbuild/11.14.0/modeler/

# 2. Get the reference hash for the target version, if you do not have it.
mx create-project --app-name Ref --output-dir /short/path
mprhash /short/path/Ref.mpr

# 3. Convert a COPY first, never the project.
cp -a MyApp /short/MyApp-probe
mx convert --in-place /short/MyApp-probe

# 4. Verify the copy before touching anything real.
mprhash /short/MyApp-probe/App.mpr     # must equal the reference from step 2
mx check /short/MyApp-probe/App.mpr

# 5. Only now, the real project.
mx convert --in-place MyApp
```

Converting a copy first, confirming its hash matches the reference, and only then
touching the real project is what makes this safe rather than lucky. Step 4 is
the whole point: it is the difference between "the conversion ran" and "the
conversion produced what the target version expects".

## Verifying MPR v2 survived

`mx convert` preserves MPR v2 — which is not a given. Its siblings
`mx update-widgets` and `mx rename-design-properties` collapse a v2 project into
a single-file v1 `.mpr` and delete `mprcontents/` as a side effect, one-way. That
is the whole reason `mxcli fix widgets` exists.

**Check the storage format, not the unit count.** Measured on an 11.13 → 11.14
conversion: `.mxunit` files went **391 → 386** while v2 was perfectly intact. A
conversion may legitimately drop or merge units, so an unchanged count is a
coincidence, not the invariant. What actually distinguishes preserved from
collapsed:

```bash
[ -d MyApp/mprcontents ] && echo "v2 intact"     # a collapse deletes this
stat -c%s MyApp/App.mpr                          # v2: tens of KB. v1: tens of MB
```

On the measured run: `mprcontents/` present, `.mpr` 73,728 bytes.

## Traps

**`mx convert` takes the app DIRECTORY, not the `.mpr`.** Pointing it at the file
fails with a message that reads like the project is missing:

```
Conversion failed: The app directory '/path/App.mpr' does not exist.
```

**`--loose-version-check` suppresses the check, it does not run a converter.**
Verified: after invoking mxbuild with the flag, `_ProductVersion` and
`_SchemaHash` are untouched. A green build proves nothing about the version.

**A runtime version and its tooling move together.** The upgrade may break the
tools around it, and the failure need not mention a version at all. On
11.13 → 11.14 it surfaced as:

```
Error: bundling web client: no rollup.config.mjs in .../deployment/web
       (run a serve Deploy build first)
```

— because 11.14's MxBuild bundles the web client itself, so the separate rollup
step has nothing left to configure. Deleting `deployment/` and rebuilding does
not help; a newer mxcli is what fixes it. **When something breaks right after an
upgrade and names no version, suspect the toolchain before the model.**

**`mx create-project` needs a short output path.** It fails with
`System.IO.PathTooLongException` under a deeply nested directory, during package
extraction — the message names a path length, not the real constraint.

## What generalises, and what does not

Most version-pair specifics will be wrong next time. The web-client bundling
change is 11.13 → 11.14 and will not recur; the two hashes above are facts about
two releases, not a pattern.

What generalises is the decision procedure — **`_SchemaHash` decides label vs
convert** — plus the three traps: convert takes a directory, `--loose-version-check`
upgrades nothing, and the tooling moves with the runtime. Check the specifics
against your own versions rather than trusting them.

## After the upgrade

Re-run whatever the project relies on that is not covered by `mx check`, because
a clean check is not evidence the app still works. On the reporting project the
thing worth being anxious about was a non-standard database connection type not
in Mendix's own picker; it survived, and a full sync cycle proved it. Pick your
own equivalent — the integration nobody would notice breaking — and exercise it.

## Related

- `run-local` — booting the app after an upgrade; the toolchain mismatch above
  surfaces there first.
- `debug-bson` — if the converted model behaves oddly, and for why `mx convert`'s
  bare error *count* is not evidence about a model.
