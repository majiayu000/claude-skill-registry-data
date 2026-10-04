---
name: tool-chm-reader
description: Read and digest CHM (compiled HTML Help) files — decompile via 7-Zip or Windows hh.exe, then info, TOC, topic-range extract, keyword search, or full-dump to a markdown file (token-cheap, re-readable later via Read/Grep). Use when the user says "read this chm", "what's in this help file", "search the help file for <term>", or hands over a .chm (software help like cymcap.chm). NOT for PDFs (use tool-pdf-reader) or digesting the dumped output into KB notes (dump first, then use eos-kb-atomize / vault-source-digest conventions on the .md).
---

# CHM Reader Skill

Read CHM (compiled HTML Help — `.chm`) files: software help files, offline manuals. Two modes, mirroring `tool-pdf-reader`: **chunked stdout** (read topics as you go, costs context) and **full-dump to a markdown file** (token-cheap, re-readable via Read/Grep).

Zero pip dependencies. Decompiles with **7-Zip** (`7z`, checked on PATH + `C:\Program Files\7-Zip`) or falls back to Windows' built-in **`hh.exe -decompile`**. Extraction is cached in `%TEMP%/chm_tool/` keyed by file identity, so repeated commands don't re-decompile.

`SKILL_DIR` below = this skill's directory (`skills/tool-chm-reader/` in the repo, or `~/.claude/skills/tool-chm-reader/`).

## Usage

### 1. Get CHM info

```bash
python "<SKILL_DIR>/chm_tool.py" info "path/to/file.chm"
```

Returns: size, title, HTML page count, TOC entry count, cache dir.

### 2. Table of contents

```bash
python "<SKILL_DIR>/chm_tool.py" toc "path/to/file.chm"
```

Numbered, indentation shows hierarchy. The numbers are what `extract --start/--end` addresses. CHMs without a `.hhc` sitemap fall back to a flat page list (same numbering).

### 3. Extract topics (TOC-number range, stdout)

```bash
python "<SKILL_DIR>/chm_tool.py" extract "file.chm" --start 11 --end 30
```

Read 10–30 topics at a time. **Use when** triaging which sections matter, or you only need one chapter.

### 4. One page by internal path

```bash
python "<SKILL_DIR>/chm_tool.py" page "file.chm" bonding.htm
```

### 5. Search

```bash
python "<SKILL_DIR>/chm_tool.py" search "file.chm" "cross bonding"
```

Case-insensitive, whole archive; prints TOC entry + matching line snippets. Search is literal — try both `crossbonding` and `cross bonding` style variants for compound terms.

### 6. Dump the whole CHM to markdown (token-saver)

```bash
python "<SKILL_DIR>/chm_tool.py" dump "file.chm" "path/to/output.md"
```

One markdown file, TOC-ordered, heading depth mirroring the TOC hierarchy, `<!-- source: page.htm -->` markers per topic, non-TOC pages appended under "Unlisted pages".

- **Use when** the CHM will be referenced more than once: dump once, then `Read`/`Grep` the .md in this and future sessions.
- For a vault CHM, dump beside it: `Foo/bar.chm` → `Foo/bar-extracted.md` (matches the `*-extracted` convention from tool-pdf-reader).
- A 381-topic / 18 MB CHM dumps to ~490 KB of markdown in seconds.

## Workflow for digesting a software help file

1. `info` — size + page count.
2. `toc` — understand the manual's structure; pick the chapters that matter.
3. `dump` to a sibling `*-extracted.md` — the durable artifact.
4. Read/Grep the .md; hand-write digests or KB notes from it (KB digestion itself belongs to the KB skills, not this one).

## Notes

- Content conversion is stdlib HTML→markdown (headings, lists, tables, pre, bold/italic, image alt text). Screenshots/toolbar-icon images render as nothing or `![alt]` — CHM manuals lean on inline images, so occasional "click on ." gaps are the image placeholders, not extraction bugs.
- CHM pages are commonly `windows-1252`; the reader honours each page's meta charset.
- `.chm` files downloaded from the internet may need "Unblock" in file Properties before *Windows' viewer* renders them — this tool reads them regardless (7z/hh don't care about the zone marker).
- Fresh Linux/mac clones need `7z` (p7zip) installed; Windows works out of the box via `hh.exe` even without 7-Zip.

## Trigger phrases

| User says | Action |
|-----------|--------|
| "read this chm" / "what's in this help file" | `info` → `toc` → `extract` chunks |
| "search the help for X" | `search` |
| "dump the chm" / "save it as markdown" | `dump` to sibling `*-extracted.md` |
| hands over software-info zip with .chm inside | extract zip → `dump` each .chm |
