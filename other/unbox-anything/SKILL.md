---
name: unbox-anything
version: "1.0.0"
user-invocable: true
description: "Universal file/container unpacker for AI agents. Use whenever the user has a specific named file that is secretly a container of other files (an installer, document, app bundle, disk image, or any archive) and wants to extract or inspect its inner contents — even when they don't say 'unbox' explicitly. Cracks ~30 'box-like' formats into clean directories with a manifest: standard archives (zip/tar/7z/rar), ZIP containers (docx/xlsx/pptx/jar/apk/whl), system packages (deb/rpm/msi), installers & disk images (exe/dmg/iso/pkg), and chained nested containers. Cross-platform (mac/linux/windows) via 7z as primary tool with graceful fallbacks. Triggers: 「拆箱」「开箱」「解压文件」「拆包」「解压任意文件」「提取容器内容」「拆开[文件]」「看[文件]里面」 / unbox, unpack any file, extract container, what's inside this file. Do NOT use for: writing extraction code/scripts, creating or editing Office documents, installing software, comparing archive formats, or merging files."
---

# unbox-anything

Universal unpacker for "box-like" files — the ones that look like a single file but are secretly a container of many files (an `.exe` installer, an `.docx` document, an `.apk` app, an `.asar` Electron bundle). Give it any such file and it cracks the box open into a clean directory, then writes a manifest describing what it found.

Designed for **agent-driven analysis** (crash investigation, reverse engineering, content extraction, build inspection), not for human-facing GUI workflows. Output is deterministic and structured so downstream steps can read it.

## Iron Rules (read first, every time)

These exist because unpacking unknown files can be dangerous. An `.exe` you unpack today might be malware; a `.dmg` auto-mounted into Finder can trigger preview handlers. The rules below keep the agent — and the user's machine — safe.

1. **Extract only. Never execute.** Never run, `source`, `open`, or double-click anything inside the extracted directory. Binaries (`.exe`, `.dll`, `.so`, `.dylib`, `.app`, scripts) are extracted as *bytes for inspection*, never launched. If a downstream task needs to run them, that is a separate human-approved step.
2. **Mount disk images read-only and quietly.** For `.dmg`/`.iso` on macOS, always pass `-nobrowse -readonly` to `hdiutil` so Finder does not auto-open and trigger preview handlers. Unmount immediately after copying files out.
3. **Detect encryption before extracting.** Run `7z l -slt <file>` first; if the output shows `Encrypted = +`, stop and report — do not let `7z` hang waiting on a password prompt. Ask the user for the password explicitly or skip.
4. **Always extract into a fresh directory.** Output to `<outname>-unboxed/` (suffix, never overwrite). Never extract into `.` or an existing populated dir — `7z`/`unar` will silently clobber.
5. **One source of truth per run.** Do not pipeline two different tools on the same source simultaneously; finish one extraction, verify, then recurse.

## Prerequisites

**Primary tool: `7z`** covers ~80% of formats (zip, 7z, tar, gz, bz2, xz, zst, cab, iso, rpm, deb, nsis, msi, ar, cpio, chm, and more). Install it once and most formats just work.

| Platform | Install command |
|----------|-----------------|
| macOS | `brew install p7zip` |
| Linux (Debian/Ubuntu) | `sudo apt install p7zip-full` |
| Linux (Fedora/RHEL) | `sudo dnf install p7zip p7zip-plugins` |
| Windows | `winget install 7zip.7zip` (or `choco install 7zip`) |

**Secondary tools** (only when a format demands them — install on demand):

- `unar` — for `.rar` (full read support including RAR5).
- `innoextract` — for Inno Setup `.exe` installers (cleaner than 7z for this format).
- `hdiutil` — **pre-installed on macOS** for `.dmg`.
- `xar` + `cpio` — for macOS `.pkg` (chain step).
- `npx @electron/asar` — for `.asar` Electron bundles (chain step; needs Node.js).

Full per-platform install commands and version notes live in [reference.md](reference.md).

## The Workflow (one pipeline for every file)

Run these six steps in order. Steps 1–4 are the happy path; step 5 is the recursion hook that makes chained formats (exe→asar, pkg→xar→cpio) work without special-casing; step 6 writes the manifest that makes the output auditable for downstream analysis.

### Step 1 — Detect the real type

File extensions lie. A `.exe` might be NSIS, Inno Setup, MSI-wrapped, or a self-extracting zip. Always confirm with the file's magic bytes before choosing a tool.

```bash
file "<input>"
# Also useful when `file` is unsure:
7z l "<input>"        # lists contents if 7z recognizes the format
```

If `file` and `7z` disagree, trust `7z l` (it understands more container formats). If both are unsure, check the magic-number table in [reference.md](reference.md#magic-numbers) and match the first bytes manually.

### Step 2 — Classify into a category

Look up the detected format in the [Classification Table](#classification-table) below. Every format maps to exactly one of five categories **A–E**. The category tells you which workflow to run — you do not need to think about the individual format again until step 5.

### Step 3 — Ensure the right tool is available (and check for encryption)

Check the category's required tool with `command -v`. If missing, print the install command from the Prerequisites table and **stop** — do not silently fall back to a different tool unless the category's workflow explicitly lists a fallback chain (using a different tool can produce inconsistent output that breaks downstream analysis).

While you are here, **run the encryption pre-check** (Iron Rule 3) so `7z x` never hangs waiting on a password prompt:

```bash
7z l -slt "<input>" | grep -i "^Encrypted"
# "Encrypted = -"  → safe, proceed to Step 4
# "Encrypted = +"  → STOP. Report to the user; do not run `7z x`.
```

This belongs in Step 3 rather than only in the Iron Rules, because an agent following the workflow linearly must hit it before extraction — otherwise a password-protected archive will block forever.

**Fallback chain for category A/B only** (standard archives + zip containers): if `7z` is missing, try `bsdtar` (pre-installed on macOS as `tar`) → `unzip` → stop and ask. For every other category, the listed tool is mandatory.

### Step 4 — Extract

Extract into a fresh `<outname>-unboxed/` directory. `<outname>` is the input file's **full name including its extension**, with every `.` replaced by `-` (hyphen). Keeping the extension (as `-docx`, `-exe`) records what type of container was unpacked; dots become hyphens so the directory name has no ambiguous extension separators.

| Input file | `<outname>` | Output dir |
|------------|-------------|------------|
| `report.docx` | `report-docx` | `report-docx-unboxed/` |
| `App-1.2.3-x64.exe` | `App-1-2-3-x64-exe` | `App-1-2-3-x64-exe-unboxed/` |

Never extract into `.` or an existing populated directory. The exact command is in each category's workflow below. Always pass `-y` (assume yes) so the agent does not hang on a prompt, and quote paths that may contain spaces or CJK characters.

### Step 5 — Scan for nested containers and recurse

This is what makes unbox-anything handle "boxes inside boxes". After *every* extraction (categories A–D), scan the output directory for files whose names or magic bytes match a **known nested container** (`.asar`, `.zip`, `.7z`, `.tar`, `.jar`, `.apk`, `.ipa`, `.whl`, `.egg`, `.deb`, `.rpm`, `.cab`, `.msi`, `.pkg`, `.dmg`, `.iso`, NSIS/Inno `.exe`).

When you find one, recurse: run the workflow again on that inner file, extracting it into `<innername>-unboxed/` beside it. Stop conditions (all three enforced):

- **Depth limit: 3.** Do not recurse beyond three levels — deeply nested packs are almost always either malicious or a packaging mistake, and a human should look.
- **Cycle guard.** Keep a set of absolute paths already extracted; never extract the same file twice (defends against zips that contain symlinks pointing back at themselves).
- **Known formats only.** Only recurse on the magic-number-confirmed list above. Do not recurse on arbitrary binaries "just in case".

Recursion is how an Electron installer becomes source code: `setup.exe` (category D, NSIS) → `$\PLUGINSDIR/app-64.7z` (category A) → `app/resources/app.asar` (detected in step 5) → `app-src/` (asar extract). One pipeline, no special-casing.

### Step 6 — Write the manifest

After the top-level extraction and any recursion completes, write `<outname>-unboxed/README.md` recording:

- Source file: name, size, detected type (`file` output), SHA-256.
- Extraction chain: a tree of every tool invoked and the directory it produced (so a reader can reproduce the chain by hand).
- Tool versions: `7z` / `unar` / `npx @electron/asar` versions actually used.
- File tree: a `tree`-style listing of the final output (depth-limited to 3 levels to avoid huge logs).
- Anomalies: encrypted entries skipped, permission errors, truncated files, anything suspicious.

The manifest is what makes the output trustworthy for downstream agent analysis — without it, the extraction is just "trust me, here are some files".

## Classification Table

The compact router. Find your format, run the category workflow. The full per-format detail (exact commands, magic numbers, edge cases) is in [reference.md](reference.md).

| Format(s) | Category | Primary tool |
|-----------|----------|--------------|
| `.zip` `.7z` `.tar` `.tar.gz`/`.tgz` `.tar.bz2` `.tar.xz` `.gz` `.bz2` `.xz` `.zst` `.lz4` | **A. Standard archive** | `7z` (rar→`unar`) |
| `.rar` | A | `unar` (7z is read-only for RAR5) |
| `.docx` `.xlsx` `.pptx` `.jar` `.war` `.ear` `.apk` `.aab` `.ipa` `.whl` `.egg` | **B. ZIP container** | `7z` (all are ZIP under the hood) |
| `.deb` `.rpm` `.msi` `.cab` | **C. System package** | `7z` (treats them as archives) |
| `.iso` | D (disk image) | `7z` / `bsdtar` |
| `.exe` (NSIS installer) | **D. Installer / image** | `7z` |
| `.exe` (Inno Setup) | D | `innoextract` |
| `.dmg` | D | macOS: `hdiutil`; others: `7z` (weak) |
| `.pkg` (macOS) | **E. Chain** | `xar` then `cpio` |
| `.asar` (Electron) | E (usually reached via recursion) | `npx @electron/asar` |
| `.old` `.doc` `.xls` `.ppt` (legacy Office) | — | **Out of scope.** These are binary OLE, not ZIP. Point the user at a converter (LibreOffice/antiword), do not pretend. |

Formats not listed here (`.snap`, `.AppImage`, encrypted/packed malware like UPX) are **explicitly out of scope** — see *Out of Scope* below.

## Category Workflows

### A. Standard archive (`zip`, `7z`, `tar*`, `gz`, `rar`, …)

```bash
7z x "<input>" -o"<outname>-unboxed" -y
# For .rar without unar installed, install it first:
#   brew install unar  /  sudo apt install unar
unar "<input>" -o "<outname>-unboxed"
```

`bsdtar` (macOS default `tar`) is a zero-dependency alternative for tar/zip/zst on Mac when 7z is unavailable: `bsdtar -xf "<input>" -C "<outname>-unboxed"`.

### B. ZIP container (`docx`, `xlsx`, `apk`, `jar`, `whl`, …)

Identical command to A — they are all ZIP. After extraction, note in the manifest that structured content is available for downstream reading: OOXML exposes `word/document.xml`, `xl/sharedStrings.xml`, etc.; `.apk`/`.jar` expose `AndroidManifest.xml` / `META-INF/MANIFEST.MF`; `.whl` exposes `METADATA` and the package source.

```bash
7z x "<input>" -o"<outname>-unboxed" -y
```

### C. System package (`deb`, `rpm`, `msi`, `cab`)

`7z` treats all four as archives and extracts their payload. For `.deb` on Linux, `dpkg-deb -x` is the native tool; for `.rpm`, `rpm2cpio <file> | cpio -idmv`. Prefer the native tool when on the matching platform, fall back to `7z` elsewhere.

```bash
7z x "<input>" -o"<outname>-unboxed" -y
```

### D. Installer / disk image (NSIS `exe`, Inno `exe`, `dmg`, `iso`)

These need format-specific handling because their headers differ.

**NSIS installer** (the most common `.exe` installer; detected by `file` reporting "Nullsoft Installation"):
```bash
7z x "<input>" -o"<outname>-unboxed" -y
# The payload is usually in $PLUGINSDIR/app-*.7z — recurse on it in step 5.
```

**Inno Setup installer** (detected by "Inno Setup" in `file` output, or magic bytes):
```bash
innoextract -d "<outname>-unboxed" "<input>"
```

**`.dmg` on macOS** (always `-nobrowse -readonly`, mount-then-copy-then-unmount):
```bash
hdiutil attach "<input>" -nobrowse -readonly -mountpoint /tmp/unbox-dmg-$$
cp -R /tmp/unbox-dmg-$$/* "<outname>-unboxed"/ 2>/dev/null
hdiutil detach /tmp/unbox-dmg-$$
```
On Linux/Windows, `7z` can read many DMGs but not all (UDZO vs UDIF): try `7z x`, and if it fails, tell the user DMG extraction on their platform is unreliable for this file.

**`.iso`**: `7z x "<input>" -o"<outname>-unboxed" -y` (or `bsdtar -xf` on macOS).

### E. Chain / nested (`.pkg`, `.asar`, and anything step 5 finds)

Two sub-types:

**`.pkg` (macOS installer)** — `xar` archive containing a `Payload` file (a cpio archive, optionally gzip'd):
```bash
7z x "<input>" -o"<outname>-unboxed" -y          # or: xar -xf "<input>" -C "<outname>-unboxed"
cd "<outname>-unboxed"
# Payload naming + compression both vary across pkgs — do not hardcode.
# 7z sometimes renames it "Payload~"; some pkgs gzip it, some ship raw cpio.
PAYLOAD=$(find . -maxdepth 1 -iname "Payload*" -type f | head -1)
case "$(file "$PAYLOAD")" in
  *gzip*) gunzip -c "$PAYLOAD" | cpio -idmv ;;   # common case: gzipped cpio
  *cpio*) cpio -idmv < "$PAYLOAD" ;;             # some pkgs ship raw cpio
  *) echo "Unrecognized Payload format: $PAYLOAD" ;;
esac
```

**`.asar` (Electron bundle)** — reached almost always via recursion from an Electron installer (NSIS exe → app-*.7z → app.asar):
```bash
npx @electron/asar extract "<input>" "<outname>-unboxed"
```

For any *other* nested container found in step 5, just re-run the whole workflow (steps 1–6) on it.

## Out of Scope

These are deliberately not handled. If a user asks, explain why and suggest an alternative rather than faking it:

- **`.AppImage`** — a self-extracting ELF that runs in place. Extracting it safely requires `--appimage-extract` which executes the binary; that violates Iron Rule 1. Suggest running it in a sandbox instead.
- **`.snap`** — squashfs image; needs `unsquashfs` which is rarely installed. Out of scope for v1.
- **Packed/encrypted malware** (UPX, Themida, password-protected archives the user won't unlock) — these belong to security research tooling, not a general unpacker.
- **Legacy binary Office** (`.doc`/`.xls`/`.ppt`) — OLE compound documents, not ZIP. Use LibreOffice or `antiword` to convert; do not pretend `7z` handles them.
- **Creating/editing** Office documents — that is what `anthropics/skills@docx` and friends are for. unbox-anything only *extracts*.

## Pitfalls (the non-obvious ones)

These are the traps that bite without warning. Skim them once and they will not bite twice.

- **`$PLUGINSDIR` shell expansion.** NSIS installers extract to a directory literally named `$PLUGINSDIR`. In bash, `$PLUGINSDIR` is variable expansion — quote it or escape the `$`: `'\$PLUGINSDIR'` or `"\$PLUGINSDIR"`. Same for any path containing a literal `$`.
- **Encrypted archives hang `7z`.** Always run `7z l -slt "<input>"` and grep for `Encrypted = +` *before* `7z x`. If encrypted, do not run `7z x` — it will block waiting for a password that never comes.
- **`.dmg` auto-opens in Finder.** Without `-nobrowse`, macOS mounts the DMG and Finder may render icons, run preview handlers, or re-trigger Quick Look. Always `-nobrowse -readonly`, always detach.
- **Unicode filenames in terminals.** `7z` and `unar` extract them correctly, but a non-UTF-8 terminal will display mojibake. Set `LANG=en_US.UTF-8` (or the user's locale) before listing if the listing looks corrupt.
- **`.exe` type detection ambiguity.** `file` sometimes reports just "PE32 executable" without naming NSIS/Inno. If the installer type is unclear, try `7z l` first — if it lists contents, it is NSIS or self-extracting; fall back to `innoextract -l` to detect Inno.
- **`.pkg` Payload naming and compression vary.** The payload inside a macOS `.pkg` is usually named `Payload` and gzip-compressed, but 7z may extract it as `Payload~`, and some pkgs (e.g. Microsoft Office installers) ship raw cpio with no gzip wrapper. Always locate the payload by `find -iname "Payload*"` and branch on `file` output (`*gzip*` → `gunzip|cpio`, `*cpio*` → `cpio` direct) rather than assuming one shape.
- **`app.asar` vs `app.asar.unpacked/`.** Electron apps ship both. `asar extract` only handles the `.asar` file; the `.unpacked/` directory already contains loose files — copy it as-is, do not try to "extract" it.
- **Large `.iso`/`.dmg` (multi-GB).** Extraction doubles disk usage. Note the size in the manifest; if the destination volume is low on space, warn before extracting.

## Reference

For the exhaustive material — full per-format × per-platform tool matrix, complete install commands (including `innoextract`, `xar`, Node.js), magic-number byte sequences for type detection, and per-format edge cases — see [reference.md](reference.md).

That file is intentionally separate so this SKILL.md stays a lean decision document. Read it when you need a command this file does not show, or when type detection in step 1 is ambiguous.
