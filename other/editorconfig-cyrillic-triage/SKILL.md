---
name: editorconfig-cyrillic-triage
description: >-
  Use when a reviewer, bot, or editorconfig-checker reports a line over max_line_length while
  Prettier reports the file as formatted, and the line contains Cyrillic or other multi-byte UTF-8
  text — Ukrainian labels, story args, i18n literals. Also when deciding whether to wrap such a line
  or to reply that the count is bytes rather than columns.
---

# editorconfig Cyrillic triage

## Profile keys consumed

- `make.format`
- `make.lint_eslint`

## Overview

`editorconfig-checker` measures a line in UTF-8 **bytes**; Prettier's `printWidth` and ESLint's
`max-len` measure **characters**. Cyrillic encodes as two bytes per character, so a line that is
comfortably inside the column limit can be reported as over it. Decide which count applies before
touching the line — a hand-wrap that Prettier disagrees with is reverted by the next format run and
turns a false positive into a real formatting failure.

## When to use

- A finding cites a line length that does not match what the editor shows.
- The flagged line holds a Ukrainian or Russian string literal, label, or story argument.
- You are about to wrap a JSX line to satisfy a length complaint.
- Not for: lines that are genuinely over the column limit, and not for non-text overruns such as
  long imports or URLs, which are wrapped normally.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — `.editorconfig` sets `max_line_length = 100` and `.prettierrc` sets
  `printWidth: 100`, but `.qlty/qlty.toml` registers no `editorconfig-checker`; the enforced
  character-count gates are the repository's check-only Prettier target and ESLint `max-len` at
  100, run through the target mapped by `make.lint_eslint`.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — `.qlty/qlty.toml` runs
  `editorconfig-checker` with `mode = "comment"`; `.editorconfig` is 100 and `.prettierrc`
  `printWidth` is 100. The target mapped by `make.format` is the Prettier pass.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — same qlty
  `mode = "comment"` setup, 100/100 limits, plus ESLint `max-len` at 100; its check-only formatter
  target runs `prettier . --check`.

## Procedure

1. **Measure both counts** for the flagged line.

   ```bash
   sed -n '<line>p' <file> | python3 -c "import sys
   raw = sys.stdin.buffer.read().rstrip(b'\n')
   print('chars', len(raw.decode()), 'bytes', len(raw))"
   ```

   Do not reach for `awk '{print length}'`: its `length` returns characters under a UTF-8 locale and
   bytes under a C locale, so it silently answers whichever question the environment happens to ask.
   Read the byte count from the raw bytes and the character count from the decoded string.

2. **Read the two limits from the repo**, never from memory.

   ```bash
   grep max_line_length .editorconfig
   grep printWidth .prettierrc
   ```

3. **Confirm the difference is the encoding.** If `bytes - chars` equals the number of Cyrillic
   characters on the line, the overrun is byte inflation, not width.

4. **Ask Prettier who owns the line.** Run the repository's check-only formatter target. Where no
   check-only target exists, run the target mapped by `make.format` (skip with a recorded note when
   it maps to `null`) and confirm it leaves the line untouched. If Prettier reports the file as
   formatted, it keeps the line single-line by choice and any manual wrap is undone on the next
   format run.

   ```bash # profile-example
   make lint-prettier    # a React SPA whose check-only Prettier target is `lint-prettier`
   make format-check     # a component library whose check-only Prettier target is `format-check`
   make format           # no check-only target: run the formatter and confirm no diff
   ```

5. **Classify and act.** Characters within `printWidth` while bytes exceed `max_line_length` is a
   byte-count artefact: reply with both numbers and leave the line. Characters over `printWidth` is
   a real overrun: restructure the line and re-run the gate.

6. **Check the mode before skipping.** `mode = "comment"` in `.qlty/qlty.toml` means the checker is
   advisory and the character-count gates decide. If the checker is ever wired as a blocking gate,
   the fix is to shorten the line for real — extract the literal to a named constant or an i18n key
   — not to relax the limit.

## Reply shape

State both numbers, name the encoding, name the owner: the line is N characters (within the
configured `printWidth`) and M UTF-8 bytes because each Cyrillic character encodes as two; Prettier
counts columns, reports the file formatted, and would revert a manual wrap.

## Common mistakes

- Wrapping the line to silence the finding, then failing the formatting gate on the next run.
- Quoting only the byte number in a reply, which reads as an admission that the line is too long.
- Assuming the checker is advisory — read the mode from the qlty config in the repo at hand.
- Extending the diagnosis to a line whose character count really is over the limit; extract the long
  literal instead.
