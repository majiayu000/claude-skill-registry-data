---
name: literature-to-manga
description: Convert selected prose, novel, biography, history, or text-archive works into manga adaptation packages. Use when asked to pick books from a local literature repository, assess manga adaptability, extract plots and characters, design chapters, write manga panel scripts, create storyboard briefs, or generate visual prompt packs for comic adaptation.
---

# Literature To Manga

## Overview

Use this skill to turn a source work or a folder of candidate books into a manga adaptation package. Default source archive: the folder in `$LITERATURE_BOOKS_DIR`, if set.

The default output is an adaptation dossier, manga bible, chapter/page/panel script, storyboard brief, and image prompt pack. Copyright is not a hard gate by default, but every package must include source attribution and a publication-risk note.

## Workflow

1. Locate the archive or source file.
   - If no path is provided, use `$LITERATURE_BOOKS_DIR`; if that is not set either, ask the user where the books are.
   - For candidate discovery, run `scripts/inventory_books.py`.
   - For source extraction, run `scripts/extract_text.py`.
   - For long texts, run `scripts/chunk_source.py` before deep adaptation.

2. Inventory and rank candidates.
   - Score narrative clarity, character strength, scene density, visual potential, length fit, and adaptation difficulty.
   - Prefer works with visible scene changes, strong conflict, recurring cast, and clear episodic arcs.
   - Use `assets/templates/candidate-dossier.md` for shortlist output.
   - Read `references/source-handling.md` when file formats, encoding, or archive extraction is uncertain.

3. Build the adaptation brief.
   - Define premise, audience, format, tone, season/chapter target, transformation strategy, and source-fidelity stance.
   - Use `assets/templates/adaptation-brief.md`.
   - Read `references/adaptation-workflow.md` for the scoring rubric and adaptation phases.

4. Build the manga bible.
   - Include logline, world rules, cast, character designs, relationships, plot arcs, recurring locations, visual motifs, and continuity rules.
   - Use `assets/templates/manga-bible.md`.
   - Read `references/visual-style-taxonomy.md` before choosing art direction or image prompt language.

5. Write chapter scripts and storyboard briefs.
   - Convert prose beats into pages and panels, not long narration.
   - Each panel needs shot type, visible action, dialogue/caption text, mood, and continuity notes.
   - Use `assets/templates/chapter-script.md`.
   - Read `references/manga-script-format.md` for panel syntax and pacing rules.

6. Generate image prompt packs.
   - Create one JSONL row per key panel or character sheet prompt.
   - Keep character identity, style, composition, lighting, and negative constraints explicit.
   - Use `assets/templates/storyboard-prompts.jsonl`.

7. Run adaptation QA.
   - Check source fidelity, continuity, character consistency, panel readability, pacing, and prompt reuse.
   - Mark invented material clearly.
   - Include a publication-risk note when the source is not confirmed public domain or licensed.

## Output Contract

For a full package, create or return:

- `candidate-dossier.md`
- `adaptation-brief.md`
- `manga-bible.md`
- `chapter-01-script.md`
- `storyboard-prompts.jsonl`
- `qa-notes.md`

If the user asks only to pick books, stop after the candidate dossier and recommendations. If the user already picked a work, skip broad inventory and start with source extraction plus the adaptation brief.
