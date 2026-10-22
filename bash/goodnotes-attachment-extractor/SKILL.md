---
name: goodnotes-attachment-extractor
description: Extract embedded audio recordings, JPEG/PNG images, and PDF documents from GoodNotes .goodnotes exports, with optional metadata inspection and recursive batch processing. Use when the user provides a .goodnotes file or a folder of notes and asks to extract, export, recover, inspect, or organize its attachments. Triggers include .goodnotes, GoodNotes 附件, 提取录音/图片/PDF, 导出笔记附件, 附件全是 UUID, and batch extraction of note attachments.
---

# GoodNotes Attachment Extractor

Extract M4A/AAC recordings, JPEG/PNG images, and PDF documents from a
GoodNotes <code>.goodnotes</code> export. The file is a ZIP container; this
skill reads it locally with the Python standard library, never modifies it,
and makes no network requests.

## Workflow

1. Confirm the path is a <code>.goodnotes</code> file or a directory containing them.
2. Run inspection first and report counts and types to the user.
3. Extract to an explicit output directory when possible; otherwise the script
   writes a sibling <code>&lt;name&gt;_提取/</code> folder.
4. Report the output path, per-type counts, and any errors.
5. Never modify, move, or delete the source file.

~~~bash
python scripts/gn_extract.py --info "笔记.goodnotes"
python scripts/gn_extract.py "笔记.goodnotes" -o "导出目录"
python scripts/gn_extract.py "笔记.goodnotes" --json
python scripts/gn_extract.py "笔记目录" -o "导出根目录"
~~~

When the working directory is not the skill folder, run the script by its
installed path, for example:

~~~bash
python "$HOME/.claude/skills/goodnotes-attachment-extractor/scripts/gn_extract.py" --info "笔记.goodnotes"
~~~

On Windows PowerShell, use the full path to the installed skill instead of $HOME.

## Output layout

Default output is organized by type:

~~~text
<name>_提取/
├── 音频/录音_11m26s.m4a
├── 图片/图片_2048x1536.png
└── 文档/文档_A08519D7.pdf
~~~

- Audio: <code>录音_&lt;minutes&gt;m&lt;seconds&gt;s.m4a</code>; fall back to the
  UUID prefix when duration cannot be parsed.
- Image: <code>图片_&lt;width&gt;x&lt;height&gt;.&lt;ext&gt;</code>; fall back to the
  UUID prefix when dimensions cannot be parsed.
- PDF: <code>文档_&lt;uuid8&gt;.pdf</code>.
- Duplicate filenames receive <code>_1</code>, <code>_2</code>; existing files are
  never overwritten.
- Batch mode writes one <code>&lt;name&gt;_提取/</code> folder per input under
  the output root.

## Options

- <code>--info</code> inspect only, do not extract.
- <code>--json</code> print a JSON array with counts, items, and output paths.
- <code>--no-organize</code> write all files to one flat folder.
- <code>--no-audio</code> / <code>--no-image</code> / <code>--no-pdf</code> filter types.
- Directories are scanned recursively for <code>*.goodnotes</code>.

## Failure handling

- A <code>BadZipFile</code> or non-ZIP input is not a valid export: ask the user
  to re-export from GoodNotes.
- Zero attachments means the export likely omitted them: check the GoodNotes
  export options before retrying.
- Permission denied: choose a writable output directory and rerun.
- Missing duration or dimensions only affects filenames; extraction still succeeds.
- The script reads one attachment into memory at a time. For very large
  containers, prefer the full desktop app or extract in smaller batches.

## Privacy

Keep everything local: do not upload note files, extracted media, or logs.
Do not echo note contents. When sharing results, avoid exposing the user's full
filesystem path.

## Related full project

The desktop GUI and CLI live at
https://github.com/ou0826/goodnotes-attachment-extractor (MIT).
Use the full app when the user wants a graphical interface; use this skill for
agent-driven extraction and inspection.
