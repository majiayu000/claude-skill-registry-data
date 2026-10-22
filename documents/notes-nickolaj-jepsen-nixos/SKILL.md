---
name: notes
description: Answer a question from Nickolaj's Obsidian notes vault, read-only. Runs only when invoked as /notes.
disable-model-invocation: true
argument-hint: <question>
---

# Look it up in my notes

The vault is `~/obsidian/notes`: plain markdown with YAML frontmatter. Read its
`AGENTS.md` first for the folder layout and frontmatter schema.

- Read-only: never create, edit, move or delete anything in the vault from here, and
  never run git write commands in it. If the answer suggests a change, say so; I make
  changes from a session inside the vault.
- Search with `rg -i`. Notes are in Danish or English, so try words in both. Narrow by
  folder and frontmatter before reading whole notes.
- If Obsidian is running, `obsidian-cli vault=notes <command>` adds
  `backlinks file=<name>`, `search query=<text>` and `base:query path=Bases/<name>.base`
  (the saved views). Optional; plain files are enough.
- Answer with the note paths you relied on, and say plainly when the notes don't cover it.
