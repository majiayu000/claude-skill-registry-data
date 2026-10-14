---
name: mode
description: "Show or switch the project's conformance mode between Enforced and À la carte, within the set the organization allows."
---

## User Input

You **MUST** consider the user input before proceeding (if not empty).

## Purpose

`/akka:mode` shows the project's conformance mode, or sets it. The mode is
recorded in `.akka/exit-conditions.yaml` and controls exactly one thing:
whether unmet exit conditions block shipping.

- **À la carte** — the default. The exit-condition set is **dormant** until the
  developer asks for it: only the Akka-intrinsic baseline resolves, no auditors
  are created, and nothing is captured. Once asked for, conditions are checked
  and shown but never block `/akka:ship`, which proceeds with an explicit
  override.
- **Enforced** — the full set applies from the start. `/akka:ship` refuses to
  release until every applicable condition is `green` and not stale, or covered
  by an effective waiver. You use sign-off, strike, and waive to resolve each
  `open` or `red` condition first.

Every Specify command is available in both modes; the mode changes what the
engine does on its own, not the command set. In Enforced mode the process gates
`PROC-AUDITOR-COVERAGE` and `PROC-ADEQUACY-REVIEWED` apply as usual. While the
set is dormant they do not resolve at all — there is nothing yet to have
covered or reviewed.

The organization can constrain this. A policy may set a different default and
lock it; when the mode is locked, only the org-allowed mode(s) may be set. A
locked Enforced mode cannot be dropped to À la carte to bypass the ship gate.

## Outline

1. **Parse the argument from `the user's request`.** Three cases:

   - **Empty** — this is a query. Skip to step 2 with no argument.
   - **`enforced` or `a-la-carte`** — pass through unchanged.
   - **A recognizable spelling of à la carte** — the documentation renders the
     mode as "À la carte", so accept `alacarte`, `a la carte`, `à-la-carte`,
     and `à la carte` and normalize them to `a-la-carte` before calling the
     CLI. The CLI accepts only the two canonical spellings.

   Anything else: stop and tell the user *"`/akka:mode` takes `enforced` or
   `a-la-carte`, or no argument to show the current mode."* Do not call the CLI.

2. **Invoke the CLI.** Run `akka specify mode` (with the normalized argument,
   if any) in the project directory, via the shell. With no argument it prints
   the effective mode and whether an org policy has locked it. With an argument
   it writes the mode to the project state and confirms.

3. **Answer the existing-conditions question, if it is asked.** Switching a
   project that already carries conditions and auditors to À la carte makes the
   CLI refuse and name the two options rather than decide for the developer.
   When that happens, ask the user plainly — *"This project already has checks
   set up. In À la carte they will not block shipping either way: do you want
   to keep checking them, or set them aside?"* — then rerun with
   `--exit-conditions=honor` or `--exit-conditions=ignore`. Nothing is deleted by `ignore`; the
   captured conditions stay in the project state and `--exit-conditions=honor` brings them
   back. A project with no conditions yet switches without any question.

4. **Handle an old CLI.** `akka specify mode` requires Akka CLI **3.0.70 or
   later**. Earlier versions expose only `akka specify init`, so the shell
   reports an unknown command. If that happens, do not report it as a project
   or policy problem — say the installed CLI is too old, show the installed
   version from `akka version`, and give the upgrade command for their
   platform (`winget upgrade Akka.Cli`, `brew upgrade akka`, or the curl
   installer).

5. **Report plainly.** State the mode in the user's terms — "Enforced" or
   "À la carte" — and say what it means for shipping. In À la carte, say
   whether the checks are dormant, being kept, or set aside. When the mode is
   locked by org policy, say that it is locked and by whom, and do not present
   the other mode as an option. When a set succeeded, say which mode is now in
   effect and that nothing else about the project changed.

## Key rules

- Never edit `.akka/exit-conditions.yaml` directly to change the mode. The CLI
  enforces the org policy; a hand-edit bypasses it.
- Never retry a refusal in another form. If the org policy rejected the mode,
  that is the answer — report it and stop.
- The mode does govern whether conditions are in play, but never silently. A
  dormant set is dormant because nobody asked for it, and a set aside one
  because the developer said so — describe which of the two it is rather than
  saying conditions were "turned off".
- `--exit-conditions=ignore` is not a delete. Never describe it as removing conditions or
  auditors; they persist in the project state and come back with `--exit-conditions=honor`.
- With no argument this command is read-only. Do not set a mode the user did
  not ask for, and do not "helpfully" switch modes as part of another command.
  Asking the existing-conditions question when the CLI refuses is not a mode
  switch of your own — it is completing the one the user asked for.

## Done When

- [ ] The argument was parsed from `the user's request` and either recognized as a
      query, normalized to `enforced` / `a-la-carte`, or rejected without
      calling the CLI.
- [ ] `akka specify mode` was invoked, and an unknown-command failure was
      reported as a CLI version problem with the upgrade instruction — never as
      a project or policy error.
- [ ] A refusal naming the existing conditions was turned into a plain question
      to the user, and the answer was applied by rerunning with `--exit-conditions=honor`
      or `--exit-conditions=ignore` — never decided on the user's behalf.
- [ ] The effective mode was reported plainly, along with what it means for
      shipping, and any org lock was stated as a lock rather than a choice.
