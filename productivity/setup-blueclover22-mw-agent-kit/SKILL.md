---
name: setup
description: Use when asked to install or update the mak common rules in ~/.claude/CLAUDE.md, optionally in Korean (ko) or English (en).
disable-model-invocation: true
---

# mak:setup — Install Common Rules into the Global CLAUDE.md

Injects the rules snippet into `~/.claude/CLAUDE.md` as a marker-delimited block:

```
<!-- mak:begin — ... -->
...rules...
<!-- mak:end -->
```

Everything between (and including) the markers is owned by mak. The user's own content outside the markers is never touched. Removal is done by `mak:teardown`.

## Procedure

1. **Pick the language and read the snippet** — two variants exist:
   - `${CLAUDE_PLUGIN_ROOT}/skills/setup/assets/claude-md-snippet.ko.md` (Korean)
   - `${CLAUDE_PLUGIN_ROOT}/skills/setup/assets/claude-md-snippet.en.md` (English)

   Selection order: an explicit skill argument (`ko` / `en`) wins; otherwise match the user's conversation language (Korean conversation → ko, anything else → en); if genuinely ambiguous, ask the user. The chosen file (markers included) is the exact block to install.
2. **Read `~/.claude/CLAUDE.md`.**
   - If it does not exist: create it with the snippet as its entire content. Report and stop.
3. **Back up once** — if `~/.claude/CLAUDE.md.mak-backup` does not exist, copy the current `~/.claude/CLAUDE.md` to it before any modification. If the backup already exists, leave it (it preserves the pre-mak state).
4. **If markers already exist** (`<!-- mak:begin` and `<!-- mak:end -->` both present): first count them — **if more than one begin or end marker exists (corrupted/duplicated state), do not modify anything**; show the user the marker locations and ask how to reconcile. With exactly one pair, replace everything from the begin marker line through the end marker line with the new snippet. This is also how the block's language is switched — the whole block is replaced with the chosen variant. Report "updated existing block" (and the language, if it changed) and stop.
5. **If no markers, check for legacy content** — earlier versions of this kit were installed by manually pasting sections into `~/.claude/CLAUDE.md`. Look outside any markers for:
   - An `## Agents` / `## Skills` catalog listing planner/coder/reviewer/doc-editor or the pre-plugin kit's 7 skills (legacy counts — today's kit ships more of both), and a `## Workflow` section matching the kit's task grades: these are superseded by the plugin and this block. **Do not delete anything silently** — show the user what overlaps and propose removing the duplicates before appending the block. Only proceed after confirmation.
   - **Everything else outside the markers is the user's own content — leave it untouched regardless of its headings**; just note what exists. This includes personal rule sections this kit's old manual seed used to ship (e.g. `## Rules` / `## Coding Rules` / `## File Handling`) as well as any user-authored sections under any name. Where the user's own coding rules overlap the block's principle mapping, the user's rules take precedence on conflict.
6. **Otherwise** — append the snippet to the end of the file, separated by one blank line.
7. **Report** — state what was done (created / block updated / appended / merged after confirmation), the backup path, and remind: "Run `/mak:teardown` before uninstalling the plugin to restore CLAUDE.md."

## Cautions

- Never modify content outside the marker block without explicit user confirmation (step 5 is the only case, and it requires confirmation).
- Do not run `git` commands; `~/.claude` may not be a repository.
- Install exactly one of the two bundled snippets — never translate on the fly or mix languages. The ko/en variants are maintained as mirrors in the plugin repository.
