---
name: flfl
description: Run /fl on a ticket with moflo's three standing considerations loaded first — cross-platform (Rule #1), consumer blast radius, and dogfooding. Use in the moflo repo itself instead of bare /fl. moflo-internal; never installed into consumer projects.
arguments: "[options] <issue-number | title>"
---

```text
$ARGUMENTS
```

# /flfl — /fl with moflo's standing considerations loaded first

Purpose: run the normal `/fl` ticket workflow, but seat the three things that break moflo changes **before** any research, code, or review happens — not after a reviewer catches them.

These are not a preamble to acknowledge and move past. Hold all three for the **whole** run: research, implementation, tests, `/flo-simplify`, `/verify`, and the PR body.

## The three considerations

| # | Consideration | What it changes about the work you are about to do |
|---|---------------|----------------------------------------------------|
| 1 | **Rule #1 — everything ships cross-platform** | Linux, macOS **and** Windows, identically. Audit every edit for: `path.join`/`path.sep` over hardcoded separators; `fs.realpathSync` on **both** sides of any path comparison; no `Foo.ts` beside `foo.ts`; platform EOL; no `bash`/`grep`/`sed`/`cat`/`find` shell-outs (use Node `fs`/`spawn`); `tasklist` vs `/proc` for process checks; `shell: true` on Windows vs `detached` on POSIX when spawning; `os.tmpdir()` and test ports in 40000–44999. Verify against CI's macOS **and** Ubuntu runs, not just your own OS. |
| 2 | **moflo is installed into a destination project** | This is a library, not an app. Before writing code, name (a) the **consumer surface** touched — `bin/`, `src/cli/`, `.claude/scripts/`, hooks, `init/`, settings/CLAUDE.md generators, anything synced into `node_modules/moflo/`; (b) the **failure mode** for someone already on the current version who upgrades — does their `.moflo/` state still parse, do their hooks still wire, is a migration needed; (c) the **round-trip cost** — does this need publish-then-reinstall to take effect. If you cannot name all three, re-scope before writing code. |
| 3 | **moflo dogfoods itself** | The daemon, hooks, statusline, MCP server and indexer all run from `node_modules/moflo/…`, **not** the source tree. A source edit changes nothing for those layers until publish + reinstall + Claude Code restart. Before diagnosing any "X is broken" symptom, establish **which copy is actually running** — diff `bin/` against `.claude/` against `node_modules/moflo/` first. Expect local flapping: the session-start launcher re-syncs `.claude/helpers/` from the **installed** package, so a local fix to a synced file reverts until published. |

## How to run

1. Restate the three considerations in one line each, mapped to **this specific ticket** — which surface it touches, which platform risks it carries, whether it needs a publish round-trip. Generic restatement is worthless; if a consideration genuinely does not apply, say so and why.
2. Invoke the real workflow with the arguments above, unchanged and in full — including every flag (`-sd`, `-s`, `-w`, `-m`, …):

   ```
   Skill({ skill: "fl", args: "<the $ARGUMENTS block above, verbatim>" })
   ```

3. Follow `/fl` from there. `/flfl` adds nothing to the workflow itself — same phases, same gates, same run-mode resolution. Re-check the three at each gate: they most often fail at `/flo-simplify` (a cross-platform miss) and at the PR body (an unnamed consumer failure mode).

## Anti-patterns

| Don't | Do |
|-------|-----|
| Acknowledge the three, then run `/fl` and never revisit them | Re-check them at implementation, simplify, and PR |
| Restate them verbatim from this file | Map each to the ticket's actual surface and risk |
| Drop or reorder `$ARGUMENTS` when calling `/fl` | Pass the argument string through untouched |
| Verify only on your own OS | Read the macOS and Ubuntu CI runs before claiming green |
| Debug a runtime symptom against the source tree | Confirm which copy is running first |

## See Also

- `.claude/skills/fl/SKILL.md` — the workflow this wraps
- `CLAUDE.md` — Rule #1, Rule #2, and the dogfooding section these three condense
- `.claude/guidance/internal/dogfooding.md` — required reading before diagnosing runtime symptoms or adding files under `bin/`
