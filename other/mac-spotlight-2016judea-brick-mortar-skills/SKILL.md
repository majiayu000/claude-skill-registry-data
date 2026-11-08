---
name: mac-spotlight
description: Find files on a Mac the way Spotlight does, from the shell — by kind, date, content, name or Finder tag — and read or write Finder tags. Use when you say "find all PDFs I touched this week", "search my Mac for the file that mentions X", "what's tagged Red", "tag these files", "why can't Spotlight find it", "is this folder indexed". Covers mdfind query syntax, mdls attributes, tag xattrs, mdimport/mdutil, and the four ways the index silently returns nothing.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Built-in tools only: mdfind, mdls, mdutil, mdimport, xattr, plutil. No network.
metadata:
  grounded: "2026-11-03 — every command below run live on macOS 26.6"
---

# Spotlight from the shell

`mdfind` is a query against the Spotlight index, not a walk of the disk. That makes it
instant on a million files, and it means **an empty result proves nothing** until you have
ruled out the four traps at the bottom. When the answer has to be exhaustive, fall back to
`find`.

## Queries that work

Always scope with `-onlyin` (faster, and keeps the result off system caches). Pipe stderr
to `/dev/null`: on macOS 26 every `mdfind` call prints two `[UserQueryParser] Loading
keywords...` lines to stderr even on success.

```bash
mdfind -onlyin ~/Documents "quarterly report" 2>/dev/null          # full-text + metadata
mdfind -onlyin ~/Documents -name invoice 2>/dev/null               # filename substring
mdfind -onlyin ~ -count 'kMDItemContentTypeTree == "com.adobe.pdf"' 2>/dev/null
mdfind -onlyin ~ 'kind:pdf' 2>/dev/null                            # same result, natural syntax
mdfind -onlyin ~/Desktop 'kMDItemFSContentChangeDate >= $time.today(-7) && kMDItemContentTypeTree == "public.image"' 2>/dev/null
mdfind -onlyin ~ 'kMDItemUserTags == "Red"' 2>/dev/null           # by Finder tag
mdfind -onlyin ~ 'tag:Red' 2>/dev/null                             # same, natural syntax
mdfind -onlyin ~/Downloads 'kMDItemWhereFroms == "*github.com*"c' 2>/dev/null  # downloaded from
mdfind -onlyin ~ 'kMDItemFSSize > 500000000' 2>/dev/null           # files over 500 MB
```

- Use **`kMDItemContentTypeTree`**, not `kMDItemContentType`, for kinds: the tree matches
  parents, so `public.image` catches PNG, JPEG and HEIC, and `public.movie` catches every video.
- Single-quote the whole query so the shell leaves `$time` and `*` alone.
- Suffix modifiers on a string: `c` case-insensitive, `d` diacritic-insensitive, `w` word.
- Time functions: `$time.today(-7)`, `$time.this_month`, `$time.iso(2026-01-01T00:00:00Z)`.
- `mdfind -live ...` keeps running and prints changes; useful in a watcher, never in a one-shot.

## What a file actually carries

```bash
mdls file.pdf                                  # every attribute
mdls -name kMDItemContentType -name kMDItemKind -name kMDItemFSSize file.pdf
mdls -raw -name kMDItemWhereFroms file.zip     # download URL; prints (null) if none
```

`mdls` is how you discover the attribute name for a query: inspect a file that should
match, copy the key.

## Finder tags — read and write without a third-party tool

Tags live in the extended attribute `com.apple.metadata:_kMDItemUserTags` as a plist array.
A colour tag is `"Name\nN"` (newline, then the colour index: 1 grey, 2 green, 3 purple,
4 blue, 5 yellow, 6 red, 7 orange). A plain label has no suffix.

```bash
# read
xattr -p com.apple.metadata:_kMDItemUserTags file.txt | plutil -p -
# write (REPLACES all tags on the file)
xattr -w com.apple.metadata:_kMDItemUserTags '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><array><string>Red
6</string><string>project-x</string></array></plist>' file.txt
mdimport file.txt                               # push the change into the index now
mdls -name kMDItemUserTags file.txt
```

- Writing replaces. To add a tag, read the array, append, write the whole array back.
- `cp` keeps the tags (it copies xattrs). `cat a > b` and most uploads drop them.
- If `brew install tag` is acceptable, `tag -a Red file` / `tag -l` is friendlier; the
  xattr route needs nothing installed.

## Index status and repair

```bash
mdutil -s /                        # "Indexing enabled." is what you want
mdutil -s /path/to/volume          # external disks are often off
mdimport /path/to/file             # re-index one file immediately (no sudo)
```

`sudo mdutil -E /` erases and rebuilds the whole index (hours, high CPU). It needs a
human with an admin password and it is almost never the fix. Reach for it only when a
whole volume returns nothing.

## The four ways mdfind returns nothing and lies about it

1. **The path is not indexed.** `/tmp`, `/private/tmp`, scratch dirs, many external
   volumes and anything under a folder ending `.noindex` are never indexed. Tell:
   `mdutil -s <path>` prints `Error: unknown indexing state.` or `Indexing disabled`.
   Verified: a file in `/private/tmp` with unique text returned 0 hits forever.
2. **The file is too new.** Indexing lags. Measured: a new file under `~` took ~6 s to
   appear. In a script, `mdimport` the file first or poll for a few seconds.
3. **Privacy exclusions.** System Settings > Spotlight > Search Privacy hides folders
   from `mdfind` with no message. Ask, or check with `find`.
4. **Your process lacks access.** Results inside TCC-protected folders (Desktop,
   Documents, Downloads, Mail, Messages) only come back if the calling app has the grant.
   See the `mac-permissions` skill.

When an exhaustive answer matters (a deletion, an audit), confirm with
`find <dir> -iname '*term*'` or `grep -rl`. Spotlight is for speed, not for proof.
