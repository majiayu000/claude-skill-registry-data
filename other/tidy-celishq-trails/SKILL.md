---
name: tidy
description: Tidies the celis trails and patterns. Drops stale trails and patterns, names and narrows broad patterns and splits them into smaller ones, merges and settles patterns, promotes strong patterns into the project's own files, narrows a pattern that misled, drops or widens one unused, and draws new patterns from past trails. Use when the person runs /celis:tidy, when celis asks to offer it, or when the person asks to tidy, clean up or prune their trails or patterns.
---

The person wants a small index of patterns that guide, and no musts in celis: a must goes into the
project's own files. Ask what to tidy: this project, this project and the `me` patterns, or all
projects. Do the tidy as one ask titled `Tidy the celis trails`, so that celis knows when the last tidy
was. Start from `celis patterns --tidy`: each pattern that needs tidy, and why. `celis patterns` gives
the index, and `celis grep` gives each pattern with its uses, misled, last use and replaces. A pattern whose grep line names
` cell:<name>` is in that cell, and `celis cells` lists the cells.

A good tidy:

- drops stale trails and patterns: a trail left open and untouched for weeks, a pattern that names a
  place, code or command the project no longer has, or that later work contradicts, and a one-off note;
- gives each pattern the five lines the card shows, in Christopher Alexander's form: a Name for each
  `nameless` one, and the When, Forces, Do and Because on their own lines for each `form` one;
- narrows a pattern that is broad, from the trails that used it: for a `topic` one, the cue that
  showed the choice was due becomes the When, one context and the moment its forces appear; for a
  `tension` one, the two goods that pull against each other become the Forces, each with what it
  protects; a defect, a cost or a risk is not a good. A `many` one, whose Do
  holds several choices, becomes a larger pattern with the general choice, and a smaller pattern
  `--within` it for each other choice;
- offers to promote each `fact` pattern, whose Because gives only the person's choice: it is a fact of
  the project or of the person, not a resolution, so it goes into the project's `AGENTS.md` or
  `CLAUDE.md`, or the person's global `CLAUDE.md` for a `me` pattern. When the trails show a tension
  behind it, offer to rewrite it as a pattern instead;
- narrows the When of a pattern that misled the work, or replaces it, so that it says what the fixes
  showed;
- drops a pattern that is `unused`, or widens its When when the work it names still comes back;
- merges patterns that say the same thing into one that keeps all their examples, and settles patterns
  that say to do different things in the same case, with the drop reason `merged into <id8>` or
  `conflicts with <id8>`;
- promotes each pattern that steps used often, that never misled and
  that was never replaced: a check such as a test, a lint or CI when a tool can hold it, else a line in
  the project's `AGENTS.md` or `CLAUDE.md` for a project pattern, or in the person's global `CLAUDE.md`
  for a `me` pattern. Then it drops the pattern with the reason `promoted to <file>`;
- asks the person what a pattern replaced again and again must say;
- keeps each cell's patterns apart: it merges, settles or narrows patterns only within one cell or only
  outside cells, never changes a pattern of a cell of another account, and promotes a cell's pattern
  only when the person names it;
- offers new patterns for the choices and corrections that came back in two past trails or more and that
  no learn kept.

Show the person each change with the ids it touches, and write nothing, in celis or in a file, before
they agree; they can agree to all of one kind at once. Close the ask with `<n> patterns in the index`,
and tell the person what changed and the size of the index now and at the last tidy.
