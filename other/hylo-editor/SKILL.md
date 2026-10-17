---
name: hylo-editor
description: "Write and revise notes live inside Hylo's open editor with the editor_type, editor_read and editor_rewrite MCP tools, so the user watches the text being typed. Use this skill whenever the user wants writing to happen in the editor — 'write it in the editor', 'type this into my note', 'continue where my cursor is', 'rewrite this paragraph', 'improve what I selected', 'fix the second section', '写到编辑器里', '接着我光标的位置写', '改写我选中的这段', '润色这一段' — or whenever you plan to call any editor_* tool. Also covers Hylo's markdown dialect (wikilinks, wiki images, mindmap blocks, tasks, tables) for anything typed into a note."
---

# Hylo Editor — live writing through MCP

The editor tools drive the Hylo editor the user has open: the note is opened in front of them, a purple "Agent" caret types the text in human rhythm, and each call lands as **one undo step** (Cmd/Ctrl+Z reverts it). The tools need the Hylo app to be open.

## Environment check

You need `editor_type`, `editor_read` and `editor_rewrite` (possibly shown as `mcp__hylo__editor_type` or `hylo_editor_type`). If they are not in your tool list, search your deferred tools for "hylo editor". If they still are not there, tell the user live editing is unavailable and ask whether to write the file directly instead. Never decide that on your own.

## Commit to the editor

Once a request is going through the editor, every write for it goes through the editor:

- **Do not** fall back to `create`, `append`, `prepend` or any file write for the same edit when an editor tool fails. The editor may still be typing, and a parallel file write duplicates text or races autosave.
- On failure, report what happened and let the user decide.

Use the regular note tools rather than the editor when the user did not ask to watch, or for bulk/background work: many files, imports, generated reports, edits to notes the user isn't looking at.

## Tools

### editor_type: insert new text

| Param     | Meaning                                                                                                                           |
| --------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `path`    | Vault-absolute path, e.g. `/journal/2026-10-10.md`. Missing notes are created empty.                                              |
| `content` | Markdown to type. Trailing whitespace is trimmed.                                                                                 |
| `at`      | `end` (default) or `cursor`, which inserts at the user's caret.                                                                   |
| `heading` | Types at the end of that section instead. The heading text is matched case-insensitively, with or without `#`. It wins over `at`. |
| `speed`   | `slow`, `normal` (default), `fast` or `instant`.                                                                                  |

- Blank lines are added around the content so it lands as its own block. Don't pad it with leading or trailing newlines.
- The exception is `at: "cursor"` in the middle of a line, which inserts inline exactly where the caret is.
- A new path fails if another note with the same file name exists anywhere in the vault, because wikilinks resolve by name. Pick a distinct name.

### editor_read: see what the user sees

Pass `path`. It returns the note as it is **in the editor**, unsaved edits included:

- `blocks`: `[{id, kind, text}]`, numbered `b1…bn` in document order, with the frontmatter excluded. `kind` is one of `heading`, `paragraph`, `list`, `code`, `quote`, `table`, `rule`, `htmlblock`; `text` is the raw markdown.
- `selection`: `{text, blocks}` when the user has text selected, otherwise absent.

Block ids are **positional**: they are only valid until the note changes. Read again after any change you didn't make yourself, and before every rewrite.

### editor_rewrite: replace or delete a region

Highlights the region briefly, deletes it, and types `content` in its place. Empty `content` deletes the region. Point at the region with exactly one of these:

| Target                      | How                                                                                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `target: "selection"`       | What the user has selected *at the moment of the call*.                                                                                                                      |
| `target: "b3"` or `"b3-b5"` | Whole blocks from `editor_read`. **Requires `expect`**: the region's first few words, copied from `editor_read`. A mismatch fails with "the note changed since it was read". |
| `from_text` (+ `to_text`)   | Exact raw text where the region starts; it must occur **once** in the note. With `to_text`, the region runs through the end of `to_text`.                                    |

- For block targets, `content` is trimmed. Deleting whole blocks also removes the blank line that separated them.

## Results and errors

| You get                              | Do                                                                                                                                                                                                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `interrupted: true`                  | The user typed in the editor, or cancelled the run, and took over. Do not retype the rest. Tell them where you stopped and ask how to proceed. After an interrupted rewrite the region may be half-written, so `editor_read` before anything else. |
| "no editor is open in Hylo"          | Ask the user to open the Hylo app, then retry the same call. Do not write the file another way.                                                                                                                                                    |
| "the editor disconnected…"           | Part of the text may already be in the note. Once the editor is back, `editor_read`, then continue from what is actually there.                                                                                                                    |
| "the note changed since it was read" | `editor_read` again and recompute ids and `expect`.                                                                                                                                                                                                |
| "heading not found"                  | `editor_read` to see the real headings. Then use the exact text, or drop `heading`.                                                                                                                                                                |
| "from_text occurs more than once"    | Quote more surrounding text until it is unique.                                                                                                                                                                                                    |
| "nothing is selected in the editor"  | Ask the user to select the text, or target it by block / `from_text`.                                                                                                                                                                              |
| "the note would start with `---`…" | Your content, or a deletion at the top, would create frontmatter. Start the note with a heading or text instead. |
| "editor switched to another note"    | The user opened something else mid-typing, which counts as an interruption. Ask before resuming.                                                                                                                                                   |

## Workflows

**Write a new note live.**
1. `editor_type` the title and the first section.
2. Type each further section with its own `editor_type` call at `end`.

**Add to an existing section.** Call `editor_type` with `heading: "Section name"`. To add a whole new section, include its heading line in `content` and type at `end` (or under the parent section via `heading`).

**Continue where the user is.** Call `editor_type` with `at: "cursor"`. Call `editor_read` first if you need the surrounding text to continue coherently.

**Revise part of the note.**
1. `editor_read`.
2. Pick the blocks.
3. `editor_rewrite` with `target: "bN"` or `"bN-bM"` and `expect` set to the first words of `bN`.

**Rewrite what the user selected ("improve this", "改这段").**
1. `editor_read` to see `selection.text`.
2. Rewrite with `target: "selection"` right away.
3. If several tool calls separate the read from the rewrite, the selection may have moved. Use `from_text`/`to_text` copied from `selection.text` instead.

**Several edits in one note.**
- Work **from the bottom of the note to the top**, so the ids above each edit stay valid.
- If you can't, `editor_read` again after each rewrite.

**Delete.** Call `editor_rewrite` with empty `content`.

## Best practices

- **One call at a time.** Ops run sequentially in the editor. Wait for each result instead of issuing parallel editor calls.
- **Chunk long writing by section.**
  - At `normal` speed, typing runs at roughly 40–70 characters per second, including natural pauses. A 3,000-character piece takes about a minute.
  - Writing section by section shows progress, keeps an interruption cheap, and avoids tool-call timeouts.
- **Choose a speed.**

  | Speed     | Use for                                                                          |
  | --------- | -------------------------------------------------------------------------------- |
  | `slow`    | Short, showcase writing.                                                         |
  | `normal`  | Everyday writing.                                                                |
  | `fast`    | Long sections.                                                                   |
  | `instant` | Pasting large reference material, tables, or content the user wants immediately. |

- **Typing steals focus.** Every op opens its note in the user's editor and scrolls to follow the caret. Stay on the note the user is working in unless they asked otherwise, and don't hop between notes needlessly.
- **Respect interruptions.** If the user types, they are taking over. Never "finish the job" after an interruption without being asked.
- **Write complete constructs.**
  - Close every code fence.
  - Give tables their separator row.
  - Leave a blank line before `---` meant as a rule. Otherwise it turns the paragraph above into a heading.
  - Everything typed passes through intermediate states. The editor auto-closes a fence as soon as you open it, so fenced content never swallows the rest of the note.
- **Link with care.**
  - Wikilinks resolve by note name, and links to missing notes render as broken.
  - Check a target with `resolve` or `search` before linking, unless you mean to create a placeholder for a note to write later.
- **Read before you rewrite.** The user may have edited since your last look. `editor_read` is cheap; a wrong rewrite is not.

## Frontmatter

The editor tools never read, write or edit frontmatter (the `---` metadata block at the top of a note):

- `editor_read` leaves it out.
- Inserts land below it, and rewrites refuse regions inside it.
- Content that would make a note start with `---` is rejected.

Never put frontmatter or tags in `content`. If the user asks for metadata or tag changes, say that the editor tools don't touch frontmatter, and leave it to them.

## Markdown dialect

Hylo renders GFM plus wiki syntax live as you type. `references/formats.md` covers each format: wikilinks, wiki images, mindmap blocks, tasks, tables, code languages, quotes and what to avoid. Load it when the content uses anything beyond plain paragraphs, headings and lists. Load it **always** before typing a mindmap.
