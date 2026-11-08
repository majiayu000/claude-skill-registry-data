---
name: ponytail
description: "Use for the smallest complete change (ponytail, minder code, kleinste diff)."
# W2-BUDGET original description (listing budget): "Use when building or fixing with the smallest complete change (ponytail, minder code, kleinste diff, write less code, lazy senior dev): lite/full/ultra. Never cuts validation or security."
---

# Ponytail — the smallest change that fully solves it

**Self-improvement substrate:** before applying this skill, read `learnings.md` in this skill's own
folder and honor its corrections. After a run that produced a genuine correction, append it there with
a date and real evidence — never invent a lesson that did not happen.

Work like the senior developer who has seen every over-built feature: the best code is code never
written. Solve the **whole** problem with the **least new code**. Lazy about the solution, never about
reading, finishing or checking.

**On and off.** On when the owner asks for it ("ponytail", "minder code", "kleinste diff", "write less
code"); it stays on for the session until "stop ponytail", "normale modus" or "normal mode". Level
switch: "ponytail lite", "ponytail full" (default) or "ponytail ultra". Build Boss may also apply the
ladder as a lens on any package; it never overrides the work package or the Forge rules below.

## Where this skill stops (siblings)
| Question | Skill |
|---|---|
| Review a diff (order, severity, blocking) | `forge-code-review` — ponytail adds only the lean lens (`references/lean-review.md`) |
| Clean up after a finished diff | `simplify` / `refactor-clean` |
| Short answers in chat (fewer output tokens) | `forge-token-economy` terse mode |
| Tests first for new behaviour | `test-driven-development` / `forge-testing` |

Extra moves while writing (existence reason, understand first, fix the shared root): `references/minimal-code-discipline.md`.

## Before you write
Read the task and the code it touches. List every place the change must reach: callers, tests,
fixtures, config, exports, docs that state the behaviour. Check what the change could break: data it
could destroy or expose, callers that stop working. That list is the scope. Extra features are not.

## The ladder — take the first rung that fully works
1. **Does it need to exist?** Skip features, options and flexibility nobody asked for; name them in one
   line. A vague ask ("bouw me X") gets the smallest version that does the core job.
2. **Already in this codebase?** A helper, component, service or pattern: use it the way the
   surrounding code does. Grep before you write.
3. **Standard library or platform feature?** Use it, unless the project has its own (a house component
   beats a native widget). On Windows + Node: `node:fs`, `node:path`, `node:test` before a package.
4. **An installed dependency?** Use it. Never add a dependency for a few lines.
5. **One line a reader understands at a glance?** One line.
6. **Otherwise:** the minimum code that works.

## Rules while building
- Finish every part the task needs, including the callers, tests and fixtures your change breaks.
- No abstraction, wrapper, option, config, boilerplate or "for later" code nobody asked for. Keep values
  in the form the platform already gives. Deletion beats addition.
- Keep the structure the codebase already has: its layers, interfaces and conventions.
- The shortest working diff wins **once you know everything it must touch**. A one-liner that needs
  decoding is not short.
- Comment only the why the code cannot show, in one line.
- **Bug fix:** grep every caller of the function you touch, then fix the root cause once in the shared
  code (see `forge-debug`: root cause first, regression test RED then GREEN).
- Code you move or merge keeps its error handling and validation.
- Between two options of equal size, take the one that is correct on edge cases.
- A shortcut with a known limit gets a comment: `shortcut: <the limit>, <when to upgrade>`.
- **Tests:** new non-trivial logic (a branch, a loop, a parser, money, security, a new script) leaves at
  least one small real test that fails when it breaks. Where Forge's testing rules ask for more (TDD for
  new behaviour, a regression test for every bug fix), Forge's rule wins. Lean never means untested.

## Never cut
Validation at trust boundaries · error handling that prevents data loss or a silent failure ·
security (auth, secrets, injection, path checks) · accessibility (labels, focus states, contrast,
keyboard use) · the calibration real hardware needs · anything the owner or the work package asked for.
If cutting one of these looks tempting, the change is not finished yet.

## Levels
| Level | Behaviour |
|---|---|
| **lite** | Build what was asked. Name the smaller option in one line and let the owner pick. |
| **full** | The ladder and rules above. Default. |
| **ultra** | Also question the ask before building: push back on any part the need does not justify, in one short list. Never drop a part on your own; the owner decides. |

## End of every reply
One or two plain lines: what you skipped or did not check, and any risk the owner must know. This is
the honesty line, not a summary: it may say "none".

## Forge fit
- The work package and Head Chef's scope stay the boundary; ponytail makes the diff smaller inside it,
  it never shrinks the scope.
- GOAT routing, the verifier gate, the Stop test gate and the hard gates are unchanged.
- Ponytail is about code size. It does not make reports, QA verdicts or copy-paste prompts shorter.

## Provenance
- **DietrichGebert/ponytail** — paths `.openclaw/skills/ponytail/SKILL.md` and
  `.openclaw/skills/ponytail-review/SKILL.md`, `README.md` (doctrine only); pinned SHA
  `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`; MIT License, Copyright (c) 2026 DietrichGebert. Taken
  (rewritten for Forge Bosses, Windows + Node and GOAT): the "write less code, never cut validation, error
  handling, security or accessibility" doctrine, the ladder, the build rules, the shortcut comment, the
  end-of-reply risk line, the lite/full/ultra levels, and the lean review categories (in
  `references/lean-review.md`). Excluded: all Node hooks and plugins (`.opencode/plugins/*`, frontmatter
  hook), every command `.toml` and per-tool rules copy (`commands/`, `.cursor`, `.windsurf`, `.kiro`, …),
  the "band" status bar and "board" local page (they write under the user's home folder), the audit, debt,
  gain and help skills, install steps, and the README benchmark numbers (not measured here).
The MIT notice above applies to the adapted portions; the full MIT text is at the source repository.
Verified 2026-11-05: the three paths above and the root `LICENSE` ("Copyright (c) 2026 DietrichGebert")
were fetched read-only at the pinned SHA from raw.githubusercontent.com (HTTP 200; the GitHub API was
unreachable); no `NOTICE` file exists at that SHA. Hidden-Unicode scan of the fetched text: clean.
