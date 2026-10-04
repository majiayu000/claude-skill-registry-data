---
name: teardown
description: Use when asked to remove the mak-managed rules block from ~/.claude/CLAUDE.md, especially before uninstalling the plugin.
disable-model-invocation: true
---

# mak:teardown — Remove the mak Block from the Global CLAUDE.md

Reverses `mak:setup`: deletes the marker-delimited block from `~/.claude/CLAUDE.md`. Content outside the markers is never touched.

## Procedure

1. **Read `~/.claude/CLAUDE.md`.**
   - If it does not exist, or contains no `<!-- mak:begin` marker: report "nothing to remove" and stop.
2. **Remove the block** — delete everything from the `<!-- mak:begin` marker line through the `<!-- mak:end -->` marker line, inclusive. Collapse any resulting runs of 3+ blank lines to one.
   - If a begin marker exists without an end marker, or **more than one begin/end marker exists** (corrupted/duplicated state): do not guess the block boundary. Show the user the marker locations and ask how far to remove.
3. **If the file is now empty or whitespace-only** — tell the user; offer to delete the file or leave the empty file (their choice). Do not delete it unprompted.
4. **Report** — state that the block was removed. If `~/.claude/CLAUDE.md.mak-backup` exists, mention it: it holds the pre-setup snapshot and can be deleted by the user once they're satisfied, or used to compare (`diff`) if anything looks off. Do not delete the backup automatically.

## Cautions

- Only the marker-delimited block is removed. Never remove legacy (pre-plugin) manually-pasted sections here — that was only offered during `mak:setup` with confirmation.
- Do not run `git` commands; `~/.claude` may not be a repository.
