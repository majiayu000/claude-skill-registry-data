---
name: android-resource-shrink-verification
description: "Prove artwork and drawables survive R8 resource shrinking in an Android release APK — why name-matching and byte-matching both give false \"stripped\" verdicts, and the aapt2 resource-table walk that actually settles it. Use after enabling shrinkResources, when release art looks missing, or before claiming a release build keeps its assets."
---

# Verifying artwork survives resource shrinking

`isShrinkResources = true` can keep a resource *entry* while replacing its
contents with a tiny stub. Two obvious checks both produce confident false
verdicts, so go straight to the resource table.

## Why the obvious checks lie

| method | typical output | why it is wrong |
|---|---|---|
| grep APK entry names for `art_empty_stats` | "0 of 18 present" | release renames files to `res/tn.png` |
| match source file sizes against APK entries | "kept 4, not found 19" | AGP re-encodes PNG to WebP, so sizes change |

A missing *name* is not evidence of removal when the toolchain renames by
design — the same rule as R8 class renaming.

## The check that settles it

Read the actual table, then follow each entry to its renamed file and look at
the byte size. A stub is a few hundred bytes; real art is not.

```python
import os, glob, subprocess, re, zipfile
sdk = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk")
aapt2 = sorted(glob.glob(os.path.join(sdk, "build-tools", "*", "aapt2.exe")))[-1]
apk = "app/build/outputs/apk/release/app-release-unsigned.apk"
out = subprocess.run([aapt2, "dump", "resources", apk],
                     capture_output=True, text=True, errors="replace").stdout
z = zipfile.ZipFile(apk)
sizes = {n: z.getinfo(n).file_size for n in z.namelist()}
lines = out.splitlines()
wanted = ("art_empty_quests", "ic_rank_monarch")      # names that MUST survive
for i, line in enumerate(lines):
    m = re.search(r"(?:drawable|mipmap)[^/]*/(\w+)$", line.strip())
    if not m or m.group(1) not in wanted:
        continue
    for j in range(i + 1, min(i + 4, len(lines))):    # the file path follows the entry
        f = re.search(r"(res/[\w\.]+)", lines[j])
        if f:
            print(f"{m.group(1):24} {f.group(1):16} {sizes.get(f.group(1), 0)} B")
            break
```

Expected shape: raster art in the tens or hundreds of KB, vector drawables
around 1 KB. Anything at a few hundred bytes for a photo-sized asset is a stub.

Note `aapt2 dump resources` prints the entry and its file on **separate lines**,
which is why the loop looks ahead a few lines rather than parsing one.

## The risk that makes stripping real

The shrinker removes what it cannot see referenced. Static `R.drawable.x` is
visible; a name lookup is not:

```bash
rtk grep -rn "getIdentifier|resources.getDrawable" app/src/main --include=*.kt
```

No hits means no dynamic lookups, so nothing can be silently stripped. Hits
mean either `tools:keep` in a `raw/keep.xml`, or convert the call site to a
static reference — the latter is the real fix.

## Pair it with the dex probe

Resources and code shrink separately. Check both before claiming a release is
verified:

```python
z = zipfile.ZipFile(apk)
dex = b"".join(z.read(n) for n in z.namelist() if n.endswith(".dex"))
for p in [b"$$serializer", b"YourDto", b"YourDatabase_Impl"]:
    print(p.decode(), "KEPT" if p in dex else "MISSING", dex.count(p))
```

## What this still does not prove

The app runs. Install a debug-signed copy of the **release** APK and open the
screens that show the art — an empty-state illustration is only proven by being
rendered. Say which of the two you did.
