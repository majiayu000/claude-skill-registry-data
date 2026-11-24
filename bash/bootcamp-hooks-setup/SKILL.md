---
name: bootcamp-hooks-setup
description: Optionally install the Senzing bootcamp's hooks into this Kiro workspace, with disclosure first and explicit consent. Use when onboarding reaches the hooks step, or when the bootcamper says "install the bootcamp hooks" or "remove the bootcamp hooks".
---

# Bootcamp hooks setup

Kiro does not load hooks from a Power, so the bootcamp follows its rules as instructions (see
`../bootcamp-onboarding/host-rules.md`). Those rules are always in force, and the bootcamp is
complete and correct with no hook installed.

This skill offers to back them with hooks in the bootcamper's own workspace. Installing is
optional and always the bootcamper's choice: it writes files into their project, so nothing is
written before they have seen what will be written and said yes.

## What to tell the bootcamper

Say this much, and no more, before asking (INV-447):

- `senzing-bootcamp-session-start.json`: runs when a session starts. It tells the guide where
  the bootcamper left off, or that the bootcamp is complete. It moves recap notes left by an
  interrupted module from `docs/progress/recap_checkpoint.md` into `docs/bootcamp_recap.md`,
  creates that notes file when it is missing, and reports the state of any container the
  bootcamp started.
- `senzing-bootcamp-prompt-submit.json`: runs each time the bootcamper sends a message. It
  creates the recap notes file, `docs/progress/recap_checkpoint.md`, when it is missing. It
  notices bootcamp feedback, a note to keep, and a request for more or less detail. It reminds
  the guide to open each module the same way, to name modules by their names, and to complete
  a finished module's records.
- `senzing-bootcamp-pre-tool-use.json`: runs before the guide writes or edits a file or runs a
  shell command. It blocks a file written outside the project, a file that holds an obvious
  secret, and a command that sends its output to the system temporary directory or to
  Downloads.
- `senzing-bootcamp-post-tool-use.json`: runs after a shell command. The first time in a
  hands-on module that a program the guide wrote fails as it runs, it records that in
  `config/steer_observations.json` and reminds the guide to show the bootcamper what went
  wrong.
- `senzing-bootcamp-stop.json`: runs when the guide finishes a turn. It checks that the turn
  ended on its one question. A hook cannot re-open a finished turn on Kiro, so this one changes
  nothing, and ending on one question stays a rule the guide follows by instruction.
- It writes a few small JSON files into `.kiro/hooks/` in their project. Every file name starts
  with `senzing-bootcamp-`, and one command removes them.
- Every hook does nothing outside a bootcamp project.

## Step 1: show the plan

Run the installer with the Python interpreter the bootcamp uses for its own scripts. The
installer records that interpreter's full path in every hook, so the one you choose here is the
one the hooks use from then on.

```
<python> <this-skill-dir>/../bootcamp-onboarding/scripts/install_hooks.py plan --workspace <project-root>
```

This writes nothing. Show the bootcamper its output as it is: every file it would write, the
command each hook would run, and the other hook files it leaves untouched. Do not summarize
the paths away.

## Step 2: ask once

End the turn with exactly one question:

👉 **Would you like me to install these bootcamp hooks into your project?** (Reply yes to
install them, or no to continue without them; the bootcamp works either way.)

## Step 3: act on the answer

- **Yes:** run the same command with `install` and `--yes` in place of `plan`. Report the files
  written in one line, then return to where the bootcamper left off.
- **No:** acknowledge in one line and return to where they left off. Do not offer again in this
  bootcamp; record `hooks_offer: declined` in `config/bootcamp_preferences.yaml` so a resumed
  session does not ask again.

## Removing them

When the bootcamper asks to remove the hooks, run the installer with `remove`. It deletes only
the files it wrote, and says how many.
