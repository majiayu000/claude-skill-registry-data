---
name: crew-tune
description: Adjust TriMixxx's agent crew (minion, bitch, nightman, and the crew tool) while it is in use - Sam says what went wrong or what he wants done differently; find what actually happened, change it at the right layer (a limit, a role's instructions, the tool and its guard), test it, and get the change to the sessions already running. Use when Sam wants to fix, tune or change how the crew works, or works through `.crew/feedback.md`.
argument-hint: "[what went wrong, or what to change]"
---

# Tuning the crew

Sam is using the crew (`.claude/crew/README.md`) and wants it to behave
differently: `$ARGUMENTS`. If that is empty, work through the crew's own
complaints in `.crew/feedback.md` with him.

Work from the main checkout, the crew's home: `crew root` prints it. Every
copy of `crew` runs the main checkout's, and new worktrees branch from main,
so that is where a fix takes effect.

## 1. Find out what actually happened

Before changing anything, look at the evidence:

- `crew status`: the branches, their sessions, PRs, review states, decks,
  and the load.
- `.crew/feedback.md`: crew sessions log there where the rules or tools got
  in their way.
- The nightman's `.crew/night/plan.md` (its log), `.crew/night/report-*.md`,
  and a branch's `.crew/notes.md` (or `.crew/archive/BRANCH-DATE/` once
  cleaned).
- The PR and its reviews: `crew pr BRANCH`, then
  `crew gh -R usr-ein/TriMixxx pr view N --comments`.
- A session's own transcript:
  1. Find its id in `.crew/sessions/*.json` (or with `claude agents --json`).
  2. Read `~/.claude/projects/DIR/ID.jsonl`, where DIR is the session's
     starting directory with `/` and `.` turned into `-` (e.g.
     `-Users-sam1902-Documents-CustomDJ--claude-worktrees-BRANCH`).
  3. Grep it for the moment in question; never read it whole.

Tell Sam in a few lines what happened and why, before proposing the change.
A one-off (a minion that misread its pitch) is fixed in that session, by
message, not in the system.

## 2. Change it at the right layer

Prefer the smallest change at the lowest layer: a number before a rule, a
rule before code.

| What's wrong | Layer | File |
|---|---|---|
| too many or too few minions, decks; load, disk, review rounds, drift-check cadence | numbers | `.claude/crew/limits.env` |
| a role asks too much or too little, decides what it shouldn't, reports badly, reviews the wrong things | the role's instructions | `.claude/skills/{minion,bitch,nightman}/SKILL.md` |
| a guard refusal that is wrong (or a hole in it), the drift check's wording, names, launching, merge or clean | the tool | `.claude/crew/crew`, with a test in `.claude/crew/test_crew.py` |
| which hooks run, and when | wiring | `.claude/settings.json` |
| how the whole thing works, for Sam | the overview | `.claude/crew/README.md` |

Keep the roles consistent: most rules have a mirror in another role. What a
minion reports is what the nightman expects; what the bitch judges is what
the minion writes in its PR; a limit a minion obeys is one the nightman
enforces. Update the README when behaviour changes, and keep the skills'
style (short sentences, concrete commands).

## 3. Test it

- Change a copy of the tool, never `.claude/crew/crew` itself: every crew
  session's hooks run that file on each tool call, so a half-edited one
  breaks the guard while it lasts. Copy `crew`, `test_crew.py` and
  `limits.env` to your scratchpad, and change and test them there
  (`python3 -m unittest discover -s DIR`).
- `python3 -m unittest discover -s .claude/crew -v`. A change to the guard,
  merge, clean or launching gets a test of its own.
- To try the tool from a worktree before it lands, prefix `CREW_LOCAL=1`:
  otherwise the main checkout's copy runs.
- Show Sam the change (a short diff or summary) and what the test showed.

## 4. Land it, on Sam's OK

Swap the tool in with one rename (`cp` it beside the live one, then `mv`),
and rerun the tests in place. Commit in the main checkout, on main, with
explicit paths:
`git -c user.name="Samuel Prevost" -c user.email=usr_ein@pm.me commit ...`.
Tuning the crew is tooling, not deck code: it lands on main directly so it
takes effect at once. Push only when Sam says, and never while a repo's main
holds commits he hasn't pushed himself.

## 5. Reach the sessions already running

- **The tool, the guard, the drift check, the limits:** at once. Every copy
  of `crew` runs the main checkout's.
- **A role's instructions:** a session keeps the text it loaded. SendMessage
  each live crew session concerned (`crew status`, `claude agents`): "Crew
  update: <what changed, in a line>. Re-read <main
  checkout>/.claude/skills/<role>/SKILL.md." A nightman passes it on to its
  minions if you ask it to.
- **`.crew/feedback.md`:** move the lines you handled under a `## Handled`
  heading at its end, with the commit.

## Never

- weaken a safety rule (the guard, the merge's refusals, a real deck only on
  Sam's go and under its lock, no AskUserQuestion at night) without Sam
  saying so explicitly
- change a role's instructions without its mirrors and the README
- rewrite history, or push, without Sam's word
