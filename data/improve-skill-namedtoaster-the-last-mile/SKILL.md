---
name: improve-skill
description: Fix a Last Mile skill that did the wrong thing, from inside the project where it went wrong. Decides whether the lesson belongs in the project's rules file or in the skill, makes the smallest change to the skill in The Last Mile repo (never the synced copy), keeps every project detail out because the repo is public, runs the checks and opens a pull request. Also adds a store or build trap other apps would hit to the ship skill's traps, through a fork when the user cannot push. Use when the user says a skill misfired, "improve the skill", "fix session-end", "that skill should have done X", or when session end lists a skill problem.
---

# Improve skill

The skills get better from real use. This turns one thing that went wrong into
one small, general fix in The Last Mile, without leaking the project it happened in.

## 0. What went wrong

Write it in three lines, from the conversation:

- **Skill:** which one.
- **What it did:** the step and the result.
- **What it should have done.**

If the conversation does not make this clear, ask one question, then wait.

## 1. Decide where the fix belongs

| The lesson is... | Fix it in |
| --- | --- |
| About this project only: a command, a file, a service, an app rule | The project's rules file (`CLAUDE.md` or `AGENTS.md`): the Settings table, Gotchas or Standing decisions. Stop there. |
| About a skill listed in `keepLocal` in `.claude/last-mile/config.json` | That skill in `.claude/skills/<name>/`, which is the project's own version. Then ask whether the general version needs the same lesson; if yes, carry on below. |
| True for any app using the skill | The Last Mile, below. |
| A store rejection or build trap other apps would hit, not yet in `skills/ship/references/traps.md` | A new trap in that file, below. |

Most misfires are a missing project setting, not a broken skill. Check that first.

## 2. Reach The Last Mile

The source repo is `source` in `.claude/last-mile/config.json`
[`namedtoaster/the-last-mile`].

- **A local clone exists:** work there, on a new branch from an up to date `main`.
- **Cloud session:** add the repo to the session with push access (for example an
  add repository tool), clone it into its own folder, and branch from `main`.
- **The user cannot push to it** (most people): fork it with
  `gh repo fork namedtoaster/the-last-mile --clone`, branch in the fork, and open the
  pull request from the fork in step 4. Without `gh`, open an issue instead: the
  "This caught me" form for a trap, the skill problem template for a skill.

Name the branch `improve/<skill>-<few-words>`.

## 3. Make the smallest change

Edit `skills/<skill>/SKILL.md`, or the reference file the step points to. For a
trap, add one entry to `skills/ship/references/traps.md` under the right heading, in
the shape `CONTRIBUTING.md` gives (What happened, Rule, How to check, Source, Status).
Mark it **From experience** unless you opened the official page this session.

- Change the step that went wrong. Do not rewrite the skill around it.
- Word it for any app. Swap this project's names for a plain example.
- **Nothing from the project goes in:** no app name, screen names, copy, user data,
  keys, URLs, device ids or analytics. The repo is public. If the lesson cannot be
  told without them, it belongs in the rules file (step 1).
- Date anything that can go stale. Follow `CONTRIBUTING.md`: plain words, no long
  dashes (em or en).
- Add one line under the unreleased heading in `CHANGELOG.md`.

## 4. Check and open the pull request

1. Run `node scripts/validate.mjs`. Fix what fails until it passes.
2. Commit only the files you changed, push the branch and open a pull request
   that follows `.github/pull_request_template.md`. Say what went wrong in general
   terms and what the change does.

## 5. Finish

- **Never edit the synced copy** in the project's `.claude/skills/<skill>/`. The
  next sync overwrites it. For the rest of this session, follow the fixed step by
  hand.
- Tell the user, in a few lines: what went wrong, where the fix went, and the pull
  request link. Once it is merged, the project picks it up on the next sync: the
  "Sync The Last Mile skills" workflow (daily, or Run workflow from the Actions
  tab), or `node .claude/last-mile/sync.mjs` and a commit.
