---
description: Set up chamnan in this repository for the first time — build the architecture index, measure how well the code describes itself, fill in missing file comments, and record a baseline. Run once per repo.
---

# Set up chamnan here

Do these in order. Report the numbers as you go; the user should see what changed, not just "done".

## 1. Build the index

```
chamnan-map
```

Read what it printed. The important line is the **described** percentage.

## 2. If coverage is under 70%, offer to fix it — do not just report it

**First read `agents` from `.chamnan/config.json` (default `true`).** With `false` the user
has switched off chamnan dispatching agents of its own: report the coverage, list the files
from `chamnan-map --undocumented`, and stop there — do not offer the commenter, do not
dispatch it, and do not write the comments yourself instead. `chamnan-map` already honours
the switch where it prints this same advice; a skill that dispatches anyway is what makes the
setting mean nothing.

A low number is not a complaint about the user, it is the single biggest lever on whether any of
this works. The index is built from each file's opening comment; without them it degrades to a list
of filenames, which is worth little.

Say plainly what the number means and what you can do about it, then — **with the user's go-ahead** —
dispatch the `chamnan:commenter` agent over the files that lack one (the plugin-scoped name, so a second installed plugin that also ships a `commenter` cannot be picked instead). That agent runs on a cheap model
because "read this file, write one line about it" does not need an expensive one; this is the
routing principle the plugin ships with, applied to its own onboarding.

Give the agent the specific file list, not the whole repo, **and tell it which language to write
in** — read `language` from `.chamnan/config.json` (default `en`). The agent writes English unless
you name something else, so this has to be passed explicitly.

**Get that list from `chamnan-map --undocumented`, which prints every one of them, one path per
line.** The names the rebuild itself prints are capped at eight and labelled "for example" — acting
on those alone fixes eight files and reports a before/after as though the gap were handled. On a
repository with forty undocumented files that leaves 80% of them untouched and unmentioned.

Mention to the user that the setting exists and that changing it is one sentence: "use Thai for the
comments" is enough, and you edit `.chamnan/config.json` for them. English costs fewer tokens on
every session, but that is a default worth overriding for a team that will not read English
comments — say the trade-off once and let them choose.

Then run `chamnan-map` again and show the before/after coverage.

Never edit files for this without asking first. It touches every undocumented file in the repo.

## 3. Record where things stand

```
chamnan-report
```

On a repo with history this prints a weekly trend and marks today. On a fresh one it will say there
is not enough history yet — that is correct, not a failure. Say so rather than hiding it.

## 4. Write the first STATE.md

Create `.chamnan/STATE.md` with what the user is actually working on right now. Keep it short —
this file is injected into every future session, so it is paid for repeatedly.

**Write it at milestones only**: a test suite passing, a commit landing, a decision being made, or
the session ending. Not after every edit. A state file rewritten every few turns costs output
tokens continuously and buries the one line that mattered in a history of near-identical versions.

## 5. Offer to keep it fresh

```
chamnan-map --install-git-hook
```

Offer this, do not run it unprompted — it writes into `.git/hooks/`, which is the user's. It appends
to an existing hook rather than replacing it, and never fails a commit. Explain the reason rather
than the mechanism: an index that drifts out of step with the code is worse than none, because the
next session trusts it and opens the wrong file.

## 6. Tell the user what they got, honestly

- how many tokens the index is versus the source it indexes
- that the full detail is grepped, never read whole
- that the effect compounds: this repo gets cheaper to work in the more it is revisited, and gives
  back nothing on a repo touched once
