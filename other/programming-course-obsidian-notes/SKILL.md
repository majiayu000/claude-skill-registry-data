---
name: programming-course-obsidian-notes
description: Convert programming-course PPTs, PDFs, handouts, screenshots, or code materials into durable Chinese Obsidian learning notes. Use when the user wants one reusable Markdown note per lesson, a course index, or a Base view for long-term relearning and syntax lookup. Do not use for non-programming courses or standalone evergreen concept notes unrelated to a lesson.
---

# Programming Course Obsidian Notes

Turn programming course materials into notes that work as a self-study text, code reference, and memory-recovery guide. Optimize for being able to relearn the topic months later, not for reproducing slides or preparing for exams.

Before handling course material, read [references/note-spec.md](references/note-spec.md) completely. It defines the required content selection, YAML, note structure, naming, index, and validation rules.

## Workflow

1. Inspect the complete source before drafting. For PPT/PPTX or PDF, use the corresponding presentation or PDF workflow so that code screenshots, diagrams, and speaker notes are not silently missed.
2. Identify course metadata from the material or the user's instructions. Use `unknown` for unavailable values; never invent a teacher, semester, date, or source.
3. Build the lesson's knowledge structure before writing. Merge repeated animation slides and reorganize by concepts rather than slide numbers.
4. Create one UTF-8 Markdown note per source lesson in the user's requested Vault folder.
5. For a multi-lesson batch, keep filenames, YAML fields, section structure, tags, and cross-links consistent. Use `Lesson NN - 主题.md` when lesson numbering is available unless the user chooses another scheme.
6. When the user requests a course directory, create or update an index note such as `0Python.md` with ordered lesson links, a short learning path, and concise descriptions.
7. When the user requests an Obsidian Base, or explicitly invokes the Bases workflow, create a `.base` file scoped to the generated course notes and embed its named view in the index note.
8. Validate the finished files and links. If the official Obsidian CLI is available, use it only for index-aware checks, Base queries, and link-aware renames; use normal filesystem tools for ordinary reading and writing.

## Content Boundary

- By default, exclude cases, exercises, project requirements, classroom activities, and exam-oriented material copied from the source.
- Preserve reusable knowledge: concepts, motivation, syntax, parameters, return values, execution behavior, common operations, use cases, comparisons, pitfalls, and quick-reference code.
- Minimal self-written examples are allowed when they are necessary to explain a concept. Keep each example independently understandable and show its output when useful.
- Do not turn the note into a page-by-page summary or a chat transcript.
- Correct clear technical inaccuracies instead of copying them. Mark necessary material not present in the source with an Obsidian `info` callout so the reader can distinguish supplementation from course content.
- Do not add self-tests or answer sections unless the user asks for them. If included, reference answers must use a collapsed `[!question]-` callout and must not use HTML disclosure elements.

## Obsidian Integration

- Use Wiki links for notes inside the Vault and Markdown links for external URLs.
- Keep cross-links selective: link lesson notes and stable concepts that are likely to recur, not every keyword or function name.
- Preserve existing frontmatter and unrelated index content when updating files.
- Use the Obsidian Markdown skill for extended syntax, the Obsidian Bases skill for `.base` files, and the Obsidian CLI skill only when the requested operation depends on the running application or its index.

## Parallel Work

When the user explicitly requests subagents for multiple source files, assign exactly one lesson to each subagent and reserve the primary agent for shared conventions, remaining lessons, integration, and final validation. Give every subagent the same naming, YAML, exclusion, and link rules. Do not let multiple agents edit the same note or index file.

## Completion Criteria

Do not finish until:

- every requested source lesson has one real `.md` file;
- filenames and lesson numbers are consistent;
- YAML fields are present and use `unknown` rather than invented metadata;
- code fences and callouts render correctly;
- source cases, exercises, and projects have been excluded as requested;
- obsolete filenames and unresolved course links are gone;
- the index and Base, when requested, reference every lesson exactly once;
- a Base query succeeds when CLI validation is available.
