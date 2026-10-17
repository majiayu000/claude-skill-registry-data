---
name: walkthrough
description: Present a list of items one at a time for focused, interactive review — each with enough context to act on, then wait for the user before advancing. Use when the user wants to step through items one at a time, or hands over findings / tasks / suggestions / a file of items to review interactively rather than as a wall of text.
---

# walkthrough

Move a **cursor** over a list, one item per turn. You present the item under the cursor with enough context to judge it, the user reacts, the cursor advances. The win is focus: the user processes and pushes back on each item instead of drowning in a dump.

The list is **pinned** — built once, held in context for the whole walkthrough. Each turn restates where the cursor is; never assume the user still sees the previous item.

## Steps

1. **Find the items.** In priority order:
   - **A file** the user named (`walk me through subtasks.json`) → read it; treat array entries / list items / top-level sections as the items.
   - **The conversation** — findings, suggestions, tasks, options just produced → enumerate those.
   - **An inline list** in the user's message → parse it directly.

   If it's ambiguous *what* to walk through, ask **once**, then proceed.

2. **Pin the list.** Enumerate the items as a stable, ordered list and hold the full text in context — `back`, `goto N`, and `find` all read from it. Do not re-derive it each turn.

3. **Announce, then present item 1.** One line: `Found N items. I'll go through them one at a time — ready for the first?` Present item 1 in the same turn unless the user's request didn't already imply go.

4. **Present the item under the cursor**, then stop and wait. One item per turn — never advance the cursor twice in one turn.

5. **Act on the response** (see Controls), move the cursor, present the new item with a fresh header.

6. **Finish** when the cursor runs off the end or the user says `done`.

## Controls

Anything unrecognized is `discuss` — the user is reacting to the current item.

| Input | Does |
|---|---|
| `next` / `n` / `ok` / Enter | Cursor → next item |
| `back` / `b` | Cursor → previous item |
| `goto N` | Cursor → item N |
| `find <term>` | Cursor → next item matching `<term>` |
| `discuss` / `d` / *(free text)* | Dig into the current item; cursor stays put |
| `edit` / `e` | Apply the change this item suggests; cursor stays put |
| `skip` / `s` | Record skipped, cursor → next item |
| `list` / `l` | Show the whole list compact (✓ done · ~ skipped · ● current), then return |
| `done` / `q` | End early and summarize |

## Presentation format

```
─── Item 3/7 · [Type] ───

**<title or one-line summary>**

<the detail — enough to understand and judge it on its own>

<suggested action, if the item implies one>

[ next · back · discuss · edit · skip · goto N · find <term> · list · done ]
```

- `[Type]` is whatever the items are — `Finding`, `Task`, `Option`, `Diff`, `Risk`. Drop it if untyped.
- The control hint line is the only menu the user sees — keep it on every item.
- For a file walkthrough, quote the relevant slice (the array element, the section) rather than making the user open the file.

## State to keep

Track across turns; reflect it in the header and wrap-up:

- **Position** — cursor index out of total.
- **Skipped** — items passed with `skip`.
- **Discussed** — items that got a `discuss` turn.
- **Edited** — items where `edit` changed something (note *what* changed).

## Finishing

Close with one line:

```
Walked through N items — X discussed, Y edited, Z skipped.
```

If anything was edited, list those changes as bullets so the user has a record. If items were skipped and the list came from a file, offer to re-run over just the skipped ones.

## Notes

- **`edit` is real work, not a note-to-self.** Actually apply the change (file edit, rewrite, whatever the item implies), confirm it landed, then leave the cursor put so the user advances deliberately.
