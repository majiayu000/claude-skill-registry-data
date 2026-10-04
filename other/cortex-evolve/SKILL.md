---
name: cortex-evolve
description: >
  Save knowledge to the cortex vault. Use when the user says "存到 cortex",
  "記一下", "save to cortex", "記到筆記", "cortex evolve", or when the
  session-suggest hook recommends saving content. Handles Notes and Projects.
---

# Cortex Evolve — Save to Vault

Save content to the cortex Obsidian vault.

## Resolve Vault Path

Read `~/.cortex/config.json` to get `vault_path`.
If the file doesn't exist, tell the user to run `/cortexes:genesis` first.
All file paths below are relative to the vault root.

## Determine Content Type

Ask the user if unclear. Use these heuristics:

| Signal | Type | Target |
|--------|------|--------|
| Technical knowledge, how-to, concept explanation | Notes | `Notes/<category>/<title>.md` |
| Related to a specific repo's design, decision, or progress | Projects | `Projects/<repo-name>/<title>.md` |

## Writing to Notes

1. Determine category from content (C++, Linux, Nginx, Web, or create new)
2. Create file at `Notes/<category>/<title>.md`
3. Use this template:

```markdown
---
title: <title>
tags:
  - <relevant-tags>
created: <YYYY-MM-DD>
source: cortex
---

# <title>

<content>

<optional: related wikilinks like [[nginx-cert-renew]] or [[other-note]]>
```

4. Use Obsidian wikilinks `[[note-name]]` for vault-internal references
5. Use standard markdown links `[text](url)` for external URLs only

## Writing to Projects

1. Determine repo name (from current session context or ask user)
2. If `Projects/<repo-name>/_index.md` doesn't exist, create it:

```markdown
---
title: <repo-name>
repo: <git-remote-url>
tags:
  - project
---

# <repo-name>

<brief description>
```

3. Create topic file at `Projects/<repo-name>/<topic>.md`

## Update _index.md

After writing the file:

1. Read `<vault_path>/_index.md`
2. Append a row under the matching `###` sub-section, creating the sub-section
   (with its table header) if it does not exist yet:
   - Notes → `### <topic>` under `## Notes`: `| [[title]] | tags | one-line summary |`
   - Projects → `### <repo-name>` under `## Projects`: `| [[topic-title]] | tags | summary |`

   Rows are per-page, not per-repo: a new repo means a new `###` sub-section,
   not a single row standing for the whole repo.
3. Bump the `updated` date in frontmatter. There is no `entries:` count to
   maintain — the field was removed by design (see `/cortexes:genesis`).

## Append Log Entry

Compose this entry with all placeholders substituted (today's date/time in `YYYY-MM-DD HH:MM` format, the vault-relative path of the saved file, the repo name or `(none)`):

````markdown
## [YYYY-MM-DD HH:MM] evolve | user-initiated
- outcome: new
- target: <vault-relative path of saved file>
- repo: <repo name or "(none)">
````

Append to `<vault>/log.md` using either the Edit tool (preferred — preserves file integrity) or bash:

````bash
printf '\n%s\n' "$ENTRY" >> "<vault>/log.md"
````

Where `$ENTRY` is the fully-substituted markdown entry.

Preserve exactly one blank line between entries (achieved by the leading `\n` in the printf above, or by ensuring the Edit tool's appended content starts with a blank line).

The `dedup_top1` field is omitted for evolve entries (evolve does not perform a dedup check in Phase 1; the user explicitly chose to save).

## Commit

In the vault repo:
```
git add <file> _index.md log.md
git commit -m "cortex: <type> <brief>"
```

If `git.commit_trailer` in config is a non-empty string, pass it as a second
`-m` so it becomes the last line of the message body:
`git commit -m "cortex: <type> <brief>" -m "<commit_trailer>"`.

If `auto_push` is true in config: `git push`

Confirm to the user what was saved and where.

## Update Vector Store

After committing the new file to the vault:

1. Run: `cortex-vec upsert <relative-path-from-vault>`
