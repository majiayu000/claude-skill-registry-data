---
name: memory-import
description: "Inherit memories from another workspace. Reads .claude/memory/ from a source path and imports its memories into the current workspace under .claude/memory/inherited/<source-name>/. Tagged with provenance so the user can tell where each came from."
argument-hint: "<path-to-other-workspace>"
---

# /memory-import

Pull memories from another workspace into the current one. Useful when the user has built a previous app and wants its accumulated context — conventions, gotchas, references — to inform a new project.

## When to use

- Starting a new project that's similar to one the user already built.
- Doing a code review on a project where the user wants you to reference patterns from another of their projects.
- Onboarding to a new repo where the team's conventions are already documented in another workspace.

## Operating method

1. **Validate the source path.** Check that `<path>/.claude/memory/MEMORY.md` exists. If not, tell the user the source workspace doesn't have a memory layer (it may not have been initialized with this toolkit).

2. **Read the source's memory index** and the files it references.

3. **Categorize what to import.** For each memory:
   - **Always copy** `project/` and `reference/` (with provenance tag) — they're the most likely to inform the new project.
   - **Ask before copying** `feedback/` — preferences from another project may not transfer ("no Tailwind in app A" doesn't mean "no Tailwind in app B"). Show the user the list and let them check/uncheck.
   - **Ask before copying** `user/` — usually applies (it's about the user, not the project), but the user should confirm.
   - **Skip** `handoffs/` — those are session-specific to the source workspace.
   - **Skip** `inherited/` — don't transitively chain inherits. If the user wants those too, they can re-import from the original source.

4. **Show a preview.** List the memories you intend to import, grouped by type. Ask: "Import these <N>?"

5. **Copy with provenance.** Each imported memory gets:
   - Filename prefixed with the source workspace name: `inherited/<source>-<original-filename>.md`.
   - Frontmatter `source-workspace: <path>` added.
   - A header line in the body: `> Imported from <source> on <date>. Treat as suggestive, not authoritative for the current project.`

6. **Update the index.** Add lines to `.claude/memory/MEMORY.md` under "Inherited (from other workspaces)."

7. **Print a summary.** "Imported N project facts, M references, K user notes from <source>."

## Behavior on conflicts

If a target file already exists:
- For an exact-name collision (rare since we prefix with source), append `-2`, `-3`, etc.
- If a similar memory (similar topic) already exists, ask the user: "Your current project already has a memory `<name>`. The inherited one says <X>. Keep both, replace, or skip?"

## What "suggestive, not authoritative" means

When an agent later relies on an inherited memory, it must:
- Cite the source workspace.
- Frame the suggestion as a pattern to consider, not a fact about the current project.
- Verify by reading current code before applying.

Example:
- Bad: "We use Postgres + Drizzle here."
- Good: "Your `app-foo` project (inherited memory) used Postgres + Drizzle. Want me to set up the same here, or is this project different?"

## Output format

```
## Source: <path>
- Found memory layer: yes
- Memories available: 4 project, 2 user, 1 feedback, 3 reference, 6 handoffs

## Plan
- Auto-import (project + reference): 4 + 3 = 7 files
- Confirm-import (user + feedback): showing 3 to review
- Skipped: handoffs (6), inherited (0)

## Confirm imports

[ ] user/role.md — "senior eng, platform team"
[ ] user/preferences.md — "terse, no emojis, vitest"
[ ] feedback/no-mocks.md — "integration tests hit real DB"

(answer with the indices to import, or "all" / "none")
```

After confirmation: write files, update index, print summary.

## Safety

- Never import secrets even if they appear in source memory (filter for patterns: `*_KEY`, `*_TOKEN`, `Bearer `, `sk_live_`, etc.). Replace with `[REDACTED — was a secret in source]`.
- Never modify the source workspace.
- Show the user every file before writing.
