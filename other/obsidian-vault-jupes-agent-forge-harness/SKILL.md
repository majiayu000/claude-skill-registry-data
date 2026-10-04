---
name: obsidian-vault
description: Search, create, and manage notes in an explicit Obsidian vault with title-case filenames, wikilinks, index notes, backlinks, and safe vault-root confirmation.
---

# obsidian-vault

Use this skill when the user wants to find, create, update, or organize notes in an Obsidian vault.

## Safety First

- Do not assume a universal vault location. The upstream private path is not a default and must not be reused unless the user explicitly provides it for their own environment.
- Resolve the vault root before reading or writing notes. Accept one of:
  - A vault path provided directly by the user.
  - A documented repo setting or project config that clearly names the vault root.
  - An environment variable such as `OBSIDIAN_VAULT_ROOT`, after confirming it points to the intended vault.
- Before creating or editing notes outside the current repository, state the resolved vault root and ask the user for explicit confirmation.
- Do not modify an actual vault while porting or testing this skill unless the user has requested a vault operation and confirmed the root.

## Vault Conventions

- Prefer a mostly flat note layout at the vault root unless the existing vault has a clear folder convention.
- Use Title Case filenames, for example `Retrieval Augmented Generation.md`.
- Name index notes as `<Topic> Index.md`, for example `Skills Index.md` or `RAG Index.md`.
- Use Obsidian wikilinks: `[[Note Title]]`.
- Put related-note wikilinks near the bottom of a note under a short heading such as `## Related`.
- Keep index notes as concise lists of wikilinks.

## Search Workflow

1. Resolve and confirm the vault root if it is outside the repository.
2. Use `Glob` to list markdown notes under the vault root, for example `**/*.md`.
3. Use `rg` for content searches scoped to the vault root.
4. Use `ReadFile` to inspect candidate notes before proposing edits.
5. Avoid shell `find` and `grep`; use Cursor-native `Glob`, `rg`, and `ReadFile` unless the user explicitly asks for shell commands.

Common searches:

- Filename search: use `Glob` for `**/*Keyword*.md`, and adjust for title-case variants.
- Content search: use `rg` for the keyword or phrase scoped to the vault root.
- Wikilink search: use `rg` for `\[\[Note Title\]\]` scoped to the vault root.
- Index discovery: use `Glob` for `**/*Index*.md` and `rg` for links from likely index notes.

## Create A Note

1. Confirm the vault root and whether writes outside the repository are allowed for this operation.
2. Convert the note title to a Title Case filename ending in `.md`.
3. Check for existing notes with the same or similar filename using `Glob`.
4. Search for related notes and indexes using `rg` and `Glob`.
5. Draft the note as a focused unit of learning.
6. Add relevant `[[wikilinks]]` near the bottom.
7. Add the new note to the best matching `<Topic> Index.md` when an index exists.
8. If no suitable index exists, ask before creating a new index note.

## Manage Existing Notes

- Read the target note and nearby index notes before editing.
- Preserve existing frontmatter, headings, and wikilink style.
- When renaming a note, update backlinks by searching for the old wikilink and replacing it only after the user confirms the rename.
- When adding a relationship, update both the note and the relevant index note when that keeps the vault easier to navigate.
- For numbered sequences, follow the vault's existing numbering scheme instead of inventing a new one.

## Backlinks And Indexes

- To find backlinks, search for the exact wikilink form: `[[Note Title]]`.
- To discover indexes, search filenames for `Index` and inspect likely matches.
- Index notes should stay lightweight: a heading plus a list of `[[wikilinks]]` is usually enough.
- Prefer connecting notes through wikilinks and index notes over creating new folders.
