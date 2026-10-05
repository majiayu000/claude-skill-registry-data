---
name: auto-luhmann-numberer
description: Assign, validate, normalize, and explain Luhmann/Zettelkasten-style project-note codes for Chinese book manuscripts, Obsidian Markdown folders, Mandala-Grid section files, HyperCard Markdown stacks, and project-note JSON to EPUB workflows. Use when Codex needs to scan folders for 部/章/節/項/目 numbering, generate stable card ids, insert branch codes without renumbering existing notes, map letter-coded branches to Obsidian Mandala sections, preserve K### keyword index cards, sanitize private catalogs into public examples, or prepare card IDs for EPUB and HyperCard output.
---

# 自動魯曼編號機

Use this skill to manage stable writing-system addresses for book manuscripts and card boxes. Prefer the active book outline as the topic-number seed, then let Luhmann-style branches grow inside the outline without renumbering existing notes. When publishing the skill or sharing outputs, reduce real catalogs to a small public example.

## Core Model

Use four separate namespaces:

- `book_topic_code`: pure numeric book addresses, at most five levels: 部、章、節、項、目. Examples: `1`, `1.1`, `1.1.3`, `1.1.3.2.1`.
- `luhmann_branch_code`: letter or mixed suffixes that grow from a book address. Examples: `1.1.a`, `1.1.E`, `1.1.c3b`, `1.1.d.1`.
- `mandala_section_code`: local Obsidian Mandala-Grid section comments inside one Markdown file. Examples: `<!--section: 1-->`, `<!--section: 1.7-->`, `<!--section: 1.8.8-->`.
- `keyword_index_code`: index-card ids such as `K001`, kept separate from topic codes.

Never merge these namespaces. A `K001` card is not a chapter. A local `section: 1.7` is not the book's `1.7` chapter unless the source explicitly says so.

## Default Preferences

Read `references/public-numbering-rules.json` when you need the numbering taste, output schema, public-case policy, or Mandala section shape. The bundled example is intentionally minimal and safe to publish.

Important defaults:

- Use book chapter numbers as the ZKII-like topic seed.
- Preserve existing codes; do not renumber old cards just because a new card appears.
- Use letter branches such as `1.1.a` to `1.1.g` for lateral inserts under a chapter.
- Keep compact variants such as `1.1.c1`, `1.1.c3a`, and `1.1.c3b` when they already exist.
- Treat letter-coded Markdown files with `mandala: true` or `<!--section: ...-->` markers as Mandala containers.
- Do not publish complete manuscript catalogs, absolute local paths, or private source titles unless the user explicitly asks for a private artifact.

## Workflow

1. Identify the source surface:
   - Folder of Markdown files.
   - Project-note JSON.
   - HyperCard Markdown stack.
   - EPUB catalog/build script.
   - One new card that needs a code.

2. Build or load a catalog:
   - Use `scripts/extract_book_codes.mjs <folder>` to scan Markdown/TXT/JSON files and write a relative-path catalog.
   - Use an existing catalog JSON if provided.
   - Keep every entry's `code`, `title`, `kind`, `source_path`, `depth`, and any `off_prefix_codes`.

3. Classify each code:
   - Pure numeric code: `部/章/節/項/目` by dot depth.
   - Code with letters: `luhmann_branch`.
   - `K###`: `keyword_index`.
   - `<!--section: ...-->`: local Mandala section.

4. Validate:
   - Flag missing chapter numbers, duplicate codes, codes deeper than five numeric levels, and off-prefix codes.
   - Flag likely local Mandala sections so they do not pollute book-level numbering.
   - Treat off-prefix codes as "待校正或跨章引用", not immediate errors.

5. Assign a new code:
   - If the note belongs to an existing pure numeric chapter, place it under the closest chapter.
   - If it is a lateral insert, use a Luhmann branch suffix instead of renumbering neighbors.
   - If it belongs inside a Mandala file, assign a display code like `1.1.E｜1.7`.
   - If it is an index concept, use the next `K###`.

6. Explain the decision:
   - Return the assigned code, code kind, parent code, previous/next neighbors, source assumption, and warnings.

## Common Requests

- "Scan this folder and list every 部、章、節、項、目 code."
- "Find missing chapter numbers and off-prefix card ids."
- "Give this new note a Luhmann number without renumbering old cards."
- "Convert Mandala section addresses into display ids for HyperCard."
- "Prepare project-note JSON codes for EPUB export."

## Output Shape

For a folder scan, produce both human and machine output when useful:

```json
{
  "summary": {
    "chapters": ["1.1"],
    "missing": [],
    "warnings": []
  },
  "catalog": [
    {
      "code": "1.1.3",
      "title": "努力：先吃青蛙",
      "kind": "節",
      "source_path": "examples/1.1-fast-day-plan.md"
    }
  ]
}
```

For a single new card, return:

```json
{
  "assigned_code": "1.1.E｜1.7",
  "code_kind": "mandala_section",
  "parent_code": "1.1.E",
  "section_code": "1.7",
  "reason": "The note belongs inside the existing Mandala branch file for non-linear numbering.",
  "warnings": []
}
```

## Public Sharing Rule

Before making a repository public, remove or replace:

- Complete book catalogs that reveal the manuscript structure.
- Absolute local paths.
- Raw source excerpts or private chapter titles.
- EPUB files generated from private catalogs.

Keep only `references/book-chapter-card-catalog.*` as a public FAST day-plan example unless the user asks for a private build.

## Bundled Resources

- `references/public-numbering-rules.json`: namespace rules, public-case policy, and example output contract.
- `references/book-chapter-card-catalog.json`: public example catalog for `1.1 FAST 日計劃`.
- `references/book-chapter-card-catalog.md`: human-readable public example catalog.
- `scripts/extract_book_codes.mjs`: scan a supplied folder and regenerate a relative-path catalog.
- `scripts/validate_luhmann_catalog.py`: validate catalog JSON for duplicates, depth, malformed Mandala sections, and off-prefix codes.
- `scripts/build_skill_guide_epub.py`: build the teaching EPUB in `assets/`.
- `assets/自動魯曼編號機_使用手冊_公開版_2026-06-17_03.epub`: public teaching ebook.
