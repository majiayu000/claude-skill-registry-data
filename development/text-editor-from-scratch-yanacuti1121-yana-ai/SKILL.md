---
name: text-editor-from-scratch
description: "Use when building a terminal or GUI text editor from first principles — buffer data structures, cursor handling, raw-mode terminal rendering, undo/redo. Not for configuring an existing editor. Triggers on: 'build a text editor', 'implement a text buffer', 'gap buffer vs piece table', 'terminal raw mode editor', 'write my own vim/nano clone', 'undo redo implementation for editor'."
origin: yana-ai — synthesized from public editor-internals write-ups (antirez's kilo, piece-table design notes used by VS Code) and community from-scratch tutorials indexed in codecrafters-io/build-your-own-x
license: Apache-2.0
version: 1.0.0
compatibility: yana-ai >= 0.43.2
---

# /text-editor-from-scratch

## When to Use

- Building a terminal-based text editor (kilo/nano/vim-clone style) from a raw byte stream and terminal escape codes.
- Choosing a buffer data structure (array-of-lines, gap buffer, piece table/rope) for a custom editor or a text-editing widget.
- Implementing undo/redo, cursor movement, or syntax-highlighting hook points for a hand-rolled editor.

## Do NOT use for

- Configuring or scripting an existing editor (Vim, Emacs, VS Code) — that's editor-specific configuration, not building one.
- General terminal UI layout unrelated to text buffers — see whatever TUI framework skill applies to the language in use.
- Rich-text/WYSIWYG web editors — those are a DOM-manipulation problem (contenteditable, ProseMirror-style document models), a different problem from a plain-text buffer.

---

## Buffer Data Structure Decision

```
Small files, simplicity over edit performance?
  → Array of lines (Step 1) — a list of strings, one per line

Large files, mostly append/insert-at-cursor edits?
  → Gap buffer (Step 2) — O(1) insert/delete AT the gap, O(n) to move the gap far

Very large files, edits scattered anywhere, need fast undo history?
  → Piece table / rope (Step 3) — O(log n) edits anywhere, immutable history for free
```

## Step 1: Array of Lines (baseline)

The buffer is just `List<String>`, one entry per line. Insert a character: split the line string at the cursor column, concatenate with the new character in between. Insert a newline: split the current line into two list entries. This is simple to reason about and fine for files up to a few thousand lines — the O(n) string-rebuild cost per keystroke on a long line is where it starts to hurt.

## Step 2: Gap Buffer

A single character array with a "gap" (unused space) sitting at the cursor position:

```
"Hello[    ]world"
       ^^^^ gap — cursor is here
```

Typing inserts into the gap (O(1), no shifting needed as long as the cursor doesn't move). Moving the cursor means sliding the gap: shift characters from one side of the gap to the other until the gap sits at the new cursor position (O(distance moved), not O(file size)). This is the structure classic Emacs uses — cheap for the common case of typing in one spot, more expensive for cursor jumps across a large file (e.g. jumping from line 1 to line 10,000).

## Step 3: Piece Table

Two immutable backing buffers: the **original** file content (never mutated) and an **add** buffer (append-only, every insertion goes here). The visible document is a list of "pieces" — `(buffer, start, length)` tuples referencing spans in either buffer, in document order.

```
original: "Hello world"
add:      "beautiful "
pieces:   [(original, 0, 6), (add, 0, 10), (original, 6, 5)]
          → "Hello " + "beautiful " + "world" = "Hello beautiful world"
```

An edit (insert/delete) only modifies the *pieces list* — splitting or adjusting tuples — never the backing buffers themselves. This gives O(log n) edits regardless of file size or edit location, and — the key win — **undo/redo is nearly free**: since the backing buffers are append-only and pieces are small immutable structs, you can snapshot the pieces list (a cheap shallow copy) before each edit and push it onto an undo stack; redo is just popping back. This is the structure VS Code's text buffer uses.

## Step 4: Terminal Rendering (raw mode)

A terminal editor needs the terminal in **raw mode** — by default, the terminal driver buffers input by line (waits for Enter) and echoes keystrokes itself; raw mode disables both so the program sees every keystroke immediately and controls all rendering.

- Enter raw mode: on POSIX, `tcgetattr`/`tcsetattr` clearing `ICANON` (line buffering) and `ECHO` (auto-echo) flags — **always save the original terminal state and restore it on exit** (including on crash — register an exit handler), or the user's shell is left in a broken raw-mode state after your program exits.
- Render by writing ANSI escape sequences: `\x1b[H` (cursor home), `\x1b[2J` (clear screen), `\x1b[<row>;<col>H` (position cursor), `\x1b[7m`/`\x1b[0m` (inverse video for status line/selection).
- **Redraw efficiently**: don't clear-and-redraw the whole screen every keystroke (visible flicker) — build the next frame in an in-memory string buffer, diff against what's already on screen if you want to go further, and write the whole frame in one syscall.

## Step 5: Cursor & Editing Operations

Track cursor as `(row, col)` logical position, separately from the byte offset into whichever buffer structure you chose (Steps 1-3) — you need the translation function `(row, col) -> buffer offset` for both rendering (where to draw the cursor) and editing (where to apply the next insert/delete).

Handle these edge cases explicitly, they're the most common source of off-by-one bugs:
- Cursor at column 0, pressing Backspace → merge with the previous line (delete the newline between them).
- Cursor at end of line, pressing Delete → merge with the next line.
- Line length differs after vertical movement (Up/Down) → clamp column to the target line's actual length, don't crash on an out-of-range index.

## What NOT to Do

- Don't rebuild the entire buffer as one giant string on every keystroke — this is the #1 performance bug in hand-rolled editors (Step 1's simple approach is fine until files get large; Steps 2-3 exist specifically to avoid this).
- Don't forget to restore terminal state on exit/crash — leaving a user's terminal in raw mode after a crash is a bad, confusing experience (`stty sane` is the manual recovery, but your program should never require it).
- Don't conflate "logical column" with "byte offset" once you support multi-byte UTF-8 or tabs — a tab or a multi-byte character occupies one logical column position but a different number of bytes/display-columns; keep the two concepts distinct from the start rather than retrofitting later.
- Don't implement undo as "save the whole buffer before every edit" for anything beyond the array-of-lines baseline — it works but wastes memory and gets slow; the piece-table approach (Step 3) gets undo essentially for free from the data structure itself.
