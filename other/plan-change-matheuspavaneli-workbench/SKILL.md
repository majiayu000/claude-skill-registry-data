---
name: plan-change
description: Turns .workflow/<KEY>/triage.json and the code into an audited implementation spec at .workflow/<KEY>/sdd.json. Use before writing code for a ticket, bug fix or feature.
---

# plan-change

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

## Steps

1. **Load the ticket.** `sdd get` is not it — read `.workflow/<KEY>/triage.json`.
   No triage yet? Run `triage-task` first, or work from what the user stated and
   record that in `questions`.

2. **Get the bar.** `repo profile`. It prints the preset, the repo's own
   conventions, and the gates that apply. Follow the conventions it reports;
   do not introduce a second test runner or package manager. `LOW confidence`
   means the preset is a guess nobody reviewed: say so, let the user settle it.
   Once the file list is known, `repo gates <paths>` resolves the bar those
   paths land in — in a monorepo that is not the repo's, and the audit fails a
   plan that declares a preset below it.

3. **Pick a persona** from `references/personas.md`. It shapes what counts as
   done, not the format.

   A change already on disk (a light-path ticket `finish` moved here) stays:
   plan around it, never revert it to plan from scratch.

4. **Confirm everything in the code.** Assume nothing. Every claim about this
   codebase needs a `file:line` and the text of that line, because the audit in
   step 7 reopens each one. A claim you cannot cite is a question, not a fact —
   put it in `questions`. Search with the strongest tool available and quote
   only lines you actually read: `../../shared/code-search.md`.

5. **Find the raised bar.** `repo zones <path>...` with every file you plan to
   touch. Billing, auth, user data, migrations and secrets are held to a higher
   standard whatever the preset says.

6. **Write `.workflow/<KEY>/sdd.json`.** Shape and required fields:
   `references/sdd.md`.

7. **Audit.** `sdd audit <KEY>`. It must pass. On failure, fix the plan — never
   the citation to match a wrong claim, and never proceed to implementation.
   Then `sdd render <KEY>` for the human-readable copy.

   The audit reports a **tier**. Give every `files[]` entry a `lines` estimate
   (added plus removed); an entry without one makes the plan `standard`. An
   estimated total within the repo's bound (100 by default), no critical zone
   and no bug/support ticket qualifies as `light`, which waives `steps` and
   `product` — nothing else. `impl check` measures the real diff against the
   bound, so an estimate written low only moves the failure later. Do not aim for a tier: write the plan the change
   needs and let the audit compute it. Citations, the file list, `verify` and
   `rollback` are required at every tier.

   The first audit is strict and reads the working tree, so get the line
   numbers right while the plan is still cheap to change. It records the commit
   it ran against; every later audit is anchored there, so **a plan can be
   corrected while it is being implemented**. Drifted citations are reported,
   not failed. A quote that was never in the code fails at every stage.

## Rules

- **Smallest change that achieves the objective.** Fixes and improvements to
  existing behaviour touch as little as possible. No refactor riding along, no
  abstraction for a second case that does not exist yet, no dependency that
  replaces code already in the repo.
- **List every file before touching any.** `implement-change` stops on a file
  that is not in the list, so an incomplete list is a plan that fails to run.
- **Verification is commands, not intentions.** `verify` holds the exact lines
  that will be executed, using this repo's runner. Shell is refused, so a
  command needing a variable declares it in `verify_env` (`{"PYTHONPATH": "lib"}`)
  rather than inlining `VAR=x`. Variables that change how a process loads code
  are refused there.
- **An open question is output.** A plan that guesses reads the same as a plan
  that knows; say which one it is.

Next: `implement-change` reads `sdd get <KEY> --section files|steps`.
