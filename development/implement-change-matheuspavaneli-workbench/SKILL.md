---
name: implement-change
description: Executes an audited plan from .workflow/<KEY>/sdd.json, holding the diff to the files it lists, then verifies it into .workflow/<KEY>/evidence.md. Use to carry out a plan, after plan-change.
---

# implement-change

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

## Steps

1. **Read the plan's own slices**, not the whole document:
   `sdd get <KEY> --section steps` and `--section files`.
   No `sdd.json`? Run `plan-change` first. A failed audit blocks every command
   here by design — fix the plan, do not work around it.

   Picking work back up mid-way? `status <KEY>` says which planned files are
   already changed and what is left, without re-reading the plan.

2. **Check where you are.** `flow show` reports the branch this work starts
   from, whether the current branch is protected, and any validation branch the
   commits will later be carried onto. `flow start <KEY> --title "..."` prints
   the branch name and base to use.

3. **Implement one step at a time**, in order, touching only the listed files.
   Follow the repo's existing patterns. Nothing tidied, renamed or upgraded
   along the way: the plan's file list is the scope, and it was reviewed.

4. **Write the tests the plan named.** `sdd get <KEY> --section tests`. Each
   entry says what must hold — assert that, not that a function was called.
   `impl verify` fails, naming it, on any `target` the branch never changed.

5. **Check the scope.** `impl check <KEY>` after each step or two: planned files
   `ok`/`pending`, `companion` (a test, lockfile or generated file tied to a
   planned one), `other` (another plan's), `overlap`. It fails on a file nothing
   accounts for; with hooks on, that edit is refused before it lands.

6. **Verify.** `impl verify <KEY>` runs the plan's `verify` commands and writes
   `.workflow/<KEY>/evidence.md`. It refuses anything that is not a known test,
   build or lint runner — run those yourself and say so. The first time a
   command appears in a checkout nothing runs: `approve <KEY>` then shows the
   commands and a token. Show it to the user; never approve on their behalf.
   The evidence is bound to the tree it saw, so verify last, then commit.
   For a bug fix, `impl verify <KEY> --regression`: each `regression` target
   runs on the commit the branch left, with the new tests carried in, and must
   fail there, then pass here. Report the result either way.

7. **Report honestly.** If verification fails, say so with the failing line.
   Fix the code, never the evidence.

Do not re-run `sdd audit` to confirm your work: it checks the plan, not the
code. Re-run it when you **change** the plan — that now passes, reporting which
citations have drifted. `impl check` and `impl verify` are the checks for this
stage.

## When the plan is wrong

It happens, and it is not a reason to improvise. Stop, say what the plan assumed
and what the code actually does, update `sdd.json`, re-run `sdd audit <KEY>`,
then continue. A deviation that goes through the plan is a correction; one that
does not is an unreviewed change wearing a reviewed plan's name.

A missed file: `sdd amend <KEY> <path> --why "..." --lines N` (`--new` to
create it) re-audits in place; if the tier rises, add what the audit asks.

## Rules

- **Smallest diff that satisfies the step.** No opportunistic refactors.
- **A file outside the plan stops the work.** Not a warning — `impl check`
  exits non-zero, and the critical zones it names raise the bar further.
- **Never weaken a test to make it pass.** If an existing test now fails, either
  the change is wrong or the test encoded the old behaviour; say which, with the
  file and line.

Next: `write-commit`, then `draft-pr`. If the flow has a validation branch,
`flow carry <KEY> --to <branch>` lists the commits to cherry-pick, oldest first,
measured against `origin/<source>` after a fetch. It prints the commands; pass
`--execute` only when the user asked you to run them.
