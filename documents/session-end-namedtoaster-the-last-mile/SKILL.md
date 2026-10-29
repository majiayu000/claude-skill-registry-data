---
name: session-end
description: Wrap up a working session automatically. Runs the project's checks, adds manual test items to the release checklist, records new gotchas and decisions, updates the handoff file and docs, checks progress against the current goal, commits only this session's files and pushes. Use when the user says they are done, wrapping up, or asks to end the session.
---

# Session end

Fully automatic. Do not ask wrap up questions. Do the work, then finish with a
short summary. Read the **Settings** table in the project's rules file
(`CLAUDE.md` or `AGENTS.md`) first; it says which check command to run, which
docs to review and where to push. If there is no settings table, use the defaults
in brackets below and say so in the summary.

## 1. Run the checks

Run the check command [`npm run check`, or lint, typecheck and tests]. Fix what
fails and run it again until it is clean. Do not report the session as done while
anything is red.

These are the automated checks only. Do not hand test features now; that is
batched into the release checklist in step 2.

## 2. Release checklist

If this session changed anything a person has to see on a device or in a browser
(a screen, layout, animation, navigation path, purchase, notification, deep link,
or anything that behaves differently in a release build), add an item to **Pending** in
`RELEASE_TEST_CHECKLIST.md`:

- **Surface:** where it is.
- **Steps:** how to reach it and what to do.
- **Expected:** the result.
- `_(added YYYY-MM-DD)_`

Tick any item verified this session, by the user or by you, with the evidence
written into the item. Never clear the file wholesale. Never add an item that no
available device can satisfy. For a web only project, the release is the deploy:
word each item so it is checked on the live site once the change is deployed.
Skip this step if nothing user facing changed.

## 3. Gotchas and decisions

If something this session cost real time (it took more than one attempt to
diagnose, or it would have caught the next person out), add a dated entry to
**Gotchas** in the rules file: the symptom, the cause, the fix and the general
rule. Normal tool behaviour that worked as expected is not a gotcha. Most sessions
add none. If the user made a decision
that should not be re-litigated, add it to **Standing decisions** with the date and
one line of why. Keep entries specific; a vague gotcha helps nobody.

**Skill problems.** If a skill from The Last Mile did the wrong thing this session
(a step that misled you, a missing step, a wrong default), and the user already
asked for it to be fixed, run the improve-skill skill now. Otherwise list it in the
summary under **Skill problems**, one line each: the skill, what it did, what it
should have done. A project setting that was missing is a rules file fix, not a
skill problem.

## 4. Docs

Review each doc listed in the settings [`CURRENT_WORK.md`, `BACKLOG.md`,
`FEATURES.md`, `docs/ALGORITHMS.md`]. Update only what this session changed. Skip
any listed doc that does not exist; do not create it just because it is listed.

Always rewrite `CURRENT_WORK.md`: status, where things stand, next steps, and
anything waiting on someone. Keep it under 80 lines.

If a doc claims something is outstanding and you know it is done, correct it and
write the date. Stale status docs send people chasing finished work.

## 5. Goals

Read `GOALS.md`.

- **No file, or no current cycle:** say "No current goal set." in the summary, once,
  and move on.
- **Current cycle:** tick any must do finished this session. If the end date is near
  and must dos are open, say so plainly in one line.
- **Cycle ended:** give one short reminder in the summary that it is time to close
  this cycle and set the next one with the set-goals skill. Do not block or nag
  beyond that one line.

## 6. Commit only this session's files

The user may run several sessions in the same repo at once, sharing one working
tree. A broad commit would sweep another session's changes into yours.

1. Build the file list from your own edits in this conversation, including the doc
   updates above. Do not build it from `git status` alone.
2. Run `git status --short` and confirm each file on your list is modified or new.
   Files that are dirty but not on your list belong to someone else; leave them.
3. For each file, run `git diff -- <file>` and compare every hunk with your own
   edits. A file where every hunk is yours gets staged whole. A file that also
   has hunks you did not write (someone else's edits, or edits that were there
   before the session) gets staged one hunk at a time, so their edits stay in
   the working tree uncommitted:
   `git add -- <whole file> <whole file> ...`
   `git diff -- <shared file> > /tmp/full.patch`, then copy it to
   `/tmp/own.patch` keeping the `diff`/`---`/`+++` header and only your hunks
   (each starts at an `@@` line), then `git apply --cached /tmp/own.patch`.
   If one hunk mixes your lines with someone else's, or `git apply` refuses the
   patch, stop and tell the user instead of committing over their work.
   Never `git add -A`, `git add .`, `git commit -a`, or `git add` on a shared file.
4. Run `git diff --cached --name-only` and confirm it lists exactly your files.
   Unstage anything else with `git restore --staged -- <file>`. Then commit what
   is staged: `git commit -m "<plain sentence describing the change>"`. Do not
   pass paths to `git commit`: with paths, git commits the whole working copy of
   those files and sweeps in the edits you just left out.
5. Run `git show HEAD` and confirm it holds only your changes, and `git diff`
   to confirm the edits you left out are still there. If something else got in,
   undo with `git reset --soft HEAD~1` and commit again correctly.

## 7. Push and confirm the checks pass

Push to the destination in the settings [a branch].

- **No remote:** skip the push and say so in the summary.
- **Push rejected because the remote moved:** run `git pull --rebase`, then push
  again. Only your own unpushed commits get replayed. Never force push and never
  rewrite commits that are already on the remote. If the rebase hits a conflict,
  stop and tell the user.

Then check whether the repo runs checks on push (for example a `.github/workflows/`
folder). If it does not, skip this part. If it does, find the run for your commit
(`gh run list` and `gh run watch` when the GitHub CLI is installed, otherwise a
GitHub tool if one is connected) and wait for it. If it fails, read the actual
failure, fix it, commit the fix the same way and push again. Stop after three
failed attempts and tell the user what is still failing. If you cannot see the run
at all, say so in the summary instead of claiming it passed.

## 8. Summary

Finish with a short summary, in the voice the rules file asks for. Keep any prose
to a line or two, then end with one table, so the next action is visible at a
glance. Rows that need the user come first and say so plainly; a question for the
user is its own row, never buried in a paragraph.

| Item | Category | Next action |
| --- | --- | --- |
| Rotate the API key | Needs you | Open the dashboard and create a new key |
| Profile screen fix | Done | None |

Categories: Needs you, Decision (the user picks), Done, FYI. The rows cover:

- What was done this session.
- The goal line from step 5.
- Whether a version bump is due, and which kind (patch for fixes, minor for new
  features), if the app ships to a store.
- Skill problems from step 3, if any, with the offer to fix them.
- Anything the user needs to do by hand.
