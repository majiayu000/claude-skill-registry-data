---
name: review-comments
description: >
  Process code review comments left in `.review/comments.json` by the
  Neovim review plugin. Triggered when the user says "process my
  review comments", "address review comments", "/review-comments", or any time
  the repo contains a `.review/comments.json` with unresolved entries.
---

# Review

The user reviews agent-produced code in Neovim (a small plugin, Diffview optional) and saves their inline comments to `<repo>/.review/comments.json`. Each entry has `file`, `side` (`new` or `old`), `line`, `code` (the line's text at comment time), `body`, and `resolved`. Your job here is to go through the unresolved ones.

## Your job

Read `<repo>/.review/comments.json` and walk through every entry where `resolved` is `false`.

For each unresolved comment, use your judgment:

- If the comment is clearly asking for a specific fix, implement it.
- If the comment is a question, suggestion, or feels ambiguous, discuss it with the user first before making any changes.
- If you disagree with a comment or see a better approach, say so and explain why.
- If a comment is now obsolete (the code already changed, the file moved, etc.), remove it from the JSON array.
- After you address a comment — by fixing it or by resolving the discussion — set its `resolved` field to `true` in the JSON file.
- Preserve `file`, `side`, `line`, and other metadata for any comments that remain unresolved.

Start by summarizing your read of each comment — whether you plan to fix it, discuss it, or think it's obsolete — and then proceed accordingly.

## Notes

- Side `new` means a line in the working tree; `old` means a line in the base revision.
- **Line drift on `side: "new"`:** comments left in a plain buffer (not Diffview) anchor to the line number at save time. If the user edited afterwards, `line` may no longer point at the right spot. Before treating a comment as obsolete, compare `code` to the current text at `file:line` — if they don't match, search a few lines above and below for the matching `code` and use that location instead. Only if `code` is nowhere nearby should you consider the comment obsolete.
- The repo's `.review/` directory is git-ignored via `.git/info/exclude`, so JSON edits don't show up in `git status`.
- If `.review/comments.json` doesn't exist, tell the user there's nothing to review — they probably haven't run `:ReviewStart` in Neovim yet, or haven't left any comments.
